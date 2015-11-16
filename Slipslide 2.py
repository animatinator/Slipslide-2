#!/usr/bin/env python

#####  SLIPSLIDE 2  #####
# The main Python file for Slipslide 2, utilising the Penuine game engine.
# Slipslide 2 and the Penuine engine are copyright David Barker 2007


# Import the required Penuine top-level modules
import pygame, sys
from levelcontrol import *
from mainmenu import *
from levelintros import *


# Initialise the window
pygame.init()
screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("Slipslide 2")

# Initialise variables
# The level - music dictionary, which tells the level loader which music track goes with each level
musicdict = {1:1, 2:1, 3:1, 4:1, 5:2, 6:2, 7:3, 8:4, 9:4, 10:4, 11:5, 12:5, 13:5, 14:6, 15:6, 16:7,
        17:7, 18:8, 19:8, 20:8, 21:8, 22:9, 23:10, 24:10, 25:10}
# Playing - a boolean variable used for controlling the game's mainloop
playing = True


def ShowMenu():
    """
Show the main menu.
    """
    menu = Menu()
    selection = menu.ShowMenu()
    return selection


while playing == True:
    # Show the menu
    selection = ShowMenu()
    
    # Process the menu selection
    # If the user selects 'New game'
    if selection == "new":
        pass
    # If the user selects 'Continue game'
    elif selection == "continue":
        pass
    # If the user selects 'Load custom levels'
    elif selection == "load":
        pass
    # If the user selects 'Quit', the main menu will quit by itself, so no processing is required
