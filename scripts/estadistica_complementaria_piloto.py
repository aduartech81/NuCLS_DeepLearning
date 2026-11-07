"""Análisis post hoc del piloto: no constituye evaluación del conjunto de prueba."""
from pathlib import Path
import itertools,json
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import f1_score,matthews_corrcoef,average_precision_score,log_loss
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados_analizados'/'estadistica_complementaria';OUT.mkdir(parents=True,exist_ok=True)
MODELS=['cnn_local','resnet18','mobilenet_v2'];SEEDS=list(range(4101,4106))
CLASSES=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']

def ece(y,p):
 confidence=p.max(1);correct=p.argmax(1)==y;value=0.;bins=[]
 for i in range(10):
  mask=(confidence>=i/10)&((confidence<(i+1)/10) if i<9 else (confidence<=1))
  n=int(mask.sum())
  acc=float(correct[mask].mean()) if n else None;conf=float(confidence[mask].mean()) if n else None
  if n:value+=n/len(y)*abs(acc-conf)
  bins.append(dict(bin=i,n=n,accuracy=acc,confianza=conf))
 return value,bins

def holm(ps):
 order=np.argsort(ps);result=np.empty(len(ps));previous=0.
 for rank,j in enumerate(order):
  previous=max(previous,min(1.,(len(ps)-rank)*ps[j]));result[j]=previous
 return result.tolist()

runs=[];calibration=[];reference=None
for model,seed in itertools.product(MODELS,SEEDS):
 file=ROOT/'resultados'/f'{model}_{seed}'/'predicciones_validacion.csv.gz'
 if not file.exists():file=file.with_suffix('')
 frame=pd.read_csv(file).sort_values('archivo').reset_index(drop=True)
 keys=frame[['archivo','paciente','clase_real']]
 if reference is None:reference=keys
 else:assert keys.equals(reference),'Predicciones no pareadas'
 y=frame.clase_real.map(dict(zip(CLASSES,range(3)))).to_numpy()
 p=frame[['p_tumor','p_linfocito','p_estroma']].to_numpy();assert np.isfinite(p).all() and np.allclose(p.sum(1),1,atol=1e-5)
 assert (p>=0).all() and (p<=1).all()
 p=p/p.sum(1,keepdims=True)  # Renormalización del redondeo numérico de probabilidades exportadas.
 pred=p.argmax(1);onehot=np.eye(3)[y];cal,bins=ece(y,p)
 runs.append(dict(modelo=model,semilla=seed,macro_f1=f1_score(y,pred,average='macro'),MCC=matthews_corrcoef(y,pred),AP_macro=average_precision_score(onehot,p,average='macro'),ECE_10=cal,Brier_multiclase=np.square(p-onehot).sum(1).mean(),log_loss=log_loss(y,p,labels=[0,1,2])))
 calibration.extend(dict(modelo=model,semilla=seed,**b) for b in bins)
runs=pd.DataFrame(runs);runs.to_csv(OUT/'metricas_corridas.csv',index=False)
pd.DataFrame(calibration).to_csv(OUT/'calibracion_bins.csv',index=False)
summary=[]
for model in MODELS:
 for metric in ['macro_f1','MCC','AP_macro','ECE_10','Brier_multiclase','log_loss']:
  x=runs.loc[runs.modelo==model,metric].to_numpy();sd=x.std(ddof=1);half=stats.t.ppf(.975,len(x)-1)*sd/np.sqrt(len(x))
  summary.append(dict(modelo=model,metrica=metric,media=x.mean(),DE=sd,IC95_t_inferior=x.mean()-half,IC95_t_superior=x.mean()+half))
pd.DataFrame(summary).to_csv(OUT/'resumen_ic_semillas.csv',index=False)
wide=runs.pivot(index='semilla',columns='modelo',values='macro_f1')[MODELS]
pairs=[];qq=[]
for a,b in itertools.combinations(MODELS,2):
 delta=(wide[a]-wide[b]).to_numpy();t=stats.ttest_rel(wide[a],wide[b]);sh=stats.shapiro(delta)
 w=stats.wilcoxon(delta,method='exact');ranks=stats.rankdata(abs(delta[delta!=0]));sign=np.sign(delta[delta!=0]);rb=float(np.sum(ranks*sign)/sum(ranks)) if len(ranks) else 0.
 half=stats.t.ppf(.975,4)*delta.std(ddof=1)/np.sqrt(5)
 pairs.append(dict(A=a,B=b,delta_A_menos_B=delta.mean(),IC95_t_inferior=delta.mean()-half,IC95_t_superior=delta.mean()+half,t=float(t.statistic),p_t=float(t.pvalue),W=float(w.statistic),p_W=float(w.pvalue),d_z=delta.mean()/delta.std(ddof=1),rango_biserial=rb,Shapiro_W=float(sh.statistic),Shapiro_p=float(sh.pvalue)))
 theoretical,observed=stats.probplot(delta,dist='norm',fit=False)
 qq.extend(dict(A=a,B=b,cuantil_normal=float(x),diferencia_ordenada=float(y)) for x,y in zip(theoretical,observed))
for name in ['t','W']:
 adjusted=holm([r['p_'+name] for r in pairs])
 for row,p in zip(pairs,adjusted):row['p_'+name+'_Holm']=p
pd.DataFrame(pairs).to_csv(OUT/'comparaciones_pareadas.csv',index=False);pd.DataFrame(qq).to_csv(OUT/'qq_diferencias.csv',index=False)
f=stats.friedmanchisquare(*(wide[m] for m in MODELS))
# Descomposición descriptiva de un diseño bloqueado, sin réplicas por celda.
x=wide.to_numpy();grand=x.mean();ss_model=5*np.square(x.mean(0)-grand).sum();ss_seed=3*np.square(x.mean(1)-grand).sum();ss_total=np.square(x-grand).sum();ss_res=ss_total-ss_model-ss_seed
report=dict(naturaleza='Post hoc exploratorio; validación seleccionó checkpoints. No prueba confirmatoria.',semillas=SEEDS,pacientes=int(reference.paciente.nunique()),recortes_por_corrida=len(reference),Friedman=dict(estadistico=float(f.statistic),p_asintotica=float(f.pvalue)),suma_cuadrados=dict(modelo=float(ss_model),semilla=float(ss_seed),residuo_interaccion=float(ss_res),total=float(ss_total)),baseline_descriptivo_piloto=wide.mean().idxmax(),advertencias=['Los IC t reflejan variación entre cinco semillas, condicionada a una misma validación; no incertidumbre entre pacientes.','Shapiro tiene poca potencia con cinco diferencias. No se usa para elegir retrospectivamente la prueba con menor p.','Holm se aplica a tres pares dentro de cada familia de pruebas; t y Wilcoxon se reportan como análisis exploratorios distintos.','AP macro es average precision, no integración trapezoidal de PR.','ECE usa diez intervalos uniformes de confianza y no implica calibración ajustada.','Las sumas de cuadrados no son componentes de varianza poblacional; interacción y residuo no se separan sin replicación.','Friedman usa aproximación asintótica con n pequeño.','Probabilidades exportadas verificadas dentro de tolerancia 1e-5 y renormalizadas por fila para corregir redondeo numérico.','No se evalúa la reserva v2.'])
(OUT/'alcance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(pd.DataFrame(summary).query("metrica == 'macro_f1'").to_string(index=False));print(report['Friedman'])
# Figuras reproducibles, sin acceso a imágenes ni a reserva.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axes=plt.subplots(1,3,figsize=(11,3.4),layout='constrained')
for ax,((a,b),group) in zip(axes,pd.DataFrame(qq).groupby(['A','B'],sort=False)):
 ax.scatter(group.cuantil_normal,group.diferencia_ordenada,color='#137f87')
 slope,intercept=np.polyfit(group.cuantil_normal,group.diferencia_ordenada,1)
 ax.plot(group.cuantil_normal,intercept+slope*group.cuantil_normal,color='#d99240')
 ax.set_title(a+' − '+b,fontsize=9);ax.set_xlabel('Cuantil normal');ax.set_ylabel('Diferencia macro-F1')
fig.savefig(ROOT/'book/figuras/qq_piloto.svg');plt.close(fig)
fig,ax=plt.subplots(figsize=(6,4),layout='constrained')
for model in MODELS:
 subset=[r for r in calibration if r['modelo']==model];xx=[];yy=[]
 for i in range(10):
  bins=[r for r in subset if r['bin']==i and r['n']];n=sum(r['n'] for r in bins)
  if n:xx.append(sum(r['n']*r['confianza'] for r in bins)/n);yy.append(sum(r['n']*r['accuracy'] for r in bins)/n)
 ax.plot(xx,yy,'o-',label=model)
ax.plot([0,1],[0,1],'--',color='gray');ax.set(xlim=(0,1),ylim=(0,1),xlabel='Confianza promedio',ylabel='Fracción correcta',title='Fiabilidad descriptiva del piloto');ax.legend()
fig.savefig(ROOT/'book/figuras/fiabilidad_piloto.svg');plt.close(fig)
