#!/usr/bin/env python

## Character - part of the Penuine game engine
# Controls the character sprite's movement, animation, sound and drawing.
# Copyright ExeSoft 2007
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Version 1.0 finished - *

import pygame


class Character(pygame.sprite.Sprite):
    """
The Slipslide 2 character class, which controls the main character sprite's drawing, movement,
events, animation, sound and physics.
    """

    def __init__(self, parent, pos, finx, finy, blocks, holes):
        """
    The initialisation method, which takes the following variables:
        -parent: The parent object
        -pos: A tuple for the grid position of the character's starting position
        -finx: The x-position in grid co-ordinates of the level's end
        -finy: The y-position in grid co-ordinates of the level's end
        -blocks: The sprite group containing all the level's blocks
        -holes: The sprite group containing all the level's holes
        """
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.startpos = pos
        self.image = pygame.image.load("Data//char//main.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.startpos[0]*24, self.startpos[1]*24
        self.screen = pygame.display.get_surface()
        self.finx, self.finy = finx, finy
        self.direction = "stop"
        self.finished = False
        self.oldrect = self.rect
        self.blocks = blocks
        self.holes = holes
        self.RedrawWithoutUpdate()

    def ProcessKeyEvent(self, event):
        """
    Processes keyboard events passed down to it by the level controller.
        """
        if self.finished == False: # Stop responding to keypress events when the level is complete
            if event == None:
                pass
            if event.key == pygame.K_r:
                self.RestartLevel()
            if self.direction == "stop":
                if event.key == pygame.K_UP:
                    self.direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.direction = "right"
                elif event.key == pygame.K_r:
                    self.RestartLevel()

    def GetGridPos(self):
        """
    Returns a tuple of the grid position (not pixel co-ordinates) of the character in a 25*20 grid.
        """
        if self.direction == "up":
            gridposx = (self.rect.x/24)
            gridposy = (self.rect.y/24)+1
        elif self.direction == "down":
            gridposx = (self.rect.x/24)
            gridposy = (self.rect.y/24)
        elif self.direction == "left":
            gridposx = (self.rect.x/24)+1
            gridposy = (self.rect.y/24)
        elif self.direction == "right":
            gridposx = (self.rect.x/24)
            gridposy = (self.rect.y/24)
        elif self.direction == "stop":
            gridposx = (self.rect.x/24)
            gridposy = (self.rect.y/24)
        return (gridposx, gridposy)

    def Update(self):
        """
    Updates the character's position, calculates physics and redraws the character.
        """
        self.gridpos = self.GetGridPos()
        if self.gridpos == (self.finx, self.finy) and self.finished == False:
            self.finished = True
            self.Finish()
        blockcollision = pygame.sprite.spritecollideany(self, self.blocks)
        if blockcollision:
            self.oldrect = self.rect
            self.direction = "stop"
            self.rect.x = self.gridpos[0]*24
            self.rect.y = self.gridpos[1]*24
            pygame.display.update()
        holecollision = pygame.sprite.spritecollideany(self, self.holes)
        if holecollision:
            self.direction = "stop"
            self.RestartLevel()
        if self.rect.x<0:
            self.direction = "stop"
            self.rect.x = 0
            pygame.display.update()
        if self.rect.x>576:
            self.direction = "stop"
            self.rect.x = 576
            pygame.display.update()
        if self.rect.y<0:
            self.direction = "stop"
            self.rect.y = 0
            pygame.display.update()
        if self.rect.y>456:
            self.direction = "stop"
            self.rect.y = 456
            pygame.display.update()
        if self.direction == "stop":
            self.Move([0,0])
        elif self.direction == "up":
            self.Move([0,-10])
        elif self.direction == "down":
            self.Move([0, 10])
        elif self.direction == "left":
            self.Move([-10, 0])
        elif self.direction == "right":
            self.Move([10, 0])
        self.Redraw()

    def Redraw(self):
        """
    Redraws the character on-screen.
        """
        self.screen.blit(self.image, self.rect)
        pygame.display.update([self.rect, self.oldrect])

    def RedrawWithoutUpdate(self):
        """
    A modified redraw method that doesn't update the screen, for use by the pause menu's update
    methods.
        """
        self.screen.blit(self.image, self.rect)

    def Move(self, amount):
        """
    Moves the character, recording the previous position in order to redraw it. Takes a list of two
    values; one for the x movement and one for the y movement (both in pixels).
        """
        self.oldrect = self.rect
        self.rect = self.rect.move(amount)

    def Finish(self):
        """
    A method which is called upon completion of the level.
        """
        self.parent.StopMusic()
        self.parent.EndLevel()

    def RestartLevel(self):
        """
    Restarts the level.
        """
        self.direction = "stop"
        self.oldrect = self.rect
        self.rect.x = self.startpos[0]*24
        self.rect.y = self.startpos[1]*24
        self.Redraw()
        self.parent.Redraw()
        pygame.display.update()

    def SetFinishPoint(self, finx, finy):
        """
    Sets the finish point to a different location.
        """
        self.finx, finy = finx, finy

    def UpdateHoles(self, holes):
        """
    Updates the character's list of hole sprites to synchronise with changes to the level
    controller's list.
        """
        self.holes = holes
