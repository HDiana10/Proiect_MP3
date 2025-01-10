from tkinter import filedialog
import os
class MusicStorage:
    def __init__(self):
        # Initialize self.playlists as a dictionary with 'Default' as a key and an empty list as its value
        self.playlists = {"Default": []}  # Use a dictionary instead of a set

    def create_playlist(self, name):
        if name in self.playlists:
            print(f"Playlist {name} already exists")
            return False
        else:
            self.playlists[name] = []  # Create an empty list for the new playlist
            print(f"Playlist {name} created!")
            return True

    def add_song_to_playlist(self):
        """Lets the user to upload .mp3 files to the default playlist"""
        file_paths = filedialog.askopenfilenames(
            title="Selectează fișiere MP3",
            filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")]
        )
        if file_paths:
            for file_path in file_paths:
                self.playlists["Default"].append(file_path)
                print(f"Playlist {file_path} added!")