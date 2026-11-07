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
