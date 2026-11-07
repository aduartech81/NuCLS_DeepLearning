# Plan estadístico y límites

Este es el plan del benchmark definitivo. El capítulo de resultados contiene el análisis exploratorio ya calculado del piloto.

1. Verificar corridas completas y fallidas sin eliminar resultados desfavorables.
2. Resumir por modelo media, desviación estándar y variabilidad de macro-F1, además de costo y métricas por clase.
3. Comparar modelos de forma pareada: misma partición, mismas unidades y semillas planificadas.
4. Estimar intervalos mediante remuestreo por paciente para respetar correlación entre recortes; mantener el pareamiento entre modelos. Distinguir incertidumbre por pacientes de variación por inicialización.
5. Definir familia de comparaciones y ajustar por multiplicidad, por ejemplo Holm para las tres parejas.
6. Usar la variabilidad exploratoria para planificar potencia objetivo 0,80 con alfa 0,05 y margen preliminar 0,02. Documentar supuestos, número de repeticiones y diferencia mínima detectable.

Con cinco pares, el menor p-valor bilateral exacto de Wilcoxon es $2/2^5=0.0625$: no puede alcanzar alfa 0,05. Añadir una semilla tampoco garantiza potencia suficiente, especialmente con corrección múltiple. La guía exige reconocer esta limitación y justificar el diseño.

No confundir ausencia de significancia con equivalencia. Una afirmación de equivalencia requerirá un análisis específico y un margen justificado. El uso compartido de prueba entre semillas produce dependencia: no tratar todas las predicciones o corridas como nuevos sujetos independientes.

La declaración definitiva del protocolo debe preceder al benchmark. Los valores de validación ya observados forman parte de la etapa exploratoria y no se presentarán como un prerregistro anterior a su observación.
