# Experimento V2: modelos y evidencia de ejecución

| Arquitectura | Parámetros entrenables, tres clases | Función |
|---|---:|---|
| CNN compacta con BatchNorm | 898.687 | Referencia de capacidad reducida |
| DenseNet121 | 6.956.931 | Conectividad densa |
| ResNet50 | 23.514.179 | Conectividad residual |

La comparación utiliza 14.539 recortes de entrenamiento y 2.049 de validación, con pacientes y TSS disjuntos. La reserva contiene 969 recortes de seis pacientes. La selección y el procedimiento se describen en la [metodología V2](04_metodologia_v2.md).

## Estado de la evidencia

El registro comunicado por el autor muestra `densenet121`, semilla 6101, época 7. Corresponde a una corrida final en curso, no al resultado agregado. Su macro-F1 de época no permite seleccionar el baseline ni estimar una ventaja entre arquitecturas. Los resultados finales V2 todavía no se han incorporado y verificado en este repositorio.

El paquete final debe conservar `estado.json`, `configuracion.json`, `plan_corridas.json`, `hiperparametros_seleccionados.json`, `resumen_experimento.csv`, predicciones, curvas y huellas de checkpoints. El notebook descargado después de la ejecución documentará las salidas y el entorno. Un archivo de notebook sin salidas solo acredita la disponibilidad del procedimiento.

## Separación del experimento anterior

Las quince corridas de CNN local, ResNet18 y MobileNetV2 corresponden al [piloto histórico](08_resultados_piloto.md). Sus métricas y contrastes no se trasladan a las referencias V2 y no definen su baseline.
