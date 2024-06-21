import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

# Step 1: Read the WAV file
sr, so = wavfile.read('Sounds/29 (F# mig).wav')

# If the audio is stereo, take one channel
if so.ndim > 1:
    so = so[:, 0]

# Normalize the data
so = so / np.max(np.abs(so))

# Step 2: Apply the Fourier Transform
ft = np.fft.fft(so)
freq = np.fft.fftfreq(len(ft), 1/sr)
rft = np.fft.rfft(so)
absrft = np.abs(rft)
rfreq = np.fft.rfftfreq(len(ft), 1/sr)

# Step 3: Manipulate the Frequency Components (Optional)
# Low-pass filter: zero out frequencies above a certain threshold
cutoff_frequency = 8000  # Hz
ft[np.abs(freq) > cutoff_frequency] = 0

# Plot the magnitude spectrum after filtering
plt.figure()
plt.plot(rfreq, absrft)
plt.title('Magnitude Spectrum after Filtering')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.show()

# Step 4: Apply the Inverse Fourier Transform
reconstructed_data = np.fft.ifft(ft)
reconstructed_data = np.real(reconstructed_data)

# Step 5: Save the Reconstructed Audio to a New WAV File
reconstructed_data = np.int16(reconstructed_data / np.max(np.abs(reconstructed_data)) * 32767)
wavfile.write('reconstructed.wav', sr, reconstructed_data)

