import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import os
import matplotlib as mpl
import itertools as it
import statistics as st
import librosa
from scipy.fft import fft

def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

arxiu = 'Sounds/29 (F# mig).wav'
mostra, senyal = waves.read(arxiu)
y, sr = librosa.load(arxiu)

sampFreq = 44110
tamany = np.shape (senyal)

ft = np.fft.rfft (senyal)
coefficients = fft(senyal)
print (len(coefficients))
ona_reconstruida = np.fft.ifft(ft)
print (ona_reconstruida)
roundft = np.round(ft)
absft = np.abs(ft)
freq = np.fft.rfftfreq (len(senyal), d=1./sampFreq)
roundfreq = np.round(freq)
absfreq = np.abs(freq)

duration = librosa.get_duration(y=y, sr=sr)
samples = len(y) +1 
sampFreq = 44100 
t1 = np.linspace (0, duration, len(y))

plt.figure(figsize=(10, 6))
plt.plot(t1, y)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.title('Audio Signal')
plt.grid(True)
plt.show()

def increment(absft):
    amplituds = []
    step = 251
    x = 251
    while  step <= len(absft):
        maxim = (max(absft[(step-251):step]))
        index = np.where(absft==maxim)[0][0]
        frequencia = freq[index]
        amplituds.append (maxim)
        #print ("Amplitude", str(maxim) + "Frequency", str(frequencia) + "Place", str(index))
        step += 250
        x += 250
        #if absft_x > maxim:
            #print ("not max" + "Amplitudex", str(absft_x) > "Amplitudemaxim", str(maxim)) 
    amplituds.sort()
    amplituds_màximes = amplituds[-1000:len(amplituds)]
    #print (amplituds_màximes)
    dicc = {}
    for i in amplituds_màximes:
        indexs = searchindex (i, absft)
        dicc [i] = freq[indexs]
        dicc [i] = coefficients[indexs]
        
    #print (dicc)
    return dicc

d = increment(absft)
array_amplituds = []
array_frequencies = []
array_coefficients = []
for i in d.keys():
    array_amplituds.append (i)
    array_frequencies.append (d[i])
    array_coefficients.append(d[i])
print(len(array_coefficients))
print (len(array_frequencies))
n = 1
z = 2
t = np.linspace(0, duration, int(duration * sampFreq), endpoint=False)
sine_waves =[]
cosine_waves = []
while n < len(array_coefficients):
    sine_wave = [array_coefficients[n] * np.sin(2 * np.pi * array_frequencies[n] * t)]
    sine_waves.append(sine_wave)
    n +=2
while z < len(array_coefficients):
    cosine_wave = [array_coefficients[z] * np.cos(2 * np.pi * array_frequencies[z] * t)]
    cosine_waves.append(cosine_wave)
    z += 2

# Combine waveforms
sum_sine = np.sum(sine_waves, axis=0)
sum_cosine = np.sum(cosine_waves, axis = 0)

total_wave = coefficients [0] + sum_sine + sum_cosine

# Normalize the waveform to be within the range [-1, 1]
total_wave /= np.max(np.abs(total_wave))

# Convert to 16-bit integers
combined_waveform_int = np.array(total_wave).astype(np.int16)
sample = 1000

x = np.arange(sample)

x_values = np.linspace (0, 1000, len(total_wave))  # Adjust the range and number of points as needed

# Calculate the corresponding y-values using the wave equation

# Plot the wave
plt.plot(x_values, combined_waveform_int)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Wave Representation')
plt.grid(True)
plt.show()
plt.close ()

# Save the waveform as a .wav file
waves.write('combined_sound.wav', sampFreq, combined_waveform_int)

# Define the range of x-values
sample = 1000

x = np.arange(sample)

x_values = np.linspace (0, 1000, len(total_wave))  # Adjust the range and number of points as needed

# Calculate the corresponding y-values using the wave equation

# Plot the wave
plt.plot(x_values, combined_waveform_int)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Wave Representation')
plt.grid(True)
plt.show()
plt.close ()

# Generate sample data for the unknown wave
# For demonstration, let's create a sample sine wave
# Replace this with your actual data
num_samples = 1000
t_values = np.linspace(0, 2*np.pi, num_samples)
sampled_wave = np.sin(t_values)

# Compute the Fourier coefficients using discrete Fourier transform (DFT)
fourier_coefficients = fft(sampled_wave)

# Reconstruct the wave using the computed Fourier coefficients
reconstructed_wave = np.fft.ifft(fourier_coefficients)

# Plot the original sampled wave and the reconstructed wave
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(t_values, sampled_wave, label='Sampled wave')
plt.plot(t_values, reconstructed_wave.real, label='Reconstructed wave')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Unknown Wave Reconstruction using Fourier Series')
plt.legend()
plt.grid(True)
plt.show()
