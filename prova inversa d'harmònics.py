import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

sr, so = wavfile.read('Sounds/29 (F# mig).wav')

ft = np.fft.fft(so)
freq = np.fft.fftfreq(len(ft), 1/sr)
rft = np.fft.rfft(so)
absrft = np.abs(rft)
rfreq = np.fft.rfftfreq(len(ft), 1/sr)

plt.figure()
plt.plot(rfreq, absrft)
plt.title('Espectre original')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.show()

reconstrucció = np.fft.ifft(ft)
part_real_original = np.real(reconstrucció)

part_real_original = np.int16(part_real_original / np.max(np.abs(part_real_original)) * 32767)
wavfile.write('ona_original2.wav', sr, part_real_original)