#!/usr/bin/env python

## Sound - part of the Penuine game engine
# Controls sound loading and playback in-game
# Copyright David Barker 2008
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Version 1.0 finished - Wednesday 13th February 2008

import pygame
from pygame import mixer
mixer.init()


class MusicPlayer():
    """
A class that plays music from a given file. This takes one argument; "filepath", which is the
filepath of the *.OGG format music to play.
    """
    def __init__(self, filepath):
        """
    Initialise the music player.
        """
        self.channel = pygame.mixer.Channel(7)
        self.music = mixer.Sound(filepath)
        self.playmode = ""
        self.paused = 0

    def Play(self):
        """
    Play the currently loaded music track.
        """
        self.channel.set_volume(1.0)
        self.channel.play(self.music, 0)
        self.playmode = "play"

    def LoopPlay(self):
        """
    Play the currently loaded music track on an infinite loop.
        """
        self.channel.set_volume(1.0)
        self.channel.play(self.music, -1)
        self.playmode = "loopplay"

    def Stop(self):
        """
    Stop the music playback.
        """
        self.channel.fadeout(1000)

    def Pause(self):
        """
    Pause the music playback.
        """
        if self.paused == 0:
            self.channel.pause()
            self.paused = 1

    def Unpause(self):
        """
    Unpause the music playback. The music must be paused in order for this to work.
        """
        if self.paused == 1:
            self.channel.unpause()
            self.paused = 0
