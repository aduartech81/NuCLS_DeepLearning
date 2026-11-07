# NuCLS · Entregable 1 · Andrés Duarte Chaves

Avance funcional con Jupyter Book, notebook ejecutado y dashboard Dash Plotly. No es todavía la entrega académica final: la literatura, revisión de calidad pendiente, diseño confirmatorio e inferencia final deben cerrarse.

## Revisar ahora sin instalar
El notebook ejecutado está en `book/07_analisis_ejecutado.ipynb`. El workflow compila el JBook desde los capítulos fuente; el HTML generado no se versiona.

## Dashboard en Mac, separado del entrenamiento
Descomprima esta carpeta dentro de `~/Desktop/Proyecto_Deep_Learning/`. En otra terminal:
```bash
cd "$HOME/Desktop/Proyecto_Deep_Learning/NuCLS_Entregable1_ConResultados"
conda run -n nucls_dl python -m venv .venv_dashboard
source .venv_dashboard/bin/activate
python -m pip install -r requirements.txt
python app.py
```
Abra http://127.0.0.1:8050/ en el navegador. No se inicia ningún entrenamiento.

## Publicar en GitHub y Render
1. Crear un repositorio independiente para Deep Learning. Colocar el contenido de esta carpeta en la raíz, conservando `.github/workflows` y `.gitignore`.
2. En GitHub, Settings > Pages > Source: GitHub Actions. Ejecutar el workflow `Publicar Jupyter Book`.
3. En Render, New > Blueprint y conectar el repositorio: detectará `render.yaml`. Alternativa: Web Service Python, build `pip install -r requirements.txt`, start `gunicorn app:server --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`.
4. Confirmar `/health`, las cinco pestañas, los filtros y el enlace público del JBook. La configuración no equivale a un despliegue confirmado.

Documentación oficial: https://render.com/docs/deploy-flask y https://dash.plotly.com/deployment

## Incorporar resultados reales
Con el ZIP del entrenador original:
```bash
python scripts/importar_resultados.py /ruta/resultados_RESULTADOS.zip
```
El importador conserva evidencia y rechaza sobreescrituras. Revisar cinco corridas por modelo, fallos y configuración antes de inferir. El dashboard mostrará medias y desviaciones de validación, claramente rotuladas como piloto.

## Reproducir documentación
En un entorno separado del entrenamiento, con Python 3.12:
```bash
python -m pip install -r requirements_book.txt
python scripts/consolidar_eda.py
jupyter nbconvert --to notebook --execute --inplace book/07_analisis_ejecutado.ipynb
jupyter-book build book
```
Los estadísticos y el notebook utilizan las evidencias incluidas. No descargan imágenes originales ni abren prueba/reserva. `requirements_entorno_verificado.txt` registra las versiones de este entorno Linux; no obliga a alterar el entorno del piloto Mac.

## Entrenamiento
`modelos/` conserva copias de los scripts originales del piloto para trazabilidad. Continúe usando la carpeta original `NuCLS_Piloto_V1` para reanudar las corridas actuales: no mueva checkpoints ni cambie su entorno. Los datos originales y pesos no se incluyen en el paquete de publicación.

## Verificación realizada
- Notebook: ocho celdas de código ejecutadas con IPython en proceso y salidas reales capturadas. Este entorno no permite abrir sockets de un kernel separado. El notebook conserva código estándar, ejecutable con Jupyter en Mac/Colab.
- Jupyter Book compilado a HTML.
- Dashboard: respuestas HTTP de raíz, health, layout y dependencias; cinco pestañas y seis combinaciones de filtros verificadas programáticamente.
- La revisión visual en navegador y el despliegue externo están pendientes.

## Actualización: piloto completo
Las quince corridas fueron incorporadas y verificadas. El notebook fue reejecutado y el JBook reconstruido. El dashboard lee resultados/resumen_modelos.csv. Ver book/08_resultados_piloto.md. GitHub y Render siguen pendientes de publicación; no se modificaron repositorios existentes.

## Evidencias en GitHub
Las predicciones por corrida se conservan como CSV gzip sin pérdida; pandas las lee directamente. De los archivos ZIP de auditoría se incluyen sus resúmenes JSON utilizados en los cálculos. Los paquetes originales se mantienen como evidencias del autor. El repositorio no redistribuye imágenes histológicas ni pesos.
