import os
import threading
from pygame import mixer
from tkinter import filedialog, END


# **Clasa PlaylistManager - Gestionarea playlist-ului**
class PlaylistManager:
    def __init__(self):
        self.playlist = []  # Lista de melodii
        self.listbox = None  # Va fi conectat la Listbox-ul din GUI

    def set_listbox(self, app_gui):
        """Setează lista (Listbox) din GUI pentru actualizare"""
        self.listbox = app_gui.Playlist

    def add_music(self):
        """Permite utilizatorului să adauge melodii dintr-un folder"""
        folder_path = filedialog.askdirectory(title="Selectează un folder cu piese muzicale")
        if folder_path:
            os.chdir(folder_path)  # Schimbă directorul curent
            files = os.listdir(folder_path)  # Obține lista fișierelor din director
            for file in files:
                if file.endswith(".mp3"):  # Adaugă doar fișierele MP3
                    self.playlist.append(file)
                    if self.listbox:
                        self.listbox.insert(END, file)

    def get_playlist(self):
        """Returnează lista completă de melodii"""
        return self.playlist

    def get_song(self, index):
        """Returnează melodia de la un index specificat din playlist"""
        if 0 <= index < len(self.playlist):
            return self.playlist[index]
        return None



class MusicControl:
    def __init__(self, app_gui, playlist_manager, current_song_index):
        self.app_gui = app_gui
        self.playlist_manager = playlist_manager
        self.current_song_index = current_song_index
        self.pause_time = -1
        self.is_playing = False
        self.song_duration = 0
        self.stop_thread_event = threading.Event()  # Eveniment pentru a opri thread-ul
        mixer.init()  # Inițializează mixerul

    def update_time_scale(self):
        """Actualizează cursorul TimeScale și eticheta cu timpul curent"""
        while not self.stop_thread_event.is_set():
            if mixer.music.get_busy():  # Verifică dacă piesa este în continuare redată
                current_pos = mixer.music.get_pos() / 1000  # Timpul curent în secunde
                current_min = int(current_pos // 60)
                current_sec = int(current_pos % 60)
                song_min = int(self.song_duration // 60)
                song_sec = int(self.song_duration % 60)

                # Actualizează cursorul TimeScale și eticheta de timp curent
                self.app_gui.TimeScale.set(current_pos)
                self.app_gui.time_label.config(text=f"{current_min:02}:{current_sec:02} / {song_min:02}:{song_sec:02}")

            threading.Event().wait(1)  # Așteaptă 1 secundă înainte de a actualiza din nou

    def add_music(self):
        """Adaugă muzică în playlist prin selectarea unui folder"""
        self.playlist_manager.add_music()  # Apelează metoda din PlaylistManager
        self.app_gui.update_playlist()  # Actualizează GUI-ul pentru a afișa playlist-ul actualizat

    def play_music(self):
        """Pornește redarea melodiei"""
        music_name = self.playlist_manager.get_song(self.current_song_index)
        if not music_name:  # Dacă nu există o piesă selectată
            return

        if self.pause_time > 0:
            # Reluăm melodia de la timpul salvat
            mixer.music.unpause()
            self.pause_time = 0  # Resetăm timpul de pauză
        else:
            # Încărcăm și redăm melodia de la început
            mixer.music.load(music_name)
            mixer.music.play()
            self.song_duration = mixer.Sound(music_name).get_length()

        # Schimb numele piesei curente
        clean_name = os.path.splitext(music_name)[0]  # Elimină extensia .mp3
        self.app_gui.song_name_label.config(text=f"{clean_name}")

        self.is_playing = True

        # Inițializează progresul într-un thread dedicat
        self.stop_thread_event.clear()
        threading.Thread(target=self.update_time_scale, daemon=True).start()

        # Actualizează selecția în playlist
        self.app_gui.Playlist.select_clear(0, END)
        self.app_gui.Playlist.select_set(self.current_song_index)

    def pause_music(self):
        """Pune muzica pe pauză"""
        mixer.music.pause()
        self.pause_time = mixer.music.get_pos() / 1000  # Salvează timpul curent al melodiei
        self.is_playing = False
        self.stop_thread_event.set()  # Oprește thread-ul de actualizare a progresului

    def stop_music(self):
        """Oprește redarea muzicii"""
        mixer.music.stop()
        self.is_playing = False
        self.stop_thread_event.set()  # Oprește thread-ul de actualizare a progresului

    def next_music(self):
        """Redă următoarea melodie din playlist"""
        self.stop_music()
        if self.current_song_index < len(self.playlist_manager.get_playlist()) - 1:
            self.current_song_index += 1
        else:
            self.current_song_index = 0
        self.play_music()

    def previous_music(self):
        """Redă melodia anterioară din playlist"""
        self.stop_music()
        if self.current_song_index > 0:
            self.current_song_index -= 1
        else:
            self.current_song_index = len(self.playlist_manager.get_playlist()) - 1
        self.play_music()
