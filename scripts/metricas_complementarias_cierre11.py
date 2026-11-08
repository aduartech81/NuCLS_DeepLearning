"""Métricas descriptivas posteriores al cierre; no ajusta modelos ni umbrales."""
import argparse,csv,json
from pathlib import Path
import numpy as np
from sklearn.metrics import (accuracy_score,balanced_accuracy_score,matthews_corrcoef,
 roc_auc_score,average_precision_score,log_loss,f1_score,confusion_matrix)
p=argparse.ArgumentParser();p.add_argument('--entrada',type=Path,required=True);p.add_argument('--salida',type=Path,required=True);a=p.parse_args();a.salida.mkdir(parents=True,exist_ok=True)
models=['softmaxcnn_bn','densenet121','resnet50'];classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal'];out=[];cms={};bins={};ref=None
for m in models:
 cms[m]=[]; bins[m]=[]
 for seed in range(6101,6112):
  rows=list(csv.DictReader((a.entrada/'reserva'/f'{m}_{seed}.csv').open()))
  ids=[(r['archivo'],r['paciente'],r['clase_real']) for r in rows]
  if ref is None:ref=ids
  assert ids==ref and len(rows)==969
  y=np.array([classes.index(r['clase_real']) for r in rows]);q=np.array([[float(r[c]) for c in ['p_tumor','p_linfocito','p_estroma']] for r in rows]);pred=q.argmax(1)
  assert np.isfinite(q).all() and (q>=0).all() and (q<=1).all() and np.allclose(q.sum(1),1,atol=1e-5)
  # Normalize floating-point roundoff only; predictions remain argmax.
  q=q/q.sum(1,keepdims=True);onehot=np.eye(3)[y];conf=q.max(1);correct=(pred==y);idx=np.minimum((conf*10).astype(int),9);ece=0.;bs=[]
  for b in range(10):
   mask=idx==b;n=int(mask.sum());acc=float(correct[mask].mean()) if n else None;confidence=float(conf[mask].mean()) if n else None
   if n:ece+=n/len(y)*abs(acc-confidence)
   bs.append({'intervalo':[b/10,(b+1)/10],'n':n,'exactitud':acc,'confianza':confidence})
  bins[m].append({'semilla':seed,'bins':bs});cms[m].append(confusion_matrix(y,pred,labels=[0,1,2]).tolist())
  r={'modelo':m,'semilla':seed,'macro_f1':f1_score(y,pred,average='macro'),'exactitud':accuracy_score(y,pred),'exactitud_balanceada':balanced_accuracy_score(y,pred),'MCC':matthews_corrcoef(y,pred),'AUC_macro_OvR':roc_auc_score(y,q,multi_class='ovr',average='macro'),'AP_macro_OvR':average_precision_score(onehot,q,average='macro'),'Brier_multiclase_suma':float(np.mean(np.sum((q-onehot)**2,axis=1))),'log_loss':log_loss(y,q,labels=[0,1,2]),'ECE_10_bins':ece};out.append(r)
with (a.salida/'metricas_reserva_por_semilla.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
summary={}
for m in models:
 selected=[r for r in out if r['modelo']==m]
 summary[m]={k:{'media':float(np.mean([r[k] for r in selected])),'sd_semillas':float(np.std([r[k] for r in selected],ddof=1))} for k in out[0] if k not in ['modelo','semilla']}
 original={r['modelo']:r for r in csv.DictReader((a.entrada/'resumen_experimento.csv').open())}
 assert np.isclose(summary[m]['macro_f1']['media'],float(original[m]['macro_f1_reserva_media']))
result={'alcance':'Descriptivo posterior al cierre. Once ajustes fijos, misma reserva de 969 recortes de seis pacientes. Media de métricas individuales, no ensemble. No se ajustan umbrales ni calibración sobre reserva. SD entre semillas no es incertidumbre entre pacientes.','definiciones':{'AUC':'ROC AUC macro one-vs-rest, sin ponderación de clases','AP':'Promedio de average precision por clase, no área trapezoidal PR','Brier':'Media sobre imágenes de suma sobre tres clases del error cuadrático; rango 0 a 2','ECE':'Diez intervalos de confianza máxima de ancho 0.1, último incluye 1. Error absoluto exactitud-confianza ponderado por número de recortes. No mide calibración individual por clase.'},'resumen':summary,'confusiones_por_semilla':cms,'calibracion_por_semilla':bins}
(a.salida/'metricas_complementarias.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
