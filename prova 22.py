import numpy as np
import matplotlib.pyplot as plt
from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.visualization import astropy_mpl_style, ZScaleInterval
from scipy.fft import fft, fftfreq

# Define the coordinates (example coordinates)
coords = SkyCoord(ra=2.02344596573482, dec=14.8398237551311, unit=(u.deg, u.deg))  # Coordinates in degrees

# Query the SDSS for object information at the given coordinates
try:
    xid = SDSS.query_region(coords, radius=2*u.arcsec, spectro=True)
    if xid is None or len(xid) == 0:
        raise ValueError("No object found for the given coordinates")

    # Display the available fields in the query result
    print("Available fields:", xid.colnames)
    print(xid)

    # Retrieve detailed information for the first matched object
    objid = xid[0]['objid']
    specobjid = xid[0]['specobjid']
    
    # Handle missing 'class' and 'subclass' fields
    obj_class = xid[0]['class'] if 'class' in xid.colnames else 'Unknown'
    sub_class = xid[0]['subclass'] if 'subclass' in xid.colnames else 'Unknown'

    print(f"Object ID: {objid}")
    print(f"Spectroscopic Object ID: {specobjid}")
    print(f"Object Class: {obj_class}")
    print(f"Subclass: {sub_class}")

    # Retrieve an image of the object from SDSS
    imsize = 0.02  # Image size in degrees
    cutout = SDSS.get_images(coordinates=coords, radius=imsize*u.deg, band='r')[0]

    # Plot the image
    plt.style.use(astropy_mpl_style)

    interval = ZScaleInterval()
    vmin, vmax = interval.get_limits(cutout[0].data)

    plt.figure(figsize=(8, 8))
    plt.imshow(cutout[0].data, cmap='gray', origin='lower', vmin=vmin, vmax=vmax)
    plt.colorbar()
    plt.title(f'SDSS Image of Object at {coords.to_string("hmsdms")}\nClass: {obj_class}, Subclass: {sub_class}')
    plt.xlabel('RA')
    plt.ylabel('Dec')
    plt.show()

    # Query the SDSS for spectral data at the given coordinates
    sp = SDSS.get_spectra(matches=xid)
    
    if sp is None or len(sp) == 0:
        raise ValueError("No spectral data found for the object")

    # Open the spectrum data
    spec_data = sp[0][1].data

    # Extract wavelength and flux
    flux = spec_data['flux']
    loglam = spec_data['loglam']
    wavelength = 10**loglam  # Convert log(wavelength) to wavelength

    # Plot the spectrum
    plt.figure(figsize=(12, 6))
    plt.plot(wavelength, flux, color='black')
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux')
    plt.title('Spectrum of Object at {} {}'.format(coords.ra.to_string(u.hour, sep=':'), coords.dec.to_string(u.deg, sep=':')))
    plt.grid(True)
    plt.show()

    # Apply Fourier Transform to the flux data
    N = len(flux)
    T = wavelength[1] - wavelength[0]  # Assuming uniform wavelength spacing
    yf = fft(flux)
    xf = fftfreq(N, T)[:N//2]

    # Plot the Fourier Transform result
    plt.figure(figsize=(12, 6))
    plt.plot(xf, 2.0/N * np.abs(yf[:N//2]), color='blue')
    plt.xlabel('Frequency (1/Å)')
    plt.ylabel('Amplitude')
    plt.title('Fourier Transform of the Flux')
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")