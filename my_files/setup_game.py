import os
from turtle import Screen, Turtle
import time
# import math
# import random

# constants - can I write these as constants
s = Screen()
t = Turtle()
file_dir = os.path.dirname(os.path.realpath('__file__')) # absolute path of this file

def setup_window():
    # t.ht() # hide turtle object
    s.title("CS5001 Sliding Puzzle Game") # change titlebar text
    s.setup(800, 800)

def splash_screen():
    # access files in adjacent folder using relative path --> change into modular function later
    # file_dir = os.path.dirname(os.path.realpath('__file__')) # absolute path of this file
    file = os.path.join(file_dir, '..\Resources\splash_screen.gif') # relative path of image

    # display & erase splash screen
    start = time.time()
    while (time.time() - start) < 3.5:
        s.bgpic(file)
        s.update()
    s.bgpic("nopic")
    s.update()

def get_user_info():
    # input player name & number of moves
    player_name = s.textinput("CS5001 Puzzle Slide", "Your Name: ")
    num_moves = s.numinput("5001 Puzzle Slide - Moves", "Enter the number of moves (chances) you want (5-200)?", 50, 5, 200)

def setup_game():
    t.ht() # hide turtle object
    setup_window()
    splash_screen()
    get_user_info()
