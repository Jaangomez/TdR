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
import scipy.io.wavfile as waves


def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

arxiu = 'Sounds/melodia piano completa (bé).wav'
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

durations = []
durations.append(duration)
temps_notes2 = np.concatenate((temps_notes, durations))

i=0
while i <= len(temps_notes2):
    if (i==0):
        print ('iep, encara no')
        i+=1
    else:
        t_final = temps_notes2[i] - 0.05
        t_inicial = temps_notes2[i-1] + 0.05
        
        arxius_sortida = f'melo piano{i}.wav'

        mostra, so = waves.read(arxiu)

        i_inici = int(t_inicial*mostra)
        i_final = int(t_final*mostra)
        porcio = so[i_inici:i_final]
        duracio = len(porcio)/mostra

        waves.write(arxius_sortida, mostra, porcio)
        print('arxiu creat: ', arxius_sortida)
        i+=1
    if (i==len(temps_notes2)):
        break

dir = "C:/Users/JoanGómezPujol/Desktop/TR/Python"
contingut = os.listdir(dir)
audios = []
for fitxer in contingut:
    if os.path.isfile(os.path.join(dir, fitxer)) and fitxer.endswith('.wav'):
        audios.append(fitxer)

def sort_file_names(arxiu):
   
    part_numèrica = ''.join(filter(str.isdigit, arxiu))
    
    return int(part_numèrica)


arxius_ordenats = sorted(audios, key=sort_file_names)


audios_definitius = []
for arxiu in arxius_ordenats:
    audios_definitius.append(arxiu)

print(audios_definitius)

freqs_melodia = []
freqs_descartades = []
audios_descartats = []
for arxiu in audios_definitius:
    file = arxiu
    mostra, senyal = waves.read(file)

    sampFreq = 44110
    tamany = np.shape (senyal)

    if  len(senyal) == 0:
        sampf = 1000  
        duració = 1      

        
        t = np.linspace(0, duració, duració*sampf, endpoint=False)

        frequencia_determinada = 10

       
        senyal2 = np.sin(2 * np.pi * frequencia_determinada * t)

        
        fft_output = np.fft.fft(senyal2)
        freqs_output = np.fft.fftfreq(len(senyal2), 1/sampf)

        audios_descartats.append(frequencia_determinada)

    else:
        ft = np.fft.rfft (senyal)
        roundft = np.round(ft)
        absft = np.abs(ft)
        freq = np.fft.rfftfreq (len(senyal), d=1./sampFreq)
        roundfreq = np.round(freq)
        absfreq = np.abs(freq)
        max_index = np.argmax(np.abs(ft))
        freq_dominant = freq [max_index]

        def increment(absft):
            amplituds = []
            step = 1
            x = 1
            while  step <= len(absft):
                maxim = (max(absft[(step-1):step]))
                index = np.where(absft==maxim)[0][0]
                frequencia = freq[index]
                amplituds.append (maxim)
                #print ("Amplitude", str(maxim) + "Frequency", str(frequencia) + "Place", str(index))
                step += 1
                x += 1
                #if absft_x > maxim:
                    #print ("not max" + "Amplitudex", str(absft_x) > "Amplitudemaxim", str(maxim)) 
            amplituds.sort()
            amplituds_màximes = amplituds[-8:len(amplituds)]
            #print (amplituds_màximes)
            dicc = {}
            for i in amplituds_màximes:
                indexs = searchindex (i, absft)
                dicc [i] = freq[indexs]
                
            #print (dicc)
            return dicc, amplituds_màximes

        d = increment(absft)[0]
        array_amplituds = []
        array_frequencies = []
        for i in d.keys():
            array_amplituds.append (i)
            array_frequencies.append (d[i])
        
        array_frequencies.sort()
        print(array_frequencies)

        if array_frequencies[0] > 138:
            freqs_melodia.append(array_frequencies[0])
        else: 
            freqs_descartades.append(array_frequencies[0])
            
melodia_wth_0 = [freq for freq in freqs_melodia if freq != 0]
arr_notes = []
for freq in melodia_wth_0:
    nota = librosa.hz_to_note(freq)
    arr_notes.append(nota)

print (arr_notes)

folder_path = "C:/Users/JoanGómezPujol/Desktop/TR/Python/lilypond-2.24.3/bin"
file_path = folder_path + "/output.pdf"

lilypond_folder = "C:/Users/JoanGómezPujol/Desktop/TR/Python/lilypond-2.24.3/bin/lilypond.exe"

environment.set('lilypondPath', lilypond_folder)

score = stream.Score()
part = stream.Part()

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

score.append(part)

lilypond_folder2 = "C:/Users/JoanGómezPujol/Desktop/TR/Python/lilypond-2.24.3/bin"

pdf_path = f"{lilypond_folder2}/output9"
score.write('lily.pdf', fp=pdf_path)

print("PDF generated successfully.")