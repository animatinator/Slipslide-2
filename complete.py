#!/usr/bin/env python

## Complete - part of the Penuine game engine
# Displays a "level complete" message at the end of each level (called by levelcontrol)
# Copyright David Barker 2008
#
# Update history:
# Created - Tuesday 12th February 2008, by David Barker
# Version 1.0 finished - Tuesday 12th February 2008, by David Barker


import pygame, sys


class Complete():
    """
The Slipslide 2 complete class, copyright David Barker 2007. This displays a "level complete" image,
and takes only the parent object as an argument.
    """
    def __init__(self, parent):
        self.image = pygame.image.load("Data\\complete.png").convert_alpha()
        self.imagerect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.imagerect.x = (self.screen.get_rect().width/2)-(self.imagerect.width/2)
        self.imagerect.y = (self.screen.get_rect().height/2)-(self.imagerect.height/2)
        self.parent = parent

    def ShowMessage(self):
        running = True
        while running == True:
            self.parent.UpdateScreen()
            self.screen.blit(self.image, self.imagerect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    running = False
            pygame.display.update()
