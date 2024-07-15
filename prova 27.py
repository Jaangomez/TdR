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
import pywt

#Forma del plat
radi_plat = 0.2  
radi_forat = 0.0065 
gruix_plat = 0.001  

#Propietats del plat
ρ = 8500  #densitat (kg/m^3)
E = 105e9  #Mòdul de Young (Pa)
ν = 0.34  #Coeficient de Poissoin

#Rigidesa de flexió
D = E * gruix_plat**3 / (12 * (1 - ν**2))

#Massa que hi ha a cada unitat d'àrea
μ = ρ * gruix_plat

#Funció de Bessel
modes = 15
modes_m = 5
modes_n_total = 3
modes_m_total= 4
#Bessel per a m o n
zeros_bessel = jn_zeros(0, modes)

#Bessel per a m i n
zeros_bessel_mn = np.zeros((modes_n_total, modes_m_total))
for n in range(modes_n_total):
    zeros_bessel_mn[n, :] = jn_zeros(n, modes_m_total)

#Càlcul freq natural per a n o m
def freqüència_natural(α, radi, D, μ):
    return (α / radi)**2 * np.sqrt(D / μ) / (2 * np.pi)

frequencies = [freqüència_natural(α, radi_plat, D, μ) for α in zeros_bessel]

print("Freqüències Naturals per m o n:")
for i, freq in enumerate(frequencies):
    print(f"Mode {i+1}: {freq:.2f} Hz")

#Càlcul freq natural per a n i m 
def freqüència_natural_mn(n, m, radi, D, μ):
    α = zeros_bessel_mn[n, m]
    return (α / radi)**2 * np.sqrt(D / μ) / (2 * np.pi)

frequencies_mn = np.zeros((modes_n_total, modes_m_total))
for n in range(modes_n_total):
    for m in range(modes_m_total):
        frequencies_mn[n, m] = freqüència_natural_mn(n, m, radi_plat, D, μ)

print("Freqüències Naturals per m i n:")
for n in range(modes_n_total):
    for m in range(modes_m_total):
        print(f"Mode ({n+1}, {m+1}): {frequencies_mn[n, m]:.2f} Hz")

#Mides dels modes i representació amb 0 diàmetres nodals
mida = 100
r = np.linspace(radi_forat, radi_plat, mida)
θ = np.linspace(0, 2 * np.pi, mida)
R, θ = np.meshgrid(r, θ)

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
plt.plot(temps, senyal)
plt.title('Senyal de vibració')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitud')
#plt.show()

def increment(absft):
    amplituds = []
    step = 251
    x = 251
    while  step <= len(absft):
        maxim = max(absft[(step-251):step])
        index = np.where(absft==maxim)[0][0]
        frequencia = ft_freq[index]
        amplituds.append (maxim)
        step += 250
        x += 250 
    amplituds.sort()
    amplituds_màximes = amplituds[-10:len(amplituds)]
    dicc = {}
    for i in amplituds_màximes:
        indexs = searchindex (i, absft)
        dicc [i] = ft_freq[indexs]
        
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
    print (f'Proporicó general: {proporció_general}%')
    print (f'Proporció dins els harmònics màxims: {proporció_dins_harmònics_màxims}%')

plt.rcParams ['figure.figsize'] = (15,8)
plt.plot (ft_freq, absft)
plt.title ('FFT vibació del plat')
plt.xlabel ('Freqüència (Hz)')
plt.ylabel ('Amplitude |X(Freq)|')
plt.plot (array_frequencies, array_amplituds, 'o', color='k')
for x, y in zip(array_frequencies, array_amplituds):
    plt.annotate(text=(round(x, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
            verticalalignment = 'bottom', fontsize=8)
        
plt.tight_layout ()
#plt.show()

#Màxims = Possibles freqüències naturals
màxims, propietats = find_peaks(absft, height=np.max(absft) * 0.1)
print("Possibles freqüències naturals (experimentals):")
for max in màxims:
    print(f"{ft_freq[max]:.2f} Hz")

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

mode_amplituds_mn = np.zeros_like(frequencies_mn)
for freq_exp, amplitud_mn in zip(freqüències_experimentals, amplituds_experimentals):
    for n in range (modes_n_total):
        for m in range (modes_m_total):
            frequency_diff = np.abs(frequencies_mn[n, m] - freq_exp)
            if frequency_diff < 50: 
                mode_amplituds_mn[n ,m] = amplitud_mn

print("Freqüències naturals i amplituds (n, m):")
for n in range(modes_n_total):
    for m in range(modes_m_total):
        print(f"Mode ({n+1}, {m+1}): Freqüència = {frequencies_mn[n, m]:.2f} Hz, Amplitud = {mode_amplituds_mn[n, m]:.2f}")

#waves.read no ho llegeix com a punt flotant, així que s'ha de tornar a introduir amb librosa
senyal2, sr = librosa.load('Sounds/recording5.wav')

#Short-Time Fourier Transform (STFT)
D = librosa.stft(senyal2)
amplitud_stft, fase_stft = librosa.magphase(D)
stft_freq = np.linspace(0, sr / 2, D.shape[0])
temps2 = np.arange(D.shape[1]) * (len_senyal / sr) / D.shape[1]

#Passar a decibels
db_amplitud = librosa.amplitude_to_db(amplitud_stft, ref=np.max)

plt.figure(figsize=(10, 8))
librosa.display.specshow(db_amplitud, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('STFT so del plat')
plt.xlabel('Temps (s)')
plt.ylabel('Freqüència (Hz)')
plt.show()

if len(màxims) == 0:
    print("Sense màxims")
else:
    print("Màxims per freqüències (Hz):")
    try: 
        for max in màxims:
            print(f"{stft_freq[max]:.2f}")
    except:
        IndexError

#Aproximació coeficient d'amortiment
def amortiment():

    index_proper1 = np.array([np.argmin(np.abs(frequencies - freq_exp)) for freq_exp in freqüències_experimentals])
    freq_propera = np.array(frequencies)[index_proper1]

    freq_natural_aprox = freq_propera[0]
    index_proper2 = np.argmin(np.abs(ft_freq - freq_natural_aprox))
    max_amplitud = absft[index_proper2]
    amplitud_meitat_intensitat = max_amplitud / np.sqrt(2)

    #Costat esquerra
    for i in range(index_proper2, -1, -1):
        if absft[i] <= amplitud_meitat_intensitat:
            banda_meitat_intensitat_esquerra = ft_freq[i]
            break

    #Costat dret
    for i in range(index_proper2, len(absft)):
        if absft[i] <= amplitud_meitat_intensitat:
            banda_meitat_intensitat_dreta = ft_freq[i]
            break

    #HPBW
    banda_meitat_intesitat = banda_meitat_intensitat_dreta - banda_meitat_intensitat_esquerra

    #Amortiment
    coeficient_amortiment = banda_meitat_intesitat / (2 * freq_natural_aprox)

    return coeficient_amortiment

print(f"Coeficient d'amortiment: {amortiment():.4f}")

#FRF
array_freqs, espectre_potència = signal.welch(senyal, sr, nperseg=1024)

plt.figure(figsize=(10, 4))
plt.semilogy(array_freqs, espectre_potència)
plt.title('FRF')
plt.xlabel('Freqüència (Hz)')
plt.ylabel('Intensitat/Freqüència (dB/Hz)')
plt.show()

max_ressonant = np.argmax(espectre_potència)
freq_ressonant = array_freqs[max_ressonant]

meitat_intesitat = espectre_potència[max_ressonant] / 2
indexs = np.where(espectre_potència >= meitat_intesitat)[0]
banda_meitat_intensitat = array_freqs[indexs[-1]] - array_freqs[indexs[0]]

#Càlcul coeficient d'amortiment
coeficient_amortiment = banda_meitat_intensitat / (2 * freq_ressonant)
print(f"Amortiment 2 càlcul: {coeficient_amortiment:.4f}")

#Càlcul sèrie de Fourier
def a0(duració, funció_senyal):
    return (2 / duració) * quad(funció_senyal, 0, duració)[0]


def an(duració, funció_senyal, n):
    return (2 / duració) * quad(lambda temps: funció_senyal(temps) * np.cos(2 * np.pi * n * temps / duració), 0, duració)[0]


def bn(duració, funció_senyal, n):
    return (2 / duració) * quad(lambda temps: funció_senyal(temps) * np.sin(2 * np.pi * n * temps / duració), 0, duració)[0]

def funció_senyal(temps):
    index = int(temps * sr)
    return senyal[index]

#Coeficients de Fourier
valor_a0 = a0(duració, funció_senyal)
coeficients = [(an(duració, funció_senyal, n), bn(duració, funció_senyal, n)) for n in range(1, 20)]

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

senyal_reconstruïda = sèrie_fourier(temps, duració, valor_a0, coeficients)

plt.figure(figsize=(12, 6))
plt.plot(temps, senyal, label='Senyal original')
plt.plot(temps, senyal_reconstruïda, '--', label='Senyal reconstruïda')
plt.title('Senyal original-Senyal reconstruïda')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitud')
plt.legend()
plt.show()