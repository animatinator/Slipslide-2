#!/usr/bin/env python

## Character - part of the Penuine game engine
# Controls the character sprite's movement, animation, sound and drawing.
# Copyright ExeSoft 2007
#
# Update history:
# Created - Monday 17th December 2007, by David Barker
# Finished - *

import pygame


class Character(pygame.sprite.Sprite):

    def __init__(self, pos, xmin, xmax, ymin, ymax, blocks):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("char//Ball.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0]*24, pos[1]*24
        self.screen = pygame.display.get_surface()
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.direction = "stop"
        self.oldrect = self.rect
        self.blocks = blocks
        self.Redraw()

    def ProcessKeyEvent(self, event):
        if event == None:
            pass
        if self.direction == "stop":
            if event.key == pygame.K_UP:
                self.direction = "up"
            elif event.key == pygame.K_DOWN:
                self.direction = "down"
            elif event.key == pygame.K_LEFT:
                self.direction = "left"
            elif event.key == pygame.K_RIGHT:
                self.direction = "right"

    def GetGridPos(self):
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
        self.gridpos = self.GetGridPos()
        collision = pygame.sprite.spritecollideany(self, self.blocks)
        if collision:
            self.oldrect = self.rect
            self.direction = "stop"
            self.rect.x = self.gridpos[0]*24
            self.rect.y = self.gridpos[1]*24
            pygame.display.update()
        if self.rect.x<self.xmin:
            self.direction = "stop"
            self.rect.x = self.xmin
            pygame.display.update()
        if self.rect.x>(self.xmax-self.rect.width):
            self.direction = "stop"
            self.rect.x = (self.xmax-self.rect.width)
            pygame.display.update()
        if self.rect.y<self.ymin:
            self.direction = "stop"
            self.rect.y = self.ymin
            pygame.display.update()
        if self.rect.y>(self.ymax-self.rect.height):
            self.direction = "stop"
            self.rect.y = (self.ymax-self.rect.height)
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
        self.screen.blit(self.image, self.rect)
        pygame.display.update([self.rect, self.oldrect])

    def Move(self, amount):
        self.oldrect = self.rect
        self.rect = self.rect.move(amount)










        
