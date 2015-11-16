#!/usr/bin/env python

## Fading - part of the Penuine game engine
# Controls scene fading in and out, to any given colour and at any given speed.
# Copyright David Barker 2008
#
# Update history:
# Created - Friday 25th December 2007, by David Barker
# Version 1.0 finished - Saturday 26th January 2008, by David Barker

import pygame, sys


class Fader():
    def __init__(self, parent):
        """
    The initialisation method, which takes no arguments.
        """
        self.parent = parent
        self.fading = False
        self.clock = pygame.time.Clock()

    def FadeOut(self, rate, colour):
        """
    Fade out to a specific colour. This takes two arguments:
        -rate: The speed to fade at (total number of frames to fade for)
        -colour: The colour to fade to
    This one will also freeze the display.
        """
        self.fading = True
        while self.fading == True:
            self.frame = 1
            self.screenbuffer = pygame.Surface(pygame.display.get_surface().get_size())
            self.screenbuffer.blit(pygame.display.get_surface(), (0,0))
            for i in range(1, rate):
                screen = pygame.display.get_surface()
                screen.fill(colour)
                newalpha = int(255-((255.0/float(rate))*self.frame))
                self.screenbuffer.set_alpha(newalpha)
                screen.blit(self.screenbuffer.convert_alpha(), (0,0))
                pygame.display.update()
                self.clock.tick(60)
                self.frame = self.frame+1
            self.fading = False
        screen = pygame.display.get_surface()
        screen.fill(colour)
        self.screenbuffer.set_alpha(0)
        screen.blit(self.screenbuffer.convert_alpha(), (0,0))
        pygame.display.update()

    def FadeIn(self, rate):
        """
    Fade a scene in. This takes one argument, rate, which defines the speed at which to fade (the
    total number of frames to fade for).
        """
        self.fading = True
        while self.fading == True:
            self.frame = 1
            for i in range(1, rate):
                # Process events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        pass # This is just here so the mouse position is actually updated each frame
                # Update the parent object's screen
                self.parent.UpdateScreen()
                # Create a black image to overlay
                black = pygame.Surface(pygame.display.get_surface().get_size())
                # Set its alpha for the current frame (becomes less each frame)
                newalpha = int(255-((255.0/float(rate))*self.frame))
                black.set_alpha(newalpha)
                # Overlay the black image
                screen = pygame.display.get_surface()
                screen.blit(black.convert_alpha(), (0,0))
                # Update, pause, and increase the frame counter
                pygame.display.update()
                self.clock.tick(60)
                self.frame = self.frame+1
            self.fading = False
        screen = pygame.display.get_surface()
        pygame.display.update()
