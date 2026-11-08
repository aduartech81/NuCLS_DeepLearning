# Estado del arte: clasificación nuclear en histología

La evidencia revisada sitúa el problema en tres líneas: clasificación por textura local, incorporación del contexto alrededor del núcleo y uso de relaciones entre células. La comparación de arquitecturas solo es interpretable si se distinguen estas representaciones y se mantiene una evaluación independiente del ajuste. El presente estudio adopta recortes RGB con contexto y tres categorías; no evalúa segmentación ni reconstrucción de relaciones celulares.


La revisión distingue clasificación de recortes nucleares, segmentación y detección. El 7 de noviembre de 2026 se recibieron exportaciones de Scopus, Web of Science e IEEE Xplore obtenidas mediante acceso institucional. La síntesis de antecedentes se complementa con un inventario reproducible de registros y decisiones de lectura.

## Recuperación y depuración bibliográfica

| Base | Exportación original | Publicación 2018–2026 |
|---|---:|---:|
| Scopus | 1.097 | 1.057 |
| Web of Science | 328 | 318 |
| IEEE Xplore | 292 | 273 |
| Total | 1.717 | 1.648 |

Se separaron 69 registros por año de publicación fuera de la ventana analítica. La normalización del DOI permitió agrupar 318 registros repetidos y producir 1.330 unidades para cribado: 1.287 con DOI distinto y 43 sin DOI. Siete grupos presentan títulos normalizados coincidentes; no se fusionaron automáticamente porque un título puede corresponder a versiones o documentos distintos. Estas cifras describen identificación y depuración, no inclusión de estudios ni un flujo PRISMA completo.

La consulta comunicada para la búsqueda fue `(nucle* AND classif*) AND (histolog* OR histopatholog*) AND ("deep learning" OR "convolutional neural network" OR CNN OR transformer*)`, con adaptación por campo en cada plataforma. Las exportaciones permiten verificar registros y fechas de publicación, pero no reconstruyen por sí solas todos los filtros de la interfaz. El historial de consultas constituye una evidencia independiente.

La extracción distingue arquitectura exacta, función del modelo, representación de entrada, conjunto de datos, unidad de partición y métrica. La lectura de títulos y resúmenes identifica candidatos para texto completo; la prioridad automática no determina exclusión ni calidad. La revisión asistida por IA no representa dos revisores independientes.

## Alcance de la lectura documental

Se documentaron decisiones o derivaciones de lectura para 115 registros del inventario. El lote más reciente comprende 80 títulos y 16 resúmenes; estos últimos se suman a las 24 lecturas adicionales de resúmenes previamente registradas. Una derivación a lectura de resumen o texto completo no equivale a inclusión definitiva. La selección dirigida identificó estudios de clasificación nuclear y separó tareas adyacentes: mitosis, intensidad inmunohistoquímica, graduación de atipia y diagnóstico de imágenes completas. Estas tareas aportan contexto, pero sus arquitecturas no se contabilizan como comparadores equivalentes de clasificación fenotípica en H&E. El inventario conserva 1.215 registros sin decisión; por ello, no se atribuye exhaustividad a la síntesis ni se estima una frecuencia poblacional de arquitecturas.

Las 80 decisiones nuevas se conservan en [el registro adicional](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/cribado_adicional_80.csv). Las decisiones previas y su fundamento se conservan en [el registro de lectura](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/revision_adicional_24.csv). La evaluación de calidad distingue información ausente de un defecto demostrado; un resumen insuficiente no constituye evidencia de fuga de datos.

## Calidad de las anotaciones y pertinencia de NuCLS

Amgad et al. (2022) sitúan la generación de etiquetas en el centro del problema: NuCLS reúne anotaciones de estudiantes y patólogos sobre histología mamaria H&E de TCGA. El trabajo distingue anotaciones individuales y múltiples, e incorpora inferencia de etiquetas y evaluación de concordancia. Por tanto, una etiqueta disponible no equivale a una observación exenta de incertidumbre.

Para este proyecto, la consecuencia es metodológica: verificar archivos, dimensiones y valores faltantes acredita integridad técnica, pero no mide concordancia diagnóstica. La selección de tres categorías y de recortes interiores también delimita la población evaluada. Las métricas obtenidas deben interpretarse respecto a esas etiquetas y reglas de selección, sin extenderlas a todas las células presentes en una lámina.

Fuente: [Amgad et al., descripción de datos, concordancia y limitaciones](https://pmc.ncbi.nlm.nih.gov/articles/PMC9112766/).

## Tendencias recientes y criterios de comparabilidad

La lectura adicional de resúmenes identifica una transición desde clasificadores de ventanas hacia sistemas que resuelven conjuntamente localización, segmentación y tipo nuclear. Esa evolución amplía las capacidades del sistema, pero también cambia el significado de sus métricas. Los siguientes registros se utilizan para orientar la recuperación de textos completos; sus cifras no se incorporan al ranking de clasificadores ni al conteo de arquitecturas verificadas.

| Línea | Estudios identificados en los resúmenes exportados | Implicación para el experimento |
|---|---|---|
| Textura y atención | TexSegNet, DOI 10.1109/EMBC58623.2025.11253497 | Distinguir desempeño conjunto de detección/clasificación del desempeño condicionado a conocer la ubicación del núcleo |
| Contexto, escala y orientación | MOSAIC, DOI 10.1016/j.cmpb.2026.109334; BDCNet, DOI 10.1016/j.eswa.2026.132123 | Las relaciones espaciales y la fusión multiescala requieren entradas y módulos diferentes de los tres clasificadores V2 |
| Generalización y categorías diversas | HistoPLUS, DOI 10.1016/j.jpi.2026.100696; KongNet, DOI 10.1016/j.media.2026.104233 | La evaluación externa y la cobertura de clases deben documentarse; no se infieren a partir de un F1 elevado |
| Balance y aprendizaje multitarea | AFINITI, DOI 10.1007/s00521-024-10114-4; aumento copy-paste, DOI 10.1007/s10278-024-01018-9 | La mejora de clases minoritarias depende del objetivo y del procedimiento; no justifica trasladar automáticamente una técnica al conjunto NuCLS |
| Clasificación con contexto y representación de láminas | HistoMSC, DOI 10.1016/j.compbiomed.2025.109991 | Separar la red de localización de los clasificadores de recortes antes de atribuir resultados a una arquitectura |

La evidencia de resumen permite reconocer líneas de investigación, pero no comprobar particiones, ablaciones ni todas las arquitecturas de comparación. La extracción de F1 por clase, Dice, AP o calidad panóptica exige conservar su definición: responden a objetivos distintos y no pueden ordenarse en una única escala de rendimiento.

## Antecedentes y comparabilidad

| Fuente primaria | Tarea / evidencia identificada | Consecuencia |
|---|---|---|
| Sirinukunwattana et al. (2016), Locality Sensitive Deep Learning. https://doi.org/10.1109/TMI.2016.2525803 ; https://pubmed.ncbi.nlm.nih.gov/26863654/ | Detección y clasificación nuclear en histología de colon; CNN y contexto vecinal. Consulta de resumen. | Apoya estudiar CNN en este problema; la CNN local implementada no es reproducción exacta del artículo. |
| Amgad et al. (2022), NuCLS. https://pmc.ncbi.nlm.nih.gov/articles/PMC9112766/ | Dataset mamario y adaptación de Mask R-CNN; la fuente se utiliza para documentar la procedencia, no para contabilizar una arquitectura de clasificación aislada. | Fuente de procedencia; no contar como uso de ResNet18 standalone ni de MobileNetV2. |
| Sánchez-Torres et al. (2026), A Comparative Analysis… https://doi.org/10.1155/acis/4540418 | Clasificación nuclear con ResNet50 y ViT sobre PanNuke. | Evidencia pertinente de familias, no frecuencia de ResNet18. |
| NDG-CAM (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9495364/ | ResNet18, ResNet50 y MobileNetV2 como backbones de DeepLab v3+ para segmentación/detección. | Tarea adyacente; **excluir del conteo de baselines de clasificación nuclear aislada**. |
| Nuclei Classification in ER-IHC Stained Histopathology Images using Deep Learning Models. https://shdl.mmu.edu.my/11229/ | Resumen institucional: comparación de 32 modelos preentrenados; familias MobileNet y ResNet entre otras, intensidad ER-IHC. | Tinción y objetivo distintos; el resumen consultado no permite establecer la lista exacta de arquitecturas comparadas. |
| SENUCLS, implementación oficial. https://github.com/Lewislou/SENUCLS | GNN con máscaras de instancia y contexto estructural. | Sesgo distinto pero requiere otro pipeline y no es automáticamente baseline simple. |

## Antecedentes del piloto exploratorio
El piloto histórico contrastó una CNN local de baja capacidad, ResNet18 con conexiones residuales y MobileNetV2 con convoluciones separables y bloques residuales invertidos. Estas diferencias permiten explorar la relación entre capacidad, aprendizaje y costo. Sin embargo, la evidencia recopilada no establece que sean los tres modelos exactos más frecuentes de la tarea. En particular, el uso de MobileNetV2 como extractor en segmentación no valida por sí solo su selección como referencia de clasificación nuclear.

## Alcance y criterios de selección de estudios

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

## Evidencia cuantitativa y comparabilidad

Sánchez-Torres et al. (2026) compararon ResNet50 y ViT en PanNuke con cinco clases. La tabla 6 distingue núcleos con contexto y núcleos aislados:

| Modelo y entrada | F1 neoplásico (%) | F1 conectivo (%) | F1 inflamatorio (%) | F1 epitelial (%) | F1 muerto (%) |
|---|---:|---:|---:|---:|---:|
| ResNet50 con contexto | 82,90 | 71,49 | 71,98 | 71,49 | 49,39 |
| ResNet50 sin contexto | 78,71 | 63,21 | 68,99 | 64,39 | 41,13 |
| ViT con contexto | 82,19 | 69,01 | 70,19 | 71,59 | 47,93 |

La tabla no presenta dispersión. La mejora conectiva de ResNet50 al conservar contexto es de 8,28 puntos; su extrapolación a NuCLS requiere cautela. Las clases, particiones y redes difieren. Además, la tabla 14 combina valores de distintos tratamientos: para núcleos muertos muestra 51,66%, asociado al sobremuestreo en la tabla 11, frente a 49,39% en la tabla 6. Se conserva una única configuración para esta extracción.

Fuente: [Sánchez-Torres et al., tablas 6, 11 y 14](https://doi.org/10.1155/acis/4540418).

### Implicación para el presente estudio

El piloto utiliza ventanas que incluyen contexto, pero no contiene una ablación que separe núcleo y entorno. En consecuencia, no permite determinar qué proporción del desempeño procede de morfología nuclear, células vecinas o tinción. Tampoco se interpreta la proximidad numérica con un resultado publicado como reproducción: una comparación válida requiere coincidencia de etiquetas, partición, métrica y tratamiento de imágenes.

La evidencia consultada respalda el interés de estudiar representaciones convolucionales y contexto. CNN local, ResNet18 y MobileNetV2 corresponden al piloto histórico; la selección V2 se fundamenta más adelante mediante comparadores exactos y adaptaciones explícitas.

## Modelos comparativos en estudios de clasificación nuclear

### Supervisión limitada y transferencia entre tejidos

Jacobs, Brostow, Freeman, Alexander y Panagiotaki (2017), en *Detecting and Classifying Nuclei on a Budget*, compararon una CNN supervisada, su ajuste por transferencia y una CNN Γ-ladder semisupervisada. La clasificación utiliza ventanas de 27×27 píxeles y tres categorías prostáticas. Se incluye como antecedente metodológico anterior al intervalo reciente de búsqueda.

| Proporción etiquetada | Macro-F1 CNN supervisada | Macro-F1 CNN ajustada | Macro-F1 Γ-ladder |
|---|---:|---:|---:|
| 1% | 0,639 ± 0,021 | 0,695 ± 0,061 | 0,738 ± 0,019 |
| 3% | 0,725 ± 0,012 | 0,752 ± 0,008 | 0,762 ± 0,010 |
| 5% | 0,761 ± 0,003 | 0,769 ± 0,007 | 0,765 ± 0,008 |
| 100% | 0,820 ± 0,005 | 0,819 ± 0,002 | 0,825 ± 0,004 |

La ventaja Γ-ladder frente a supervisión completa pasa de 9,9 puntos con 1% etiquetado a 0,5 puntos con todos los datos. La ventaja arquitectónica depende, por tanto, del régimen de supervisión. La dispersión publicada no debe confundirse con un intervalo de confianza. La CNN de este estudio no es idéntica a la CNN local implementada en NuCLS.

Fuente: [texto completo institucional, tabla 3](https://discovery.ucl.ac.uk/id/eprint/1573202/1/LABELS2017_7.pdf).

### Conexiones densas y recurrencia convolucional

Alom, Asari, Parwani y Taha (2022) evaluaron clasificación, segmentación y detección en experimentos separados. Para clasificación de núcleos de colon compararon DenseNet y DCRN, con resultados F1 de **0,7941** y **0,8111**, respectivamente, en el apartado de análisis. La diferencia es de 1,70 puntos. El trabajo describe validación cruzada de cinco particiones.

Su comparación incluye la referencia softmax CNN con predictor de vecindad; no corresponde a una evaluación de MobileNetV2 como clasificador aislado. Los resultados de Dice de R2U-Net y F1 de detección de UD-Net pertenecen a otras tareas y se excluyen de la comparación de clasificación. Las cinco particiones no equivalen a cinco semillas y, sin equiparar agrupación y protocolo, la diferencia publicada no es directamente comparable con el piloto NuCLS.

Referencia: Alom, Z., Asari, V. K., Parwani, A. y Taha, T. M. (2022). *Microscopic nuclei classification, segmentation, and detection with improved deep convolutional neural networks (DCNN).* Diagnostic Pathology, 17, 38. [doi:10.1186/s13000-022-01189-5](https://doi.org/10.1186/s13000-022-01189-5).

## Síntesis crítica de los protocolos

| Estudio | Problema y conjunto | Comparadores identificados | Evidencia cuantitativa | Condición que limita la comparación |
|---|---|---|---|---|
| Jacobs et al. (2017) | Clasificación prostática; tres clases | CNN supervisada, ajuste por transferencia y Γ-ladder | Macro-F1 y dispersión, tabla anterior | Cambia la fracción etiquetada; tamaño de ventana y tejido distintos de NuCLS |
| Alom et al. (2022) | Clasificación nuclear de colon | DenseNet, DCRN y referencia CNN con vecindad | F1 0,7941 y 0,8111 para DenseNet y DCRN | Cinco particiones de validación cruzada; no son repeticiones por semilla |
| Sánchez-Torres et al. (2026) | Clasificación PanNuke; cinco clases | ResNet50 y ViT | F1 por clase, tabla anterior | Contexto y balance cambian los resultados; sin dispersión en la tabla extraída |
| Amgad et al. (2022), NuCLS | Clasificación, localización y segmentación mamaria | Adaptación de Mask R-CNN | Fuente de datos y diseño de tareas | Un detector con clasificación no equivale a un clasificador de recortes |
| NDG-CAM (2022) | Detección mediante segmentación | U-Net, SegNet y DeepLab v3+ con diferentes extractores | No se incorpora su Dice al F1 de clasificación | ResNet18 y MobileNetV2 aparecen como componentes de otra tarea |

La coincidencia de un nombre de familia no acredita coincidencia de arquitectura. Una CNN supervisada con ventanas de 27×27 no constituye evidencia específica de la configuración 32–64–128 implementada aquí. De igual modo, los resultados de ResNet50 no se trasladan a ResNet18. Tampoco se interpreta la existencia de comparadores publicados como ausencia demostrada de fuga de datos: la unidad de partición, el acceso a validación y la selección de hiperparámetros deben establecerse para cada protocolo.

## Relación con la selección del piloto

La literatura examinada muestra tres dimensiones relevantes: capacidad de representación, aprovechamiento del contexto y cantidad de supervisión. El piloto estudia principalmente la primera mediante tres redes convolucionales entrenadas desde cero, manteniendo fijos contexto y etiquetas. No reproduce las comparaciones semisupervisadas ni las arquitecturas con grafos o máscaras de instancia.

El hallazgo bibliográfico central es una limitación de correspondencia: **la evidencia recuperada no sustenta todavía una selección por frecuencia de las tres arquitecturas exactas del piloto**. No se convierte una frecuencia de familias en frecuencia de modelos, ni se sustituye una revisión sistemática por el número de enlaces recuperados. En consecuencia, estos resultados establecen una referencia experimental para las implementaciones evaluadas, sin acreditar que constituyan las tres referencias más recurrentes del campo.

La búsqueda adicional del 7 de noviembre de 2026 utilizó las consultas web `"nuclei classification" "ResNet18" baseline NuCLS`, `"nuclei classification" "MobileNetV2"` y `"nucleus classification" "CNN" comparative baseline histology`. Estas consultas complementan la revisión narrativa y no se presentan como búsquedas ejecutadas dentro de WoS, Scopus o IEEE Xplore. La selección no contó con un segundo revisor independiente; no se atribuye un procedimiento de consenso inexistente.

## CNN de complejidad moderada: RCCNet

Basha et al. compararon RCCNet con softmaxCNN_IN27, una variante softmaxCNN, AlexNet adaptada, CIFAR-VGG, GoogLeNet adaptada y WRN. RCCNet utiliza entradas RGB de 32×32, cuatro convoluciones de 32, 32, 64 y 64 filtros, dos reducciones espaciales y capas densas de 512, 512 y cuatro salidas. El entrenamiento incorpora BatchNorm y dropout.

En CRCHistoPhenotypes se informa una partición 80/20 de 22.444 recortes y un F1 ponderado de 0,7887. El texto no establece en esa descripción separación por paciente; tampoco presenta dispersión entre semillas en la tabla comparativa. Además, muestra curvas de exactitud de prueba durante el entrenamiento. Estos aspectos limitan la interpretación de generalización y requieren distinguir seguimiento de prueba de selección de modelos.

El estudio aporta una arquitectura verificable y comparadores concretos, pero su métrica, resolución, tejido y clases difieren del piloto NuCLS. Su presencia no prueba que RCCNet sea uno de los tres modelos más frecuentes.

Fuente: Basha et al., ICARCV 2018, [texto completo de autor, secciones II–IV](https://arxiv.org/html/1810.02797v3), [DOI](https://doi.org/10.1109/ICARCV.2018.8581147).


## Clasificadores independientes y sistemas híbridos: OLConvNet

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

## Justificación metodológica derivada de la revisión

La evidencia permite formular tres decisiones para NuCLS. Primero, las comparaciones deben mantener la misma unidad de entrada y salida: recortes RGB y categorías nucleares. Segundo, las transformaciones aprendidas y el balanceo se estiman únicamente con entrenamiento, después de fijar la partición. Tercero, la complejidad y el rendimiento se documentan para la implementación exacta; una familia residual no equivale a una profundidad concreta ni un extractor a un sistema completo.

El aporte del experimento se sitúa en una comparación reproducible bajo separación por paciente y centro de origen, con incertidumbre entre ejecuciones y entre pacientes. Esta delimitación evita presentar diferencias entre publicaciones como superioridad de una red, cuando también cambian el tejido, las etiquetas, el contexto, el balanceo y la evaluación.


## Referencia residual explícita: GrEp

Frei et al. (2026) evaluaron ResNet18 aislada en la ablación de GrEp, una propuesta de refinamiento mediante grafos. La comparación corresponde a células epiteliales normales y malignas.

| Referencia | Problema | Dataset de evaluación | Modelo de referencia | Métricas | Valores (%) |
|---|---|---|---|---|---|
| Frei et al., tabla 4 | Subclasificación epitelial binaria | TCGA | ResNet18 sin grafo ni filtro mediano | F epitelial / F maligno / F normal | 87,58 ± 0,97 / 90,83 ± 0,84 / 82,01 ± 1,22 |

La implementación parte de ImageNet, incorpora pooling adaptativo y salida binaria, y utiliza AdamW con tasa 10⁻⁶ durante 150 épocas. Este antecedente acredita el uso de ResNet18 como referencia de clasificación nuclear, además de su papel como extractor. Sin embargo, no reproduce el entrenamiento desde cero ni las tres categorías del piloto NuCLS. El valor del sistema completo con grafos no se atribuye a ResNet18 aislada.

Fuente: [Frei et al., texto completo de autor, sección 3.3 y tabla 4](https://aibex.ch/research/papers/Frei2025.pdf); [DOI](https://doi.org/10.1016/j.patcog.2025.112197).


## Frecuencia de comparadores y selección operativa v2

La extracción estructurada cuenta una vez cada DOI por arquitectura y separa variantes adaptadas de versiones estándar. En cuatro textos con comparaciones verificadas, ResNet50 aparece en dos estudios; las restantes arquitecturas identificadas aparecen en uno. Estas frecuencias describen el subconjunto extraído y no todo el corpus recuperado. La [tabla completa de comparadores](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/evidencias/literatura/comparadores_texto_completo.csv) conserva problema, conjunto, modelo, métricas y valores por fuente.

| Selección v2 | Estudios verificados | Parámetros, tres clases | Rasgo estructural |
|---|---:|---:|---|
| softmaxCNN con BatchNorm, adaptada | 1 | 898.687 | Convoluciones secuenciales y clasificador pequeño |
| DenseNet121 | 1 | 6.956.931 | Concatenación densa de representaciones |
| ResNet50 | 2 | 23.514.179 | Conexiones residuales bottleneck |

ResNet50 se prioriza por recurrencia exacta en clasificación nuclear multiclase. La CNN pequeña aporta una referencia de menor capacidad; DenseNet121 añade otro tipo de conectividad con menos parámetros que las variantes VGG/AlexNet registradas. Esta selección combina frecuencia, complejidad y diversidad estructural; no supone que las tres minimicen simultáneamente todos los criterios. DenseNet121 tiene más profundidad nominal que ResNet50, aunque menos parámetros.

La CNN pequeña reproduce el conteo publicado de 899.200 parámetros para cuatro clases y entrada 27×27. Para utilizar las ventanas comunes de 128×128 se reduce el mapa de 30×30 a una cuadrícula de 5×5 mediante promedios en bloques disjuntos de 6×6, equivalentes al pooling adaptativo de esas dimensiones. Se conservan las dimensiones del clasificador sin añadir parámetros. Esa adaptación modifica la agregación espacial y se declara explícitamente; no constituye reproducción exacta del experimento original. Las tres implementaciones superaron pruebas de propagación y gradientes con tensores sintéticos, sin entrenamiento sobre NuCLS v2.

El protocolo contempla inicialización desde cero y condiciones comunes, a diferencia de algunos estudios que emplean transferencia. La función de estas redes como referencia es comparable a la de un modelo logístico en una evaluación clásica: establecer un desempeño reproducible que deba superarse. No implica igualdad de capacidad ni supuestos lineales.

La selección y sus adaptaciones se describen en [el protocolo v2](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/protocolo/seleccion_modelos_v2.md). El [flujo experimental](https://github.com/aduartech81/NuCLS_DeepLearning/blob/main/protocolo/ejecucion_integrada_v2.md) separa búsqueda, piloto, planificación de corridas, evaluación final y reserva. Los resultados de CNN local, ResNet18 y MobileNetV2 siguen correspondiendo al piloto anterior.

## Evaluación crítica de los antecedentes principales

La evaluación se organiza por aspectos que afectan la comparabilidad; no se asigna una puntuación agregada que convierta información no reportada en un defecto demostrado.

| Estudio | Aporte verificable | Aspecto que limita la comparación | Consecuencia para NuCLS |
|---|---|---|---|
| Basha et al., RCCNet (2018) | CNN compacta y comparadores adaptados; arquitectura y conteo de parámetros descritos | F1 ponderado, cuatro clases y resolución distinta; agrupación por paciente no establecida en la descripción revisada | Declarar la adaptación a 128×128 y mantener separación por paciente; no comparar directamente el F1 publicado con macro-F1 |
| OLConvNet, DOI 10.1145/3345318 | Separa clasificadores CNN de sistemas híbridos con características manuales | Generación sintética descrita antes de la división; riesgo de dependencia entre particiones; agrupación por paciente no establecida | Evitar generación previa a la partición y atribuir a ResNet50 aislada únicamente su resultado de la tabla correspondiente |
| Sánchez-Torres et al. (2026) | Comparación de contexto frente a núcleo aislado con cinco categorías PanNuke | La tabla comparativa no informa dispersión; distintas tablas combinan tratamientos diferentes | Conservar una configuración por comparación y estudiar los recortes con contexto como una entrada definida, sin mezclar resultados |
| Frei et al., GrEp (2026) | Ablación que identifica ResNet18 sin refinamiento por grafo | Subclasificación epitelial binaria y transferencia desde ImageNet; tarea distinta de las tres categorías de NuCLS | Utilizarlo como evidencia de una referencia residual, sin trasladar su puntuación a clasificación multiclase desde cero |

Las referencias y las tablas de origen se identifican en las secciones anteriores. La incertidumbre por semillas, la separación por paciente y la unidad de cálculo del F1 no se consideran intercambiables entre publicaciones.

## Síntesis de la evidencia y brecha de investigación

Los clasificadores convolucionales constituyen referencias pertinentes porque aprenden características locales directamente de los píxeles. Sin embargo, la evidencia revisada no sostiene una arquitectura universalmente superior. Las puntuaciones dependen del tejido, de las categorías, del contexto incluido, del preentrenamiento y de la forma de dividir los datos. El resultado de un sistema híbrido tampoco equivale al de su red extractora utilizada aisladamente.

La comparación de PanNuke muestra que retirar contexto puede disminuir el F1 de determinadas categorías; esto justifica declarar con precisión qué información contiene cada ventana. No permite afirmar que todo contexto sea beneficioso: el fondo y las características de adquisición también pueden introducir señales de procedencia. El diagnóstico de desplazamiento de NuCLS indica que las particiones son parcialmente distinguibles mediante descriptores sencillos, lo que refuerza la necesidad de separación por paciente y TSS y de una interpretación prudente de la generalización.

La brecha que aborda este entregable es una comparación controlada de tres referencias sobre la misma selección de recortes NuCLS, con preprocesamiento ajustado en entrenamiento, esfuerzo de búsqueda común y variabilidad entre ejecuciones. Se trata de una contribución experimental dentro del proyecto académico, no de una afirmación de novedad mundial ni de una arquitectura original. El baseline resultante deberá expresarse con su incertidumbre y su alcance poblacional.

## Conclusión de la revisión dirigida

La extracción disponible respalda el uso de una CNN compacta con BatchNorm y de redes con conexiones densas o residuales como comparadores técnicamente diferenciados. La selección v2 queda vinculada a implementaciones concretas y adaptaciones explícitas. Su respaldo documental no demuestra que sean los tres modelos más básicos o más frecuentes de todo el campo: esa afirmación requeriría completar el cribado y contrastar las alternativas del corpus.

La síntesis permite fundamentar el diseño actual y formular sus límites. El inventario bibliográfico permanece como un proceso de selección parcial; los registros aún no evaluados no se cuentan como exclusiones ni como estudios incluidos. Por tanto, el flujo de identificación y depuración no se presenta como un PRISMA completo.
