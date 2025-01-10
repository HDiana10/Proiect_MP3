import customtkinter as ctk
from music_functions import MusicControl
import os
from PIL import Image, ImageTk
import functools

class AppGui:
    def __init__(self, playlist_manager):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk() # interfata
        self.playlist_manager = playlist_manager
        self.current_playlist = "Default"  # Initializeaza playlistul curent
        self.current_song = None
        self.song_index = 0
        self.song_duration = 0
        self.toggle_play_pause = 0
        self.shuffle = 0
        self.repeat = 0
        self.music_control = MusicControl(playlist_manager, self.repeat, self.shuffle) # clasa din music_functions
        self.update_id = None  # Variabilă pentru stocarea ID-ului after
        self.const_time = 0
        self.current_time = 0

        #interface
        self.menu = None
        self.playlist_frame = None
        self.center_label = None
        self.center_frame = None
        self.TimeScale = None
        self.SongLabel = None
        self.TimeLabel = None

        # images
        self.play_image = Image.open("images/play_button.png").resize((120, 120))
        self.play_image = ImageTk.PhotoImage(self.play_image)

        self.pause_image = Image.open("images/pause_button.png").resize((120, 120))
        self.pause_image = ImageTk.PhotoImage(self.pause_image)

        self.shuffle_image_on = Image.open("images/shuffle_button_on.png").resize((120, 120))
        self.shuffle_image_on = ImageTk.PhotoImage(self.shuffle_image_on)

        self.shuffle_image_off = Image.open("images/shuffle_button_off.png").resize((120, 120))
        self.shuffle_image_off = ImageTk.PhotoImage(self.shuffle_image_off)

        self.repeat_image_on = Image.open("images/repeat_button_on.png").resize((120, 120))
        self.repeat_image_on = ImageTk.PhotoImage(self.repeat_image_on)

        self.repeat_image_off = Image.open("images/repeat_button_off.png").resize((120, 120))
        self.repeat_image_off = ImageTk.PhotoImage(self.repeat_image_off)

        self.repeat_image_2 = Image.open("images/repeat_button_2.png").resize((120, 120))
        self.repeat_image_2 = ImageTk.PhotoImage(self.repeat_image_2)

        self.stop_image = Image.open("images/stop_button.png").resize((120, 120))
        self.stop_image = ImageTk.PhotoImage(self.stop_image)

        self.previous_image = Image.open("images/previous_button.png").resize((120, 120))
        self.previous_image = ImageTk.PhotoImage(self.previous_image)

        self.next_image = Image.open("images/next_button.png").resize((120, 120))
        self.next_image = ImageTk.PhotoImage(self.next_image)

        # Butoane
        self.TogglePlayButton = None
        self.ToggleShuffleButton = None
        self.ToggleRepeatButton = None
        self.NextButton = None
        self.PreviousButton = None
        self.StopButton = None

        self.layout()

    def layout(self):
        """"Layoutul principal al aplicatiei"""
        self.root.geometry("1200x700")
        self.root.title("MP3 Player")

        # Configurare grilă pentru root
        self.root.columnconfigure(0, weight=1)  # Sidebar (coloana 0)
        self.root.columnconfigure(1, weight=3)  # Menu și center (coloana 1)
        self.root.rowconfigure(0, weight=4)  # Center (rândul 0)
        self.root.rowconfigure(1, weight=0)  # Menu (rândul 1)

        self.sidebar_setup()
        self.menu_setup()
        self.center_setup()

    def sidebar_setup(self):
        """Creează un sidebar pentru playlists"""
        sidebar = ctk.CTkFrame(self.root, fg_color="#A20582")
        sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Configurați grila pentru sidebar
        sidebar.rowconfigure(0, weight=1)  # Rândul pentru butoane
        sidebar.rowconfigure(1, weight=0)  # Rândul pentru titlu
        sidebar.rowconfigure(2, weight=0)  # Rândul pentru playlist_frame (extinde maxim)
        sidebar.columnconfigure(0, weight=1)  # Coloana unică

        # Titlu sidebar
        title_sidebar = ctk.CTkLabel(
            sidebar,
            text="Playlists",
            font=("Roboto", 24),
            anchor="center"
        )
        title_sidebar.grid(row=1, column=0, pady=5)

        # Container pentru butoane
        button_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        button_container.grid(row=0, column=0, pady=5)

        # Configureaza grila pentru containerul de butoane
        button_container.columnconfigure(0, weight=0)
        button_container.columnconfigure(1, weight=0)


        # Butoane în container
        button_create_playlist = ctk.CTkButton(
            button_container,
            text="Create Playlist",
            command=self.create_playlist_prompt,
            fg_color="white",
            text_color="black",
            hover_color="magenta",
        )
        button_create_playlist.grid(row=0, column=0, padx=(0, 5))

        button_add_song_default = ctk.CTkButton(
            button_container,
            text="Add Songs to Default",
            command=self.add_songs,
            fg_color="white",
            text_color="black",
            hover_color="magenta",
        )
        button_add_song_default.grid(row=0, column=1, padx=(5, 0))

        # Creează un scrollbar pentru a afișa playlisturile
        self.playlist_frame = ctk.CTkScrollableFrame(sidebar, width=280, height=560, fg_color="#ffb3d7")
        self.playlist_frame.grid(row=2, column=0, sticky="nsew", pady=(10, 10), padx=10)

        # Actualizează afisarea playlisturilor
        self.update_playlists_display()

    def add_songs(self):
        """Adauga cantectul si updateaza center"""
        self.playlist_manager.add_song_to_default()
        self.update_center()

    def create_playlist_prompt(self):
        """Afișează o fereastră pentru a introduce numele playlist-ului"""
        dialog = ctk.CTkInputDialog(text="Enter playlist name:", title="Create Playlist")
        playlist_name = dialog.get_input()

        if playlist_name:
            self.playlist_manager.create_playlist(playlist_name)
            self.update_playlists_display()

    def update_playlists_display(self):
        """Reafiseaza lista de playlisturi atunci cand se adauga unul nou"""

        # sterge frame-ul existent
        for widget in self.playlist_frame.winfo_children():
            widget.destroy()

        # Adauga un label pentru fiecare playlist
        for playlist in self.playlist_manager.playlists:
            label = ctk.CTkLabel(
                self.playlist_frame,
                text=playlist,
                font=("Helvetica", 16),
                fg_color="transparent",
                text_color="Purple",
                anchor="w" # aliniaza textul la stanga
            )
            label.pack(fill="x", padx=10, pady=5)
            label.bind("<Button-1>", lambda event, p=playlist: self.select_playlist(p))  # Asociază clicul stânga

            # Adaugă efect hover
            label.bind("<Enter>", lambda event, l=label: l.configure(fg_color="pink"))  # Schimbă culoarea de fundal
            label.bind("<Leave>", lambda event, l=label: l.configure(fg_color="transparent"))  # Revine la fundal transparent

    def select_playlist(self, playlist_name):
        """Functia de selectie pentru un playlist"""
        self.current_playlist = playlist_name  # Setează playlistul selectat
        print(f"Playlist selected: {self.current_playlist}")
        self.update_center()

    def center_setup(self):
        """Creează secțiunea center"""
        center = ctk.CTkFrame(self.root, fg_color="#C7439D")
        center.grid(row=0, column=1, sticky="nsew", pady=10, padx=(0, 10))  # Poziționat sub menu
        center.grid_propagate(False)

        # Configurează grila pentru "center"
        center.rowconfigure(0, weight=0)  # Rândul pentru label
        center.rowconfigure(1, weight=1)  # Rândul pentru frame
        center.columnconfigure(0, weight=1)  # Coloană 0, extindere pe orizontală
        center.columnconfigure(1, weight=1)  # Coloană 1, extindere pe orizontală

        # Adaugă un label pentru secțiunea "center"
        self.center_label = ctk.CTkLabel(center, text="Current Playlist", font=("Helvetica", 24))
        self.center_label.grid(row=0, column=0, pady=10, sticky="w")  # Aliniază la stânga (west)

        # Adaugă un buton pentru a adăuga melodii în playlist
        #self.add_songs_to_playlist = ctk.CTkButton(center, text="Add Songs", font=("Helvetica", 14), command=self.open_song_selection_window)
        #self.add_songs_to_playlist.grid(row=0, column=1, pady=10, padx=10, sticky="e")  # Aliniază la dreapta (east)

        # Creează un container pentru lista de melodii
        self.center_frame = ctk.CTkScrollableFrame(center, fg_color="#ffb3d7")
        self.center_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10), padx=10)

        # Actualizează lista de melodii din playlistul curent
        self.update_center()

    def update_center(self):
        """Ștergeți widgeturile existente"""
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        # Actualizează titlul playlistului curent
        self.center_label.configure(text=f"Playlist: {self.current_playlist}")

        # Adăugăm fiecare melodie
        for song_id, song_name in self.playlist_manager.playlists[self.current_playlist]:
            song_button = ctk.CTkButton(
                self.center_frame,
                text=os.path.splitext(song_name)[0],  # Afișează doar numele fișierului
                font=("Helvetica", 16),
                anchor="w",
                fg_color=("transparent" if song_id != self.song_index else "#75025D"),
                hover_color="magenta",
                command=lambda s_id=song_id: self.select_song(s_id)
            )
            song_button.pack(fill="x", padx=10, pady=(5, 0))

    def select_song(self, song_id):
        """ Actualizează melodia selectată"""
        self.song_index = song_id
        self.current_song = self.playlist_manager.Default[song_id]
        print(f"Song selected: {os.path.basename(self.current_song)}")
        self.toggle_play_pause = 0
        self.toggle_play()
        self.update_center()  # Reîmprospătează lista pentru a evidenția selecția

    def menu_setup(self):
        """Creează un meniu pentru player"""
        menu = ctk.CTkFrame(self.root, fg_color="#75025D")
        menu.grid(row=1, column=1, sticky="nsew", padx=(0, 10), pady=(0, 10))
        menu.grid_propagate(False)

        # Configurează coloanele pentru a permite plasarea widget-urilor la dreapta
        menu.grid_columnconfigure(0, weight=1)  # Coloana 0 se va extinde pentru a face loc widget-urilor
        menu.grid_columnconfigure(1, weight=0)  # Coloana 1 va fi folosită doar pentru imagine

        # Adaugă imaginea pentru volum
        volume_image = Image.open("images/volume.png").resize((40, 40))
        volume_image = ImageTk.PhotoImage(volume_image)

        volume_image_label = ctk.CTkLabel(menu, image=volume_image, text="")
        volume_image_label.image = volume_image  # Păstrează referința imaginii
        volume_image_label.grid(row=0, column=0, sticky="ne", padx=(10, 0), pady=25)  # Poziționează imaginea în dreapta

        # Volume scale
        VolumeScale = ctk.CTkSlider(
            menu,
            from_=0,
            to=100,
            width=100,
            fg_color="magenta",
            progress_color="pink",
            button_color="purple",
            button_hover_color="purple",
            command=self.update_volume,
        )
        VolumeScale.grid(row=0, column=1, sticky="ne", padx=(0, 10),pady=(30, 0))  # Poziționează VolumeScale în dreapta

        VolumeScale.set(100)


        # Adaugă un label în meniu
        self.SongLabel = ctk.CTkLabel(menu, text="No song playing", font=("Helvetica", 20))
        self.SongLabel.pack(pady=(30, 0))

        # Temporizator
        self.TimeLabel = ctk.CTkLabel(menu, text="00:00 / 00:00", font=("Helvetica", 20))
        self.TimeLabel.pack(pady=(10, 5))

        # Time Scale
        self.TimeScale = ctk.CTkSlider(
            menu,
            from_=0,
            to=100,
            width=600,
            fg_color="pink",
            progress_color="magenta",
            button_color="purple",
            button_hover_color="purple"
        )
        # Asociază evenimentul de eliberare a click-ului cu funcția `update_time_on_release`
        self.TimeScale.bind("<ButtonRelease-1>", self.update_time)

        self.TimeScale.pack(pady=(5, 5))
        self.TimeScale.set(0)

        self.buttons(menu)

    def update_volume(self, val):
        volume = float(val)/100
        self.music_control.update_volume(volume)

    def update_time_scale(self):
        """Actualizează scala de timp automat"""
        self.current_time = self.music_control.get_current_time()
        self.TimeScale.set((self.current_time + self.const_time))

        current_min = int((self.current_time + self.const_time) // 60)
        current_sec = int((self.current_time + self.const_time) % 60)
        song_min = int(self.song_duration // 60)
        song_sec = int(self.song_duration % 60)

        self.TimeLabel.configure(text=f"{current_min:02}:{current_sec:02} / {song_min:02}:{song_sec:02}")

        # Verifică dacă am ajuns la final
        if self.current_time < 0 or self.current_time + self.const_time >= self.song_duration:
            print(f"Am ajuns la finalul {self.current_song}")
            self.stop_time_scale_update()
            if self.repeat or self.shuffle:
                self.song_index, self.current_song = self.music_control.on_song_end()
                self.set_time_scale()
                self.update_center()
            else:
                self.toggle_play_pause = 0
                self.TogglePlayButton.configure(image=self.play_image)
            return  # Oprește bucla de actualizare

        print(f"Current time: {self.current_time + self.const_time}, total time: {self.song_duration}, self.const_time: {self.const_time}")
        self.update_id = self.root.after(1000, self.update_time_scale)

    def stop_time_scale_update(self):
        """Anulează actualizarea automată a TimeScale."""
        if self.update_id is not None:
            self.root.after_cancel(self.update_id)
            self.update_id = None

    def update_time(self, event=None):
        """Actualizează timpul piesei la eliberarea slider-ului."""
        self.const_time = self.TimeScale.get()  # Preia valoarea curentă a slider-ului

        # Dezactivează actualizarea automată temporar
        self.stop_time_scale_update()  # Anulează actualizarea TimeScale

        # Actualizează poziția piesei
        self.music_control.update_song_position(self.const_time)

        # Reîmprospătează label-ul și slider-ul
        current_min = int(self.const_time // 60)
        current_sec = int(self.const_time % 60)
        song_min = int(self.song_duration // 60)
        song_sec = int(self.song_duration % 60)

        self.TimeLabel.configure(text=f"{current_min:02}:{current_sec:02} / {song_min:02}:{song_sec:02}")

        # Repornim actualizarea automată după modificarea manuală
        self.update_time_scale()

    def set_time_scale(self):
        """Setează scala de timp pentru noua piesă."""
        self.song_duration = self.music_control.get_song_duration()
        self.SongLabel.configure(text=self.current_song)
        self.TimeLabel.configure(text=f"00:00 / {int(self.song_duration // 60):02}:{int(self.song_duration % 60):02}")
        self.TimeScale.configure(from_=0, to=self.song_duration)
        self.const_time = 0 # Resetăm const_time pentru noua piesă
        self.current_time = 0
        self.TimeScale.set(0)

        # Pornește actualizarea automată a slider-ului
        self.update_time_scale()

    def buttons(self, menu):
        """Creează un subframe pentru butoane"""
        button_frame = ctk.CTkFrame(menu, fg_color="transparent")
        button_frame.pack(pady=(0, 30))  # Adăugăm spațiu între label și butoane

        # Încarcă imaginea pentru buton

        # BUTONUL DE SHUFFLE
        self.ToggleShuffleButton = ctk.CTkButton(master=button_frame,
                                                image=self.shuffle_image_off,
                                                width=100, height=100,
                                                command=self.toggle_shuffle,
                                                text="", fg_color="transparent",
                                                hover_color="#13060d")
        self.ToggleShuffleButton.grid(row=0, column=0, padx=(5,0))

        # BUTONUL DE PREVIOUS
        self.PreviousButton = ctk.CTkButton(master=button_frame,
                                         image=self.previous_image,
                                         width=120, height=120,
                                         command=self.previous_music,
                                         text="", fg_color="transparent",
                                         hover_color="#13060d")
        self.PreviousButton.grid(row=0, column=1, padx=(5,0))

        # BUTONUL DE STOP
        self.StopButton = ctk.CTkButton(master=button_frame,
                                                   image=self.stop_image,
                                                   width=120, height=120,
                                                   command=self.stop,
                                                   text="", fg_color="transparent",
                                                   hover_color="#13060d")
        self.StopButton.grid(row=0, column=2, padx=(5,0))

        # BUTONUL PLAY/PAUSE
        self.TogglePlayButton = ctk.CTkButton(master=button_frame,
                                         image=self.play_image,
                                         width=120, height=120,
                                         command=self.toggle_play,
                                         text="", fg_color="transparent",
                                         hover_color="#13060d")
        self.TogglePlayButton.grid(row=0, column=3, padx=(5,0))

        # BUTONUL DE NEXT
        self.NextButton = ctk.CTkButton(master=button_frame,
                                            image=self.next_image,
                                            width=120, height=120,
                                            command=self.next_music,
                                            text="", fg_color="transparent",
                                            hover_color="#13060d")
        self.NextButton.grid(row=0, column=4, padx=(0,0))

        # BUTONUL DE REPEAT
        self.ToggleRepeatButton = ctk.CTkButton(master=button_frame,
                                                   image=self.repeat_image_off,
                                                   width=120, height=120,
                                                   command=self.toggle_repeat,
                                                   text="", fg_color="transparent",
                                                   hover_color="#13060d")
        self.ToggleRepeatButton.grid(row=0, column=5, padx=5)

    def toggle_shuffle(self):
        if self.shuffle:
            self.shuffle = self.music_control.shuffle = False
            self.ToggleShuffleButton.configure(image=self.shuffle_image_off)
        else:
            self.shuffle = self.music_control.shuffle = True
            self.ToggleShuffleButton.configure(image=self.shuffle_image_on)
            self.repeat = False
            self.ToggleRepeatButton.configure(image=self.repeat_image_off)

    def toggle_repeat(self):
        if self.repeat == 2:
            self.repeat = 0
            self.ToggleRepeatButton.configure(image=self.repeat_image_off)
        elif self.repeat == 1:
            self.repeat = self.music_control.repeat = 2
            self.ToggleRepeatButton.configure(image=self.repeat_image_2)
        elif self.repeat == 0:
            self.repeat = self.music_control.repeat = 1
            self.ToggleRepeatButton.configure(image=self.repeat_image_on)
            self.shuffle = False
            self.ToggleShuffleButton.configure(image=self.shuffle_image_off)

    def toggle_play(self):
        if self.toggle_play_pause:
            # are rol de pause
            self.toggle_play_pause = False
            print("Paused")
            self.music_control.pause_song()
            # self.stop_time_scale_update()  # Anulează actualizarea TimeScale
            self.TogglePlayButton.configure(image=self.play_image)
        else:
            # are rol de play
            self.toggle_play_pause = True
            self.current_song = self.music_control.play_song(self.song_index, self.current_playlist)
            self.TogglePlayButton.configure(image=self.pause_image)
            self.set_time_scale()

    def next_music(self):
        self.song_index, self.current_song = self.music_control.next_song()
        self.update_center()
        self.set_time_scale()

    def previous_music(self):
        self.song_index, self.current_song = self.music_control.previous_song()
        self.update_center()
        self.set_time_scale()

    def stop(self):
        self.TogglePlayButton.configure(image=self.play_image)
        self.ToggleShuffleButton.configure(image=self.shuffle_image_off)
        self.ToggleRepeatButton.configure(image=self.repeat_image_off)
        self.toggle_play_pause = False
        self.repeat = False
        self.shuffle = False
        self.current_song = os.path.basename(self.playlist_manager.Default[0])
        self.song_index = 0
        self.stop_time_scale_update()  # Anulează actualizarea TimeScale
        self.current_playlist = "Default"
        self.SongLabel.configure(text="Niciun cantec selectat")
        self.TimeScale.set(0)
        self.TimeLabel.configure(text="00:00 / 00:00")
        self.music_control.stop_song()
        self.update_center()

    def run(self):
        self.root.mainloop()