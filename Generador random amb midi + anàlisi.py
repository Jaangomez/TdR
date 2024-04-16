import random
import pygame.midi
import time
import rtmidi

# Initialize Pygame and the MIDI module
pygame.init()
pygame.midi.init()

# Open a MIDI output device (change the device ID as needed)
output_device_id = pygame.midi.get_default_output_id()
midi_output = pygame.midi.Output(output_device_id)

# Define musical parameters
scale = [60, 62, 64, 65, 67, 69, 71]  # C major scale (MIDI note numbers)
tempo = 120  # Beats per minute (BPM)
num_notes = 16  # Number of notes in the melody

# Generate random melody
melody = []
time = 0
for _ in range(num_notes):
    note = random.choice(scale)  # Randomly select a note from the scale
    duration = random.uniform(0.25, 1.0)  # Random duration between 0.25 and 1.0 beats
    melody.append((note, duration))
    time += duration

# Play the melody
beat_duration = 60 / tempo  # Duration of one beat in seconds
for note, duration in melody:
    # Play the note
    midi_output.note_on(note, velocity=127)
    time.sleep(duration * beat_duration)  # Wait for the duration of the note
    midi_output.note_off(note)

# Close the MIDI output device
del midi_output

# Quit Pygame
pygame.midi.quit()
pygame.quit()
