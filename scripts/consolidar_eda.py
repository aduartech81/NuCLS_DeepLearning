from pathlib import Path
import json,zipfile,shutil,hashlib,csv
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.covariance import MinCovDet
o=Path(__file__).resolve().parents[1];r=o

for d in ['evidencias','book/figuras','scripts']:(o/d).mkdir(exist_ok=True)
def load(z):
 return json.loads((o/'evidencias'/(Path(z).stem+'_resumen.json')).read_text())
s=load('CONTROL_PILOTO_QC_20261105_225210.zip');a=pd.DataFrame(s['seleccion']);a['retencion']=a.incluidas/a.origen;a['porcentaje']=a.incluidas/a.groupby('particion').incluidas.transform('sum')*100
a.to_csv(o/'evidencias/seleccion_clases.csv',index=False)
df=pd.read_csv(o/'evidencias/calidad_por_imagen.csv');assert len(df)==1182 and df.paciente.nunique()==79
# Exploración multivariada a nivel de paciente; sin inferencia ni exclusión.
features=['gris_media','gris_sd','saturacion_media','laplaciano_var_tejido','fondo_claro_235','entropia_gris']
p=df.groupby('paciente')[features].median();x=p.copy();x['laplaciano_var_tejido']=np.log1p(x['laplaciano_var_tejido'])
z=(x-x.median())/(x.quantile(.75)-x.quantile(.25));assert np.isfinite(z.to_numpy()).all()
m=MinCovDet(random_state=4101).fit(z);p['distancia_robusta_cuadrada']=m.mahalanobis(z);q=p.distancia_robusta_cuadrada.quantile(.95);p['revision_prioritaria']=p.distancia_robusta_cuadrada>=q;p.sort_values('distancia_robusta_cuadrada',ascending=False).to_csv(o/'evidencias/calidad_multivariada_pacientes.csv')
fig,ax=plt.subplots(1,2,figsize=(11,4),layout='constrained');names=['Tumor no mitótico','Linfocito','Estromal']
for part,color in [('entrenamiento','#197c87'),('validacion','#db9445')]:
 v=a[a.particion==part];offset=-.18 if part=='entrenamiento' else .18
 ax[0].bar(np.arange(3)+offset,v.porcentaje,.36,label=part,color=color);ax[1].bar(np.arange(3)+offset,v.retencion*100,.36,label=part,color=color)
for t,title in zip(ax,['Composición después de seleccionar','Retención desde anotaciones de origen']):t.set_xticks(range(3),names);t.set_ylabel('%');t.set_title(title);t.legend();t.spines[['top','right']].set_visible(False)
fig.savefig(o/'book/figuras/seleccion.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(11,4),layout='constrained');ax[0].scatter(df.gris_media,df.laplaciano_var_tejido,s=9,alpha=.4,color='#197c87');ax[0].set(xlabel='Intensidad gris media (campo)',ylabel='Varianza del Laplaciano (tejido)',title='1.182 campos de entrenamiento')
v=p.sort_values('distancia_robusta_cuadrada',ascending=False);ax[1].plot(range(1,len(v)+1),v.distancia_robusta_cuadrada,'o',ms=3);ax[1].axhline(q,color='#b65033',ls='--',label='Percentil empírico 95');ax[1].set(xlabel='Paciente ordenado por distancia',ylabel='Distancia robusta cuadrada',title='79 medianas por paciente');ax[1].legend();fig.savefig(o/'book/figuras/calidad.png',dpi=160);plt.close(fig)
print("Tablas y gráficas recalculadas")
