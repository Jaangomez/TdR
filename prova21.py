import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq
from scipy.signal import find_peaks
from astroquery.sdss import SDSS
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

# Define the coordinates for querying SDSS
coords = SkyCoord('05h06m36.6s +09d29m51s', unit=(u.hourangle, u.deg))

# Query SDSS for spectra at the given coordinates with a small search radius
xid = SDSS.query_region(coords, spectro=True, radius=2*u.arcsec)

# Extract plate, mjd, and fiberID from the query result
plate = xid[0]['plate']
mjd = xid[0]['mjd']
fiberID = xid[0]['fiberID']

# Fetch the spectra using plate, mjd, and fiberID
spec = SDSS.get_spectra(plate=plate, mjd=mjd, fiberID=fiberID)[0]

# Read the FITS file from the SDSS query result
hdulist = spec[1].data
wavelengths = 10**hdulist['loglam']  # Wavelengths in Angstroms
flux = hdulist['flux']  # Flux values

# Add noise to simulate a more realistic scenario
np.random.seed(0)
noise = 0.1 * np.random.normal(size=flux.size)
noisy_flux = flux + noise

# Perform Fourier transform
spectrum_fft = fft(noisy_flux)
frequencies = fftfreq(wavelengths.size, wavelengths[1] - wavelengths[0])

# Apply inverse FFT to filter noise (high pass filter example)
spectrum_fft_filtered = spectrum_fft.copy()
spectrum_fft_filtered[np.abs(frequencies) < 0.001] = 0  # Remove low-frequency noise
filtered_spectrum = np.real(ifft(spectrum_fft_filtered))

# Find peaks in the filtered spectrum
peaks, _ = find_peaks(filtered_spectrum, height=0.1)

# Plot original and filtered spectrum
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(wavelengths, noisy_flux, label='Noisy Spectrum')
plt.plot(wavelengths, flux, 'r--', label='Original Spectrum')
plt.xlabel('Wavelength (Angstrom)')
plt.ylabel('Flux')
plt.title('Noisy Spectrum')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(wavelengths, filtered_spectrum, label='Filtered Spectrum')
plt.plot(wavelengths[peaks], filtered_spectrum[peaks], 'x', label='Detected Peaks')
plt.xlabel('Wavelength (Angstrom)')
plt.ylabel('Flux')
plt.title('Filtered Spectrum and Detected Peaks')
plt.legend()

plt.tight_layout()
plt.show()

# Print the wavelengths of the detected peaks
detected_lines = wavelengths[peaks]
print("Detected spectral lines (Angstrom):", detected_lines)