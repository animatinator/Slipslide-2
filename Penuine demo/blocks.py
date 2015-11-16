#!/usr/bin/env python

## Blocks - part of the Penuine game engine
# Creates block sprites
# Copyright ExeSoft 2007
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Finished - *


import pygame

class Block(pygame.sprite.Sprite):
    """
The Slipslide block class, copyright David Barker 2007
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
