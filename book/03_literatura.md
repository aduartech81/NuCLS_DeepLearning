# Estado del arte: clasificación nuclear en histología

Esta revisión orienta candidatos, no constituye búsqueda sistemática completa. No se han ejecutado búsquedas autenticadas en WoS o Scopus ni se ha generado un PRISMA verificable. No se inventan frecuencias de uso.

| Fuente primaria | Tarea / evidencia identificada | Consecuencia |
|---|---|---|
| Sirinukunwattana et al. (2016), Locality Sensitive Deep Learning. https://doi.org/10.1109/TMI.2016.2525803 ; https://pubmed.ncbi.nlm.nih.gov/26863654/ | Detección y clasificación nuclear en histología de colon; CNN y contexto vecinal. Consulta de resumen. | Apoya estudiar CNN en este problema; la CNN local implementada no es reproducción exacta del artículo. |
| Amgad et al. (2022), NuCLS. https://pmc.ncbi.nlm.nih.gov/articles/PMC9112766/ | Dataset mamario y adaptación de Mask R-CNN; ResNet50 como backbone. | Fuente de procedencia; no contar como uso de ResNet18 standalone ni de MobileNetV2. |
| Sánchez-Torres et al. (2026), A Comparative Analysis… https://doi.org/10.1155/acis/4540418 | Clasificación nuclear con ResNet50 y ViT sobre PanNuke. | Evidencia pertinente de familias, no frecuencia de ResNet18. |
| NDG-CAM (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9495364/ | ResNet18, ResNet50 y MobileNetV2 como backbones de DeepLab v3+ para segmentación/detección. | Tarea adyacente; **excluir del conteo de baselines de clasificación nuclear aislada**. |
| Nuclei Classification in ER-IHC Stained Histopathology Images using Deep Learning Models. https://shdl.mmu.edu.my/11229/ | Resumen institucional: comparación de 32 modelos preentrenados; familias MobileNet y ResNet entre otras, intensidad ER-IHC. | Tinción y objetivo distintos; recuperar texto y lista exacta antes de contar arquitecturas. |
| SENUCLS, implementación oficial. https://github.com/Lewislou/SENUCLS | GNN con máscaras de instancia y contexto estructural. | Sesgo distinto pero requiere otro pipeline y no es automáticamente baseline simple. |

## Decisión de ingeniería provisional
CNN pequeña: convoluciones convencionales y bajo número de parámetros. ResNet18: conexiones residuales. MobileNetV2: convoluciones separables, bottlenecks y residuales invertidos. Estas diferencias permiten explorar coste/aprendizaje, pero **no prueban que sean los tres modelos más frecuentes y básicos exigidos**. MobileNetV2 es especialmente provisional. La revisión podría exigir reemplazarlo.

## Búsqueda pendiente reproducible
Cadena base: ("nucleus classification" OR "nuclei classification" OR "cell type classification") AND (histopatholog* OR histolog*) AND ("deep learning" OR CNN OR "convolutional neural network") AND (baseline OR compar*).

Registrar por base: fecha, cadena exacta, filtros, resultados exportados, duplicados, motivos de exclusión; por estudio: dataset/tinción/etiquetas, unidad de partición, arquitectura exacta, si baseline o propuesta, preentrenamiento y complejidad. Separar clasificación de núcleos aislados de segmentación, detección y clasificación de parches tumorales. Contar una vez por estudio y arquitectura, sin convertir automáticamente un backbone en clasificador independiente. Publicar la matriz y la frecuencia antes de declarar modelos definitivos.
