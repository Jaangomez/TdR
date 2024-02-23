import numpy as np
import matplotlib.pyplot as plt

#Generar  sèrie  de temps
time = np.arange (0,10,0.01)
signal =  2*np.sin(2*np.pi*1*time) + 1*np.sin(2*np.pi*2*time) 

#Gràfiica de la sèrie original
plt.figure (figsize=(10,4))
plt.subplot (2,1,1)
plt.plot (time,signal)
plt.title ('Original time series')
plt.xlabel ('Time')
plt.ylabel ('Amplitude')

#Transformada de Fourier
fourier_transform = np.fft.fft (signal)
frequencies = np.fft.fftfreq (len(signal),0.01)
plt.subplot (2,1,2)
plt.plot (frequencies,np.abs(fourier_transform))
plt.title ('Fourier  transform')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Magnitude')
plt.xlim (0,5)

#Ensenyar gràfica
plt.tight_layout ()
plt.show ()