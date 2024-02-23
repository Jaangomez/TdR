import pyaudio
import os
import struct
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.fftpack import fft
from tkinter import TclError

CHUNK = 1024 * 4 #samples per frame
FORMAT = pyaudio.paInt16 #pulls audio info as 16bit 
CHANNELS = 1 # number of channels
RATE = 44100 #sample rate

fig, (ax, ax2) = plt.subplots(2, figsize=(15,7))
p = pyaudio.PyAudio() #create pyaudio object

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = CHUNK
)

# variable for plotting
x = np.arange(0, 2*CHUNK, 2)
x_fft = np.linspace(0, RATE, CHUNK)

# create random line w/ random data. Can use either semilogx or plot
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=2)#you only need one chunk because we slice the data in half in the while loop
line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)

# basic formatting for axes
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0,255)
ax.set_xlim(0,2*CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2*CHUNK], yticks=[0,128,255])

ax2.set_xlim(20, RATE / 2)

# show the plot
plt.show(block=False)

print('stream started')

# for measuring frame rate
frame_count = 0
start_time = time.time()

while True:
    
    # binary data
    data = stream.read(CHUNK)
    data_int = struct.unpack(str(2*CHUNK) + 'B', data)
    
    # convert data to integers, make np array, then offset it by 127
    data_np = np.array(data_int).astype(dtype='b')[::2] +128
    
    line.set_ydata(data_np)
    
    # get fft, slice, and rescale to get magnitudes
    y_fft = fft(data_int)
    
    # multiply by 2 and divide by the number of frequencies in spectrum times the amplitude of the waveform
    line_fft.set_ydata(np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK))
    
    # update figure canvas
    try:
        fig.canvas.draw()
        fig.canvas.flush_events()
        frame_count += 1
        
    except TclError:
        
        #calculate average frame rate
        frame_rate = frame_count / (time.time() - start_time)
        
        print('stream stopped')
        print('average frame rate = {:.0f} FPS'.format(frame_rate))
        break

    #Import statements
import pyaudio #The module used for pulling in audio information
import os
import struct
import numpy as np #Module used to convert Audio info into easily processed arrays
import time #used to continuously call the stream by sleeping for the proper amount of time
import math #used to perform certatin advanced mathematical calculations
import cProfile #used to get timing info on the performancce of the program
import keyboard
import wave #how we make wave recording
import winsound #Sound for metronome

from midiutil import MIDIFile #how we build MIDI
from scipy.fftpack import fft   #Fast Fourier transform is a computaionaly effective fouier transform
from tkinter import TclError    #acces TclError funtion of Gui pack

MINMIDI = 28 #min midi value considered by Algo
MAXMIDI = 108 #max midi value considered by Algo
data = []

#create list of midi and frequency values
n = MINMIDI
noteNfreq = []
while n <= MAXMIDI:
    f = 440*(2**((n-69)/12))
    noteNfreq.append(f)
    n = n + 1
noteArray = np.asarray(noteNfreq)

#defines stream information
CHUNK = 1024 * 4 #samples per frame
FORMAT = pyaudio.paInt16 #pulls audio info as 16bit
CHANNELS = 1 # number of channels
RATE = 44100 #sample rate
FREQ = 2500  # Set Frequency To 2500 Hertz
DUR = 2 #set Duration of metronome to To 2 ms == .002 second

# for measuring frame rate
frame_count = 0

totalTicks = 0
ticksPerBeat = 4

#keep track of notes
noteValue = [] #stores midi Values of read data
noteTime = [] #stores time(ticks) midi Values were read at

#keep track of track
midiNote = []  #Defines note values of midi Files
mididuration = [] #defines length of note values within a Midi File
midionset = [] #defines starting point of midi values within a Midi File
tracker = 0 #tracks num of values have been tracked by the note
track    = 0
channel  = 0
midiTime = 0   # In beats
tempo    = int(input("Set Tempo in bpm: "))  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

#tempo data
secPerQnote = 1/(tempo/60)
MINREAD = 16 #1/how long the smallest note is
secPerMin = secPerQnote/(MINREAD/4)
TICKTIME = secPerMin/ticksPerBeat
delay = 0

#stores audio data to provide recording
framez = []

# get device information of system
# d = pyaudio.PyAudio()
#
# for i in range(d.get_device_count()):
#     dev = d.get_device_info_by_index(i)
#     print((i,dev['name'],dev['maxInputChannels']))
# d.terminate()

#Calbackfunction that puts pyaudio in non-blocking mode
def callback(in_data, frame_count, time_info, status):
    global totalTicks
    global data
    global delay
    global TICKTIME

    data = in_data
    #if the program took longer to run than the required tick time
    if(TICKTIME-delay > 0):
        time.sleep(TICKTIME-delay)
    else:
        print("wrong")
    #Only allows program to run for 300 ticks, for the purpose of testing
    if(totalTicks > 300):
        return (data, pyaudio.paAbort)

    return (data, pyaudio.paContinue)

#uses midi info stored from the real time processing to build midi file
def buildMidi():
    global track
    global channel
    global midiTime
    #global duration = noteDuration/(total time/(beat per second))  # In beats
    global tempo
    global volume
    global totalTicks
    global ticksPerBeat
    global midiNote
    global mididuration
    global midionset

    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
    MyMIDI.addTempo(track, midiTime,tempo)
    delay = midionset[0]


    #add logic to convert ticks to time value

    for num in range(0, len(midiNote)):
        MyMIDI.addNote(track, channel, midiNote[num], math.floor((midionset[num]-delay)/2), mididuration[num]/2, volume)

    print(midiNote)
    print(midionset)
    with open("midiTest.MIDI", "wb") as output_file:
        MyMIDI.writeFile(output_file)


def main():
    global TICKTIME
    global data
    global noteValue
    global noteTime
    global totalTicks
    global ticksPerBeat
    global midiNote
    global mididuration
    global tracker
    global midionset
    global framez
    global data
    global delay
    global secPerQnote
    #instantiate PyAudio
    p = pyaudio.PyAudio()

    #open Stream Using Callback
    stream = p.open(
            format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            output = False,
            #input_device_index=1,
            frames_per_buffer = CHUNK,
            stream_callback = callback
        )

    streamin = True
    #Count in
    print("Stream start in 4")
    for x in range(0,3):
        winsound.Beep(FREQ, DUR)
        time.sleep(secPerQnote)

    #start Stream
    stream.start_stream()
    while stream.is_active():
        startTime = stream.get_time()
        if(totalTicks % 16 == 0):
            winsound.Beep(FREQ, DUR)
        if(data != []):
            framez.append(data)
            data_int = struct.unpack(str(2*CHUNK) + 'B', data)
            # convert data to integers, make np array, then offset it by 127
            #this is the magnitude data?
            data_np = np.array(data_int, dtype='b')[::2] +128

            # get fft, slice, and rescale to get magnitudes
            # multiply by 2 and divide by the number of frequencies in spectrum times the amplitude of the waveform
            y_fft = fft(data_int)
            frequencies = np.abs(y_fft[0:CHUNK]) * 2 / (256 * CHUNK)
            maxf = max(frequencies[1:])
            flist = frequencies.tolist()
            findex = flist.index(maxf)


            if findex < 1000:
               #find midinums
                frequency_val = findex * (RATE/CHUNK)
                arrindex = (np.abs(noteArray - frequency_val)).argmin()
                midiNum = arrindex + MINMIDI


                #if we find a midiValue we wanna keep
                if midiNum <= MAXMIDI:
                   #if there have already been a notes worth of midiValues stored up
                    if len(noteValue) >= ticksPerBeat:
                       #if the midi we see is the same as the other notes, add it to the list
                            if midiNum == noteValue[tracker-3] and midiNum == noteValue[0]:
                                noteValue.append(midiNum)
                                noteTime.append(totalTicks)
                                tracker = len(noteValue)
                            #otherwise add note to track, display and clear variables
                            else:
                                midiNote.append(noteValue[0])
                                midionset.append(noteTime[0]/ticksPerBeat)
                                duration = (totalTicks - noteTime[0])/ticksPerBeat
                                mididuration.append(duration)
                                print ("{} note, at time {}, for {}".format(noteValue[0], noteTime[0], duration), end="\r")
                                tracker = 1
                                noteValue = [midiNum]
                                noteTime = [totalTicks]
                    #if the note is empty
                    elif len(noteValue) == 0:
                            noteValue.append(midiNum)
                            noteTime.append(totalTicks)
                            tracker = 1
                    else:
                            #if note is the same as last, store value else, restart
                            if noteValue[tracker-1] == midiNum:
                                noteValue.append(midiNum)
                                noteTime.append(totalTicks)
                                tracker = len(noteValue)
                            else:
                                tracker = 1
                                noteValue = [midiNum]
                                noteTime = [totalTicks]
        delay = stream.get_time()-startTime
        #if the program ran slower than the required ticktime.
        if(TICKTIME-delay > 0):
            time.sleep(TICKTIME-delay)
        else:
            print("wrong")
        totalTicks = totalTicks+1


    #Stop Stream
    stream.stop_stream()
    stream.close()

    #close pyAudio
    p.terminate()
    wf = wave.open('recorded_audio.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(framez))
    wf.close()

    #build Midi
    buildMidi()
    return

#cProfile.run('main()')