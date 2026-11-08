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
| Informe no recuperado al corte de entrega | 13 |
| Con lectura o extracción de secciones del texto documentada | 166 |
| Duplicado identificado durante recuperación | 1 |
| **Total** | **1.330** |

La contabilidad cumple **1.717 = 69 + 318 + 1.330** y **1.330 = 820 + 330 + 1 + 13 + 166**. De 180 candidatos históricos, uno era duplicado y quedaron 179 informes: 166 con lectura dirigida documentada y 13 no recuperados al corte. Los 330 antecedentes son contexto anterior a la recuperación; no se suman a los 166. El número de estudios independientes no está establecido. La adjudicación por capas se refiere a informes, según el nivel de lectura registrado.

El [flujo conciliado](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/flujo_prisma_parcial.json) utiliza las etapas de [PRISMA 2020](https://www.prisma-statement.org/prisma-2020-flow-diagram), sin presentarse como revisión sistemática concluida. De los siete grupos de títulos coincidentes, se confirmó que LIT-1168 y LIT-0602 son el mismo artículo: autores, revista, año, volumen y páginas coinciden; al registro WoS le faltaba el DOI. Se conserva la fila histórica como duplicado tardío, sin contar una lectura adicional. Las demás coincidencias no se fusionan automáticamente. Un artículo y su preprint cuentan como una publicación; una coincidencia de resultados entre artículos diferentes requiere una auditoría adicional de independencia.

<!-- CAPAS_SINTESIS_INICIO -->
### Asignación a capas de síntesis al corte

La revisión de las decisiones individuales organiza los 166 informes leídos en cinco grupos excluyentes. Esta asignación no altera el nivel de lectura documentado: algunos registros tienen extracción dirigida y no lectura íntegra de apéndices.

| Capa de síntesis | Informes |
|---|---:|
| Clasificación nuclear localizada o ablación separable: síntesis focal | 21 |
| Sistemas conjuntos, contextuales y representaciones relacionadas | 83 |
| Tareas o modalidades adyacentes, fuera de la comparación focal | 49 |
| Revisiones, editoriales y comentarios | 12 |
| Sensibilidad separada por preocupación editorial | 1 |
| **Total con lectura documentada** | **166** |

La matriz `adjudicacion_sintesis_20261108.csv` identifica cada informe, motivo, limitación y fuente. Los 21 informes focales no son 21 experimentos independientes ni 21 usos de cada arquitectura. Incluyen clasificadores modificados, máscaras, ensambles y subclasificación binaria; sus diferencias se conservan. Las frecuencias de arquitecturas siguen restringidas al subconjunto de comparadores exactos verificados. Los sistemas conjuntos fundamentan la discusión del campo, sin mezclar sus PQ, F1 de detección o métricas por píxel con macro-F1 de recortes. La recuperación se cierra para esta entrega con 13 informes no recuperados, individualizados en `informes_no_recuperados_20261108.csv`. No se consideran leídos ni excluidos por pertinencia. Podrán recuperarse en una actualización posterior.
<!-- CAPAS_SINTESIS_FIN -->

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

Se excluyen como comparadores nucleares LIT-0016 (parches mamarios benignos/malignos), LIT-0076 (diagnóstico de imagen gástrica), LIT-0610 (segmentación por píxel) y LIT-0684 (mitosis y primitivas histológicas). LIT-1105 se deriva a revisión secundaria. Estas cinco disposiciones están contenidas en el total de textos leídos: no se suman nuevamente a las exclusiones de título/resumen. Los intentos de recuperación se conservan como historial; el estado vigente de los 13 informes no recuperados se documenta por separado.

El [registro de esta ampliación](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/evaluaciones_texto_20261108.csv) permite comprobar cada decisión. El diagrama presenta el corte de entrega y la adjudicación por capas; la cobertura incompleta y la falta de un segundo revisor impiden presentarlo como revisión sistemática exhaustiva.

<!-- AMPLIACION_CIERRE_INICIO -->
### Evidencia adicional y relación con los resultados V2

La nueva ampliación contiene 137 lecturas dirigidas, con fuente y secciones identificadas en `evaluaciones_texto_cierre_20261108.csv`. Se distinguen sistemas conjuntos, clasificadores modificados, tareas IHC y fuentes secundarias. Las frecuencias conservadoras anteriores se mantienen restringidas a su conjunto de comparadores verificados; no se presentan como un censo de todas las arquitecturas mencionadas.

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


























### Clasificadores de recortes recuperados mediante la biblioteca

La lectura institucional permite precisar tres estrategias complementarias. [DV-CNNs](https://doi.org/10.1007/978-3-030-03335-4_20) combina recortes de 27×27 y 36×36 con BatchNorm y extracción de varias regiones. Su tabla 2 informa F1 promedio 0,843 y AUC multiclase 0,947 en HistoPhenotypes; el experimento de tres clases alcanza exactitud 90,40%. Estas cifras apoyan investigar el contexto, pero no establecen equivalencia con tres clases mamarias ni con una partición por paciente. Los comparadores tomados de Bayramoglu no constituyen nuevas réplicas independientes.

El [ensamble difuso de CNN](https://doi.org/10.1109/ICCCNT56998.2023.10308315) clasifica recortes PanNuke de 64×64 utilizando DenseNet201, IBN-DenseNet201 y MixNet preentrenadas. La tabla de ablación informa F1 0,788 para DenseNet201 y 0,811 para el ensamble; el promediado no queda inequívocamente identificado. DenseNet201 se distingue de DenseNet121 y el resultado del ensamble no se atribuye a un solo modelo. La eliminación de núcleos pequeños o de borde también modifica la población evaluada.

El [sistema FCRN–CNN](https://doi.org/10.1109/AIPR.2018.8707397) añade a RGB un mapa aprendido de localización nuclear. Obtiene F1 ponderado 0,8526 al transferir el detector desde mama hacia clasificación de colon. La clasificación se entrena en colon: este resultado no demuestra validación externa del clasificador. En conjunto, los tres trabajos muestran que tamaño del recorte, información adicional, transferencia y agregación de predicciones deben registrarse antes de comparar cifras.

Los modelos conjuntos [TexSegNet](https://doi.org/10.1109/EMBC58623.2025.11253497), [ANet](https://doi.org/10.1007/s42979-024-02661-3), [AFINITI](https://doi.org/10.1007/s00521-024-10114-4) y [TRG-Dilated HoVer-Net](https://doi.org/10.1007/s00521-023-08394-3) amplían este contexto mediante atención, mapas de forma o información tisular. Sus puntuaciones incluyen localización, segmentación o entradas adicionales; no se mezclan con el macro-F1 de recortes V2. TRG-Dilated HoVer-Net muestra además que una guía tisular errónea puede inducir errores de tipo nuclear, una razón para evaluar señales de contexto y no asumir que toda mejora de capacidad mejora la generalización.












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



### Comparaciones adicionales verificadas en acceso institucional

| Referencia | Problema | Datos | Modelo y función | Métrica | Resultado publicado |
|---|---|---|---|---|---|
| [DV-CNN](https://doi.org/10.1007/978-3-030-03335-4_20) | Cuatro tipos nucleares | CRCHistoPhenotypes; vistas 27 y 36 píxeles | CNN de doble vista, fusión de puntuaciones | F1 medio / AUC, tabla 2 | 0,843 / 0,947 |
| [Ensamble difuso](https://doi.org/10.1109/icccnt56998.2023.10308315) | Cinco tipos nucleares | PanNuke; recortes 64×64 | DenseNet201 / IBN-DenseNet201 / MixNet / ensamble de los tres | F1; promedio no aclarado en esta extracción | 0,788 / 0,789 / 0,781 / 0,811 |
| [FCRN y CNN](https://ieeexplore.ieee.org/document/8707397) | Cuatro tipos celulares | Colon; 22.444 células | CNN de 14 capas, RGB más mapa de distancia | F1 ponderado | 0,8526 con detector aprendido en mama |
| [Comparación de arquitecturas profundas](https://doi.org/10.1007/978-981-13-9184-2_33) | Cuatro tipos nucleares | Colon; 22.444 recortes ampliados de 27 a 224 píxeles | AlexNet / VGG16 / VGG19 con ImageNet | F1; promedio no aclarado | 63,52% / 65,41% / 64,39% |
| [Células inflamatorias](https://doi.org/10.1007/978-981-13-9190-3_73) | Núcleo, linfocito, neutrófilo e impureza | Hígado H&E institucional; 4.522/518 recortes de entrenamiento/prueba | CNN de cuatro convoluciones y salida softmax | Exactitud global | 88,61% |
| [Forma nuclear mediante esqueletos](https://doi.org/10.1007/978-3-030-66415-2_20) | Tumor/no tumor | BreCaHAD; muestra balanceada | AlexNet ImageNet como extractor y SVM / rasgos MAT y SVM | Exactitud | 0,632 ± 0,001 / 0,850 ± 0,004 |

Estas comparaciones amplían la evidencia de clasificadores de recortes, pero sus valores no forman una clasificación conjunta de eficacia. DV-CNN evalúa contexto a dos escalas; el ensamble difuso combina modelos preentrenados; FCRN añade información de localización; la CNN hepática utiliza una taxonomía distinta. En el estudio de esqueletos se evalúan únicamente los núcleos recuperados por una segmentación previa y se balancea la muestra mediante muestreo con reemplazo. La independencia por paciente no queda acreditada en las secciones consultadas de estos estudios.

La CNN hepática constituye un antecedente adicional de una arquitectura compacta con cuatro convoluciones y softmax. El artículo describe ventanas de 80×80, pero enumera una entrada de 32×32 en su configuración; esa ambigüedad impide presentarlo como una reproducción exacta de nuestra red. Del mismo modo, DenseNet201 no se contabiliza como DenseNet121, y AlexNet utilizada para extraer rasgos no se describe como una red ajustada de extremo a extremo. Las frecuencias de la sección anterior conservan su subconjunto expresamente documentado.


### Qué cambia al evaluar pacientes nuevos

El trabajo de [Qu et al.](https://doi.org/10.1109/ISBI.2019.8759457) es particularmente ilustrativo: utiliza 40 imágenes de ocho casos pulmonares y declara que cada partición contiene imágenes de todos los casos. Su exactitud de clasificación se calcula únicamente sobre los núcleos detectados correctamente. Aun cuando las clases tumor, linfocito y estroma parecen cercanas a las de NuCLS, el protocolo mide una condición distinta de la generalización a pacientes nuevos y omite del denominador de clasificación los núcleos no detectados.

[StarDist multiclase](https://ieeexplore.ieee.org/document/9854534) aporta una observación complementaria: el aumento de tinción no parecía tan favorable en la validación interna como en la prueba preliminar del desafío CoNIC. Los autores relacionan esa diferencia con un posible cambio de dominio. Su resultado final combina cuatro modelos, aumentos en inferencia y refinamiento de contornos; se vincula con el informe CoNIC y no se cuenta como una réplica independiente de ese mismo resultado.

Estos antecedentes respaldan dos decisiones del experimento local: separar pacientes y mantener una reserva sin ajustes posteriores. La caída entre validación y reserva observada en los tres modelos debe informarse completa. La literatura ofrece hipótesis sobre contexto, tinción, etiquetas y composición celular; identificar cuál explica nuestros errores requiere análisis específicos y no puede resolverse por semejanza con un artículo.

### Contexto tisular y alcance de la comparación

[HistoMSC (Ahmad et al., 2025)](https://doi.org/10.1016/j.compbiomed.2025.109991) separa localización de clasificación y compara recortes PanNuke con ResNet34, SqueezeNet, ResNet101 y EfficientNet-B5/B7. La tabla 1 informa *weighted accuracy* de 0.83486, 0.83251, 0.84532, 0.84627 y 0.85422, respectivamente. Además de la imagen, el marco coloreado de cada recorte codifica el tipo de tejido. Por ello, estas cifras no constituyen una comparación equivalente con nuestro macro-F1 de tres clases y entrada RGB. En ese trabajo, ResNet50 aparece como parte del detector U-Net; no debe contarse como clasificador evaluado en la tabla. El estudio también encuentra discrepancias al aplicar el sistema a 73 láminas TCGA, reforzando la necesidad de distinguir resultados internos de generalización a nuevas muestras.


### Comparación de encoders y adaptación entre tinciones

[SPNet](https://doi.org/10.1016/j.compmedimag.2023.102296) compara encoders dentro de un sistema conjunto basado en HoVer-Net. En CoNSeP, ResNet50 obtiene PQ de 0,516 y ResNet50-SE, 0,526; los cuatro F1 por tipo del segundo son 0,540, 0,669, 0,644 y 0,579. La variante DenseNet169 sólo utiliza preentrenamiento en la primera capa, por lo que su resultado inferior no demuestra inferioridad de la familia DenseNet. Esta comparación tampoco reproduce nuestra DenseNet121 entrenada desde cero. [DRCA-Net](https://doi.org/10.1016/j.bspc.2022.104199) utiliza un ResNet50 modificado, con atención espacial y de canal en los decodificadores, para segmentar y tipificar simultáneamente. Ambos trabajos justifican estudiar representaciones residuales, pero sus F1 incluyen decisiones de detección y sus entradas no son los recortes nucleares independientes de V2.

[ISC-GAN](https://doi.org/10.1016/j.cmpb.2023.107768) estudia transferencia de H&E a IHC mediante CycleGAN, Mask R-CNN y aprendizaje por etapas. Evalúa tumor, estroma y linfocitos en seis imágenes IHC anotadas que contienen 750 células; obtiene AP de segmentación de 39,1 y AJI de 77,1. La coincidencia nominal de clases con NuCLS no vuelve comparables esas métricas con nuestro macro-F1. Además, emplea imágenes del dominio objetivo durante la adaptación: aplicar ese procedimiento a nuestra reserva cambiaría su condición de evaluación externa intacta. Es una línea para un experimento futuro predefinido, no una modificación retrospectiva del cierre actual.


### Evidencia en recortes nucleares y sesgo de procedencia

El estudio [Deep Learning for Cell Classification…](https://doi.org/10.1109/bibe60311.2023.00020) reúne aproximadamente 206.000 recortes de 64×64 píxeles: tres clases inmunes de Lizard y dos clases epiteliales/tumorales de PanNuke. Compara ResNet18, ConvNeXt y EfficientNet; ResNet18 preentrenada con entropía cruzada y muestreo ponderado obtiene el mejor resultado, con AUC por clase superiores a 0,97. Sin embargo, los aciertos de neutrófilos y eosinófilos permanecen alrededor de 63–65%, por lo que una AUC alta no elimina el problema de las clases minoritarias. El split aleatorio 70/30 se realiza por recorte y clase, sin separación por paciente documentada. Además, la procedencia de los datos está asociada a la clase. Estos factores limitan la comparación con la reserva independiente por paciente de NuCLS y apoyan reportar métricas por clase, además del promedio. La descripción de ConvNeXt como modificación de ResNet50 en la introducción no constituye una ejecución de ResNet50 estándar.


### Refinamiento contextual y límites de la comparación

[Hassan et al.](https://doi.org/10.1109/TIP.2023.3337666) entrenan un clasificador ResNet50 sobre recortes de núcleos y luego retiran su cabeza para construir representaciones de un grafo. El refinamiento utiliza núcleos detectados por HoVer-Net y relaciones entre células: su evaluación combina errores de detección y tipificación. Este trabajo respalda la utilidad de ResNet50 como representación nuclear, pero sus resultados finales no aíslan el clasificador ni constituyen una réplica de nuestro experimento. También muestra una limitación práctica: el grafo no puede recuperar un núcleo que el detector omitió.

Las propuestas recientes [UL-HVNet](https://doi.org/10.1145/3706890.3706921), [MDH-CMambaNet](https://doi.org/10.1109/IJCNN69854.2026.11729110) y [AMN](https://doi.org/10.1109/ICETCI71772.2026.11710727) añaden atención, deformaciones o contexto global a sistemas de segmentación y tipificación. Sus métricas requieren distinguir instancia, píxel y detección: por ejemplo, AMN calcula F1 sobre píxeles e incluye el fondo. El mayor tamaño o complejidad no garantiza transferencia: en su evaluación binaria externa MoNuSeg, AMN reporta F1 de 0,6191 frente a 0,6510 de U-Net. Las inconsistencias internas de algunos artículos y la ausencia de particiones explícitas por paciente se conservan en la matriz de lectura, en lugar de convertirlas en evidencia concluyente.


### Tamaño del recorte y agregación de predicciones

El estudio de [clasificación y fusión de características nucleares](https://doi.org/10.1002/ima.22676) compara InceptionV3, InceptionResNetV2 y NASNetLarge preentrenadas en ImageNet sobre CRCHistoPhenotypes. Al ampliar la ventana de 27 a 54 píxeles, InceptionV3 pasa de F1 ponderado 0,773 a 0,816; combinar cuatro tamaños produce 0,832. El ensamble de doce modelos alcanza 0,837. Estos resultados muestran una asociación entre representación contextual y desempeño dentro de ese experimento, sin aislar el efecto causal del contexto ni equivaler a macro-F1. Se excluyen núcleos próximos al borde, y los dos folds se separan por imagen sin independencia por paciente explícita. NuCLS también restringe recortes interiores, por lo que debe conservar esa condición al describir la población analizada. El SoftmaxCNN citado por este artículo no se cuenta como una nueva ejecución independiente.


### Cierre de recuperación y alcance de la entrega

La última lectura incorpora la revisión de [Xiong y Guo sobre diagnóstico renal](https://doi.org/10.12354/j.issn.1000-8179.2025.20251345), páginas 1258–1263. Integra imagen radiológica, histología, grado nuclear y pronóstico; es una fuente secundaria, sin experimento propio de clasificación nuclear. Sus modelos citados no incrementan las frecuencias de comparadores.

Los 13 informes no recuperados incluyen barreras editoriales o institucionales, repositorios sin archivo y un resumen de congreso sin informe extenso identificado. El capítulo IGI de 2023 no se da por leído a partir del capítulo homónimo de 2019 con DOI diferente. El acceso institucional no garantiza que todos los títulos estén suscritos. Se conserva título, DOI, fuente consultada y motivo individual. Esta limitación puede sesgar la cobertura y las frecuencias observadas.

La entrega satisface el alcance de una síntesis crítica documentada: comparación de tareas, entradas, particiones, métricas y limitaciones; justificación de tres modelos base; conexión con EDA y resultados. No afirma exhaustividad, revisión humana doble ni equivalencia entre métricas heterogéneas. La clasificación focal reúne 21 informes; los otros 145 informes leídos se distribuyen como contexto, tareas adyacentes, fuentes secundarias o sensibilidad editorial.
