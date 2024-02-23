import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile  as waves

arxiu = 'acoustic-guitar-loop-f-91bpm-132687.wav'
mostra, soroll = waves.read (arxiu)

print ('mostra (Hz) : ', mostra)
print(soroll)
plt.plot(soroll)
plt.show()