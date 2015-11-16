#!/usr/bin/env python

## Blocks - part of the Penuine game engine
# Creates block sprites
# Copyright David Barker 2008
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Version 1.0 finished - *


import pygame

class Block(pygame.sprite.Sprite):
    """
The Slipslide block class, copyright David Barker 2007.
    """
    def __init__(self, pos, image):
        """
    The initialisation method. This takes two arguments:
        -pos: A tuple for the block's on-screen position
        -image: The image to use
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.posx, self.posy = pos
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.posx, self.posy
        self.screen = pygame.display.get_surface()
        self.screen.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    """
The Slipslide wall class, copyright David Barker 2007.
    """
    def __init__(self, pos):
        """
    The initialisation method. This takes only one argument; a tuple for the wall section's
    on-screen position.
    NOTE: Needs to be cleaned up and speeded up. It's currently loading a PNG image unnecessarily in
    order to get a rect of the right size and shape.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data//wall.png").convert_alpha()
        self.posx, self.posy = pos
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.posx, self.posy
        self.screen = pygame.display.get_surface()
        #self.screen.blit(self.image, self.rect)

class Hole(pygame.sprite.Sprite):
    """
The Slipslide hole class, copyright David Barker 2007
    """
    def __init__(self, pos, image):
        """
    Write some friggin' documentation you foo'!
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.posx, self.posy = pos[0]*24, pos[1]*24
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.posx, self.posy
        self.screen = pygame.display.get_surface()
        self.screen.blit(self.image, self.rect)
