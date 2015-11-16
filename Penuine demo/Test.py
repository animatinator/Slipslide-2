import sys
import pygame
from levelcontrol import *


pygame.init()
screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("Penuine test")
level = LevelController("2")
clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        else:
            level.ProcessEvent(event)
    level.Redraw()
    clock.tick(60)
