# Discusión del diseño y alcance V2

<!-- PRESENTACION_CAPITULO -->
<div class="chapter-deck"><p class="book-eyebrow">06 / DISCUSIÓN</p><p>Interpretar los hallazgos dentro de su alcance</p><div class="chapter-tags"><span>Literatura + EDA + experimento</span><span>Sin validación clínica</span><span>Limitaciones explícitas</span></div></div>

<div class="chapter-takeaway"><b>La evidencia no sostiene una superioridad universal.</b> Los resultados corresponden a esta partición, taxonomía y protocolo. Seis pacientes de reserva, cobertura bibliográfica incompleta y tareas pendientes limitan la conclusión.</div>
<!-- FIN_PRESENTACION_CAPITULO -->

## Coherencia entre evidencia y comparación

El experimento V2 compara CNN compacta con BatchNorm, DenseNet121 y ResNet50. Los resultados de CNN local, ResNet18 y MobileNetV2 pertenecen a una partición y un experimento anteriores; se conservan en los anexos históricos y no determinan el baseline V2. El cierre de entrega contiene once semillas por modelo y 33 evaluaciones de reserva verificadas. ResNet50 se seleccionó por validación (macro-F1 medio 0,7934) y obtuvo 0,6378 en reserva, frente a 0,6052 de DenseNet121 y0,4542 de la compacta. No se atribuyen métricas del piloto a las arquitecturas nuevas.

## Consecuencias del EDA

El desarrollo reúne 16.588 recortes de 104 pacientes. La separación por paciente y TSS reduce el solapamiento de procedencia entre particiones. El diagnóstico de dominio muestra que los descriptores de imagen distinguen parcialmente entrenamiento y validación; por tanto, separar los identificadores no vuelve idénticas sus distribuciones. El análisis no establece si esa diferencia procede de tinción, adquisición o composición celular.

La clase estromal tiene menor representación en el desarrollo. Macro-F1 evita que la clase tumoral domine por frecuencia el promedio de F1, aunque no corrige el desbalance durante el ajuste ni garantiza una sensibilidad estromal adecuada. La interpretación exige resultados por clase y por paciente, además del promedio global.

## Reserva y precisión de la evaluación

La reserva V2 comprende seis pacientes y 969 recortes: 769 tumorales, 130 linfocitarios y 70 estromales, según el control del manifiesto. Es una limitación sustancial de tamaño efectivo y cobertura de clases. Las predicciones exportadas confirman que 42 de los 70 recortes estromales proceden de un paciente. El F1 estromal medio de ResNet50 es 0,3022; una media global superior no resuelve esta debilidad. La tabla de anotaciones originales no sustituye el inventario de recortes elegibles.

La agrupación por paciente evita tratar 969 recortes como pacientes independientes, pero seis grupos proporcionan una estimación frágil de la variabilidad poblacional. Las semillas describen variación algorítmica y no compensan esta limitación. Los resultados por TSS tendrán carácter descriptivo y no acreditarán generalización a centros nuevos.

## Anotaciones y referencia humana

La integridad técnica y la ausencia de faltantes no prueban exactitud de las etiquetas. La concordancia del subconjunto multi-rater requiere emparejar anotaciones del mismo núcleo, conservar identidad del evaluador y distinguir etiquetas individuales de consenso. Su resultado describe acuerdo bajo ese protocolo; no es automáticamente un techo de desempeño ni equivale a la exactitud de un experto frente a una verdad biológica independiente.

## Alcance de las conclusiones

La selección bibliográfica sustenta la pertinencia de las tres referencias, pero no demuestra que sean la tríada más frecuente y sencilla de todo el corpus. Esta restricción permanece explícita. La comparación local ya establece medias y dispersión entre semillas; el costo de inferencia controlado permanece pendiente. La caída de 0,1556 en ResNet50 es compatible con problemas de generalización, pero no identifica por sí sola su causa. El diagnóstico previo de dominio, el desbalance y la concentración de clases justifican examinar heterogeneidad, sin atribuir causalidad.

El objeto del estudio es clasificar núcleos previamente localizados, no detectar células en láminas completas ni establecer diagnósticos clínicos. Las conclusiones cuantitativas V2 se vincularán exclusivamente a sus predicciones y checkpoints. La [discusión del piloto histórico](anexo_discusion_piloto.md) conserva su propio alcance.

## Enmienda del número de semillas

El plan exigía 22 semillas y se cerró la entrega con las primeras 11 por restricción temporal. Se conserva esta desviación y la enmienda previa a reserva; no se afirma haber cumplido la potencia planificada. La incertidumbre exploratoria por paciente es amplia y se condiciona a los modelos ya ajustados. La extensión posterior no autoriza seleccionar modelos o hiperparámetros a partir de la reserva ya examinada.
