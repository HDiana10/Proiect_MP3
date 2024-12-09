from turtledemo.clock import current_day

from graphics import AppGUI
from music_functions import MusicControl, PlaylistManager

def main():
    # Inițializăm managerul de playlist
    playlist_manager = PlaylistManager()  # Corectat aici

    current_song_index = 0

    # Creăm interfața grafică
    app_gui = AppGUI(playlist_manager)

    # Creăm controlerul muzicii
    music_control = MusicControl(app_gui, playlist_manager, current_song_index)

    # Rulăm aplicația
    app_gui.run()

if __name__ == "__main__":
    main()
