import argparse
import subprocess
import os
from pathlib import Path
import sys
import librosa 
import numpy as np
import soundfile as sf


def seperate_audio(audio_file):

    audio_file  =  ".\\test_data\\" + audio_file
    if os.path.exists(audio_file):
        print(f" Seperating the audio: {audio_file}")
        command = ["demucs",audio_file]
        subprocess.run(command, check=True)

        audio_file =  Path(audio_file)
        file_name = audio_file.stem
        output_folder = f"separated/htdemucs/{file_name}"
        return output_folder
    else:
        print(f"❌ Error: File '{audio_file}' not found!")

def creat_instrumental(audio_path):
    files_list = [audio for audio in os.listdir(audio_path) if audio != "vocals.wav"]
    
    combined_signal = None
    sample_rate = None
    
    for file in files_list:
        singl_audio = os.path.join(audio_path,file)

        signal ,sr =  librosa.load(singl_audio, sr = None)
        if combined_signal == None:
            combined_signal = signal
            sampling_rate = sr
        else:
            combined_signal += signal 

    combined_signal = combined_signal / np.max(np.abs(combined_signal))
    instrumental_output = os.path.join(audio_path, "instrumental.wav")
    sf.write(instrumental_output, combined_signal, sample_rate)
    
    print(f"✅ Instrumental saved as: {instrumental_output}")
    return instrumental_output


# Function to combine separated tracks (without vocals)
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

    # Save the final instrumental file
    instrumental_output = os.path.join(output_folder, "instrumental.wav")
    sf.write(instrumental_output, combined_signal, sample_rate)
    
    print(f"✅ Instrumental saved as: {instrumental_output}")
    return instrumental_output
def main():
    parser = argparse.ArgumentParser(description="Automatically extract instrumental from an audio file.")
    parser.add_argument("audio_file", type=str, help="Path to the input audio file")
    parser.add_argument("audio_output",type=str, help="Path to the output audio file")
    args = parser.parse_args()

    separated_audio_folder = seperate_audio(args.audio_file)
    print(separated_audio_folder)
    # Step 2: Create instrumental version
    instrumental_path = create_instrumental(separated_audio_folder)

    print(f"🎵 Done! Your instrumental is at: {instrumental_path}")

if __name__ == "__main__":
    sys.argv = ["script_name.py", "2Sba3.mp3", "output_audio.mp3"]
    main()