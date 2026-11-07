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

**Pregunta:** ¿qué desempeño y variabilidad alcanzan tres modelos básicos bajo condiciones comparables y sin pacientes compartidos entre entrenamiento y validación?

Esta tarea no identifica telocitos ni detecta núcleos en una imagen completa. La selección de recortes interiores limita la generalización a núcleos próximos a bordes.

**Métrica primaria:** macro-F1. **Unidad de independencia:** paciente. NuCLS completo y la selección del piloto tienen tamaños distintos.''')]
 if tab=='imagenes':return [html.H2('Qué recibe la red'),md('Recortes reales RGB de **128 × 128 píxeles**. La etiqueta corresponde al núcleo objetivo; pueden aparecer otros núcleos. Son ejemplos de entrenamiento, no predicciones.'),html.Label('Clase anotada',htmlFor='clase-galeria'),dcc.Dropdown(id='clase-galeria',options=[{'label':a,'value':b} for a,b in [('Tumoral no mitótico','tumor_nonMitotic'),('Linfocito','lymphocyte'),('Estromal','nonTILnonMQ_stromal')]],value='tumor_nonMitotic',clearable=False),html.Div(id='imagenes-clase'),md('**Procedencia:** doce ejemplos de la galería original del piloto, cuatro por clase, con pacientes verificados en entrenamiento. Selección ilustrativa, no aleatoria. No se utilizaron imágenes de validación o prueba.'),md('**Preparación:** recortes centrados sin relleno; RGB dividido por 255; rotaciones y reflexión horizontal solo en entrenamiento. Sin CLAHE ni normalización de tinción. La selección excluye núcleos cercanos a los bordes.')]
 if tab=='discusion':return [html.H2('Hallazgos y límites'),md('**1.** ResNet18 y MobileNetV2 superan descriptivamente a la CNN local.\n\n**2.** La diferencia entre los dos mejores promedios es de **0,49 puntos porcentuales**; su intervalo exploratorio cruza cero.\n\n**3.** Los núcleos estromales tienen el menor F1 en los tres modelos.'),html.Div('La validación seleccionó las épocas. Estos resultados son exploratorios y no demuestran superioridad en pacientes nuevos.',className='notice'),md('La clasificación se limita a recortes previamente localizados. No se ha demostrado detección en lámina completa, reconocimiento de telocitos ni utilidad clínica.'),html.A('Leer discusión completa',href='https://aduartech81.github.io/NuCLS_DeepLearning/09_discusion.html')]
 if tab=='literatura':return [html.H2('Estado del arte: evidencia y límites'),md((R/'book/03_literatura.md').read_text()),md('**Alcance de la revisión:** la síntesis narrativa no estima la frecuencia de uso de las tres arquitecturas exactas.')]
 if tab=='eda':return [html.H2('Balance, retención y calidad'),html.Label('Partición',htmlFor='particion'),dcc.Dropdown(id='particion',options=[{'label':'Entrenamiento','value':'entrenamiento'},{'label':'Validación','value':'validacion'}],value='entrenamiento',clearable=False),html.Div(id='balance'),html.H3('Calidad de campos de entrenamiento'),html.Label('Indicador',htmlFor='indicador'),dcc.Dropdown(id='indicador',options=[{'label':l,'value':v} for l,v in [('Intensidad gris','gris_media'),('Saturación','saturacion_media'),('Laplaciano en tejido','laplaciano_var_tejido'),('Fondo claro','fondo_claro_235')]],value='gris_media',clearable=False),html.Div(id='calidad'),md('**Interpretación:** son mediciones de campo, no del núcleo. Un Laplaciano bajo no demuestra desenfoque. No se excluyeron imágenes automáticamente. El análisis multivariado prioriza cuatro pacientes para revisión visual; no confirma defectos.'),md('**Alcance:** la auditoría no cuantifica similitud perceptual, concordancia de etiquetas ni desplazamiento entre particiones. No permite descartar esas fuentes de sesgo.')]
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
  return cards+[graph(fig),md('**Lectura:** media ± desviación estándar de cinco semillas. MobileNetV2 supera descriptivamente a ResNet18 en solo 0,49 puntos porcentuales; esto no demuestra superioridad.'),graph(classes),md('**Interpretación:** el F1 estromal aumenta de 53,69% con la CNN local a 69,85% con ResNet18 y 70,24% con MobileNetV2. Esta mejora no elimina la diferencia respecto a las otras clases ni identifica la causa de los errores.'),graph(intervals),md('**Incertidumbre:** IC percentiles exploratorios del 95 %, con 5.000 remuestreos pareados de 19 pacientes y cinco semillas fijas. Sin ajuste por comparaciones múltiples. La validación seleccionó épocas; no es una prueba independiente.')]

 return [html.H2('Protocolo y trazabilidad'),md((R/'book/04_protocolo.md').read_text()),md('**Reproducibilidad:** el repositorio contiene código, notebook ejecutado, evidencias y JBook. El dashboard presenta los resultados registrados y no ejecuta nuevos entrenamientos.')]
@app.callback(Output('imagenes-clase','children'),Input('clase-galeria','value'))
def images_for_class(cls):
 return html.Div([html.Figure([html.Img(src='/galeria/'+x['archivo'],alt='Recorte de entrenamiento: '+cls),html.Figcaption(x['paciente']+' · '+x['fila'])]) for x in gallery if x['clase']==cls],className='image-grid')
@app.callback(Output('balance','children'),Input('particion','value'))
def balance(part):
 d=selection[selection.particion==part]
 return [graph(px.bar(d,x='clase',y='incluidas',color='clase',hover_data=['origen','retencion'],title='Recortes incluidos por clase')),md(f'**{int(d.incluidas.sum()):,} recortes.** La tasa de retención va de {100*d.retencion.min():.1f} % a {100*d.retencion.max():.1f} %. La selección cambia la representación de las clases; macro-F1 evita que la clase más frecuente domine el promedio.')]
@app.callback(Output('calidad','children'),Input('indicador','value'))
def quality_plot(ind):return graph(px.histogram(quality,x=ind,nbins=35,title='Distribución en 1.182 campos de entrenamiento'))
if __name__=='__main__':app.run(host='127.0.0.1',port=int(os.environ.get('PORT',8050)),debug=False)
