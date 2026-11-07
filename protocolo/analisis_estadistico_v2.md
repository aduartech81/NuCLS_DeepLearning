# Plan de análisis para la nueva partición

## Estimando y selección

La métrica primaria será macro-F1 de las tres clases, con predicción por argmax. Cada semilla producirá un modelo y sus probabilidades; se resumirán media y desviación estándar entre semillas. No se interpretará el número de recortes como tamaño muestral independiente. Los modelos se seleccionarán y ajustarán usando entrenamiento y validación, sin consultar desempeño en reserva.

La referencia operativa será el modelo con mayor macro-F1 medio de validación entre las configuraciones fijadas. La regla de desempate será menor número de parámetros. Su desempeño se estimará después en reserva; no se cambiará retrospectivamente la referencia para favorecer un resultado de prueba.

## Margen y contrastes

Se propone un margen práctico académico de 0,02 unidades absolutas de macro-F1. Este margen no procede de una validación clínica ni se presenta como umbral universal. Para la comparación posterior con un modelo avanzado, la hipótesis de mejora relevante será H0: diferencia ≤ 0,02 frente a H1: diferencia > 0,02. Un resultado no significativo no demostrará equivalencia.

Las tres comparaciones entre baselines se reportarán bilateralmente alrededor de cero, con corrección de Holm por familia. Los contrastes sobre margen práctico se distinguirán de los contrastes de igualdad. La mejora mínima detectable se calculará con la variabilidad del piloto correspondiente a las arquitecturas y partición finalmente utilizadas, alfa familiar 0,05 y potencia 0,80. No se trasladará automáticamente el cálculo R=12 del piloto anterior a modelos o datos diferentes.

## Incertidumbre y métricas secundarias

Se informarán IC t entre semillas y, por separado, bootstrap pareado por paciente que aplique la misma muestra a todos los modelos. Para no confundir fuentes de variación, el segundo análisis condicionará en las semillas entrenadas y explicitará que no reentrena sobre nuevas muestras. Con solo seis pacientes de reserva, sus intervalos serán exploratorios y potencialmente inestables; se incluirá sensibilidad al retirar un paciente cada vez.

Se reportarán precisión, recobrado y F1 por clase, matrices de confusión, MCC, ROC-AUC uno-contra-resto y average precision macro. Se registrarán Brier multiclase, log-loss, ECE de diez intervalos y fiabilidad. Si una réplica carece de una clase, su AUC será indefinida y se informará la cantidad de réplicas válidas, sin sustituirla por cero.

La batería requerida por la guía comprenderá Shapiro y Q-Q de diferencias, t pareada, Wilcoxon, Friedman con comparaciones de rangos y ANOVA de medidas repetidas con supuestos explícitos. Con n pequeño, estos resultados no se presentarán como pruebas de normalidad o garantías de potencia. Se distinguirán análisis confirmatorios planificados de sensibilidad y exploratorios.

Para errores y AUC se mantendrá el emparejamiento por observación y paciente. Un McNemar calculado por recorte se identificará como análisis convencional que no modela dependencia intrapaciente y se acompañará de incertidumbre agrupada. No se afirmará que DeLong convencional resuelve por sí solo esa dependencia.

## Protección de la reserva

La reserva no participa en selección de arquitectura, búsqueda, elección de época, calibración ni decisiones de preprocesamiento. Antes de obtener sus predicciones se guardarán versiones, hashes, configuración, semillas, número de repeticiones y checkpoints. Cualquier cambio posterior se documentará como análisis exploratorio.

Este documento establece reglas analíticas prospectivas para una evaluación aún no ejecutada. No es un prerregistro completo: la selección bibliográfica de arquitecturas, el espacio de búsqueda y el número definitivo de corridas todavía deben incorporarse y fijarse antes del entrenamiento correspondiente.
