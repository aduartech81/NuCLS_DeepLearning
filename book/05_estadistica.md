# Variabilidad, comparación y tamaño del experimento

**MobileNetV2 presenta la mayor media, pero el piloto no demuestra una ventaja concluyente frente a ResNet18.** Las quince corridas permiten cuantificar la variación por semilla y planificar un experimento posterior. Los análisis de este capítulo son exploratorios: se realizaron después de observar la validación.

```{figure} figuras/visual_planificacion.svg
:name: fig-planificacion

Izquierda: cinco semillas por modelo; la barra resume media ± desviación estándar muestral. Derecha: diferencia mínima detectable con cinco pares, potencia 80% y ajuste Bonferroni para tres comparaciones, bajo un modelo t pareado normal. La línea marca el margen práctico preliminar de dos puntos porcentuales.
```

## ¿Cuánto cambia el resultado entre semillas?

| Modelo | Corridas | Macro-F1 medio | Desviación estándar | CV |
|---|---:|---:|---:|---:|
| CNN local | 5 | 0,7203 | 0,01059 | 1,47% |
| ResNet18 | 5 | 0,8191 | 0,01058 | 1,29% |
| MobileNetV2 | 5 | 0,8239 | 0,00780 | 0,95% |

El coeficiente de variación es $CV=100s/\bar x$. MobileNetV2 tiene menor dispersión relativa en estas cinco corridas. Esto describe estabilidad de entrenamiento en **una partición fija**; no mide generalización a hospitales o pacientes nuevos. No se descartan semillas por resultados desfavorables.

## Comparación pareada exploratoria

Cada pareja comparte partición y número de semilla. Se analiza una diferencia de macro-F1 por semilla, sin convertir cada recorte en una repetición independiente. Compartir semilla no garantiza idénticas inicializaciones ni idéntica secuencia de aumentación entre arquitecturas; el emparejamiento es por identificador de corrida.

| Comparación (primero menos segundo) | Diferencia media | DE de diferencias | p exacta Wilcoxon | p ajustada Holm |
|---|---:|---:|---:|---:|
| ResNet18 − CNN local | +0,09871 | 0,01494 | 0,0625 | 0,1875 |
| MobileNetV2 − CNN local | +0,10359 | 0,01783 | 0,0625 | 0,1875 |
| MobileNetV2 − ResNet18 | +0,00488 | 0,01232 | 0,6250 | 0,6250 |

El contraste bilateral de rangos con signo supone diferencias independientes entre corridas y una distribución simétrica bajo la hipótesis nula. Se verificó ausencia de ceros y empates en valores absolutos; se utilizó el cálculo exacto. Con cinco pares, la menor p bilateral posible es $2/2^5=0,0625$. **La falta de significación no implica igualdad de modelos**; el diseño tiene una resolución limitada. No se usó una prueba de normalidad con cinco observaciones para declarar demostrado un supuesto.

La familia comprende las tres comparaciones, corregidas con Holm. Estos resultados se refieren a variación por entrenamiento condicionada al conjunto de validación, no a inferencia poblacional por paciente. Además, la selección del mejor checkpoint en esa misma validación introduce optimismo.

## Estimación del número de repeticiones

Se adopta provisionalmente $\delta=0,02$ de macro-F1, $\alpha=0,05$ bilateral y potencia $1-\beta=0,80$. El margen representa una referencia de relevancia práctica utilizada en el análisis exploratorio; no corresponde al efecto observado ni a un umbral clínico validado.

Para diferencias pareadas con desviación $s_d$, la aproximación normal es:

$$R \approx \left\lceil\frac{(z_{1-\alpha/2}+z_{1-\beta})^2s_d^2}{\delta^2}\right\rceil.$$

Se compara esa aproximación con potencia t no central, que contempla estimar la varianza con pocas repeticiones. Para planificar conservadoramente la familia de tres contrastes se usa $\alpha/3$; el análisis posterior puede emplear Holm. **La planificación t no es un cálculo de potencia de Wilcoxon.**

| Comparación | $\delta/s_d$ | R normal sin ajuste | R normal con Bonferroni | R t con Bonferroni |
|---|---:|---:|---:|---:|
| ResNet18 − CNN local | 1,339 | 5 | 6 | 9 |
| MobileNetV2 − CNN local | 1,122 | 7 | 9 | 12 |
| MobileNetV2 − ResNet18 | 1,623 | 3 | 4 | 8 |

Los valores normales son resultados de la fórmula, no autorizan bajar del mínimo de cinco corridas; para pruebas de rangos se requiere como mínimo seis y, aun así, no se garantiza potencia. Bajo los supuestos t y la varianza puntual del piloto, **12 corridas por modelo** cubren la mayor necesidad de las tres parejas. Esta estimación depende de los supuestos de distribución y de la precisión de la varianza del piloto.

### Sensibilidad a la incertidumbre de la varianza

Cinco diferencias proporcionan una estimación imprecisa de $s_d$. Como análisis conservador, bajo normalidad se reemplaza por su límite superior unilateral de confianza 95%:

$$s_{d,\mathrm{sup}}=s_d\sqrt{\frac{R-1}{\chi^2_{0,05;R-1}}}.$$

La planificación t con ajuste asciende entonces a **36, 50 y 26 pares**, respectivamente. Esta amplitud aconseja no presentar 12 como garantía. Los tamaños calculados no cuantifican la potencia de una prueba de rangos; su extrapolación a Wilcoxon no está justificada. El límite de varianza es por comparación, no simultáneo para las tres.

## ¿Qué diferencias puede detectar el piloto actual?

Para cinco pares, la aproximación normal sin ajuste produce MDE de 1,87; 2,23 y 1,54 puntos porcentuales. Al incorporar t y Bonferroni, las MDE aumentan a **3,42; 4,09 y 2,82 puntos**, respectivamente. Todas exceden el margen práctico de dos puntos. Estas cifras asumen normalidad y la varianza estimada; no representan potencia observada ni corrigen el sesgo de selección de checkpoints.

La diferencia observada MobileNetV2–ResNet18 es apenas **0,49 puntos**. El bootstrap por paciente, que aborda otra fuente de incertidumbre, estima para esa diferencia un intervalo marginal de **−1,08 a +2,01 puntos**. No hay evidencia suficiente para declarar superioridad ni equivalencia. Sus intervalos son exploratorios y no están ajustados por las tres comparaciones.

## Alcance inferencial

La planificación se calculó después de observar los resultados y constituye una estimación exploratoria para dimensionar experimentos, no un prerregistro. La selección de épocas y la comparación de modelos utilizaron la validación; por ello, las cifras no sustentan inferencia confirmatoria sobre una población externa.

Las semillas evalúan aleatoriedad del entrenamiento. Los pacientes son la unidad de generalización: el remuestreo por paciente mantiene juntos sus recortes. Ningún aumento del número de semillas sustituye una evaluación independiente por paciente o centro.

## Reproducibilidad

El script `scripts/planificar_piloto.py` lee las quince corridas verificadas, comprueba el emparejamiento, calcula tablas y genera la figura sin entrenar modelos. Los archivos `resultados_analizados/variabilidad_semillas.csv` y `planificacion_semillas.csv` contienen los valores sin redondear.

Referencia de implementación: [SciPy, Wilcoxon](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html), [distribución t no central](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.nct.html). La fórmula de planificación corresponde a una comparación pareada bilateral con diferencias normales.
