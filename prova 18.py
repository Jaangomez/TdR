import librosa
import numpy as np
import matplotlib.pyplot as plt

# Load audio file
audio_file = 'Sounds/In a sentimental mood.wav'
y, sr = librosa.load(audio_file)

# Perform onset detection
onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=512, backtrack=True)

# Define window size for each frame
window_size = 2048  # Adjust as needed

# Extract frames around each onset
frames = []
for onset in onset_frames:
    frame = y[max(0, onset - window_size // 2):min(len(y), onset + window_size // 2)]
    frames.append(frame)

# Perform FFT on each frame
fft_frames = []
for frame in frames:
    if len(frame) > 0:  # Check if frame is not empty
        fft = np.fft.fft(frame)
        fft_frames.append(fft)

# Compute frequency axis for visualization
freqs = np.fft.fftfreq(window_size, d=1/sr)

# Plot the magnitude spectrum of each frame's FFT
for i, fft in enumerate(fft_frames):
    plt.figure()
    plt.plot(freqs[:window_size//2], np.abs(fft)[:window_size//2], label='Magnitude Spectrum')
    plt.title(f'FFT Magnitude Spectrum for Frame {i+1}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.grid(True)

plt.show()



