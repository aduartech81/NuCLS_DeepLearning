"""Figuras del informe a partir de evidencia real; no reentrena ni modifica métricas."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
R=Path(__file__).resolve().parents[1]; O=R/'book/figuras'
models=['cnn_local','resnet18','mobilenet_v2']; names=['CNN local','ResNet18','MobileNetV2']
colors=['#64748b','#087f8c','#b87320']; classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal']; labels=['Tumoral','Linfocito','Estromal']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#22394b','text.color':'#22394b','axes.titleweight':'bold','svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white'})
def save(fig,n):
 fig.savefig(O/f'visual_{n}.svg',bbox_inches='tight');plt.close(fig)
s=pd.read_csv(R/'resultados_analizados/resumen_verificado.csv').set_index('modelo').loc[models]
runs=pd.read_csv(R/'resultados_analizados/corridas_verificadas.csv')
fig,ax=plt.subplots(figsize=(9,3.8),layout='constrained')
for i,m in enumerate(models):
 vals=runs.loc[runs.modelo==m,'macro_f1'].to_numpy()*100
 ax.scatter(vals,np.arange(5)*.055+i-.11,color=colors[i],alpha=.5,s=30)
 mean=s.loc[m,'macro_f1_media']*100;sd=s.loc[m,'macro_f1_sd']*100
 ax.errorbar(mean,i,xerr=sd,fmt='D',color=colors[i],capsize=6,ms=7,lw=2.5)
 ax.text(100,i,f'{mean:.1f} ± {sd:.1f}',ha='right',va='center',weight='bold')
ax.set(yticks=range(3),yticklabels=names,xlim=(0,102),xlabel='Macro-F1 de validación (%)',title='Dos arquitecturas cercanas; una referencia más sencilla')
ax.invert_yaxis();ax.grid(axis='x',alpha=.15);fig.supxlabel('Puntos: semillas individuales · Rombo: media · Barra: ±1 desviación estándar',fontsize=9)
save(fig,'rendimiento')
f=pd.read_csv(R/'resultados_analizados/f1_por_clase.csv');mat=f.pivot(index='modelo',columns='clase',values='mean').loc[models,classes].to_numpy()*100
fig,ax=plt.subplots(figsize=(8,3.5),layout='constrained');im=ax.imshow(mat,cmap='YlGnBu',vmin=0,vmax=100,aspect='auto')
for i in range(3):
 for j in range(3):ax.text(j,i,f'{mat[i,j]:.1f}%',ha='center',va='center',color='white' if mat[i,j]>65 else '#132b44',weight='bold',fontsize=15)
ax.set(xticks=range(3),xticklabels=labels,yticks=range(3),yticklabels=names,title='Los núcleos estromales son la clase más difícil');fig.colorbar(im,ax=ax,label='F1 medio (%)');save(fig,'clases')
fig,axes=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
for ax,m,name in zip(axes,models,names):
 matrices=[]
 for seed in range(4101,4106):
  p=pd.read_csv(R/f'resultados/{m}_{seed}/predicciones_validacion.csv.gz')
  cm=confusion_matrix(p.clase_real,p.clase_predicha,labels=classes);matrices.append(cm/cm.sum(axis=1,keepdims=True)*100)
 cm=np.mean(matrices,axis=0);ax.imshow(cm,cmap='Blues',vmin=0,vmax=100)
 for i in range(3):
  for j in range(3):ax.text(j,i,f'{cm[i,j]:.1f}',ha='center',va='center',color='white' if cm[i,j]>60 else '#132b44')
 ax.set(xticks=range(3),xticklabels=labels,yticks=range(3),yticklabels=labels,title=name,xlabel='Predicción')
 ax.tick_params(axis='x',labelrotation=25)
axes[0].set_ylabel('Etiqueta de referencia');fig.suptitle('¿Con qué clase se confunde cada núcleo?');save(fig,'confusion')
b=pd.read_csv(R/'resultados_analizados/diferencias_bootstrap_paciente.csv');fig,ax=plt.subplots(figsize=(9,3.6),layout='constrained')
for i,row in b.iterrows():
 d=row.diferencia*100;lo=row.ic95_inferior*100;hi=row.ic95_superior*100
 ax.errorbar(d,i,xerr=[[d-lo],[hi-d]],fmt='o',color=colors[i],capsize=6,ms=8)
 ax.text(15.5,i,f'{d:+.2f} pp',va='center',fontsize=10)
ax.axvline(0,color='#64748b',ls='--',lw=1);ax.set(yticks=range(3),yticklabels=['ResNet18 − CNN local','MobileNetV2 − CNN local','MobileNetV2 − ResNet18'],xlabel='Diferencia de macro-F1 (puntos porcentuales)',xlim=(-3,19),title='La ventaja entre los dos mejores modelos es incierta');ax.invert_yaxis();ax.grid(axis='x',alpha=.15);save(fig,'incertidumbre')
fig,axes=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
for ax,m,name,c in zip(axes,models,names,colors):
 for seed in range(4101,4106):
  h=json.loads((R/f'resultados/{m}_{seed}/historia.json').read_text());x=[a['epoca'] for a in h];y=[a['val_macro_f1']*100 for a in h]
  ax.plot(x,y,color=c,alpha=.5,lw=1.4);best=np.argmax(y);ax.scatter(x[best],y[best],color=c,s=18)
 ax.set(title=name,xlabel='Época',ylim=(30,90),xlim=(1,25));ax.grid(alpha=.15)
axes[0].set_ylabel('Macro-F1 validación (%)');fig.suptitle('Cinco trayectorias de aprendizaje por modelo');save(fig,'aprendizaje')
e=pd.read_csv(R/'evidencias/seleccion_clases.csv');fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
for ax,part,title in zip(axes,['entrenamiento','validacion'],['Entrenamiento · 79 pacientes','Validación · 19 pacientes']):
 d=e[e.particion==part].set_index('clase').loc[classes]
 ax.barh(labels,d.incluidas,color=['#087f8c','#7c67aa','#b87320'])
 for i,(_,row) in enumerate(d.iterrows()):ax.text(row.incluidas+60,i,f'{int(row.incluidas):,} · {row.porcentaje:.1f}%',va='center',fontsize=10)
 ax.set(xlim=(0,d.incluidas.max()*1.47),title=title,xlabel='Recortes incluidos');ax.invert_yaxis();ax.grid(axis='x',alpha=.15)
fig.suptitle('Tres clases con distinta representación');save(fig,'balance')
q=pd.read_csv(R/'evidencias/calidad_por_imagen.csv');fig,axes=plt.subplots(1,3,figsize=(11,3.4),layout='constrained')
for ax,key,title,c in zip(axes,['gris_media','saturacion_media','laplaciano_var_tejido'],['Intensidad media (0–255)','Saturación media (0–1)','Varianza del Laplaciano'],colors):
 ax.hist(q[key],bins=35,color=c,alpha=.85);ax.axvline(q[key].median(),color='#172f45',ls='--');ax.set(xlabel=title,ylabel='Campos');ax.grid(axis='y',alpha=.15)
fig.suptitle('La apariencia varía entre los 1.182 campos de entrenamiento');save(fig,'calidad')
print('7 figuras SVG generadas con datos reales')
