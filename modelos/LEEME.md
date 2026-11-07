# NuCLS — piloto exploratorio reproducible

## Estado y alcance
Este paquete permite ejecutar 3 candidatos × 5 semillas. **La selección de las tres arquitecturas exigidas por el profesor todavía depende de completar la revisión bibliográfica.** Estas corridas son exploratorias y no se presentan como benchmark final. Si cambian los modelos o el protocolo habrá que ejecutar las nuevas condiciones. No es un modelo de telocitos ni de localización en una imagen completa: clasifica recortes centrados en núcleos ya anotados.

## Mac: ejecutar ahora
Descomprime la carpeta `NuCLS_Piloto_V1` dentro de `~/Desktop/Proyecto_Deep_Learning`.
En la terminal de VS Code o Terminal de macOS:

```bash
cd "$HOME/Desktop/Proyecto_Deep_Learning/NuCLS_Piloto_V1"
conda run --no-capture-output -n nucls_dl python entrenar.py
```

No se requiere reinstalar dependencias: utiliza torch, torchvision, numpy y Pillow del entorno que ya pasó la prueba. Mantén el Mac conectado a corriente, la terminal abierta y evita suspenderlo. Son entrenamientos completos, pueden tardar horas; los tiempos de la prueba de 48 imágenes no permiten prometer una duración. Cada época informa su tiempo real.

El programa verifica primero 17.999 imágenes y los hashes. Luego ejecuta secuencialmente CNN local, ResNet18 y MobileNetV2 para cada semilla 4101–4105. No ejecuta 15 modelos simultáneamente. Ctrl+C interrumpe; repetir el mismo comando retoma desde la última época guardada y omite las corridas terminadas. El trabajo de una época interrumpida se repite. No cambies el código, la configuración, las versiones ni el equipo dentro de una misma carpeta de resultados. No cargues checkpoints de terceros.

## Datos y preprocesamiento
- Train: 14.428 recortes, 79 pacientes; validación: 3.571 recortes, 19 pacientes.
- RGB 128×128 centrados, sin padding; elegibilidad y sesgo hacia núcleos interiores ya documentados.
- Intensidades /255. Rotaciones de múltiplos de 90° y reflexión horizontal únicamente en entrenamiento.
- No se ajusta normalización de tinción ni se aplica CLAHE, suavizado o realce sin experimento comparativo.
- Se comprueban separación de pacientes, hashes exactos y formato. Esto no sustituye la auditoría pendiente de casi duplicados ni el análisis multivariado de calidad.
- No se abren imágenes de prueba/reserva. La prueba histórica expuesta no se presenta como test virgen.

## Protocolo v1 antes de correr
Mismos datos, semillas, transformaciones y presupuesto máximo para todos: sin preentrenamiento, Adam lr=0.001, batch=32, entropía cruzada no ponderada, gradiente limitado a norma 5, máximo 25 épocas, mínimo 5 y paciencia 5. Mejor época por macro-F1 de validación; empate conserva la primera. Early stopping puede producir distintas épocas reales: se reportan.

Métrica primaria macro-F1 de 3 clases; secundarias accuracy, balanced accuracy, precisión/recall/F1 por clase, matrices de confusión, tiempos y parámetros. Se registran métricas por paciente; el F1 de ese archivo fija siempre las 3 clases (si faltan clases en un paciente, se debe interpretar con su soporte). Las probabilidades casi constantes y las predicciones de una sola clase generan avisos y quedan en los resultados, sin eliminar corridas.

Margen operativo preliminar delta=0.02 absoluto de macro-F1: elección de diseño, no umbral de importancia clínica demostrado. Alfa=0.05, potencia objetivo=0.80 para planificar el benchmark posterior, todavía no calculados con datos reales. Cinco semillas estiman variabilidad del algoritmo, **no equivalen a cinco pacientes**. No se generan p-valores ni afirmaciones de superioridad con este paquete. La selección de época usa validación: sus resultados no estiman desempeño final insesgado.

Reproducibilidad: versiones, dispositivo, plataforma, hash del código, configuración y semillas se guardan al inicio. Checkpoints contienen modelo, optimizador y estados aleatorios. Se solicita determinismo con avisos: no se garantiza igualdad bit a bit entre CPU, MPS y CUDA.

## Archivos que devuelve
`resultados/`: configuración, control de datos, historia/curvas por época, mejores y últimos pesos, predicciones de validación, métricas por paciente, resumen entre semillas e informe HTML.

**Adjunta `resultados_RESULTADOS.zip`**, que se actualiza durante la ejecución. Contiene evidencia, no imágenes ni pesos. Los pesos permanecen en `resultados/`. El ZIP parcial no significa que se hayan completado 15 corridas: comprueba el mensaje final y `resumen_modelos.csv` (5 por modelo).

## Colab Pro (alternativa)
1. En tu Mac, dentro de esta carpeta, ejecuta:
   `conda run --no-capture-output -n nucls_dl python empaquetar_datos.py`
2. Sube `NuCLS_DATOS_PILOTO.zip` y el paquete original `NuCLS_Piloto_V1.zip` a la raíz de **Mi unidad** de Drive.
3. Abre `Ejecutar_en_Colab.ipynb` en Colab y selecciona un entorno GPU.
4. Ejecuta sus celdas en orden. Los datos se extraen al disco temporal de Colab; los checkpoints se guardan en Drive.
5. Para reanudar, vuelve a montar/copiar los datos y ejecuta el mismo notebook con iguales versiones y dispositivo. El script rechazará mezclas de configuraciones. No combines automáticamente semillas de Mac y Colab como si fueran un mismo experimento.

Colab Pro ofrece más disponibilidad de cómputo, pero no una GPU ni duración ilimitada garantizadas. https://research.google.com/colaboratory/faq.html

## Pendientes del entregable
Cerrar revisión WoS/Scopus/IEEE y tabla de frecuencias; justificar 3 modelos básicos no redundantes; completar EDA/ruido de etiquetas/casi duplicados/desplazamiento; revisar aprendizaje; calcular tamaño experimental; benchmark final; inferencia por paciente y comparaciones múltiples; Jupyter Book con interpretaciones. No declarar el entregable terminado al finalizar este piloto.
