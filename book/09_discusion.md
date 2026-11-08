# Discusión del diseño y alcance V2

## Coherencia entre evidencia y comparación

El experimento V2 compara CNN compacta con BatchNorm, DenseNet121 y ResNet50. Los resultados de CNN local, ResNet18 y MobileNetV2 pertenecen a una partición y un experimento anteriores; se conservan en los anexos históricos y no determinan el baseline V2. La ejecución comunicada de Colab ha alcanzado las corridas finales, pero el repositorio aún no contiene sus resultados finales verificables. No se atribuyen métricas del piloto a las arquitecturas nuevas.

## Consecuencias del EDA

El desarrollo reúne 16.588 recortes de 104 pacientes. La separación por paciente y TSS reduce el solapamiento de procedencia entre particiones. El diagnóstico de dominio muestra que los descriptores de imagen distinguen parcialmente entrenamiento y validación; por tanto, separar los identificadores no vuelve idénticas sus distribuciones. El análisis no establece si esa diferencia procede de tinción, adquisición o composición celular.

La clase estromal tiene menor representación en el desarrollo. Macro-F1 evita que la clase tumoral domine por frecuencia el promedio de F1, aunque no corrige el desbalance durante el ajuste ni garantiza una sensibilidad estromal adecuada. La interpretación exige resultados por clase y por paciente, además del promedio global.

## Reserva y precisión de la evaluación

La reserva V2 comprende seis pacientes y 969 recortes: 769 tumorales, 130 linfocitarios y 70 estromales, según el control del manifiesto. Es una limitación sustancial de tamaño efectivo y cobertura de clases. La auditoría docente señala que 42 de los 70 recortes estromales proceden de un paciente; esa concentración debe contrastarse con el manifiesto final antes de incorporarla como conteo verificado. La tabla de anotaciones originales no sustituye el inventario de recortes elegibles.

La agrupación por paciente evita tratar 969 recortes como pacientes independientes, pero seis grupos proporcionan una estimación frágil de la variabilidad poblacional. Las semillas describen variación algorítmica y no compensan esta limitación. Los resultados por TSS tendrán carácter descriptivo y no acreditarán generalización a centros nuevos.

## Anotaciones y referencia humana

La integridad técnica y la ausencia de faltantes no prueban exactitud de las etiquetas. La concordancia del subconjunto multi-rater requiere emparejar anotaciones del mismo núcleo, conservar identidad del evaluador y distinguir etiquetas individuales de consenso. Su resultado describe acuerdo bajo ese protocolo; no es automáticamente un techo de desempeño ni equivale a la exactitud de un experto frente a una verdad biológica independiente.

## Alcance de las conclusiones

La selección bibliográfica sustenta la pertinencia de las tres referencias, pero no demuestra que sean la tríada más frecuente y sencilla de todo el corpus. Esta restricción permanece explícita. La comparación local deberá establecer desempeño, variabilidad y costo sin inferir superioridad a partir de profundidad o número de parámetros.

El objeto del estudio es clasificar núcleos previamente localizados, no detectar células en láminas completas ni establecer diagnósticos clínicos. Las conclusiones cuantitativas V2 se vincularán exclusivamente a sus predicciones y checkpoints. La [discusión del piloto histórico](anexo_discusion_piloto.md) conserva su propio alcance.
