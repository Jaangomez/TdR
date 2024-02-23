import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
import numpy
import pylab
import struct

class VoiceRecorder:

    def __init__(self):
        self.RATE=44100
        self.BUFFERSIZE=1024
        self.secToRecord=.1
        self.threadsDieNow=False
        self.newAudio=False
        self.chunksToRecord=(100)
        self.secPerPoint=1.0/self.RATE
        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(format=pyaudio.paInt16,channels=1,
            rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)
        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE),dtype=numpy.int16)
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

    def setup(self):
        self.buffersToRecord=int(self.RATE*self.secToRecord/self.BUFFERSIZE)
        if self.buffersToRecord==0: self.buffersToRecord=1
        self.samplesToRecord=int(self.BUFFERSIZE*self.buffersToRecord)
        self.chunksToRecord=int(self.samplesToRecord/self.BUFFERSIZE)
        self.secPerPoint=1.0/self.RATE

        self.p = pyaudio.PyAudio()
        self.inStream = self.p.open(format=pyaudio.paInt16,channels=1,
            rate=self.RATE,input=True,frames_per_buffer=self.BUFFERSIZE)
        self.xsBuffer=numpy.arange(self.BUFFERSIZE)*self.secPerPoint
        self.xs=numpy.arange(self.chunksToRecord*self.BUFFERSIZE)*self.secPerPoint
        self.audio=numpy.empty((self.chunksToRecord*self.BUFFERSIZE),dtype=numpy.int16)

    def close(self):
        self.p.close(self.inStream)
    
    def getaudio (self):
        audioString=self.inStream.read(self.BUFFERSIZE)
        return numpy.frombuffer(audioString,dtype=numpy.int16)
    def downsample(self,data,mult):
                overhang=len(data)%mult
                if overhang: data=data[:-overhang]
                data=numpy.reshape(data,(len(data)/mult,mult))
                data=numpy.average(data,1)
                return data
    
    def fft(self,data=None,trimBy=10,logScale=False,divBy=100):
        if data==None:
            data=self.audio.flatten()
            left,right=numpy.split(numpy.abs(numpy.fft.fft(data)),2)
            ys=numpy.add(left,right[::-1])
        if logScale:
            ys=numpy.multiply(20,numpy.log10(ys))
            xs=numpy.arange(self.BUFFERSIZE/2,dtype=float)
        if trimBy:
            i=int((self.BUFFERSIZE/2)/trimBy)
            ys=ys[:i]
            xs=xs[:i]*self.RATE/self.BUFFERSIZE
        if divBy:
            ys=ys/float(divBy)
        return xs,ys
        
    def plotAudio(self): 
        pylab.plot(self.audio.flatten())
        pylab.show()

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

        while True:
            if self.threadsDieNow: break
            for i in range(self.chunksToRecord):
                self.audio[i*self.BUFFERSIZE:(i+1)*self.BUFFERSIZE]=self.getaudio()
            self.newAudio=True
            if self.recording==False: break

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