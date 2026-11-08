# NuCLS · Aprendizaje profundo en histología

**Andrés Duarte Chaves · Maestría en Ingeniería Biomédica · Entregable 1**

Comparación V2 de CNN compacta con BatchNorm, DenseNet121 y ResNet50 para tres categorías nucleares NuCLS. Entrenamiento: 14.539 recortes / 83 pacientes; validación: 2.049 / 21; reserva: 969 / 6. Los TSS y pacientes son disjuntos entre particiones.

- [Dashboard](https://nucls-andres-duarte.onrender.com/)
- [Jupyter Book](https://aduartech81.github.io/NuCLS_DeepLearning/intro.html)
- [EDA ejecutado](book/10_eda_v2.ipynb)
- [Experimento V2 y evidencia](book/08_resultados_v2.md)
- [Notebook Colab ejecutado, con salidas](colab/Experimento_NuCLS_v2_ejecutado_cierre11.ipynb)
- [Plantilla de entrenamiento](colab/Experimento_NuCLS_v2.ipynb)
- [Estadística V2 y umbral de mejora](book/05_estadistica.md)
- [Curvas, búsqueda, piloto y tiempos recuperados](resultados_analizados/auditoria_v2/)
- [Anexo: piloto histórico](book/08_resultados_piloto.md)

## Alcance científico

La selección V2 combina evidencia bibliográfica verificable, capacidad y conectividad. La revisión no acredita que estos sean los tres modelos más frecuentes y sencillos de todo el corpus. Esta restricción no se resuelve cambiando la redacción.

V2 está cerrado con 11 semillas por modelo (33 corridas). ResNet50 fue seleccionado por validación antes de evaluar la reserva. El notebook ejecutado conserva 805 registros de épocas del desarrollo y cierre; las curvas, tiempos y validación por semilla se reconstruyeron de su stdout redondeado. El plan original exigía 22 semillas: la reducción limita la potencia. En reserva ResNet50 y DenseNet121 no se distinguen por semillas; el bootstrap por pacientes responde a otra fuente de incertidumbre. Solo hay seis pacientes y 70 recortes estromales.

## Dashboard

El dashboard Dash Plotly presenta siete pestañas: problema, imágenes, estado del arte, EDA, modelos y resultados, discusión y reproducibilidad. Consume evidencias y predicciones ya calculadas; no entrena modelos.

Desde la raíz de una copia de este repositorio, con Python 3.12:

```bash
python3 -m venv .venv_dashboard
source .venv_dashboard/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Dirección local: http://127.0.0.1:8050/.

`render.yaml` define un servicio gratuito con verificación `/health`. El servicio está publicado en https://nucls-andres-duarte.onrender.com/.

## Reproducción del análisis histórico

En un entorno separado del entrenamiento:

```bash
python -m pip install -r requirements_book.txt -r requirements_eda.txt
python scripts/consolidar_eda.py
python scripts/analizar_piloto.py
python scripts/presentacion_visual.py
python scripts/generar_galeria.py
python scripts/ampliar_eda.py
python scripts/planificar_piloto.py
jupyter nbconvert --to notebook --execute --inplace book/07_analisis_ejecutado.ipynb
jupyter-book build book
```

El notebook contiene salidas de cálculos ejecutados. La publicación conserva esas salidas y compila el libro sin ejecutar nuevos entrenamientos. Los análisis V2 adicionales consumen predicciones de reserva ya guardadas, sin ejecutar inferencia.

## Organización y procedencia

- `book/`: capítulos, notebook y figuras.
- `app.py`, `assets/`: dashboard.
- `modelos/`: implementaciones del piloto y del experimento V2.
- `resultados/`: predicciones comprimidas, curvas y configuración de quince corridas históricas.
- `resultados_analizados/`: métricas recalculadas, incertidumbre y planificación.
- `evidencias/`: auditorías, selección, trazabilidad y hashes.
- `scripts/`: análisis y generación de figuras.

La galería contiene doce ejemplos ilustrativos de entrenamiento, con trazabilidad en `evidencias/galeria_train.json`. El conjunto completo de imágenes y los pesos no se incluyen. El EDA V2 incluye medias y desviaciones RGB de recortes de entrenamiento; los análisis de campos del piloto están identificados por separado.

## Comprobaciones

Se verificaron las predicciones, las métricas, el emparejamiento de semillas y el cálculo exacto de Wilcoxon mediante enumeración de signos. La publicación del JBook se verifica mediante GitHub Actions. El dashboard fue comprobado con el cliente de pruebas de Flask y funciones de sus siete pestañas. La validación local y la publicación en Render son comprobaciones distintas.

## Reproducción del piloto de entrenamiento

Python 3.11. El entorno registrado se encuentra en `requirements_entrenamiento.txt`.

```bash
python -m pip install -r requirements_entrenamiento.txt
python modelos/entrenar.py --datos /ruta/al/piloto_interior128/20261105_225210 --salida resultados_reproduccion
```

La ruta se proporciona explícitamente. El entrenador exige el manifiesto original con su hash y conserva las comprobaciones de pacientes y píxeles entre particiones. Este comando reproduce el piloto; no construye una nueva partición confirmatoria ni descarga las imágenes.

## Evidencia bibliográfica

Las exportaciones originales se conservan por separado. `evidencias/literatura/` contiene el inventario bibliográfico, las decisiones de lectura y los conteos de depuración. Los registros por revisar no son estudios incluidos. Los resúmenes completos exportados no se redistribuyen en este repositorio.


## Auditoría V2

`python scripts/auditoria_estadistica_v2.py` reconstruye curvas y contrastes de las salidas conservadas. `python scripts/robustez_reserva_v2.py /ruta/al/cierre/reserva` calcula sensibilidad por paciente/TSS y pruebas exploratorias agrupadas. Latencia de inferencia y Grad-CAM siguen pendientes: los tiempos de época no son latencia.
