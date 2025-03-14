from fastapi import FastAPI, File, UploadFile
import shutil
import os
from pathlib import Path
import librosa
import numpy as np
import soundfile as sf
import subprocess

app = FastAPI()

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "..\\..\\InstrumentalExtractorUI\\results_instruments"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def seperate_audio(audio_file):
    if os.path.exists(audio_file):
        print(f"Separating the audio: {audio_file}")
        command = ["demucs", audio_file]
        subprocess.run(command, check=True)

        file_name = Path(audio_file).stem
        output_folder = f"separated/htdemucs/{file_name}"
        return output_folder
    else:
        raise FileNotFoundError(f"Error: File '{audio_file}' not found!")

def create_instrumental(output_folder):
    print(f"Creating instrumental from: {output_folder}")
    files_to_combine = ["drums.wav", "bass.wav", "other.wav"]
    combined_signal = None
    sample_rate = None

    for file in files_to_combine:
        file_path = os.path.join(output_folder, file)
        signal, sr = librosa.load(file_path, sr=None)

        if combined_signal is None:
            combined_signal = signal
            sample_rate = sr
        else:
            combined_signal += signal

    combined_signal = combined_signal / np.max(np.abs(combined_signal))
    instrumental_output = os.path.join(RESULT_FOLDER, "instrumental.wav")
    sf.write(instrumental_output, combined_signal, sample_rate)

    return instrumental_output

@app.post("/extract")
async def extract_instrumental(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_folder = seperate_audio(file_location)
    instrumental_path = create_instrumental(output_folder)

    return {"instrumental_path": instrumental_path}
