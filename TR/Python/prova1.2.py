import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves

arxiu = 'acoustic-guitar-loop-f-91bpm-132687.wav'
mostra, soroll = waves.read (arxiu)

tamany = np.shape (soroll)
canals = len(tamany)
tipus = 'estéreo'
if (canals<2):
    tipus = 'monofònic'
duració = len(soroll) /mostra
print ('mostra (Hz) :', mostra)
print ('canals:' + str(canals) + ' tipus' + tipus)
print ('duració (s):', duració)
print ('tamany de la matriu:', tamany)
print (soroll)
plt.rcParams ['figure.figsize'] = (15,5)
sorollscaled = soroll/(2**15)
timeValues = np.arange (0, len(sorollscaled), 1)/mostra
timeValues = timeValues * 3000
plt.plot (timeValues, sorollscaled)
plt.title('prova1.2', size=16)
plt.text (0-50, np.max(sorollscaled), 'màxim', fontsize = 16, bbox=dict(facecolor='red', alpha=0.5))
plt.xlabel ('temps (ms)')
plt.ylabel  ('Amplitud')
plt.show ()