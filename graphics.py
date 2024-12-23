from tkinter import *
from PIL import Image, ImageTk
from pygame import mixer
from music_functions import MusicControl, PlaylistManager


class AppGUI:
    def __init__(self, playlist_manager):
        self.root = Tk()
        self.root.title("MP3 Player")  # Setează titlul ferestrei
        self.root.geometry("600x700")  # Dimensiunea ferestrei mp3-ului
        self.root.configure(background="pink")
        self.playlist_manager = playlist_manager
        self.current_song_index = 0
        self.music_control = MusicControl(self, self.playlist_manager, self.current_song_index)

        self.is_playing = False  # Starea implicită este că muzica nu rulează


        self.shuffle = False
        self.repeat = False

        #imagini play/pause
        self.PlayButton = Image.open("images/play_button.png").resize((80, 80))
        self.PlayButton = ImageTk.PhotoImage(self.PlayButton)
        self.PauseButton = Image.open("images/pause_button.png").resize((80, 80))
        self.PauseButton = ImageTk.PhotoImage(self.PauseButton)

        #imagini shuffle
        self.ShuffleButtonON = Image.open("images/shuffle_button_on.png").resize((80, 80))
        self.ShuffleButtonON = ImageTk.PhotoImage(self.ShuffleButtonON)
        self.ShuffleButtonOFF = Image.open("images/shuffle_button_off.png").resize((80, 80))
        self.ShuffleButtonOFF = ImageTk.PhotoImage(self.ShuffleButtonOFF)

        #imagini repeat
        self.RepeatButtonON = Image.open("images/repeat_button_on.png").resize((80, 80))
        self.RepeatButtonON = ImageTk.PhotoImage(self.RepeatButtonON)
        self.RepeatButtonOFF = Image.open("images/repeat_button_off.png").resize((80, 80))
        self.RepeatButtonOFF = ImageTk.PhotoImage(self.RepeatButtonOFF)

        self.create_widgets()
        self.create_buttons()

    def create_widgets(self):
        # Creăm logo care apare langa titlul ferestrei
        image_icon = PhotoImage(file="images/logo.png")
        self.root.iconphoto(False, image_icon)
        self.create_background()
        self.create_scroll()
        self.create_scale()

    def create_background(self):
        # Cream background-ul
        self.Bg_image = Image.open("images/bg_mp3.png")
        self.Bg_image = self.Bg_image.resize((600, 300))
        self.BgImage = ImageTk.PhotoImage(self.Bg_image)
        Label(self.root, image=self.BgImage).place(x=0, y=0)
        lower_frame = Frame(self.root, background="white", width=600, height=150)
        lower_frame.place(x=0, y=300)

    def create_scroll(self):
        Frame_Music = Frame(self.root, bd=2, relief=RIDGE, background="purple")
        Frame_Music.place(x=0, y=450, width=600, height=300)

        Button(self.root,
               cursor="hand2",
               text="Browse Music",
               height=1,
               font=("Times new roman", 12, "bold"),
               fg="pink",
               bg="white",
               bd=(2, "pink"),
               command=self.music_control.add_music).place(x=250, y=415)

        Scroll = Scrollbar(Frame_Music, orient=VERTICAL)

        self.Playlist = Listbox(Frame_Music,
                                width=100,
                                height=100,
                                font=("Times new roman", 14),
                                bg="white",
                                fg="pink",
                                selectmode=SINGLE,
                                cursor="hand2",
                                bd=0,
                                yscrollcommand=Scroll.set)

        self.Playlist.config(selectbackground="purple", selectforeground="white")
        self.Playlist.bind("<<ListboxSelect>>", self.on_select_song)

        Scroll.config(command=self.Playlist.yview)
        Scroll.pack(side=RIGHT, fill=Y)
        self.Playlist.pack(side=LEFT, fill=BOTH, expand=True)

    def create_scale(self):
        # Adaugă un Scale pentru cursorul de timp fără a arăta valoarea
        self.TimeScale = Scale(self.root, from_=0, to=100, orient=HORIZONTAL, length=350, sliderlength=10, troughcolor="purple", bg="white", width = 20, showvalue=0, borderwidth=0)
        self.TimeScale.bind("<ButtonRelease-1>", self.music_control.on_time_scale_move)
        self.TimeScale.place(x=200, y=250)

        # Adaugă un Label pentru a afișa numele piesei
        self.song_name_label = Label(self.root, text="Nici o melodie selectată", font=("Times New Roman", 14), fg="purple")
        self.song_name_label.place(x=200, y=220)

        # Adaugă un Label pentru a afișa timpul curent (ex: 00:00 / 03:45)
        self.time_label = Label(self.root, text="00:00 / 00:00", font=("Times New Roman", 12), bg="white", fg="purple")
        self.time_label.place(x=465, y=220)


    def create_buttons(self):

        # Creează butonul Play/Pause
        self.PlayPauseButton = Button(self.root,
                                      image=self.PlayButton,
                                      cursor="hand2",
                                      bd=0,
                                      bg="white",
                                      command=self.toggle_play_pause)
        self.PlayPauseButton.place(x=300, y=330)

        # Butonul de stop
        self.Stop_button = Image.open("images/stop_button.png")
        self.Stop_button = self.Stop_button.resize((80, 80))
        self.ButtonStop = ImageTk.PhotoImage(self.Stop_button)
        Button(self.root,
               cursor="hand2",
               image=self.ButtonStop,
               bg="white",
               bd=0,
               command=self.music_control.stop_music).place(x=220, y=330)

        # Butonul de Next
        self.Next_button = Image.open("images/next_button.png")
        self.Next_button = self.Next_button.resize((80, 80))
        self.ButtonNext = ImageTk.PhotoImage(self.Next_button)
        Button(self.root,
               cursor="hand2",
               image=self.ButtonNext,
               bg="white",
               bd=0,
               command=self.music_control.next_music).place(x=380, y=330)

        # Butonul de Previous
        self.Previous_button = Image.open("images/previous_button.png")
        self.Previous_button = self.Previous_button.resize((80, 80))
        self.ButtonPrevious = ImageTk.PhotoImage(self.Previous_button)
        Button(self.root,
               cursor="hand2",
               image=self.ButtonPrevious,
               bg="white",
               bd=0,
               command=self.music_control.previous_music).place(x=140, y=330)

        # Butonul de Shuffle
        self.ShuffleButton = Button(self.root,
                                      image=self.ShuffleButtonOFF,
                                      cursor="hand2",
                                      bd=0,
                                      bg="white",
                                      command=self.toggle_shuffle)
        self.ShuffleButton.place(x=60, y=330)

        # Butonul de Repeat
        self.RepeatButton = Button(self.root,
                                      image=self.RepeatButtonOFF,
                                      cursor="hand2",
                                      bd=0,
                                      bg="white",
                                      command=self.toggle_repeat)
        self.RepeatButton.place(x=460, y=330)

    def update_playlist(self):
        """Actualizează lista de redare în GUI"""
        for song in self.playlist_manager.get_playlist():
            self.Playlist.insert(END, song)  # Adaugă fiecare melodie în listă

    def on_select_song(self, event):
        """Actualizează eticheta cu numele melodiei selectate"""
        selected_song = self.Playlist.get(self.Playlist.curselection())
        self.song_name_label.config(text=selected_song)
        self.current_song_index = self.Playlist.curselection()[0]  # Actualizează indexul melodiei selectate

        # Actualizam obiectul MusicControl cu noul index
        self.music_control.current_song_index = self.current_song_index
        self.PlayPauseButton.config(image = self.PlayPauseButton)
        self.music_control.play_music()

    def toggle_play_pause(self):
        if self.is_playing:
            # funtie de pause
            self.is_playing = False
            self.PlayPauseButton.config(image = self.PlayButton)
            self.music_control.pause_music()
        else:
            # functie de play
            self.is_playing = True
            self.PlayPauseButton.config(image = self.PauseButton)
            self.music_control.play_music()

    def toggle_shuffle(self):
        if self.shuffle:
            self.shuffle = False
            self.ShuffleButton.config(image = self.ShuffleButtonOFF)
            print("Shuffle is OFF\n")
        else:
            self.shuffle = True
            self.repeat = False
            self.ShuffleButton.config(image=self.ShuffleButtonON)
            self.RepeatButton.config(image = self.RepeatButtonOFF)
            print("Shuffle is ON\n")
        self.music_control.shuffle = self.shuffle

    def toggle_repeat(self):
        if self.repeat:
            self.repeat = False
            print("Repeat is OFF\n")
            self.RepeatButton.config(image = self.RepeatButtonOFF)
        else:
            self.repeat = True
            self.shuffle = False
            self.RepeatButton.config(image=self.RepeatButtonON)
            self.ShuffleButton.config(image = self.ShuffleButtonOFF)
            print("Repeat is ON\n")
        #self.music_control.repeat = self.repeat

    def run(self):
        """Pornește aplicația"""
        self.root.mainloop()