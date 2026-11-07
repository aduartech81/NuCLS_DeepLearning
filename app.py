from pathlib import Path
import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
R=Path(__file__).resolve().parent
selection=pd.read_csv(R/'evidencias/seleccion_clases.csv')
quality=pd.read_csv(R/'evidencias/calidad_por_imagen.csv')
app=Dash(__name__,title='NuCLS | Andrés Duarte',suppress_callback_exceptions=True)
server=app.server
@server.get('/health')
def health(): return {'status':'ok','campos_eda':len(quality),'estado':'avance'}
def md(s):return dcc.Markdown(s)
def graph(fig):
 fig.update_layout(template='plotly_white',font_family='Arial',margin=dict(l=35,r=20,t=55,b=45),colorway=['#137f87','#d99240','#485994'])
 return dcc.Graph(figure=fig,config={'displaylogo':False})
app.layout=html.Div([
 html.Header([html.Div('INGENIERÍA BIOMÉDICA · DEEP LEARNING',className='eyebrow'),html.H1('NuCLS: del núcleo al modelo'),html.P('Andrés Duarte Chaves · Entregable 1 · Avance verificable'),html.Div('Piloto completo: 15 corridas · validación exploratoria',className='badge')]),
 html.Div([html.Div([html.Strong(n),html.Span(t)],className='card') for n,t in [('17.999','recortes del piloto'),('98','pacientes train + validación'),('1.182','campos del EDA'),('3','clases seleccionadas')]],className='cards'),
 dcc.Tabs(id='tabs',value='contexto',children=[dcc.Tab(label=l,value=v) for l,v in [('Problema','contexto'),('Estado del arte','literatura'),('EDA','eda'),('Modelos y resultados','modelos'),('Reproducibilidad','protocolo')]]),
 html.Main(id='contenido'),html.Footer('NuCLS · Clasificación de recortes previamente localizados · Uso académico')],className='shell')
@app.callback(Output('contenido','children'),Input('tabs','value'))
def page(tab):
 if tab=='contexto':return [html.H2('Clasificar núcleos, con una evaluación por paciente'),md('''Entrada: recortes RGB **128×128** centrados en núcleos anotados. Salida: tumor no mitótico, linfocito o estromal no TIL/no macrófago.

**Pregunta:** ¿qué desempeño y variabilidad alcanzan tres modelos básicos bajo condiciones comparables y sin pacientes compartidos entre entrenamiento y validación?

Esta tarea no identifica telocitos ni detecta núcleos en una imagen completa. La selección de recortes interiores limita la generalización a núcleos próximos a bordes.

**Métrica primaria:** macro-F1. **Unidad de independencia:** paciente. NuCLS completo y nuestra selección del piloto tienen tamaños distintos.''')]
 if tab=='literatura':return [html.H2('Estado del arte: evidencia y límites'),md((R/'book/03_literatura.md').read_text()),md('**Cierre pendiente:** búsqueda trazable en las bases exigidas, matriz de estudios, flujo PRISMA y frecuencia de las arquitecturas exactas. No presentar los candidatos actuales como selección definitiva.')]
 if tab=='eda':return [html.H2('Balance, retención y calidad'),html.Label('Partición',htmlFor='particion'),dcc.Dropdown(id='particion',options=[{'label':'Entrenamiento','value':'entrenamiento'},{'label':'Validación','value':'validacion'}],value='entrenamiento',clearable=False),html.Div(id='balance'),html.H3('Calidad de campos de entrenamiento'),html.Label('Indicador',htmlFor='indicador'),dcc.Dropdown(id='indicador',options=[{'label':l,'value':v} for l,v in [('Intensidad gris','gris_media'),('Saturación','saturacion_media'),('Laplaciano en tejido','laplaciano_var_tejido'),('Fondo claro','fondo_claro_235')]],value='gris_media',clearable=False),html.Div(id='calidad'),md('**Interpretación:** son mediciones de campo, no del núcleo. Un Laplaciano bajo no demuestra desenfoque. No se excluyeron imágenes automáticamente. El análisis multivariado prioriza cuatro pacientes para revisión visual; no confirma defectos.'),md('**Pendientes:** casi duplicados, revisión de etiquetas y desplazamiento entre particiones.')]
 if tab=='modelos':
  cards=[html.H2('Tres candidatos en evaluación'),md('CNN local · ResNet18 · MobileNetV2. Desde cero, cinco semillas por candidato. La literatura debe justificar la selección final. Validación se usa para elegir época; no equivale a prueba independiente.')]
  f=R/'resultados/resumen_modelos.csv'
  if not f.exists():return cards+[html.Div('Resultados del entrenamiento pendientes de incorporar. No se muestran métricas simuladas.',className='notice')]
  d=pd.read_csv(f);required={'modelo','ejecuciones','macro_f1_media','macro_f1_sd'}
  if not required.issubset(d.columns):return cards+[md('El resumen no tiene el esquema esperado. Revisar el archivo antes de publicarlo.')]
  return cards+[graph(px.bar(d,x='modelo',y='macro_f1_media',error_y='macro_f1_sd',hover_data=['ejecuciones'],title='Macro-F1 de validación: media y desviación entre semillas')),md('Las barras expresan desviación estándar, no intervalos de confianza. Comprobar cinco ejecuciones completas por modelo. No inferir superioridad con esta figura.')]
 return [html.H2('Protocolo y trazabilidad'),md((R/'book/04_protocolo.md').read_text()),md('**Publicación:** el repositorio debe conservar código, notebook ejecutado, evidencias y JBook. El entrenamiento se ejecuta separadamente; el servidor del dashboard solo presenta resultados.')]
@app.callback(Output('balance','children'),Input('particion','value'))
def balance(part):
 d=selection[selection.particion==part]
 return [graph(px.bar(d,x='clase',y='incluidas',color='clase',hover_data=['origen','retencion'],title='Recortes incluidos por clase')),md(f'**{int(d.incluidas.sum()):,} recortes.** La tasa de retención va de {100*d.retencion.min():.1f} % a {100*d.retencion.max():.1f} %. La selección cambia la representación de las clases; macro-F1 evita que la clase más frecuente domine el promedio.')]
@app.callback(Output('calidad','children'),Input('indicador','value'))
def quality_plot(ind):return graph(px.histogram(quality,x=ind,nbins=35,title='Distribución en 1.182 campos de entrenamiento'))
if __name__=='__main__':app.run(host='127.0.0.1',port=int(os.environ.get('PORT',8050)),debug=False)
