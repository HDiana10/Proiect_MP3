# 🎵 Python MP3 Player

**Status:** Completed (University Project)  
**Tech Stack:** Python, CustomTkinter, Pygame

## 📄 Project Overview
This application is a feature-rich desktop media player designed to provide a modern user experience for local audio playback. Built using **Python**, it utilizes **CustomTkinter** for a polished, dark-mode-ready GUI and **Pygame** for the audio mixing engine.

The core engineering challenge was implementing a **multithreaded architecture** to decouple the UI event loop from the audio processing, ensuring the interface remains responsive during playback updates.

## ✨ Key Features
* **Modern GUI:** Designed with `customtkinter` for a responsive, high-DPI compatible interface.
* **Multithreaded Performance:** Uses Python's `threading` module to handle real-time timer updates and progress bar synchronization without freezing the main application loop.
* **Playlist Logic:** Custom algorithms for:
    * **Shuffle:** Randomized queue generation without repetition.
    * **Repeat:** Toggle between "Repeat One" and "Repeat All" states.
    * **Queue Management:** Dynamic addition and removal of tracks.
* **File Handling:** specific support for `.mp3` file parsing and metadata retrieval.

## 🛠️ Technologies Used
* **Language:** Python 3.x
* **GUI Framework:** CustomTkinter
* **Audio Engine:** `pygame.mixer`
* **Concurrency:** `threading` module

## 🚀 How to Run
To run this application locally, you will need Python installed.

1.  **Clone the repository**

2.  **Install Dependencies**
    ```bash
    pip install customtkinter pygame
    ```

3.  **Run the Application**
    ```bash
    python main.py
    ```

## 🔮 Future Improvements
* Add an equalizer visualization using Fast Fourier Transform (FFT) on the audio stream.
* Package the application as an executable (`.exe`) using PyInstaller.
