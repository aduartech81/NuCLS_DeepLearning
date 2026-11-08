# Clasificación nuclear con aprendizaje profundo

**Andrés Duarte Chaves · Maestría en Ingeniería Biomédica · Entregable 1**

El experimento V2 compara una CNN compacta con BatchNorm, DenseNet121 y ResNet50 para clasificar núcleos tumorales no mitóticos, linfocitarios y estromales en recortes RGB de NuCLS. El diseño estudia desempeño, variabilidad y costo bajo una partición común por paciente y procedencia.

<div class="nucls-grid">
<div class="nucls-card"><strong>14.539</strong><span>recortes de entrenamiento · 83 pacientes</span></div>
<div class="nucls-card"><strong>2.049</strong><span>recortes de validación · 21 pacientes</span></div>
<div class="nucls-card"><strong>969</strong><span>recortes de reserva · 6 pacientes</span></div>
</div>

## Datos y representación

![Composición del desarrollo V2.](figuras/eda_desarrollo_v2.svg)

La unidad de predicción es un núcleo previamente localizado en una ventana de 128×128 píxeles. Los recortes de un mismo paciente están correlacionados. La reserva tiene solo 70 recortes estromales y seis pacientes; su tamaño limita la precisión de la evaluación.

## Organización

- [EDA V2](02_desarrollo_v2.md): integridad, balance, intensidad, similitud y desplazamiento.
- [Estado del arte](03_literatura.md): síntesis crítica y fundamento de las referencias.
- [Metodología](04_metodologia_v2.md): arquitecturas, parámetros y entrenamiento.
- [Comparación estadística](05_estadistica.md): unidades de análisis e incertidumbre.
- [Experimento V2](08_resultados_v2.md): estado verificable de la evidencia.
- [Discusión](09_discusion.md): interpretación del diseño y límites.
- [Notebook EDA ejecutado](10_eda_v2.ipynb): cálculos y salidas reproducibles.

La ejecución V2 está en curso según los registros comunicados por el autor. Los resultados finales no están incorporados en esta versión. Los resultados de CNN local, ResNet18 y MobileNetV2 se conservan como anexos históricos y no sustituyen la comparación V2. El estudio aborda clasificación de recortes, no detección en láminas completas ni uso clínico.
