# Selección operativa de modelos v2

La selección utiliza comparadores identificados en textos completos y separa arquitectura, función y tarea. La tabla `evidencias/literatura/frecuencia_comparadores_verificados.csv` cuenta cada DOI una sola vez por arquitectura. No suma preprints y artículos del mismo estudio ni agrupa variantes distintas bajo un nombre genérico.

## Alcance de la evidencia

La extracción estructurada comprende cuatro textos con comparaciones verificadas: RCCNet, OLConvNet, GrEp y Sánchez-Torres et al. No representa el cribado completo de los 1.330 registros recuperados. Las frecuencias son conteos del subconjunto leído y no estimaciones de prevalencia en toda la literatura. La selección permite especificar un experimento trazable; no acredita por sí sola que la revisión bibliográfica esté completa.

| Modelo elegido | Estudios verificados | Parámetros para tres clases | Criterio |
|---|---:|---:|---|
| softmaxCNN con BatchNorm, adaptada a 128×128 | 1 | 898.687 | Referencia pequeña y reproducible, conexiones secuenciales |
| DenseNet121 | 1 | 6.956.931 | Reutilización de características mediante concatenación densa |
| ResNet50 | 2 | 23.514.179 | Mayor frecuencia exacta en la extracción, conexiones residuales |

ResNet50 se prioriza frente a ResNet18 por su presencia en dos comparaciones de clasificación nuclear multiclase. No se afirma que sea la alternativa residual más pequeña. Entre las referencias con una observación, la CNN pequeña minimiza parámetros y DenseNet121 aporta conexiones diferentes con menor tamaño que las variantes VGG/AlexNet registradas. No existe una ordenación única que minimice simultáneamente frecuencia, profundidad y parámetros: la decisión explicita ese compromiso. DenseNet121 tiene mayor profundidad nominal que ResNet50, aunque menos parámetros.

CNN3L informa una arquitectura pequeña, pero la correspondencia entre dimensiones descritas y parámetros requiere resolución adicional; no se presenta como reproducción verificada. ViT no se selecciona sin identificar su variante. Las variantes adaptadas de AlexNet y GoogLeNet no se equiparan automáticamente a las implementaciones estándar. La referencia ResNet18 de GrEp corresponde a subclasificación epitelial binaria con preentrenamiento; se conserva como contexto.

## Arquitectura y adaptación

La CNN pequeña contiene convoluciones válidas 3→36 (4×4) y 36→48 (3×3), cada una seguida por ReLU, BatchNorm y max-pooling 2×2. La representación 48×5×5 alimenta capas densas 512, 512 y tres salidas. Las capas densas ocultas incorporan ReLU, BatchNorm y dropout 0,5. El orden implementado es ReLU→BatchNorm→dropout.

Para entradas 27×27 y cuatro clases se verifican los 899.200 parámetros publicados en RCCNet. Para mantener ventanas comunes de 128×128 se añade un pooling adaptativo 5×5 sin parámetros antes del clasificador. En entradas 27×27 ese adaptador es identidad. En 128×128 cambia la agregación espacial; por tanto, el experimento es una adaptación declarada, no una reproducción exacta del protocolo publicado.

DenseNet121 conserva crecimiento 32 y bloques 6–12–24–16 de la implementación de torchvision, con salida de tres clases. ResNet50 conserva bloques bottleneck 3–4–6–3, con salida de tres clases. Ambas incluyen pooling global. Las tres redes se inicializan sin pesos preentrenados, con el mismo conjunto de datos, estandarización, aumentos, pérdida y presupuesto de configuraciones. Este diseño compara implementaciones bajo condiciones comunes, sin reproducir los regímenes de transferencia de todos los artículos fuente.

## Función de referencia

Estas redes proporcionan puntos de comparación para modelos posteriores. Su equivalencia con un modelo logístico como referencia es funcional: fijar un desempeño reproducible que deba superarse. No comparten su hipótesis lineal ni su capacidad. La CNN secuencial aprende filtros locales; DenseNet concatena representaciones y ResNet suma transformaciones residuales. Los parámetros y el tiempo de inferencia se informan para valorar el costo de cada representación.

## Fuentes

- Basha et al., RCCNet: https://doi.org/10.1109/ICARCV.2018.8581147 ; secciones III y tabla I, https://arxiv.org/pdf/1810.02797 .
- Tripathi y Singh, OLConvNet: https://doi.org/10.1145/3345318 ; tabla 1, https://arxiv.org/pdf/2202.10177 .
- Sánchez-Torres et al.: https://doi.org/10.1155/acis/4540418 ; tabla 6.
- Frei et al., GrEp: https://doi.org/10.1016/j.patcog.2025.112197 ; sección 3.3 y tabla 4.
