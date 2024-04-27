import librosa
import numpy as np

arxiu = 'Sounds/In a sentimental mood.wav'
y, sr = librosa.load(arxiu)

hop_length = 512

f0, voice_flag, voice_probs = librosa.pyin(y)

note_onsets = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)

notes = []
for onset in note_onsets:
    frame_start = onset * hop_length
    frame_end = frame_start + hop_length
    frame_f0 = f0[frame_start:frame_end]
    if np.any(frame_f0):
        median_f0 = np.median(frame_f0[frame_f0>0])
        note = librosa.hz_to_note (median_f0)
        notes.append(note)

print (notes)