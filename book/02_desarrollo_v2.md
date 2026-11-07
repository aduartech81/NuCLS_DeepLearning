# Desarrollo v2: calidad, balance y distribución

La nueva partición contiene 14.539 recortes de entrenamiento, correspondientes a 83 pacientes, y 2.049 de validación, de 21 pacientes. Los pacientes y los códigos TSS son disjuntos entre grupos. Este análisis utiliza metadatos de esas dos particiones y no calcula predicciones ni medidas de rendimiento sobre la reserva.

![Composición por clase, retención e imágenes aportadas por paciente.](figuras/eda_desarrollo_v2.svg)

## Calidad de datos y tratamiento de faltantes

La unidad de entrada es una ventana RGB de 128×128 píxeles vinculada a una anotación, una clase y un paciente. En los 16.588 recortes de desarrollo se completó la lectura y verificación de formato, dimensiones y huellas digitales. La ausencia de fallos en ese conjunto procesado no acredita por sí sola que todos los archivos originales de NuCLS estén completos ni que sus anotaciones sean correctas.

Los faltantes deben distinguirse de las exclusiones geométricas: una ventana que exige relleno no es un valor ausente imputable. El conjunto analítico conserva únicamente recortes elegibles y no incorpora píxeles sintéticos para completar bordes. Las etiquetas no se imputan. Tampoco se imputa la identidad del paciente, indispensable para separar las particiones. Las entradas del clasificador son los píxeles, no metadatos clínicos; por ello no se aplica imputación tabular al modelo actual. No se ha establecido un mecanismo MCAR, MAR o MNAR para los metadatos originales.

La verificación de integridad y la evaluación de calidad visual responden a preguntas distintas. Una imagen puede abrir correctamente y presentar artefactos o una anotación discutible. Los descriptores de color y textura caracterizan heterogeneidad; no constituyen un diagnóstico automático de desenfoque ni validan las etiquetas. La concordancia entre anotadores requiere un análisis específico de anotaciones comparables.

## Composición de los grupos

La razón entre la clase más frecuente y la menos frecuente es 2,25 en entrenamiento y 3,22 en validación. Existe desequilibrio; las clases no tienen igual representación. El protocolo mantiene entropía cruzada sin ponderación para los tres candidatos, con macro-F1 como criterio de selección y métricas por clase para identificar pérdidas de sensibilidad. Esta elección constituye una condición común del experimento, no una demostración de que el desequilibrio esté resuelto.

La proporción tumoral aumenta 6,09 puntos porcentuales en validación y la estromal disminuye 4,55. Por tanto, la exactitud global depende de una composición distinta en cada grupo. Macro-F1 conserva el mismo peso para las tres categorías, pero no elimina cambios de dominio ni diferencias entre pacientes. Su interpretación debe acompañarse de sensibilidad, precisión y F1 por clase.

## Selección de ventanas interiores

La retención se calcula sobre las anotaciones de cada clase antes de las exclusiones geométricas. En entrenamiento se conserva una proporción menor de linfocitos que de núcleos tumorales: una diferencia descriptiva de 4,34 puntos. La regla espacial modifica así la composición de la muestra. Los resultados posteriores corresponderán a núcleos con una ventana interior elegible, sin generalización automática a núcleos periféricos.

Los intervalos proceden de 5.000 remuestreos de pacientes, con semilla 4101, conservando juntas sus anotaciones. En cada repetición se calcula la razón entre recortes retenidos y anotaciones originales. Son intervalos percentiles, condicionados a los TSS observados; no describen la incertidumbre entre centros ni prueban una diferencia entre clases.

## Contribución de cada paciente

La mediana es de 121 recortes por paciente en entrenamiento, con rango de 7 a 547, y de 79 en validación, con rango de 2 a 231. El conjunto no aporta la misma cantidad de observaciones por paciente. Una métrica calculada sobre todos los recortes otorga mayor influencia a quienes aportan más imágenes. El análisis de incertidumbre por paciente reconoce esa dependencia y complementa la variabilidad entre semillas; ambos componentes responden a preguntas distintas.

## Intensidad y variabilidad de los recortes

Se analizaron los píxeles de los 16.588 recortes de desarrollo, con verificación de dimensiones RGB 128×128 y hashes frente al manifiesto. Las estadísticas de normalización se estimaron exclusivamente en entrenamiento, sobre 238.206.976 píxeles por canal.

| Canal | Media en escala 0–1 | Desviación estándar |
|---|---:|---:|
| Rojo | 0,63920 | 0,21397 |
| Verde | 0,45917 | 0,22150 |
| Azul | 0,62775 | 0,17429 |

La media del canal verde es inferior a las de rojo y azul. La distribución no es equivalente entre canales: una transformación que centre y escale cada uno debe utilizar sus parámetros de entrenamiento. Esta operación no normaliza la tinción ni elimina variación de adquisición. Los valores corresponden a recortes nucleares con contexto; no son mediciones exclusivas del núcleo ni medidas cuantitativas de hematoxilina o eosina.

![Histogramas RGB por clase y partición, normalizados dentro de cada distribución.](figuras/histogramas_pixeles_v2.svg)

Cada curva representa la proporción de píxeles por intervalo dentro de una clase y partición. La normalización permite comparar la forma de las distribuciones sin confundirla con el número de recortes. Los histogramas contienen tanto el núcleo objetivo como su entorno; sus diferencias no pueden atribuirse exclusivamente a morfología celular o a tinción.

## Desplazamiento entre particiones y señal de procedencia

Se construyeron diez descriptores de color y textura por recorte. Para evitar que los pacientes con más imágenes dominaran el diagnóstico, se utilizó la mediana de cada descriptor por paciente. Una regresión logística con pesos balanceados se evaluó en tres pliegues, manteniendo cada paciente en un único grupo y estimando el escalado dentro de entrenamiento. Los hiperparámetros se fijaron antes de la ejecución, sin búsqueda.

| Diagnóstico | Pacientes | Categorías | Exactitud balanceada | AUC |
|---|---:|---:|---:|---:|
| Entrenamiento frente a validación | 104 | 2 | 0,6770 | 0,7097 |
| TSS entre pacientes de entrenamiento | 77 | 8 | 0,3983 | No calculada |

![Matrices de confusión de los diagnósticos, con predicciones fuera del pliegue.](figuras/diagnosticos_pixeles_v2.svg)

La clasificación de partición reconoció 61 de 83 pacientes de entrenamiento y 13 de 21 de validación. Su AUC de 0,7097 describe señal disponible en estos descriptores para distinguir los grupos. No se presenta como prueba confirmatoria: el diagnóstico carece de intervalo de confianza y puede reflejar conjuntamente diferencias de composición celular, tejido, adquisición y procedencia. La separación por TSS evita compartir esos códigos entre grupos, pero no garantiza distribuciones visuales equivalentes.

El diagnóstico de procedencia incluyó únicamente los ocho TSS de entrenamiento con al menos tres pacientes. Su exactitud balanceada de 0,3983 supera descriptivamente la referencia uniforme de 0,125 para ocho categorías. Esto indica que los descriptores contienen señal asociada al TSS; no demuestra que una CNN entrenada para clasificar núcleos utilice esa señal. Tampoco estima rendimiento en TSS nuevos. Se mantiene la separación por paciente y TSS, y se evita interpretar la normalización RGB como solución demostrada a este desplazamiento.

## Similitud perceptual entre entrenamiento y validación

Se compararon 29.790.411 pares de recortes mediante dHash de 64 bits. No se identificaron candidatos con distancia de Hamming menor o igual a cuatro. La comparación fue recalculada de forma independiente a partir de los hashes exportados. El resultado complementa la comprobación de duplicados exactos, pero no descarta todas las rotaciones, cambios de escala, recortes parcialmente solapados ni otras similitudes que este descriptor puede omitir. No se eliminaron imágenes por este análisis.

## Procedencia y alcance de la verificación

El procesamiento de píxeles se ejecutó en el equipo del autor. La segunda verificación contrastó los 16.588 registros con el manifiesto, recalculó medias y desviaciones RGB mediante los descriptores, comprobó los conteos de los histogramas y reconstruyó las matrices de confusión y sus exactitudes balanceadas. La AUC adversarial se conserva tal como la registró el script: el archivo exporta etiquetas predichas, pero no sus probabilidades, por lo que esa AUC no se recalculó de forma independiente. No se recibieron los píxeles en esta segunda revisión.

No se utilizaron imágenes de reserva. Las mediciones de calidad de campos del piloto se conservan en su apartado original y no se atribuyen a los recortes de esta nueva partición.

## Completitud del manifiesto y entropía de clases

Se verificaron los campos paciente, TSS, partición, clase, ruta de archivo y las dos huellas digitales en los 16.588 registros de desarrollo: cada campo presenta **0 valores vacíos (0 %)**. Este resultado describe el manifiesto de recortes seleccionados, no la completitud de todos los metadatos originales de NuCLS. Tampoco demuestra que una etiqueta no vacía sea correcta.

La entropía de las tres clases es **1.5068 bits** en entrenamiento y **1.4302 bits** en validación; normalizada por log₂(3), corresponde a **0.9507** y **0.9024**, respectivamente. El máximo normalizado es uno. La menor entropía de validación confirma una composición más concentrada, coherente con su mayor proporción tumoral. La entropía resume balance; no mide dificultad visual ni independencia entre recortes.
