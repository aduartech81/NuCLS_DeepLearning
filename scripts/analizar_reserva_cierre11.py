import csv,json,hashlib,itertools
from pathlib import Path
import numpy as np
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--entrada',type=Path,required=True,help='Carpeta del ZIP de cierre extraído')
ap.add_argument('--zip',type=Path,required=True,help='ZIP original para huella')
ap.add_argument('--salida',type=Path,required=True)
args=ap.parse_args()
R=args.entrada; O=args.salida; O.mkdir(parents=True,exist_ok=True)
models=['softmaxcnn_bn','densenet121','resnet50']; classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']
freeze=json.loads((R/'evaluacion_reserva_fijada.json').read_text()); mats=[]; reference=None
for m in models:
 ms=[]
 for seed in range(6101,6112):
  rows=list(csv.DictReader((R/'reserva'/f'{m}_{seed}.csv').open()))
  ident=[(r['paciente'],r['archivo'],r['clase_real']) for r in rows]
  if reference is None: reference=ident
  assert ident==reference and len(rows)==969 and len(set(r['archivo'] for r in rows))==969
  patients=sorted(set(r['paciente'] for r in rows)); assert len(patients)==6
  cm=np.zeros((6,3,3),dtype=int)
  for r in rows:
   prob=np.array([float(r[k]) for k in ['p_tumor','p_linfocito','p_estroma']]); assert np.isfinite(prob).all() and abs(prob.sum()-1)<1e-5
   assert classes[prob.argmax()]==r['clase_predicha']
   cm[patients.index(r['paciente']),classes.index(r['clase_real']),classes.index(r['clase_predicha'])]+=1
  saved=json.loads((R/'reserva'/f'{m}_{seed}.json').read_text())
  assert saved['checkpoint_sha256']==freeze['sha256_checkpoints'][f'{m}_{seed}']
  assert cm.sum(axis=0).tolist()==saved['metricas']['confusion']; ms.append(cm)
 mats.append(ms)
a=np.array(mats)
def f1(cm):
 den=cm.sum(axis=-1)+cm.sum(axis=-2); num=2*np.diagonal(cm,axis1=-2,axis2=-1)
 return np.divide(num,den,out=np.zeros_like(num,dtype=float),where=den>0).mean(axis=-1)
observed=f1(a.sum(axis=2)); summary=list(csv.DictReader((R/'resumen_experimento.csv').open()))
for i,r in enumerate(summary):
 assert np.isclose(observed[i].mean(),float(r['macro_f1_reserva_media']))
 assert np.isclose(observed[i].std(ddof=1),float(r['macro_f1_reserva_sd']))
# Exhaustive ordered cluster bootstrap: 6^6 equally likely resamples.
# Keep all 11 fixed fits; same patient draws for all models. Macro-F1 of
# pooled crops in each draw, then mean over fits, not ensemble predictions.
indices=np.array(list(itertools.product(range(6),repeat=6)))
weights=np.array([(indices==p).sum(axis=1) for p in range(6)]).T
samplecm=np.einsum('bp,mspij->bmsij',weights,a)
values=f1(samplecm).mean(axis=-1)
ci=np.quantile(values,[.025,.975],axis=0)
result={'procedencia':'ZIP descargado por el usuario; contraste de 33 CSV y 33 JSON', 'sha256_zip':hashlib.sha256(args.zip.read_bytes()).hexdigest(),'n_imagenes':969,'n_pacientes':6,'R':11,'metodo':'Bootstrap agrupado por paciente exhaustivo, 46656 remuestras ordenadas de seis pacientes con reemplazo. Once ajustes fijos por modelo; media del macro-F1 agrupado por remuestra. Percentiles 2.5 y 97.5; clases fijas y cero si denominador cero. Comparaciones pareadas con mismos pacientes. Análisis posterior al cierre, exploratorio; no remuestrea entrenamiento ni semillas.', 'modelos':{},'diferencias':[]}
for i,m in enumerate(models):
 perclass=[]
 for k,c in enumerate(classes):
  cm=a[i].sum(axis=1); den=cm.sum(axis=-1)[:,k]+cm.sum(axis=-2)[:,k]
  perclass.append({'clase':c,'soporte':int(cm[0,k].sum()),'f1_media':float((2*cm[:,k,k]/den).mean())})
 result['modelos'][m]={'macro_f1_reserva_media':float(observed[i].mean()),'IC95_pacientes_inf':float(ci[0,i]),'IC95_pacientes_sup':float(ci[1,i]),'clases':perclass}
for i,j in [(2,1),(2,0),(1,0)]:
 diff=values[:,i]-values[:,j]; q=np.quantile(diff,[.025,.975]);result['diferencias'].append({'A':models[i],'B':models[j],'diferencia':float(observed[i].mean()-observed[j].mean()),'IC95_inf':float(q[0]),'IC95_sup':float(q[1])})
result['soporte_pacientes']=[{'paciente':p,'clases':a[0,0,k].sum(axis=1).tolist()} for k,p in enumerate(patients)]
(O/'analisis_reserva.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for f in ['resumen_experimento.csv','estado.json','enmienda_11.json','original_configuracion.json','original_plan_corridas.json','original_hiperparametros_seleccionados.json']:
 (O/f).write_bytes((R/f).read_bytes())
print(json.dumps(result,ensure_ascii=False,indent=2))
