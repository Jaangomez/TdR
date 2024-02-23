import numpy as np
import os
import time
import pyaudio
import matplotlib.pyplot as plt
from scipy.fftpack import fft

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

import os
import wave
import time
import threading
import tkinter as tk
import pyaudio

class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable = (False, False)
        self.button = tk.Button (text= "🎤", font = ("Arial", 120, "bold"),
                                 command = self.click_handler)
        self.button.pack ()
        self.label = tk.Label(text="00:00:00")
        self.label.pack ()
        self.recording = False
        self.root.mainloop ()
        self.threadsDieNow=False
        self.newAudio=False


    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread (target=self.record).start()

    def record(self,forever=True):
        audio = pyaudio.PyAudio ()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        frames = []

        start = time.time ()

        while self.recording:
            if forever==False : break
            data = stream.read(1024)
            frames.append(data)
           
            RECORD_SECONDS = time.time () - start
            s = RECORD_SECONDS % 60
            min = RECORD_SECONDS // 60
            h = min // 60
            self.label.config(text=f"{int(h):02d}:{int(min):02d}:{int(s):02d}")
            n = 1024
            k=np.arange(n)
            T = n/RATE
            frq = k/T
            frq = frq[range(int(n/2))] # one side frequency range
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                self.newAudio=True
                if forever==False: break
                data = stream.read(CHUNK)
                frames.append(data)
                decoded = np.fromstring(data, dtype=np.int16) #grab the data in stream
                fft_decode=fft(decoded)/(len(decoded)/2) #normalized FFT
                mags=np.absolute(fft(decoded)) #
                plt.ylim(top=50000)
                plt.xlabel('Freq (Hz)')
                plt.ylabel('|Y(freq)|')
                plt.plot(frq, mags[range(int(n/2))],'b')
                #plt.pause(2)
                #plt.gcf().clear()
                #plt.close()
        
        stream.stop_stream ()
        stream.close ()
        audio.terminate ()

        exists = True
        i = 1
        while exists:
            if os.path.exists (f"recording{i}.wav"):
                i += 1

            else:
                exists = False

        sound_file = wave.open (f"recording{i}.wav", "wb")
        sound_file.setnchannels (1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate (44100)
        sound_file.writeframes (b"".join(frames))
        sound_file.close ()


VoiceRecorder ()

