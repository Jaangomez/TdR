import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import os
import matplotlib as mpl
import itertools as it
import statistics as st
import scipy
import librosa
from pydub import AudioSegment as ag
from pydub import utils
import pydub

def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

arxiu = 'idk.wav'
mostra, senyal = waves.read(arxiu)
x, sr = librosa.load ('idk.wav')

sampFreq = 44110
tamany = np.shape (senyal)
len_senyal = len(senyal)
sound = ag.from_file(arxiu)
chunks = utils.make_chunks(sound, 10000)
print (chunks)


ft = np.fft.rfft (senyal)
roundft = np.round(ft)
absft = np.abs(ft)
freq = np.fft.rfftfreq (len(senyal), d=1./sampFreq)
roundfreq = np.round(freq)
absfreq = np.abs(freq)

onset_frames = librosa.onset.onset_detect(y=x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
print(onset_frames) # frame numbers of estimated onsets
onset_times = librosa.frames_to_time(onset_frames)
print(onset_times)

#t = []
#def output_duration(length): 
    #hours = length // 3600  # calculate in hours 
    #length %= 3600
    #mins = length // 60  # calculate in minutes 
    #length %= 60
    #seconds = length  # calculate in seconds 
  
    #return seconds

#z = len_senyal/sampFreq
#seconds = (output_duration(int(z)))
#print (seconds)
#i = 0
#while i<seconds+1:
    #t.append(i)
    #print (t)
    #i+=1
#print('Total Duration: {}:{}:{}'.format(hours, mins, seconds)) 
def trobar_nota (frq):
    if 127.143 <= frq and frq < 134.702:
        return "C3"
    elif 134.703 <= frq  and frq <= 142.7115:
        return "C#3/Db3"
    elif 142.7116 <= frq and frq <= 151.1975:
        return "D3"
    elif 151.1976 <= frq and frq <= 160.1885:
        return "D#3/Eb3"
    elif 160.1886 <= frq < 169.714:
        return "E3"
    elif 169.715 <= frq < 179.8055:
        return "F3"
    elif 179.8056 <= frq < 190.4975:
        return "F#3/Gb3"
    elif 190.4976 <= frq < 201.825:
        return "G3"
    elif 202.826 <= frq < 213.826:
        return "G#3/Ab3"
    elif 213.827 <= frq < 226.941:
        return "A3"
    elif 226.942 <= frq < 240.412:
        return "A#3/Bb3"
    elif 240.413 <= frq < 254.284:
        return "B3"
    elif 254.284 <= frq < 269.4045:
        return "C4"
    elif 269.4046 <= frq < 285.424:
        return "C#4/Db4"
    elif 285.425 <= frq < 302.396:
        return "D4" 
    elif 302.397 <= frq < 320.3775:
        return "D#4/Eb4"
    elif 320.3776 <= frq < 339.428:
        return "E4"
    elif 339.429 <= frq < 359.611:
        return "F4"
    elif 359.612 <= frq < 380.9945:
        return "F#4/Gb4"
    elif 380.9946 <= frq < 403.65:
        return "G4"
    elif 403.66 <= frq < 427.6525:
        return "G#4/Ab4"
    elif 427.6526 <= frq < 453.082:
        return "A4"
    elif 453.083 <= frq < 479.7985:
        return "A#4/Bb4"
    elif 479.7986 <= frq < 508.567:
        return "B4"
    elif 508.568 <= frq < 538.808:
        return "C5"
    elif 538.809 <= frq < 570.8515:
        return "C#5/Db5"
    elif 570.8516 <= frq < 604.796:
        return "D5"
    elif 604.797 <= frq < 640.7545:
        return "D#5/Eb5"
    elif 640.7546 <= frq < 678.8555:
        return "E5"
    elif 678.8556 <= frq < 719.2225:
        return "F5"
    elif 719.2226 <= frq < 760.99:
        return "F#5/Gb5"
    elif 760.991 <= frq < 811.8:
        return "G5"
    elif 811.801 <= frq < 859.2085:
        return "G#5/Ab5"
    elif 859.2086 <= frq < 906.568:
        return "A5"
    elif 906.569 <= frq < 960.0475:
        return "A#5/Bb5"
    elif 960.0476 <= frq < 1017.1735:
        return "B5"
    elif 1017.1736 <= frq < 1077.615:
        return "C6"
    elif 1077.616 <= frq < 1141.695:
        return "C#6/Db6"
    elif 1141.695 <= frq < 1209.585:
        return "D6"
    elif 1209.586 <= frq < 1281.51:
        return "D#6/Eb6"
    elif 1281.511 <= frq < 1358.71:
        return "E6"
    elif 1358.711 <= frq < 1439.445:
        return "F6"
    else:
        return "Nota no identificada"
    
def increment(absft):
    amplituds = []
    step = 251
    x = 251
    while  step <= len(absft):
        maxim = max(absft[(step-251):step])
        index = np.where(absft==maxim)[0][0]
        frequencia = freq[index]
        amplituds.append (maxim)
        #print ("Amplitude", str(maxim) + "Frequency", str(frequencia) + "Place", str(index))
        step += 250
        x += 250
        #if absft_x > maxim:
            #print ("not max" + "Amplitudex", str(absft_x) > "Amplitudemaxim", str(maxim)) 
    amplituds.sort()
    amplituds_màximes = amplituds[-len(onset_times):len(amplituds)]
    #print (amplituds_màximes)
    dicc = {}
    for i in amplituds_màximes:
        indexs = searchindex (i, absft)
        dicc [i] = freq[indexs]
        
    print (dicc)
    return dicc

d = increment(absft)
array_amplituds = []
array_frequencies = []
for i in d.keys():
    array_amplituds.append (i)
    array_frequencies.append (d[i])

plt.rcParams ['figure.figsize'] = (15,8)
plt.plot (onset_times, array_frequencies)
plt.title ('Harmònics Bb (C#6)')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Amplitude |X(Freq)|')
notes = trobar_nota(array_frequencies(np.argmax(array_amplituds)))
plt.plot (onset_times, array_frequencies, 'o', color='k', label=notes)
for x, y in zip(onset_times, array_frequencies):
    plt.annotate(text=(round(y, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
            verticalalignment = 'bottom', fontsize=8)
    plt.legend()
    
        
plt.tight_layout ()



#existeix = True
#i = 1
#while existeix:
    #if os.path.exists(f"nota{i}.jpg"):
        #i += 1
    #else: 
        #existeix = False 
#plt.savefig (f"nota{i}.png")
plt.show ()