from pathlib import Path
import json,shutil
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];D=R/'resultados_analizados/eda_pixeles_v2';F=R/'book/figuras'
h=pd.read_csv(D/'histogramas.csv');d=json.loads((D/'resumen.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal'];names=['Tumorales','Linfocitos','Estromales'];colors=['#176B87','#CC8C2D','#589675']
fig,axes=plt.subplots(2,3,figsize=(13,7),layout='constrained')
for row,(split,label) in enumerate([('train','Entrenamiento'),('validation','Validación')]):
 for col,c in enumerate('RGB'):
  ax=axes[row,col]
  for cls,name,color in zip(classes,names,colors):
   q=h[(h.particion==split)&(h.clase==cls)&(h.canal==c)].sort_values('bin_inferior');ax.plot(q.bin_inferior+4,q.pixeles/q.pixeles.sum()*100,label=name,color=color,lw=2)
  ax.set(title=f'{label} · canal {c}',xlabel='Intensidad (0–255)',ylabel='% de píxeles por intervalo',xlim=(0,255),ylim=(0,10));ax.grid(alpha=.15)
axes[0,0].legend(frameon=False)
fig.savefig(F/'histogramas_pixeles_v2.svg');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(12,5.2),layout='constrained')
for ax,key,title in zip(axes,['diagnostico_dominio','diagnostico_sitio'],['Predicción de partición · 104 pacientes','Predicción de TSS · 77 pacientes']):
 q=d[key];cm=np.array(q['confusion']);normalized=cm/cm.sum(1,keepdims=True)
 im=ax.imshow(normalized,vmin=0,vmax=1,cmap='Blues');labels=['Entrenamiento','Validación'] if key=='diagnostico_dominio' else q['clases'];ax.set_xticks(range(len(labels)),labels,rotation=35,ha='right');ax.set_yticks(range(len(labels)),labels);ax.set(title=title,xlabel='Predicción fuera del pliegue',ylabel='Etiqueta real')
 for i in range(len(labels)):
  for j in range(len(labels)):ax.text(j,i,str(cm[i,j]),ha='center',va='center',color='white' if normalized[i,j]>.55 else '#132A3B',fontsize=10)
fig.colorbar(im,ax=axes,shrink=.7,label='Proporción dentro de cada etiqueta real')
fig.savefig(F/'diagnosticos_pixeles_v2.svg');plt.close(fig)
for f in ['histogramas_pixeles_v2.svg','diagnosticos_pixeles_v2.svg']:shutil.copy(F/f,R/'assets'/f)
