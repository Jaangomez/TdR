import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io import wavfile
from scipy.special import jn, jn_zeros
from scipy.signal import find_peaks
import librosa
import librosa.display
import scipy.signal as signal
from scipy.optimize import curve_fit
from scipy.integrate import quad

#Forma del plat
radi_plat = 0.2  
radi_forat = 0.0065 
gruix_plat = 0.001  

#Propietats del plat
ρ = 8500  #densitat (kg/m^3)
E = 105e9  #Mòdul de Young (Pa)
ν = 0.34  #Proporicó de Poissoin's

#Rigidesa de flexió
D = E * gruix_plat**3 / (12 * (1 - ν**2))

#Massa que hi ha a cada unitat d'àrea
μ = ρ * gruix_plat

#Funció de Bessel
modes = 15
zeros_bessel = jn_zeros(0, modes)

def freqüència_natural(α, radi, D, μ):
    return (α / radi)**2 * np.sqrt(D / μ) / (2 * np.pi)

frequencies = [freqüència_natural(α, radi_plat, D, μ) for α in zeros_bessel]

print("Freqüències Naturals:")
for i, freq in enumerate(frequencies):
    print(f"Mode {i+1}: {freq:.2f} Hz")

#Mides dels modes i representació
mida = 100
r = np.linspace(radi_forat, radi_plat, mida)
θ = np.linspace(0, 2 * np.pi, mida)
R, θ = np.meshgrid(r, θ)

def mode_shape(r, θ, α, radi):
    return jn(0, α * r / radi)

for i, α in enumerate(zeros_bessel):
    Z = mode_shape(R, θ, α, radi_plat)
    X = R * np.cos(θ)
    Y = R * np.sin(θ)
    
    plt.figure(figsize=(8, 8))
    plt.contourf(X, Y, Z, cmap='RdBu_r')
    plt.colorbar(label='Desplaçament')
    plt.title(f'Forma del mde {i+1} per α={α:.2f}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.show()

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='RdBu_r', edgecolor='k')
    ax.set_title(f'Forma del mode {i+1} per α={α:.2f}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Desplaçament')

print("Equacions de les formes de mode:")
for i, (α, freq) in enumerate(zip(zeros_bessel, frequencies)):
    print(f"Forma del mode {i+1}: w_{i+1}(r, θ, t) = J_0({α:.2f} * r / {radi_plat:.2f}) * cos({freq:.2f} * t + φ)")

sr, senyal = wavfile.read('Sounds/recording5.wav')

#Per conveniència ja que surt diverses vegades
len_senyal = len(senyal)

duració = librosa.get_duration(y=senyal, sr=sr)
temps = np.linspace(0, duració, num=len_senyal)


def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

sampFreq = 44110
tamany = np.shape (senyal)

ft = np.fft.rfft (senyal)
roundft = np.round(ft)
absft = np.abs(ft)
ft_freq = np.fft.rfftfreq (len(senyal), d=1./sampFreq)
roundfreq = np.round(freq)
absfreq = np.abs(freq)

plt.figure(figsize=(10, 4))
plt.plot(senyal, temps)
plt.title('Senyal de vibració')
plt.xlabel('Temps (mostres)')
plt.ylabel('Amplitud')
plt.show()

def increment(absft):
    amplituds = []
    step = 251
    x = 251
    while  step <= len(absft):
        maxim = max(absft[(step-251):step])
        index = np.where(absft==maxim)[0][0]
        frequencia = freq[index]
        amplituds.append (maxim)
        step += 250
        x += 250 
    amplituds.sort()
    amplituds_màximes = amplituds[-10:len(amplituds)]
    dicc = {}
    for i in amplituds_màximes:
        indexs = searchindex (i, absft)
        dicc [i] = freq[indexs]
        
    print (dicc)
    return dicc

d = increment(absft)
array_amplituds = []
array_frequencies = []
for i in d.keys():
    array_amplituds.append (i)
    array_frequencies.append (d[i])
    print (array_amplituds)
    print(array_frequencies)

for i in array_amplituds:
    proporció_general = i*100/sum(absft)
    proporció_dins_harmònics_màxims = i*100/sum(array_amplituds)
    print (f'{proporció_general}%')
    print (f'{proporció_dins_harmònics_màxims}%')

plt.rcParams ['figure.figsize'] = (15,8)
plt.plot (freq, absft)
plt.title ('FFT vibació del plat')
plt.xlabel ('Freqüència (Hz)')
plt.ylabel ('Amplitude |X(Freq)|')
plt.plot (array_frequencies, array_amplituds, 'o', color='k')
for x, y in zip(array_frequencies, array_amplituds):
    plt.annotate(text=(round(x, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
            verticalalignment = 'bottom', fontsize=8)
        
plt.tight_layout ()
plt.show()

#Màxims = Freqüènces naturals
màxims, propietats = find_peaks(absft, height=np.max(absft) * 0.1)
print("Freqüències naturals (experimentals):")
for max in màxims:
    print(f"{ft_freq[max]:.2f}")

freqüències_experimentals = ft_freq[màxims]
amplituds_experimentals = propietats['peak_heights']

#Cercar valors propers entre els valors experimentals i analítics/teòrics
mode_amplituds = np.zeros_like(frequencies)
for freq_exp, amplitud in zip(freqüències_experimentals, amplituds_experimentals):
    index_proper = np.argmin(np.abs(np.array(frequencies) - freq_exp))
    mode_amplituds[index_proper] = amplitud

print("Freqüències naturals i amplituds:")
for i, (freq, amp) in enumerate(zip(frequencies, mode_amplituds)):
    print(f"Mode {i+1}: Freqüència = {freq:.2f} Hz, Amplitud = {amp:.2f}")

#Superposició de modes
def combined_mode_shape(r, θ, αs, radi, amplituds):
    resultat = np.zeros_like(r)
    for α, amplitud in zip(αs, amplituds):
        resultat += amplitud * jn(0, α * r / radi)
    return resultat

mode_combinat = combined_mode_shape(R, θ, zeros_bessel, radi_plat, mode_amplituds)
X = R * np.cos(θ)
Y = R * np.sin(θ)

plt.figure(figsize=(8, 8))
plt.contourf(X, Y, mode_combinat, cmap='RdBu_r')
plt.colorbar(label='Desplaçament')
plt.title('Mode combinat')
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal')
plt.show()

#Short-Time Fourier Transform (STFT)
D = librosa.stft(senyal)
amplitud_stft, fase_stft = librosa.magphase(D)
stft_freq = np.linspace(0, sr / 2, D.shape[0])
temps = np.arange(D.shape[1]) * (len_senyal / sr) / D.shape[1]

#Passar a decibels
log_magnitude = librosa.amplitude_to_db(amplitud_stft, ref=np.max)

plt.figure(figsize=(10, 8))
librosa.display.specshow(log_magnitude, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('STFT so del plat')
plt.xlabel('Temps (s)')
plt.ylabel('Freqüència (Hz)')
plt.show()

if len(màxims) == 0:
    print("No peaks detected in the spectrum.")
else:
    print("Peaks detected at frequencies (Hz):")
    for max in màxims:
        print(f"{stft_freq[max]:.2f}")

#FFT amb màxims marcats
plt.figure(figsize=(10, 6))
plt.plot(stft_freq, absft)
plt.scatter(frequencies[màxims], absft[màxims], color='red')
plt.title('Frequency Spectrum with Identified Peaks')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

#Aproximació d'harmònics
def trobar_harmonics(stft_freq, freq_actual, error=0.01):
    harmonics = []
    n = 1
    while True:
        freq_harmonic = freq_actual * n
        index_proper = np.argmin(np.abs(stft_freq - freq_harmonic))
        if np.abs(stft_freq[index_proper] - freq_harmonic) / freq_harmonic < error:
            harmonics.append(stft_freq[index_proper])
        else:
            break
        n += 1
    return harmonics

if len(màxims) > 0:
    print("Harmònics freqüencies naturals (experimentals amb STFT):")
    for freq_actual in frequencies[màxims]:
        harmonic_series = trobar_harmonics(frequencies, freq_actual)
        print(f"Harmònics amb freqüència natural {freq_actual:.2f} Hz: {harmonic_series}")
else:
    print("Sense màxims")

#Aproximació amortiment
def amortiment(senyal, sr):
    
    freq_natural_aprox = freqüències_experimentals[np.argmin(np.abs(np.array(frequencies)-freqüències_experimentals))]

    max_index = np.argmin(np.abs(ft_freq - freq_natural_aprox))
    max_amplitud = absft[max_index]
    hp_amplitud = max_amplitud / np.sqrt(2)
    
    #HPBW
    index_menor = np.argmin(np.abs(absft[:max_index]) - hp_amplitud)
    index_major = np.argmin(np.abs(absft[max_index:]) - hp_amplitud) + max_index
    
    hp_bandwith = ft_freq[index_major] - ft_freq[index_menor]
    
    #Amoritment
    rao_amortiment = hp_bandwith / freq_natural_aprox
    
    return rao_amortiment, freq_natural_aprox

amortiment_hp_bandwith = amortiment(senyal, sr)[0]

print(f"Amortiment: {amortiment_hp_bandwith:.4f}")
print(f"Freqüència natural: {amortiment(senyal, sr)[1]:.2f} Hz")

#FRF
array_freqs, espectre_intensitat = signal.welch(senyal, sr, nperseg=1024)

plt.figure(figsize=(10, 4))
plt.semilogy(array_freqs, espectre_intensitat)
plt.title('FRF')
plt.xlabel('Freqüència (Hz)')
plt.ylabel('Intensitat/Freqüència (dB/Hz)')
plt.show()

max_ressonant = np.argmax(espectre_intensitat)
freq_ressonant = array_freqs[max_ressonant]

hp = espectre_intensitat[max_ressonant] / 2
indexs = np.where(espectre_intensitat >= hp)[0]
bandwidth = array_freqs[indexs[-1]] - array_freqs[indexs[0]]

# Calculate the damping ratio
hp_bandwith = bandwidth / (2 * freq_ressonant)
print(f"Amortiment 2 càlcul: {hp_bandwith:.4f}")

# Fourier Series Coefficients Calculation
def a0(duració, funció_senyal):
    return (1 / duració) * quad(funció_senyal, 0, duració)[0]

def an(duració, funció_senyal, n):
    return (2 / duració) * quad(lambda t: funció_senyal(temps) * np.cos(2 * np.pi * n * temps / duració), 0, duració)[0]

def bn(duració, funció_senyal, n):
    return (2 / duració) * quad(lambda t: funció_senyal(temps) * np.sin(2 * np.pi * n * temps / duració), 0, duració)[0]

def funció_senyal(temps):
    index = int(temps * sr)
    if index >= len_senyal:
        return 0
    return senyal[index]

#Coeficients  de Fourier
valor_a0 = a0(duració, funció_senyal)
coeficients = [(an(duració, funció_senyal, n), bn(duració, funció_senyal, n)) for n in range(1, 10)]

print("Coeficients de Fourier:")
print(f"a0: {valor_a0:.4f}")
for n, (a_n, b_n) in enumerate(coeficients, start=1):
    print(f"a{n}: {a_n:.4f}, b{n}: {b_n:.4f}")

#Reconstrucció senyal
def sèrie_fourier(temps, duració, a0, coeficients):
    resultat = a0
    for n, (a_n, b_n) in enumerate(coeficients, start=1):
        resultat += a_n * np.cos(2 * np.pi * n * temps / duració) + b_n * np.sin(2 * np.pi * n * temps / duració)
    return resultat

# Reconstructed signal
senyal_reconstruïda = sèrie_fourier(temps, duració, valor_a0, coeficients)

plt.figure(figsize=(12, 6))
plt.plot(temps, senyal, label='Senyal original')
plt.plot(temps, senyal_reconstruïda, '--', label='Senyal reconstruïda')
plt.title('Senyal original-Senyal reconstruïda')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.show()