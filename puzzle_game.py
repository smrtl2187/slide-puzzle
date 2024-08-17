'''
	CS5001
	Fall 2022
	Final Project: Slide Puzzle

	Stephanie Mortel

        This program implements the gameplay for a slide-puzzle.
        It can load different puzzles and keeps track of wins on a leaderboard display.
        Please read design.txt file if running into any issues.
'''

import os
from turtle import Screen, Turtle
import time
import math
import random

s = Screen() # screen turtle
t = Turtle() # drawing turtle
status = Turtle() # turtle to be used for status line of player moves
thumbnail = Turtle() # turtle to be used for thumbnail display
leaderboard = Turtle() # turtle for leaderboard
file_dir = os.path.dirname(os.path.realpath('__file__')) # absolute path of this file

def setup_window():
    ''' sets up titlebar and screensize '''
    
    t.ht() # hide turtle object
    s.title("CS5001 Sliding Puzzle Game") # change titlebar text
    s.setup(900, 850)

def splash_screen():
    ''' displays splashscreen for 3.5 seconds then erases it '''
    
    splash = 'Resources/splash_screen.gif'
    
    # while loop for timer
    start = time.time()
    while (time.time() - start) < 3.5:
        s.bgpic(splash)
        s.update()
    s.bgpic("nopic")
    s.update()

def move(x, y):
    ''' moves the turtle to a location but does not draw anything '''
    
    t.up()
    t.goto(x, y)
        
def draw_rectangle(color: str, pensize: int, width: int, length: int):
    ''' draws a rectangle '''
    t.down()
    t.speed(0)
    t.pensize(pensize)
    t.pencolor(color)
    for side in range(4):
        if side % 2 == 0: # draws sides 1 & 3
            t.forward(width)
            t.right(90)
        else: # draws sides 2 & 4
            t.forward(length)
            t.right(90)
    t.up()
    t.ht()

def draw_borders():
    '''
    draws rectangular borders for all areas of game board
    '''
    
    # creates play area
    move(-400, 350) # top left corner
    draw_rectangle("black", 5, 500, 550)

    # creates status area
    move(-400, -250) # top left corner
    draw_rectangle("black", 5, 800, 150)

    # creates leaderboard
    move(140, 350) # top left corner
    draw_rectangle("blue", 5, 260, 550)

def create_puzzle_list():
    ''' creates list of all puzzle files from directory '''

    puzzle_list = [f.name for f in os.scandir(file_dir) if f.name.endswith('.puz')]

    if len(puzzle_list) > 10: # for 10 puzzle limit
        s.addshape("Resources/file_warning.gif")
        limit_msg = Turtle()
        s.delay(1500)
        limit_msg.shape("Resources/file_warning.gif")
        limit_msg.ht()
        s.delay(0)
        
    return puzzle_list
    

def create_puzzle_dict(puzzle_filename: str):
    ''' given a puzzle filename, will return a dictionary
        with associated puzzle info'''
    
    with open(puzzle_filename, "r") as myfile:
        puzzle_info = [] # nested list of puzzle info
        for lines in myfile:
            lines = lines.strip()
            puzzle_info.append(lines)
        for i in range(len(puzzle_info)):
            puzzle_info[i] = puzzle_info[i].split(': ')

    puzzle_dict = {}
    for i in range(len(puzzle_info)):
        puzzle_dict[puzzle_info[i][0]] = puzzle_info[i][1]
    return puzzle_dict

def get_tile_img_list(puzzle_dict):
    ''' creates list of tile images in correct oder for use in puzzle solution'''
    
    num_tiles = int(puzzle_dict['number']) # total number of tiles for puzzle
    unscrambled_tiles = []
    for i in range(int(num_tiles)):
        unscrambled_tiles.append(puzzle_dict[str(i+1)])
    return unscrambled_tiles
    
def scramble_tiles(unscrambled_tiles):
    ''' randomly scrambles a list of tiles' images given a dictionary
        of puzzle file metadata and the total number of tiles
        for the selected puzzle file'''
    
    # create scrambled list of tile images
    copy = unscrambled_tiles.copy()
    random.shuffle(copy)
    return copy

def register_images(scrambled_tiles):
        '''register images as available shapes on screen'''
        
        for img in scrambled_tiles:
            s.addshape(img)
            
class Tile:
    def __init__(self, img, i, j, tile_length, turt=Turtle(), isClicked=False):
        self.img = img
        self.turt = Turtle()
        self.turt.shape(img)
        self.turt.speed("fast")

        # position on board matrix
        self.row = j
        self.column = i

        # center coordinates of [0][0] tile + [i][j] adjustments
        self.x = -400 + 50 + (tile_length / 2) + (tile_length * i)
        self.y = 350 - 100 - (tile_length * j)
        self.turt.up()
        self.turt.setpos(self.x, self.y)
    
    def __str__(self):
        return f"{self.row, self.column}"  

    def hide_turtle(self):
        '''hide tiles'''
        
        self.turt.speed("fast")
        self.turt.ht()

    def swap_img(self, other):
        '''swap images between two tiles'''
        
        temp = self.img
        self.img = other.img
        other.img = temp

        '''display swapped images on board'''
        
        self.turt.shape(self.img)
        other.turt.shape(other.img)

def create_board(tile_img_list, tile_length):
    ''' creates custom board given a list of tile images and length of each tile'''
    
    # create matrix of tile class objects
    x = int(math.sqrt(len(tile_img_list)))
    tile_list = []
    for column in range(x):
        tile_list.append([])
    i = 0
    for column in range(x):
        for row in range(x):
            tile_list[column].append(Tile(tile_img_list[i], row, column, tile_length))
            i += 1
            
    return tile_list

def hide_turtles(tile_list):
    ''' hide each tile object'''
    
    for row in range(len(tile_list)):
        for column in range(len(tile_list)):
            Tile.hide_turtle(tile_list[row][column])
            
def find_blank():
    '''finds and returns blank tile object from 2D array of tile objects'''
    
    for i in range(len(scrambled_puzzle)):
        for tile in scrambled_puzzle[i]:
            if "blank" in tile.img:
                return tile
def is_adjacent(tile):
    '''check if blank tile and clicked tile are adjacent, returns True if they are, False if not'''
    
    blank_tile = find_blank()
    
    if abs(blank_tile.row - tile.row) == 1 and abs(blank_tile.column - tile.column) == 0:
        return True
    if abs(blank_tile.column - tile.column) == 1 and abs(blank_tile.row - tile.row) == 0:
        return True
    return False

def swap_tile(tile):
    '''processes clicked tile to see if it will be swapped'''
    
    blank_tile = find_blank()

    if is_adjacent(tile):
        ''' swaps clicked tile if adjacent to blank tile'''
        
        tile.swap_img(blank_tile)
        
        global move_count
        move_count += 1 # update move count

        update_status(status) # update move count display
                    
def update_status(status):
    '''updates status line displaying number of moves made'''
    
    status.ht()
    status.up()
    status.speed('fastest')
    status.goto(-400 + 100, -250 - 80)

    status.clear()
    status.write(f"Player Moves: {move_count}", font=('Arial', 24, 'normal'))
    s.update()
            
def process_clicked_tile():
    '''registers click, finds tile object clicked, then passes to swap_tile function'''
    
    for i in range(len(scrambled_puzzle)):
        for tile in scrambled_puzzle[i]:
            def check_click(x, y, tile=tile):
                return swap_tile(tile) # determine if clicked tile will be swapped w/blank
            tile.turt.onclick(check_click) # register click
            
def reset_tiles(unscrambled_tiles):
        ''' will solve the puzzle'''

        global solved_puzzle
        
        hide_turtles(scrambled_puzzle) # hide scrambled tiles
        solved_puzzle = create_board(unscrambled_tiles, tile_length) # show solution

def check_win():
    ''' checks if scrambled tile images match unscrambled image order
    return True if all match'''
    
    scrambled_puzzle
    unscrambled_tiles
    
    k = 0
    for i in range(len(scrambled_puzzle)):
        for tile in scrambled_puzzle[i]:
            if tile.img != unscrambled_tiles[k]:
                return False
            k += 1 # checks each image in ordered list
    return True

def display_win():
    '''displays win pop-up message'''
    
    win_img = 'Resources/winner.gif'
    s.addshape(win_img)
    win_msg = Turtle()
    s.delay(1500)
    win_msg.shape(win_img)
    win_msg.ht()
    s.delay(0)
    
def display_lose():
    ''' displays lose pop-up message'''
    
    lose_img = 'Resources/Lose.gif'
    lose_msg = Turtle()
    s.addshape(lose_img)
    s.delay(1500)
    lose_msg.shape(lose_img)
    lose_msg.ht()
    s.delay(0)

def quit_program():
    ''' quits program by displaying quit message and closing window screen'''
    
    s.addshape('Resources/quitmsg.gif')
    t.speed('fast')
    t.setpos(0, 0)
    s.delay(750)
    t.shape('Resources/quitmsg.gif')
    t.st()
    s.delay(0)
    s.bye()

def setup_reset():
    ''' sets up reset button display on screen & it's functionality'''
    
    # reset button
    reset_button = Turtle()
    reset_button.ht()
    s.addshape('Resources/resetbutton.gif')
    reset_button.up()
    reset_button.setpos(-400 + 100 + 430, -250 - 80)
    reset_button.shape('Resources/resetbutton.gif')
    reset_button.st()

    # reset if clicked
    def reset_clicked(x, y, reset_button=reset_button):
        reset_tiles(unscrambled_tiles) # shows solution
    reset_button.onclick(reset_clicked)

def setup_quit():
    ''' sets up quit button display on screen & it's functionality'''
    
    # quit button
    quit_button = Turtle()
    quit_button.ht()
    quit_button.speed('fast')
    s.addshape('Resources/quitbutton.gif')
    quit_button.up()
    quit_button.setpos(-400 + 100 + 630, -250 - 80)
    quit_button.shape('Resources/quitbutton.gif')
    quit_button.st()
    
    # quit if clicked
    def quit_clicked(x, y, quit_button=quit_button):
        quit_program() # closes screen
    quit_button.onclick(quit_clicked)

def display_thumbnail(thumbnail_img):
    ''' set up thumbnail display on leaderboard'''
    
    s.addshape(thumbnail_img)
    thumbnail.ht()
    thumbnail.speed('fast')
    thumbnail.up()
    thumbnail.setpos(140 + 240, 320)
    thumbnail.shape(thumbnail_img)
    thumbnail.st()

def read_leaderboard():
    '''read leaderboard.txt file and return list of lines in file'''
        
    leaderboard_content = []

    try:
        with open("leaderboard.txt", mode="r") as in_file:
            for each in in_file:
                each = each.strip("\n")
                leaderboard_content.append(each)
    except IOError:

        # display leaderboard error message
        leaderboard_msg = Turtle()
        s.addshape("Resources/leaderboard_error.gif")
        s.delay(1500)
        leaderboard_msg.shape("Resources/leaderboard_error.gif")
        leaderboard_msg.ht()
        s.delay(0)

        # log error in file
        with open("5001_puzzle.err", mode="a") as file:
            file.write(f"{time.ctime()}:Error:" \
                       + f"could not open leaderboard.txt"\
                       + f" LOCATION: read_leaderboard()" + "\n")
    else:
        return leaderboard_content
    

def update_leaderboard():
    # update leaderboard display
    leaderboard.clear()
    leaderboard_content = read_leaderboard()
    leaderboard_content = "\n".join(leaderboard_content) # creates string to display
    leaderboard.write(leaderboard_content, font=('Arial', 24, 'normal'))
    s.update()

def play(player_name: str, moves_max: int, puzzle_filename: str):
    '''this function will process either the default puzzle file
    or a new puzzle selected by the user, extract the information for use
    in creating and deploying game components on the board, and also initiates
    the puzzle gameplay for one puzzle'''
    
    global scrambled_puzzle
    global tile_length
    global move_count
    global unscrambled_tiles

    '''puzzle information extraction'''

    puzzle_dict = create_puzzle_dict(puzzle_filename)

    # call dictionary value by key
    img_subfolder = puzzle_dict['name'] # filename for subfolder in Images
    num_tiles = int(puzzle_dict['number']) # total number of tiles for puzzle
    tile_length = int(puzzle_dict['size']) # sidelength of image/square tile
    thumbnail_img = puzzle_dict['thumbnail'] # thumbnail filename

    # check if num_tiles is perfect square
    if round(math.sqrt(num_tiles)) != math.sqrt(num_tiles):

        # display error message
        puz_msg = Turtle()
        s.addshape("Resources/file_error.gif")
        s.delay(1500)
        puz_msg.shape("Resources/file_error.gif")
        puz_msg.ht()
        s.delay(0)

        # log error
        with open("5001_puzzle.err", mode="a") as file:
            file.write(f"{time.ctime()}:Error:" \
                       + f"could not load puzzle"\
                       + f" LOCATION: play()" + "\n")
        return # cannot load puzzle
        
    '''tile & image setup'''
    
    # get lists of unscrambled & scrambled tile images
    unscrambled_tiles = get_tile_img_list(puzzle_dict)
    scrambled_tiles = scramble_tiles(unscrambled_tiles)

    # register tile images on screen
    register_images(scrambled_tiles)

    # create board w/scrambled tiles --- 2d array of turtle objects
    scrambled_puzzle = create_board(scrambled_tiles, tile_length)

    # display thumbnail
    display_thumbnail(thumbnail_img)

    '''board gameplay'''
    
    # initialize move_count; will be updated when swap occurs
    move_count = 0
    update_status(status) # update move count display
    while move_count < moves_max:
        process_clicked_tile() # register clicked tiles & process swapping
        # update_status(status) # update move count display
        if check_win() == True:
            display_win()
            with open("leaderboard.txt", mode="a") as out_file:
                update = str(move_count) + ': ' + player_name
                out_file.write(update + "\n")  # update leaderboard
                update_leaderboard() 
            break
        elif move_count >= moves_max:
            display_lose()
            break

def main():

    puzzle_list = create_puzzle_list() # list of .puz files in directory
    puzzle_filename = 'luigi.puz' # default puzzle file

    # puzzle menu to display to user when load button clicked
    puzzle_menu = []
    for i in range(len(puzzle_list)):
        puzzle_menu.append(puzzle_list[i])
    puzzle_menu = "\n".join(puzzle_menu)
    
    '''window setup'''
    
    setup_window()
    splash_screen()
    draw_borders()

    '''input player name & number of moves allowed'''
    
    player_name = s.textinput("CS5001 Puzzle Slide", "Your Name: ")
    moves_max = s.numinput("5001 Puzzle Slide - Moves", \
                           "Enter the number of moves (chances) you want (5-200)?", 50, 5, 200)
    moves_max = int(moves_max)

    '''leaderboard setup'''
    
    # setup leaderboard turtle
    
    leaderboard.ht()
    leaderboard.up()
    leaderboard.speed('fastest')
    leaderboard.goto(140, 350)
    
    # create txt file & add leaderboard header
    with open("leaderboard.txt", mode="w") as out_file:
        out_file.write("Leaders: " + "\n")

    # read leaderboard file
    leaderboard_content = read_leaderboard() # list

    # display leaderboard contents
    leaderboard_content = "\n".join(leaderboard_content) # creates string to display
    leaderboard.write(leaderboard_content, font=('Arial', 24, 'normal'))

    '''setup functional buttons'''
    
    setup_reset() # reset button & functionality if clicked
    setup_quit() # quit button & functionality if clicked

    '''setup_load():'''
    
    # load button
    load_button = Turtle()
    load_button.ht()
    s.addshape('Resources/loadbutton.gif')
    load_button.up()
    load_button.setpos(-400 + 100 + 530, -250 - 80)
    load_button.shape('Resources/loadbutton.gif')
    load_button.st()

    # load new puzzle if clicked
    def load_clicked(x, y, load_button=load_button):

        global puzzle_filename
        puzzle_filename = s.textinput("Load Puzzle", f"Choices are:\n{puzzle_menu}")
        puzzle_filename = puzzle_filename.lower()
        
        if puzzle_filename not in puzzle_menu:

            # display error message
            puz_msg = Turtle()
            s.addshape("Resources/file_error.gif")
            s.delay(1500)
            puz_msg.shape("Resources/file_error.gif")
            puz_msg.ht()
            s.delay(0)

            # log error
            with open("5001_puzzle.err", mode="a") as file:
                file.write(f"{time.ctime()}:Error:" \
                           + f"could not load puzzle"\
                           + f" LOCATION: main(), load_clicked()" + "\n")
                puzzle_filename = s.textinput("Load Puzzle", f"Choices are:\n{puzzle_menu}")
        
        hide_turtles(scrambled_puzzle) # hide scrambled tiles
        hide_turtles(solved_puzzle) # hide unscrambled tiles

        # sets the game in play again
        play(player_name, moves_max, puzzle_filename)
        
    load_button.onclick(load_clicked)

    '''gameplay'''
    
    play(player_name, moves_max, puzzle_filename)


if __name__ == "__main__":
    main()
