# Datos, unidades y separación por paciente

## Del archivo al experimento

Los conteos tienen unidades distintas. Un archivo puede ser una imagen, una tabla o una anotación; un campo contiene varios núcleos, y varios campos pueden proceder del mismo paciente. Por eso no se interpreta el número de archivos como tamaño muestral independiente.

| Nivel | Cantidad documentada | Significado |
|---|---:|---|
| Inventario local | 30.540 archivos examinados | Inventario comunicado por el autor; incluye distintos tipos de archivo. |
| Subconjunto QC | 1.744 imágenes RGB | Conteo que coincide con la referencia usada por la auditoría. |
| Campos para EDA | 1.182 | Imágenes de los 79 pacientes de entrenamiento auditadas cuantitativamente. |
| Recortes de entrenamiento | 14.428 | Ventanas RGB seleccionadas para el piloto. |
| Recortes de validación | 3.571 | Ventanas usadas para seleccionar época y describir desempeño. |
| Pacientes del piloto | 98 | 79 de entrenamiento y 19 de validación, sin cruce entre ambos grupos. |

El conjunto noQC contó 2.200 imágenes RGB y presentó discrepancia con el conteo de referencia. Los conjuntos multi-rater contienen anotaciones relacionadas y no se suman automáticamente como imágenes o pacientes independientes. El piloto se limita a la selección documentada de QC.

## Etiquetas operativas

| Etiqueta del archivo | Nombre en las figuras | Alcance |
|---|---|---|
| `tumor_nonMitotic` | Tumoral | Núcleo tumoral no mitótico anotado. |
| `lymphocyte` | Linfocito | Categoría linfocitaria anotada. |
| `nonTILnonMQ_stromal` | Estromal | Categoría estromal de la selección; no identifica telocitos. |

Se conserva trazabilidad **recorte → anotación → campo → paciente → partición**. La supervisión procede de etiquetas publicadas; estas no se han revalidado individualmente para este proyecto.

## Qué datos responden cada pregunta

- **Entrenamiento:** EDA, diagnóstico de calidad y ajuste de parámetros. Los aumentos se aplican solo aquí.
- **Validación:** selección de la mejor época y comparación exploratoria de las corridas.
- **Prueba independiente:** no se reporta un resultado confirmatorio. La prueba histórica ya expuesta no se considera virgen.

Las cinco semillas generan cinco entrenamientos sobre la misma partición; no multiplican por cinco el número de pacientes. El remuestreo por paciente utilizado en los resultados reconoce la dependencia de los recortes de un mismo sujeto.

## Auditoría y preprocesamiento

El [EDA](02_resultados_eda.md) cuantifica balance, retención, geometría y calidad de los campos. La [galería](02_galeria.md) muestra ejemplos reales y el tratamiento de imagen aplicado. No se presupone que más filtros produzcan mejores predicciones; una modificación de tinción o contraste requiere evaluación bajo un protocolo definido.

Los hashes de las evidencias están en `evidencias/procedencia.json`. El inventario y los hashes facilitan la reproducibilidad, pero no sustituyen la verificación de licencia, versión, calidad de etiquetas o representatividad. La documentación de procedencia y permisos debe completarse antes de redistribuir el conjunto íntegro.
