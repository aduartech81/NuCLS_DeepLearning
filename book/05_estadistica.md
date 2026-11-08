# Plan de comparación estadística V2

## Unidad de análisis y selección de referencia

Se comparan CNN compacta con BatchNorm, DenseNet121 y ResNet50 sobre la misma partición. Macro-F1 es la métrica primaria. El baseline se selecciona mediante el mayor macro-F1 medio de validación en las corridas finales; los empates se resuelven por menor número de parámetros. No se utiliza la reserva para elegir arquitectura, hiperparámetros ni épocas.

## Búsqueda, piloto y corridas finales

Cada arquitectura dispone de cuatro configuraciones de hiperparámetros. Las cinco semillas 5101–5105 estiman variabilidad preliminar para planificar el número de corridas por modelo. El archivo `plan_corridas.json` registra el número calculado, que no debe confundirse con cinco corridas fijas. Las semillas finales comienzan en 6101. El margen de planificación es 0,02 absoluto de macro-F1, con potencia objetivo 0,80 y nivel 0,05/3 para tres comparaciones. Es una decisión operativa, no un umbral clínico validado.

## Diferencias e incertidumbre

El análisis por semillas utiliza diferencias pareadas entre arquitecturas bajo la misma partición. Se informarán magnitud, dispersión e intervalos, distinguiendo supuestos paramétricos de contrastes basados en rangos. La normalidad de diferencias se examina conjuntamente con Q-Q; una prueba no significativa, especialmente con pocas semillas, no demuestra normalidad. La multiplicidad se tratará por familias de contrastes previamente identificadas, evitando elegir la prueba que produzca el menor valor p.

El análisis por paciente conserva juntos los recortes de cada individuo. El remuestreo de predicciones fijas mide incertidumbre condicionada a los modelos ajustados; no reproduce el entrenamiento ni estima toda la variabilidad entre centros. Los intervalos por semillas y por pacientes responden a preguntas diferentes y se presentan por separado.

## Métricas complementarias y errores

El cierre incorpora matrices de confusión, F1 por clase, MCC, AP macro, AUC y calibración descriptiva de reserva a partir de las probabilidades guardadas. Las métricas indefinidas en pacientes o TSS sin alguna categoría se identificarán como tales. McNemar sobre recortes correlacionados no se interpretará como inferencia poblacional independiente; la dependencia por paciente debe incorporarse en la comparación de errores.

La galería de errores y Grad-CAM se construirán sobre validación con criterios de selección explícitos. Grad-CAM describe sensibilidad espacial del modelo y no demuestra causalidad ni corrección biológica. La medición de inferencia registrará dispositivo, lote, calentamiento y sincronización. Los resultados por paciente y TSS acompañarán el promedio global para mostrar heterogeneidad.

## Referencia humana y límites

La concordancia multi-rater es una referencia distinta de un límite teórico de rendimiento. Requiere etiquetas alineadas por núcleo y evaluador. Sin esa evidencia no se estimará una cota humana mediante cifras tomadas de otro experimento ni mediante uno menos el error del modelo. La reserva de seis pacientes y 70 recortes estromales limita fuertemente la precisión, incluso con numerosas semillas.

## Evidencia disponible

Los contrastes ya calculados para CNN local, ResNet18 y MobileNetV2 se conservan en el [anexo estadístico histórico](anexo_estadistica_piloto.md). No constituyen resultados V2. El cierre V2 verificó 33 archivos de predicciones y sus resúmenes. Se incorporó un remuestreo exhaustivo exploratorio por paciente, manteniendo fijas las once semillas de cada modelo, descrito en el [capítulo de resultados](08_resultados_v2.md). Este análisis no sustituye los contrastes y la potencia planificados; el cuaderno de Colab publicado como plantilla no sustituye un cuaderno ejecutado con salidas.

## Cierre intermedio y precisión

El piloto requirió 11, 22 y 12 semillas para las parejas compacta–DenseNet121, compacta–ResNet50 y DenseNet121–ResNet50; se adoptó 22. El cierre autorizado utilizó 11 por modelo y no satisface ese máximo. La potencia objetivo no se deduce de la significación observada. Los intervalos agrupados por paciente son exploratorios, posteriores al cierre y nominales, sin ajuste por multiplicidad; no constituyen evidencia confirmatoria de superioridad.
