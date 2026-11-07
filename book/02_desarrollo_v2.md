# Desarrollo v2: composición y retención

La nueva partición contiene 14.539 recortes de entrenamiento, correspondientes a 83 pacientes, y 2.049 de validación, de 21 pacientes. Los pacientes y los códigos TSS son disjuntos entre grupos. Este análisis utiliza metadatos de esas dos particiones y no calcula predicciones ni medidas de rendimiento sobre la reserva.

![Composición por clase, retención e imágenes aportadas por paciente.](figuras/eda_desarrollo_v2.svg)

## Composición de los grupos

| Clase | Entrenamiento | Proporción | Validación | Proporción |
|---|---:|---:|---:|---:|
| Tumoral no mitótica | 6.977 | 47,99% | 1.108 | 54,08% |
| Linfocito | 4.460 | 30,68% | 597 | 29,14% |
| Estromal | 3.102 | 21,34% | 344 | 16,79% |

La proporción tumoral aumenta 6,09 puntos porcentuales en validación y la estromal disminuye 4,55. Por tanto, la exactitud global depende de una composición distinta en cada grupo. Macro-F1 conserva el mismo peso para las tres categorías, pero no elimina cambios de dominio ni diferencias entre pacientes. Su interpretación debe acompañarse de sensibilidad, precisión y F1 por clase.

## Selección de ventanas interiores

| Clase | Retención en entrenamiento | IC95% por paciente | Retención en validación | IC95% por paciente |
|---|---:|---:|---:|---:|
| Tumoral no mitótica | 49,18% | 47,64–50,51% | 47,35% | 43,15–51,83% |
| Linfocito | 44,84% | 43,44–46,29% | 44,99% | 38,72–49,80% |
| Estromal | 46,94% | 44,98–48,87% | 48,45% | 43,83–53,03% |

La retención se calcula sobre las anotaciones de cada clase antes de las exclusiones geométricas. En entrenamiento se conserva una proporción menor de linfocitos que de núcleos tumorales: una diferencia descriptiva de 4,34 puntos. La regla espacial modifica así la composición de la muestra. Los resultados posteriores corresponderán a núcleos con una ventana interior elegible, sin generalización automática a núcleos periféricos.

Los intervalos proceden de 5.000 remuestreos de pacientes, con semilla 4101, conservando juntas sus anotaciones. En cada repetición se calcula la razón entre recortes retenidos y anotaciones originales. Son intervalos percentiles, condicionados a los TSS observados; no describen la incertidumbre entre centros ni prueban una diferencia entre clases.

## Contribución de cada paciente

La mediana es de 121 recortes por paciente en entrenamiento, con rango de 7 a 547, y de 79 en validación, con rango de 2 a 231. El conjunto no aporta la misma cantidad de observaciones por paciente. Una métrica calculada sobre todos los recortes otorga mayor influencia a quienes aportan más imágenes. El análisis de incertidumbre por paciente reconoce esa dependencia y complementa la variabilidad entre semillas; ambos componentes responden a preguntas distintas.

## Alcance del análisis

Estas mediciones describen etiquetas, selección y agrupamiento. No miden color, desenfoque, normalización de tinción ni similitud perceptual de los nuevos recortes. Las estadísticas de campos del piloto se presentan por separado y no se atribuyen a esta partición. El notebook de desarrollo v2 reproduce las tablas a partir de las salidas verificadas del script `scripts/eda_particion_v2.py`.
