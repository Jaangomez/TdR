import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import os
import matplotlib as mpl
import itertools as it
import statistics as st
import librosa
import re
import math


arxius = 'Sounds/Skylark.wav'

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
        
        arxius_sortida = f'Skylark{i}.wav'

        mostra, so = waves.read(arxius)

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

z=0
for arxiu in audios_definitius:
    file = arxiu
    mostra, senyal = waves.read(file)

    sampFreq = 44110
    tamany = np.shape (senyal)

    if  len(senyal) == 0:
        sampf = 1000  
        duració = 1      

        # Generate time vector
        t = np.linspace(0, duració, duració*sampf, endpoint=False)

        frequencia_determinada = 10

        # Generate a signal containing only the frequency of interest
        senyal2 = np.sin(2 * np.pi * frequencia_determinada * t)

        # Perform FFT
        fft_output = np.fft.fft(senyal2)
        freqs_output = np.fft.fftfreq(len(senyal2), 1/sampf)

        # Plot the signal
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(t, senyal2)
        plt.title('No hi ha soroll, així que imprimeixo això')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')

        # Show the plot
        plt.tight_layout()
        plt.show()

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
        
        #càlcul frequencia més abundant --> funciona només per piano
        max_index = np.argmax(np.abs(ft))
        freq_dominant = freq [max_index]

        #càlcul frequencia real --> la resta d'instruments

        def freq_fonamental (amplituds_màximes, absft, freq):
            frequencies = []
            for i in amplituds_màximes:
                indexs = searchindex (i, absft)
                frequencies.append(freq[indexs])

            sorted_frequencies = sorted(frequencies)
            #print (sorted_frequencies)
            diff_freq = np.diff(sorted_frequencies)
            print (diff_freq)

    
            return diff_freq
        
        def descartar_valors_i_suma_final (frequenncia):
            llista_filtrada = []
            print (llista_filtrada)

            for i in frequenncia:
                if i > 100 and i < freq_dominant:
                    llista_filtrada.append(i)
            
            if len(llista_filtrada) == 0:
                mitj = 0

            else:
                mitj = (sum(llista_filtrada)/len(llista_filtrada))
                print(mitj)

            return mitj
        
        if descartar_valors_i_suma_final(freq_fonamental(increment(absft)[1], absft, freq))== 0:
            if freq_dominant == 0:
                nota = 'No identificat'
                plt.rcParams ['figure.figsize'] = (15,8)
                plt.plot (freq, absft)
                plt.title (f'Anàlisi Fourier Skylark{z}')
                plt.xlabel ('Frequency (Hz)')
                plt.ylabel ('Amplitude |X(Freq)|')
                plt.plot (array_frequencies, array_amplituds, 'o', color='k', label=f'audio{z} = {nota}')
                for x, y in zip(array_frequencies, array_amplituds):
                    plt.annotate(text=(round(x, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
                            verticalalignment = 'bottom', fontsize=8)
                
                plt.legend()
                plt.tight_layout ()
                nom_arxiu = f'Skylark nota {z}'
                plt.savefig (nom_arxiu)
                plt.show ()
                plt.close ()
                z += 1

            else:
                nota = librosa.hz_to_note(freq_dominant)
                plt.rcParams ['figure.figsize'] = (15,8)
                plt.plot (freq, absft)
                plt.title (f'Anàlisi Fourier Skylark{z}')
                plt.xlabel ('Frequency (Hz)')
                plt.ylabel ('Amplitude |X(Freq)|')
                plt.plot (array_frequencies, array_amplituds, 'o', color='k', label=f'audio{z} = {nota}')
                for x, y in zip(array_frequencies, array_amplituds):
                    plt.annotate(text=(round(x, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
                            verticalalignment = 'bottom', fontsize=8)
                
                plt.legend()
                plt.tight_layout ()
                nom_arxiu = f'Skylark nota {z}'
                plt.savefig (nom_arxiu)
                plt.show ()
                plt.close ()
                z += 1
        
        else:
            nota = librosa.hz_to_note(descartar_valors_i_suma_final(freq_fonamental(increment(absft)[1], absft, freq)))

        
        #freq_real = (freq_fonamental(array_amplituds, absft, freq))
        #nota = librosa.hz_to_note(freq_real)

            plt.rcParams ['figure.figsize'] = (15,8)
            plt.plot (freq, absft)
            plt.title (f'Anàlisi Fourier Skylark{z}')
            plt.xlabel ('Frequency (Hz)')
            plt.ylabel ('Amplitude |X(Freq)|')
            plt.plot (array_frequencies, array_amplituds, 'o', color='k', label=f'audio{z} = {nota}')
            for x, y in zip(array_frequencies, array_amplituds):
                plt.annotate(text=(round(x, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
                        verticalalignment = 'bottom', fontsize=8)
            
            plt.legend()
            plt.tight_layout ()
            nom_arxiu = f'Skylark nota {z}'
            plt.savefig (nom_arxiu)
            plt.show ()
            plt.close ()
            z += 1