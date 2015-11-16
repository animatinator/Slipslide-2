#!/usr/bin/env python

## Main menu - part of the Penuine game engine
# Creates a main menu and sends data back to the main file
# Copyright ExeSoft 2007
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Version 1.0 finished - *

import pygame, sys
from sound import *
from fading import *


pygame.init()

class Menu():
    def __init__(self):
        """
    The initialisation method, which takes no arguments.
        """
        # Get the screen
        self.screen = pygame.display.get_surface()
        # Initialise the clock
        self.clock = pygame.time.Clock()
        # Initialise a variable to tell the mainloop to keep going
        self.running = True
        # Initialise the return value - if it is returned unchanged, there must have been an error
        # therefore the return value begins as "error"
        self.returnval = "error"
        # Initialise the main font and the four font colours
        self.mainfont = pygame.font.Font("Data\\LithosPro-Black.otf", 40)
        self.col1 = (0,0,0)
        self.col2 = (0,0,0)
        self.col3 = (0,0,0)
        self.col4 = (0,0,0)
        # Load the images
        # The bottom bar
        self.bottombar = pygame.image.load("Data\\mainmenu\\bottombar.png").convert_alpha()
        self.bottombarrect = self.bottombar.get_rect()
        self.bottombarrect.y = 350
        # The first clouds layer
        self.clouds1a = pygame.image.load("Data\\mainmenu\\clouds1.png")
        self.clouds1arect = self.clouds1a.get_rect()
        self.clouds1b = pygame.image.load("Data\\mainmenu\\clouds1.png")
        self.clouds1brect = self.clouds1b.get_rect()
        self.clouds1brect.x = -600
        # The second clouds layer
        self.clouds2a = pygame.image.load("Data\\mainmenu\\clouds2.png")
        self.clouds2arect = self.clouds2a.get_rect()
        self.clouds2b = pygame.image.load("Data\\mainmenu\\clouds2.png")
        self.clouds2brect = self.clouds2b.get_rect()
        self.clouds2brect.x = 600
        # The third clouds layer
        self.clouds3a = pygame.image.load("Data\\mainmenu\\clouds3.png")
        self.clouds3arect = self.clouds3a.get_rect()
        self.clouds3b = pygame.image.load("Data\\mainmenu\\clouds3.png")
        self.clouds3brect = self.clouds3b.get_rect()
        self.clouds3brect.x = -600
        # Create the title
        self.titlefont = pygame.font.Font("Data\\HoboStd.otf", 100)
        self.title = self.titlefont.render("Slipslide 2", True, (0,0,0))
        self.titlerect = self.title.get_rect()
        # Centre it
        self.titlerect.x = (600/2) - (self.titlerect.width/2)
        self.titlerect.y = 150
        # Some text-spacing variables
        self.edge = 50
        self.spacing = 100
        # Create the text objects
        self.item1 = self.mainfont.render("New game", True, self.col1)
        self.item1rect = self.item1.get_rect()
        self.item1rect.y = 420
        self.item2 = self.mainfont.render("Continue game", True, self.col2)
        self.item2rect = self.item2.get_rect()
        self.item2rect.y = 420
        self.item3 = self.mainfont.render("Load custom levels", True, self.col3)
        self.item3rect = self.item3.get_rect()
        self.item3rect.y = 420
        self.item4 = self.mainfont.render("Quit", True, self.col4)
        self.item4rect = self.item4.get_rect()
        self.item4rect.y = 420
        # Play the music
        self.player = MusicPlayer("Data\\music\\1.ogg")
        self.player.LoopPlay()

    def ShowMenu(self):
        """
    Show the menu. This method also contains the menu's mainloop.
        """
        # Draw the screen
        self.AnimateClouds()
        self.UpdateText(pygame.mouse.get_pos())
        self.Redraw()
        # Fade in
        self.fader = Fader(self)
        self.fader.FadeIn(60)
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.UpdateText(event.pos)
                    self.UpdateTextHighlights(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.ProcessClick(event.pos)
            self.Redraw()
            pygame.display.update()
            self.clock.tick(60)
        self.fader.FadeOut(60, (0,0,0))
        self.player.Stop()
        return self.returnval

    def Redraw(self):
        """
    Redraw the screen and everything on it.
        """
        # Animate the cloud positions
        self.AnimateClouds()
        # Fill the screen with the background colour
        self.screen.fill((180,249,255))
        # Blit in the first cloud layer
        self.screen.blit(self.clouds1a, self.clouds1arect)
        self.screen.blit(self.clouds1b, self.clouds1brect)
        # Blit in the title
        self.screen.blit(self.title, self.titlerect)
        # Blit the second clouds layer
        self.screen.blit(self.clouds2a, self.clouds2arect)
        self.screen.blit(self.clouds2b, self.clouds2brect)
        # Blit the third clouds layer
        self.screen.blit(self.clouds3a, self.clouds3arect)
        self.screen.blit(self.clouds3b, self.clouds3brect)
        # Blit in the bottom bar
        self.screen.blit(self.bottombar, self.bottombarrect)
        # Render the menu options to the bottom bar
        self.RenderText()

    def RenderText(self):
        """
    Render the four text objects.
        """
        self.item1 = self.mainfont.render("New game", True, self.col1)
        self.item2 = self.mainfont.render("Continue game", True, self.col2)
        self.item3 = self.mainfont.render("Load custom levels", True, self.col3)
        self.item4 = self.mainfont.render("Quit", True, self.col4)
        self.screen.blit(self.item1, self.item1rect)
        self.screen.blit(self.item2, self.item2rect)
        self.screen.blit(self.item3, self.item3rect)
        self.screen.blit(self.item4, self.item4rect)

    def UpdateText(self, mousepos):
        """
    Update the text objects' positions.
        """
        newrootpos = int((0 - ((float(mousepos[0])/600.0)*(self.item1rect.width + self.item2rect.width + self.item3rect.width + self.item4rect.width + (self.spacing*3) + (self.edge*2))))+mousepos[0])
        self.item1pos = newrootpos+self.edge
        self.item2pos = self.item1pos + self.item1rect.width + self.spacing
        self.item3pos = self.item2pos + self.item2rect.width + self.spacing
        self.item4pos = self.item3pos + self.item3rect.width + self.spacing
        self.item1rect.x = self.item1pos
        self.item2rect.x = self.item2pos
        self.item3rect.x = self.item3pos
        self.item4rect.x = self.item4pos

    def UpdateTextHighlights(self, pos):
        """
    Update the highlights on the four text objects depending on which one currently has mouse focus.
        """
        # New game button
        if pos[0]>self.item1rect.x and pos[0]<(self.item1rect.x+self.item1rect.width) and pos[1]>self.item1rect.y and pos[1]<(self.item1rect.y+self.item1rect.height):
            self.col1 = (0,255,0)
            self.col2 = (0,0,0)
            self.col3 = (0,0,0)
            self.col4 = (0,0,0)
        # Continue game button
        elif pos[0]>self.item2rect.x and pos[0]<(self.item2rect.x+self.item2rect.width) and pos[1]>self.item2rect.y and pos[1]<(self.item2rect.y+self.item2rect.height):
            self.col1 = (0,0,0)
            self.col2 = (0,255,0)
            self.col3 = (0,0,0)
            self.col4 = (0,0,0)
        # Load custom levels button
        elif pos[0]>self.item3rect.x and pos[0]<(self.item3rect.x+self.item3rect.width) and pos[1]>self.item3rect.y and pos[1]<(self.item3rect.y+self.item3rect.height):
            self.col1 = (0,0,0)
            self.col2 = (0,0,0)
            self.col3 = (0,255,0)
            self.col4 = (0,0,0)
        # Quit game button
        elif pos[0]>self.item4rect.x and pos[0]<(self.item4rect.x+self.item4rect.width) and pos[1]>self.item4rect.y and pos[1]<(self.item4rect.y+self.item4rect.height):
            self.col1 = (0,0,0)
            self.col2 = (0,0,0)
            self.col3 = (0,0,0)
            self.col4 = (0,255,0)
        # Otherwise, make sure no other buttons are highlighted
        else:
            self.col1 = (0,0,0)
            self.col2 = (0,0,0)
            self.col3 = (0,0,0)
            self.col4 = (0,0,0)

    def ProcessClick(self, pos):
        """
    Handles mouseclick events sent by the mainloop.
        """
         # New game button
        if pos[0]>self.item1rect.x and pos[0]<(self.item1rect.x+self.item1rect.width) and pos[1]>self.item1rect.y and pos[1]<(self.item1rect.y+self.item1rect.height):
            self.returnval = "new"
            self.running = False
        # Continue game button
        elif pos[0]>self.item2rect.x and pos[0]<(self.item2rect.x+self.item2rect.width) and pos[1]>self.item2rect.y and pos[1]<(self.item2rect.y+self.item2rect.height):
            self.returnval = "continue"
            self.running = False
        # Load custom levels button
        elif pos[0]>self.item3rect.x and pos[0]<(self.item3rect.x+self.item3rect.width) and pos[1]>self.item3rect.y and pos[1]<(self.item3rect.y+self.item3rect.height):
            # Get the list of custom levels from the customlevels.dat data file
            infile = open("customlevels.dat", "r")
            levels = infile.readlines()
            infile.close()
            # Remove the first line (this contains a "do not edit" warning)
            levels.pop(0)    
            # For each line, remove the tailing "\n" character and print it (just a test)
            for level in levels:
                level = level.split("\n")[0]
                print level    
            levelname = "did_it_work?"
            self.returnval = "load %s" % levelname
            self.running = False
        # Quit game button
        elif pos[0]>self.item4rect.x and pos[0]<(self.item4rect.x+self.item4rect.width) and pos[1]>self.item4rect.y and pos[1]<(self.item4rect.y+self.item4rect.height):
            sys.exit()

    def AnimateClouds(self):
        """
    Animates the positions of the cloud layers.
        """
        # The first clouds layer
        if self.clouds1arect.x == 600:
            self.clouds1arect.x = -600
            self.clouds1brect.x = 0
        elif self.clouds1brect.x == 600:
            self.clouds1brect.x = -600
            self.clouds1arect.x = 0
        else:
            self.clouds1arect.x = self.clouds1arect.x+1
            self.clouds1brect.x = self.clouds1brect.x+1
        # The second clouds layer
        if self.clouds2arect.x == -600:
            self.clouds2arect.x = 600
            self.clouds2brect.x = 0
        elif self.clouds2brect.x == -600:
            self.clouds2brect.x = 600
            self.clouds2arect.x = 0
        else:
            self.clouds2arect.x = self.clouds2arect.x-2
            self.clouds2brect.x = self.clouds2brect.x-2
        # The third clouds layer
        if self.clouds3arect.x == 600:
            self.clouds3arect.x = -600
            self.clouds3brect.x = 0
        elif self.clouds3brect.x == 600:
            self.clouds3brect.x = -600
            self.clouds3arect.x = 0
        else:
            self.clouds3arect.x = self.clouds3arect.x+4
            self.clouds3brect.x = self.clouds3brect.x+4

    def UpdateScreen(self):
        """
    Updates all on-screen objects' positions but doesn't redraw. Called by the fading class to make
    the display continue to animate while it is fading in or out.
        """
        mousepos = pygame.mouse.get_pos()
        self.UpdateText(mousepos)
        self.UpdateTextHighlights(mousepos)
        self.Redraw()




    

