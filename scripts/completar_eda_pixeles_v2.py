"""Una ejecución local para completar el EDA de píxeles v2 sin abrir la reserva.
Dependencias: numpy, Pillow, scikit-learn. No entrena clasificadores de núcleos.
"""
import argparse,csv,hashlib,json,os,platform,time,zipfile
from pathlib import Path
from collections import Counter
os.environ.setdefault('OMP_NUM_THREADS','1')
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import numpy as np
import sklearn, PIL
from PIL import Image
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score,balanced_accuracy_score,confusion_matrix

EXPECTED='623adf36520751addc324e44cd1b89d95e47842e53cda494914c0248a8be86d4'
CLASSES=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']
FEATURES=['R_media','G_media','B_media','R_sd','G_sd','B_sd','saturacion_media','fondo_fraccion','laplaciano_var','entropia_gris']

def write_csv(path,rows):
    if not rows:return
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def features(a):
    x=a.astype(np.float64)/255
    gray=x@np.array([.299,.587,.114]);mx=x.max(2);mn=x.min(2)
    sat=np.divide(mx-mn,mx,out=np.zeros_like(mx),where=mx>0)
    lap=-4*gray[1:-1,1:-1]+gray[:-2,1:-1]+gray[2:,1:-1]+gray[1:-1,:-2]+gray[1:-1,2:]
    hist=np.histogram(gray,bins=32,range=(0,1))[0];p=hist[hist>0]/hist.sum()
    return np.r_[x.mean((0,1)),x.std((0,1)),sat.mean(),(x.min(2)>235/255).mean(),lap.var(),-(p*np.log2(p)).sum()]

def dhash(a):
    z=np.asarray(Image.fromarray(a).convert('L').resize((9,8),Image.Resampling.LANCZOS))
    return np.uint64(sum(int(v)<<i for i,v in enumerate((z[:,1:]>z[:,:-1]).flat)))

def cross_candidates(hashes,rows,out):
    train=np.array([i for i,r in enumerate(rows) if r['particion']=='train']);val=np.array([i for i,r in enumerate(rows) if r['particion']=='validation'])
    lut=np.array([i.bit_count() for i in range(256)],dtype=np.uint8);candidate=[];total=0
    for start in range(0,len(train),128):
        block=train[start:start+128]
        xor=np.bitwise_xor(hashes[block,None],hashes[val][None,:])
        dist=lut[xor.view(np.uint8).reshape(len(block),len(val),8)].sum(2)
        ii,jj=np.nonzero(dist<=4);total+=len(ii)
        for i,j in zip(ii,jj):
            if len(candidate)<500:
                a,b=rows[block[i]],rows[val[j]]
                candidate.append(dict(archivo_train=a['archivo'],archivo_validation=b['archivo'],paciente_train=a['paciente'],paciente_validation=b['paciente'],distancia=int(dist[i,j]),clase_train=a['clase'],clase_validation=b['clase']))
    write_csv(out/'candidatos_similares.csv',candidate)
    return {'metodo':'dHash 64 bits, distancia Hamming <=4, entre train y validation','pares_examinados':int(len(train)*len(val)),'candidatos':total,'filas_exportadas':len(candidate),'limite_exportacion':500,'interpretacion':'Candidatos a inspección visual; no prueba duplicación. No detecta todas las rotaciones, escalas o solapamientos. No elimina imágenes.'}

def cv_diagnostic(X,rows,target):
    # Una observación por paciente: evita que muchos recortes del mismo sujeto dominen el diagnóstico.
    patients=sorted({r['paciente'] for r in rows});A=[];y=[]
    for patient in patients:
        ix=[i for i,r in enumerate(rows) if r['paciente']==patient]
        A.append(np.median(X[ix],axis=0));y.append(rows[ix[0]][target])
    A=np.array(A);y=np.array(y);groups=np.array(patients)
    if target=='tss':
        n=Counter(y);eligible={k for k,v in n.items() if v>=3};keep=np.array([v in eligible for v in y])
        A,y,groups=A[keep],y[keep],groups[keep]
    classes=sorted(set(y));n=Counter(y)
    if len(classes)<2 or min(n.values())<3:return {'estado':'No estimable: menos de dos clases con tres pacientes'}
    splitter=StratifiedGroupKFold(n_splits=3,shuffle=True,random_state=4101)
    pred=np.empty(len(y),dtype=object);prob=np.zeros((len(y),len(classes)));fold_rows=[]
    for fold,(tr,va) in enumerate(splitter.split(A,y,groups),1):
        assert not(set(groups[tr])&set(groups[va]))
        if set(y[tr])!=set(classes):return {'estado':'No estimable: un pliegue de entrenamiento carece de una clase'}
        model=make_pipeline(StandardScaler(),LogisticRegression(C=1,max_iter=2000,class_weight='balanced',random_state=4101))
        model.fit(A[tr],y[tr]);pred[va]=model.predict(A[va]);p=model.predict_proba(A[va]);order=list(model[-1].classes_)
        for j,c in enumerate(classes):prob[va,j]=p[:,order.index(c)]
        fold_rows.extend({'paciente':str(groups[i]),'fold':fold,'real':str(y[i]),'prediccion':str(pred[i])} for i in va)
    result={'estado':'Calculado','unidad':'Paciente; mediana de descriptores de sus recortes','n_pacientes':len(y),'clases':classes,'balanced_accuracy':float(balanced_accuracy_score(y,pred)),'confusion':confusion_matrix(y,pred,labels=classes).tolist(),'validacion':'3 pliegues estratificados por etiqueta y agrupados por paciente; escalado dentro de cada entrenamiento','configuracion':'Regresión logística C=1, pesos balanceados, sin búsqueda','predicciones':fold_rows}
    if target=='particion':result['auc_validation']=float(roc_auc_score(y=='validation',prob[:,classes.index('validation')]))
    if target=='tss':result['restriccion']='Solo TSS de entrenamiento con >=3 pacientes; no mide transferencia a centros nuevos.'
    return result

def run(root,out):
    raw=(root/'manifiesto.csv').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED:raise ValueError('El manifiesto no coincide con la versión v2 verificada')
    allrows=list(csv.DictReader(raw.decode().splitlines()))
    rows=[r for r in allrows if r['particion'] in ('train','validation')]
    if Counter(r['particion'] for r in rows)!=Counter(train=14539,validation=2049):raise ValueError('Conteos inesperados')
    out.mkdir(parents=True,exist_ok=False)
    results=[];X=[];hashes=[];hist={};sum_rgb=np.zeros(3);sum_sq=np.zeros(3);pixels=0
    for i,r in enumerate(rows):
        path=(root/r['archivo']).resolve()
        if not path.is_relative_to(root.resolve()):raise ValueError('Ruta fuera de datos')
        with Image.open(path) as im:
            im.load()
            if im.mode!='RGB' or im.size!=(128,128):raise ValueError('Formato inesperado: '+str(path))
            a=np.array(im)
        if hashlib.sha256(a.tobytes()).hexdigest()!=r['sha_pixeles']:raise ValueError('Píxeles modificados: '+str(path))
        f=features(a);h=dhash(a);X.append(f);hashes.append(h)
        results.append({**{k:r[k] for k in ('paciente','tss','particion','clase','archivo')},**dict(zip(FEATURES,map(float,f))),'dhash':f'{int(h):016x}'})
        key=(r['particion'],r['clase']);hist.setdefault(key,np.zeros((3,32),dtype=np.int64))
        for c in range(3):hist[key][c]+=np.histogram(a[:,:,c],bins=32,range=(0,256))[0]
        if r['particion']=='train':
            z=a.astype(np.float64)/255;sum_rgb+=z.sum((0,1));sum_sq+=(z*z).sum((0,1));pixels+=128*128
        if (i+1)%1000==0:print('Imágenes verificadas:',i+1,'/',len(rows),flush=True)
    write_csv(out/'descriptores_recortes.csv',results)
    histrows=[dict(particion=k[0],clase=k[1],canal='RGB'[c],bin_inferior=b*8,bin_superior_exclusivo=(b+1)*8,pixeles=int(v[c,b])) for k,v in hist.items() for c in range(3) for b in range(32)]
    write_csv(out/'histogramas.csv',histrows)
    X=np.array(X);hashes=np.array(hashes,dtype=np.uint64)
    mean=sum_rgb/pixels;sd=np.sqrt(np.maximum(0,sum_sq/pixels-mean**2))
    print('Calculando diagnósticos por paciente y similitud entre particiones...',flush=True)
    domain=cv_diagnostic(X,rows,'particion');ix=[i for i,r in enumerate(rows) if r['particion']=='train'];site=cv_diagnostic(X[ix],[rows[i] for i in ix],'tss')
    similar=cross_candidates(hashes,rows,out)
    report={'estado':'EDA_PIXELES_COMPLETADO','fecha_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'manifiesto_sha256':EXPECTED,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'python':platform.python_version(),'numpy':np.__version__,'scikit_learn':sklearn.__version__,'Pillow':PIL.__version__,'recortes':len(rows),'normalizacion_train':{'media_RGB_0_1':mean.tolist(),'sd_RGB_0_1':sd.tolist(),'pixeles':pixels,'uso':'Estimaciones de entrenamiento; no se aplica ni decide normalización de tinción'},'diagnostico_dominio':domain,'diagnostico_sitio':site,'similitud':similar,'limites':['Descriptores de color y textura no prueban calidad diagnóstica ni desenfoque.','Predicción de partición puede reflejar composición de clases, pacientes, tejido o adquisición; no identifica por sí sola la causa.','Predicción de TSS muestra señal disponible, no que la CNN vaya a utilizarla.','No se abre ninguna imagen de reserva; no se entrena ni selecciona un modelo de clasificación nuclear.']}
    (out/'resumen.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))
    archive=out.with_suffix('.zip')
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for f in out.iterdir():z.write(f,f.name)
    print('COMPLETADO. Adjunta este único ZIP:',archive,flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--datos',type=Path,required=True);ap.add_argument('--salida',type=Path,required=True);a=ap.parse_args()
    run(a.datos.expanduser().resolve(),a.salida.expanduser().resolve())
if __name__=='__main__':main()
