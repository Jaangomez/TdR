# Extrae porción de un archivo de audio .wav
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves

# INGRESO 
# archivo = input('archivo de sonido:' )
archivo = 'idk.wav'
archivosalida = 'idk2.wav'
# tiempo en segundos
desde = 3
hasta = 5

muestreo, sonido = waves.read(archivo)

# PROCEDIMIENTO
# indices de muestras
idesde = int(desde*muestreo)
ihasta = int(hasta*muestreo)
porcion = sonido[idesde:ihasta]
duracion = len(porcion)/muestreo

# SALIDA
waves.write(archivosalida, muestreo, porcion)
print('archivo creado: ', archivosalida)