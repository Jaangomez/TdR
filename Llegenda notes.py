import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import os
import matplotlib as mpl
import statistics as st
import librosa

def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

def increment(mostres, senyals):
    array_amplituds = []
    array_frequencies = []
    amplituds = []
    sampFreq = 44100
    tamany = np.shape(senyals)
    ft = np.fft.rfft(senyals)
    absft = np.abs(ft)
    freq = np.fft.rfftfreq (len(senyals), d=1./sampFreq)
    step = 251
    x = 251
    while  step <= len(absft):
        maxim = max(absft[(step-251):step])
        #absft_x = (absft[x])
        #index_x = np.where(absft==max_x)[0][0]
        index = np.where(absft==maxim)[0][0]
        frequencia = freq[index]
        amplituds.append (maxim)
        #print ("Amplitude", str(maxim) + "Frequency", str(frequencia) + "Place", str(index))
        step += 250
        x += 250
    amplituds.sort()
    amplituds_màximes = amplituds[-10:len(amplituds)]
    #print (amplituds_màximes)
    for i in amplituds_màximes:
        index_màxims = searchindex (i, absft)
        array_amplituds.append (i)
        array_frequencies.append (freq[index_màxims])
    return freq,absft, array_frequencies, array_amplituds


def descartar_valors_extrems (dades):
    q1 = np.percentile(dades, 60)
    q3 = np.percentile(dades, 75)

    IQR = q3 - q1 

    zona_inferior = q1 - 1.5 * IQR   
    zona_superior = q3 + 1.5 * IQR

    dades_filtrades = dades[(dades >= zona_inferior) & (dades <= zona_superior)]

    return dades_filtrades


def freq_fonamental (amplituds_màximes, absft, freq):
    frequencies = []
    for i in amplituds_màximes:
        indexs = searchindex (i, absft)
        frequencies.append(freq[indexs])

    k = sorted(frequencies)
    diff_freq = np.diff(k)
    #print (diff_freq)
    #mitj_diff_freq = sum(diff_freq)/len(diff_freq)
    #print (mitj_diff_freq)
    #z = []
    mitj_z = descartar_valors_extrems(diff_freq)
    print (mitj_z)
    return (sum(mitj_z)/len(mitj_z))

def trobar_nota (frq):
    librosa.hz_to_note(frq)


#funció per a fer el gràfic de tots els arxius de la carpeta Sounds
def grafic(llista):
    plt.rcParams ['figure.figsize'] = (15,8)
    n_lines = len(llista)
    cmap = mpl.colormaps['plasma']

    # Take colors at regular intervals spanning the colormap.
    colors = cmap(np.linspace(0, 1, n_lines))

    a=0
    numeracio = 1
    for i in llista:
        freq = i[0]
        absft = i[1]
        array_frequencies = i[2]
        round_array_frequencies = [round(elem, 2) for elem in array_frequencies]
        array_amplituds = i[3]
        #print (array_amplituds)
        fonamental = freq_fonamental(array_amplituds, absft, freq)
        notes = trobar_nota(fonamental)
        plt.plot (array_frequencies, array_amplituds, 'o', color=colors[a], label=notes)
        plt.legend(loc= 'center left', bbox_to_anchor=(1, 0.5), fontsize ='x-small', handletextpad = 0.3)
        a+=1
        numeracio += 1
    
    plt.title ('Harmònics principals de totes les notes del registre del saxo alt')
    plt.xlabel ('Frequency (Hz)')
    plt.ylabel ('Amplitude |X(Freq)|')

    plt.tight_layout ()
    plt.show ()
    #plt.legend([array_frequencies, array_amplituds])
    #for x, y in zip(i[2], i[3]):
        #plt.annotate(text=(round(x, 2),round(y, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left',
            #verticalalignment = 'bottom', fontsize=8)
#recorrer tots els arxius de la carpeta Sounds
Llista_punts = []
numeracio = 1
for r, d, f in sorted(os.walk('Sounds')):
    for file in f:
        arxiu = os.path.join (r, file)
        mostres, senyals = waves.read(arxiu)
        #print (numeracio,end=" ")
        dades = increment(mostres, senyals)
        freq=dades[0]
        absft=dades[1]
        array_frequencies=dades[2]
        array_amplituds=dades[3]
        Llista_punts.append([freq,absft,array_frequencies,array_amplituds])
        numeracio += 1
        
grafic(Llista_punts)