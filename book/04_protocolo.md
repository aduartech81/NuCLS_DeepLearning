# Implementación y protocolo exploratorio

CNN local, ResNet18 y MobileNetV2 son candidatos técnicos implementados. Su elección definitiva depende de la matriz de literatura y de la frecuencia de uso de la arquitectura exacta en la tarea. Una referencia sobre una familia o sobre un backbone de segmentación no demuestra que una variante concreta sea un baseline frecuente de clasificación de recortes.

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

Cinco semillas por tres modelos equivalen a quince corridas planificadas. El ZIP recibido contiene quince resultados completos. Las predicciones y las métricas se verificaron; el capítulo de resultados presenta los promedios y sus límites.

Las épocas reales pueden diferir por parada temprana. Reportar tiempo y épocas, dispositivo, versiones y presupuesto efectivo. No mezclar corridas de Mac y Colab sin tratar el cambio de entorno explícitamente. El piloto permite planificar recursos y variabilidad; no sustituye el benchmark definitivo.
