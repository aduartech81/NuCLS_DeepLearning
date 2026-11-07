# Qué ve la red: imágenes y preparación

<div class="nucls-note"><strong>Idea central.</strong> La unidad de entrada es un recorte RGB de 128 × 128 píxeles alrededor de una anotación nuclear. La etiqueta corresponde al núcleo objetivo, aunque en el recorte aparezcan otros núcleos.</div>

## Tres clases, imágenes reales

![Doce recortes de entrenamiento: cuatro por clase, con paciente y fila de anotación.](figuras/galeria_train.jpg)

**Procedencia:** ejemplos incluidos en `CONTROL_PILOTO_QC_20261105_225210.zip`, miembro `galeria_train.html`. Se verificó que los cinco pacientes mostrados pertenecen al entrenamiento. Los archivos originales son RGB de 128 × 128 píxeles; la figura los amplía para lectura, sin realce de color ni filtrado. Las etiquetas se conservan del paquete recibido: no son predicciones ni una nueva revisión anatomopatológica.

**Selección:** se muestran los doce ejemplos ya disponibles en la galería, cuatro por clase. No constituyen una muestra aleatoria nueva ni permiten estimar la frecuencia de artefactos del conjunto completo. Los hashes y las etiquetas están en `evidencias/galeria_train.json`.

## Qué podemos observar y qué implica

| Observación visible | Implicación para el experimento |
|---|---|
| Los recortes contienen distintas cantidades de tejido y fondo claro. | El modelo puede aprovechar contexto además del núcleo; debemos estudiar posibles atajos. |
| Aparecen varios núcleos en una misma ventana. | Clasificar la ventana no equivale a localizar o segmentar cada núcleo. |
| La apariencia cambia entre pacientes y ejemplos. | La separación por paciente es necesaria para evaluar generalización. |
| Las tres categorías conservan variabilidad interna. | No se puede justificar una clasificación perfecta a partir de unos pocos ejemplos visuales. |

La galería ilustra el problema, pero no establece que una etiqueta sea correcta o incorrecta. Tampoco acredita capacidad para reconocer telocitos.

## Preparación que realmente se ejecutó

<div class="nucls-grid">
<div class="nucls-card"><strong>128 × 128</strong><span>Ventana centrada y completamente contenida en la imagen. Se descartan recortes que necesitan relleno.</span></div>
<div class="nucls-card"><strong>RGB / 255</strong><span>Reescalado fijo de intensidad. Sin CLAHE, normalización de tinción ni estandarización por canal.</span></div>
<div class="nucls-card"><strong>Solo train</strong><span>Rotaciones en múltiplos de 90° y reflexión horizontal durante entrenamiento.</span></div>
</div>

**Decisión y costo:** conservar el centro evita desplazar el objetivo. Excluir ventanas que requieren relleno evita ese artefacto, pero reduce la muestra y favorece núcleos interiores. El [EDA cuantifica esa retención](02_resultados_eda.md); no se presenta la selección como neutra.

## Qué falta para una galería de errores

Para mostrar aciertos y fallos se debe unir cada predicción con **su recorte exacto**, modelo, semilla, clase de referencia y probabilidad. Las imágenes de esta página son de entrenamiento y no se asociarán a predicciones de validación de otros archivos. La inspección de errores requiere recuperar los recortes correspondientes; las [matrices de confusión](08_resultados_piloto.md) ya resumen los errores medidos sin simular ejemplos.

La atribución visual —por ejemplo, Grad-CAM— necesitará además los pesos del modelo correspondiente y verificación de la capa utilizada. No se presenta un mapa decorativo como explicación del clasificador.
