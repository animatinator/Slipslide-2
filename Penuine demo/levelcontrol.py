#!/usr/bin/env python

## Level Control - part of the Penuine game engine
# Controls the loading, drawing and updating of game levels
# Copyright ExeSoft 2007
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Finished - *


import pygame
from blocks import *
from character import *


class LevelController():
    """
The Slipslide 2 level loader, copyright David Barker 2007
This takes only one argument, the name of the folder the level's data is stored in. This can be
either relative or absolute as necessary.
    """

    def __init__(self, levelname):
        """
    The initialisation method, which takes the level's name (folder name) as an argument.
        """
        self.screen = pygame.display.get_surface()
        self.levelname = levelname
        self.blocks = pygame.sprite.Group()
        self.LoadLevelObjects()
        self.LoadLevel()
        self.DrawLevel()
        self.Redraw()
        pygame.display.update()

    def Redraw(self):
        self.screen.blit(self.bg, self.bgrect)
        self.blocks.draw(self.screen)
        self.character.Update()

    def LoadLevelObjects(self):
        """
    Loads all the images and data for the current level.
        """
        block = "%s\\block.png" % self.levelname
        background = "%s\\background.png" % self.levelname
        self.blockimage = pygame.image.load(block)
        self.bg = pygame.image.load(background)
        self.bgrect = self.bg.get_rect()
        self.layoutfilepath = "%s\\layout.slf" % self.levelname
        rawminmaxpath = "%s\\area.dat" % self.levelname
        rawminmax = open(rawminmaxpath)
        linelist = []
        for line in rawminmax.readlines():
            line = line.replace("\n", "")
            item = int(line)
            linelist.append(item)
        self.xmin, self.xmax, self.ymin, self.ymax = linelist
        
    def LoadLevel(self):
        """
    Loads the level from the level data file.
        """
        layoutfile = open(self.layoutfilepath)
        lines = layoutfile.readlines()
        self.leveldata = []
        for rawline in lines:
            line = []
            for character in rawline:
                if character == "\n":
                    pass
                else:
                    line.append(character)
            self.leveldata.append(line)

    def DrawLevel(self):
        """
    Creates the level on-screen using the loaded level data and the sprites.
        """
        self.horcount = 0
        self.vercount = 0
        for line in self.leveldata:
            for item in line:
                if item == "2":
                    self.CreateCharacter(self.horcount, self.vercount)
                elif item == "1":
                    self.AddBlock(self.horcount, self.vercount)
                elif item == "0":
                    pass
                self.horcount = self.horcount+1
            self.vercount = self.vercount+1
            self.horcount = 0
        self.screen.blit(self.bg, self.bgrect)
        pygame.display.update()

    def AddBlock(self, posx, posy):
        posx = posx*24
        posy = posy*24
        block = Block((posx, posy), self.blockimage)
        self.blocks.add(block)

    def CreateCharacter(self, posx, posy):
        self.character = Character((posx, posy), self.xmin, self.xmax, self.ymin, self.ymax, self.blocks)

    def ProcessEvent(self, event):
        if event.type == pygame.KEYDOWN:
            self.character.ProcessKeyEvent(event)
        
    def GetBlocks(self):
        """
    Gets the level's block sprite group.
        """
        return self.blocks
