# 🎵 Instrumental Audio Extractor 🎶

This project **automates the extraction of instrumental tracks** from audio files by separating vocals, drums, bass, and other components. It uses **Demucs**, a deep learning-based source separation tool, to process music files and reconstruct the instrumental version **without vocals**.

## 🚀 Features
- **Automated Audio Processing** – Just provide an audio file, and the script does the rest.  
- **Deep Learning-Based Separation** – Uses **Demucs** to split tracks.  
- **Rebuilds the Instrumental** – Combines drums, bass, and other elements into a final instrumental track.  
- **Fully Scripted** – No manual work required.  

## 🛠️ How It Works
1. **Separates the input audio** into multiple tracks: `vocals.wav`, `drums.wav`, `bass.wav`, and `other.wav`.
2. **Removes the vocals** and reconstructs an instrumental version.
3. **Saves the final instrumental file** as `instrumental.wav`.

## 📦 Installation
Make sure you have **Python 3.9+** installed.

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/instrumental-extractor.git
cd instrumental-extractor
