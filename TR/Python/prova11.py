try:
    import pyaudio
    import numpy as np
    import pylab
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    import time
    import sys
    import threading
    import tkinter as tk
    import seaborn as sns
    import wave
    import os
except:
    print ("no s'ha importat")

i=0
f,ax = plt.subplots(2)

x = np.arange (10000)
y = np.random.randn(10000)

grafic1 = ax[0].plot(x,y)
ax[0].set_xlim (0,100)
ax[0].set_ylim (0,10000)
ax[0].set_title ("senyal d'audio")

grafic2 = ax[1].plot(x,y)
ax[1].set_xlim (0,100)
ax[1].set_ylim (0, 10000)
ax[1].set_title ("Transformada de Fourier")
plt.tight_layout()

class VoiceRecorder:

    def plot_data (in_data):
        audio_data = np.fromstring(in_data, np.int16)
        dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))
        grafic1.set_xdata(np.arange(len(audio_data)))
        grafic1.set_ydata(audio_data)
        grafic2.set_xdata(np.arange(len(dfft))*10.)
        grafic2.set_ydata(dfft)

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

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread (target=self.record).start()

    def record(self):
        audio = pyaudio.PyAudio ()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        frames = []

        start = time.time ()

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

            passed = time.time () - start
            s = passed % 60
            min = passed // 60
            h = min // 60
            self.label.config(text=f"{int(h):02d}:{int(min):02d}:{int(s):02d}")
        
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

