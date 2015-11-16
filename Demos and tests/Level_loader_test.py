import pygame
import sys

class Loader():
    """
A level loading class for loading game levels from text files.
Still in alpha currently, as it is missing the ability to load block sprites and
does not yet use the standard screen and sprite sizes.
"""
    def __init__(self, filepath):
        """
The initialisation class for the level loader.
Variables:
    -filepath: The file to load the level from
"""
        self.screen = pygame.display.get_surface()
        self.squares = []
        self.LoadLevelData(filepath)

    def LoadLevelData(self, filepath):
        infile = open(filepath)
        lines = infile.readlines()
        self.rects = []
        self.leveldata = []
        for rawline in lines:
            line = []
            for character in rawline:
                if character == "\n":
                    pass
                else:
                    line.append(character)
            self.leveldata.append(line)

    def GetLevelData(self):
        """
A method for getting the raw level data from the opened file.
"""
        return self.leveldata

    def DrawLevel(self):
        """
Draws the currently-loaded level to the screen. Should eventually return a group
of block sprites.
"""
        self.horcount = 0
        self.vercount = 0
        for line in self.leveldata:
            for item in line:
                if item == "1":
                    self.CreateSquare(self.horcount, self.vercount, (255,255,255))
                elif item == "0":
                    pass
                self.horcount = self.horcount+1
            self.vercount = self.vercount+1
            self.horcount = 0
        pygame.display.update(self.rects)

    def CreateSquare(self, posx, posy, colour):
        """
Creates a 24*24 square and draws it to the screen in the position specified.
"""
        posx = (posx)*24
        posy = int(posy)*24
        square = pygame.Surface((24,24))
        square.fill(colour)
        squarerect = square.get_rect()
        squarerect.x = posx
        squarerect.y = posy
        self.squares.append([square, squarerect])
        self.screen.blit(square, squarerect)
        self.rects.append(squarerect)


def Main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600,480))
    screen.fill((0,0,0))
    pygame.display.set_caption("ExeSoft Slipslide level loader -- Pre-alpha test version")
    loader = Loader("Test level.txt")
    loader.DrawLevel()
    Main()
