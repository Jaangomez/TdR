import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as waves

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

def absftincrementi ():
    for z in range (len(absft)):
        z = np.arange (0, 101)       
        array = np.arange (0, 101)
        step = 47459
        for step in range (len(absft)):
            step += 47459
            array_increment = [float(i) + step for i in array]
            my_list = list(absft)
            round_int_array_increment = np.round(array_increment).astype(int)
            index_i = my_list.index(max((absft[(round_int_array_increment)])))
            absft_index_i = absft[index_i]
            print ("amplitude =", (absft_index_i))
                
absftincrementi ()

def absfreqincrementi ():
        for z in range (len(absft)):
            z = np.arange (0, 101)       
            array = np.arange (0, 101)
            step = 250
            for step in range (len(absft)):
                step += 250
                array_increment = [float(i) + step for i in array]
                my_list = list(absft)
                round_int_array_increment = np.round(array_increment).astype(int)
                index_i = my_list.index(max((absft[(round_int_array_increment)])))
                freq_index_i = freq[index_i]
                print ("frequency = ", (freq_index_i))
absfreqincrementi ()

def incrementx ():
        x = 101
        for x in range (len(absft)):
            x += 250
            my_list = list(absft)
            index_x = my_list.index(absft[x])
            absft_index_x = absft[index_x]
            return absft_index_x
incrementx () 

def comparar ():
    absftincrementi ()
    incrementx ()    
    my_list = list(absft)
    #for element in range (my_list): 
    if incrementx () > absftincrementi ():
        my_list == False 
        print ('not max')  
comparar ()


plt.rcParams ['figure.figsize'] = (15,5)
plt.plot (freq, np.abs(ft))
#plt.plot (x_interp, y_val, 'o', color='k')
plt.title ('prova6')
plt.xlabel ('Frequency (Hz)')
plt.ylabel ('Amplitude')
plt.tight_layout ()
plt.show ()