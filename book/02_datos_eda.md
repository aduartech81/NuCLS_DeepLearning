# Datos y EDA orientado a decisiones

## Evidencia disponible
El inventario comunicado por el autor examinó 30.540 archivos sin errores de lectura reportados. Para QC contó 1.744 RGB y señaló coincidencia de estructura y conteo. Para noQC contó 2.200 RGB con discrepancia respecto al conteo de referencia. Otros subconjuntos permanecían pendientes de contraste remoto. Esto no demuestra por sí solo completitud, calidad de etiquetas ni ausencia de duplicados.

El paquete de piloto documenta 14.428 recortes de entrenamiento de 79 pacientes y 3.571 recortes de validación de 19 pacientes, para un total de 17.999 recortes. Estos conteos describen la selección del piloto, no todas las imágenes del dataset. El paquete verifica formato, separación de pacientes y hashes exactos; falta integrar sus salidas como evidencia final.

Se debe mantener trazabilidad recorte → anotación → imagen original → paciente → subconjunto. Los conjuntos multi-rater no se sumarán como observaciones independientes de los mismos campos.

## Plan de análisis y decisión asociada
| Análisis | Evidencia que debe incorporarse | Decisión que sustenta |
|---|---|---|
| Procedencia y permisos | Versión, URL, licencia comprobada, hashes y exclusiones | Uso y reproducibilidad |
| Balance | Conteos por clase/paciente, razón mayoritaria/minoritaria y entropía | Pérdida y métricas ante desbalance |
| Integridad y formato | Lectura completa, canales, bits, dimensiones, archivos ausentes | Elegibilidad de entradas |
| Inspección estratificada | Muestras aleatorias con etiquetas y origen | Ruido, artefactos y atajos visuales |
| Color y contraste | Histogramas, media y desviación por canal solo en train; saturación y contraste | Normalización y necesidad de transformación |
| Calidad multivariada | Análisis conjunto de indicadores de desenfoque, color y contraste, con revisión visual | Señalar atípicos; no borrarlos automáticamente |
| Duplicados | Hash exacto y similitud perceptual; revisión de candidatos | Evitar fuga entre particiones |
| Etiquetas | Revisión muestral y acuerdo de anotadores cuando esté disponible | Incertidumbre de la supervisión |
| Dependencia | Pacientes/campos y ausencia de cruce entre grupos | Partición e inferencia |
| Desplazamiento | Comparación train-validación con efecto e incertidumbre | Evaluar generalización y sesgo |

Cada figura debe acompañarse de resultado observado, interpretación, decisión y limitación. No se atribuirán mecanismos biológicos a efectos pequeños ni se afirmará MAR sin evidencia. Las pruebas múltiples, cuando se utilicen, tendrán familia definida y corrección, por ejemplo Holm.

## Preprocesamiento implementado en el piloto
Recortes RGB 128×128 sin padding; intensidades divididas por 255; rotaciones múltiplos de 90° y reflexión horizontal únicamente en train. No se aplica CLAHE ni normalización de tinción. Dividir por 255 no equivale a estandarizar con media y desviación aprendidas en train: esa diferencia debe resolverse y documentarse para cumplir la guía antes del benchmark, sin modificar silenciosamente el piloto en curso.

## Protección de la evaluación
No usar la prueba histórica ya expuesta como test virgen. Definir y congelar una reserva no utilizada, verificar agrupamiento y hashes antes del benchmark. La validación selecciona época e hiperparámetros; su desempeño no es una estimación final insesgada.
