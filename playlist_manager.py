from tkinter import filedialog
import os


class PlaylistManager:
    def __init__(self):
        # Initialize `Default` as a list to store full file paths
        self.Default = []
        # Initialize `playlists` as a dictionary to store playlists with (id, song name)
        self.playlists = {"Default": []}
        #self.load_default_from_folder(r"C:\Users\Diana\Music")

        # Determină calea implicită pentru folderul "Music" din directorul utilizatorului
        user_profile = os.environ.get("USERPROFILE", "")
        music_folder = os.path.join(user_profile, "Music") if user_profile else None

        # Verifică dacă folderul implicit există
        if music_folder and os.path.exists(music_folder):
            folder_path = music_folder
            # Încarcă fișierele MP3 din folderul selectat
            if folder_path:
                self.load_default_from_folder(folder_path)

    def load_default_from_folder(self, folder_path):
        """Populează lista Default și playlist-ul cu fișiere .mp3 dintr-un folder dat."""
        try:
            # Parcurge toate fișierele din folder
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(".mp3"):
                        full_path = os.path.join(root, file)
                        if full_path not in self.Default:
                            self.Default.append(full_path)
                            song_id = len(self.Default) - 1  # Index of the newly added song
                            song_name = os.path.basename(full_path)  # Extract the file name
                            # Add (id, song_name) to the "Default" playlist
                            self.playlists["Default"].append((song_id, song_name))
                            print(f"Loaded: ID={song_id}, Name={song_name}")
            # Sortează lista după numele fișierelor
            # self.Default = sorted(self.Default)
            # self.playlists["Default"] = sorted(self.playlists["Default"], key=lambda x: x[1])
        except Exception as e:
            print(f"Error loading songs from folder: {e}")

    def create_playlist(self, name):
        """Creeaza un playlist nou"""
        if name in self.playlists:
            print(f"Playlist {name} already exists")
            return False
        else:
            self.playlists[name] = []  # Create an empty playlist
            print(f"Playlist {name} created!")
            return True

    def add_song_to_default(self):
        """Permite utilizatorului sa adauge cantece"""
        file_paths = filedialog.askopenfilenames(
            title="Selectează fișiere MP3",
            filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")]
        )
        if file_paths:
            for file_path in file_paths:
                # Add the full file path to `self.Default`
                if file_path not in self.Default:
                    self.Default.append(file_path)
                    song_id = len(self.Default) - 1  # Index of the newly added song
                    song_name = os.path.basename(file_path)  # Extract the file name
                    # Add (id, song_name) to the "Default" playlist
                    self.playlists["Default"].append((song_id, song_name))
                    print(f"Added to Default: ID={song_id}, Name={song_name}")
                else:
                    print(f"Song {file_path} already exists in Default.")
        self.Default = sorted(self.Default)
        self.playlists['Default'] = sorted(self.playlists['Default'], key=lambda x: x[1])

    def get_song(self, index, playlist):
        """Returnează melodia de la un index specificat din playlist"""
        if 0 <= index < len(self.playlists[playlist]):
            song_id, song_name = self.playlists[playlist][index]  # Extrage tuplul
            print(f"Song id = {song_id}, song name = {song_name}")
            return self.Default[song_id]
        else:
            print(f"Index invalid: {index} pentru playlistul {playlist}.")
            return None

    def get_next_song(self, index, playlist):
        """Returneaza melodia urmatoare"""
        index = index + 1
        if index == len(self.playlists[playlist]): # verify if we reached the end of the playlist
            index = 0
        song_id, song_name = self.playlists[playlist][index]
        return index, self.Default[song_id]

    def get_previous_song(self, index, playlist):
        index = index - 1
        if index < 0: # verify if we reached the end of the playlist
            index = len(self.playlists[playlist]) - 1
        song_id, song_name = self.playlists[playlist][index]
        return index, self.Default[song_id]

