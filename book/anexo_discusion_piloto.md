# Anexo: discusión del piloto histórico


## Hallazgos principales

<div class="nucls-grid">
<div class="nucls-card"><strong>+10,36 pp</strong><span>Diferencia descriptiva de macro-F1 de MobileNetV2 frente a la CNN local.</span></div>
<div class="nucls-card"><strong>0,49 pp</strong><span>Diferencia entre MobileNetV2 y ResNet18: pequeña y con intervalo exploratorio que cruza cero.</span></div>
<div class="nucls-card"><strong>Estroma</strong><span>La clase con menor F1 medio en las tres arquitecturas; principal limitación del desempeño por clase.</span></div>
</div>

**Respuesta a la pregunta:** las arquitecturas candidatas no obtienen el mismo desempeño descriptivo. ResNet18 y MobileNetV2 superan a la CNN local en este piloto y muestran promedios cercanos entre sí. Esto no establece cuál generaliza mejor a pacientes nuevos: la validación intervino en la selección de épocas.

## Qué aporta el experimento

El aporte actual es una comparación reproducible de tres implementaciones sobre la misma selección de recortes y la misma partición por paciente, con cinco semillas por modelo. Se verificaron las predicciones y se conservaron curvas, configuración y evidencia numérica. No se afirma una arquitectura nueva ni originalidad metodológica demostrada.

## Interpretación del desempeño

La menor puntuación estromal puede orientar la revisión de ejemplos y confusiones, pero las métricas por sí solas no identifican una causa. No permiten atribuir los errores a mecanismos biológicos, calidad de anotación, tinción o tamaño nuclear sin análisis adicional.

MobileNetV2 utiliza menos parámetros que ResNet18, pero registró mayor tiempo medio en el equipo utilizado. La eficiencia depende de la ejecución y del hardware; el número de parámetros no sustituye una medición controlada de latencia o memoria.

## Límites que condicionan las conclusiones

- **Selección de imágenes:** los recortes sin relleno favorecen núcleos interiores y no representan automáticamente todos los núcleos de QC.
- **Dependencia y tamaño efectivo:** 3.571 recortes de validación proceden de 19 pacientes; no son 3.571 observaciones clínicas independientes.
- **Selección del modelo:** la mejor época se eligió con la validación que después se resume. Los intervalos exploratorios no eliminan ese optimismo.
- **Incertidumbre:** el bootstrap conserva fijas las cinco corridas y no reproduce nuevos entrenamientos. Sus intervalos marginales no tienen corrección múltiple.
- **Literatura:** la síntesis narrativa contextualiza las familias de redes, pero no estima la frecuencia de uso de las tres arquitecturas exactas. La selección se interpreta como exploratoria.
- **Alcance:** se clasifican ventanas previamente localizadas. No se ha evaluado detección en lámina completa ni uso clínico.

## Conclusión

ResNet18 y MobileNetV2 alcanzaron macro-F1 medios de 81,91% y 82,39%, respectivamente, frente al 72,03% de la CNN local. La proximidad entre las dos primeras, la incertidumbre de la diferencia y la menor sensibilidad estromal de MobileNetV2 impiden resumir el resultado en un único modelo superior. El estudio aporta una comparación reproducible dentro del dominio y la selección evaluados; su alcance es exploratorio y no acredita utilidad clínica ni generalización externa.

La síntesis se basa en las [quince corridas verificadas](08_resultados_piloto.md), no en un entrenamiento adicional ni en resultados simulados.
