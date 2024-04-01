import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import os
import matplotlib as mpl
import itertools as it

def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

arxiu = 'Sounds/1 (Bb inferior).wav'
mostra, senyal = waves.read(arxiu)


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
    step = 251
    x = 251
    while  step <= len(absft):
        maxim = max(absft[(step-251):step])
        absft_x = (absft[x])
        index = np.where(absft==maxim)[0][0]
        frequencia = freq[index]
        amplituds.append (maxim)
        print ("Amplitude", str(maxim) + "Frequency", str(frequencia) + "Place", str(index))
        step += 250
        x += 250
        if absft_x > maxim:
             print ("not max" + "Amplitudex", str(absft_x) > "Amplitudemaxim", str(maxim)) 
    amplituds.sort()
    amplituds_màximes = amplituds[-10:len(amplituds)]
    print (amplituds_màximes)
    dicc = {}
    for i in amplituds_màximes:
        index_màxims = searchindex (i, absft)
        dicc [i] = freq[index_màxims]
    print (dicc)
    return dicc

d = increment(absft)
array_amplituds = []
array_frequencies = []
for i in d.keys():
    array_amplituds.append (i)
    array_frequencies.append (d[i])



plt.rcParams ['figure.figsize'] = (15,8)
plt.plot (freq, absft)
plt.title ('Harmònics Bb (C#4)')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Amplitude |X(Freq)|')
plt.plot (array_frequencies, array_amplituds, 'o', color='k')
for x, y in zip(array_frequencies, array_amplituds):
    plt.annotate(text=(round(x, 2)), xy=(x,y), xytext = (x, y), horizontalalignment = 'left', 
            verticalalignment = 'bottom', fontsize=8)
        
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