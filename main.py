import tkinter
from tkinter.ttk import Progressbar
import pygame
from PIL import Image, ImageTk
from threading import Thread
import time
import math

root = tkinter.Tk()
root.title('Music Player')
root.geometry('400x480')
root.configure(bg='black')  # Set background color to black
pygame.mixer.init()
list_of_songs = ['music/City.wav', 'music/chillin.wav', 'C:/Users/Lenovo/OneDrive/Desktop/py project/music/fav (1).wav', 'music/missin.wav', 'music/retro-city.wav']
list_of_covers = ['img/city.jpg', 'img/chillin.jpg', 'img/fav(1).jpg','img/missin.jpg', 'img/retro-city.jpg']

n = 0

paused = False  # Track if music is paused
start_time = 0  # Track start time of current song

def get_album_cover(song_name, n):
    image1 = Image.open(list_of_covers[n])
    image2 = image1.resize((250, 250))
    load = ImageTk.PhotoImage(image2)
    
    label1 = tkinter.Label(root, image=load, bg='black')
    label1.image = load
    label1.place(relx=.19, rely=.06)

    stripped_string = song_name[6:-4]
    song_name_label = tkinter.Label(root, text=stripped_string, bg='black', fg='white')
    song_name_label.place(relx=.4, rely=.6)

def update_progress():
    global start_time
    while pygame.mixer.music.get_busy():
        if not paused:
            current_time = pygame.mixer.music.get_pos() / 1000  # Current time in seconds
            progressbar['value'] = current_time
            time_label.config(text=format_time(current_time))
        else:
            start_time = time.time() - start_time  # Adjust start time to elapsed time
        root.update()
        time.sleep(0.1)

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f'{minutes:02}:{seconds:02}'

def threading():
    t1 = Thread(target=update_progress)
    t1.start()

def play_music():
    global n, start_time, paused
    current_song = n
    if n >= len(list_of_songs):
        n = 0
    song_name = list_of_songs[n]
    try:
        pygame.mixer.music.load(song_name)
        pygame.mixer.music.play(loops=0)
        pygame.mixer.music.set_volume(0.5)
        start_time = time.time()  # Record start time
        get_album_cover(song_name, n)
        threading()
        paused = False
        n += 1
    except pygame.error as e:
        print("Error loading music file:", e)
        # Handle the error gracefully

def pause_music():
    global paused, start_time
    if not paused:
        paused = True
        start_time = time.time() - start_time  # Record elapsed time
        pygame.mixer.music.pause()
    else:
        paused = False
        pygame.mixer.music.unpause()
        start_time = time.time() - start_time  # Adjust start time to elapsed time
        threading()

def skip_forward():
    play_music()

def skip_back():
    global n
    n -= 2
    play_music()

def volume(value):
    pygame.mixer.music.set_volume(float(value))

play_button = tkinter.Button(master=root, text='Play', command=play_music, bg='black', fg='white')
play_button.place(relx=0.35, rely=0.7, anchor=tkinter.CENTER)

pause_button = tkinter.Button(master=root, text='Pause', command=pause_music, bg='black', fg='white')
pause_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

skip_f = tkinter.Button(master=root, text='>', command=skip_forward, width=2, bg='black', fg='white')
skip_f.place(relx=0.65, rely=0.7, anchor=tkinter.CENTER)

skip_b = tkinter.Button(master=root, text='<', command=skip_back, width=2, bg='black', fg='white')
skip_b.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

slider = tkinter.Scale(master=root, from_=0, to=1, command=volume, orient=tkinter.HORIZONTAL, length=210, bg='black', fg='white')
slider.place(relx=0.5, rely=0.78, anchor=tkinter.CENTER)

time_label = tkinter.Label(root, text='00:00', bg='black', fg='white')
time_label.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

progressbar = Progressbar(master=root, orient=tkinter.HORIZONTAL, length=250, mode='determinate', style='black.Horizontal.TProgressbar')
progressbar.place(relx=.5, rely=.92, anchor=tkinter.CENTER)

root.mainloop()
