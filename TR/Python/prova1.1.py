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
plt.plot (soroll)
plt.show ()