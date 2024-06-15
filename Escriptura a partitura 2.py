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

arxiu = 'Sounds/In a sentimental mood complet.wav'
y, sr = librosa.load(arxiu)

duration = librosa.get_duration(y=y, sr=sr)
#print (duration)
frame_notes_en_el_temps = librosa.onset.onset_detect(y=y, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
#print(frame_notes_en_el_temps) 
temps_notes = librosa.frames_to_time(frame_notes_en_el_temps)
#print(temps_notes)

frame = 2048
salt = 512
frames_arxiu = librosa.util.frame(y, frame_length=frame, hop_length=salt)

durations = []
durations.append(duration)
temps_notes2 = np.concatenate((temps_notes, durations))

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
        return "C2"
    
i=0
while i <= len(temps_notes2):
    if (i==0):
        print ('iep, encara no')
        i+=1
    else:
        t_final = temps_notes2[i] -0.05
        t_inicial = temps_notes2[i-1] +0.05
        
        arxius_sortida = f'In a sentimental mood{i}.wav'

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

def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

melodia = []
z=0
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
    
    else:
        ft = np.fft.rfft (senyal)
        roundft = np.round(ft)
        absft = np.abs(ft)
        freq = np.fft.rfftfreq (len(senyal), d=1./sampFreq)
        roundfreq = np.round(freq)
        absfreq = np.abs(freq)

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
            amplituds_màximes = amplituds[-10:len(amplituds)]
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
        
        #càlcul frequencia més abundant --> funciona només per piano
        max_index = np.argmax(np.abs(ft))
        freq_dominant = freq [max_index]

        def freq_fonamental (amplituds_màximes, absft, freq):
            frequencies = []
            for i in amplituds_màximes:
                indexs = searchindex (i, absft)
                frequencies.append(freq[indexs])

            sorted_frequencies = sorted(frequencies)
            #print (sorted_frequencies)
            diff_freq = np.diff(sorted_frequencies)
            #print (diff_freq)

    
            return diff_freq
        
        def descartar_valors_i_suma_final (frequenncia):
            llista_filtrada = []
            #print (llista_filtrada)

            for i in frequenncia:
                if i > 100 and i < freq_dominant:
                    llista_filtrada.append(i)
            
            if len(llista_filtrada) == 0:
                mitj = 0

            else:
                llista_filtrada.sort()
                mitj = llista_filtrada[0]
                print(mitj)

            return mitj
        
        if descartar_valors_i_suma_final(freq_fonamental(increment(absft)[1], absft, freq))== 0:
            if freq_dominant == 0:
                nota = 'No identificat'
            
            else:
                melodia.append(freq_dominant)

        else:
           melodia.append(descartar_valors_i_suma_final(freq_fonamental(increment(absft)[1], absft, freq)))

melodia_wth_0 = [freq for freq in melodia if freq != 0]
arr_notes = []
for freq in melodia_wth_0:
    nota = trobar_nota(freq)
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

pdf_path = f"{lilypond_folder2}/output5"
score.write('lily.pdf', fp=pdf_path)

print("PDF generated successfully.")
array_frequencies.sort()