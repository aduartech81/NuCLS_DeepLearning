# NuCLS · Aprendizaje profundo en histología

**Andrés Duarte Chaves · Maestría en Ingeniería Biomédica · Entregable 1**

Comparación exploratoria de CNN local, ResNet18 y MobileNetV2 para clasificar recortes nucleares en tres categorías de NuCLS. El análisis comprende 17.999 recortes, 98 pacientes y quince entrenamientos registrados. La partición por paciente separa entrenamiento y validación.

- [Dashboard público](https://nucls-andres-duarte.onrender.com/)
- [Informe Jupyter Book](https://aduartech81.github.io/NuCLS_DeepLearning/intro.html)
- [Notebook ejecutado](https://aduartech81.github.io/NuCLS_DeepLearning/07_analisis_ejecutado.html)
- [Archivo notebook](book/07_analisis_ejecutado.ipynb)
- [Resultados e incertidumbre](https://aduartech81.github.io/NuCLS_DeepLearning/08_resultados_piloto.html)

## Alcance científico

El piloto compara desempeño, variabilidad entre semillas y tiempo de entrenamiento. La selección de épocas utiliza la validación; los resultados no constituyen evaluación externa. La revisión narrativa contextualiza las familias de redes, pero no demuestra que las tres implementaciones sean los modelos base más recurrentes de la literatura. El sistema clasifica recortes nucleares previamente localizados de NuCLS. La detección en lámina completa no forma parte de la evaluación.

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

## Reproducción del análisis

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

El notebook contiene salidas de cálculos ejecutados. La publicación conserva esas salidas y compila el libro sin ejecutar nuevos entrenamientos. Los scripts analíticos no acceden a imágenes de prueba o reserva.

## Organización y procedencia

- `book/`: capítulos, notebook y figuras.
- `app.py`, `assets/`: dashboard.
- `modelos/`: implementaciones y entrenador del piloto.
- `resultados/`: predicciones comprimidas, curvas y configuración de quince corridas.
- `resultados_analizados/`: métricas recalculadas, incertidumbre y planificación.
- `evidencias/`: auditorías, selección, trazabilidad y hashes.
- `scripts/`: análisis y generación de figuras.

La galería contiene doce ejemplos ilustrativos de entrenamiento, con trazabilidad en `evidencias/galeria_train.json`. El conjunto completo de imágenes y los pesos no se incluyen. Los estadísticos RGB describen campos completos; no son parámetros de normalización de recortes.

## Comprobaciones

Se verificaron las predicciones, las métricas, el emparejamiento de semillas y el cálculo exacto de Wilcoxon mediante enumeración de signos. El JBook compila sin advertencias. El dashboard fue comprobado con el cliente de pruebas de Flask y funciones de sus siete pestañas. La validación local y la publicación en Render son comprobaciones distintas.

## Reproducción del piloto de entrenamiento

Python 3.11. El entorno registrado se encuentra en `requirements_entrenamiento.txt`.

```bash
python -m pip install -r requirements_entrenamiento.txt
python modelos/entrenar.py --datos /ruta/al/piloto_interior128/20261105_225210 --salida resultados_reproduccion
```

La ruta se proporciona explícitamente. El entrenador exige el manifiesto original con su hash y conserva las comprobaciones de pacientes y píxeles entre particiones. Este comando reproduce el piloto; no construye una nueva partición confirmatoria ni descarga las imágenes.

## Evidencia bibliográfica

Las exportaciones originales se conservan por separado. `evidencias/literatura/` contiene el inventario bibliográfico, las decisiones de lectura y los conteos de depuración. Los registros por revisar no son estudios incluidos. Los resúmenes completos exportados no se redistribuyen en este repositorio.
