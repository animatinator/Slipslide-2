import pygame
import sys

class Drawing():
    def __init__(self, blocks):
        self.blocks = blocks
        self.screen = pygame.display.get_surface()
        self.bg = pygame.image.load("Background.jpg").convert()
        self.bgrect = self.bg.get_rect()
        self.screen.blit(self.bg, self.bgrect)
        self.blocks.draw(screen)
        pygame.display.update()
    def Redraw(self):
        self.screen.blit(self.bg, self.bgrect)
        self.blocks.draw(self.screen)

class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Block.png")
        self.posx, self.posy = pos
        self.posx = self.posx*24
        self.posy = self.posy*24
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.posx, self.posy
        self.screen = pygame.display.get_surface()
        self.screen.blit(self.image, self.rect)

class Character(pygame.sprite.Sprite):
    def __init__(self, pos, xmin, xmax, ymin, ymax, animframes, blocks):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ball.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0]*24, pos[1]*24
        self.screen = pygame.display.get_surface()
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax
        self.animframes = animframes
        self.direction = "stop"
        self.oldrect = self.rect
        self.blocks = blocks
    def KeyRespond(self, event):
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
            gridposy = (self.rect.y/24)-1
        elif self.direction == "left":
            gridposx = (self.rect.x/24)+1
            gridposy = (self.rect.y/24)
        elif self.direction == "right":
            gridposx = (self.rect.x/24)-1
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
            self.Move([0, -10])
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

pygame.init()
screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("ExeSoft Slipslide 2 -- Pre-alpha test")
block1 = Block((10, 5))
#rect1 = block1.image.get_rect()
block2 = Block((12, 17))
#rect2 = block2.image.get_rect()
block3 = Block((1, 1))
#rect3 = block3.image.get_rect()
blocks = pygame.sprite.Group()
blocks.add([block1, block2, block3])
#blockrects = [rect1, rect2, rect3]
character = Character((3, 5), 24, 576, 24, 456, ["not", "implemented", "yet"], blocks)
blocks.draw(screen)
pygame.display.update()
clock = pygame.time.Clock()
drawing = Drawing(blocks)

while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            character.KeyRespond(event)
    drawing.Redraw()
    character.Update()
