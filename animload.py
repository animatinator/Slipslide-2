#!/usr/bin/env python

## Animation loader - part of the Penuine game engine
# Loads individual animation frames from filmstrip image files, and returns a list
# Copyright David Barkeer 2008
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Development began - Monday 11th February 2008
# Version 1.0 finished - Tuesday 12th February 2008


import pygame


class AnimLoader():
    """
The Slipslide 2 animation loader class, copyright David Barker 2008. This takes one argument, the
filmstrip file to load.
    """
    def __init__(self, filepath):
        """
    The initialisation method, which takes one argument for the location of the filmstrip animation
    to load.
        """
        self.filepath = filepath
        self.filmstrip = pygame.image.load(filepath)
        self.filmstriprect= self.filmstrip.get_rect()

    def GetArray(self):
        """
    Returns the animation as an array of images
        """
        array = []
        for num in range(0, self.filmstriprect.height/24):
            rect = self.filmstrip.get_rect()
            rect.height = ((self.filmstriprect.height/24)-num)*24
            rect.width = 0
            rect.y = (num+1)*24
            image = pygame.transform.chop(self.filmstrip, rect)
            rect = self.filmstrip.get_rect()
            rect.width = 0
            rect.height = num*24
            rect.y = 0
            image = pygame.transform.chop(image, rect).convert_alpha()
            array.append(image)
        return array
