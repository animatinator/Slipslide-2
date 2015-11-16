import sys
import pygame
#from levelcontrol import *
#from mainmenu import *
#from levelintros import *
from penuine import *


pygame.init()
screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("Penuine test")

levels = open("Levels\\levels.dat", "r")
levels = levels.read()
levels = levels.split("\n")

menu = Menu()
option = menu.ShowMenu()
print levels

if option == "new":

    for item in levels:
        print item
        itemn = item.split("\t")
        print itemn
        intro = Intro(itemn[0], itemn[1], itemn[2])
        intro.ShowIntro()
    
        level = LevelController("Levels\\%s" % str(itemn[0]), "Data\\music\\%s.ogg" %  str(itemn[3]))
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

   

elif option.split(" ")[0] == "load":
    option = option.split()
    option.pop(0)
    levelname = "".join(option)
    level = LevelController(levelname, "%s\\music.ogg" % levelname, True)
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

elif option == "continue":
    print "Selection is a work in progress"
    raw_input()

else:
    print "Selection is unimplemented!"
    raw_input()
