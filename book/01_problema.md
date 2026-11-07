# Problema, pregunta y alcance

## Formulación
El estudio aborda un problema de clasificación multiclase de imágenes. Cada observación es un recorte RGB de 128×128 píxeles centrado en un núcleo anotado. El espacio de entrada es $\mathcal X=[0,1]^{3\times128\times128}$; el espacio de salida es $\mathcal Y=\{0,1,2\}$, correspondiente, en orden, a `tumor_nonMitotic`, `lymphocyte` y `nonTILnonMQ_stromal`.

El modelo $f_\theta:\mathcal X\to\Delta^2$ produce tres probabilidades cuya suma es uno. La clase predicha es $\hat y=\arg\max_k f_\theta(x)_k$. El piloto minimiza entropía cruzada no ponderada:

$$\mathcal L(\theta)=-\frac1N\sum_{i=1}^{N}\log f_\theta(x_i)_{y_i}.$$

Las etiquetas se conservan con sus nombres originales para evitar equivalencias biológicas no justificadas. La imagen aporta apariencia y contexto local; no confirma por sí sola identidad molecular o diagnóstico clínico.

## Pregunta de investigación
¿Qué desempeño y variabilidad presentan una CNN local, ResNet18 y MobileNetV2 al clasificar estos recortes de NuCLS bajo partición por paciente y condiciones experimentales comparables?

Hipótesis operativa: las diferencias de arquitectura pueden producir diferencias reproducibles de macro-F1. El estudio estima diferencias pareadas e incertidumbre, sin asumir que mayor complejidad implica mejor desempeño. La comparación descriptiva considera la diferencia media pareada; el contraste exploratorio de Wilcoxon evalúa simetría de las diferencias respecto a cero. La relevancia práctica se examina por separado.

## Objetivos
1. Auditar procedencia, integridad, etiquetas y dependencias de los datos.
2. Desarrollar EDA orientado a decisiones de preprocesamiento y evaluación.
3. Contextualizar las tres arquitecturas evaluadas mediante antecedentes de clasificación nuclear, distinguiendo evidencia directa y tareas adyacentes.
4. Implementar condiciones comparables y cuantificar variabilidad mediante múltiples semillas.
5. Establecer el baseline y sus límites con inferencia apropiada a la dependencia entre recortes.

## Métricas y unidad de independencia
La métrica primaria del piloto es macro-F1 de las tres clases. Se calculan también precisión, sensibilidad y F1 por clase, exactitud, matrices de confusión, AUC multiclase uno contra el resto y tiempo de entrenamiento. El AUC se considera una métrica secundaria exploratoria. No se realizaron análisis de saliencia.

El paciente es la unidad de agrupamiento para partición e inferencia. Los recortes son observaciones correlacionadas; las semillas son repeticiones algorítmicas, no nuevos pacientes. El margen operativo preliminar es $\delta=0.02$ absoluto de macro-F1; no constituye un umbral clínico validado. Se utiliza como referencia exploratoria de magnitud, sin atribuirle validación clínica ni carácter de prerregistro.

## Alcance de generalización
La validación incluye pacientes distintos de los utilizados para ajustar los parámetros, aunque interviene en la selección de épocas. No demuestra generalización a otros órganos, centros, tinciones, escáneres ni imágenes sin localización previa. La elegibilidad de recortes interiores sin padding puede excluir núcleos próximos al borde y sesgar la muestra.
