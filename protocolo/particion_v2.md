# Diseño de partición para el siguiente experimento

La clasificación comprende núcleos tumorales no mitóticos, linfocitos y núcleos estromales. Las quince ejecuciones existentes corresponden al piloto y no constituyen una evaluación confirmatoria de este diseño.

## Separación de las observaciones

La asignación agrupa pacientes por código de procedencia TCGA (TSS). Este código se emplea como agrupador de origen; no acredita por sí mismo un protocolo homogéneo de adquisición. Se excluyen del nuevo entrenamiento los pacientes que comparten TSS con la reserva candidata.

| Función | Pacientes | TSS |
|---|---:|---|
| Entrenamiento | 83 | A1, A2, AC, AR, C8, D8, E2, EW, GI, GM, LL, S3 |
| Validación | 21 | AQ, BH, OL |
| Reserva candidata | 6 | A7, AN, AO |
| Excluidos por procedencia de la reserva | 14 | A7, AN, AO |

La validación se asignó buscando el 20% de los pacientes de desarrollo, con al menos dos TSS y desempate determinista por SHA256. El algoritmo no consultó imágenes, etiquetas ni resultados de modelos. Después de la asignación se comprobó la presencia de las tres clases en los inventarios de entrenamiento y validación. Estos conteos corresponden a anotaciones, no a recortes definitivos.

## Antecedentes de exposición

El test histórico fue evaluado en notebooks anteriores. Por tanto, no se presenta como una prueba intacta. Los seis pacientes de la reserva candidata no aparecen en los manifiestos históricos y del piloto examinados; esta comprobación documental no demuestra ausencia de cualquier acceso previo fuera de esos registros. La nueva separación tampoco elimina el conocimiento adquirido durante los experimentos anteriores.

El control local identificó 24 campos de los seis pacientes, sin errores reportados de lectura de encabezados o tablas. Se identificaron 969 ventanas geométricamente posibles de 128 × 128 píxeles: 769 tumorales, 130 linfocitarias y 70 estromales. No se ejecutaron modelos sobre ellas. La comprobación no incluyó decodificación completa de píxeles ni validación biológica de las anotaciones.

## Reglas para la preparación y evaluación

1. La construcción de recortes debe generar coordenadas, clase, paciente, TSS, origen y hash de cada archivo. Debe verificar dimensiones y decodificación completa. Los recortes de una imagen y un paciente conservan su partición.
2. La regla geométrica debe ser idéntica en todas las particiones. Las exclusiones deben conservarse con su motivo. No se cambiará el tamaño ni la regla de selección para mejorar resultados observados en la reserva.
3. La estimación de normalización, ponderación de clases o parámetros de preprocesamiento utilizará exclusivamente entrenamiento. Los aumentos aleatorios se aplicarán solamente a entrenamiento.
4. La validación se utilizará para selección de hiperparámetros y checkpoints. La reserva candidata quedará fuera de esos procesos. No se inspeccionarán sus errores para ajustar modelos.
5. Antes de evaluar la reserva se registrarán arquitecturas, presupuesto de búsqueda, semillas, criterio de checkpoint, métrica primaria y análisis estadístico. Esta versión documenta la partición y no representa un protocolo completo prerregistrado.
6. La incertidumbre debe considerar el agrupamiento por paciente. Los 969 candidatos no son observaciones independientes; seis pacientes y tres TSS limitan la precisión y la generalización de una evaluación final. La variabilidad entre semillas no sustituye la variabilidad entre pacientes.

## Reproducción

Desde la raíz del repositorio:

```bash
python scripts/particionar_desarrollo.py --entrada evidencias/particion_candidata_por_sitio.csv --salida configs
```

La ejecución reproduce `configs/particion_por_tss_v2.csv` y su hash. Rechaza pacientes duplicados y una sobrescritura con asignación diferente. Los controles y las fuentes se conservan en `configs/control_particion_v2.json`, `configs/control_clases_v2.json` y `evidencias/control_reserva_local.json`.

La asignación queda versionada para preparar los datos. La integridad completa de los recortes y el protocolo de modelos deben verificarse antes del siguiente entrenamiento.
