#!/usr/bin/env python

## Level Intros - part of the Penuine game engine
# Creates level intro sequences which terminate when the user clicks "play".
# Copyright David Barker 2008
#
# Update history:
# Created - Tuesday 29th January 2008, by David Barker
# Version 1.0 finished - *


import pygame
from fading import *


class Intro():
    """
The Penuine intro sequence class, copyright David Barker 2008.
    """
    def __init__(self, levelnum, title, text):
        """
    The initialisation mathod, which takes two arguments:
        -levelnum - The number of the current level
        -title - The level's title
        -text - The text to be displayed as a description
        """
        # Initialise the variables
        self.levelnum = levelnum
        self.title = title
        self.text = text
        # Get the screen
        self.screen = pygame.display.get_surface()
        # Initialise the clock
        self.clock = pygame.time.Clock()
        # Initialise a variable to tell the mainloop to keep going
        self.running = True

        # Initialise the fonts
        # The title font
        self.font1 = pygame.font.Font("Data\\HoboStd.otf", 30)
        # The description font
        self.font2 = pygame.font.Font("Data\\LithosPro-Black.otf", 20)
        # The 'Start' text font
        self.font3 = pygame.font.Font("Data\\LithosPro-Black.otf", 40)
        # The 'Start' text colour
        self.col1 = (0,0,0)

        # Load the images
        # The first clouds layer
        self.clouds1a = pygame.image.load("Data\\mainmenu\\clouds1.png").convert_alpha()
        self.clouds1arect = self.clouds1a.get_rect()
        self.clouds1b = pygame.image.load("Data\\mainmenu\\clouds1.png").convert_alpha()
        self.clouds1brect = self.clouds1b.get_rect()
        self.clouds1brect.x = -600
        # The second clouds layer
        self.clouds2a = pygame.image.load("Data\\mainmenu\\clouds2.png").convert_alpha()
        self.clouds2arect = self.clouds2a.get_rect()
        self.clouds2b = pygame.image.load("Data\\mainmenu\\clouds2.png").convert_alpha()
        self.clouds2brect = self.clouds2b.get_rect()
        self.clouds2brect.x = 600
        # The third clouds layer
        self.clouds3a = pygame.image.load("Data\\mainmenu\\clouds3.png").convert_alpha()
        self.clouds3arect = self.clouds3a.get_rect()
        self.clouds3b = pygame.image.load("Data\\mainmenu\\clouds3.png").convert_alpha()
        self.clouds3brect = self.clouds3b.get_rect()
        self.clouds3brect.x = -600

        # Get the level description as an array of word-wrapped lines
        self.textarray = self.GetWrappedTextArray()

    def ShowIntro(self):
        """
    Show the level intro. This method also contains the intro's mainloop.
        """
        # Draw the screen
        self.AnimateClouds()
        self.Redraw()
        # Fade in
        self.fader = Fader(self)
        self.fader.FadeIn(60)
        while self.running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.OnMouseMove(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.ProcessClick(event.pos)
            self.Redraw()
            pygame.display.update()
            self.clock.tick(60)
        self.fader.FadeOut(60, (0,0,0))

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
        # Blit the second clouds layer
        self.screen.blit(self.clouds2a, self.clouds2arect)
        self.screen.blit(self.clouds2b, self.clouds2brect)
        # Blit the third clouds layer
        self.screen.blit(self.clouds3a, self.clouds3arect)
        self.screen.blit(self.clouds3b, self.clouds3brect)
        # Draw in the description text
        self.DrawDescriptionText()
        # Draw in the title
        self.DrawTitle()
        # Draw the "Start" text
        self.DrawStartText()

    def DrawTitle(self):
        string = "Level %s - %s" % (self.levelnum, self.title)
        text = self.font1.render(string, True, (0,0,0)).convert_alpha()
        textrect = text.get_rect()
        textrect.x = (self.screen.get_rect().width/2)-(textrect.width/2)
        textrect.y = 25
        self.screen.blit(text, textrect)

    def ProcessClick(self, pos):
        if pos[0]>self.starttextrect.x and pos[1]>self.starttextrect.y and pos[0]<(self.starttextrect.x+self.starttextrect.width) and pos[1]<(self.starttextrect.y+self.starttextrect.height):
            self.running = False

    def OnMouseMove(self, pos):
        if pos[0]>self.starttextrect.x and pos[1]>self.starttextrect.y and pos[0]<(self.starttextrect.x+self.starttextrect.width) and pos[1]<(self.starttextrect.y+self.starttextrect.height):
            self.col1 = (0,255,0)
        else:
            self.col1 = (0,0,0)

    def DrawDescriptionText(self):
        for num in range(0, len(self.textarray)):
            item = self.textarray[num]
            text = self.font2.render(item, True, (0,0,0))
            textrect = text.get_rect()
            textrect.x = self.textrect.x
            textrect.y = (self.textrect.y) + (num*(textrect.height))
            self.screen.blit(text, textrect)

    def DrawStartText(self):
        text = self.font3.render("Start >", True, self.col1).convert_alpha()
        textrect = text.get_rect()
        textrect.x = 400
        textrect.y = 400
        self.starttextrect = textrect
        self.screen.blit(text, textrect)
        
    def GetWrappedTextArray(self):
        rect = self.screen.get_rect()
        rect.width = 500
        rect.height = 300
        rect.x = (self.screen.get_rect().width/2)-(rect.width/2)
        rect.y = 100
        self.textrect = rect
        wrapper = TextWrapper(self.text, self.textrect, self.font2)
        textarray = wrapper.GetArray()
        return textarray

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
        self.Redraw()

class TextWrapper():
    def __init__(self, string, size, font):
        self.screen = pygame.display.get_surface()
        self.rect = size
        self.font = font
        self.string = string

    def GetArray(self):
        # Split the string into words
        self.words = self.string.split(" ")
        # Create lines from the words
        self.lines = []
        self.currentline = ""
        for word in self.words:
            currentlinelength = self.font.size(self.currentline+word)[0]
            if currentlinelength > self.rect.width:
                self.lines.append(self.currentline)
                self.currentline = word+" "
            else:
                self.currentline = self.currentline+word+" "
        self.lines.append(self.currentline)
        # Make an array of the lines
        self.array = []
        for i in range(0, len(self.lines)):
            self.array.append(self.lines[i])
        # Return the array
        return self.array















        
