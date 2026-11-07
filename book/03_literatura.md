# Estado del arte: clasificación nuclear en histología

Se presenta una revisión narrativa de antecedentes de clasificación nuclear. Su propósito es distinguir evidencia directamente relacionada con la clasificación de recortes y trabajos sobre tareas adyacentes. La revisión no incluye una búsqueda sistemática autenticada en WoS o Scopus; por tanto, no estima exhaustividad, frecuencias de uso ni un flujo PRISMA.

| Fuente primaria | Tarea / evidencia identificada | Consecuencia |
|---|---|---|
| Sirinukunwattana et al. (2016), Locality Sensitive Deep Learning. https://doi.org/10.1109/TMI.2016.2525803 ; https://pubmed.ncbi.nlm.nih.gov/26863654/ | Detección y clasificación nuclear en histología de colon; CNN y contexto vecinal. Consulta de resumen. | Apoya estudiar CNN en este problema; la CNN local implementada no es reproducción exacta del artículo. |
| Amgad et al. (2022), NuCLS. https://pmc.ncbi.nlm.nih.gov/articles/PMC9112766/ | Dataset mamario y adaptación de Mask R-CNN; la fuente se utiliza para documentar la procedencia, no para contabilizar una arquitectura de clasificación aislada. | Fuente de procedencia; no contar como uso de ResNet18 standalone ni de MobileNetV2. |
| Sánchez-Torres et al. (2026), A Comparative Analysis… https://doi.org/10.1155/acis/4540418 | Clasificación nuclear con ResNet50 y ViT sobre PanNuke. | Evidencia pertinente de familias, no frecuencia de ResNet18. |
| NDG-CAM (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9495364/ | ResNet18, ResNet50 y MobileNetV2 como backbones de DeepLab v3+ para segmentación/detección. | Tarea adyacente; **excluir del conteo de baselines de clasificación nuclear aislada**. |
| Nuclei Classification in ER-IHC Stained Histopathology Images using Deep Learning Models. https://shdl.mmu.edu.my/11229/ | Resumen institucional: comparación de 32 modelos preentrenados; familias MobileNet y ResNet entre otras, intensidad ER-IHC. | Tinción y objetivo distintos; el resumen consultado no permite establecer la lista exacta de arquitecturas comparadas. |
| SENUCLS, implementación oficial. https://github.com/Lewislou/SENUCLS | GNN con máscaras de instancia y contexto estructural. | Sesgo distinto pero requiere otro pipeline y no es automáticamente baseline simple. |

## Relación entre antecedentes y modelos evaluados
CNN pequeña: convoluciones convencionales y bajo número de parámetros. ResNet18: conexiones residuales. MobileNetV2: convoluciones separables, bottlenecks y residuales invertidos. Estas diferencias permiten explorar la relación entre capacidad, aprendizaje y costo. Sin embargo, la evidencia recopilada no establece que sean los tres modelos exactos más frecuentes de la tarea. En particular, el uso de MobileNetV2 como extractor en segmentación no valida por sí solo su selección como referencia de clasificación nuclear.

## Delimitación bibliográfica
La cadena temática que delimita el alcance de esta revisión es: ("nucleus classification" OR "nuclei classification" OR "cell type classification") AND (histopatholog* OR histolog*) AND ("deep learning" OR CNN OR "convolutional neural network") AND (baseline OR compar*).

Esta cadena expresa el alcance temático y no se presenta como una consulta ejecutada en las bases mencionadas. La clasificación de núcleos aislados se distingue de la segmentación, la detección y la clasificación de parches tumorales. La comparación entre estudios también está condicionada por la tinción, el tejido, las etiquetas y la unidad de partición. En consecuencia, los resultados publicados no se consideran directamente comparables con el macro-F1 de las tres categorías del presente piloto.

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

La evidencia consultada respalda el interés de estudiar representaciones convolucionales y contexto. No proporciona una frecuencia verificable de CNN local, ResNet18 y MobileNetV2 como las tres referencias más utilizadas. Esta distinción delimita la fuerza de la justificación bibliográfica del experimento.

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
