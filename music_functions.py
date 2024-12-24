from random import shuffle

from pygame import mixer
import os, random

mixer.init()  # Inițializează mixer-ul pentru a reda muzica

class MusicControl:
    def __init__(self, playlist_manager, toggle_repeat, toggle_shuffle):
        self.playlist_manager = playlist_manager  # Obiect pentru gestionarea playlist-urilor
        self.repeat = toggle_repeat
        self.shuffle = toggle_shuffle
        self.pause_time = 0
        self.is_playing = False
        self.current_song = None
        self.current_song_id = -1
        self.current_playlist = None

    def play_song(self, song_id, playlist):
        if self.pause_time != 0 and song_id == self.current_song_id and self.current_playlist == playlist:
            # Reluăm melodia de la timpul salvat
            mixer.music.unpause()
            self.pause_time = 0  # Resetăm timpul de pauză
        else:
            self.current_song_id = song_id
            self.current_playlist = playlist

            # Obține calea fișierului melodiilor din playlist
            self.current_song = self.playlist_manager.get_song(song_id, playlist)
            print(f"Music name: {self.current_song}")

            mixer.music.load(self.current_song)  # Încarcă fișierul audio
            mixer.music.play()  # Redă melodia
            self.is_playing = True
            return os.path.splitext(os.path.basename(self.current_song))[0]

    def pause_song(self):
        mixer.music.pause()
        self.pause_time = mixer.music.get_pos() / 1000  # Salvează timpul curent al melodiei
        self.is_playing = False

    def stop_song(self):
        self.current_song = None
        self.current_song_id = None
        mixer.music.stop()

    def next_song(self):

        length = len(self.playlist_manager.playlists[self.current_playlist]) - 1

        if self.shuffle:
            song_index = random.randint(0, length)  # Dacă shuffle este activ
            while song_index == self.current_song_id:
                song_index = random.randint(0, length)
            self.current_song_id = song_index

        elif self.repeat == 1:
            self.current_song_id = self.current_song_id + 1
            if self.current_song_id == length:  # verify if we reached the end of the playlist
                self.current_song_id = 0

        self.current_song_id, self.current_song= self.playlist_manager.get_next_song(self.current_song_id, self.current_playlist)
        mixer.music.load(self.current_song)
        mixer.music.play()

        return self.current_song_id, os.path.splitext(os.path.basename(self.current_song))[0]

    def previous_song(self):
        self.current_song_id, self.current_song = self.playlist_manager.get_previous_song(self.current_song_id, self.current_playlist)
        mixer.music.load(self.current_song)
        mixer.music.play()

        return self.current_song_id, os.path.splitext(os.path.basename(self.current_song))[0]

    def on_song_end(self):
        print(f"Am ajuns la finalul cantecului {self.current_song}\n repeat = {self.repeat} and shuffle = {self.shuffle}")
        if self.shuffle or self.repeat == 1:
            return self.next_song()
        elif self.repeat == 2:
            return self.current_song_id, self.play_song(self.current_song_id, self.current_playlist)


    def get_song_duration(self):
        return mixer.Sound(self.current_song).get_length()

    def get_current_time(self):
        return mixer.music.get_pos() / 1000

    def update_song_position(self, time):
        if self.is_playing:
            mixer.music.stop()
            mixer.music.play(start = time)

        else:
            self.pause_time = time