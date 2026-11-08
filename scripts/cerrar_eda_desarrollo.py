"""Diagnósticos exploratorios sobre evidencia exportada; no abre reserva ni entrena CNN."""
from pathlib import Path
import json,hashlib
import numpy as np
import pandas as pd
from sklearn.covariance import MinCovDet
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
D=R/'resultados_analizados/eda_pixeles_v2';O=R/'resultados_analizados/eda_cierre';O.mkdir(exist_ok=True)
SEED=4101;B=5000
results={}
for key in ['dominio','sitio']:
 p=D/f'diagnostico_{key}_predicciones.csv';df=pd.read_csv(p)
 assert df.paciente.is_unique
 groups=[(g.real==g.prediccion).to_numpy(dtype=float) for _,g in df.groupby('real')]
 rng=np.random.default_rng(SEED)
 boot=np.mean([g[rng.integers(0,len(g),size=(B,len(g)))].mean(axis=1) for g in groups],axis=0)
 results[key]={'pacientes':len(df),'clases':len(groups),'balanced_accuracy':float(np.mean([g.mean() for g in groups])),
 'ic95_percentil':np.quantile(boot,[.025,.975]).tolist(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
# Patient-level outlier ranking: fit exclusively on training descriptors.
f=D/'medianas_por_paciente.csv';m=pd.read_csv(f)
cols=['R_media','G_media','B_media','R_sd','G_sd','B_sd','saturacion_media','fondo_fraccion','laplaciano_var','entropia_gris']
assert np.isfinite(m[cols].to_numpy()).all(); train=m.particion.eq('train')
x=m[cols].copy();x['laplaciano_var']=np.log1p(x['laplaciano_var'])
center=x[train].median();scale=x[train].quantile(.75)-x[train].quantile(.25)
used=scale[scale>0].index.tolist();z=((x[used]-center[used])/scale[used]).to_numpy()
fit=MinCovDet(random_state=SEED).fit(z[train]);dist=fit.mahalanobis(z)
cut=float(np.quantile(dist[train],.95))
m['distancia_robusta_cuadrada']=dist;m['prioridad_inspeccion']=dist>cut
m[['paciente','particion','tss','distancia_robusta_cuadrada','prioridad_inspeccion']].to_csv(O/'distancias_paciente.csv',index=False)
results['atipicos']={'variables':used,'transformacion':'log1p de Laplaciano; mediana e IQR de entrenamiento','umbral_p95_train':cut,
'pacientes_por_grupo':m.groupby('particion').size().to_dict(),'priorizados_por_grupo':m.groupby('particion').prioridad_inspeccion.sum().astype(int).to_dict(),
'mediana_train':center.to_dict(),'iqr_train':scale.to_dict(),'sha256_fuente':hashlib.sha256(f.read_bytes()).hexdigest()}
results['metodo']={'semilla':SEED,'replicas':B,'unidad':'paciente','intervalos':'Remuestreo estratificado por etiqueta real de predicciones OOF fijas; sin reentrenamiento. Condicionados a TSS y partición observados; no incluyen incertidumbre de ajuste ni entre centros.','outliers':'Priorización exploratoria, no exclusión. Umbral empírico; no p-valores ni diagnóstico de mala calidad.','reserva_abierta':False}
(O/'resumen.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(1,2,figsize=(11.8,4.4),layout='constrained')
for i,(key,label) in enumerate([('dominio','Partición (2 grupos)'),('sitio','Procedencia (8 TSS)')]):
 q=results[key];v=q['balanced_accuracy'];lo,hi=q['ic95_percentil'];axes[0].errorbar(v,i,xerr=[[v-lo],[hi-v]],fmt='o',color='#087f8c',capsize=5)
 axes[0].scatter(1/q['clases'],i,marker='|',s=180,color='#b87320',label='Referencia uniforme' if i==0 else None)
axes[0].set(yticks=[0,1],yticklabels=['Partición','Procedencia'],xlabel='Exactitud balanceada',xlim=(0,1),ylim=(-.6,1.6),title='Predicciones por paciente e IC 95%')
axes[0].grid(axis='x',alpha=.2)
axes[0].legend(fontsize=9,loc='lower right')
for part,color,label in [('train','#087f8c','Entrenamiento'),('validation','#b87320','Validación')]:
 v=np.sort(m.loc[m.particion.eq(part),'distancia_robusta_cuadrada']);axes[1].plot(np.arange(1,len(v)+1)/len(v),v,'o',ms=3,label=label,color=color)
axes[1].axhline(cut,ls='--',color='#64748b',label='P95 de entrenamiento')
axes[1].set(yscale='log',xlabel='Fracción acumulada de pacientes',ylabel='Distancia robusta² (escala log)',title='Heterogeneidad multivariada')
axes[1].legend(fontsize=9)
for folder in ['book/figuras','assets']:
 fig.savefig(R/folder/'eda_incertidumbre_v2.svg',bbox_inches='tight')
print(json.dumps({k:v for k,v in results.items() if k!='atipicos'},ensure_ascii=False))
print(results['atipicos']['priorizados_por_grupo'])
