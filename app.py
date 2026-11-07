from pathlib import Path
import os
import json
from flask import send_from_directory, abort
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
R=Path(__file__).resolve().parent
selection=pd.read_csv(R/'evidencias/seleccion_clases.csv')
quality=pd.read_csv(R/'evidencias/calidad_por_imagen.csv')
app=Dash(__name__,title='NuCLS | Andrés Duarte',suppress_callback_exceptions=True)
server=app.server
gallery=json.loads((R/'evidencias/galeria_train.json').read_text())['registros']
@server.get('/galeria/<filename>')
def gallery_image(filename):
 if filename not in {x['archivo'] for x in gallery}: abort(404)
 return send_from_directory(R/'book/figuras/galeria',filename)

@server.get('/health')
def health(): return {'status':'ok','campos_eda':len(quality),'estado':'avance'}
def md(s):return dcc.Markdown(s)
def graph(fig):
 fig.update_layout(template='plotly_white',font_family='Arial',margin=dict(l=35,r=20,t=55,b=45),colorway=['#137f87','#d99240','#485994'])
 return dcc.Graph(figure=fig,config={'displaylogo':False})
app.layout=html.Div([
 html.Header([html.Div('INGENIERÍA BIOMÉDICA · DEEP LEARNING',className='eyebrow'),html.H1('NuCLS: del núcleo al modelo'),html.P('Andrés Duarte Chaves · Entregable 1 · Estudio exploratorio'),html.Div('Piloto completo: 15 corridas · validación exploratoria',className='badge')]),
 html.Div([html.Div([html.Strong(n),html.Span(t)],className='card') for n,t in [('17.999','recortes del piloto'),('98','pacientes train + validación'),('1.182','campos del EDA'),('3','clases seleccionadas')]],className='cards'),
 dcc.Tabs(id='tabs',value='contexto',children=[dcc.Tab(label=l,value=v) for l,v in [('Problema','contexto'),('Imágenes','imagenes'),('Estado del arte','literatura'),('EDA','eda'),('Modelos y resultados','modelos'),('Discusión','discusion'),('Reproducibilidad','protocolo')]]),
 html.Nav([html.A('Informe JBook',href='https://aduartech81.github.io/NuCLS_DeepLearning/intro.html'),html.A('Notebook ejecutado',href='https://aduartech81.github.io/NuCLS_DeepLearning/07_analisis_ejecutado.html'),html.A('Código y evidencias',href='https://github.com/aduartech81/NuCLS_DeepLearning')],className='resource-nav'),html.Main(id='contenido'),html.Footer('NuCLS · Clasificación de recortes previamente localizados · Uso académico')],className='shell')
@app.callback(Output('contenido','children'),Input('tabs','value'))
def page(tab):
 if tab=='contexto':return [html.H2('Clasificar núcleos, con una evaluación por paciente'),md('''Entrada: recortes RGB **128×128** centrados en núcleos anotados. Salida: tumor no mitótico, linfocito o estromal no TIL/no macrófago.

**Pregunta de investigación:** ¿qué desempeño y variabilidad presentan una CNN local, ResNet18 y MobileNetV2 en la clasificación de tres categorías nucleares de NuCLS, bajo una partición por paciente y condiciones comunes de entrenamiento?

La clasificación nuclear permite resumir la composición celular de imágenes histológicas anotadas. En este estudio se evalúa el componente de clasificación a partir de una localización ya conocida. La comparación busca establecer una referencia experimental de desempeño, variabilidad y costo para las implementaciones evaluadas.

El estudio clasifica recortes centrados en núcleos previamente anotados de NuCLS. La selección de ventanas completamente contenidas en la imagen restringe la evaluación a los recortes que cumplen ese criterio.

La selección contiene **14.428 recortes de 79 pacientes** para entrenamiento y **3.571 recortes de 19 pacientes** para validación. Las tres redes se entrenaron desde cero con cinco semillas cada una. Macro-F1 asigna igual peso a las tres clases, de modo que la frecuencia tumoral no determine por sí sola el promedio. Los recortes de un mismo paciente están correlacionados; el número de imágenes no equivale al número de unidades clínicas independientes. Las cifras corresponden a la selección del piloto y no a la totalidad de NuCLS.''')]
 if tab=='imagenes':return [html.H2('Imágenes histológicas y representación de entrada'),md('Recortes reales RGB de **128 × 128 píxeles**. La etiqueta corresponde al núcleo objetivo; pueden aparecer otros núcleos. Son ejemplos de entrenamiento, no predicciones.'),html.Label('Clase anotada',htmlFor='clase-galeria'),dcc.Dropdown(id='clase-galeria',options=[{'label':a,'value':b} for a,b in [('Tumoral no mitótico','tumor_nonMitotic'),('Linfocito','lymphocyte'),('Estromal','nonTILnonMQ_stromal')]],value='tumor_nonMitotic',clearable=False),html.Div(id='imagenes-clase'),md('**Procedencia:** doce ejemplos de la galería original del piloto, cuatro por clase, con pacientes verificados en entrenamiento. Selección ilustrativa, no aleatoria. No se utilizaron imágenes de validación o prueba.'),md('''Los recortes conservan el núcleo objetivo centrado y se admiten únicamente cuando la ventana de 128 × 128 cabe por completo en el campo. Esta regla evita introducir relleno artificial, pero modifica la muestra al excluir parte de los núcleos periféricos. La división RGB por 255 cambia la escala numérica; no normaliza la tinción ni iguala las distribuciones de color entre pacientes. Las rotaciones en múltiplos de 90° y la reflexión horizontal se aplican solo durante entrenamiento. No se utilizaron CLAHE ni filtros de realce.

El contexto puede contribuir a la predicción porque una ventana contiene tejido y, en ocasiones, otros núcleos. El experimento no separó mediante ablación la contribución del núcleo y la del entorno; la galería ilustra la representación de entrada, no explica las decisiones internas del modelo.''')]
 if tab=='discusion':return [html.H2('Contrastes ampliados del piloto'),md((R/'book/08_resultados_piloto.md').read_text().split('## Contrastes globales y discriminación')[1]),md((R/'book/09_discusion.md').read_text()),html.H3('Síntesis cuantitativa'),html.H2('Hallazgos y límites'),md('**1.** ResNet18 y MobileNetV2 superan descriptivamente a la CNN local.\n\n**2.** La diferencia entre los dos mejores promedios es de **0,49 puntos porcentuales**; su intervalo exploratorio cruza cero.\n\n**3.** Los núcleos estromales tienen el menor F1 en los tres modelos.'),html.Div('La validación seleccionó las épocas. Estos resultados son exploratorios y no demuestran superioridad en pacientes nuevos.',className='notice'),md('La evaluación corresponde a la clasificación de recortes nucleares previamente localizados. Sus resultados no acreditan detección en lámina completa ni utilidad clínica.'),html.A('Leer discusión completa',href='https://aduartech81.github.io/NuCLS_DeepLearning/09_discusion.html')]
 if tab=='literatura':return [html.H2('Estado del arte: evidencia y límites'),md((R/'book/03_literatura.md').read_text()),md('**Alcance de la revisión:** la síntesis narrativa no estima la frecuencia de uso de las tres arquitecturas exactas.')]
 if tab=='eda':return [html.H2('Desarrollo v2: composición y retención'),html.Img(src='/assets/eda_desarrollo_v2.svg',style={'width':'100%'},alt='Composición y retención por clase en entrenamiento y validación v2'),md('La partición v2 reúne **14.539 recortes de 83 pacientes** para entrenamiento y **2.049 de 21 pacientes** para validación. La proporción tumoral aumenta de 47,99% a 54,08%; la estromal disminuye de 21,34% a 16,79%. Macro-F1 equilibra el peso de las clases, pero no elimina ese cambio de composición.'),md('La retención en entrenamiento es 49,18% tumoral, 44,84% linfocitaria y 46,94% estromal. Los intervalos del gráfico se calcularon con 5.000 remuestreos de pacientes, condicionados a los TSS observados. La selección representa núcleos con ventanas interiores elegibles. Las mediciones siguientes corresponden al piloto anterior.'),html.A('Análisis completo de la partición v2',href='https://aduartech81.github.io/NuCLS_DeepLearning/02_desarrollo_v2.html'),html.H3('Píxeles y desplazamiento entre grupos'),html.Img(src='/assets/histogramas_pixeles_v2.svg',style={'width':'100%'},alt='Histogramas RGB por clase y partición'),md('Las medias RGB de entrenamiento fueron 0,6392, 0,4592 y 0,6277; sus desviaciones fueron 0,2140, 0,2215 y 0,1743. El escalado por canal no equivale a normalización de tinción.'),html.Img(src='/assets/diagnosticos_pixeles_v2.svg',style={'width':'100%'},alt='Matrices de confusión por paciente para partición y TSS'),md('El diagnóstico de partición alcanzó AUC 0,7097 y exactitud balanceada 0,6770 en 104 pacientes. Los descriptores distinguen parcialmente entrenamiento y validación, sin identificar la causa del desplazamiento. La predicción de ocho TSS alcanzó 0,3983 de exactitud balanceada en 77 pacientes; no demuestra que la CNN use ese atajo. No se hallaron candidatos dHash con distancia ≤4 entre 29.790.411 pares, sin que esto descarte toda similitud perceptual.'),html.H2('Piloto anterior: balance y calidad'),html.Label('Partición',htmlFor='particion'),dcc.Dropdown(id='particion',options=[{'label':'Entrenamiento','value':'entrenamiento'},{'label':'Validación','value':'validacion'}],value='entrenamiento',clearable=False),html.Div(id='balance'),html.H3('Calidad de campos de entrenamiento'),html.Label('Indicador',htmlFor='indicador'),dcc.Dropdown(id='indicador',options=[{'label':l,'value':v} for l,v in [('Intensidad gris','gris_media'),('Saturación','saturacion_media'),('Laplaciano en tejido','laplaciano_var_tejido'),('Fondo claro','fondo_claro_235')]],value='gris_media',clearable=False),html.Div(id='calidad'),md('**Interpretación:** son mediciones de campo, no del núcleo. Un Laplaciano bajo no demuestra desenfoque. No se excluyeron imágenes automáticamente. El análisis multivariado prioriza cuatro pacientes para revisión visual; no confirma defectos.'),md('**Alcance:** la auditoría no cuantifica similitud perceptual, concordancia de etiquetas ni desplazamiento entre particiones. No permite descartar esas fuentes de sesgo.')]
 if tab=='modelos':
  cards=[html.H2('Tres candidatos en evaluación'),md('CNN local · ResNet18 · MobileNetV2. Desde cero, cinco semillas por candidato. La selección es exploratoria; la revisión no establece que sean las tres arquitecturas más frecuentes. Validación se usa para elegir época; no equivale a prueba independiente.')]
  f=R/'resultados/resumen_modelos.csv'
  if not f.exists():return cards+[html.Div('Los resultados no están disponibles en esta instancia del dashboard.',className='notice')]
  d=pd.read_csv(f);required={'modelo','ejecuciones','macro_f1_media','macro_f1_sd'}
  if not required.issubset(d.columns):return cards+[md('El resumen no puede visualizarse porque su estructura no es compatible.')]
  names={'cnn_local':'CNN local','resnet18':'ResNet18','mobilenet_v2':'MobileNetV2'}
  d['Modelo']=d.modelo.map(names);d['Macro-F1 (%)']=100*d.macro_f1_media;d['DE (%)']=100*d.macro_f1_sd
  fig=px.bar(d,x='Modelo',y='Macro-F1 (%)',error_y='DE (%)',color='Modelo',text_auto='.1f',title='Resultados cercanos entre ResNet18 y MobileNetV2',range_y=[0,100],color_discrete_sequence=['#64748b','#087f8c','#b87320'])
  cl=pd.read_csv(R/'resultados_analizados/f1_por_clase.csv');cl['Modelo']=cl.modelo.map(names)
  cl['Clase']=cl.clase.map({'tumor_nonMitotic':'Tumoral','lymphocyte':'Linfocito','nonTILnonMQ_stromal':'Estromal'})
  cl['F1 (%)']=100*cl['mean'];cl['DE (%)']=100*cl['std']
  classes=px.bar(cl,x='Clase',y='F1 (%)',color='Modelo',barmode='group',error_y='DE (%)',range_y=[0,100],title='La clase estromal presenta el menor F1',color_discrete_map={'CNN local':'#64748b','ResNet18':'#087f8c','MobileNetV2':'#b87320'})
  dif=pd.read_csv(R/'resultados_analizados/diferencias_bootstrap_paciente.csv')
  labels=[names[a]+' − '+names[b] for a,b in zip(dif.modelo_A,dif.modelo_B)]
  intervals=go.Figure(go.Scatter(x=100*dif.diferencia,y=labels,mode='markers',error_x=dict(type='data',symmetric=False,array=100*(dif.ic95_superior-dif.diferencia),arrayminus=100*(dif.diferencia-dif.ic95_inferior)),marker=dict(size=11,color='#087f8c')))
  intervals.add_vline(x=0,line_dash='dash',line_color='#64748b');intervals.update_layout(title='Diferencias e incertidumbre exploratoria',xaxis_title='Diferencia de macro-F1 (puntos porcentuales)')
  return cards+[graph(fig),md('MobileNetV2 obtuvo un macro-F1 medio de **82,39%**, frente a **81,91%** de ResNet18 y **72,03%** de la CNN local. La ventaja frente a la CNN local fue de 10,36 puntos porcentuales; frente a ResNet18 se redujo a 0,49 puntos, por debajo del margen exploratorio de dos puntos. Las barras representan desviación estándar entre cinco entrenamientos, no intervalos de confianza. La menor dispersión de MobileNetV2 describe estabilidad en esta partición y no garantiza generalización externa.'),graph(classes),md('El F1 estromal aumenta de **53,69%** con la CNN local a **69,85%** con ResNet18 y **70,24%** con MobileNetV2. En MobileNetV2, la mejora frente a la CNN local es de 16,56 puntos para estroma, 10,77 para linfocitos y 3,75 para núcleos tumorales. La ganancia global se acompaña de una mejora especialmente marcada en la categoría de menor desempeño. Sin embargo, ResNet18 presenta mayor sensibilidad estromal: **71,91%**, frente a **66,97%** de MobileNetV2. Por tanto, el mayor F1 global no implica mejor reconocimiento de todas las clases. Estas métricas no permiten atribuir causalmente los errores a morfología, tinción o anotación.'),graph(intervals),md('La diferencia MobileNetV2–ResNet18 presenta un intervalo exploratorio de **−1,08 a +2,01 puntos porcentuales**. Los datos son compatibles tanto con una pequeña ventaja de ResNet18 como con una ventaja de MobileNetV2; no establecen superioridad ni equivalencia. Los intervalos proceden de 5.000 remuestreos pareados de 19 pacientes, conservando juntas sus observaciones y fijas las cinco redes entrenadas. Son intervalos marginales sin ajuste múltiple. La selección de épocas en esta misma validación introduce optimismo que el remuestreo no elimina.')]

 return [html.H2('Protocolo y trazabilidad'),md((R/'book/04_protocolo.md').read_text()),md('**Reproducibilidad:** el repositorio contiene código, notebook ejecutado, evidencias y JBook. El dashboard presenta los resultados registrados y no ejecuta nuevos entrenamientos.')]
@app.callback(Output('imagenes-clase','children'),Input('clase-galeria','value'))
def images_for_class(cls):
 return html.Div([html.Figure([html.Img(src='/galeria/'+x['archivo'],alt='Recorte de entrenamiento: '+cls),html.Figcaption(x['paciente']+' · '+x['fila'])]) for x in gallery if x['clase']==cls],className='image-grid')
@app.callback(Output('balance','children'),Input('particion','value'))
def balance(part):
 d=selection[selection.particion==part]
 return [graph(px.bar(d,x='clase',y='incluidas',color='clase',hover_data=['origen','retencion'],title='Recortes incluidos por clase')),md(f'**{int(d.incluidas.sum()):,} recortes.** La tasa de retención va de {100*d.retencion.min():.1f} % a {100*d.retencion.max():.1f} %. La selección cambia la representación de las clases; macro-F1 evita que la clase más frecuente domine el promedio.')]
@app.callback(Output('calidad','children'),Input('indicador','value'))
def quality_plot(ind):
 labels={'gris_media':'Intensidad gris media','saturacion_media':'Saturación media','laplaciano_var_tejido':'Varianza del Laplaciano en tejido','fondo_claro_235':'Fracción de fondo claro'}
 explanations={
 'gris_media':'La intensidad media resume conjuntamente tejido y fondo. Su variación puede reflejar diferencias de adquisición, tinción o composición del campo; no permite distinguir por sí sola esas causas. El piloto conservó los valores originales y aplicó únicamente división por 255.',
 'saturacion_media':'La saturación cuantifica la intensidad relativa del color. Su heterogeneidad documenta diferencias de apariencia entre campos, pero no demuestra un defecto de tinción. No se aplicó normalización de color ni se atribuyó causalmente el rendimiento a este indicador.',
 'laplaciano_var_tejido':'La varianza del Laplaciano responde a cambios locales de intensidad. Un valor bajo puede corresponder a menor detalle o a tejido homogéneo, además de desenfoque; por ello no se utilizó como umbral automático de exclusión.',
 'fondo_claro_235':'El indicador corresponde a la fracción de píxeles cuyos tres canales alcanzan al menos 235. El fondo modifica la información disponible dentro de una ventana y puede actuar como señal contextual. El umbral no identifica de forma exhaustiva todos los espacios sin tejido, especialmente los que conservan coloración.'}
 v=quality[ind].dropna();q=v.quantile([.05,.5,.95])
 fig=px.histogram(quality,x=ind,nbins=35,labels={ind:labels[ind]},title=labels[ind]+' en campos de entrenamiento')
 fig.add_vline(x=float(q.loc[.5]),line_dash='dash',line_color='#b87320')
 return [graph(fig),md(f'En los **{len(v):,} campos**, la mediana es **{q.loc[.5]:.3f}** y el intervalo entre percentiles 5 y 95 es **{q.loc[.05]:.3f}–{q.loc[.95]:.3f}**. Estos percentiles describen dispersión entre campos; no son un intervalo de confianza. '+explanations[ind])]

if __name__=='__main__':app.run(host='127.0.0.1',port=int(os.environ.get('PORT',8050)),debug=False)
