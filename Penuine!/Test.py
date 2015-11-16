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
    intro = Intro("1", "Dan's house", "I'm in yer house, testin' yer game engine!")
    intro.ShowIntro()
    
    level = LevelController("Levels\\1", "Data\\music\\1.ogg")
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

    #################################################
    
    intro = Intro("3", "Streets", "To get to the airport safely, you decided to take the underground train. But unfortunately, the nearest stop to the airport is a few streets away, so you'll need to skate for the rest of the journey.")
    intro.ShowIntro()
    
    level = LevelController("Levels\\3", "Data\\music\\1.ogg")
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

    #################################################
    
    intro = Intro("18", "Pixels everywhere", "Apparently travelling through that portal was a bad idea. You've ended up in the realm of underpowered computers - everything's pixellated!")
    intro.ShowIntro()
    
    level = LevelController("Levels\\18", "Data\\music\\8.ogg")
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

    #################################################

    intro = Intro("19", "Ping", "You've found your way onto a Ping playing field! Get off quickly before the game begins again.")
    intro.ShowIntro()
    
    level = LevelController("Levels\\19", "Data\\music\\8.ogg")
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
    raw_input()    

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

else:
    print "Selection is unimplemented!"
    raw_input()
