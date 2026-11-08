from pathlib import Path
from literatura_panel import panel_literatura
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
 html.Header([html.Div('INGENIERÍA BIOMÉDICA · DEEP LEARNING',className='eyebrow'),html.H1('NuCLS: del núcleo al modelo'),html.P('Andrés Duarte Chaves · Entregable 1 · Estudio exploratorio'),html.Div('V2 · tres modelos · cierre de 11 semillas por modelo',className='badge')]),
 html.Div([html.Div([html.Strong(n),html.Span(t)],className='card') for n,t in [('16.588','recortes de desarrollo V2'),('104','pacientes de desarrollo V2'),('969','recortes de reserva'),('3','clases seleccionadas')]],className='cards'),
 dcc.Tabs(id='tabs',value='contexto',children=[dcc.Tab(label=l,value=v) for l,v in [('Problema','contexto'),('Imágenes','imagenes'),('Estado del arte','literatura'),('EDA','eda'),('Modelos y resultados','modelos'),('Discusión','discusion'),('Reproducibilidad','protocolo')]]),
 html.Nav([html.A('Informe JBook',href='https://aduartech81.github.io/NuCLS_DeepLearning/intro.html'),html.A('Notebook ejecutado',href='https://aduartech81.github.io/NuCLS_DeepLearning/10_eda_v2.html'),html.A('Código y evidencias',href='https://github.com/aduartech81/NuCLS_DeepLearning')],className='resource-nav'),html.Main(id='contenido'),html.Footer('NuCLS · Clasificación de recortes previamente localizados · Uso académico')],className='shell')
@app.callback(Output('contenido','children'),Input('tabs','value'))
def page(tab):
 if tab=='contexto':return [html.H2('Clasificar núcleos, con una evaluación por paciente'),md('''Entrada: recortes RGB **128×128** centrados en núcleos anotados. Salida: tumor no mitótico, linfocito o estromal no TIL/no macrófago.

**Pregunta V2:** ¿qué desempeño y variabilidad presentan una CNN compacta con BatchNorm, DenseNet121 y ResNet50 en la clasificación de tres categorías nucleares de NuCLS, bajo una partición por paciente y condiciones comunes de entrenamiento?

La clasificación nuclear permite resumir la composición celular de imágenes histológicas anotadas. En este estudio se evalúa el componente de clasificación a partir de una localización ya conocida. La comparación busca establecer una referencia experimental de desempeño, variabilidad y costo para las implementaciones evaluadas.

El estudio clasifica recortes centrados en núcleos previamente anotados de NuCLS. La selección de ventanas completamente contenidas en la imagen restringe la evaluación a los recortes que cumplen ese criterio.

El desarrollo V2 reúne **14.539 recortes de entrenamiento y 2.049 de validación**, de 83 y 21 pacientes, respectivamente. La reserva contiene 969 recortes de seis pacientes y no interviene en el EDA de píxeles. El protocolo V2 compara una CNN compacta, DenseNet121 y ResNet50; el cierre documentado contiene 11 semillas por modelo y 33 evaluaciones de reserva, con ResNet50 seleccionado mediante validación.

El piloto histórico contiene **14.428 recortes de 79 pacientes** para entrenamiento y **3.571 recortes de 19 pacientes** para validación. Las tres redes se entrenaron desde cero con cinco semillas cada una. Macro-F1 asigna igual peso a las tres clases, de modo que la frecuencia tumoral no determine por sí sola el promedio. Los recortes de un mismo paciente están correlacionados; el número de imágenes no equivale al número de unidades clínicas independientes. Las cifras corresponden a la selección del piloto y no a la totalidad de NuCLS.''')]
 if tab=='imagenes':return [html.H2('Imágenes histológicas y representación de entrada'),md('Recortes reales RGB de **128 × 128 píxeles**. La etiqueta corresponde al núcleo objetivo; pueden aparecer otros núcleos. Son ejemplos de entrenamiento, no predicciones.'),html.Label('Clase anotada',htmlFor='clase-galeria'),dcc.Dropdown(id='clase-galeria',options=[{'label':a,'value':b} for a,b in [('Tumoral no mitótico','tumor_nonMitotic'),('Linfocito','lymphocyte'),('Estromal','nonTILnonMQ_stromal')]],value='tumor_nonMitotic',clearable=False),html.Div(id='imagenes-clase'),md('**Procedencia:** doce ejemplos de la galería original del piloto, cuatro por clase, con pacientes verificados en entrenamiento. Selección ilustrativa, no aleatoria. No se utilizaron imágenes de validación o prueba.'),md('''Los recortes conservan el núcleo objetivo centrado y se admiten únicamente cuando la ventana de 128 × 128 cabe por completo en el campo. Esta regla evita introducir relleno artificial, pero modifica la muestra al excluir parte de los núcleos periféricos. La división RGB por 255 cambia la escala numérica; no normaliza la tinción ni iguala las distribuciones de color entre pacientes. Las rotaciones en múltiplos de 90° y la reflexión horizontal se aplican solo durante entrenamiento. No se utilizaron CLAHE ni filtros de realce.

El contexto puede contribuir a la predicción porque una ventana contiene tejido y, en ocasiones, otros núcleos. El experimento no separó mediante ablación la contribución del núcleo y la del entorno; la galería ilustra la representación de entrada, no explica las decisiones internas del modelo.''')]
 if tab=='discusion':return [md((R/'book/09_discusion.md').read_text())]
 if tab=='literatura':return panel_literatura(R)
 if tab=='eda':return [html.H2('Desarrollo v2: calidad y balance'),md('Se verificaron formato RGB, dimensiones 128×128 e integridad de los 16.588 recortes de desarrollo. La razón entre clases mayoritaria y minoritaria es 2,25 en entrenamiento y 3,22 en validación. No se imputan etiquetas ni píxeles de bordes; la ausencia de fallos de lectura no valida por sí sola las anotaciones. La separación por paciente y TSS se conserva durante el análisis.'),html.Img(src='/assets/eda_desarrollo_v2.svg',style={'width':'100%'},alt='Composición y retención por clase en entrenamiento y validación v2'),md('La partición v2 reúne **14.539 recortes de 83 pacientes** para entrenamiento y **2.049 de 21 pacientes** para validación. La proporción tumoral aumenta de 47,99% a 54,08%; la estromal disminuye de 21,34% a 16,79%. Macro-F1 equilibra el peso de las clases, pero no elimina ese cambio de composición.'),md('La retención en entrenamiento es 49,18% tumoral, 44,84% linfocitaria y 46,94% estromal. Los intervalos del gráfico se calcularon con 5.000 remuestreos de pacientes, condicionados a los TSS observados. La selección representa núcleos con ventanas interiores elegibles. Los análisis de píxeles siguientes corresponden a v2; el piloto histórico se presenta al final de esta pestaña.'),html.A('Análisis completo de la partición v2',href='https://aduartech81.github.io/NuCLS_DeepLearning/02_desarrollo_v2.html'),html.H3('Píxeles y desplazamiento entre grupos'),html.Img(src='/assets/histogramas_pixeles_v2.svg',style={'width':'100%'},alt='Histogramas RGB por clase y partición'),md('Las medias RGB de entrenamiento fueron 0,6392, 0,4592 y 0,6277; sus desviaciones fueron 0,2140, 0,2215 y 0,1743. El escalado por canal no equivale a normalización de tinción.'),html.Img(src='/assets/diagnosticos_pixeles_v2.svg',style={'width':'100%'},alt='Matrices de confusión por paciente para partición y TSS'),md('El diagnóstico de partición alcanzó AUC 0,7097 y exactitud balanceada 0,6770 en 104 pacientes. Los descriptores distinguen parcialmente entrenamiento y validación, sin identificar la causa del desplazamiento. La predicción de ocho TSS alcanzó 0,3983 de exactitud balanceada en 77 pacientes; no demuestra que la CNN use ese atajo. No se hallaron candidatos dHash con distancia ≤4 entre 29.790.411 pares, sin que esto descarte toda similitud perceptual.'),html.H3('Incertidumbre y heterogeneidad V2'),html.Img(src='/assets/eda_incertidumbre_v2.svg',style={'width':'100%'},alt='Intervalos exploratorios y distancias robustas por paciente'),md('Los IC 95% de exactitud balanceada son 0,5579–0,7846 para partición y 0,2937–0,5038 para procedencia. Se remuestrean pacientes con predicciones fijas, sin reentrenar. El análisis multivariado ajustado en entrenamiento prioriza cinco pacientes de entrenamiento y uno de validación; no confirma defectos ni excluye imágenes.'),html.H2('Piloto anterior: balance y calidad'),html.Label('Partición',htmlFor='particion'),dcc.Dropdown(id='particion',options=[{'label':'Entrenamiento','value':'entrenamiento'},{'label':'Validación','value':'validacion'}],value='entrenamiento',clearable=False),html.Div(id='balance'),html.H3('Calidad de campos de entrenamiento'),html.Label('Indicador',htmlFor='indicador'),dcc.Dropdown(id='indicador',options=[{'label':l,'value':v} for l,v in [('Intensidad gris','gris_media'),('Saturación','saturacion_media'),('Laplaciano en tejido','laplaciano_var_tejido'),('Fondo claro','fondo_claro_235')]],value='gris_media',clearable=False),html.Div(id='calidad'),md('**Interpretación:** son mediciones de campo, no del núcleo. Un Laplaciano bajo no demuestra desenfoque. No se excluyeron imágenes automáticamente. El análisis multivariado prioriza cuatro pacientes para revisión visual; no confirma defectos.'),md('**Alcance histórico:** esta auditoría de campos no incluyó similitud perceptual ni desplazamiento. V2 incorpora esos diagnósticos en las secciones superiores. La concordancia de etiquetas no se ha estimado sobre los recortes del proyecto.')]
 if tab=='modelos':return [md((R/'book/08_resultados_v2.md').read_text()),html.A('Anexo histórico: resultados del piloto',href='https://aduartech81.github.io/NuCLS_DeepLearning/08_resultados_piloto.html')]
 return [html.H2('Reproducibilidad V2'),md((R/'book/04_metodologia_v2.md').read_text()),html.A('Notebook EDA ejecutado',href='https://aduartech81.github.io/NuCLS_DeepLearning/10_eda_v2.html'),html.Br(),html.A('Plantilla de entrenamiento Colab',href='https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/colab/Experimento_NuCLS_v2.ipynb')]

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
