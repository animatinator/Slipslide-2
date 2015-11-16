import pygame, sys

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 480))
mainfont = pygame.font.Font(None, 50)
rootpos = (10, 400)
item1 = mainfont.render("New game", True, (255,255,255), (0,0,0))
item1rect = item1.get_rect()
item1rect.y = 400
item2 = mainfont.render("Continue game", True, (255,255,255), (0,0,0))
item2rect = item2.get_rect()
item2rect.y = 400
item3 = mainfont.render("Load custom levels", True, (255,255,255), (0,0,0))
item3rect = item3.get_rect()
item3rect.y = 400
item4 = mainfont.render("Quit", True, (255,255,255), (0,0,0))
item4rect = item4.get_rect()
item4rect.y = 400
spacing = 100
edge = 50

def Update(mousepos):
    newrootpos = int((0 - ((float(mousepos[0])/600.0)*(item1rect.width + item2rect.width + item3rect.width + item4rect.width + (spacing*3) + (edge*2))))+mousepos[0])
    item1pos = newrootpos+edge
    item2pos = item1pos + item1rect.width+spacing
    item3pos = item2pos + item2rect.width + spacing
    item4pos = item3pos + item3rect.width + spacing
    return item1pos, item2pos, item3pos, item4pos
    
def RedrawText():
    screen.blit(item1, item1rect)
    screen.blit(item2, item2rect)
    screen.blit(item3, item3rect)
    screen.blit(item4, item4rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            rects = Update(event.pos)
            item1rect.x, item2rect.x, item3rect.x, item4rect.x = rects

    screen.fill((0,0,0))
    RedrawText()
    pygame.display.update()
    clock.tick(60)
