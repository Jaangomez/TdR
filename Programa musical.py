import numpy as np
import scipy.fftpack as fft
import pandas as pd
import os
from midiutil.MidiFile import MIDIFile as md
import pyaudio

rate = 44100
buffer = 1024
channel = 1
format = pyaudio.paInt16
n = np.arange(buffer)
bf = buffer/rate
frq = n/bf
frq = frq[range(int(n/2))]

p = pyaudio.PyAudio ()

if frq in range (16.3516, 16.83775):
    print = "C0"
if frq in range (16.83776, 17.83695):
    print = "C#0" or "Db0"
if frq in range (17,83696, 18.8997):
    print = "D0"
if frq in range (18.8998, 19.9911):
    print = "D#0" or "Eb0"
if frq in range (19.9912, 21,7985):
    print = "E0"
if frq in range (21.7986, 22.47575):
    print = "F0"
if frq in range (21.47576, 23.8122):
    print = "F#0" or "Gb0"
if frq in range (23.8123, 25.2281):
    print = "G0"
if frq in range (25.2282, 26.72825):
    print = "G#0" or "Ab0"
if frq in range  (26.72826, 28.3176):
    print = "A0"
if frq in range (28.3177, 30.00115):
    print = "A#0" or "Bb0"
if frq in range (30.00116, 31.78665):
    print = "B0"
if frq in range (31.78666, 33.677):
    print = "C1"
if frq in range (33.678, 35.67795):
    print = "C#1" or "Db1"
if frq in range (35.67796, 37.7995):
    print = "D1"
if frq in range (37.7996, 40.04715):
    print = "D#1" or "Eb1"
if frq in range (40.04716, 42.4285):
    print = "E1"
if frq in range  (42.4286, 44.95135):
    print = "F1"
if frq in range (44.95136, 47.62435):
    print = "F#1" or "Gb1"
if frq in range (47.62436, 50.45625):
    print = "G1"
if frq in range (50.45626, 53.45655):
    print = "G#1" or "Ab1"
if frq in range (53.45656, 56.63525):
    print = "A1"
if frq in range (56.62526, 61.00295):
    print = "A#1" or "Bb1"
if frq in range (61.00296, 64.5709):
    print = "B1"
if frq in range (64.571, 67.35105):
    print = "C2"
if frq in range (67.35106, 71.35595):
    print = "C#2" or "Db2"
if frq in range (71.35596, 75.59895):
    print = "D2"
if frq in range (75.59896, 80.0943):
    print = "D#2" or "Eb2"
if frq in range (80.0944, 84.857):
    print = "E2"
if frq in range (84.858, 89.90285):
    print = "F2"
if frq in range (89.90286, 95.24875):
    print = "F#2" or "Gb2"
if frq in range (95.24876, 100.91245):
    print = "G2"
if frq in range (100.91246, 106.913):
    print = "G#2" or "Ab2"
if frq in range (106.914, 113.2705):
    print = "A2"
if frq in range (113.2706, 120.006):
    print = "A#2" or "Bb2"
if  frq in range (120.007, 127.142):
    print = "B2"
if frq in range (127.143, 134.702):
    print = "C3"
if frq in range (134.703, 142.7115):
    print = "C#3" or "Db3"
if frq in range (142.7116, 151.1975):
    print = "D3"
if frq in range (151.1976, 160.1885):
    print = "D#3" or "Eb3"
if frq in range (160.1886, 169.714):
    print = "E3"
if frq in range (169.715, 179.8055):
    print = "F3"
if frq in range (179.8056, 190.4975):
    print = "F#3" or "Gb3"
if frq in range (190.4976, 201.825):
    print = "G3"
if frq in range (202.826, 213.826):
    print = "G#3" or "Ab3"
if frq in range (213.827, 226.941):
    print = "A3"
if frq in range (226.942, 240.412):
    print = "A#3" or "Bb3"
if frq in range (240.413, 254.284):
    print = "B3"
if frq in range (254.284, 269.4045):
    print = "C4"
if frq in range (269.4046, 285.424):
    print = "C#4" or "Db4"
if frq in range (285.425, 302.396):
    print = "D4" 
if frq in range (302.397, 320.3775):
    print = "D#4" or "Eb4"
if frq in range (320.3776, 339.428):
    print = "E4"
if frq in range (339.429, 359.611):
    print = "F4"
if frq in range (359.612, 380.9945):
    print = "F#4" or "Gb4"
if frq in range (380.9946, 403.65):
    print = "G4"
if frq in range (403.66, 427.6525):
    print ="G#4" or "Ab4"
if frq in range (427.6526, 453.082):
    print = "A4"
if frq in range (453.083, 479.7985):
    print = "A#4" or "Bb4"
if frq in range (479.7986, 508.567):
    print = "B4"
if frq in range (508.568, 538.808):
    print = "C5"
if frq in range (538.809, 570.8515):
    print = "C#5" or "Db5"
if frq in range (570.8516, 604.796):
    print = "D5"
if frq in range (604.797, 640.7545):
    print = "D#5" or "Eb5"
if frq in range (640.7546, 678.8555):
    print = "E5"
if frq in range (678.8556, 719.2225):
    print = "F5"
if frq in range (719.2226, 760.99):
    print = "F#5" or "Gb5"
if frq in range (760.991, 811.8):
    print = "G5"
if frq in range (811.801, 859.2085):
    print = "G#5" or "Ab5"
if frq in range (859.2086, 906.568):
    print = "A5"
if frq in range (906.569, 960.0475):
    print = "A#5" or "Bb5"
if frq in range (960.0476, 1017.1735):
    print = "B5"
if frq in range (1017.1736, 1077.615):
    print = "C6"
if frq in range (1077.616, 1141.695):
    print = "C#6" or "Db6"
if frq in range (1141.695, 1209.585):
    print = "D6"
if frq in range (1209.586, 1281.51):
    print = "D#6" or "Eb6"
if frq in range (1281.511, 1358.71):
    print = "E6"
if frq in range (1358.711, 1439.445):
    print = "F6"
if frq in range (1439.446, 1523.98):
    print = "F#6" or "Gb6"
if frq in range (1523.981, 1614.6):
    print = "G6"
if frq in range (1614.601, 1710.61):
    print = "G#6" or "Ab6"
if frq in range (1710.601, 1812.33):
    print = "A6"
if frq in range (1812.331, 1920.095):
    print = "A#6" or "Bb6"
if frq in range (1920.096, 1975.53):
    print = "B6"
if frq in range (0, 16.3515):
    print = "to low, undetected"
if frq>1975.53:
    print = "to high, undetectable"
if frq in range (None):  
    print = "analizing error"
        