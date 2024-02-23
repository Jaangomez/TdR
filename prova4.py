import wave
w = wave.open('ray-charles.wav', 'r')
for i in range(w.getnframes()):
    frame = w.readframes(i)
    print; frame



