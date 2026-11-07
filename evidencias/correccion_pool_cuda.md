# Corrección de pooling CUDA

El primer backward en Colab T4 falló por AdaptiveAvgPool2d con determinismo estricto. Para la CNN con entrada 128, el mapa previo es 30x30 y las regiones adaptativas 5x5 son exactamente bloques disjuntos 6x6. Se sustituye por AvgPool2d(6,6); para entrada 27 el mapa 5x5 se conserva mediante identidad. No cambian pesos ni número de parámetros. Se mantiene el modo determinista.

Se verificaron en CPU float64 la salida y los gradientes frente a AdaptiveAvgPool2d para ambos tamaños con tolerancias 1e-12. La verificación GPU debe ejecutarse en Colab. Se utiliza otra carpeta de salida para no mezclar huellas de código con el intento fallido.
