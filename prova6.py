import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves

arxiu = 'acoustic-guitar-loop-f-91bpm-132687.wav'
mostra, senyal = waves.read (arxiu)


senyalescalda = senyal/(2**15)
time = np.arange  (0, len(senyal), 1)/mostra
time = time * 3000
tamany = np.shape (senyal)
esquerra = senyal [:,0].copy ()

ft = np.fft.fft (esquerra)
freq = np.fft.fftfreq (len(esquerra),0.01)
plt.rcParams ['figure.figsize'] = (15,5)
plt.plot (freq, np.abs(ft))
plt.title ('prova6')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Magnitude')
plt.xlim (0,1)
plt.ylim (0,10000)
plt.tight_layout ()
plt.show ()