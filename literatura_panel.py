"""Síntesis bibliográfica para el dashboard; detalles y fuentes en el JBook."""
import json
from dash import dcc, html

def panel_literatura(root):
    p=json.loads((root/'evidencias/literatura/progreso_lectura.json').read_text())
    def md(text): return dcc.Markdown(text, link_target='_blank')
    def section(title,text):
        return html.Details([html.Summary(title),md(text)],className='literature-detail')
    return [
        html.H2('Estado del arte: de la apariencia nuclear al contexto'),
        md('La comparación de redes depende de **qué se clasifica, qué información contiene la imagen y cómo se separan los datos**. La literatura orienta esas decisiones; una puntuación publicada en otro tejido no constituye un objetivo directamente equivalente para NuCLS.'),
        html.Div([html.Div([html.Strong(a),html.Span(b)],className='card') for a,b in [('1.717','registros exportados'),('1.330','unidades tras depuración'),(str(p['registros_con_decision']),'registros con decisión o derivación'),('3','arquitecturas seleccionadas para V2')]],className='cards'),
        html.H3('Tres decisiones sustentadas por los antecedentes'),
        html.Div([
            html.Article([html.H4('Representación local'),html.P('Las CNN compactas ofrecen una referencia de menor capacidad. RCCNet documenta comparadores concretos; su F1 ponderado en colon no equivale al macro-F1 de tres clases de NuCLS.')]),
            html.Article([html.H4('Contexto alrededor del núcleo'),html.P('En PanNuke, ResNet50 alcanza un F1 conectivo de 71,49% con contexto y 63,21% sin él: 8,28 puntos de diferencia. El resultado motiva declarar el contenido de cada ventana, pero no demuestra que toda señal contextual sea útil en otros conjuntos.')]),
            html.Article([html.H4('Evaluación comparable'),html.P('OLConvNet separa CNN independientes de sistemas híbridos. Sus resultados no deben mezclarse. En NuCLS se mantienen entrada, etiquetas y presupuesto comunes, con separación por paciente y TSS.')])
        ],className='literature-grid'),
        html.H3('Selección de arquitecturas V2'),
        md('''| Modelo | Respaldo documental | Función en la comparación |
|---|---|---|
| softmaxCNN con BatchNorm, adaptada | Comparador descrito en RCCNet | Referencia compacta: 898.687 parámetros |
| DenseNet121 | Clasificador independiente en OLConvNet | Conexiones densas: 6.956.931 parámetros |
| ResNet50 | OLConvNet y comparación PanNuke | Conexiones residuales: 23.514.179 parámetros |

La selección combina evidencia de uso, complejidad y diversidad estructural. **No establece que sean las tres arquitecturas más frecuentes de todo el campo.** Las implementaciones V2 se entrenan desde cero; los resultados publicados con transferencia no se interpretan como reproducciones de este protocolo.'''),
        section('Comparación crítica de estudios', '''| Estudio | Hallazgo relevante | Límite de extrapolación |
|---|---|---|
| [RCCNet, Basha et al.](https://doi.org/10.1109/ICARCV.2018.8581147) | Comparadores CNN compactos y adaptados | Cuatro clases, otra resolución y F1 ponderado; separación por paciente no establecida en la descripción revisada |
| [OLConvNet](https://doi.org/10.1145/3345318) | ResNet50 aislada: F1 0,8892; DenseNet121: 0,8706 | La generación sintética se describe antes de dividir datos; riesgo de dependencia. No comparar directamente con NuCLS |
| [Sánchez-Torres et al.](https://doi.org/10.1155/acis/4540418) | El contexto modifica el F1 por categoría | Cinco clases PanNuke; sin dispersión en la tabla extraída |
| [GrEp, Frei et al.](https://doi.org/10.1016/j.patcog.2025.112197) | Ablación de ResNet18 sin refinamiento por grafo | Clasificación epitelial binaria con preentrenamiento; antecedente, no modelo V2 |

F1 ponderado, macro-F1, F1 por clase y métricas de segmentación responden a preguntas distintas. No se construye un ranking entre estudios con protocolos incompatibles.'''),
        section('Tendencias recientes identificadas en resúmenes', '''TexSegNet incorpora textura y atención; MOSAIC combina escala y orientación; BDCNet incorpora relaciones espaciales; HistoPLUS y KongNet amplían la caracterización celular y la evaluación entre conjuntos. HistoMSC describe clasificación de parches con contexto y representación de láminas.

Estos antecedentes se identificaron en los resúmenes exportados. Sus comparadores exactos y protocolos requieren lectura de texto completo; **no se agregan al conteo de arquitecturas verificadas**. La distinción evita atribuir a una red aislada el rendimiento de un sistema completo de detección, segmentación y clasificación.

[Referencias y decisiones individuales](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/cribado_adicional_80.csv).'''),
        section('Búsqueda, selección y alcance', f'''Se integraron exportaciones de Scopus (1.097), Web of Science (328) e IEEE Xplore (292). Tras separar 69 registros fuera de 2018–2026 y agrupar 318 repeticiones por DOI, se conservaron 1.330 unidades.

Existen **{p['registros_con_decision']} registros con decisión o derivación de lectura** y **{p['registros_sin_decision']} sin decisión**. Estos conteos no equivalen a estudios incluidos. La revisión sigue siendo dirigida y parcial; no se presenta como revisión sistemática exhaustiva ni como flujo PRISMA completo.

Las tareas de detección, segmentación, diagnóstico de láminas y clasificación nuclear se distinguen durante la selección. Las exclusiones por título y las lecturas de resumen se documentan por separado, sin atribuir una segunda revisión independiente inexistente.'''),
        html.H3('Aporte del experimento'),
        md('El proyecto evalúa tres clasificadores sobre los mismos recortes y etiquetas, con condiciones comunes y variabilidad entre ejecuciones. Su aporte es una comparación experimental reproducible. La separación por paciente y TSS reduce el riesgo de compartir procedencia entre grupos, pero no acredita por sí sola validez clínica ni generalización a cualquier imagen histológica.'),
        html.A('Consultar el estado del arte completo y sus fuentes',href='https://aduartech81.github.io/NuCLS_DeepLearning/03_literatura.html',className='literature-link')
    ]
