"""Contrastes exploratorios del piloto; no utiliza ni evalúa la reserva v2."""
from pathlib import Path
import itertools,json
import numpy as np
import pandas as pd
from scipy.stats import rankdata,studentized_range,f,binomtest
R=Path(__file__).resolve().parents[1];O=R/'resultados_analizados/contrastes_ampliados';O.mkdir(exist_ok=True)
MODELS=['cnn_local','resnet18','mobilenet_v2'];SEEDS=list(range(4101,4106));CLASSES=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']
x=pd.read_csv(R/'resultados_analizados/estadistica_complementaria/metricas_corridas.csv').pivot(index='semilla',columns='modelo',values='macro_f1').loc[SEEDS,MODELS].to_numpy();n,k=x.shape
ssmodel=n*np.sum((x.mean(0)-x.mean())**2);sssubject=k*np.sum((x.mean(1)-x.mean())**2);sstotal=np.sum((x-x.mean())**2);sse=sstotal-ssmodel-sssubject
F=(ssmodel/(k-1))/(sse/((n-1)*(k-1)))
S=np.cov(x,rowvar=False);H=np.eye(k)-np.ones((k,k))/k;V=H@S@H;eps=np.trace(V)**2/((k-1)*np.trace(V@V));eps=float(np.clip(eps,1/(k-1),1))
ranks=np.array([rankdata(-row) for row in x]);meanrank=ranks.mean(0);nemenyi=[]
for a,b in itertools.combinations(range(k),2):
 q=abs(meanrank[a]-meanrank[b])/np.sqrt(k*(k+1)/(6*n))*np.sqrt(2)
 nemenyi.append(dict(A=MODELS[a],B=MODELS[b],rango_A=meanrank[a],rango_B=meanrank[b],q=q,p_Nemenyi=float(studentized_range.sf(q,k,np.inf))))
pd.DataFrame(nemenyi).to_csv(O/'nemenyi.csv',index=False)
ref=None;frames={};probs={}
for model in MODELS:
 for seed in SEEDS:
  d=pd.read_csv(R/f'resultados/{model}_{seed}/predicciones_validacion.csv.gz').sort_values(['paciente','archivo']).reset_index(drop=True)
  keys=d[['paciente','archivo','clase_real']]
  if ref is None:ref=keys
  else:pd.testing.assert_frame_equal(ref,keys)
  frames[model,seed]=d;p=d[['p_tumor','p_linfocito','p_estroma']].to_numpy();assert np.allclose(p.sum(1),1,atol=1e-5);probs[model,seed]=p/p.sum(1,keepdims=True)
y=np.array([CLASSES.index(v) for v in ref.clase_real]);patients,pid=np.unique(ref.paciente,return_inverse=True)
B=2000;rng=np.random.default_rng(4101);draw=rng.integers(0,len(patients),(B,len(patients)));clusterweights=np.array([np.bincount(a,minlength=len(patients)) for a in draw]);boot={m:np.zeros(B) for m in MODELS};observed={}
# AUC exacta ponderada con empates: las repeticiones conservan juntos los recortes de cada paciente.
def auc_weighted(score,target,weights):
 order=np.argsort(score,kind='stable');starts=np.r_[0,np.flatnonzero(np.diff(score[order]))+1];w=weights[:,order]
 pos=np.add.reduceat(w*target[order],starts,axis=1);neg=np.add.reduceat(w*(1-target[order]),starts,axis=1)
 denom=pos.sum(1)*neg.sum(1)
 return np.divide((pos*(np.cumsum(neg,axis=1)-.5*neg)).sum(1),denom,out=np.full(len(w),np.nan),where=denom>0)
for model in MODELS:
 vals=[]
 for seed in SEEDS:
  p=probs[model,seed]
  vals.append(float(np.mean([auc_weighted(p[:,c],(y==c).astype(int),np.ones((1,len(y))))[0] for c in range(3)])))
  for start in range(0,B,100):
   w=clusterweights[start:start+100,pid]
   a=np.array([auc_weighted(p[:,c],(y==c).astype(int),w) for c in range(3)])
   boot[model][start:start+100]+=a.mean(0)/len(SEEDS)
 observed[model]=float(np.mean(vals))
auc=[]
for a,b in itertools.combinations(MODELS,2):
 delta=boot[a]-boot[b];valid=delta[np.isfinite(delta)];lo,hi=np.percentile(valid,[2.5,97.5]);auc.append(dict(A=a,B=b,delta_auc_macro=observed[a]-observed[b],IC95_inferior=lo,IC95_superior=hi,repeticiones_validas=len(valid)))
pd.DataFrame(auc).to_csv(O/'diferencias_auc_por_paciente.csv',index=False)
mcn=[]
for seed in SEEDS:
 for a,b in itertools.combinations(MODELS,2):
  ca=frames[a,seed].clase_predicha.to_numpy()==ref.clase_real.to_numpy();cb=frames[b,seed].clase_predicha.to_numpy()==ref.clase_real.to_numpy();ab=int((ca&~cb).sum());ba=int((~ca&cb).sum())
  mcn.append(dict(semilla=seed,A=a,B=b,A_acierta_B_falla=ab,A_falla_B_acierta=ba,p_McNemar_nominal=float(binomtest(ab,ab+ba,.5).pvalue) if ab+ba else 1.,interpretacion='Nominal: independencia de recortes no satisfecha; no usar como inferencia confirmatoria'))
pd.DataFrame(mcn).to_csv(O/'mcnemar_nominal.csv',index=False)
report={'naturaleza':'Post hoc, validación seleccionó checkpoints; no confirma generalización','ANOVA_medidas_repetidas':{'bloque':'semilla','F':float(F),'gl_modelo':k-1,'gl_error':(n-1)*(k-1),'p_sin_correccion':float(f.sf(F,k-1,(n-1)*(k-1))),'epsilon_Greenhouse_Geisser':eps,'p_GG':float(f.sf(F,(k-1)*eps,(n-1)*(k-1)*eps))},'AUC_macro_media_cinco_semillas':observed,'bootstrap':{'B':B,'semilla':4101,'unidad':'paciente','predicciones':'Fijas las cinco redes por modelo; promedio de sus AUC, no ensemble de probabilidades','clases_ausentes':'Repetición excluida si alguna AUC no es estimable'},'limites':['ANOVA y Nemenyi describen cinco ejecuciones condicionadas a una misma validación.','Greenhouse-Geisser corrige grados de libertad por esfericidad; no soluciona tamaño pequeño ni selección de checkpoints.','Nemenyi controla comparaciones de rangos en su aproximación de rango studentizado; n=5 limita su precisión.','McNemar nominal supone independencia entre recortes; la correlación por paciente impide interpretarlo como prueba confirmatoria.','IC de diferencias AUC marginales sin ajuste múltiple; exploratorios.']}
(O/'metodo.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2));print(pd.DataFrame(auc).to_string(index=False));print(pd.DataFrame(nemenyi).to_string(index=False))
