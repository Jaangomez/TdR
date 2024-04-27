import librosa
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import lilypond
import ly
from music21 import stream, note
import subprocess
import ly
import os
import mingus.extra.lilypond as LilyPond
from mingus.containers import Bar

arxiu = 'idk.wav'
y, sr = librosa.load(arxiu)

hop_length = 512

f0, voice_flag, _ = librosa.pyin(y, fmin =librosa.note_to_hz('C2'), fmax = librosa.note_to_hz("C7"), sr= sr)

onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)

def trobar_nota (frq):
    if 127.143 <= frq and frq < 134.702:
        return "c"
    elif 134.703 <= frq  and frq <= 142.7115:
        return "cis"
    elif 142.7116 <= frq and frq <= 151.1975:
        return "d"
    elif 151.1976 <= frq and frq <= 160.1885:
        return "dis"
    elif 160.1886 <= frq < 169.714:
        return "e"
    elif 169.715 <= frq < 179.8055:
        return "f"
    elif 179.8056 <= frq < 190.4975:
        return "fis"
    elif 190.4976 <= frq < 201.825:
        return "g"
    elif 202.826 <= frq < 213.826:
        return "gis"
    elif 213.827 <= frq < 226.941:
        return "a"
    elif 226.942 <= frq < 240.412:
        return "ais"
    elif 240.413 <= frq < 254.284:
        return "b"
    elif 254.284 <= frq < 269.4045:
        return "c'"
    elif 269.4046 <= frq < 285.424:
        return "cis'"
    elif 285.425 <= frq < 302.396:
        return "d" 
    elif 302.397 <= frq < 320.3775:
        return "dis'"
    elif 320.3776 <= frq < 339.428:
        return "e'"
    elif 339.429 <= frq < 359.611:
        return "f'"
    elif 359.612 <= frq < 380.9945:
        return "fis'"
    elif 380.9946 <= frq < 403.65:
        return "g"
    elif 403.66 <= frq < 427.6525:
        return "gis'"
    elif 427.6526 <= frq < 453.082:
        return "a'"
    elif 453.083 <= frq < 479.7985:
        return "ais'"
    elif 479.7986 <= frq < 508.567:
        return "b'"
    elif 508.568 <= frq < 538.808:
        return "c''"
    elif 538.809 <= frq < 570.8515:
        return "cis''"
    elif 570.8516 <= frq < 604.796:
        return "d''"
    elif 604.797 <= frq < 640.7545:
        return "dis''"
    elif 640.7546 <= frq < 678.8555:
        return "e''"
    elif 678.8556 <= frq < 719.2225:
        return "f''"
    elif 719.2226 <= frq < 760.99:
        return "fis''"
    elif 760.991 <= frq < 811.8:
        return "g''"
    elif 811.801 <= frq < 859.2085:
        return "gis''"
    elif 859.2086 <= frq < 906.568:
        return "a''"
    elif 906.569 <= frq < 960.0475:
        return "ais''"
    elif 960.0476 <= frq < 1017.1735:
        return "b''"
    elif 1017.1736 <= frq < 1077.615:
        return "c'''"
    elif 1077.616 <= frq < 1141.695:
        return "cis'''"
    elif 1141.695 <= frq < 1209.585:
        return "d'''"
    elif 1209.586 <= frq < 1281.51:
        return "dis'''"
    elif 1281.511 <= frq < 1358.71:
        return "e'''"
    elif 1358.711 <= frq < 1439.445:
        return "f'''"
    else:
        return "Nota no identificada"

lilypond_code = ""
for frame in onset_frames:
    if voice_flag[frame]:
        pitch = trobar_nota(f0[frame])
        lilypond_code += f"{pitch}"

print ("LilyPond code")
print (lilypond_code)


lilypond_code2 = f"""
\\version "2.24.3"
{
    lilypond_code
}
"""
