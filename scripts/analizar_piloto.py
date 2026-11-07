from pathlib import Path
import json,itertools,hashlib
import numpy as np,pandas as pd
from sklearn.metrics import f1_score,confusion_matrix,roc_auc_score
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];O=R/'resultados_analizados';O.mkdir(exist_ok=True)
classes=['tumor_nonMitotic','lymphocyte','nonTILnonMQ_stromal'];models=['cnn_local','resnet18','mobilenet_v2'];seeds=list(range(4101,4106))
records=[];classrows=[];baseline=None;cms={};histories={}
for model,seed in itertools.product(models,seeds):
 d=R/'resultados'/f'{model}_{seed}';r=json.loads((d/'resultado.json').read_text());h=json.loads((d/'historia.json').read_text());p=(pd.read_csv(d/'predicciones_validacion.csv') if (d/'predicciones_validacion.csv').exists() else pd.read_csv(d/'predicciones_validacion.csv.gz')).sort_values('archivo').reset_index(drop=True)
 assert r['estado']=='COMPLETO_EXPLORATORIO' and r['semilla']==seed and r['modelo']==model
 assert len(p)==3571 and p.paciente.nunique()==19 and p.archivo.nunique()==3571
 keys=p[['archivo','paciente','clase_real']]
 if baseline is None:baseline=keys.copy();patients=sorted(p.paciente.unique())
 else:assert keys.equals(baseline)
 y=p.clase_real.map({v:i for i,v in enumerate(classes)}).to_numpy();yp=p.clase_predicha.map({v:i for i,v in enumerate(classes)}).to_numpy();probs=p[['p_tumor','p_linfocito','p_estroma']].to_numpy()
 assert np.isfinite(probs).all() and (probs>=0).all() and (probs<=1).all() and np.allclose(probs.sum(1),1,atol=1e-5)
 assert np.array_equal(probs.argmax(1),yp)
 score=f1_score(y,yp,labels=[0,1,2],average='macro');cm=confusion_matrix(y,yp,labels=[0,1,2]);assert np.isclose(score,r['validacion']['macro_f1'],atol=1e-12) and np.array_equal(cm,r['validacion']['confusion'])
 assert len(h)==r['epocas_ejecutadas'] and r['mejor_epoca']==max(h,key=lambda x:x['val_macro_f1'])['epoca']
 assert np.isclose(max(x['val_macro_f1'] for x in h),score)
 records.append(dict(modelo=model,semilla=seed,macro_f1=score,accuracy=r['validacion']['accuracy'],auc_ovr_macro=roc_auc_score(y,probs,multi_class='ovr',average='macro'),parametros=r['parametros'],minutos=r['segundos']/60,mejor_epoca=r['mejor_epoca'],epocas=r['epocas_ejecutadas']))
 for c in r['validacion']['clases']:classrows.append(dict(modelo=model,semilla=seed,**c))
 cms[model,seed]=np.stack([confusion_matrix(y[p.paciente==patient],yp[p.paciente==patient],labels=[0,1,2]) for patient in patients]);histories[model,seed]=h
runs=pd.DataFrame(records);runs.to_csv(O/'corridas_verificadas.csv',index=False);pd.DataFrame(classrows).to_csv(O/'metricas_clases.csv',index=False)
s=runs.groupby('modelo',sort=False).agg(n=('macro_f1','size'),macro_f1_media=('macro_f1','mean'),macro_f1_sd=('macro_f1','std'),accuracy=('accuracy','mean'),auc_macro=('auc_ovr_macro','mean'),minutos_media=('minutos','mean'),parametros=('parametros','first'));s.to_csv(O/'resumen_verificado.csv')
# Conditional uncertainty: paired patient bootstrap, fixed five trained seeds.
rng=np.random.default_rng(4101);w=rng.multinomial(len(patients),[1/len(patients)]*len(patients),size=5000)
def mf(cm):
 tp=np.diagonal(cm,axis1=-2,axis2=-1);den=cm.sum(-1)+cm.sum(-2)
 return np.divide(2*tp,den,out=np.zeros_like(tp,dtype=float),where=den>0).mean(-1)
boot={m:np.stack([mf(np.einsum('bp,pij->bij',w,cms[m,seed])) for seed in seeds]).mean(0) for m in models}
pairs=[]
for a,b in [('resnet18','cnn_local'),('mobilenet_v2','cnn_local'),('mobilenet_v2','resnet18')]:
 delta=boot[a]-boot[b];lo,hi=np.quantile(delta,[.025,.975]);pairs.append(dict(modelo_A=a,modelo_B=b,diferencia=float(s.loc[a,'macro_f1_media']-s.loc[b,'macro_f1_media']),ic95_inferior=lo,ic95_superior=hi,alcance='Exploratorio; validación usada para elegir época; 19 pacientes; cinco semillas fijas; IC marginal sin ajuste múltiple'))
pd.DataFrame(pairs).to_csv(O/'diferencias_bootstrap_paciente.csv',index=False)
fig,ax=plt.subplots(figsize=(8,4));x=np.arange(3);ax.bar(x,s.macro_f1_media,yerr=s.macro_f1_sd,capsize=5,color=['#4c6680','#137f87','#d99240']);ax.set_xticks(x,models);ax.set_ylim(0,1);ax.set_ylabel('Macro-F1 de validación');ax.set_title('Cinco semillas: media ± desviación estándar');fig.tight_layout();fig.savefig(R/'book/figuras/piloto_modelos.png',dpi=150);plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(12,3.8),layout='constrained')
for ax,m in zip(axes,models):
 for seed in seeds:
  h=histories[m,seed];ax.plot([v['epoca'] for v in h],[v['val_macro_f1'] for v in h],label=str(seed))
 ax.set_title(m);ax.set_xlabel('Época');ax.set_ylim(.3,1);ax.set_ylabel('Macro-F1 validación');ax.legend(fontsize=7)
fig.savefig(R/'book/figuras/piloto_curvas.png',dpi=150);plt.close(fig)
class_summary=pd.DataFrame(classrows).groupby(['modelo','clase']).f1.agg(['mean','std']);class_summary.to_csv(O/'f1_por_clase.csv')
summary={'corridas_verificadas':15,'recortes_por_corrida':3571,'pacientes_validacion':19,'semillas':seeds,'bootstrap_replicas':5000,'bootstrap_semilla':4101,'fuente':'resultados_RESULTADOS.zip','naturaleza':'piloto exploratorio; no evaluación confirmatoria'};(O/'auditoria.json').write_text(json.dumps(summary,indent=2))
lines=['# Resultados verificados del piloto','', '**Estado:** quince corridas completas, cinco por modelo. Se recalcularon macro-F1 y matrices de confusión a partir de 3.571 predicciones por corrida; coinciden con los informes originales. Se verificaron identidad de recortes/pacientes/etiquetas entre corridas, probabilidades y mejor época.','',s.to_markdown(floatfmt='.4f'),'','![Resultados](figuras/piloto_modelos.png)','', '**Interpretación:** MobileNetV2 obtiene el mayor promedio observado, pero su ventaja sobre ResNet18 es 0,00488 de macro-F1 (0,49 puntos porcentuales), inferior al margen operativo preliminar de 0,02. Esto no demuestra equivalencia ni superioridad. Ambos superan descriptivamente a la CNN local.','', '## Resultados por clase','',class_summary.to_markdown(floatfmt='.4f'),'','La clase estromal presenta el menor F1 promedio en los tres modelos. El análisis de errores debe priorizar esta categoría, sin atribuir automáticamente los fallos a ruido de anotación o mecanismos biológicos.','', '## Aprendizaje y costo','', '![Curvas](figuras/piloto_curvas.png)','', 'Los modelos paran en diferentes épocas. Los tiempos son los acumulados registrados por el entrenador en el Mac y pueden verse afectados por carga del equipo y reanudaciones; no constituyen un benchmark controlado de hardware. Los parámetros describen capacidad, no tiempo garantizado.','', '## Diferencias e incertidumbre exploratoria','',pd.DataFrame(pairs).drop(columns='alcance').to_markdown(floatfmt='.4f'),'','Se remuestrearon 19 pacientes con reemplazo, 5.000 veces; cada selección se aplicó de forma pareada a todos los modelos y semillas. Se recalculó macro-F1 agrupando las matrices de los pacientes seleccionados y se promedió sobre las cinco semillas fijas. Los IC percentiles marginales no tienen ajuste por comparaciones múltiples y no sustentan decisiones confirmatorias.','', 'La validación ya seleccionó la mejor época: este remuestreo no elimina ese optimismo. Tampoco incorpora incertidumbre por reentrenar en nuevas muestras de entrenamiento. No se reportan pruebas confirmatorias ni equivalencia.','', '## Decisión para el siguiente experimento','', 'El piloto permite estimar variación entre semillas y priorizar la comparación MobileNetV2–ResNet18. La selección bibliográfica de los tres baselines, el diseño con potencia suficiente y la protección del conjunto de prueba siguen pendientes. Las cinco semillas cumplen el mínimo del piloto, no garantizan potencia estadística.','', 'Fuentes reproducibles: `resultados/`, `resultados_analizados/` y `scripts/analizar_piloto.py`. No se usaron imágenes de prueba/reserva.']
(R/'book/08_resultados_piloto.md').write_text('\n'.join(lines),encoding='utf-8')
print(s.to_string());print(pd.DataFrame(pairs).drop(columns='alcance').to_string(index=False))
