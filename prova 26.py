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

# Parameters for the circular plate
outer_radius = 0.2  # 20 cm
hole_radius = 0.0065  # 0.65 cm
thickness = 0.001  # 1 mm

# Material properties for brass (63% Cu and 37% Zn)
density = 8500  # density of brass in kg/m^3
E = 105e9  # Young's modulus for brass in Pascals
nu = 0.34  # Poisson's ratio for brass

# Flexural rigidity
D = E * thickness**3 / (12 * (1 - nu**2))

# Mass per unit area
mu = density * thickness

# Bessel function roots for mode calculation (clamped inner, free outer edge)
modes = 8  # Number of modes to calculate
jmn = jn_zeros(0, modes)

# Calculate natural frequencies
def natural_frequency(alpha, radius, D, mu):
    return (alpha / radius)**2 * np.sqrt(D / mu)

frequencies = [natural_frequency(alpha, outer_radius, D, mu) for alpha in jmn]

print("Natural Frequencies (Hz):")
for i, freq in enumerate(frequencies):
    print(f"Mode {i+1}: {freq:.2f} Hz")

# Generate mode shapes for visualization
size = 100  # Grid size for visualization
r = np.linspace(hole_radius, outer_radius, size)
theta = np.linspace(0, 2 * np.pi, size)
R, Theta = np.meshgrid(r, theta)

# Function to generate mode shape
def mode_shape(r, theta, alpha, radius):
    return jn(0, alpha * r / radius)

# Plot mode shapes
for i, alpha in enumerate(jmn):
    Z = mode_shape(R, Theta, alpha, outer_radius)
    X = R * np.cos(Theta)
    Y = R * np.sin(Theta)
    
    plt.figure(figsize=(8, 8))
    plt.contourf(X, Y, Z, cmap='RdBu_r')
    plt.colorbar(label='Displacement')
    plt.title(f'Mode Shape {i+1} for Alpha={alpha:.2f}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.show()

print("Mode Shape Equations:")
for i, (alpha, freq) in enumerate(zip(jmn, frequencies)):
    print(f"Mode Shape {i+1}: w_{i+1}(r, θ, t) = J_0({alpha:.2f} * r / {outer_radius:.2f}) * cos({freq:.2f} * t + φ)")

# Read audio file (recorded vibration signal)
sample_rate, data = wavfile.read('Sounds/recording5.wav')
N = len(data)

plt.figure(figsize=(10, 4))
plt.plot(data)
plt.title('Vibration Signal')
plt.xlabel('Time (samples)')
plt.ylabel('Amplitude')
plt.show()

# Perform FFT
yf = np.fft.rfft(data)
xf = np.fft.rfftfreq(N, 1 / sample_rate)

# Plot the FFT result
plt.figure(figsize=(12, 6))
plt.plot(xf, np.abs(yf))
plt.title('FFT of Plate Vibration')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Identify peaks corresponding to natural frequencies
peaks, properties = find_peaks(np.abs(yf), height=1000)
print("Identified Natural Frequencies (Hz):")
for peak in peaks:
    print(f"{xf[peak]:.2f}")

# Analytical frequencies (calculated previously)
analytical_frequencies = frequencies

# Identified experimental frequencies
experimental_frequencies = xf[peaks]
experimental_amplitudes = properties['peak_heights']

# Map experimental frequencies to analytical modes
mode_amplitudes = np.zeros_like(frequencies)

for exp_freq, amplitude in zip(experimental_frequencies, experimental_amplitudes):
    closest_idx = (np.abs(np.array(frequencies) - exp_freq)).argmin()
    mode_amplitudes[closest_idx] = amplitude

print("Identified Natural Frequencies and Amplitudes:")
for i, (freq, amp) in enumerate(zip(frequencies, mode_amplitudes)):
    print(f"Mode {i+1}: Frequency = {freq:.2f} Hz, Amplitude = {amp:.2f}")

# Generate mode shapes for visualization
size = 100  # Grid size for visualization
r = np.linspace(hole_radius, outer_radius, size)
theta = np.linspace(0, 2 * np.pi, size)
R, Theta = np.meshgrid(r, theta)

# Function to generate mode shape
def mode_shape(r, theta, alpha, radius):
    return jn(0, alpha * r / radius)

# Combined mode shape based on experimental amplitudes
def combined_mode_shape(r, theta, alphas, radius, amplitudes):
    result = np.zeros_like(r)
    for alpha, amplitude in zip(alphas, amplitudes):
        result += amplitude * jn(0, alpha * r / radius)
    return result

# Reconstruct the combined mode shape
Z_combined = combined_mode_shape(R, Theta, jmn, outer_radius, mode_amplitudes)
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# Plot the combined mode shape
plt.figure(figsize=(8, 8))
plt.contourf(X, Y, Z_combined, cmap='RdBu_r')
plt.colorbar(label='Displacement')
plt.title('Combined Mode Shape Due to Impact Near Outer Edge')
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal')
plt.show()

harmonics = []
for freq in frequencies:
    mode_harmonics = [freq * n for n in range(1, 4)]  # Consider up to 3rd harmonic
    harmonics.append(mode_harmonics)

# Plot FFT again with identified harmonics
plt.figure(figsize=(12, 6))
plt.plot(xf, np.abs(yf))
for mode_idx, mode_freqs in enumerate(harmonics):
    for freq in mode_freqs:
        plt.axvline(x=freq, color=f'C{mode_idx}', linestyle='--', label=f'Mode {mode_idx+1} Harmonic')
plt.title('FFT of Plate Vibration with Harmonics')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.legend()
plt.show()

# Define a function to estimate the damping ratio from the free decay signal
def estimate_damping(data, sample_rate):
    # Find peaks in the signal
    peaks, _ = find_peaks(data, height=np.max(data) * 0.1, distance=sample_rate // 10)
    peak_amplitudes = data[peaks]
    
    # Log-transform the peak amplitudes
    log_peak_amplitudes = np.log(peak_amplitudes)
    
    # Fit a linear decay to the log-transformed peak amplitudes
    def log_decay_func(t, log_A, zeta_omega_n):
        return log_A - zeta_omega_n * t
    
    # Time values for the peaks
    peak_times = peaks / sample_rate
    
    # Initial guess for the fit parameters: log(A), zeta_omega_n
    initial_log_A_guess = np.log(peak_amplitudes[0])
    initial_zeta_omega_n_guess = 0.01 * 2 * np.pi * frequencies[0]
    
    initial_guess = [initial_log_A_guess, initial_zeta_omega_n_guess]
    
    # Perform the curve fit
    popt, _ = curve_fit(log_decay_func, peak_times, log_peak_amplitudes, p0=initial_guess)
    
    log_A, zeta_omega_n = popt
    
    # Calculate the fitted parameters
    A = np.exp(log_A)
    zeta = zeta_omega_n / (2 * np.pi * frequencies[0])
    omega_n = zeta_omega_n / zeta
    
    fitted_log_decay = log_decay_func(peak_times, log_A, zeta_omega_n)
    fitted_decay = np.exp(fitted_log_decay)
    
    # Plot the decay envelope and the fitted model
    plt.figure(figsize=(10, 6))
    plt.plot(peak_times, peak_amplitudes, 'bo', label='Peak Amplitudes')
    plt.plot(peak_times, fitted_decay, 'r--', label='Fitted Decay Model')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Decay Envelope and Fitted Model')
    plt.legend()
    plt.show()

    return zeta, omega_n / (2 * np.pi), A, log_decay_func

# Estimate the damping ratio and natural frequency
zeta, fn, A, decay_model = estimate_damping(data, sample_rate)

print(f"Damping Ratio: {zeta:.4f}")
print(f"Natural Frequency: {fn:.2f} Hz")

# Compute the frequency response function (FRF)
f, Pxx = signal.welch(data, sample_rate, nperseg=1024)

# Plot the FRF
plt.figure(figsize=(10, 4))
plt.semilogy(f, Pxx)
plt.title('Frequency Response Function (FRF)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power/Frequency (dB/Hz)')
plt.show()

# Find the resonant peak
resonant_peak = np.argmax(Pxx)
f_resonant = f[resonant_peak]

# Measure the half-power bandwidth
half_power = Pxx[resonant_peak] / 2
indices = np.where(Pxx >= half_power)[0]
bandwidth = f[indices[-1]] - f[indices[0]]

# Calculate the damping ratio
zeta = bandwidth / (2 * f_resonant)
print(f"Damping Ratio (Half-Power Bandwidth Method): {zeta:.4f}")

T = N / sample_rate  # Total duration of the signal

# Time array
t = np.linspace(0, T, N)

# Fourier Series Coefficients Calculation
def a0(T, f):
    return (1 / T) * quad(f, 0, T)[0]

def an(T, f, n):
    return (2 / T) * quad(lambda t: f(t) * np.cos(2 * np.pi * n * t / T), 0, T)[0]

def bn(T, f, n):
    return (2 / T) * quad(lambda t: f(t) * np.sin(2 * np.pi * n * t / T), 0, T)[0]

# Define the signal function based on the audio data
def signal_function(t):
    index = int(t * sample_rate)
    if index >= len(data):
        return 0
    return data[index]

# Calculate Fourier coefficients
a0_value = a0(T, signal_function)
coefficients = [(an(T, signal_function, n), bn(T, signal_function, n)) for n in range(1, 6)]

print("Fourier Series Coefficients:")
print(f"a0: {a0_value:.4f}")
for n, (a_n, b_n) in enumerate(coefficients, start=1):
    print(f"a{n}: {a_n:.4f}, b{n}: {b_n:.4f}")

# Reconstruct the signal using Fourier series
def fourier_series(t, T, a0, coefficients):
    result = a0
    for n, (a_n, b_n) in enumerate(coefficients, start=1):
        result += a_n * np.cos(2 * np.pi * n * t / T) + b_n * np.sin(2 * np.pi * n * t / T)
    return result

# Reconstructed signal
f_t_reconstructed = fourier_series(t, T, a0_value, coefficients)

# Plot the reconstructed signal
plt.figure(figsize=(12, 6))
plt.plot(t, data, label='Original Signal')
plt.plot(t, f_t_reconstructed, '--', label='Reconstructed Signal')
plt.title('Original and Reconstructed Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.show()