# Control de recortes de la partición v2

El procesamiento local produjo 17.557 recortes RGB de 128 × 128 píxeles a partir de 1.484 campos correspondientes a 110 pacientes. El manifiesto se contrastó con la partición publicada, las coordenadas, los hashes de origen y el registro de exclusiones.

| Partición | Pacientes | Tumorales | Linfocitos | Estromales | Total |
|---|---:|---:|---:|---:|---:|
| Entrenamiento | 83 | 6.977 | 4.460 | 3.102 | 14.539 |
| Validación | 21 | 1.108 | 597 | 344 | 2.049 |
| Reserva candidata | 6 | 769 | 130 | 70 | 969 |

No se encontraron pacientes ni códigos TSS compartidos entre estas tres particiones. Los hashes de píxeles registrados en el manifiesto fueron únicos. Esta comprobación descarta duplicados exactos registrados, pero no imágenes casi idénticas ni solapamientos parciales.

## Retención y alcance de la población evaluada

De las 36.474 anotaciones pertenecientes a las tres clases objetivo, se conservaron 17.557 (48,14%). Se excluyeron 18.299 por requerir relleno para construir una ventana interior, 523 por cajas fuera de la imagen, 86 por cajas inválidas y nueve por no quedar completamente contenidas en la ventana. Otras 13.342 anotaciones pertenecían a clases fuera del objetivo y no integran el denominador de retención.

La selección descarta principalmente núcleos próximos a los bordes. En consecuencia, el desempeño posterior describirá la clasificación de núcleos con una ventana interior elegible; no describirá la clasificación de todos los núcleos de un campo. Los 128 píxeles se conservaron en escala nativa, sin acreditar una extensión física homogénea entre imágenes.

La reserva contiene solo seis pacientes y predominan los núcleos tumorales. La cantidad de recortes no debe interpretarse como igual número de observaciones independientes. La incertidumbre y la presentación de resultados deben reconocer el agrupamiento por paciente y las diferencias de composición entre grupos.

## Procedencia de la comprobación

La lectura completa de imágenes y la generación de hashes se ejecutaron en el equipo del autor. El ZIP de control contiene metadatos y fue revisado de forma independiente: se recalcularon conteos, coordenadas, pertenencia a grupos y exclusiones. Las imágenes no se adjuntaron, por lo que su decodificación no se repitió en esta segunda revisión.

El resultado permite continuar la preparación del experimento. No acredita rendimiento predictivo ni reemplaza el cierre de arquitecturas, búsqueda de hiperparámetros y análisis estadístico previo a la evaluación de la reserva. Las quince corridas anteriores mantienen su condición de piloto con una partición distinta.

La evidencia verificable se conserva en `evidencias/control_recortes_v2.json`, incluyendo hashes del ZIP, manifiesto, partición y tablas de control.
