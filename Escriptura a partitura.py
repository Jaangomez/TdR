import librosa
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import lilypond
import ly.lex
import ly
from music21 import stream, note, environment
import subprocess
import ly
import os
import mingus.extra.lilypond as LilyPond
from mingus.containers import Bar

arxiu = 'Sounds/melodia piano completa.wav'
y, sr = librosa.load(arxiu)

duration = librosa.get_duration(y=y, sr=sr)
print (duration)
frame_notes_en_el_temps = librosa.onset.onset_detect(y=y, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
print(frame_notes_en_el_temps) 
temps_notes = librosa.frames_to_time(frame_notes_en_el_temps)
print(temps_notes)

frame = 2048
salt = 512
frames_arxiu = librosa.util.frame(y, frame_length=frame, hop_length=salt)

fft_frames = np.fft.fft(frames_arxiu, axis = 0)
fft_freq = np.fft.fftfreq(len(fft_frames), d=1./sr)
amplitud = np.abs(fft_frames)
melodia = []
for i in (temps_notes):
    index = int(i*sr/salt)
    temps = amplitud[:,index]
    freqindex = np.argmax(temps)
    freq = np.abs(fft_freq[freqindex])
    melodia.append(freq)

print (melodia)

melodia_wth_0 = [freq for freq in melodia if freq != 0]
arr_notes = []
for freq in melodia_wth_0:
    nota = librosa.hz_to_note(freq)
    arr_notes.append(nota)

print (arr_notes)

#f0, voice_flag, _ = librosa.pyin(y, fmin =librosa.note_to_hz('C2'), fmax = librosa.note_to_hz("C7"), sr= sr)

#onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)

def trobar_nota (frq):
    if 127.143 <= frq and frq < 134.702:
        return "C3"
    elif 134.703 <= frq  and frq <= 142.7115:
        return "C#3"
    elif 142.7116 <= frq and frq <= 151.1975:
        return "D3"
    elif 151.1976 <= frq and frq <= 160.1885:
        return "D#3"
    elif 160.1886 <= frq < 169.714:
        return "E3"
    elif 169.715 <= frq < 179.8055:
        return "F3"
    elif 179.8056 <= frq < 190.4975:
        return "F#3"
    elif 190.4976 <= frq < 201.825:
        return "G3"
    elif 202.826 <= frq < 213.826:
        return "G#3"
    elif 213.827 <= frq < 226.941:
        return "A3"
    elif 226.942 <= frq < 240.412:
        return "A#3"
    elif 240.413 <= frq < 254.284:
        return "B3"
    elif 254.284 <= frq < 269.4045:
        return "C4"
    elif 269.4046 <= frq < 285.424:
        return "C#4"
    elif 285.425 <= frq < 302.396:
        return "D4" 
    elif 302.397 <= frq < 320.3775:
        return "D#4"
    elif 320.3776 <= frq < 339.428:
        return "E4"
    elif 339.429 <= frq < 359.611:
        return "F4"
    elif 359.612 <= frq < 380.9945:
        return "F#4"
    elif 380.9946 <= frq < 403.65:
        return "G4"
    elif 403.66 <= frq < 427.6525:
        return "G#4"
    elif 427.6526 <= frq < 453.082:
        return "A4"
    elif 453.083 <= frq < 479.7985:
        return "A#4"
    elif 479.7986 <= frq < 508.567:
        return "B4"
    elif 508.568 <= frq < 538.808:
        return "C5"
    elif 538.809 <= frq < 570.8515:
        return "C#5"
    elif 570.8516 <= frq < 604.796:
        return "D5"
    elif 604.797 <= frq < 640.7545:
        return "D#5"
    elif 640.7546 <= frq < 678.8555:
        return "E5"
    elif 678.8556 <= frq < 719.2225:
        return "F5"
    elif 719.2226 <= frq < 760.99:
        return "F#5"
    elif 760.991 <= frq < 811.8:
        return "G5"
    elif 811.801 <= frq < 859.2085:
        return "G#5"
    elif 859.2086 <= frq < 906.568:
        return "A5"
    elif 906.569 <= frq < 960.0475:
        return "A#5"
    elif 960.0476 <= frq < 1017.1735:
        return "B5"
    elif 1017.1736 <= frq < 1077.615:
        return "C6"
    elif 1077.616 <= frq < 1141.695:
        return "C#6"
    elif 1141.695 <= frq < 1209.585:
        return "D6"
    elif 1209.586 <= frq < 1281.51:
        return "D#6"
    elif 1281.511 <= frq < 1358.71:
        return "E6"
    elif 1358.711 <= frq < 1439.445:
        return "F6"
    else:
        return "Nota no identificada"
    
#def trobar_nota (frq):
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

#lilypond_code = ""
#for frame in onset_frames:
    if voice_flag[frame]:
        pitch = trobar_nota(f0[frame])
        lilypond_code += f"{pitch}"

#lilypond_code2 = []
#for frame in onset_frames:
    if voice_flag[frame]:
        pitch = trobar_nota(f0[frame])
        lilypond_code2.append(pitch)

#print ("LilyPond code")
#print (lilypond_code)
#print (lilypond_code2)
#print (len(lilypond_code2))

folder_path = "C:/Users/JoanGómezPujol/Desktop/TR/Python/lilypond-2.24.3/bin"
file_path = folder_path + "/output.pdf"

lilypond_folder = "C:/Users/JoanGómezPujol/Desktop/TR/Python/lilypond-2.24.3/bin/lilypond.exe"

environment.set('lilypondPath', lilypond_folder)
# Create a Stream object to represent the music score
score = stream.Score()

# Create a Part object to contain the musical notes
part = stream.Part()

# Add some musical notes to the Part
#notes = [note.Note("C4"), note.Note("D4"), note.Note("E4"), note.Note("F4")]
#for n in notes:
    #part.append(n)

#if i <= len(lilypond_code2):
    #notes2 = [note.Note(f"{lilypond_code2[i]}")]
    #i+=1

def reemplaçar_alteracions (sq_notes):
    sq_notes = sq_notes.replace("♯", "#")
    sq_notes = sq_notes.replace("♭", "b")
    return sq_notes

arr_notes = [reemplaçar_alteracions(n) for n in arr_notes]

i=0

while i <= len(arr_notes):
    try:
        notes = [note.Note(f"{arr_notes[i]}")]
        part.append(notes)
        i+=1
    except IndexError:
        break

# Add the Part to the Score
score.append(part)

# Specify the full path to the folder where LilyPond is installed

lilypond_folder2 = "C:/Users/JoanGómezPujol/Desktop/TR/Python/lilypond-2.24.3/bin"

# Write the Score to a PDF file in the specified folder
pdf_path = f"{lilypond_folder2}/output4"
score.write('lily.pdf', fp=pdf_path)

print("PDF generated successfully.")