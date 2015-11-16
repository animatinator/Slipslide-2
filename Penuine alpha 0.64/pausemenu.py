#!/usr/bin/env python

## Pause Menu - part of the Penuine game engine
# Creates a pause menu, sending signals back to the level controller
# Copyright ExeSoft 2007
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Version 1.0 finished - *

import sys
import pygame


class PauseMenu():
    def __init__(self, parent):
        """
    The initialisation method, which takes no variables.
        """
        # Make a local reference to the parent object
        self.parent = parent
        # Load the background image, get its rect and centre it
        self.image = pygame.image.load("Data\\pause\\background.png")
        self.mainrect = self.image.get_rect()
        self.mainrect.x = 150
        self.mainrect.y = 120
        # Keep a record of the menu's position
        self.pos = (self.mainrect.x, self.mainrect.y)
        # Some variables
        self.paused = True
        self.dragging = False
        self.continuetextcolour = (0,0,0)
        self.quittextcolour = (0,0,0)
        # Get the screen surface
        self.screen = pygame.display.get_surface()
         # Create the main font
        self.mainfont = pygame.font.Font(None, 50)
        # Render the text
        self.RenderText()

    def RenderText(self):
        """
    Create a font and render the text objects with it.
    WARNING: This method contains a megaton of numbers!
        """
        # Render the text objects and get their rects
        self.continuetext = self.mainfont.render("Continue", True, self.continuetextcolour)
        self.continuetextrect = self.continuetext.get_rect()
        self.quittext = self.mainfont.render("Quit", True, self.quittextcolour)
        self.quittextrect = self.quittext.get_rect()
        # Center the text objects in the pause menu window
        self.continuetextrect.x = self.pos[0]+((self.mainrect.width/2)-(self.continuetextrect.width/2))
        self.quittextrect.x = self.pos[0]+((self.mainrect.width/2)-(self.quittextrect.width/2))
        # Set their Y-positions
        self.continuetextrect.y = self.pos[1]+80
        self.quittextrect.y = self.pos[1]+120
        # Blit them to the screen and update
        self.screen.blit(self.continuetext, self.continuetextrect)
        self.screen.blit(self.quittext, self.quittextrect)
        pygame.display.update([self.continuetextrect, self.quittextrect])

    def RedrawText(self):
        """
    Redraws the menu text.
        """
        # Center both text objects in the pause menu window
        self.continuetextrect.x = self.pos[0]+((self.mainrect.width/2)-(self.continuetextrect.width/2))
        self.quittextrect.x = self.pos[0]+((self.mainrect.width/2)-(self.quittextrect.width/2))
        # Set their Y-positions
        self.continuetextrect.y = self.pos[1]+80
        self.quittextrect.y = self.pos[1]+120
        # Blit them to the screen
        self.screen.blit(self.continuetext, self.continuetextrect)
        self.screen.blit(self.quittext, self.quittextrect)
        
    def ShowMenu(self):
        """
    Shows the menu. This method contains the menu's mainloop and calls all other methods.
        """
        clock = pygame.time.Clock()
        while self.paused == True:
            self.ProcessEvents()
            self.Redraw()
            clock.tick(60)
        self.parent.Redraw()

    def ProcessEvents(self):
        """
    Handle all incoming events.
        """
        for event in pygame.event.get():
            # If the user quits the program, make it quit
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # If the user presses the "P" key, the game is no longer paused. This will automatically
                # exit the mainloop in the ShowMenu() method
                if event.key == pygame.K_p:
                    self.paused = False
            # If the user presses down the mouse button
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse position
                pos = event.pos
                # If the mouse is within the pause menu window
                if pos[0]>self.pos[0] and pos[1]>self.pos[1] and pos[0]<(self.pos[0]+300) and pos[1]<(self.pos[1]+224):
                    # If the user has clicked "Continue", the game is no longer paused
                    if pos[0]>self.continuetextrect.x and pos[1]>self.continuetextrect.y and pos[0]<self.continuetextrect.width+self.continuetextrect.x and pos[1]<self.continuetextrect.height+self.continuetextrect.y:
                        self.paused = False
                    if pos[0]>self.quittextrect.x and pos[1]>self.quittextrect.y and pos[0]<self.quittextrect.width+self.quittextrect.x and pos[1]<self.quittextrect.height+self.quittextrect.y:
                        self.Quit()
                    else:
                        # Start dragging the window
                        self.dragging = True
                        # Get the relative mouse position (position on the pause menu window)
                        self.relmousepos = (pos[0]-self.pos[0], pos[1]-self.pos[1])
            # If the user releases the mouse button and they were dragging, stop dragging
            elif event.type == pygame.MOUSEBUTTONUP and self.dragging == True:
                self.dragging = False
            # If the user moves the mouse
            elif event.type == pygame.MOUSEMOTION:
                # Get the new mouse position
                pos = event.pos
                # If the window is being dragged
                if self.dragging == True:
                    # Set the pause menu window's position to the new mouse mosition minus the mouse's
                    # position on the window
                    self.mainrect.x = pos[0]-self.relmousepos[0]
                    self.mainrect.y = pos[1]-self.relmousepos[1]
                    # Record the window's position
                    self.pos = (self.mainrect.x, self.mainrect.y)
                # If not dragging
                else:
                    # If the mouse is hovering over the continue button, highlight it
                    if pos[0]>self.continuetextrect.x and pos[1]>self.continuetextrect.y and pos[0]<self.continuetextrect.width+self.continuetextrect.x and pos[1]<self.continuetextrect.height+self.continuetextrect.y:
                        self.continuetextcolour = (0,255,0)
                        self.quittextcolour = (0,0,0) # Make sure the quit button is not highlighted
                        self.RenderText() # Re-render the text using the new colours
                    # If the mouse is hovering over the quit button, highlight it
                    elif pos[0]>self.quittextrect.x and pos[1]>self.quittextrect.y and pos[0]<self.quittextrect.width+self.quittextrect.x and pos[1]<self.quittextrect.height+self.quittextrect.y:
                        self.quittextcolour = (0,255,0)
                        self.continuetextcolour = (0,0,0) # Make sure the continue button is not highlighted
                        self.RenderText() # Re-render the text using the new colours
                    # Otherwise, make sure neither of the menu items are highlighted
                    else:
                        self.continuetextcolour = (0,0,0)
                        self.quittextcolour = (0,0,0)
                        self.RenderText()

    def Redraw(self):
        """
    Redraw the screen.
        """
        # First redraw the level
        self.parent.RedrawPause()
        # Blit the background image to its new position and update
        self.screen.blit(self.image, self.mainrect)
        self.RedrawText()
        pygame.display.update(self.mainrect)
        # If the pause menu window is being dragged, update the whole screen to avoid trails when
        # the window moves
        if self.dragging == True:
            pygame.display.update()

    def Quit(self):
        """
    Quit the game.
        """
        sys.exit()
