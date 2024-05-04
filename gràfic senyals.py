import librosa
import numpy as np
import scipy.io.wavfile as waves
import matplotlib.pyplot as plt

arxiu = "Sounds/29 (F# mig).wav"
mostra, senyal = waves.read(arxiu)
ft = np.fft.rfft (senyal)
print (np.abs(ft))
freq = np.fft.rfftfreq (len(senyal), d=1./44110)
print (freq)
temps1 = 2
tempsfinal = 2.02

def ona_tems_freq(arxiu, temps1, tempsfinal):
    y, sr = librosa.load(arxiu, sr=None, offset=temps1, duration=tempsfinal - temps1)

    duració_audio = librosa.times_like(y, sr=sr)/50

    plt.figure(figsize=(10, 4))
    plt.plot(duració_audio, y)
    plt.xlabel('Temps (s)')
    plt.ylabel('Amplitud')
    plt.title('Ona F#(A4)')
    plt.show()

ona_tems_freq(arxiu, temps1, tempsfinal)