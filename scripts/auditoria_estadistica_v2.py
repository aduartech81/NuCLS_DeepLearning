"""Auditoría post hoc de salidas guardadas. No entrena ni vuelve a evaluar modelos."""
from pathlib import Path
import json,re,csv,hashlib,itertools,collections,math
import numpy as np
import pandas as pd
from scipy import stats,optimize,integrate
from sklearn.metrics import f1_score,roc_auc_score,accuracy_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'resultados_analizados/auditoria_v2';OUT.mkdir(parents=True,exist_ok=True)
FIG=ROOT/'book/figuras';FIG.mkdir(exist_ok=True)
MODELS=['softmaxcnn_bn','densenet121','resnet50'];LABELS=['CNN-BN','DenseNet121','ResNet50'];COLORS=['#687eaa','#ba8250','#087e83'];PAIRS=[(2,1),(2,0),(1,0)]
CLASSES=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']
def dump(name,d): (OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def csvout(name,rows):pd.DataFrame(rows).to_csv(OUT/name,index=False)
def holm(ps):
 p=np.asarray(ps);order=np.argsort(p);a=np.empty(len(p));a[order]=np.minimum(1,np.maximum.accumulate(p[order]*(len(p)-np.arange(len(p)))));return a
nbpath=ROOT/'colab/Experimento_NuCLS_v2_ejecutado_cierre11.ipynb';nb=json.loads(nbpath.read_text());text='\n'.join(''.join(o.get('text',o.get('data',{}).get('text/plain',[]))) for c in nb['cells'] for o in c.get('outputs',[]))
pat=r'(softmaxcnn_bn|densenet121|resnet50) semilla=(\d+) época=(\d+) loss=([\d.]+) val_F1=([\d.]+) tiempo=([\d.]+)s'
rows=[];run=collections.Counter()
for model,seed,epoch,loss,val,secs in re.findall(pat,text):
 seed=int(seed);epoch=int(epoch)
 if epoch==1:run[(model,seed)]+=1
 phase='busqueda' if seed==4001 else 'piloto' if 5101<=seed<=5105 else 'cierre11' if 6101<=seed<=6111 else 'fuera_cierre'
 rows.append(dict(modelo=model,semilla=seed,repeticion_registro=run[(model,seed)],fase=phase,epoca=epoch,train_loss_impresa=float(loss),val_macro_f1_impreso=float(val),segundos_epoca_impresos=float(secs)))
curves=pd.DataFrame(rows);csvout('curvas_desde_notebook.csv',rows)
summ=[]
for keys,g in curves.groupby(['modelo','semilla','repeticion_registro','fase'],sort=False):
 model,seed,rep,phase=keys;assert list(g.epoca)==list(range(1,len(g)+1)),keys
 summ.append(dict(modelo=model,semilla=int(seed),repeticion_registro=int(rep),fase=phase,epocas=len(g),val_max_impreso=float(g.val_macro_f1_impreso.max()),primera_epoca_max_impreso=int(g.loc[g.val_macro_f1_impreso.idxmax(),'epoca']),segundos_epocas_sumados=float(g.segundos_epoca_impresos.sum())))
sumdf=pd.DataFrame(summ);csvout('corridas_desde_notebook.csv',summ)
final=sumdf[sumdf.fase=='cierre11'];assert len(final)==33
validation=final.pivot(index='semilla',columns='modelo',values='val_max_impreso')[MODELS]
assert list(validation.index)==list(range(6101,6112))
ref=pd.read_csv(ROOT/'resultados_analizados/cierre_11/resumen_experimento.csv').set_index('modelo')
assert np.all(np.abs(validation.mean()-ref.loc[MODELS,'macro_f1_val_media'])<.00005)
validation.to_csv(OUT/'validacion_por_semilla_desde_stdout.csv')
search=sumdf[sumdf.fase=='busqueda'].copy();assert len(search)==12 and (search.groupby('modelo').size()==4).all()
GRID=[(lr,wd) for lr in [1e-4,1e-3] for wd in [0.,1e-4]]
search['lr']=[GRID[int(x)-1][0] for x in search.repeticion_registro];search['weight_decay']=[GRID[int(x)-1][1] for x in search.repeticion_registro];search.to_csv(OUT/'busqueda_desde_stdout.csv',index=False)
# Final curves: individual runs, not averages after early stopping.
fig,axes=plt.subplots(3,2,figsize=(11,9),constrained_layout=True)
for i,m in enumerate(MODELS):
 for seed,g in curves[(curves.modelo==m)&(curves.fase=='cierre11')].groupby('semilla'):
  axes[i,0].plot(g.epoca,g.train_loss_impresa,color=COLORS[i],alpha=.45,lw=1)
  axes[i,1].plot(g.epoca,g.val_macro_f1_impreso,color=COLORS[i],alpha=.45,lw=1)
 for j in range(2):axes[i,j].grid(alpha=.2);axes[i,j].set_xlabel('Época');axes[i,j].set_title(LABELS[i]+(' · pérdida train' if j==0 else ' · macro-F1 validación'))
 axes[i,1].set_ylim(0,1)
fig.suptitle('33 corridas del cierre · curvas reconstruidas del stdout (4 decimales)',fontsize=13);fig.savefig(FIG/'curvas_entrenamiento_v2.svg');plt.close(fig)
# Tests conditional on a common split; seed number is the pairing key.
reserva=pd.read_csv(ROOT/'resultados_analizados/cierre_11/metricas_reserva_por_semilla.csv')
sets={'validacion_redondeada':validation,'reserva':reserva.pivot(index='semilla',columns='modelo',values='macro_f1')[MODELS],'AUC_reserva':reserva.pivot(index='semilla',columns='modelo',values='AUC_macro_OvR')[MODELS]}
contrasts=[];omnibus={};qqfig,qqax=plt.subplots(2,3,figsize=(12,7),constrained_layout=True)
for name,df in sets.items():
 block=[]
 for j,(ai,bi) in enumerate(PAIRS):
  a,b=MODELS[ai],MODELS[bi];d=(df[a]-df[b]).to_numpy();n=len(d);sd=d.std(ddof=1);mean=d.mean();tt=stats.ttest_rel(df[a],df[b]);w=stats.wilcoxon(d,method='exact');sw=stats.shapiro(d);rr=stats.rankdata(abs(d));rb=float(np.sum(np.sign(d)*rr)/rr.sum());ci=stats.t.interval(.95,n-1,loc=mean,scale=sd/np.sqrt(n))
  block.append(dict(conjunto=name,A=a,B=b,n=n,diferencia=float(mean),sd_diferencia=float(sd),IC95_t_inf=float(ci[0]),IC95_t_sup=float(ci[1]),t=float(tt.statistic),p_t=float(tt.pvalue),W=float(w.statistic),p_wilcoxon=float(w.pvalue),dz=float(mean/sd),r_biserial_pareado=rb,shapiro_W=float(sw.statistic),shapiro_p=float(sw.pvalue)))
  if name!='AUC_reserva':
   ax=qqax[0 if name=='validacion_redondeada' else 1,j];stats.probplot(d,dist='norm',plot=ax);ax.set_title(name+'\n'+LABELS[ai]+' − '+LABELS[bi],fontsize=10);ax.grid(alpha=.2)
 for key in ['p_t','p_wilcoxon']:
  for row,p in zip(block,holm([x[key] for x in block])):row[key+'_holm']=float(p)
 contrasts+=block
 ranks=np.array([stats.rankdata(-r) for r in df.to_numpy()]);fr=stats.friedmanchisquare(*[df[m] for m in MODELS]);mr=ranks.mean(0)
 # Exact null distribution for 3 models and 11 complete blocks, without ties.
 assert all(len(set(r))==3 for r in df.to_numpy())
 states={(0,0,0):1}
 for _ in range(len(df)):
  nxt=collections.defaultdict(int)
  for state,cnt in states.items():
   for perm in itertools.permutations([1,2,3]):nxt[tuple(x+y for x,y in zip(state,perm))]+=cnt
  states=nxt
 exact=sum(cnt for sums,cnt in states.items() if 12/(len(df)*3*4)*sum(s*s for s in sums)-3*len(df)*4 >= fr.statistic-1e-10)/6**len(df)
 nem=[]
 for ai,bi in PAIRS:
  q=abs(mr[ai]-mr[bi])/np.sqrt(3*4/(6*len(df)));nem.append(dict(A=MODELS[ai],B=MODELS[bi],diferencia_rangos=float(mr[bi]-mr[ai]),p_nemenyi=float(stats.studentized_range.sf(q*np.sqrt(2),3,np.inf))))
 omnibus[name]=dict(friedman_Q=float(fr.statistic),p_chi2_aproximado=float(fr.pvalue),p_permutacion_exacta=float(exact),kendall_W=float(fr.statistic/(len(df)*2)),rangos_medios=dict(zip(MODELS,mr.tolist())),nemenyi_aproximado=nem)
qqfig.savefig(FIG/'qq_diferencias_v2.svg');plt.close(qqfig);csvout('contrastes_semillas.csv',contrasts);dump('omnibus.json',omnibus)
# Prospective detectable difference based ONLY on the development pilot SD.
plan=json.loads((ROOT/'resultados_analizados/cierre_11/original_plan_corridas.json').read_text());alpha=.05/3;n=11;crit=stats.t.ppf(1-alpha/2,n-1)
def power(delta,sd):
 nc=delta*np.sqrt(n)/sd
 return integrate.quad(lambda v: (stats.norm.sf(crit*np.sqrt(v/(n-1))-nc)+stats.norm.cdf(-crit*np.sqrt(v/(n-1))-nc))*stats.chi2.pdf(v,n-1),0,np.inf,epsabs=1e-10)[0]
mde=[]
for p in plan['comparaciones']:
 sd=p['sd_diferencias'];delta=optimize.brentq(lambda v:power(v,sd)-.8,1e-8,.05);mde.append(dict(A=p['A'],B=p['B'],sd_piloto=sd,R=11,alpha_por_par=alpha,potencia_objetivo=.8,mejora_minima_detectable=float(delta),potencia_para_delta_002=float(power(.02,sd))))
dump('mejora_minima_detectable.json',mde)
dump('procedencia_stdout.json',dict(notebook_sha256=hashlib.sha256(nbpath.read_bytes()).hexdigest(),epocas_impresas=len(curves),corridas_cierre=33,piloto=len(sumdf[sumdf.fase=='piloto']),busqueda=len(search),precision_f1_loss=4,precision_segundos=1,limitacion='Reconstrucción del stdout, no archivos historia.json originales. Máximo impreso valida las medias a tolerancia 0.00005; puede no resolver empates de época. Segundos suman épocas train+validación, excluyen gastos externos; no latencia de inferencia. Semilla 6112 excluida del cierre.'))
print('CONTRASTES',pd.DataFrame(contrasts).to_string(index=False));print('MDE',mde);print('OMNIBUS',omnibus,flush=True)
