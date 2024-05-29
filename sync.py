## For syncing ##
import librosa
import numpy as np
import os

# Augmentation functions
def time_stretch(audio, rate=1.1):
    return librosa.effects.time_stretch(audio, rate)

def pitch_shift(audio, sr, n_steps=2):
    return librosa.effects.pitch_shift(audio, sr, n_steps)

def add_noise(audio, noise_level=0.005):
    noise = np.random.randn(len(audio))
    augmented_audio = audio + noise_level * noise
    return augmented_audio

def volume_adjust(audio, gain=1.5):
    return audio * gain

# Function to augment a single audio file multiple ways
def augment_audio_file(audio_file, sr):
    augmented_audios = []
    audio, _ = librosa.load(audio_file, sr=sr)

    # Original
    augmented_audios.append(audio)

    # Time stretching
    augmented_audios.append(time_stretch(audio, rate=1.1))
    augmented_audios.append(time_stretch(audio, rate=0.9))

    # Pitch shifting
    augmented_audios.append(pitch_shift(audio, sr, n_steps=2))
    augmented_audios.append(pitch_shift(audio, sr, n_steps=-2))

    # Adding noise
    augmented_audios.append(add_noise(audio, noise_level=0.005))
    augmented_audios.append(add_noise(audio, noise_level=0.01))

    # Volume adjustment
    augmented_audios.append(volume_adjust(audio, gain=1.5))
    augmented_audios.append(volume_adjust(audio, gain=0.5))

    return augmented_audios

# Directory to save augmented files
augmented_path = 'path_to_augmented_audio/'

# Create the directory if it doesn't exist
os.makedirs(augmented_path, exist_ok=True)

# Load and augment your normal engine noise files
normal_files_path = 'path_to_normal_audio_files/'
sr = 22050  # Example sampling rate

for file_name in os.listdir(normal_files_path):
    if file_name.endswith('.wav'):
        file_path = os.path.join(normal_files_path, file_name)
        augmented_audios = augment_audio_file(file_path, sr)
        
        for idx, augmented_audio in enumerate(augmented_audios):
            augmented_file_path = os.path.join(augmented_path, f"{file_name.replace('.wav', '')}_augmented_{idx}.wav")
            librosa.output.write_wav(augmented_file_path, augmented_audio, sr)
