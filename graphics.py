import customtkinter as ctk
from music_storage import MusicStorage
import os

class AppGui:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.music_storage = MusicStorage()
        self.current_playlist = "Default"  # Initialize the current playlist
        self.selected_song = None
        self.layout()

    def layout(self):
        self.root.geometry("1200x700")
        self.root.title("MP3 Player")

        # Configurare grilă pentru root
        self.root.columnconfigure(0, weight=1)  # Sidebar (coloana 0)
        self.root.columnconfigure(1, weight=3)  # Menu și center (coloana 1)
        self.root.rowconfigure(0, weight=3)  # Center (rândul 0)
        self.root.rowconfigure(1, weight=1)  # Menu (rândul 1)

        self.sidebar()
        self.menu()
        self.center()

    def sidebar(self):
        # Creează un sidebar
        sidebar = ctk.CTkFrame(self.root)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)  # Extinde pe toate rândurile din coloana 0

        # Configurați grila pentru sidebar
        sidebar.rowconfigure(0, weight=0)  # Rândul pentru titlu
        sidebar.rowconfigure(1, weight=0)  # Rândul pentru butonul "Create Playlist"
        sidebar.rowconfigure(2, weight=1)  # Rândul pentru playlist-uri (extindere maximă)
        sidebar.columnconfigure(0, weight=1)  # Extindere pe orizontală

        # Titlu sidebar
        title_sidebar = ctk.CTkLabel(sidebar, text="Playlists", font=("Helvetica", 20))
        title_sidebar.grid(row=0, column=0, pady=10)

        # Buton pentru crearea playlisturilor
        button_create_playlist = ctk.CTkButton(
            sidebar,
            text="Create Playlist",
            command=self.create_playlist_prompt,
            fg_color="white",
            text_color="black",
            hover_color="pink",
        )
        button_create_playlist.grid(row=1, column=0, pady=10)

        # Button to add new song(s)
        button_add_song_default = ctk.CTkButton(
            sidebar,
            text="Add Songs to Default",
            command= self.add_songs,
            fg_color="white",
            text_color="black",
            hover_color="pink",
        )
        button_add_song_default.grid(row=2, column=0, pady=10)

        # Creează un scrollbar pentru a afisa playlisturile
        self.playlist_frame = ctk.CTkScrollableFrame(sidebar, width=280, height=500, fg_color="#391326")
        self.playlist_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 10), padx=10)

        self.update_playlists_display()

    def add_songs(self):
        self.music_storage.add_song_to_playlist()
        self.update_center()

    def create_playlist_prompt(self):
        # Afișează o fereastră pentru a introduce numele playlist-ului
        dialog = ctk.CTkInputDialog(text="Enter playlist name:", title="Create Playlist")
        playlist_name = dialog.get_input()

        if playlist_name:
            self.music_storage.create_playlist(playlist_name)
            self.update_playlists_display()

    def update_playlists_display(self):
        print("Hello, ar trebui sa afisez cantecele acum")
        # sterge frame-ul existent
        for widget in self.playlist_frame.winfo_children():
            widget.destroy()

        # Adauga un label pentru fiecare playlist
        for playlist in self.music_storage.playlists:
            label = ctk.CTkLabel(
                self.playlist_frame,
                text=playlist,
                font=("Helvetica", 14),
                fg_color="transparent",
                anchor="w" # aliniaza textul la stanga
            )
            label.pack(fill="x", padx=10, pady=5)
            label.bind("<Button-1>", lambda event, p=playlist: self.select_playlist(p))  # Asociază clicul stânga

    def select_playlist(self, playlist_name):
        # Functia de selectie pentru un playlist
        self.current_playlist = playlist_name  # Setează playlistul selectat
        print(f"Playlist selected: {self.current_playlist}")
        self.update_center()

    def center(self):
        # Creează secțiunea "center"
        center = ctk.CTkFrame(self.root)
        center.grid(row=0, column=1, sticky="nsew", pady=10, padx=(0, 10))  # Poziționat sub menu
        center.grid_propagate(False)

        # Adaugă un label pentru secțiunea "center" care să afişeze numele playlistului curent
        self.center_label = ctk.CTkLabel(center, text=f"Playlist: {self.current_playlist}", font=("Helvetica", 20))
        self.center_label.pack(pady=10)

        # Creează un container pentru lista de melodii
        self.center_frame = ctk.CTkScrollableFrame(center, height=400, width=800, fg_color="#601f40")
        self.center_frame.pack(pady=10, padx=10, fill = "both", expand=True)
        self.center_frame.propagate(False)

        # Actualizează lista de melodii din playlistul curent
        self.update_center()

    def update_center(self):
        # Ștergeți widgeturile existente din secțiunea "center"
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        # Actualizează titlul playlistului curent
        self.center_label.configure(text=f"Playlist: {self.current_playlist}")  # Actualizează textul titlului

        # Obține lista de melodii din playlistul curent
        songs = self.music_storage.playlists[self.current_playlist]

        # Adăugăm fiecare melodie în lista din secțiunea "center"
        for song in songs:
            song_button = ctk.CTkButton(
                self.center_frame,
                text=os.path.basename(song),  # Afișează doar numele fișierului
                font=("Helvetica", 14),
                anchor="w",
                fg_color=("transparent" if song != self.selected_song else "pink"),
                hover_color="purple",
                # Schimbă culoarea butonului dacă este selectat
                command=lambda s=song: self.select_song(s)
            )
            song_button.pack(fill="x", padx=10, pady=5)

    def select_song(self, song):
        # Actualizează melodia selectată și schimbă culoarea butonului
        self.selected_song = song
        print(f"Song selected: {os.path.basename(song)}")
        self.update_center()  # Reîmprospătează lista cu melodiile pentru a evidenția selecția

    def menu(self):
        # Creează un meniu
        menu = ctk.CTkFrame(self.root, fg_color="#13060d")
        menu.grid(row=1, column=1, sticky="nsew", padx=(0,10), pady=(0,10))  # Poziționat în partea de sus
        menu.grid_propagate(False)

        # Adaugă un label în meniu
        menu_label = ctk.CTkLabel(menu, text="Menu", font=("Helvetica", 20))
        menu_label.pack(pady=10)

    def run(self):
        self.root.mainloop()
