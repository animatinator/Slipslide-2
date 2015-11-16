import pygame, sys
from animload import *

pygame.init()

screen = pygame.display.set_mode((600, 480))

animloader = AnimLoader("Data\\char\\slideanim.png")
array = animloader.GetArray()

for i in range(0, len(array)):
    screen.blit(array[i], (i*24, 100))
pygame.display.update()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    for i in range(0, len(array)):
        screen.blit(array[i], (i*24, 100))
        pygame.display.update()

