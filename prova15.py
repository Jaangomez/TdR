import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves
from scipy.signal import argrelextrema

arxiu = 'recording23.wav'
mostra, senyal = waves.read (arxiu)

sampFreq = 44110
tamany = np.shape (senyal)

ft = np.fft.rfft (senyal)
roundft = np.round(ft)
absft = np.abs(ft)
freq = np.fft.rfftfreq (len(senyal), d=1./sampFreq)
roundfreq = np.round(freq)
absfreq = np.abs(freq)

#def increment ():
    #for z in range (len(absft)):
        #z = np.arange (0, 101)       
        #array = np.arange (0, 101)
        #step = 100
        #for step in range (len(absft)):
            #step += 100
            #array_increment = [float(x) + step for x in array]
            #print (array_increment)
#increment ()

#def absftincrementi ():
    #for array in range (len(absft)):       
        #array = np.arange (0, 251)
        #step = 250
        #for step in range (len(absft)):
            #array += step
            #array_increment = [float(i) + step for i in array]
            #my_list = list(absft)
            #round_int_array_increment = np.round(array_increment).astype(int)
            #print (array)

#absftincrementi ()

array = np.arange (1,6)
step = 5
for array in range (len(absft)):
    array += step
    print (array)



plt.rcParams ['figure.figsize'] = (15,5)
plt.plot (freq, np.abs(ft))
#plt.plot (x_interp, y_val, 'o', color='k')
plt.title ('prova6')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Amplitude')
plt.tight_layout ()
plt.show ()
      
#for i, f in enumerate (np.abs(ft)):
    #if 3000 > i > 1000:
       #print ('frequency = {} Hz with amplitude {} '.format(np.round(freq[i], 1)), (np.round(f)))
       #print (max(np.abs(ft)))
    
#senyalescalda = senyal/(2**15)
#esquerra = senyal [0:,].copy()

#print (i_index2)
#print (len(freq))
#print (len(absft))
#y_val = amplitude
#x_interp = np.interp(y_val, absft, freq) 
#print (x_interp)
     

