import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# Load the audio file
audio_path = 'aaaaaa.wav'  # Replace with your audio file path
y, sr = librosa.load(audio_path, sr=None)

# Compute the Short-Time Fourier Transform (STFT)
D = librosa.stft(y)

# Convert the complex-valued STFT into magnitude
D_magnitude = np.abs(D)

# Convert amplitude to decibels (optional, for better visualization)
D_db = librosa.amplitude_to_db(D_magnitude, ref=np.max)

# Plot the STFT
plt.figure(figsize=(10, 6))
librosa.display.specshow(D_db, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Short-Time Fourier Transform (STFT)')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show()