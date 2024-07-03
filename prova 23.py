import matplotlib.pyplot as plt
from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.io import fits

# Define the coordinates (example coordinates)
coords = SkyCoord(ra=72.9849512083396, dec=0.907273814191271, unit=(u.deg, u.deg))

# Query the SDSS for spectral data at the given coordinates
try:
    xid = SDSS.query_region(coords, radius=2*u.arcsec, spectro=True)
    if xid is None or len(xid) == 0:
        raise ValueError("No object found for the given coordinates")

    # Get the spectrum
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

    # Identify key spectral lines for common elements
    lines = {
        'Hydrogen alpha (Hα)': [6563],
        'Hydrogen beta (Hβ)': [4861],
        'Hydrogen gamma (Hγ)': [4340],
        'Hydrogen delta (Hδ)': [4102],
        'Helium I': [4471],
        'Helium II': [4686],
        'Oxygen III (OIII)': [5007],
        'Oxygen II (OII)': [3727],
        'Carbon II (CII)': [1335],
        'Carbon III (CIII)': [1909],
        'Carbon IV (CIV)': [1549],
        'Nitrogen II (NII)': [6584],
        'Nitrogen III (NIII)': [1750],
        'Nitrogen IV (NIV)': [1486],
        'Sodium D': [5895.92, 5889.95],
        'Magnesium I (MgI)': [2852],
        'Magnesium II (MgII)': [2803, 2796],
        'Calcium II (CaII) K': [3934],
        'Calcium II (CaII) H': [3968],
        'Calcium I (CaI)': [4227],
        'Iron I (FeI)': [3720, 4045, 4383, 4958],
        'Iron II (FeII)': [2344, 2383, 2586, 2599],
        'Silicon II (SiII)': [1260, 1304, 1527, 1808],
        'Silicon III (SiIII)': [1206],
        'Silicon IV (SiIV)': [1393, 1402],
        'Sulfur II (SII)': [6716, 6731],
        'Sulfur III (SIII)': [9069, 9532],
        'Neon III (NeIII)': [3869, 3968],
        'Neon IV (NeIV)': [4720],
        'Aluminum I (AlI)': [3944, 3961],
        'Aluminum II (AlII)': [1670],
        'Argon II (ArII)': [4806, 4657],
        'Chromium I (CrI)': [4254, 4274, 4290],
        'Chromium II (CrII)': [2056, 2062, 2066]
    }

    # Mark spectral lines on the plot
    for element, waves in lines.items():
        for wave in waves:
            plt.axvline(x=wave, color='red', linestyle='--')
            # Annotate the element name near the spectral line
            plt.text(wave, max(flux) * 0.9, element, rotation=90, verticalalignment='bottom', fontsize=8, color='blue')

    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")

    import matplotlib.pyplot as plt
from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.io import fits

# Define the coordinates (example coordinates)
coords = SkyCoord(ra=2.0235, dec=14.8398, unit=(u.deg, u.deg))

# Query the SDSS for spectral data at the given coordinates
try:
    xid = SDSS.query_region(coords, radius=2*u.arcsec, spectro=True)
    if xid is None or len(xid) == 0:
        raise ValueError("No object found for the given coordinates")

    # Get the spectrum
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

    # Identify key spectral lines for common elements
    lines = {
        'Hydrogen alpha (Hα)': [6563],
        'Hydrogen beta (Hβ)': [4861],
        'Hydrogen gamma (Hγ)': [4340],
        'Hydrogen delta (Hδ)': [4102],
        'Helium I': [4471],
        'Helium II': [4686],
        'Oxygen III (OIII)': [5007],
        'Oxygen II (OII)': [3727],
        'Carbon II (CII)': [1335],
        'Carbon III (CIII)': [1909],
        'Carbon IV (CIV)': [1549],
        'Nitrogen II (NII)': [6584],
        'Nitrogen III (NIII)': [1750],
        'Nitrogen IV (NIV)': [1486],
        'Sodium D': [5895.92, 5889.95],
        'Magnesium I (MgI)': [2852],
        'Magnesium II (MgII)': [2803, 2796],
        'Calcium II (CaII) K': [3934],
        'Calcium II (CaII) H': [3968],
        'Calcium I (CaI)': [4227],
        'Iron I (FeI)': [3720, 4045, 4383, 4958],
        'Iron II (FeII)': [2344, 2383, 2586, 2599],
        'Silicon II (SiII)': [1260, 1304, 1527, 1808],
        'Silicon III (SiIII)': [1206],
        'Silicon IV (SiIV)': [1393, 1402],
        'Sulfur II (SII)': [6716, 6731],
        'Sulfur III (SIII)': [9069, 9532],
        'Neon III (NeIII)': [3869, 3968],
        'Neon IV (NeIV)': [4720],
        'Aluminum I (AlI)': [3944, 3961],
        'Aluminum II (AlII)': [1670],
        'Argon II (ArII)': [4806, 4657],
        'Chromium I (CrI)': [4254, 4274, 4290],
        'Chromium II (CrII)': [2056, 2062, 2066]
    }

    # Mark spectral lines on the plot
    plt.figure(figsize=(12, 6))
    plt.plot(wavelength, flux, color='black')
    for element, waves in lines.items():
        for wave in waves:
            plt.axvline(x=wave, color='red', linestyle='--', label=f'{element} ({wave} Å)')
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux')
    plt.title('Spectrum of Object with Key Spectral Lines')
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.grid(True)
    plt.show()

except Exception as e:
    print(f"An error occurred: {e}")
