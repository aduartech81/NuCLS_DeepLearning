"""Análisis post hoc de predicciones guardadas; no carga ni evalúa checkpoints.
Uso: python scripts/robustez_reserva_v2.py /ruta/al/cierre/reserva
"""
from pathlib import Path
import sys,itertools,json
import numpy as np
import pandas as pd
from scipy.stats import binomtest
from sklearn.metrics import f1_score,roc_auc_score
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'resultados_analizados/auditoria_v2';OUT.mkdir(exist_ok=True)
raw=Path(sys.argv[1]);models=['softmaxcnn_bn','densenet121','resnet50'];classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal'];pairs=[(2,1),(2,0),(1,0)]
def holm(p):
 p=np.array(p);o=np.argsort(p);a=np.empty(len(p));a[o]=np.minimum(1,np.maximum.accumulate(p[o]*(len(p)-np.arange(len(p)))));return a
frames={};base=None
for m in models:
 for seed in range(6101,6112):
  d=pd.read_csv(raw/f'{m}_{seed}.csv',float_precision='round_trip').sort_values(['paciente','archivo']).reset_index(drop=True)
  if base is None:base=d
  assert d[['paciente','archivo','clase_real']].equals(base[['paciente','archivo','clase_real']])
  frames[m,seed]=d
truth=base.clase_real.to_numpy();patients=base.paciente.to_numpy();tss=base.paciente.str.split('-').str[1].to_numpy();rows=[]
for (m,seed),d in frames.items():
 for level,groups in [('paciente',patients),('TSS',tss)]:
  for group in sorted(set(groups)):
   for mode,mask in [('grupo',groups==group),('sin_grupo',groups!=group)]:
    y=truth[mask];pred=d.clase_predicha.to_numpy()[mask]
    rows.append(dict(modelo=m,semilla=seed,nivel=level,grupo=group,analisis=mode,n=int(mask.sum()),clases_presentes=len(set(y)),macro_f1_tres_clases=f1_score(y,pred,labels=classes,average='macro',zero_division=0),accuracy=float(np.mean(y==pred))))
pd.DataFrame(rows).to_csv(OUT/'robustez_grupos_por_semilla.csv',index=False)
pd.DataFrame(rows).groupby(['modelo','nivel','grupo','analisis']).agg(n=('n','first'),clases_presentes=('clases_presentes','first'),macro_f1_media=('macro_f1_tres_clases','mean'),macro_f1_sd=('macro_f1_tres_clases','std')).reset_index().to_csv(OUT/'robustez_grupos_resumen.csv',index=False)
mc=[];cluster=[]
y=np.array([classes.index(x) for x in truth]);unique=sorted(set(patients))
for ai,bi in pairs:
 a,b=models[ai],models[bi];pa=np.array([frames[a,s][['p_tumor','p_linfocito','p_estroma']].to_numpy() for s in range(6101,6112)]);pb=np.array([frames[b,s][['p_tumor','p_linfocito','p_estroma']].to_numpy() for s in range(6101,6112)])
 pa=pa/pa.sum(2,keepdims=True);pb=pb/pb.sum(2,keepdims=True)
 ca=pa.argmax(2)==y;cb=pb.argmax(2)==y
 for k,s in enumerate(range(6101,6112)):
  ab=int((ca[k]&~cb[k]).sum());ba=int((~ca[k]&cb[k]).sum());mc.append(dict(A=a,B=b,semilla=s,A_correcto_B_error=ab,A_error_B_correcto=ba,p_exacto_recortes=binomtest(ab,ab+ba).pvalue if ab+ba else 1.))
 def auc(p):return np.mean([roc_auc_score(y,x,multi_class='ovr',average='macro',labels=[0,1,2]) for x in p])
 obsauc=auc(pa)-auc(pb);obsacc=float((ca.astype(float)-cb).mean());na=[];nc=[]
 for signs in itertools.product([False,True],repeat=len(unique)):
  swap=np.isin(patients,[g for g,s in zip(unique,signs) if s]);aa=np.where(swap[None,:,None],pb,pa);bb=np.where(swap[None,:,None],pa,pb)
  na.append(auc(aa)-auc(bb));nc.append(float(((aa.argmax(2)==y).astype(float)-(bb.argmax(2)==y)).mean()))
 cluster.append(dict(A=a,B=b,n_pacientes=len(unique),permutaciones=len(na),delta_AUC=obsauc,p_AUC=float(np.mean(np.abs(na)>=abs(obsauc)-1e-12)),delta_accuracy=obsacc,p_accuracy=float(np.mean(np.abs(nc)>=abs(obsacc)-1e-12))))
for r,p in zip(mc,holm([r['p_exacto_recortes'] for r in mc])):r['p_holm_33']=p
for key in ['p_AUC','p_accuracy']:
 for r,p in zip(cluster,holm([r[key] for r in cluster])):r[key+'_holm_3']=p
pd.DataFrame(mc).to_csv(OUT/'mcnemar_diagnostico.csv',index=False);pd.DataFrame(cluster).to_csv(OUT/'permutacion_por_paciente.csv',index=False)
print(pd.DataFrame(cluster).to_string(index=False))
