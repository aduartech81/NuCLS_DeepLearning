# Ejecución NuCLS v2 en Colab

[Abrir cuaderno en Colab](https://colab.research.google.com/github/aduartech81/NuCLS_DeepLearning/blob/main/colab/Experimento_NuCLS_v2.ipynb)

El cuaderno utiliza el código fijado en el commit `6d672bcb13a33536f9e1c48d002c6f7c513d969e`. No contiene resultados simulados ni sustituye el notebook de análisis ejecutado del informe.

Primero se genera `NuCLS_V2_DATOS.zip` mediante `scripts/empaquetar_datos_v2.py` y se sube a la raíz de Mi unidad. El cuaderno verifica los archivos, extrae las imágenes al disco local de Colab y conserva checkpoints y resultados en Drive. Se requiere GPU y espacio para los pesos de las corridas.

Las fases y sus límites se documentan en [ejecución integrada](../protocolo/ejecucion_integrada_v2.md). Al terminar se incorpora el ZIP de resultados al análisis; la revisión bibliográfica y la interpretación científica requieren su propio cierre.
