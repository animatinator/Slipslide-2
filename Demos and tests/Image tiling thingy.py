
import pygame, sys


pygame.init()
screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("Image tiling testorama thingummyjizzler of AWESOMENESS!!!11!!!!1!!1!3!")

clock = pygame.time.Clock()

tlcorner = pygame.image.load("Tile images\\topleft.png")
trcorner = pygame.image.load("Tile images\\topright.png")
banner = pygame.image.load("Tile images\\banner.png")
tile = pygame.image.load("Tile images\\tile.png")

def DrawBox(size):
    surface = pygame.Surface(size, flags=pygame.SRCALPHA)
    rect = surface.get_rect()
    rect.x = 300-(rect.width/2)
    rect.y = 240-(rect.height/2)
    
    surface.blit(tlcorner, (0,0))
    surface.blit(trcorner, ((rect.width-trcorner.get_rect().width), 0))

    for column in range (24, (rect.width-trcorner.get_rect().width)):
        surface.blit(banner, (column, 0))

    surface.set_alpha(0)
    
    return surface, rect

def Redraw():
    screen.blit(surface, rect)
    pygame.display.update()

def UpdateSurface(count):
    for column in range(0, rect.width):
        surface.blit(tile, (column, count*2))
    stepcount = ((rect.height-24)/2)
    jump = 255.0/float(stepcount)
    currentanimframe = count-12
    surface.set_alpha(jump*currentanimframe)
    count = count+1
    return surface, count

surface, rect = DrawBox((400, 300))

count = 12

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill((0,0,0))
    surface, count = UpdateSurface(count)
    Redraw()
    clock.tick(60)
