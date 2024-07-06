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
ν = 0.34  #Coeficient de Poissoin

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
    plt.title(f'Forma del mode {i+1} per α={α:.2f}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.show()
    plt.savefig(f'Forma del mode {i+1} 2D')

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='RdBu_r', edgecolor='k')
    ax.set_title(f'Forma del mode {i+1} per α={α:.2f}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Desplaçament')
    plt.savefig(f'Forma del mode {i+1} 3D')
    
print("Equacions de les formes de mode:")
for i, (α, freq) in enumerate(zip(zeros_bessel, frequencies)):
    print(f"Forma del mode {i+1}: w_{i+1}(r, θ, t) = J_0({α:.2f} * r / {radi_plat:.2f}) * cos({freq:.2f} * t + φ)")