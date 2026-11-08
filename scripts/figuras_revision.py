from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'evidencias/literatura/progreso_lectura.json').read_text())
plt.rcParams.update({'font.size':11})
def box(ax,x,y,w,h,text,fc='#eef7f7'):
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.01',facecolor=fc,edgecolor='#087f8c'))
 ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=10.5)
def arrow(ax,a,b):ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#64748b'})
fig,ax=plt.subplots(figsize=(11,7));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
box(ax,.23,.84,.54,.11,'Identificación: 1.717 registros\nScopus 1.097 · WoS 328 · IEEE 292')
box(ax,.23,.64,.54,.11,'Ventana 2018–2026: 1.648\n69 registros fuera del periodo')
box(ax,.23,.44,.54,.11,'Depuración DOI: 1.330 unidades\n318 repeticiones agrupadas')
box(ax,.02,.19,.43,.13,f"Decisión o derivación: {p['registros_con_decision']}\nNo equivale a inclusión definitiva")
box(ax,.55,.19,.43,.13,f"Sin decisión: {p['registros_sin_decision']}\nNo se cuentan como exclusiones",'#fff5e9')
for a,b in [((.5,.84),(.5,.75)),((.5,.64),(.5,.55)),((.4,.44),(.235,.32)),((.6,.44),(.765,.32))]:arrow(ax,a,b)
ax.text(.5,.06,'Flujo documental parcial · Sin cifra de inclusión final\nSelección asistida por IA; sin segundo revisor independiente',ha='center',fontsize=11,color='#475569')
for folder in ['book/figuras','assets']:fig.savefig(R/folder/'flujo_literatura.svg',bbox_inches='tight')
plt.close(fig)
fig,ax=plt.subplots(figsize=(12,5));ax.axis('off');ax.set(xlim=(0,1),ylim=(0,1))
lines=[('CNN compacta',['RGB 128×128','Conv 36 → 48\nBN + ReLU + pooling','Cuadrícula 5×5\nDensas 512 → 512','3 logits']),('DenseNet121',['RGB 128×128','Bloques densos\n6 / 12 / 24 / 16','Promedio global\n1.024 características','3 logits']),('ResNet50',['RGB 128×128','Bloques residuales\n3 / 4 / 6 / 3','Promedio global\n2.048 características','3 logits'])]
for i,(name,labels) in enumerate(lines):
 y=.72-i*.31;ax.text(.02,y+.16,name,weight='bold',color='#075e68')
 for j,label in enumerate(labels):
  x=.02+j*.25;box(ax,x,y,.21,.13,label)
  if j<3:arrow(ax,(x+.215,y+.065),(x+.248,y+.065))
fig.savefig(R/'book/figuras/arquitecturas_referencias.svg',bbox_inches='tight')
