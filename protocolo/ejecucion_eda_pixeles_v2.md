# EDA de píxeles de desarrollo v2

El script `scripts/completar_eda_pixeles_v2.py` procesa exclusivamente los recortes de entrenamiento y validación del manifiesto v2 verificado. La lectura de la reserva queda excluida antes de abrir los archivos de imagen.

La ejecución verifica dimensiones, modo RGB y hashes; calcula media y desviación RGB de los píxeles de entrenamiento, histogramas por clase y partición, descriptores de color y textura, candidatos de similitud perceptual entre particiones y diagnósticos por paciente mediante regresión logística. La estimación de escalado se realiza dentro de cada pliegue.

La clasificación adversarial usa como etiqueta la partición train/validation y como observación la mediana de descriptores por paciente. La predicción de sitio utiliza únicamente entrenamiento y TSS con al menos tres pacientes. Son diagnósticos descriptivos de señal disponible; no representan clasificación nuclear ni demuestran por sí solos un atajo aprendido por las redes.

Los candidatos de dHash son pares con distancia Hamming <=4. Se informa el total y se exportan hasta 500 pares para inspección; el umbral no valida duplicación ni descarta todos los posibles solapamientos. No se eliminan imágenes.

## Ejecución

Dependencias: Python, NumPy, Pillow y scikit-learn. Se registran versiones y hashes en el resultado. No requiere PyTorch ni GPU.

```bash
python scripts/completar_eda_pixeles_v2.py --datos /ruta/a/recortes_v2 --salida /ruta/nueva/EDA_PIXELES_V2
```

La carpeta de salida debe ser nueva. Se produce un único ZIP con descriptores, histogramas, candidatos y resumen. El programa no modifica los datos originales, no ajusta clasificadores de núcleos y no evalúa la reserva.

## Comprobaciones del código

Se comprobaron descriptores de una imagen constante, distancia de hashes conocida, un diagnóstico sintético separable con validación agrupada y rechazo de manifiestos que no coinciden. Estas comprobaciones no equivalen a ejecutar el análisis sobre las imágenes reales del autor.
