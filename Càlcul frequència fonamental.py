import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
import os
import matplotlib as mpl
import itertools as it
import statistics as st

def searchindex (Amplituds, llista_amplituds):
    index = 0
    for i in llista_amplituds:
        if Amplituds == i:
            return index
        index += 1

arxiu = 'Sounds/10 (B inferior).wav'
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
        index = np.where(absft==maxim)[0][0]
        amplituds.append (maxim)
        step += 250
        x += 250
    amplituds.sort()
    amplituds_màximes = amplituds[-10:len(amplituds)]

    return amplituds_màximes

def freq_fonamental (amplituds_màximes, absft, freq):
    frequencies = []
    for i in amplituds_màximes:
        indexs = searchindex (i, absft)
        frequencies.append(freq[indexs])

    frequencies.sort()
    print (frequencies)
    diff_freq = np.diff(frequencies)
    print (diff_freq)
    mitj_diff_freq = st.mean(diff_freq)
    print (mitj_diff_freq)
    z = []
    mitj_z = []
    for y in diff_freq:
        if y <= mitj_diff_freq + 20 and y >= mitj_diff_freq - 20:
            z.append (y)
            mitj_z.append(sum(z)/len(z))
    return (sum(mitj_z)/len(mitj_z))

freq_fonamental (increment(absft))
             