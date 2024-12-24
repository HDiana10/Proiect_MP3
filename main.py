from graphics import AppGui
from playlist_manager import PlaylistManager

def main():
    # Creează instanța de MusicStorage
    music_storage = PlaylistManager()

    # Creează instanțele pentru AppGui și MusicControl
    app_gui = AppGui(music_storage)

    # Rulăm aplicația
    app_gui.run()

if __name__ == "__main__":
    main()
