import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn, jn_zeros
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from scipy.io import wavfile
from scipy.integrate import simps
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
import librosa
import librosa.display

# Load the audio file
audio_path = 'Sounds/recording5.wav'
y, sr = librosa.load(audio_path, sr=None)

# Compute the Short-Time Fourier Transform (STFT)
D = librosa.stft(y)
magnitude, phase = librosa.magphase(D)
frequencies = np.linspace(0, sr / 2, D.shape[0])
times = np.arange(D.shape[1]) * (len(y) / sr) / D.shape[1]

# Compute the log amplitude of the spectrogram
log_magnitude = librosa.amplitude_to_db(magnitude, ref=np.max)

# Plot the spectrogram
plt.figure(figsize=(10, 8))
librosa.display.specshow(log_magnitude, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Log-Amplitude Spectrogram')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.show()

# Average spectrum over time to find dominant frequencies
spectrum = np.mean(magnitude, axis=1)

# Plot the averaged spectrum
plt.figure(figsize=(10, 6))
plt.plot(frequencies, spectrum)
plt.title('Averaged Frequency Spectrum')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Identify the peaks in the spectrum using scipy's find_peaks
peaks, _ = find_peaks(spectrum, height=np.max(spectrum)*0.1, distance=20)

# Check if peaks are detected
if len(peaks) == 0:
    print("No peaks detected in the spectrum.")
else:
    print("Peaks detected at frequencies (Hz):")
    for peak in peaks:
        print(f"{frequencies[peak]:.2f}")

# Plot the frequency spectrum with identified peaks
plt.figure(figsize=(10, 6))
plt.plot(frequencies, spectrum)
plt.scatter(frequencies[peaks], spectrum[peaks], color='red')
plt.title('Frequency Spectrum with Identified Peaks')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Harmonics analysis function
def find_harmonics(frequencies, base_freq, tolerance=0.01):
    harmonics = []
    n = 1
    while True:
        harmonic_freq = base_freq * n
        idx = np.argmin(np.abs(frequencies - harmonic_freq))
        if np.abs(frequencies[idx] - harmonic_freq) / harmonic_freq < tolerance:
            harmonics.append(frequencies[idx])
        else:
            break
        n += 1
    return harmonics

# Example: Analyzing harmonics for each identified mode frequency
if len(peaks) > 0:
    print("Harmonics for identified peaks:")
    for base_freq in frequencies[peaks]:
        harmonic_series = find_harmonics(frequencies, base_freq)
        print(f"Harmonics for base frequency {base_freq:.2f} Hz: {harmonic_series}")
else:
    print("No peaks to analyze for harmonics.")

sample_rate, data = wavfile.read('Sounds/recording5.wav')
# Parameters for the circular plate
radi_plat = 0.2  # 20 cm
hole_radius = 0.0065  # 0.65 cm
thickness = 0.001  # 1 mm

# Material properties for brass (63% Cu and 37% Zn)
density = 8500  # density of brass in kg/m^3
E = 105e9  # Young's modulus for brass in Pascals
ν = 0.34  # Poisson's ratio for brass

# Flexural rigidity
D = E * thickness**3 / (12 * (1 - ν**2))
print(D)

# Mass per unit area
μ = density * thickness
print(μ)

# Speed of sound in air (m/s)
c = 343

# Air density (kg/m^3)
rho_air = 1.225

# Observation points (distance from the cymbal)
distance = 1.0  # 1 meter

# Bessel function roots for mode calculation (clamped inner, free outer edge)
modes = 30  # Number of modes to calculate
zeros_bessel = jn_zeros(0, modes)

# Calculate natural frequencies
def natural_frequency(alpha, radius, D, μ):
    return (alpha / radius)**2 * np.sqrt(D / μ) / (2 * np.pi)

frequencies = [natural_frequency(alpha, radi_plat, D, μ) for alpha in zeros_bessel]

print("Natural Frequencies (Hz):")
for i, freq in enumerate(frequencies):
    print(f"Mode {i+1}: {freq:.2f} Hz")

f = mggfhtd

# Generate mode shapes for visualization
size = 100  # Grid size for visualization
r = np.linspace(hole_radius, radi_plat, size)
theta = np.linspace(0, 2 * np.pi, size)
R, Theta = np.meshgrid(r, theta)

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, fftfreq

def estimate_damping_hpbw(data, sample_rate):
    # Perform FFT
    N = len(data)
    yf = fft(data)
    xf = fftfreq(N, 1 / sample_rate)[:N//2]  # Frequency axis
    
    # Find peaks in the FFT spectrum
    peaks, _ = find_peaks(np.abs(yf[:N//2]), height=np.max(np.abs(yf[:N//2])) * 0.1)
    peak_frequencies = xf[peaks]
    
    # Select the peak closest to the expected natural frequency
    fn = peak_frequencies[np.argmin(np.abs(peak_frequencies - frequencies[0]))]
    
    # Find half power points around the peak frequency
    peak_index = np.argmin(np.abs(xf - fn))
    peak_amplitude = np.abs(yf[peak_index])
    half_power_amplitude = peak_amplitude / np.sqrt(2)
    
    # Find half power bandwidth (HPBW)
    lower_index = np.argmin(np.abs(np.abs(yf[:peak_index]) - half_power_amplitude))
    upper_index = np.argmin(np.abs(np.abs(yf[peak_index:]) - half_power_amplitude)) + peak_index
    
    hpbw = xf[upper_index] - xf[lower_index]
    
    # Calculate damping ratio
    zeta = hpbw / fn
    
    return zeta

# Example usage with your data
zeta_hpbw = estimate_damping_hpbw(data, sample_rate)

print(f"Damping Ratio (Half Power Bandwidth Method): {zeta_hpbw:.4f}")


# Function to generate mode shape
def mode_shape(r, theta, alpha, radius):
    return jn(0, alpha * r / radius)

# Calculate sound pressure level (SPL)
def sound_pressure_level(Z, r, theta, frequency, distance, rho_air, c):
    omega = 2 * np.pi * frequency
    k = omega / c
    Z_dot = omega * Z
    integral = np.trapz(np.trapz(Z_dot * np.exp(-1j * k * r) / r, theta), r)
    p = rho_air * c * integral / (2 * np.pi * distance)
    epsilon = 1e-10  # Small value to avoid log of zero
    spl = 20 * np.log10(np.abs(np.real(p)) / 20e-6 + epsilon)  # Reference pressure in air: 20 µPa
    return spl

# Plot and calculate SPL
print("Mode Shape Equations and SPL:")
for i, (alpha, freq) in enumerate(zip(zeros_bessel, frequencies)):
    Z = mode_shape(R, Theta, alpha, radi_plat)
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)

    # 3D Plot mode shape
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='RdBu_r', edgecolor='k')
    ax.set_title(f'Mode Shape {i+1} for Alpha={alpha:.2f}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Displacement')
    #plt.show()

    # Calculate SPL
    spl = sound_pressure_level(Z, R, Theta, freq, distance, rho_air, c)
    
    if np.iscomplexobj(spl):
        spl_value = np.abs(spl)
    else:
        spl_value = spl
    
    #print(spl_value)
    #print(f"Mode Shape {i+1}: w_{i+1}(r, θ, t) = J_0({alpha:.2f} * r / {radi_plat:.2f}) * cos({2 * np.pi * freq:.2f} * t + φ)")
    #print(f"Mode {i+1} SPL at {distance} m: {spl_value[0]:.2f} dB")

# Kinetic energy density
def kinetic_energy_density(Z, omega, mu):
    Z_dot = omega * Z
    return 0.5 * mu * Z_dot**2

# Potential energy density using numerical integration (Simpson's rule)
def potential_energy_density(Z, D, nu, R, Theta):
    w_rr = np.gradient(np.gradient(Z, axis=0), axis=0)
    mask = np.gradient(R[:, 0], axis=0)[:, np.newaxis]
    w_r = np.gradient(Z, axis=0) / R[:, np.newaxis]
    w_tt = np.gradient(np.gradient(Z, axis=1), axis=1) / R[:, np.newaxis]**2
    w_rt = np.gradient(np.gradient(Z, axis=0), axis=1) / R[:, np.newaxis]

    term1 = (w_rr + w_r + w_tt)**2
    term2 = 2 * (1 - nu) * (w_r * w_tt - w_rt**2)
    pe_density = 0.5 * D * (term1 + term2)

    return pe_density

# Total energy density using numerical integration
def total_energy_density(Z, omega, mu, D, nu, R, Theta):
    ke_density = kinetic_energy_density(Z, omega, mu)
    pe_density = potential_energy_density(Z, D, nu, R, Theta)
    return ke_density + pe_density

# Calculate and plot energy densities
print("\nEnergy Densities:")
for i, (alpha, freq) in enumerate(zip(zeros_bessel, frequencies)):
    Z = mode_shape(R, Theta, alpha, radi_plat)
    omega = 2 * np.pi * freq

    total_energy_density_mode = total_energy_density(Z, omega, μ, D, ν, R, Theta)

    # Integrate over the surface to get the total energy
    total_energy = simps(simps(total_energy_density_mode * R[:, 0], theta), r)

    print(f"Mode {i+1} Total Energy: {total_energy[0]:.6e} Joules")