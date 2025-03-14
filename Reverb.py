import argparse
import subprocess
import os
from pathlib import Path
import sys
import librosa 
import numpy as np
import soundfile as sf
from scipy.signal import lfilter

class ReverbEffect:
    def __init__(self, decay=0.5, delay=0.02, sampling_rate=44100):
        self.decay = decay  # How much echo is added
        self.delay = delay  # Delay time in seconds
        self.sampling_rate = sampling_rate  # Default sampling rate

    def apply_reverb(self, audio_signal):
        delay_samples = int(self.sampling_rate * self.delay)
        impulse_response = np.zeros(delay_samples * 2)
        impulse_response[::delay_samples] = self.decay  # Create a delayed signal
        
        # Apply convolution (Reverb effect)
        reverb_signal = lfilter(impulse_response, [1.0], audio_signal)
        return reverb_signal

def separate_audio(audio_file):
    audio_file = f"./test_data/{audio_file}"
    if os.path.exists(audio_file):
        print(f"🎼 Separating the audio: {audio_file}")
        command = ["demucs", audio_file]
        subprocess.run(command, check=True)
        
        file_name = Path(audio_file).stem
        output_folder = f"separated/htdemucs/{file_name}"
        return output_folder
    else:
        print(f"❌ Error: File '{audio_file}' not found!")
        return None

def create_instrumental(output_folder):
    print(f"🔹 Creating instrumental from: {output_folder}")
    
    files_to_combine = ["drums.wav", "bass.wav", "other.wav"]  # Ignore vocals
    combined_signal = None
    sample_rate = None

    for file in files_to_combine:
        file_path = os.path.join(output_folder, file)
        signal, sr = librosa.load(file_path, sr=None)  # Load the file
        
        if combined_signal is None:
            combined_signal = signal  # Initialize with first track
            sample_rate = sr
        else:
            combined_signal += signal  # Sum all waveforms

    # Normalize the audio
    combined_signal = combined_signal / np.max(np.abs(combined_signal))
    instrumental_output = os.path.join(output_folder, "instrumental.wav")
    sf.write(instrumental_output, combined_signal, sample_rate)
    
    print(f"✅ Instrumental saved as: {instrumental_output}")
    return instrumental_output

def main():
    parser = argparse.ArgumentParser(description="Automatically extract instrumental and apply reverb effect.")
    parser.add_argument("audio_file", type=str, help="Path to the input audio file")
    args = parser.parse_args()

    separated_audio_folder = separate_audio(args.audio_file)
    if separated_audio_folder:
        instrumental_path = create_instrumental(separated_audio_folder)
        
        # Apply Reverb
        reverb = ReverbEffect(decay=0.5, delay=0.03)  # Create a ReverbEffect instance
        print(f"🎛️ Applying reverb to: {instrumental_path}")
        
        signal, sr = librosa.load(instrumental_path, sr=None)
        processed_signal = reverb.apply_reverb(signal)
        
        reverb_output = os.path.join(separated_audio_folder, "instrumental_reverb.wav")
        sf.write(reverb_output, processed_signal, sr)
        print(f"✨ Reverb effect applied! Saved as: {reverb_output}")

if __name__ == "__main__":
    sys.argv = ["script_name.py", "2Sba3.mp3"]
    main()
