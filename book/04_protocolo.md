# Implementación y protocolo exploratorio

Se evaluaron una CNN local, ResNet18 y MobileNetV2. Las tres implementaciones representan distintas configuraciones de capacidad y procesamiento convolucional. La selección responde al diseño exploratorio del piloto; la revisión bibliográfica no establece que sean las tres arquitecturas exactas más frecuentes para clasificación nuclear. Las referencias a familias de modelos o a extractores de características de segmentación no se consideran evidencia equivalente.

La CNN local tiene tres convoluciones 3×3 de 32, 64 y 128 canales, ReLU, dos max-pooling, promedio global, dropout 0,3 y salida lineal de tres clases. ResNet18 y MobileNetV2 usan implementaciones de torchvision, sin pesos preentrenados y con salida adaptada a tres clases. La CNN local es una implementación propia; no se presenta como réplica de una arquitectura publicada.

| Condición | Piloto implementado |
|---|---|
| Semillas | 4101, 4102, 4103, 4104, 4105 |
| Entrenamiento | Desde cero para los tres candidatos |
| Optimizador | Adam, learning rate 0,001 |
| Batch | 32 |
| Pérdida | Entropía cruzada no ponderada |
| Límite de gradiente | Norma 5 |
| Presupuesto | Máximo 25 épocas, mínimo 5, paciencia 5 |
| Mejor época | Mayor macro-F1 de validación; primer máximo en empate |
| Resultados | Curvas, predicciones, métricas, tiempos y configuración |

Se completaron quince corridas: cinco semillas por cada una de las tres arquitecturas. Las predicciones y las métricas se verificaron; el capítulo de resultados presenta los promedios y sus límites.

La parada temprana produjo presupuestos efectivos diferentes: 11–15 épocas para la CNN local, 8–20 para ResNet18 y 10–24 para MobileNetV2. Las corridas se registraron en macOS 26.4, arquitectura arm64 y dispositivo MPS, con Python 3.11.18, PyTorch 2.15.0 y torchvision 0.29.2. Los tiempos corresponden a ese entorno y no constituyen una comparación controlada entre equipos. La configuración común facilita la comparación, pero no iguala la capacidad de las redes ni el número de operaciones ejecutadas.

## Fundamento matemático de las arquitecturas

Las redes comparten entrada RGB, salida de tres logits y entropía cruzada, pero difieren en el modo de transformar las representaciones. Para una convolución de kernel $k$, $C_{in}$ canales de entrada y $C_{out}$ de salida, con sesgo, el número de parámetros es $k^2C_{in}C_{out}+C_{out}$. Su costo de inferencia es del orden de $HWk^2C_{in}C_{out}$ operaciones por mapa de salida de tamaño $H\times W$. Estos órdenes no equivalen a tiempos medidos.

### CNN local: composición de filtros espaciales

La transformación elemental es $h_{l+1}=\operatorname{ReLU}(W_l*h_l+b_l)$. Las convoluciones comparten filtros entre posiciones y favorecen la detección de patrones locales; la agrupación reduce resolución espacial. El promedio global elimina gran parte de la información de posición antes de la clasificación.

| Etapa | Salida (canales × alto × ancho) | Parámetros entrenables |
|---|---|---:|
| Convolución 3×3, 3→32; ReLU | 32×128×128 | 896 |
| Max-pooling 2×2 | 32×64×64 | 0 |
| Convolución 3×3, 32→64; ReLU | 64×64×64 | 18.496 |
| Max-pooling 2×2 | 64×32×32 | 0 |
| Convolución 3×3, 64→128; ReLU | 128×32×32 | 73.856 |
| Promedio global; dropout 0,3 | 128 | 0 |
| Capa lineal 128→3 | 3 | 387 |
| **Total** | | **93.635** |

El conteo resulta de $896+18496+73856+387=93635$. La red tiene menor capacidad que las otras dos implementaciones y carece de normalización por lotes y conexiones residuales. Su menor desempeño puede ser compatible con diferencias de capacidad u optimización, pero el experimento no permite aislar la contribución de cada componente. La arquitectura es propia y no se presenta como réplica exacta de una referencia publicada.

### ResNet18: aprendizaje de transformaciones residuales

Un bloque residual calcula $h_{l+1}=\operatorname{ReLU}(F(h_l;W_l)+S(h_l))$, donde $S$ es identidad o una proyección que compatibiliza dimensiones. La ruta de atajo permite combinar la representación de entrada con una transformación aprendida. La implementación contiene cuatro etapas de bloques básicos y termina en promedio global y una capa de tres salidas.

Se utilizaron **11.178.051 parámetros entrenables**. El conteo se obtiene sumando pesos convolucionales, parámetros afines de normalización y la capa final: $P=\sum_l k_l^2C_{in,l}C_{out,l}+\sum_{BN}2C_l+(512\times3+3)$. Las medias y varianzas móviles de normalización son estados del modelo, no parámetros entrenables.

La conexión residual facilita la optimización, pero no elimina el riesgo de sobreajuste. El entrenamiento desde cero evalúa esta implementación sin transferencia de características aprendidas en ImageNet.

### MobileNetV2: expansión y proyección de canales

El bloque combina expansión 1×1, convolución por canal (*depthwise*) y proyección lineal 1×1. Para expansión $E=tC$, kernel $k$ y salida $C'$, los pesos convolucionales de un bloque expandido suman $CE+k^2E+EC'$. A ellos se añaden los parámetros afines de normalización. El atajo se aplica cuando la resolución y los canales son compatibles.

Separar el filtrado espacial de la mezcla de canales reduce el costo respecto a una convolución densa comparable. Sin embargo, expansión, accesos a memoria y eficiencia del dispositivo afectan el tiempo real. La implementación completa, incluida la salida de tres clases, tiene **2.227.715 parámetros**. En el piloto su menor tamaño que ResNet18 no se tradujo en menor tiempo de entrenamiento.

### Comparación del propósito y las restricciones

| Propiedad | CNN local | ResNet18 | MobileNetV2 |
|---|---|---|---|
| Transformación característica | Convolución densa secuencial | Bloques con suma residual | Expansión y filtrado por canal |
| Sesgo compartido | Localidad y filtros compartidos | Localidad y filtros compartidos | Localidad y filtros compartidos |
| Diferencia principal | Baja capacidad | Rutas residuales y mayor capacidad | Factorización y compresión de canales |
| Limitación | Capacidad restringida | Mayor número de parámetros | Eficiencia dependiente del hardware |

Las tres redes pertenecen a la familia convolucional; sus diferencias no implican independencia completa de sesgos inductivos. Su función comparativa es análoga a la de una referencia simple en aprendizaje automático: establecer un nivel de desempeño bajo condiciones comunes. No son matemáticamente equivalentes a regresión logística, pues aprenden representaciones no lineales a partir de píxeles.

El orden de costo por paso de entrenamiento conserva la dependencia de las convoluciones, multiplicada por el tamaño del lote e incluyendo propagación inversa. El costo total también depende del número efectivo de épocas. No se midieron FLOPs, memoria máxima ni latencia de inferencia; no se atribuyen ventajas en esos indicadores.

**Referencias de arquitectura:** He, K., Zhang, X., Ren, S. y Sun, J. (2015), *Deep Residual Learning for Image Recognition*, [doi:10.48550/arXiv.1512.03385](https://doi.org/10.48550/arXiv.1512.03385). Sandler, M., Howard, A., Zhu, M., Zhmoginov, A. y Chen, L.-C. (2018), *MobileNetV2: Inverted Residuals and Linear Bottlenecks*, [doi:10.48550/arXiv.1801.04381](https://doi.org/10.48550/arXiv.1801.04381). Estas referencias fundamentan los mecanismos de las redes; no demuestran su frecuencia como modelos base en histología.
