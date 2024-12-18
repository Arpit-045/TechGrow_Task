import tkinter as tk
from tkinter import filedialog, messagebox
from pygame import mixer
import time
import threading
import os


class MP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("600x600")
        self.root.configure(bg="#2c3e50")

        # Initialize mixer
        mixer.init()

        # Playlist and current song details
        self.playlist = []
        self.current_song_index = None
        self.song_length = 0

        # Playlist Box
        self.listbox = tk.Listbox(
            self.root, bg="#34495e", fg="white", font=("Helvetica", 12)
        )
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=10)

        # Song Info
        self.info_frame = tk.Frame(self.root, bg="#2c3e50")
        self.info_frame.pack()

        self.track_title = tk.Label(
            self.info_frame, text="Track: None", font=("Helvetica", 14), bg="#2c3e50", fg="white"
        )
        self.track_title.grid(row=0, column=0, pady=5)

        self.track_duration = tk.Label(
            self.info_frame, text="Duration: 00:00", font=("Helvetica", 14), bg="#2c3e50", fg="white"
        )
        self.track_duration.grid(row=0, column=1, pady=5)

        # Seek Bar
        self.seek_bar = tk.Scale(
            self.root, from_=0, to=100, orient="horizontal", command=self.seek_song, bg="#34495e", fg="white"
        )
        self.seek_bar.pack(fill=tk.X, padx=10, pady=10)

        # Control Buttons
        self.controls_frame = tk.Frame(self.root, bg="#2c3e50")
        self.controls_frame.pack()

        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_song, width=10, bg="#1abc9c", fg="white")
        self.play_button.grid(row=0, column=0, padx=5)

        self.pause_button = tk.Button(self.controls_frame, text="Pause", command=self.pause_song, width=10, bg="#e67e22", fg="white")
        self.pause_button.grid(row=0, column=1, padx=5)

        self.resume_button = tk.Button(self.controls_frame, text="Resume", command=self.resume_song, width=10, bg="#3498db", fg="white")
        self.resume_button.grid(row=0, column=2, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop_song, width=10, bg="#e74c3c", fg="white")
        self.stop_button.grid(row=0, column=3, padx=5)

        # Volume Slider
        self.volume_slider = tk.Scale(
            self.root, from_=0, to=100, orient="horizontal", command=self.set_volume, bg="#34495e", fg="white"
        )
        self.volume_slider.set(50)
        mixer.music.set_volume(0.5)
        self.volume_slider.pack(fill=tk.X, padx=10, pady=10)

        # Add Song Button
        self.add_button = tk.Button(self.root, text="Add Songs", command=self.add_songs, bg="#9b59b6", fg="white")
        self.add_button.pack(fill=tk.X, padx=10, pady=5)

        # Background Thread to Update Seek Bar
        self.update_thread = threading.Thread(target=self.update_seek_bar, daemon=True)
        self.update_thread.start()

    def add_songs(self):
        """Add songs to the playlist."""
        files = filedialog.askopenfilenames(filetypes=[("MP3 Files", "*.mp3")])
        for file in files:
            self.playlist.append(file)
            self.listbox.insert(tk.END, os.path.basename(file))

    def play_song(self):
        """Play the selected song."""
        try:
            selected_song = self.listbox.curselection()
            if selected_song:
                self.current_song_index = selected_song[0]
                song = self.playlist[self.current_song_index]
                mixer.music.load(song)
                mixer.music.play()
                self.update_song_info(song)
            else:
                messagebox.showerror("Error", "No song selected!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_song(self):
        """Pause the current song."""
        mixer.music.pause()

    def resume_song(self):
        """Resume the paused song."""
        mixer.music.unpause()

    def stop_song(self):
        """Stop the current song."""
        mixer.music.stop()
        self.seek_bar.set(0)

    def set_volume(self, value):
        """Set the volume."""
        volume = int(value) / 100
        mixer.music.set_volume(volume)

    def seek_song(self, value):
        """Seek to a specific part of the song."""
        if mixer.music.get_busy():
            mixer.music.rewind()
            mixer.music.set_pos(float(value))

    def update_song_info(self, song):
        """Update the current track title and duration."""
        self.track_title.config(text=f"Track: {os.path.basename(song)}")
        self.song_length = mixer.Sound(song).get_length()
        self.track_duration.config(text=f"Duration: {time.strftime('%M:%S', time.gmtime(self.song_length))}")
        self.seek_bar.config(to=int(self.song_length))

    def update_seek_bar(self):
        """Continuously update the seek bar during playback."""
        while True:
            if mixer.music.get_busy():
                current_time = mixer.music.get_pos() / 1000
                self.seek_bar.set(current_time)
            time.sleep(1)


# Create the GUI window
root = tk.Tk()
mp3_player = MP3Player(root)
root.mainloop()
