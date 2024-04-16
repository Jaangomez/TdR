import librosa
import matplotlib.pyplot as plt

arxiu = "Sounds Judit/G (F3) Judit.wav"
temps1 = 1.0  
tempsfinal = 1.02   

def plot_waveform_in_time_range(arxiu, temps1, tempsfinal):
    y, sr = librosa.load(arxiu, sr=None, offset=temps1, duration=tempsfinal - temps1)

    duració_audio = librosa.times_like(y, sr=sr)/10

    plt.figure(figsize=(10, 4))
    plt.plot(duració_audio, y)
    plt.xlabel('Temps (s)')
    plt.ylabel('Amplitud')
    plt.title('El G (F3) tocat per la Judit')
    plt.show()


plot_waveform_in_time_range(arxiu, temps1, tempsfinal)