#!/usr/bin/env python

## Level Control - part of the Penuine game engine
# Controls the loading, drawing and updating of game levels
# Copyright ExeSoft 2007
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Version 1.0 finished - *


import pygame
from blocks import *
from character import *
from pausemenu import *
from sound import *
from fading import *


class LevelController():
    """
The Slipslide 2 level loader, copyright David Barker 2007
This takes only one argument, the name of the folder the level's data is stored in. This can be
either relative or absolute as necessary.
    """

    def __init__(self, levelname, musicpath):
        """
    The initialisation method, which takes the level's name (folder name) and the level's music
    location as arguments.
        """
        # Get the screen surface
        self.screen = pygame.display.get_surface()
        # Get the current levelname and the music location
        self.levelname = levelname
        self.musicpath = musicpath
        # Create a binary variable that tells whether or not the game is paused
        self.paused = 0
        # Create a boolean variable for whether the level is finished or not
        self.complete = False
        # Initialise the finish position
        self.finx, self.finy = 0, 0
        # Create a sprite group for the blocks (used for collision detection)
        self.blocks = pygame.sprite.Group()
        # Create a sprite group for the holes (also used for collision detection)
        self.holes = pygame.sprite.Group()
        # Load the level's required objects
        self.LoadLevelObjects()
        # Start playing the level's music
        self.PlayMusic()
        # Build the level
        self.LoadLevel()
        self.DrawLevel()
        # Redraw without updating the display
        self.RedrawPause()
        # Fade in
        self.fader = Fader(self)
        self.fader.FadeIn(60)

    def Redraw(self):
        """
    Redraws the screen and all the sprites.
        """
        # Blit in the background image
        self.screen.blit(self.bg, self.bgrect)
        # Redraw the blocks
        self.blocks.draw(self.screen)
        # Redraw the holes
        self.holes.draw(self.screen)
        # Call the character's update method
        self.character.Update()

    def RedrawPause(self):
        """
    A modified redraw method for use by the pause menu, which doesn't update the character's position.
        """
        # Blit in the background image
        self.screen.blit(self.bg, self.bgrect)
        # Redraw the blocks
        self.blocks.draw(self.screen)
        # Redraw the holes
        self.holes.draw(self.screen)
        # Redraw the character without updating its position
        self.character.RedrawWithoutUpdate()

    def LoadLevelObjects(self):
        """
    Loads all the images and data for the current level.
        """
        # Load the images
        block = "%s\\block.png" % self.levelname
        hole = "%s\\hole.png" % self.levelname
        background = "%s\\background.png" % self.levelname
        self.blockimage = pygame.image.load(block)
        self.holeimage = pygame.image.load(hole)
        self.bg = pygame.image.load(background)
        self.bgrect = self.bg.get_rect()
        # Load the layout
        self.layoutfilepath = "%s\\layout.slf" % self.levelname

    def LoadLevel(self):
        """
    Loads the level from the level data file.
        """
        layoutfile = open(self.layoutfilepath)
        lines = layoutfile.readlines()
        # Create the level data list
        self.leveldata = []
        # For each line in the level data file, create a list and add all items in that line to it
        # so they can be looped through.
        for rawline in lines:
            line = []
            for character in rawline:
                if character == "\n":
                    pass
                else:
                    line.append(character)
            # Append the line list to the level data list
            self.leveldata.append(line)

    def DrawLevel(self):
        """
    Creates the level on-screen using the loaded level data and the sprites.
        """
        # Create variables for the current row and column in the file
        self.horcount = 0
        self.vercount = 0
        # For each line in the file
        for line in self.leveldata:
            # For each item (column) in the line
            for item in line:
                # If it's a "C", insert a character there (supplying the row and column numbers as grid
                # co-ordinates)
                if item == "C":
                    self.CreateCharacter(self.horcount, self.vercount)
                # If it's a "B", insert a block there (supplying the row and column numbers as grid
                # co-ordinates)
                elif item == "B":
                    self.AddBlock(self.horcount, self.vercount)
                # If it's a "W", insert a (transparent) wall section there (as above)
                elif item == "W":
                    self.AddWall(self.horcount, self.vercount)
                # If it's an "H", insert a hole there
                elif item == "H":
                    self.AddHole(self.horcount, self.vercount)
                    try:
                        self.character.UpdateHoles(self.holes)
                    except:
                        pass
                # If it's an "F", change the level's finish point to the grid location of the "F"
                elif item == "F":
                    self.finx = self.horcount
                    self.finy = self.vercount
                    try:
                        self.character.SetFinishPoint(self.finx, self.finy)
                    except:
                        pass
                # If it's a "0", do nothing
                elif item == "0":
                    pass
                # Increment the column count
                self.horcount = self.horcount+1
            # Increment the line count
            self.vercount = self.vercount+1
            # Return the column count to 0 to begin the next line
            self.horcount = 0
        # Blit in the background image and update everything
        self.screen.blit(self.bg, self.bgrect)

    def AddBlock(self, posx, posy):
        """
    Adds a block sprite at the supplied position.
        """
        # Change the supplied grid co-ordinates into pixel co-ordinates
        posx = posx*24
        posy = posy*24
        # Create an instance of the Block sprite (defined in the blocks module)
        block = Block((posx, posy), self.blockimage)
        # Add it to the blocks sprite group
        self.blocks.add(block)
        
    def AddWall(self, posx, posy):
        """
    Adds a (transparent) wall section at the supplied position.
        """
        # Change the supplied grid co-ordinates into pixel co-ordinates
        posx = posx*24
        posy = posy*24
        # Create an instance of the Wall sprite (defined in the blocks module)
        block = Wall((posx, posy))
        # Add it to the blocks sprite group (so that it's detected by their collision detection)
        self.blocks.add(block)

    def AddHole(self, posx, posy):
        """
    Adds a hole sprite at the supplied position.
        """
        hole = Hole((posx, posy), self.holeimage)
        self.holes.add(hole)

    def CreateCharacter(self, posx, posy):
        """
    Adds the character sprite.
        """
        self.character = Character(self, (posx, posy), self.finx, self.finy, self.blocks, self.holes)

    def ProcessEvent(self, event):
        """
    Processes events sent by the main file.
        """
        #' If the event is a keypress
        if event.type == pygame.KEYDOWN:
            # If it's the "P" key, pause the game
            if event.key == pygame.K_p:
                # If it's already paused, don't bother
                if self.paused == 1:
                    pass
                # Otherwise...
                else:
                    # The game is now paused
                    self.paused = 1
                    # While the game is paused, show the pause menu
                    while self.paused == 1:
                        self.player.Pause()
                        pausemenu = PauseMenu(self)
                        pausemenu.ShowMenu()
                        self.player.Unpause()
                        self.paused = 0
                        pygame.display.update()
            # Otherwise, send the key event to the character
            else:
                self.character.ProcessKeyEvent(event)
        
    def GetBlocks(self):
        """
    Gets the level's block sprite group. May actually be completely useless.
        """
        return self.blocks

    def PlayMusic(self):
        """
    Plays the level's music on an infinite loop.
        """
        # Create an instance of the MusicPlayer class (part of the sound module)
        self.player = MusicPlayer(self.musicpath)
        # Use it to play the music
        self.player.LoopPlay()

    def StopMusic(self):
        """
    Stops music playback.
        """
        self.player.Stop()

    def GetLevelName(self):
        """
    Returns the name of the current level.
        """
        return self.levelname

    def IsPaused(self):
        """
    Returns True or False depending on whether or not the game is currently paused.
    This method may be completely useless; it depends on how the pause menu will function.
        """
        if self.paused == 1:
            return True
        elif self.paused == 0:
            return False
        else:
            return

    def EndLevel(self):
        self.complete = True

    def UpdateScreen(self):
        """
    Update everything on screen without refreshing the display.
        """
        self.RedrawPause()
