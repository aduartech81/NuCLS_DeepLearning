# Problema, pregunta y alcance

## Formulación
El problema pertenece a clasificación multiclase de imágenes. Cada observación es un recorte RGB de 128×128 píxeles centrado en un núcleo anotado. El espacio de entrada es $\mathcal X=[0,1]^{3\times128\times128}$; el espacio de salida es $\mathcal Y=\{0,1,2\}$, correspondiente, en orden, a `tumor_nonMitotic`, `lymphocyte` y `nonTILnonMQ_stromal`.

El modelo $f_\theta:\mathcal X\to\Delta^2$ produce tres probabilidades cuya suma es uno. La clase predicha es $\hat y=\arg\max_k f_\theta(x)_k$. El piloto minimiza entropía cruzada no ponderada:

$$\mathcal L(\theta)=-\frac1N\sum_{i=1}^{N}\log f_\theta(x_i)_{y_i}.$$

Las etiquetas se conservan con sus nombres originales para evitar equivalencias biológicas no justificadas. La imagen aporta apariencia y contexto local; no confirma por sí sola identidad molecular o diagnóstico clínico.

## Pregunta de investigación
¿Qué desempeño y variabilidad presentan tres modelos básicos de Deep Learning, seleccionados mediante literatura pertinente, al clasificar estos recortes de NuCLS bajo partición por paciente y condiciones experimentales comparables?

Hipótesis operativa: las diferencias de arquitectura pueden producir diferencias reproducibles de macro-F1. El estudio estimará diferencias pareadas e incertidumbre, sin asumir que mayor complejidad implica mejor desempeño. Para cada pareja, la hipótesis nula es diferencia esperada igual a cero; la relevancia práctica se examinará separadamente.

## Objetivos
1. Auditar procedencia, integridad, etiquetas y dependencias de los datos.
2. Desarrollar EDA orientado a decisiones de preprocesamiento y evaluación.
3. Extraer y justificar exactamente tres modelos básicos de la literatura.
4. Implementar condiciones comparables y cuantificar variabilidad mediante múltiples semillas.
5. Establecer el baseline y sus límites con inferencia apropiada a la dependencia entre recortes.

## Métricas y unidad de independencia
La métrica primaria del piloto es macro-F1 de las tres clases. Se reportarán también precisión, recall y F1 por clase, accuracy, balanced accuracy, matrices de confusión y costo computacional. Para el benchmark se incorporarán AUC multiclase justificadas y análisis cualitativo de saliencia, conforme a la guía.

El paciente es la unidad de agrupamiento para partición e inferencia. Los recortes son observaciones correlacionadas; las semillas son repeticiones algorítmicas, no nuevos pacientes. El margen operativo preliminar es $\delta=0.02$ absoluto de macro-F1; no constituye un umbral clínico validado. Debe quedar justificado y fechado antes del benchmark definitivo.

## Alcance de generalización
La evaluación propuesta alcanza pacientes no usados para ajustar modelos dentro del dominio estudiado. No demuestra generalización a otros órganos, centros, tinciones, escáneres ni imágenes sin localización previa. La elegibilidad de recortes interiores sin padding puede excluir núcleos próximos al borde y sesgar la muestra.
