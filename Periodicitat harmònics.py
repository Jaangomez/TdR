import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import os
import matplotlib as mpl
import itertools as it
import statistics as st
import librosa
import re


arxius = 'Sounds/melodia piano.wav'

y, sr = librosa.load(arxius)

duration = librosa.get_duration(y=y, sr=sr)
print (duration)
frame_notes_en_el_temps = librosa.onset.onset_detect(y=y, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
print(frame_notes_en_el_temps) 
temps_notes = librosa.frames_to_time(frame_notes_en_el_temps)
print(temps_notes)

durations = []
durations.append(duration)
temps_notes2 = np.concatenate((temps_notes, durations))



i=0
while i <= len(temps_notes2):
    if (i==0):
        print ('iep, encara no')
        i+=1
    else:
        t_final = temps_notes2[i] -0.05
        t_inicial = temps_notes2[i-1] +0.05
        
        arxius_sortida = f'melodia piano{i}.wav'

        mostra, so = waves.read(arxius)

        i_inici = int(t_inicial*mostra)
        i_final = int(t_final*mostra)
        porcio = so[i_inici:i_final]
        duracio = len(porcio)/mostra

        waves.write(arxius_sortida, mostra, porcio)
        print('arxiu creat: ', arxius_sortida)
        i+=1
    if (i==19):
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

z=0
for arxiu in audios_definitius:
    file = arxiu
    mostra, senyal = waves.read(file)

    sampFreq = 44110
    tamany = np.shape (senyal)

    ft = np.fft.rfft (senyal)
    roundft = np.round(ft)
    absft = np.abs(ft)
    freq = np.fft.rfftfreq (len(senyal), d=1./sampFreq)
    roundfreq = np.round(freq)
    absfreq = np.abs(freq)

    def increment(absft):
        amplituds = []
        step = 2
        x = 2
        while  step <= len(absft):
            maxim = (max(absft[(step-2):step]))
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
        print (amplituds_màximes)
        dicc = {}
        for i in amplituds_màximes:
            indexs = searchindex (i, absft)
            dicc [i] = freq[indexs]
            
        print (dicc)
        return dicc, amplituds_màximes

    d = increment(absft)[0]
    array_amplituds = []
    array_frequencies = []
    for i in d.keys():
        array_amplituds.append (i)
        array_frequencies.append (d[i])

    for i in array_amplituds:
        proporció_general = i*100/sum(absft)
        proporció_dins_harmònics_màxims = i*100/sum(array_amplituds)
        print (f'proporció general = {proporció_general}%')
        print (f'proporció dins els màxims = {proporció_dins_harmònics_màxims}%')
    
    #càlcul frequencia més abundant
    max_index = np.argmax(np.abs(ft))
    freq_dominant = freq [max_index]
    #def freq_fonamental (amplituds_màximes, absft, freq):
        #frequencies = []
        #amplituds_màximes = increment(absft)[1]
        #for i in amplituds_màximes:
            #indexs = searchindex (i, absft)
            #frequencies.append(freq[indexs])

        #frequencies.sort()
        #print (frequencies)
        #diff_freq = np.diff(frequencies)
        #print (diff_freq)
        #mitj_diff_freq = st.mean(diff_freq)
        #print (mitj_diff_freq)
        #array = []
        #mitj_array = []
        #for y in diff_freq:
            #if y <= mitj_diff_freq + 20 and y >= mitj_diff_freq - 20:
                #array.append (y)
                #mitj_array.append(sum(array)/len(array))
        #return (sum(mitj_array)/len(mitj_array))
    nota = librosa.hz_to_note(freq_dominant)
    #nota = librosa.hz_to_note(freq_fonamental (increment(absft)[1], absft, freq))

    plt.rcParams ['figure.figsize'] = (15,8)
    plt.plot (freq, absft)
    plt.title (f'Anàlisi Fourier melodia piano{z}')
    plt.xlabel ('Frequency (Hz)')
    plt.ylabel ('Amplitude |X(Freq)|')
    plt.plot (array_frequencies, array_amplituds, 'o', color='k', label=f'audio{z} = {nota}')
    for x, y in zip(array_frequencies, array_amplituds):
        plt.annotate(text=(round(x, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
                verticalalignment = 'bottom', fontsize=8)
    
    plt.legend()
    plt.tight_layout ()
    plt.show ()
    plt.close ()
    z += 1