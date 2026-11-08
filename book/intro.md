# NuCLS · Evidencia, datos y modelos

<div class="book-hero">
<div class="book-hero-copy">
<p class="book-eyebrow">INGENIERÍA BIOMÉDICA / DEEP LEARNING</p>
<h2>De la morfología nuclear<br><em>a la evidencia experimental.</em></h2>
<p class="book-lead">Clasificación de núcleos tumorales, linfocitarios y estromales. Una comparación de tres modelos base conectada con la literatura, la calidad de los datos y la evaluación por paciente.</p>
<p class="book-byline">Andrés Duarte Chaves · Entregable 1 · 8 de noviembre de 2026</p>
<div class="book-actions"><a class="book-button" href="08_resultados_v2.html">Explorar los resultados →</a><a class="book-button secondary" href="https://nucls-andres-duarte.onrender.com/">Dashboard interactivo ↗</a></div>
</div>
<div class="book-atlas">
<figure><img src="_static/galeria/tumor_nonMitotic_00.png" alt="Ejemplo anotado de núcleo tumoral de entrenamiento"><figcaption>Tumoral</figcaption></figure>
<figure><img src="_static/galeria/lymphocyte_02.png" alt="Ejemplo anotado de linfocito de entrenamiento"><figcaption>Linfocito</figcaption></figure>
<figure><img src="_static/galeria/nonTILnonMQ_stromal_01.png" alt="Ejemplo anotado de núcleo estromal de entrenamiento"><figcaption>Estromal</figcaption></figure>
<p>H&E · RGB 128 × 128<br>Ejemplos ilustrativos de entrenamiento, no predicciones.</p>
</div>
</div>

<div class="book-metrics">
<div><span>DESARROLLO</span><strong>16.588</strong><small>104 pacientes · entrenamiento y validación</small></div>
<div><span>RESERVA</span><strong>969</strong><small>6 pacientes · evaluación final</small></div>
<div><span>EXPERIMENTO</span><strong>33</strong><small>11 semillas por cada uno de los 3 modelos</small></div>
<div><span>LITERATURA</span><strong>166</strong><small>informes con lectura dirigida documentada</small></div>
</div>

## Tres recorridos para evaluar el proyecto

<div class="book-route-grid">
<a class="book-route" href="03_literatura.html"><span class="book-route-number">01 / ESTADO DEL ARTE</span><h3>De la búsqueda al diseño</h3><p>Síntesis crítica, comparadores exactos, diferencias de tarea y flujo documental adaptado de PRISMA.</p><strong>1.330 registros cribados · 21 informes focales</strong><span class="route-cta">Leer la evidencia →</span></a>
<a class="book-route" href="02_desarrollo_v2.html"><span class="book-route-number">02 / ANÁLISIS EXPLORATORIO</span><h3>Entender la muestra</h3><p>Integridad, balance, selección espacial, similitud entre recortes, heterogeneidad y desplazamiento.</p><strong>83 pacientes de entrenamiento · 21 de validación</strong><span class="route-cta">Explorar el EDA →</span></a>
<a class="book-route" href="04_metodologia_v2.html"><span class="book-route-number">03 / IMPLEMENTACIÓN</span><h3>Comparar en condiciones comunes</h3><p>CNN compacta con BN, DenseNet121 y ResNet50; arquitectura, entrenamiento, selección y reproducibilidad.</p><strong>Inicialización desde cero · entrada RGB común</strong><span class="route-cta">Examinar los modelos →</span></a>
</div>

## Resultado principal: el reto de generalizar

ResNet50 obtuvo el mayor macro-F1 medio en validación y fue seleccionado antes de evaluar la reserva. El cierre incorpora **11 semillas por modelo**, las predicciones de reserva y un análisis exploratorio agrupado por paciente.

![Macro-F1 medio de validación y reserva de los tres modelos, calculado sobre once semillas por modelo.](figuras/resumen_modelos_portada.svg)

<div class="book-insights">
<div><span class="book-eyebrow">DESEMPEÑO EN RESERVA</span><h3>0,638 · ResNet50</h3><p>Frente a 0,605 de DenseNet121 y 0,454 de la CNN compacta. Son medias del mismo experimento local; no una clasificación universal de arquitecturas.</p></div>
<div><span class="book-eyebrow">CLASE MÁS DIFÍCIL</span><h3>0,302 · F1 estromal</h3><p>La reserva contiene 70 recortes estromales y 42 pertenecen a un solo paciente. El promedio global no elimina esta fragilidad.</p></div>
</div>

Los [resultados completos](08_resultados_v2.md) distinguen variación entre semillas de incertidumbre entre pacientes. Los intervalos agrupados son exploratorios y condicionados a los ajustes disponibles. La [discusión](09_discusion.md) relaciona estos resultados con la evidencia bibliográfica y el EDA.

## Un protocolo que conserva la trazabilidad

<div class="book-process">
<div><b>1</b><h3>Definir la tarea</h3><p>Clasificar un núcleo ya localizado, con tres categorías y ventanas interiores elegibles.</p></div>
<div><b>2</b><h3>Separar pacientes</h3><p>Desarrollo: 14.539 recortes de entrenamiento y 2.049 de validación. Reserva separada.</p></div>
<div><b>3</b><h3>Seleccionar con validación</h3><p>Mismo protocolo local y búsqueda documentada. ResNet50 seleccionado antes de la reserva.</p></div>
<div><b>4</b><h3>Evaluar y declarar límites</h3><p>Resultados por clase, semillas y pacientes, con las restricciones del cierre académico.</p></div>
</div>

<div class="book-scope"><strong>Alcance del cierre de entrega</strong><p>13 informes no recuperados al corte y un duplicado tardío documentado. Revisión crítica dirigida, sin segundo revisor independiente; no revisión sistemática exhaustiva. El experimento se cierra con 11 de las 22 semillas previstas por modelo. Concordancia entre anotadores, Grad-CAM y latencia controlada permanecen pendientes.</p></div>

## Evidencia para profundizar

- [Notebook EDA ejecutado](10_eda_v2.ipynb): cálculos y salidas del análisis exploratorio.
- [Galería de entrenamiento](02_galeria.md): representación de entrada y etiquetas ilustrativas.
- [Comparación estadística](05_estadistica.md): unidades de análisis, selección e incertidumbre.
- [Repositorio de código y evidencias](https://github.com/aduartech81/NuCLS_DeepLearning): implementaciones, matrices bibliográficas y resultados derivados.
- [Dashboard interactivo](https://nucls-andres-duarte.onrender.com/): exploración de métricas, clases y artículos.

Los anexos históricos conservan el piloto anterior de CNN local, ResNet18 y MobileNetV2. No sustituyen la comparación V2 ni se mezclan con sus resultados. Este proyecto estudia clasificación de recortes previamente localizados; no valida detección en láminas completas ni uso clínico.
