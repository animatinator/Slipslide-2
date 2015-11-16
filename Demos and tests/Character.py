import pygame
import sys

class Character(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load("Ball.png")
        self.imagerect = self.image.get_rect()
        self.imagerect.x = posx
        self.imagerect.y = posy
        self.screen.blit(self.image, self.imagerect)
        pygame.display.update()

    def Move(self, amount):
        oldrect = self.imagerect
        self.imagerect = self.imagerect.move(amount)
        self.screen.blit(self.image, self.imagerect)
        pygame.display.update([self.imagerect, oldrect])
        print dir(oldrect)

    def Update(self, event):
        if event == None:
            return
        if event.key == pygame.K_UP:
            self.Move([0, -10])
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 480))
    character = Character(20, 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                character.Update(event)

    
if __name__ == "__main__":
    main()
