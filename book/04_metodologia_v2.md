# Metodología del experimento v2

## Objetivo y unidad de análisis

El experimento compara tres redes para clasificar recortes nucleares en las categorías tumoral no mitótica, linfocitaria y estromal. La localización del núcleo procede de las anotaciones; la tarea evalúa clasificación de ventanas previamente seleccionadas. Cada recorte conserva el identificador de paciente y el código TSS para examinar dependencia y procedencia.

La partición comprende 83 pacientes de entrenamiento, 21 de validación y seis de reserva, con códigos TSS disjuntos. El conjunto histórico de prueba ya fue examinado y no se reutiliza como reserva independiente. La nueva reserva se define respecto a los registros de exposición auditados; esa comprobación no demuestra ausencia de cualquier acceso anterior no registrado.

## Arquitecturas y condiciones comunes

| Arquitectura | Parámetros entrenables | Organización característica |
|---|---:|---|
| softmaxCNN-BN adaptada | 898.687 | Convoluciones secuenciales y capas densas |
| DenseNet121 | 6.956.931 | Concatenación de representaciones entre capas |
| ResNet50 | 23.514.179 | Bloques bottleneck con conexiones residuales |

Los modelos se inicializan sin pesos preentrenados. La selección se fundamenta en los comparadores exactos extraídos de los textos revisados, con el alcance documental descrito en el estado del arte; no representa un ranking exhaustivo de toda la literatura. La adaptación de softmaxCNN conserva una cuadrícula de 5×5 antes de las capas densas. Para entradas de 128×128, el mapa previo de 30×30 se agrupa mediante bloques disjuntos de 6×6. Esta operación equivale al promedio adaptativo correspondiente y permite mantener el modo determinista de CUDA. La adaptación no añade parámetros y no constituye una reproducción idéntica del experimento publicado a otra resolución.

## Preprocesamiento y entrenamiento

Las intensidades se dividen por 255 y se estandarizan por canal con parámetros calculados exclusivamente en entrenamiento. Las rotaciones en múltiplos de 90° y la reflexión horizontal se aplican únicamente durante el entrenamiento. No se aplica normalización de tinción, CLAHE ni sobremuestreo previo a la partición. La validación y la reserva conservan su distribución observada.

Se utiliza entropía cruzada sin ponderación, lotes de 32 y limitación de la norma del gradiente a cinco. AdamW evalúa cuatro combinaciones por arquitectura: tasas de aprendizaje 0,0001 y 0,001, con penalización de pesos 0 o 0,0001. Cada ajuste dispone de hasta 25 épocas, un mínimo de cinco y paciencia de cinco. El checkpoint corresponde al mayor macro-F1 de validación; un empate conserva la primera época. La igualdad del presupuesto se refiere a configuraciones y épocas máximas, no a tiempo ni operaciones de cómputo.

## Selección y planificación de corridas

La búsqueda utiliza la semilla 4001. Los hiperparámetros se fijan por arquitectura mediante macro-F1 de validación; los empates favorecen menor tasa de aprendizaje y después menor penalización. Cinco semillas nuevas, 5101–5105, estiman la variabilidad de las diferencias pareadas. El número de corridas finales se planifica para una diferencia de 0,02 en macro-F1, potencia de 0,80 y nivel 0,05/3 para las tres parejas. Se adopta el mayor tamaño requerido, con mínimo cinco; si supera 50 por arquitectura, el flujo registra el límite y se detiene sin evaluar la reserva.

Las corridas finales comienzan en la semilla 6101. La referencia se selecciona por macro-F1 medio de validación, resolviendo empates por menor número de parámetros. El número de semillas describe estabilidad de optimización: aumentar semillas no aumenta el número de pacientes ni sustituye validación externa.

## Evaluación y reproducibilidad

Los identificadores y huellas de todos los checkpoints finales se fijan antes de evaluar la reserva. Cada checkpoint se evalúa una vez dentro del lote previsto. Las predicciones de reserva no intervienen en cambios de arquitectura, hiperparámetros o selección de épocas. Se conservan versiones, configuración, curvas y predicciones por paciente. La latencia se registra con calentamiento y sincronización de GPU; el tiempo por recorte dentro de un lote no equivale a latencia individual de una aplicación.

Las métricas del piloto histórico se presentan en su propio capítulo. La ejecución v2 aporta una evidencia diferente y sus resultados no se infieren a partir de aquel piloto.

## Alcance de la comparación posterior

La comparación de un modelo propuesto con las referencias corresponde al Entregable 3. Antes de observar sus resultados deberán fijarse la modificación propuesta, las hipótesis y la población sobre la cual se busca generalizar. El efecto principal será la diferencia de macro-F1 sobre los mismos casos, acompañada por incertidumbre, métricas por clase y análisis de errores. Una mejora de dos puntos se utiliza como objetivo operativo de planificación; no se interpreta como umbral clínico validado.

La independencia no se demuestra mediante una única métrica. Se documentan solapamientos de pacientes y TSS, duplicados y similitud perceptual; para la incertidumbre se conservan juntos los recortes de cada paciente. Con seis pacientes de reserva, la evidencia entre pacientes es limitada incluso si existen numerosas imágenes o semillas. La ausencia de significación no demuestra equivalencia, y una diferencia estadísticamente detectable no basta por sí sola para afirmar utilidad práctica.
