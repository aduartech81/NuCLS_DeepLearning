# Experimento integrado v2

Este protocolo se publica antes de ejecutar los modelos v2 sobre NuCLS. Las pruebas técnicas con tensores y datos sintéticos no se consideran resultados del conjunto real. Las quince corridas históricas permanecen identificadas como piloto anterior.

## Secuencia fijada

1. Verificar el manifiesto SHA256 `623adf36520751addc324e44cd1b89d95e47842e53cda494914c0248a8be86d4`, los hashes de píxeles de desarrollo y la separación por paciente/TSS. No abrir imágenes de reserva.
2. Comparar softmaxCNN-BN adaptada, DenseNet121 y ResNet50. Cada una evalúa cuatro configuraciones de AdamW: tasas 0,0001/0,001 y weight decay 0/0,0001. La búsqueda utiliza la semilla 4001, hasta 25 épocas, paciencia cinco y un mínimo de cinco. Se conserva el checkpoint con mayor macro-F1 de validación. El presupuesto es igual en número de configuraciones y épocas máximas, no en FLOPs ni minutos.
3. Fijar hiperparámetros por arquitectura según mayor macro-F1. Los empates se resuelven por menor tasa y menor penalización, en ese orden.
4. Ejecutar cinco semillas nuevas por modelo, 5101–5105, para estimar la desviación de las diferencias pareadas. Calcular el número de corridas con t no central, diferencia objetivo 0,02, potencia 0,8 y alpha 0,05/3. Utilizar el mayor R de las tres parejas, con mínimo cinco. Si requiere más de 50, detener y registrar el límite; no reducir R silenciosamente ni evaluar la reserva.
5. Ejecutar R semillas independientes, desde 6101, por arquitectura. No reutilizar las cinco del piloto como corridas finales. Seleccionar la referencia por mayor macro-F1 medio de validación; empate, menor número de parámetros.
6. Fijar hashes de todos los checkpoints antes de abrir la reserva y registrar el lote previsto. Evaluar una vez cada checkpoint dentro de ese lote. No cambiar arquitectura, hiperparámetros, épocas o semillas a partir de esos resultados. Una interrupción puede reanudar el mismo lote; una configuración o checkpoint diferente se rechaza.

## Tratamiento de imágenes

Ventanas RGB 128×128, división por 255 y estandarización con medias `[0.6392034726, 0.4591705400, 0.6277451964]` y desviaciones `[0.2139743516, 0.2214966922, 0.1742893380]`, estimadas únicamente en entrenamiento. Rotaciones de múltiplos de 90° y reflexión horizontal durante entrenamiento. Sin normalización de tinción, CLAHE ni eliminación adicional de imágenes. Entropía cruzada sin pesos y clipping de gradiente en norma cinco, iguales para las tres arquitecturas. Batch 32.

## Inferencia y reproducibilidad

Se registran versiones, código, dispositivo, hiperparámetros, curvas, predicciones por paciente y hashes. Se mide la latencia de inferencia del checkpoint seleccionado con cinco calentamientos y veinte repeticiones, sincronizando GPU cuando corresponde. Se informa tiempo por recorte dentro del batch; no incluye lectura de archivos y no equivale a latencia individual.

En CPU/CUDA se solicitan algoritmos deterministas; en MPS se registran advertencias y no se afirma determinismo estricto. Las configuraciones, el entorno y los checkpoints deben mantenerse para reanudar. La ejecución guarda épocas completadas y resultados parciales.

## Interpretación estadística

La planificación por semillas está condicionada al conjunto de validación y se estima con cinco diferencias; no sustituye el análisis por paciente. Los IC t de medias describen variabilidad entre semillas. La reserva contiene seis pacientes de tres TSS; sus 969 recortes no constituyen 969 unidades clínicas independientes. El análisis final debe añadir intervalos agrupados por paciente y no transformar ausencia de significación en equivalencia.

## Ejecución

```bash
python modelos/experimento_v2.py --datos /ruta/a/recortes_v2 --salida /ruta/nueva/EXPERIMENTO_V2 --device cuda
```

Se recomienda GPU para las tres arquitecturas. El tiempo depende del dispositivo, la parada temprana y R; no se ha estimado mediante entrenamiento real v2. `auto` selecciona CUDA, MPS o CPU. Al finalizar produce un ZIP de métricas y predicciones; los checkpoints permanecen en la carpeta de ejecución.
