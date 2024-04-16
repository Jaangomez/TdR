import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import librosa

arxiu = "la4 pur.wav"

def plot_frequency_spectrum(arxiu):

    sampFreq, senyal = waves.read(arxiu)
    canal_esquerra = senyal [:,0].copy ()
  
    ft = np.fft.rfft(canal_esquerra)
    freq = np.fft.rfftfreq(len(canal_esquerra), d=1./sampFreq)
    absft = np.abs(ft)

    print (absft)
    maxim = max(absft)
    index_maxim = np.argmax(absft)    
    freq_maxima = freq[index_maxim]
    print (freq_maxima)

    absft = absft[:len(freq)]
    
    
    plt.figure(figsize=(10, 6))
    plt.plot(freq, absft)
    plt.plot(freq_maxima, maxim, 'o', color='k')
    plt.annotate(text = round(freq_maxima, 2), xy=(freq_maxima, maxim), xytext=(freq_maxima, maxim), horizontalalignment='left',
                  verticalalignment= 'bottom', fontsize=8)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude |X(Freq)|')
    plt.title('Fourier A4 pur')
    plt.show()

plot_frequency_spectrum(arxiu)

