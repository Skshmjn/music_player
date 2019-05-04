import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
from pygame import mixer

playlist = []


class Music:
    def __init__(self):
        mixer.init()

    def browse_file(self):
        global filename_path
        filename_path = filedialog.askopenfilename()
        self.add_to_playlist(filename_path)

        mixer.music.queue(filename_path)

    def add_to_playlist(self, filename):
        filename = os.path.basename(filename)
        index = 0
        playlistbox.insert(index, filename)
        playlist.insert(index, filename_path)
        index += 1

    def del_song(self):
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])
        playlistbox.delete(selected_song)
        playlist.pop(selected_song)

    def show_details(self, play_song):
        file_data = os.path.splitext(play_song)

        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
        else:
            a = mixer.Sound(play_song)
            total_length = a.get_length()

        # div - total_length/60, mod - total_length % 60
        mins, secs = divmod(total_length, 60)
        mins = round(mins)
        secs = round(secs)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        lengthlabel['text'] = "Total Length" + ' - ' + timeformat

        t1 = threading.Thread(target=self.start_count, args=(total_length,))
        t1.start()

    def start_count(self, t):
        global paused
        # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
        # Continue - Ignores all of the statements below it. We check if music is paused or not.
        current_time = 0
        while current_time <= t and mixer.music.get_busy():
            if paused:
                continue
            else:
                mins, secs = divmod(current_time, 60)
                mins = round(mins)
                secs = round(secs)
                timeformat = '{:02d}:{:02d}'.format(mins, secs)
                currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
                time.sleep(1)
                current_time += 1

    def play_music(self):
        global paused

        if paused:
            mixer.music.unpause()

            paused = FALSE
        else:
            try:
                self.stop_music()
                time.sleep(1)
                selected_song = playlistbox.curselection()
                selected_song = int(selected_song[0])
                play_it = playlist[selected_song]
                mixer.music.load(play_it)
                mixer.music.play()
                self.show_details(play_it)
            except:
                tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')

    def pause_music(self):
        global paused
        paused = TRUE
        mixer.music.pause()

    def set_vol(self, val):
        volume = float(val) / 100
        mixer.music.set_volume(volume)

    def stop_music(self):
        mixer.music.stop()

    def on_closing(self):
        self.stop_music()
        root.destroy()


root = Tk()

root.title("Music Player")
root.iconbitmap('musical.ico')

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (playlist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame
object = Music()
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = Button(leftframe, text="+ Add", command=object.browse_file)
addBtn.pack(side=LEFT)

delBtn = Button(leftframe, text="- Del", command=object.del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = Label(topframe, text='Total Length : --:--')
lengthlabel.pack(pady=5)

currenttimelabel = Label(topframe, text='Current Time : --:--', relief=GROOVE)
currenttimelabel.pack()

paused = FALSE

# set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

playPhoto = PhotoImage(file="play-button.png")
playBtn = Button(middleframe, image=playPhoto, command=object.play_music)
playBtn.grid(row=0, column=0, padx=10)

stopPhoto = PhotoImage(file="stop.png")
stopBtn = Button(middleframe, image=stopPhoto, command=object.stop_music)
stopBtn.grid(row=0, column=1, padx=10)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = Button(middleframe, image=pausePhoto, command=object.pause_music)
pauseBtn.grid(row=0, column=2, padx=10)

# Bottom Frame for volume, rewind, mute etc.

bottomframe = Frame(rightframe)
bottomframe.pack()

scale = Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=object.set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)

root.protocol("WM_DELETE_WINDOW", object.on_closing)


root.mainloop()
