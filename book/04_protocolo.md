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
