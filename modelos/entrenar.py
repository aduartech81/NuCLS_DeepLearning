"""Piloto exploratorio NuCLS. No abre test/reserva ni selecciona modelos definitivos."""
import argparse, csv, hashlib, json, math, os, platform, random, sys, time, zipfile
from pathlib import Path
from collections import Counter
import numpy as np
import torch
import torchvision
import PIL
from torch import nn
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from base_modelos import build, CLASSES

EXPECTED = 'd287767a890607533e87ef4958612ceb8a4d77738af698f2e06b26e5a828f9de'
ROOT = Path.home() / 'Desktop/Proyecto_Deep_Learning'
DEFAULT_DATA = ROOT / 'NuCLS_DL_Entregable1/data/piloto_interior128/20261105_225210'

def save_json(path, data):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False))
    tmp.replace(path)

def csv_write(path, rows):
    if not rows: return
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def scores(y, p):
    cm = np.zeros((3, 3), dtype=int)
    np.add.at(cm, (np.asarray(y), np.asarray(p)), 1)
    tp = np.diag(cm); support = cm.sum(1); predicted = cm.sum(0)
    precision = np.divide(tp, predicted, out=np.zeros(3), where=predicted > 0)
    recall = np.divide(tp, support, out=np.zeros(3), where=support > 0)
    f1 = np.divide(2*precision*recall, precision+recall, out=np.zeros(3), where=precision+recall > 0)
    return dict(macro_f1=float(f1.mean()), accuracy=float(tp.sum()/max(cm.sum(), 1)),
                balanced_accuracy=float(recall.mean()), confusion=cm.tolist(),
                clases=[dict(clase=c, precision=float(precision[i]), recall=float(recall[i]),
                             f1=float(f1[i]), soporte=int(support[i])) for i,c in enumerate(CLASSES)])

def read_data(root):
    raw = (root/'manifiesto.csv').read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXPECTED:
        raise ValueError('El manifiesto no coincide con el dataset auditado; no se inicia entrenamiento.')
    rows = list(csv.DictReader(raw.decode().splitlines()))
    groups = {s:[r for r in rows if r['particion']==s and r['estado']=='incluida']
              for s in ('entrenamiento','validacion')}
    if [len(groups[s]) for s in groups] != [14428,3571]:
        raise ValueError('Conteos distintos de los auditados.')
    for key in ('paciente', 'sha_pixeles'):
        if {r[key] for r in groups['entrenamiento']} & {r[key] for r in groups['validacion']}:
            raise ValueError('Solapamiento entre particiones: '+key)
    if [len({r['paciente'] for r in groups[s]}) for s in groups] != [79,19]:
        raise ValueError('Conteos de pacientes distintos.')
    for s, rr in groups.items():
        for i,r in enumerate(rr):
            if r['clase'] not in CLASSES: raise ValueError('Clase inesperada')
            p = (root/r['archivo']).resolve()
            if not p.is_relative_to(root.resolve()): raise ValueError('Ruta fuera del dataset')
            with Image.open(p) as im:
                if im.mode!='RGB' or im.size!=(128,128): raise ValueError('Formato incorrecto: '+str(p))
                digest = hashlib.sha256(np.asarray(im).tobytes()).hexdigest()
            if digest != r['sha_pixeles']: raise ValueError('Imagen modificada: '+str(p))
            if i%2000==0: print('Verificando',s,i,'/',len(rr),flush=True)
    return groups

class Crops(Dataset):
    def __init__(self, root, rows, augment=False): self.root,self.rows,self.augment=root,rows,augment
    def __len__(self): return len(self.rows)
    def __getitem__(self, i):
        r=self.rows[i]
        with Image.open(self.root/r['archivo']) as im: x=np.asarray(im).copy()
        if self.augment:
            x=np.rot90(x, random.randrange(4))
            if random.random()<.5: x=x[:,::-1]
        return torch.from_numpy(x.copy()).permute(2,0,1).float()/255, CLASSES.index(r['clase'])

def seed_all(seed):
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(seed)

def synchronize(device):
    if device.type=='cuda': torch.cuda.synchronize()
    elif device.type=='mps': torch.mps.synchronize()

def evaluate(model, loader, device):
    model.eval(); probs=[]; ys=[]; loss=0.; n=0
    with torch.no_grad():
        for x,y in loader:
            logits=model(x.to(device)); ll=nn.functional.cross_entropy(logits,y.to(device))
            if not torch.isfinite(ll): raise ValueError('Pérdida de validación no finita')
            probs.extend(logits.softmax(1).cpu().tolist());ys.extend(y.tolist())
            loss+=float(ll)*len(y);n+=len(y)
    a=np.asarray(probs)
    if not np.isfinite(a).all() or not np.allclose(a.sum(1),1,atol=1e-5): raise ValueError('Probabilidades inválidas')
    return loss/n, np.asarray(ys), a

def archive(out):
    target=out.parent/(out.name+'_RESULTADOS.zip'); tmp=target.with_suffix('.tmp')
    with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file() and p.suffix in ('.json','.csv','.html','.txt'):
                z.write(p,p.relative_to(out))
    tmp.replace(target)
    return target

def summary(out):
    results=[json.loads(p.read_text()) for p in sorted(out.glob('*/resultado.json'))]
    table=[]
    for name in ('cnn_local','resnet18','mobilenet_v2'):
        rr=[r for r in results if r['modelo']==name]
        if not rr: continue
        values=np.array([r['validacion']['macro_f1'] for r in rr])
        sd=float(values.std(ddof=1)) if len(values)>1 else None
        table.append(dict(modelo=name,ejecuciones=len(rr),macro_f1_media=float(values.mean()),
                          macro_f1_sd=sd,cv=sd/float(values.mean()) if sd is not None and values.mean()>0 else None))
    csv_write(out/'resumen_modelos.csv',table)
    body='<h1>Piloto exploratorio NuCLS</h1><p>Validación utilizada para elegir época. No constituye evaluación final ni selección bibliográfica cerrada.</p>'
    body+='<p>Las semillas miden variabilidad de entrenamiento; no son pacientes independientes.</p>'
    for r in results:
        history=json.loads((out/(r['modelo']+'_'+str(r['semilla']))/'historia.json').read_text())
        points=' '.join(f'{40+i*580/max(len(history)-1,1):.1f},{210-180*h["val_macro_f1"]:.1f}' for i,h in enumerate(history))
        body+=f'<h2>{r["modelo"]} — semilla {r["semilla"]}</h2><p>Mejor macro-F1: {r["validacion"]["macro_f1"]:.4f}; época {r["mejor_epoca"]}. Macro-F1 por época (0–1):</p>'
        body+=f'<svg viewBox="0 0 660 240" width="660"><path d="M40 20V210H630" fill="none" stroke="gray"/><text x="5" y="30">1</text><text x="5" y="210">0</text><polyline points="{points}" fill="none" stroke="teal" stroke-width="3"/></svg>'
    (out/'INFORME.html').write_text('<!doctype html><meta charset="utf-8"><style>body{font-family:Arial;max-width:900px;margin:40px auto;line-height:1.6}svg{max-width:100%}</style>'+body)
    return archive(out)

def run_one(name, seed, groups, args, device):
    run=args.salida/(name+'_'+str(seed));run.mkdir(exist_ok=True)
    if (run/'resultado.json').exists():
        print('Ya completado:',name,seed,flush=True);return
    seed_all(seed);model=build(name).to(device)
    optimizer=torch.optim.Adam(model.parameters(),lr=args.lr)
    gen=torch.Generator().manual_seed(seed)
    tr=DataLoader(Crops(args.datos,groups['entrenamiento'],True),batch_size=args.batch,shuffle=True,generator=gen,num_workers=0)
    va=DataLoader(Crops(args.datos,groups['validacion']),batch_size=args.batch,num_workers=0)
    history=[];best=-1.;best_epoch=0;bad=0;start_epoch=1
    checkpoint=run/'ultimo.pt'
    if checkpoint.exists():
        # Solo checkpoints propios de esta carpeta, nunca archivos de terceros.
        ck=torch.load(checkpoint,map_location='cpu',weights_only=False)
        model.load_state_dict(ck['model']);optimizer.load_state_dict(ck['optimizer'])
        torch.save(ck['best_model'],run/'mejor.pt')
        # Adam conserva su contador en CPU; sus momentos deben estar junto al parámetro.
        for state in optimizer.state.values():
            for key in ('exp_avg','exp_avg_sq','max_exp_avg_sq'):
                if key in state: state[key]=state[key].to(device)
        history=ck['history'];best=ck['best'];best_epoch=ck['best_epoch'];bad=ck['bad'];start_epoch=ck['epoch']+1
        random.setstate(ck['python_rng']);np.random.set_state(ck['numpy_rng']);torch.set_rng_state(ck['torch_rng'])
        gen.set_state(ck['loader_rng'])
        if device.type=='cuda':torch.cuda.set_rng_state_all(ck['device_rng'])
        elif device.type=='mps':torch.mps.set_rng_state(ck['device_rng'])
        print('Reanudando',name,seed,'época',start_epoch,flush=True)
    for epoch in range(start_epoch,args.epocas+1):
        if bad>=args.paciencia and epoch>args.min_epocas: break
        synchronize(device);tic=time.perf_counter();model.train();train_loss=0.;n=0;correct=0
        for step,(x,y) in enumerate(tr,1):
            optimizer.zero_grad(set_to_none=True);logits=model(x.to(device));target=y.to(device)
            loss=nn.functional.cross_entropy(logits,target)
            if not torch.isfinite(loss):raise ValueError('Pérdida de entrenamiento no finita')
            loss.backward();norm=nn.utils.clip_grad_norm_(model.parameters(),5.,error_if_nonfinite=True)
            optimizer.step();train_loss+=float(loss.detach())*len(y);n+=len(y)
            correct+=int((logits.argmax(1)==target).sum())
            if step%100==0:print(name,seed,'época',epoch,'lote',step,'/',len(tr),flush=True)
        vl,y,prob=evaluate(model,va,device);met=scores(y,prob.argmax(1));synchronize(device)
        secs=time.perf_counter()-tic
        row=dict(epoca=epoch,train_loss=train_loss/n,train_accuracy=correct/n,val_loss=vl,
                 val_macro_f1=met['macro_f1'],val_accuracy=met['accuracy'],segundos=secs,
                 clases_predichas=len(np.unique(prob.argmax(1))),prob_std_media=float(prob.std(0).mean()))
        history.append(row)
        if met['macro_f1']>best:
            best=met['macro_f1'];best_epoch=epoch;bad=0
            tmp=run/'mejor.tmp';torch.save(model.state_dict(),tmp);tmp.replace(run/'mejor.pt')
        else:bad+=1
        print(f'{name} semilla={seed} época={epoch} loss={train_loss/n:.4f} val_F1={met["macro_f1"]:.4f} tiempo={secs:.1f}s',flush=True)
        if row['clases_predichas']==1:print('AVISO: predice una sola clase; se registra para revisión, no se oculta.',flush=True)
        state=dict(model=model.state_dict(),optimizer=optimizer.state_dict(),epoch=epoch,history=history,
                   best_model=torch.load(run/'mejor.pt',map_location='cpu',weights_only=True),
                   best=best,best_epoch=best_epoch,bad=bad,python_rng=random.getstate(),numpy_rng=np.random.get_state(),
                   torch_rng=torch.get_rng_state(),loader_rng=gen.get_state(),
                   device_rng=torch.cuda.get_rng_state_all() if device.type=='cuda' else torch.mps.get_rng_state() if device.type=='mps' else None)
        tmp=run/'ultimo.tmp';torch.save(state,tmp);tmp.replace(checkpoint)
        save_json(run/'historia.json',history);csv_write(run/'curvas.csv',history)
        archive(args.salida)
    model.load_state_dict(torch.load(run/'mejor.pt',map_location=device,weights_only=True))
    vl,y,prob=evaluate(model,va,device);pred=prob.argmax(1)
    records=[dict(paciente=r['paciente'],archivo=r['archivo'],clase_real=CLASSES[int(y[i])],
                  clase_predicha=CLASSES[int(pred[i])],p_tumor=float(prob[i,0]),p_linfocito=float(prob[i,1]),p_estroma=float(prob[i,2]))
             for i,r in enumerate(groups['validacion'])]
    csv_write(run/'predicciones_validacion.csv',records)
    patient_rows=[]
    for patient in sorted({r['paciente'] for r in records}):
        ix=[i for i,r in enumerate(records) if r['paciente']==patient];m=scores(y[ix],pred[ix])
        patient_rows.append(dict(paciente=patient,n=len(ix),macro_f1_tres_clases=m['macro_f1'],accuracy=m['accuracy'],clases_reales=len(set(y[ix]))))
    csv_write(run/'metricas_por_paciente.csv',patient_rows)
    result=dict(modelo=name,semilla=seed,mejor_epoca=best_epoch,epocas_ejecutadas=len(history),
                parametros=sum(p.numel() for p in model.parameters()),segundos=sum(r['segundos'] for r in history),
                validacion=scores(y,pred),val_loss=vl,estado='COMPLETO_EXPLORATORIO')
    save_json(run/'resultado.json',result);print('Evidencia:',summary(args.salida),flush=True)
    del model,optimizer,tr,va
    if device.type=='mps':torch.mps.empty_cache()
    elif device.type=='cuda':torch.cuda.empty_cache()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--datos',type=Path,default=DEFAULT_DATA)
    p.add_argument('--salida',type=Path,default=ROOT/'NuCLS_Piloto_V1/resultados')
    p.add_argument('--epocas',type=int,default=25);p.add_argument('--batch',type=int,default=32)
    p.add_argument('--paciencia',type=int,default=5);p.add_argument('--min-epocas',type=int,default=5)
    p.add_argument('--lr',type=float,default=.001)
    p.add_argument('--device',choices=['auto','cpu','mps','cuda'],default='auto')
    args=p.parse_args()
    if min(args.epocas,args.batch,args.paciencia,args.min_epocas)<=0 or args.lr<=0:p.error('Parámetros positivos requeridos')
    args.datos=args.datos.expanduser().resolve();args.salida=args.salida.expanduser().resolve()
    if args.salida.is_relative_to(args.datos):p.error('La salida debe estar fuera de los datos')
    device=torch.device(args.device if args.device!='auto' else 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
    torch.set_num_threads(2)
    if device.type=='cuda':torch.backends.cudnn.benchmark=False;torch.backends.cudnn.deterministic=True
    torch.use_deterministic_algorithms(True,warn_only=True)
    args.salida.mkdir(parents=True,exist_ok=True)
    config={k:str(v) if isinstance(v,Path) else v for k,v in vars(args).items()}
    config.update(tipo='PILOTO_EXPLORATORIO_SELECCION_BIBLIOGRAFICA_PENDIENTE',device=str(device),
                  modelos=['cnn_local','resnet18','mobilenet_v2'],semillas=list(range(4101,4106)),
                  manifest_sha256=EXPECTED,preentrenamiento=False,preprocesamiento='RGB /255; rotaciones 90 y flip horizontal solo train',
                  perdida='cross_entropy sin ponderación',grad_clip=5,metrica_primaria='macro_f1',delta_operativo=.02,
                  python=sys.version,torch=torch.__version__,torchvision=torchvision.__version__,numpy=np.__version__,pillow=PIL.__version__,platform=platform.platform(),
                  fuente_sha256=hashlib.sha256(Path(__file__).read_bytes()+(Path(__file__).parent/'base_modelos.py').read_bytes()).hexdigest())
    cfg=args.salida/'configuracion.json'
    if cfg.exists() and json.loads(cfg.read_text())!=config:
        raise ValueError('Configuración/entorno cambió: usa otra carpeta --salida para no mezclar corridas.')
    save_json(cfg,config)
    try:
        groups=read_data(args.datos)
        save_json(args.salida/'control_datos.json',{s:dict(n=len(rr),pacientes=len({r['paciente'] for r in rr}),clases=dict(Counter(r['clase'] for r in rr))) for s,rr in groups.items()})
        print('Datos verificados. Dispositivo:',device,'15 corridas exploratorias. Ctrl+C conserva épocas terminadas.',flush=True)
        for seed in range(4101,4106):
            for name in config['modelos']:run_one(name,seed,groups,args,device)
        print('15 CORRIDAS COMPLETADAS. Adjunta:',summary(args.salida),flush=True)
    except BaseException:
        import traceback
        (args.salida/'ultima_interrupcion.txt').write_text(traceback.format_exc())
        print('Evidencia parcial:',archive(args.salida),flush=True)
        raise

if __name__=='__main__':main()
