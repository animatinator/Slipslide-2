import sys
import pygame
from levelcontrol import *
from mainmenu import *
from levelintros import *


pygame.init()
screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("Penuine test")

menu = Menu()
option = menu.ShowMenu()

if option == "new":
    #intro = Intro("1", "Test level one", "Get to the end of the test level!")
    #intro.ShowIntro()
    level = LevelController("Levels\\Test_1", "Data\\music\\1.ogg")
    clock = pygame.time.Clock()

    while level.complete == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                level.ProcessEvent(event)
        level.Redraw()
        clock.tick(60)

    print "Congratulations, you finished the level!"

    ##########
    level = LevelController("Levels\\Test_3", "Data\\music\\2.ogg")
    clock = pygame.time.Clock()

    while level.complete == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                level.ProcessEvent(event)
        level.Redraw()
        clock.tick(60)

    print "Congratulations, you finished the level!"
    ##########
    raw_input()

elif option.split(" ")[0] == "load":
    option = option.split()
    option.pop(0)
    levelname = "".join(option)
    level = LevelController("New_level", "New level\\music.ogg")
    clock = pygame.time.Clock()

    while level.complete == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                level.ProcessEvent(event)
        level.Redraw()
        clock.tick(60)

    print "Congratulations, you finished the level!"

else:
    print "Selection is unimplemented!"
    raw_input()
