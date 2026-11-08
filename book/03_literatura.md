# Estado del arte: clasificación nuclear en histología

La clasificación nuclear requiere distinguir células con apariencia parcialmente semejante y variaciones de tinción, adquisición y contexto tisular. La literatura aborda el problema mediante representaciones locales, información del entorno y relaciones entre células. El interés de una arquitectura depende tanto de esa representación como de la calidad de las etiquetas y del protocolo de evaluación.

El proyecto NuCLS compara tres clasificadores de recortes RGB con contexto: una CNN compacta con BatchNorm, DenseNet121 y ResNet50. La revisión fundamenta esta comparación y examina las condiciones que permiten interpretar sus resultados. La unidad de predicción es el núcleo previamente localizado; los sistemas de segmentación, detección y diagnóstico de láminas se consideran antecedentes relacionados, con objetivos de evaluación diferentes.


## 1. Método de la revisión crítica

| Base | Exportación original | Publicación 2018–2026 |
|---|---:|---:|
| Scopus | 1.097 | 1.057 |
| Web of Science | 328 | 318 |
| IEEE Xplore | 292 | 273 |
| Total | 1.717 | 1.648 |

Se separaron 69 registros por año de publicación fuera de la ventana analítica. La normalización del DOI permitió agrupar 318 registros repetidos y producir 1.330 unidades para cribado: 1.287 con DOI distinto y 43 sin DOI. Siete grupos presentan títulos normalizados coincidentes; no se fusionaron automáticamente porque un título puede corresponder a versiones o documentos distintos. Estas cifras describen identificación y depuración, no inclusión de estudios ni un flujo PRISMA completo.

Se desarrolla una revisión crítica dirigida, apoyada en una búsqueda multibase y en la extracción verificable de estudios pertinentes. La síntesis no constituye una revisión sistemática exhaustiva: sus conclusiones se restringen a las fuentes examinadas. El inventario amplio permite conservar la trazabilidad de la recuperación, mientras que la discusión se organiza alrededor de comparaciones cuya tarea, entrada y métrica pueden identificarse.

La consulta comunicada para la búsqueda fue `(nucle* AND classif*) AND (histolog* OR histopatholog*) AND ("deep learning" OR "convolutional neural network" OR CNN OR transformer*)`, con adaptación por campo en cada plataforma. Las exportaciones permiten verificar registros y fechas de publicación, pero no reconstruyen por sí solas todos los filtros de la interfaz. El historial de consultas constituye una evidencia independiente.

La extracción distingue arquitectura exacta, función del modelo, representación de entrada, conjunto de datos, unidad de partición y métrica. La lectura de títulos y resúmenes identifica candidatos para texto completo; la prioridad automática no determina exclusión ni calidad. La revisión asistida por IA no representa dos revisores independientes.

La revisión se centra en modelos que asignan una categoría celular a un núcleo previamente localizado en una imagen histológica. Este alcance permite identificar referencias comparables con la tarea NuCLS y distinguirlas de sistemas cuyo resultado principal es detectar núcleos, delimitar sus contornos o diagnosticar una imagen completa.

| Criterio | Aplicación en la revisión |
|---|---|
| Pertinencia de la tarea | Priorizar clasificación de tipos nucleares a partir de imágenes histológicas; registrar por separado subclasificación binaria, mitosis e intensidad inmunohistoquímica |
| Función de la arquitectura | Identificar si actúa como clasificador independiente, extractor de características o componente de un sistema híbrido |
| Información de entrada | Documentar tejido, tinción, resolución, contexto, máscaras y otras entradas necesarias |
| Evidencia extraíble | Registrar arquitectura exacta, dataset, partición, métrica y valor; conservar como no reportado aquello que la fuente no permite verificar |
| Periodo de identificación | Aplicar la ventana 2018–2026 a las exportaciones; distinguir los antecedentes fundacionales anteriores utilizados para contextualizar el problema |
| Comparabilidad | Evitar ordenar conjuntamente resultados con distintas clases, métricas, tratamientos o unidades de partición |

Los estudios de tareas adyacentes pueden fundamentar el contexto metodológico, pero no se contabilizan automáticamente como usos de un clasificador nuclear independiente. La selección por pertinencia tampoco equivale a una evaluación de calidad: ambas decisiones se documentan por separado. Estos criterios organizan la lectura dirigida realizada; no se presentan como criterios prerregistrados antes de las búsquedas ni como evidencia de que todos los registros recuperados hayan sido evaluados.

![Flujo documental: identificación, depuración y estado de lectura.](figuras/flujo_literatura.svg)


### Conciliación del flujo y alcance de la lectura

La reconstrucción de las tres exportaciones reprodujo los conteos iniciales y sus hashes SHA256. La ampliación examinó los **1.174 títulos antes pendientes** y resolvió la cola de **364 resúmenes** mediante lectura completa o de fragmentos dirigidos a objetivo, tarea y evaluación, según el nivel registrado individualmente. La ausencia o insuficiencia de resumen derivó a texto, no a exclusión. Los fragmentos no se presentan como lectura íntegra. Los motivos son decisiones asistidas por IA sin segunda revisión independiente.

| Estado actual mutuamente excluyente | Registros |
|---|---:|
| Sin primera decisión | 0 |
| Exclusión explícita por título | 723 |
| Exclusión explícita por resumen | 97 |
| Contexto de tarea distinta | 143 |
| Fuente metodológica | 50 |
| Revisión secundaria | 137 |
| En cola de resumen | 0 |
| Pendiente de recuperación o aclaración en texto completo | 107 |
| Con lectura o extracción de secciones del texto documentada | 73 |
| **Total** | **1.330** |

La contabilidad cumple **1.717 = 69 + 318 + 1.330** y **1.330 = 820 + 330 + 107 + 73**. Los 330 antecedentes no se convierten en exclusiones finales. Los 73 textos documentados tampoco equivalen a estudios incluidos. La primera pasada está resuelta, pero permanecen 107 candidatos de texto y la adjudicación final de elegibilidad. No se estableció el total de informes no recuperados ni de estudios incluidos; se conserva como no determinado, no cero.

El [flujo conciliado](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/flujo_prisma_parcial.json) utiliza las etapas de [PRISMA 2020](https://www.prisma-statement.org/prisma-2020-flow-diagram), sin presentarse como revisión sistemática concluida. Siete grupos de títulos coincidentes siguen sin fusión automática. Un artículo y su preprint cuentan como una publicación; una coincidencia de resultados entre artículos diferentes requiere una auditoría adicional de independencia.

### Trazabilidad de la selección

Las decisiones anteriores se conservan como eventos históricos, aunque una lectura posterior cambie el estado vigente. El consolidado contiene una fila por registro. La ampliación incorpora [1.174 decisiones por título](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/cribado_titulos_ampliado.csv), [364 decisiones de resumen o fragmento](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/cribado_resumenes_ampliado.csv) y [siete nuevas lecturas de textos](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/lecturas_texto_ampliadas.csv). Los resúmenes originales se identifican por hash y no se redistribuyen. Un resumen insuficiente no demuestra fuga de datos ni ausencia de una evaluación pertinente.

## 2. Etiquetas, contexto y definición del problema

Amgad et al. (2022) sitúan la generación de etiquetas en el centro del problema: NuCLS reúne anotaciones de estudiantes y patólogos sobre histología mamaria H&E de TCGA. El trabajo distingue anotaciones individuales y múltiples, e incorpora inferencia de etiquetas y evaluación de concordancia. Por tanto, una etiqueta disponible no equivale a una observación exenta de incertidumbre.

Para este proyecto, la consecuencia es metodológica: verificar archivos, dimensiones y valores faltantes acredita integridad técnica, pero no mide concordancia diagnóstica. La selección de tres categorías y de recortes interiores también delimita la población evaluada. Las métricas obtenidas deben interpretarse respecto a esas etiquetas y reglas de selección, sin extenderlas a todas las células presentes en una lámina.

Fuente: [Amgad et al., descripción de datos, concordancia y limitaciones](https://pmc.ncbi.nlm.nih.gov/articles/PMC9112766/).

La independencia de los recortes constituye otra condición central: muchos núcleos pueden proceder de un mismo paciente o campo histológico. Por ello, el número de imágenes no equivale al número de observaciones biológicas independientes. La comparación experimental utiliza agrupación por paciente y procedencia, y distingue variabilidad entre inicializaciones de variabilidad entre pacientes. Esta decisión responde al diseño de la evaluación; no elimina por sí sola los efectos de selección del conjunto de datos.

## 3. Evidencia cuantitativa de los modelos de referencia

El texto de autor de OLConvNet permite separar dos resultados: CNN con salida softmax y fusión de características profundas con descriptores manuales. La tabla 1 corresponde al primer caso.

| Referencia | Problema | Datos | Modelo básico | Métricas | Valores publicados |
|---|---|---|---|---|---|
| OLConvNet, tabla 1 | Clasificación nuclear, cuatro clases | Colon; recortes 27×27 | CNN3L | F1 / AUC multiclase | 0,8040 / 0,9441 |
| OLConvNet, tabla 1 | Igual | Igual | AlexNet | F1 / AUC multiclase | 0,8216 / 0,9386 |
| OLConvNet, tabla 1 | Igual | Igual | VGG16 | F1 / AUC multiclase | 0,8689 / 0,9757 |
| OLConvNet, tabla 1 | Igual | Igual | VGG19 | F1 / AUC multiclase | 0,8578 / 0,9701 |
| OLConvNet, tabla 1 | Igual | Igual | ResNet50 | F1 / AUC multiclase | 0,8892 / 0,9799 |
| OLConvNet, tabla 1 | Igual | Igual | InceptionV3 | F1 / AUC multiclase | 0,8175 / 0,9538 |
| OLConvNet, tabla 1 | Igual | Igual | DenseNet121 | F1 / AUC multiclase | 0,8706 / 0,9756 |

ResNet50 aislada obtiene F1 0,8892; el 0,9677 publicado para su variante híbrida incorpora otra representación y otro clasificador. Atribuir ambos resultados a la misma configuración confundiría el efecto de la arquitectura con el de la fusión.

La sección 4.1 describe generación sintética antes de una división 70/15/15. Ese orden introduce riesgo de dependencia entre subconjuntos; la descripción tampoco establece agrupación por paciente. No se traslada este procedimiento al experimento NuCLS. El artículo y su preprint se consideran una sola unidad bibliográfica.

Fuente: [texto de autor, sección 4.1 y tablas 1–4](https://arxiv.org/pdf/2202.10177); [DOI 10.1145/3345318](https://doi.org/10.1145/3345318).

### Capacidad y referencias compactas

Basha et al. compararon RCCNet con softmaxCNN_IN27, una variante softmaxCNN, AlexNet adaptada, CIFAR-VGG, GoogLeNet adaptada y WRN. RCCNet utiliza entradas RGB de 32×32, cuatro convoluciones de 32, 32, 64 y 64 filtros, dos reducciones espaciales y capas densas de 512, 512 y cuatro salidas. El entrenamiento incorpora BatchNorm y dropout.

En CRCHistoPhenotypes se informa una partición 80/20 de 22.444 recortes y un F1 ponderado de 0,7887. El texto no establece en esa descripción separación por paciente; tampoco presenta dispersión entre semillas en la tabla comparativa. Además, muestra curvas de exactitud de prueba durante el entrenamiento. Estos aspectos limitan la interpretación de generalización y requieren distinguir seguimiento de prueba de selección de modelos.

El estudio aporta una arquitectura verificable y comparadores concretos, pero su métrica, resolución, tejido y clases difieren del piloto NuCLS. Su presencia no prueba que RCCNet sea uno de los tres modelos más frecuentes.

Fuente: Basha et al., ICARCV 2018, [texto completo de autor, secciones II–IV](https://arxiv.org/html/1810.02797v3), [DOI](https://doi.org/10.1109/ICARCV.2018.8581147).

### Efecto del contexto

Sánchez-Torres et al. (2026) compararon ResNet50 y ViT en PanNuke con cinco clases. La tabla 6 distingue núcleos con contexto y núcleos aislados:

| Modelo y entrada | F1 neoplásico (%) | F1 conectivo (%) | F1 inflamatorio (%) | F1 epitelial (%) | F1 muerto (%) |
|---|---:|---:|---:|---:|---:|
| ResNet50 con contexto | 82,90 | 71,49 | 71,98 | 71,49 | 49,39 |
| ResNet50 sin contexto | 78,71 | 63,21 | 68,99 | 64,39 | 41,13 |
| ViT con contexto | 82,19 | 69,01 | 70,19 | 71,59 | 47,93 |

La tabla no presenta dispersión. La mejora conectiva de ResNet50 al conservar contexto es de 8,28 puntos; su extrapolación a NuCLS requiere cautela. Las clases, particiones y redes difieren. Además, la tabla 14 combina valores de distintos tratamientos: para núcleos muertos muestra 51,66%, asociado al sobremuestreo en la tabla 11, frente a 49,39% en la tabla 6. Se conserva una única configuración para esta extracción.

Fuente: [Sánchez-Torres et al., tablas 6, 11 y 14](https://doi.org/10.1155/acis/4540418).



### Supervisión y conectividad

#### Supervisión limitada y transferencia entre tejidos

Jacobs, Brostow, Freeman, Alexander y Panagiotaki (2017), en *Detecting and Classifying Nuclei on a Budget*, compararon una CNN supervisada, su ajuste por transferencia y una CNN Γ-ladder semisupervisada. La clasificación utiliza ventanas de 27×27 píxeles y tres categorías prostáticas. Se incluye como antecedente metodológico anterior al intervalo reciente de búsqueda.

| Proporción etiquetada | Macro-F1 CNN supervisada | Macro-F1 CNN ajustada | Macro-F1 Γ-ladder |
|---|---:|---:|---:|
| 1% | 0,639 ± 0,021 | 0,695 ± 0,061 | 0,738 ± 0,019 |
| 3% | 0,725 ± 0,012 | 0,752 ± 0,008 | 0,762 ± 0,010 |
| 5% | 0,761 ± 0,003 | 0,769 ± 0,007 | 0,765 ± 0,008 |
| 100% | 0,820 ± 0,005 | 0,819 ± 0,002 | 0,825 ± 0,004 |

La ventaja Γ-ladder frente a la CNN supervisada, con la misma proporción etiquetada, pasa de 9,9 puntos con 1% etiquetado a 0,5 puntos con todos los datos. La ventaja arquitectónica depende, por tanto, del régimen de supervisión. La dispersión publicada no debe confundirse con un intervalo de confianza. La CNN de este estudio no es idéntica a la CNN local implementada en NuCLS.

Fuente: [texto completo institucional, tabla 3](https://discovery.ucl.ac.uk/id/eprint/1573202/1/LABELS2017_7.pdf).

#### Conexiones densas y recurrencia convolucional

Alom, Asari, Parwani y Taha (2022) evaluaron clasificación, segmentación y detección en experimentos separados. Para clasificación de núcleos de colon compararon DenseNet y DCRN, con resultados F1 de **0,7941** y **0,8111**, respectivamente, en el apartado de análisis. La diferencia es de 1,70 puntos. El trabajo describe validación cruzada de cinco particiones.

Su comparación incluye la referencia softmax CNN con predictor de vecindad; no corresponde a una evaluación de MobileNetV2 como clasificador aislado. Los resultados de Dice de R2U-Net y F1 de detección de UD-Net pertenecen a otras tareas y se excluyen de la comparación de clasificación. Las cinco particiones no equivalen a cinco semillas y, sin equiparar agrupación y protocolo, la diferencia publicada no es directamente comparable con el piloto NuCLS.

Referencia: Alom, Z., Asari, V. K., Parwani, A. y Taha, T. M. (2022). *Microscopic nuclei classification, segmentation, and detection with improved deep convolutional neural networks (DCNN).* Diagnostic Pathology, 17, 38. [doi:10.1186/s13000-022-01189-5](https://doi.org/10.1186/s13000-022-01189-5).

### Referencias residuales y refinamiento espacial

Frei et al. (2026) evaluaron ResNet18 aislada en la ablación de GrEp, una propuesta de refinamiento mediante grafos. La comparación corresponde a células epiteliales normales y malignas.

| Referencia | Problema | Dataset de evaluación | Modelo de referencia | Métricas | Valores (%) |
|---|---|---|---|---|---|
| Frei et al., tabla 4 | Subclasificación epitelial binaria | TCGA | ResNet18 sin grafo ni filtro mediano | F epitelial / F maligno / F normal | 87,58 ± 0,97 / 90,83 ± 0,84 / 82,01 ± 1,22 |

La implementación parte de ImageNet, incorpora pooling adaptativo y salida binaria, y utiliza AdamW con tasa 10⁻⁶ durante 150 épocas. Este antecedente acredita el uso de ResNet18 como referencia de clasificación nuclear, además de su papel como extractor. Sin embargo, no reproduce el entrenamiento desde cero ni las tres categorías del piloto NuCLS. El valor del sistema completo con grafos no se atribuye a ResNet18 aislada.

Fuente: [Frei et al., texto completo de autor, sección 3.3 y tabla 4](https://aibex.ch/research/papers/Frei2025.pdf); [DOI](https://doi.org/10.1016/j.patcog.2025.112197).

## 4. Magnitud de las diferencias y calidad metodológica

Las diferencias siguientes se calculan dentro de una misma publicación y conservan su configuración de referencia. Se expresan en puntos porcentuales: para métricas en escala 0–1, Δ = 100 × (resultado del método − resultado del comparador). Describen diferencias observadas; no constituyen pruebas de significación ni estimaciones del efecto esperado en NuCLS.

| Comparación interna | Métrica y condición | Referencia | Alternativa | Δ (puntos) | Interpretación |
|---|---|---:|---:|---:|---|
| OLConvNet: ResNet50 aislada frente a su sistema híbrido | F1, cuatro clases | 0,8892 | 0,9677 | +7,85 | Cambian representación y clasificador; la diferencia no se atribuye solo a ResNet50 |
| PanNuke: ResNet50 sin y con contexto | F1 conectivo | 63,21% | 71,49% | +8,28 | El contexto modifica el desempeño de esta categoría bajo el protocolo publicado |
| Jacobs: CNN supervisada frente a Γ-ladder | Macro-F1, 1% etiquetado | 0,639 | 0,738 | +9,90 | Ventaja observada en un régimen de supervisión escasa |
| Jacobs: CNN supervisada frente a Γ-ladder | Macro-F1, 100% etiquetado | 0,820 | 0,825 | +0,50 | La ventaja se reduce al aumentar la supervisión |
| Alom: DenseNet frente a DCRN | F1 de clasificación | 0,7941 | 0,8111 | +1,70 | Diferencia bajo validación cruzada; no equivale a una comparación local por semillas |

La disminución de la diferencia en Jacobs muestra que una ventaja arquitectónica depende del régimen de datos. En OLConvNet, la mejora corresponde a un sistema híbrido completo. En PanNuke, la modificación de la entrada produce cambios por categoría. En conjunto, estos hallazgos justifican mantener constantes entrada, etiquetas y presupuesto de ajuste al comparar las redes del proyecto.

La evaluación se organiza por aspectos que afectan la comparabilidad; no se asigna una puntuación agregada que convierta información no reportada en un defecto demostrado.

| Estudio | Aporte verificable | Aspecto que limita la comparación | Consecuencia para NuCLS |
|---|---|---|---|
| Basha et al., RCCNet (2018) | CNN compacta y comparadores adaptados; arquitectura y conteo de parámetros descritos | F1 ponderado, cuatro clases y resolución distinta; agrupación por paciente no establecida en la descripción revisada | Declarar la adaptación a 128×128 y mantener separación por paciente; no comparar directamente el F1 publicado con macro-F1 |
| OLConvNet, DOI 10.1145/3345318 | Separa clasificadores CNN de sistemas híbridos con características manuales | Generación sintética descrita antes de la división; riesgo de dependencia entre particiones; agrupación por paciente no establecida | Evitar generación previa a la partición y atribuir a ResNet50 aislada únicamente su resultado de la tabla correspondiente |
| Sánchez-Torres et al. (2026) | Comparación de contexto frente a núcleo aislado con cinco categorías PanNuke | La tabla comparativa no informa dispersión; distintas tablas combinan tratamientos diferentes | Conservar una configuración por comparación y estudiar los recortes con contexto como una entrada definida, sin mezclar resultados |
| Frei et al., GrEp (2026) | Ablación que identifica ResNet18 sin refinamiento por grafo | Subclasificación epitelial binaria y transferencia desde ImageNet; tarea distinta de las tres categorías de NuCLS | Utilizarlo como evidencia de una referencia residual, sin trasladar su puntuación a clasificación multiclase desde cero |

Las referencias y las tablas de origen se identifican en las secciones anteriores. La incertidumbre por semillas, la separación por paciente y la unidad de cálculo del F1 no se consideran intercambiables entre publicaciones.

### Incertidumbre, reproducibilidad y costo

Jacobs presenta dispersión para sus condiciones de supervisión y GrEp la informa en la ablación residual. La tabla de contexto de PanNuke y la comparación extraída de RCCNet no ofrecen una dispersión equivalente. La ausencia de esa información en una tabla no demuestra que el artículo carezca de todo análisis de variabilidad. Tampoco permite reconstruir intervalos de confianza o pruebas pareadas a partir de medias aisladas.

Los tiempos publicados no se ordenan como si procedieran de un mismo equipo: dependen de hardware, resolución, lote, épocas e implementación. El número de parámetros describe almacenamiento y capacidad, pero no determina por sí solo latencia o memoria de activaciones. En el experimento NuCLS, costo y rendimiento deben medirse bajo condiciones comunes y atribuirse a la implementación exacta.

## 5. Desarrollo reciente del campo

La lectura adicional de resúmenes identifica una transición desde clasificadores de ventanas hacia sistemas que resuelven conjuntamente localización, segmentación y tipo nuclear. Esa evolución amplía las capacidades del sistema, pero también cambia el significado de sus métricas. Los siguientes registros se utilizan para orientar la recuperación de textos completos; sus cifras no se incorporan al ranking de clasificadores ni al conteo de arquitecturas verificadas.

| Línea | Estudios identificados en los resúmenes exportados | Implicación para el experimento |
|---|---|---|
| Textura y atención | TexSegNet, DOI 10.1109/EMBC58623.2025.11253497 | Distinguir desempeño conjunto de detección/clasificación del desempeño condicionado a conocer la ubicación del núcleo |
| Contexto, escala y orientación | MOSAIC, DOI 10.1016/j.cmpb.2026.109334; BDCNet, DOI 10.1016/j.eswa.2026.132123 | Las relaciones espaciales y la fusión multiescala requieren entradas y módulos diferentes de los tres clasificadores V2 |
| Generalización y categorías diversas | KongNet, DOI 10.1016/j.media.2026.104233 | La evaluación externa y la cobertura de clases deben documentarse; no se infieren a partir de un F1 elevado |
| Balance y aprendizaje multitarea | AFINITI, DOI 10.1007/s00521-024-10114-4; aumento copy-paste, DOI 10.1007/s10278-024-01018-9 | La mejora de clases minoritarias depende del objetivo y del procedimiento; no justifica trasladar automáticamente una técnica al conjunto NuCLS |
| Clasificación con contexto y representación de láminas | HistoMSC, DOI 10.1016/j.compbiomed.2025.109991 | Separar la red de localización de los clasificadores de recortes antes de atribuir resultados a una arquitectura |

La evidencia de resumen permite reconocer líneas de investigación, pero no comprobar particiones, ablaciones ni todas las arquitecturas de comparación. La extracción de F1 por clase, Dice, AP o calidad panóptica exige conservar su definición: responden a objetivos distintos y no pueden ordenarse en una única escala de rendimiento.

Lou et al. (2024), en *Structure Embedded Nucleus Classification for Histopathology Images*, incorporan contornos y relaciones entre núcleos. Sus comparadores incluyen HoVer-Net y Mask2former. El artículo distingue evaluación con instancias predichas y con máscaras de referencia; por ello, su F-score no se equipara automáticamente al macro-F1 de recortes. Esta lectura confirma que la información de entrada debe formar parte de toda comparación de arquitecturas. [Texto de autor, secciones IV–V](https://guanbinli.com/papers/Structure_Embedded_Nucleus_Classification_for_Histopathology_Images.pdf), [DOI](https://doi.org/10.1109/TMI.2024.3388328).

Estas líneas amplían la representación disponible, pero no invalidan las referencias convolucionales. Un modelo que recibe máscaras, relaciones celulares o información multiescala responde a una pregunta distinta de un clasificador alimentado únicamente con un recorte RGB. Su comparación requiere una ablación que separe la contribución de la entrada, la arquitectura y el entrenamiento. Por ello, la complejidad de un sistema reciente no se interpreta como evidencia suficiente de superioridad para el problema delimitado.

### Sistema conjunto frente a clasificador aislado: HistoNeXt

HistoNeXt utiliza ConvNeXt como codificador preentrenado y decodificadores para segmentación y predicción del tipo nuclear. La descripción de referencia emplea ConvNeXt-Base, entradas de 270×270 y salidas espaciales de 80×80. Las ecuaciones 20–21 distinguen F1 de detección y F1 por tipo, incorporando en este último errores de detección. Por ello, sus puntuaciones no son equivalentes al macro-F1 de recortes previamente localizados de V2. Las conexiones densas del decodificador tampoco constituyen evidencia de uso de DenseNet121. Se registra como sistema conjunto, fuera de la frecuencia de clasificadores aislados. Fuente: [Chen et al., diseño, entrenamiento y métricas](https://link.springer.com/article/10.1186/s12880-025-01550-2).

### Sistemas conjuntos, contexto y modalidades adicionales

HoVer-Net usa un codificador ResNet50 preactivado y modificado, inicializado con ImageNet, con ramas de segmentación, distancias y tipo nuclear. Su PQ de 0,516 en CoNSeP evalúa segmentación de instancias; no equivale al macro-F1 condicionado a recortes localizados. Contar ese codificador como ResNet50 aislada confundiría funciones. [Texto de autor, arquitectura, entrenamiento y tabla V](https://arxiv.org/pdf/1812.06499).

CellViT combina codificadores Transformer con decodificadores nucleares. CellViT-256 utiliza ViT-S preentrenada mediante HIPT; CellViT-SAM-H utiliza el codificador SAM. En PanNuke, la PQ neoplásica es 0,567 y 0,581, respectivamente. Es una comparación dentro del sistema y protocolo publicados, no evidencia de superioridad frente a V2. La versión consultada es el preprint v2 de 2023. [Métodos y tablas 1–2](https://arxiv.org/html/2306.15350v2).

Pérez-Cano et al. refinan HoVer-Net con grafos. En nueve pacientes y 85 imágenes, el macro-F1 que incluye núcleos perdidos pasa de 66,06% a 72,54% con GCN. Se separan pacientes, pero la selección de prueba sin etiquetas inciertas restringe su representatividad. El efecto corresponde a un refinamiento contextual del sistema. [Métodos y tabla 2](https://imatge.upc.edu/web/sites/default/files/pub/aPerez-Cano24.pdf).

Immunocto vincula etiquetas inmunofluorescentes con H&E. Su clasificador adapta ResNet50 con una entrada adicional de máscara: no es el clasificador RGB estándar. El preprint describe 40 pacientes divididos en 35/4/1; la prueba de un paciente limita la cobertura poblacional. La concordancia de expertos pertenece a ese estudio y no valida las etiquetas locales de NuCLS. Se consultó el preprint v2 de febrero de 2025, sin confirmar identidad completa con la versión editorial final. [Métodos III–IV](https://arxiv.org/html/2406.02618v2).

ConvPath clasifica recortes RGB de 80×80 en células tumorales, estromales y linfocitos con una CNN propia. Informa exactitud externa global de 90,1% en SPORE. Es un antecedente cercano por taxonomía y validación externa; no identifica por sí mismo una de las tres arquitecturas V2 ni ofrece una comparación directa de macro-F1. [Métodos y validación externa](https://pmc.ncbi.nlm.nih.gov/articles/PMC6921240/).

Zormpas-Petridis et al. incorporan contexto SLIC a rasgos morfológicos con SVM, no CNN. En melanoma, la exactitud aumenta de 86,4% a 91,6% al añadir contexto y a 92,8% con votación. La comparación muestra que el contexto también modifica métodos clásicos; su taxonomía de cuatro clases y su exactitud no son intercambiables con macro-F1 de NuCLS. [Métodos 2.1–2.4 y tabla 3](https://arxiv.org/pdf/1808.02355).

### Comparadores reutilizados y evidencia independiente

Ensembling evalúa AlexNet, VGG16, VGG19, InceptionV3, ResNet50 y DenseNet121 con transferencia de ImageNet, división aleatoria 70/15/15 y balance mediante ADASYN. La tabla 5 separa CNN aisladas de la combinación de características con MLP de la tabla 6. ResNet50 obtiene F1 0,8892 y DenseNet121 0,8706. Varios pares F1/AUC coinciden exactamente con OLConvNet; se registra posible solapamiento y se presenta sensibilidad por grupos. No se afirma independencia por paciente ni que sean réplicas independientes. [Secciones 3–4 y tablas 5–6, preprint del artículo de 2020](https://arxiv.org/pdf/2202.10694).

### Ampliación de textos del 8 de noviembre

Se añadieron 16 evaluaciones dirigidas de secciones de texto completo. El registro individual conserva fuente, secciones examinadas, decisión y limitaciones; cuando la consulta fue mediante texto indexado de la fuente primaria, se identifica expresamente. Cuatro trabajos se descartan como comparadores de tipificación nuclear por abordar otra unidad o tarea; uno es revisión secundaria. Los demás aportan antecedentes pertinentes, con distintos grados de comparabilidad. Esta clasificación preliminar no cierra la inclusión del corpus ni acredita lectura integral de suplementos.

| Antecedente | Aporte a la comparación | Límite y consecuencia |
|---|---|---|
| [SuperCRF](https://doi.org/10.3389/fonc.2019.01045) | CNN con refinamiento espacial; exactitud 84,63% frente a 96,48% en el experimento celular | Cuatro tipos de melanoma; exactitud no equivale a macro-F1. La ganancia corresponde al contexto añadido |
| [Cell Graph Transformer](https://doi.org/10.1609/aaai.v38i4.28179) | En NuCLS, Favg de HoVer-Net 0,337 y CGT+HoVer-Net 0,377 | Cuatro superclases y dependencia de detecciones; no comparar directamente con los tres tipos V2 |
| [Lizard](https://doi.org/10.1109/ICCVW54120.2021.00082) | Evaluación nuclear con separación por paciente y prueba externa TCGA | Aporta diseño de validación; multi-PQ combina identificación y segmentación |
| [AER-Net](https://doi.org/10.3390/s24227208) | ResNet50 modificado con atención, ramas y refinamiento | Su codificador no se contabiliza como ResNet50 aislada |
| [SBC-UNet3+](https://doi.org/10.5220/0013232900003912) | Combina contornos, segmentación y clasificación | Inconsistencias entre texto y tabla en métricas de segmentación; evitar ranking cuantitativo |
| [Bai et al.](https://doi.org/10.1093/bioinformatics/btac167) | Combina varios campos de visión con contexto | Separar resultados H&E de Ki67; suplemento H&E no extraído |
| [Abel et al.](https://doi.org/10.1038/s41698-024-00623-9) | Segmentación seguida de clasificación PathExplore | ResNet50 pertenece al segmentador; no prueba un clasificador RGB independiente |
| [HistoPLUS](https://doi.org/10.1016/j.jpi.2026.100696) | CellViT con codificador H0-mini y validación externa de 13 tipos | Tres folds con semilla fija no son tres inicializaciones; taxonomía y entrada difieren de V2 |
| [Altini et al.](https://doi.org/10.3390/bioengineering10040396) | NuCLS: Mask-RCNN conjunto frente a detector y SVM/ANN de características | Fusiona categorías en tumor/no tumor; AP y evaluación binaria no equivalen al macro-F1 V2 |
| [Verdicchio et al.](https://doi.org/10.1016/j.heliyon.2023.e14371) | Clasifica TIL/no-TIL con características manuales y modelos clásicos | Referencia de contexto; no candidato CNN. Agrupación por paciente no acreditada en la descripción revisada |

Estos trabajos permiten precisar la brecha del proyecto: comparar tres clasificadores de recortes RGB manteniendo constantes taxonomía, contexto, partición y ajuste. Las ganancias de sistemas con máscaras o grafos no permiten atribuir una mejora únicamente a su codificador. La validación externa y la separación por paciente son dimensiones adicionales al cambio de arquitectura.

#### Alerta editorial y límites de inclusión

El artículo sobre segmentación y clasificación federada, [DOI 10.1371/journal.pone.0322749](https://doi.org/10.1371/journal.pone.0322749), incluye comparadores nucleares, pero tiene una [expresión de preocupación de PLOS del 30 de octubre de 2026](https://doi.org/10.1371/journal.pone.0361682). El aviso se refiere a datos de figuras no aportados y a la indisponibilidad del código original, con código recreado posterior. Se conserva la trazabilidad de la fuente y se mantiene fuera de la tabla principal de frecuencias sin alerta; no se utiliza para reforzar artificialmente la selección.

Se excluyen como comparadores nucleares LIT-0016 (parches mamarios benignos/malignos), LIT-0076 (diagnóstico de imagen gástrica), LIT-0610 (segmentación por píxel) y LIT-0684 (mitosis y primitivas histológicas). LIT-1105 se deriva a revisión secundaria. Estas cinco disposiciones están contenidas en el total de textos leídos: no se suman nuevamente a las exclusiones de título/resumen. La cola de registros pendientes incluye textos todavía no buscados, no recuperados y no aclarados; no se denomina «informes inaccesibles».

El [registro de esta ampliación](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/evaluaciones_texto_20261108.csv) permite comprobar cada decisión. El diagrama continúa siendo parcial: cerrar el estado del arte como narrativa no sustituye el cierre de elegibilidad solicitado en la guía.

<!-- AMPLIACION_CIERRE_INICIO -->
### Evidencia adicional y relación con los resultados V2

La nueva ampliación contiene 44 lecturas dirigidas, con fuente y secciones identificadas en `evaluaciones_texto_cierre_20261108.csv`. Se distinguen sistemas conjuntos, clasificadores modificados, tareas IHC y fuentes secundarias. Las frecuencias conservadoras anteriores se mantienen restringidas a su conjunto de comparadores verificados; no se presentan como un censo de todas las arquitecturas mencionadas.

| Fuente | Problema y datos | Modelos o representación | Métrica extraída y valor | Consecuencia para NuCLS |
|---|---|---|---|---|
| [Task-Ready PanNuke/NuCLS](https://doi.org/10.1109/ACCESS.2025.3589477) | Tipificación binaria PanNuke; preparación NuCLS | DenseNet121, ResNet18, EfficientNetB0 | DenseNet121 epitelial 64: exactitud 0,9513; AUC 0,9727 | No equivale a macro-F1 triclase. Inconsistencia sobre ResNet50 entre método y resultados; no usarla para aumentar su frecuencia |
| [Remedios et al.](https://doi.org/10.1117/1.JMI.11.6.067501) | Catorce subtipos en H&E virtual y evaluación real | ResNet18 con InstanceNorm y etiquetas MxIF | PPV/NPV y cotas externas; sin macro-F1 comparable extraído | Veinte pacientes, partición 12/4/4 por fold; muestra límites del cambio de dominio y de taxonomía |
| [PointNu-Net](https://doi.org/10.1109/TETCI.2023.3281864) | Segmentación y tipificación CoNSeP/PanNuke | Puntos clave, fusión piramidal, máscaras dinámicas | CoNSeP mPQ 0,536 frente HoVer-Net 0,516 | Ganancia de sistema conjunto, no de clasificador de recortes aislado |
| [TSHVNet](https://doi.org/10.1155/2022/7921922) | Segmentación y clasificación conjunta | HoVer-Net con Transformer y SimAM | CoNSeP F1 epitelial 0,669; inflamatorio 0,621 | Atención y preentrenamiento modifican protocolo; separar Fd del macro-F1 V2 |
| [CoNIC](https://doi.org/10.1016/j.media.2023.103047) | Seis tipos nucleares, prueba oculta | Sistemas participantes y HoVer-Net | Mejores tres mPQ+: 0,501; 0,476; 0,463 | Distinguir modelos individuales de ensembles y métricas de segmentación de clasificación |
| [Zhang et al.](https://doi.org/10.1016/j.csbj.2024.10.046) | Lizard, PanNuke, MoNuSAC | Ensemble SEResNeXt50/101 y HoVer | Lizard mPQ+ 0,5599±0,0086 | Comparte resultados de desafío con CoNIC; no es una replicación independiente de ese experimento |
| [HoVer-NeXt](https://proceedings.mlr.press/v250/baumann24a.html) | Lizard-mitosis y PanNuke | ConvNeXt-v2 y doble decodificador | PanNuke Tiny TTA16 mPQ_tiss 0,477 | Sus tiempos miden pipeline WSI, no latencia del clasificador NuCLS |
| [KongNet](https://doi.org/10.1016/j.media.2026.104233) | Detección y tipo nuclear en MONKEY, PUMA y PanNuke | EfficientNetV2-L y decodificadores por tipo | PanNuke F1 medio por tipo 0,674 | Sistemas preentrenados; rendimiento incluye localización, no sólo clasificación |
| [MSA-Net](https://doi.org/10.1186/s12859-025-06066-8) | Quinientos parches TCGA, tres tipos celulares | ViT, CLIP y grafo | Fc promedio 0,858 | Partición aleatoria de parches; independencia por paciente no demostrada |
| [AC-Former](https://doi.org/10.1109/ICCV51070.2023.01955) | CoNSeP, BRCA-M2C y Lizard | ConvNeXt-B, Transformer y consistencia afín | CoNSeP Fc medio 0,613 | Anotación por centroides y pérdida conjunta; no equivalente a V2 |
| [PUMA](https://doi.org/10.1093/gigascience/giaf011) | Melanoma, prueba oculta de 94 ROI | HoVer-Net y HoVer-NeXt | HoVer-NeXt entrenado PUMA: F1 medio triclase 0,70 | Reagrupación tumor/linfocito/otro; documenta acuerdo de observadores y clases raras |
| [TSFD-Net](https://doi.org/10.1016/j.neunet.2022.02.020) | PanNuke, partición 80/20 | Destilación específica de tejido y BiFPN | mPQ 0,504; bPQ 0,6377 | Tiempos de competidores provienen de otro dataset; no usar para ranking de latencia |
| [Cerberus](https://doi.org/10.1016/j.media.2022.102685) | Recortes nucleares y tareas relacionadas de colon | ResNet34/18 congelados y cabeza entrenable | ResNet34 MTL: mF1 externo 0,506±0,010 | Transferencia y contexto importan; no equivale a entrenar ResNet50 desde cero |
| [Ruido de anotación](https://doi.org/10.1016/j.compbiomed.2024.108586) | MoNuSAC/PanNuke con corrupción simulada | HoVer-Net y parada temprana | Tabla 8: exactitud balanceada 0,964 con parada frente a 0,839 sin ella, con 30% de ruido | Evidencia metodológica; no demuestra la causa de errores en NuCLS |

Además, [HD-Yolo](https://doi.org/10.1016/j.modpat.2023.100196) evaluó NuCLS multirater después de entrenar en single-rater: F1 de detección y tipo 0,8493, con coincidencia IoU>0,5. Su ensemble de cinco folds no representa cinco semillas ni la tarea de recortes V2. [CAPL-Net](https://arxiv.org/abs/2207.01233) ilustra la adaptación entre dominios con datos objetivo sin etiquetas; utilizar esa estrategia sobre nuestra reserva modificaría el protocolo. Por tanto, estos trabajos orientan mejoras futuras, sin justificar ajustes retrospectivos tras conocer la reserva.

La ampliación también identifica radiomía con selección de aciertos de prueba antes de segmentar (LIT-0549), clasificación clásica basada en rasgos (LIT-0213), citología tiroidea multietiqueta (LIT-0398) y un comentario sobre MRI prostática (LIT-0071). Se documentan como contexto o exclusión preliminar, sin tratarlos como réplicas de la clasificación H&E triclase.

El manuscrito de Yousefi y Nie se deriva a contexto IHC/ISH y agrupamiento, y Alzoubi et al. a revisión secundaria. El editorial de Pinto-Coelho et al. no es evidencia experimental primaria. Los registros permanecen trazables dentro de la etapa de lectura, sin sumarlos nuevamente a las exclusiones de título/resumen.

El cierre experimental V2 seleccionó ResNet50 por validación y obtuvo macro-F1 de reserva 0,6378, frente a 0,6052 de DenseNet121 y 0,4542 de la compacta. Esta comparación local comparte partición, tres clases e inicialización desde cero, pero no reproduce las taxonomías ni todas las condiciones de los artículos. La caída de desempeño y el F1 estromal 0,3022 de ResNet50 refuerzan la necesidad de analizar clases y pacientes, sin probar una explicación causal ni superioridad general de una familia arquitectónica. Los [resultados completos](08_resultados_v2.md) distinguen incertidumbre por semillas y por pacientes.
<!-- AMPLIACION_CIERRE_FIN -->







## 6. Selección de arquitecturas y contribución del proyecto

La extracción cuenta una vez cada DOI por arquitectura exacta y separa las variantes adaptadas. **Siete publicaciones** sustentan la tabla parcial. ResNet50 aparece en tres; DenseNet121, AlexNet, VGG16, VGG19, InceptionV3, ResNet18 y ResNet34, en dos. Las restantes arquitecturas exactas aparecen en una. ViT sin variante identificable y codificadores de sistemas conjuntos no se suman como clasificadores aislados.

Ensembling y OLConvNet comparten autores, dataset y varios valores F1/AUC de comparadores. Esto sugiere posible reutilización, sin demostrar que sean el mismo estudio. Una sensibilidad conservadora agrupa ambos: ResNet50 queda en dos grupos y DenseNet121 en uno. Los siete artículos corresponden a seis grupos bajo esa hipótesis, no a seis estudios definitivamente adjudicados. Véanse la [tabla por publicación](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/frecuencia_comparadores_verificados.csv) y la [sensibilidad por grupos](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/frecuencia_sensibilidad_estudios.csv). El campo histórico `estudios_verificados` de la primera tabla significa DOI/publicaciones, no independencia experimental demostrada.

| Selección V2 | Publicaciones / grupos conservadores | Parámetros, tres clases | Rasgo estructural |
|---|---:|---:|---|
| softmaxCNN con BatchNorm, adaptada | 1 / 1 | 898.687 | Convoluciones secuenciales |
| DenseNet121 | 2 / 1 | 6.956.931 | Conexiones densas |
| ResNet50 | 3 / 2 | 23.514.179 | Conexiones residuales |

La selección responde a tres funciones experimentales complementarias. La CNN compacta establece el desempeño alcanzable con menor capacidad; DenseNet121 permite evaluar reutilización de características mediante concatenaciones; ResNet50 incorpora aprendizaje residual y presenta la mayor recurrencia exacta en el subconjunto comparativo extraído. El objetivo es contrastar estas referencias bajo la misma entrada y partición, no identificar retrospectivamente una arquitectura ganadora a partir de puntuaciones de datasets diferentes.

| Referencia | Fundamento de elección | Pregunta que aporta a la comparación | Límite de la justificación |
|---|---|---|---|
| CNN compacta con BatchNorm | Comparador documentado en RCCNet y menor número de parámetros entre las tres implementaciones | ¿Qué rendimiento se obtiene con una representación convolucional secuencial de capacidad reducida? | La adaptación espacial a 128×128 impide tratarla como reproducción exacta del estudio de origen |
| DenseNet121 | Clasificador aislado cuantificado en OLConvNet; reutilización de características y capacidad intermedia | ¿La conectividad densa mejora el compromiso entre desempeño y número de parámetros? | Menos parámetros que ResNet50 no implica menor latencia ni menor memoria de activaciones |
| ResNet50 | Comparador multiclase identificado en OLConvNet y PanNuke; conexiones residuales | ¿La mayor capacidad residual aporta una ganancia reproducible frente a las otras referencias? | Su recurrencia provisional no demuestra predominio en el corpus completo |

La ampliación añade HistoContours (ResNet34/101 y EfficientNet-B5/B7) y Cerberus (ResNet34/18 como encoders congelados para clasificación por recortes). Se cuenta presencia de arquitectura, no igualdad de entrenamiento ni de información de entrada. HistoContours codifica tejido en un marco de color, al que su GradCAM presta atención; ilustra por qué una explicación visual debe examinar señales de contexto. La selección V2 ya estaba fijada y no se modifica retrospectivamente.

Esta es una selección multicriterio sustentada en evidencia extraída. El criterio de la guía referido a las tres arquitecturas más frecuentes y sencillas no queda demostrado para el corpus completo: la recurrencia disponible se limita a siete publicaciones, con posible solapamiento de comparadores y la sencillez admite indicadores diferentes. Se informa esta restricción para distinguir la pertinencia científica de las referencias del cumplimiento literal de ese criterio. No se modifica la selección a partir de resultados de entrenamiento observados.

La CNN pequeña reproduce el conteo publicado de 899.200 parámetros para cuatro clases y entrada 27×27. Para utilizar las ventanas comunes de 128×128 se reduce el mapa de 30×30 a una cuadrícula de 5×5 mediante promedios en bloques disjuntos de 6×6, equivalentes al pooling adaptativo de esas dimensiones. Se conservan las dimensiones del clasificador sin añadir parámetros. Esa adaptación modifica la agregación espacial y se declara explícitamente; no constituye reproducción exacta del experimento original. La verificación técnica inicial incluyó propagación y gradientes con tensores sintéticos; esa prueba comprueba ejecutabilidad y no estima capacidad predictiva.

El protocolo contempla inicialización desde cero y condiciones comunes, a diferencia de algunos estudios que emplean transferencia. Las redes establecen referencias experimentales con mecanismos de conectividad distintos, sin asumir igualdad de capacidad.

La selección y sus adaptaciones se describen en [el protocolo v2](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/protocolo/seleccion_modelos_v2.md). El [flujo experimental](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/protocolo/ejecucion_integrada_v2.md) separa búsqueda, piloto, planificación de corridas, evaluación final y reserva. Los resultados de CNN local, ResNet18 y MobileNetV2 siguen correspondiendo al piloto anterior.

### Brecha experimental

Los clasificadores convolucionales constituyen referencias pertinentes porque aprenden características locales directamente de los píxeles. Sin embargo, la evidencia revisada no sostiene una arquitectura universalmente superior. Las puntuaciones dependen del tejido, de las categorías, del contexto incluido, del preentrenamiento y de la forma de dividir los datos. El resultado de un sistema híbrido tampoco equivale al de su red extractora utilizada aisladamente.

La comparación de PanNuke muestra que retirar contexto puede disminuir el F1 de determinadas categorías; esto justifica declarar con precisión qué información contiene cada ventana. No permite afirmar que todo contexto sea beneficioso: el fondo y las características de adquisición también pueden introducir señales de procedencia. El diagnóstico de desplazamiento de NuCLS indica que las particiones son parcialmente distinguibles mediante descriptores sencillos, lo que refuerza la necesidad de separación por paciente y TSS y de una interpretación prudente de la generalización.

La brecha que aborda este entregable es una comparación controlada de tres referencias sobre la misma selección de recortes NuCLS, con preprocesamiento ajustado en entrenamiento, esfuerzo de búsqueda común y variabilidad entre ejecuciones. Se trata de una contribución experimental dentro del proyecto académico, no de una afirmación de novedad mundial ni de una arquitectura original. El cierre con once semillas informa esa incertidumbre y explicita el límite de seis pacientes de reserva.

La pregunta resultante es si, bajo una misma partición y tratamiento de imágenes, la conectividad densa o residual ofrece una mejora reproducible frente a una referencia compacta y qué costo implica. La literatura aporta antecedentes para formular la pregunta; la respuesta corresponde al experimento local. No se presupone que la red de mayor tamaño deba ganar.

### Conclusión

La evidencia examinada converge en una condición metodológica: la comparación de clasificadores nucleares exige controlar simultáneamente la representación de entrada, las etiquetas y la partición. Las diferencias observadas dentro de cada publicación muestran que el contexto, el régimen de supervisión y la combinación de descriptores pueden modificar el rendimiento tanto como el cambio de arquitectura. Por ello, los valores publicados sirven para fundamentar decisiones experimentales, no para anticipar el resultado en NuCLS.

El estudio adopta tres referencias verificables de capacidad y conectividad distintas y las compara sobre los mismos recortes. El EDA aporta la caracterización de balance, integridad y heterogeneidad de procedencia necesaria para interpretar esa comparación. La evaluación de once semillas favorece descriptivamente a ResNet50, pero muestra incertidumbre entre pacientes y bajo F1 estromal. La latencia controlada sigue pendiente, por lo que no se establece un ranking de eficiencia.

La revisión crítica queda delimitada a las fuentes y comparaciones documentadas. Su contribución es una síntesis metodológica aplicable al experimento; no acredita exhaustividad bibliográfica ni identifica los tres modelos dominantes de toda la literatura. Esta distinción preserva la trazabilidad entre lo que las fuentes permiten afirmar y lo que el experimento debe responder.

## 7. Fuentes principales y evidencia reproducible

Las referencias se vinculan a su DOI o al texto de autor utilizado. Los antecedentes de 2016 y 2017 se conservan como fundamentos históricos externos a la ventana reciente. El artículo OLConvNet y su preprint constituyen una sola unidad de estudio. No se asignan cuartiles bibliométricos sin verificar la revista, categoría y año correspondientes.

1. Sirinukunwattana et al. (2016). *Locality Sensitive Deep Learning for Detection and Classification of Nuclei in Routine Colon Cancer Histology Images*. [DOI](https://doi.org/10.1109/TMI.2016.2525803). Antecedente de detección y clasificación; consulta de resumen.
2. Jacobs et al. (2017). *Detecting and Classifying Nuclei on a Budget*. [Texto institucional](https://discovery.ucl.ac.uk/id/eprint/1573202/1/LABELS2017_7.pdf). Evidencia de supervisión limitada, tabla 3.
3. Basha et al. (2018). *RCCNet: An Efficient Convolutional Neural Network for Histological Routine Colon Cancer Nuclei Classification*. [DOI](https://doi.org/10.1109/ICARCV.2018.8581147). [Texto de autor](https://arxiv.org/html/1810.02797v3).
4. Tripathi y Singh (2020). *Cell nuclei classification in histopathological images using hybrid OLConvNet*. [DOI](https://doi.org/10.1145/3345318). [Preprint de 2022](https://arxiv.org/abs/2202.10177).
5. Alom et al. (2022). *Microscopic nuclei classification, segmentation, and detection with improved deep convolutional neural networks (DCNN)*. Diagnostic Pathology, 17, 38. [DOI](https://doi.org/10.1186/s13000-022-01189-5).
6. Amgad et al. (2022). *NuCLS: A scalable crowdsourcing approach and dataset for nucleus classification and segmentation in breast cancer*. GigaScience, 11, giac037. [DOI](https://doi.org/10.1093/gigascience/giac037).
7. Sánchez-Torres et al. (2026). Estudio comparativo de clasificación nuclear en PanNuke; tablas 6, 11 y 14. [Identificador del artículo](https://doi.org/10.1155/acis/4540418).
8. Frei et al. (2026). GrEp; Pattern Recognition, 171, 112197; sección 3.3 y tabla 4. [DOI](https://doi.org/10.1016/j.patcog.2025.112197). [Texto de autor](https://aibex.ch/research/papers/Frei2025.pdf).

El [inventario y las extracciones](https://github.com/aduartech81/NuCLS_DeepLearning/tree/main/evidencias/literatura) conservan la procedencia y el nivel de lectura. La [tabla de frecuencia](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/frecuencia_comparadores_verificados.csv) contabiliza publicaciones por arquitectura; la sensibilidad separada explora su posible dependencia. Los registros no evaluados permanecen identificados como tales; no se transforman en exclusiones para cerrar artificialmente el flujo de selección.

