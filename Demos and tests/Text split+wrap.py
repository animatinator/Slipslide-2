import pygame, sys

pygame.init()

class TextWrapper():
    def __init__(self, string):
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 50)
        self.string = string
        # Split the string into words
        self.words = self.string.split(" ")
        # Create lines from the words
        self.lines = []
        self.currentline = ""
        for word in self.words:
            currentlinelength = self.font.size(self.currentline+word)[0]
            if currentlinelength > self.screen.get_rect().width:
                self.lines.append(self.currentline)
                self.currentline = word+" "
            else:
                self.currentline = self.currentline+word+" "
        self.lines.append(self.currentline)
        # Make an array of the lines containing position and colour data
        array = []
        for i in range(0, len(self.lines)):
            array.append([self.lines[i], (0, int(i*(self.font.size("I")[1]))), (255,255,255)])
        # Draw the array of text objects to the screen
        for item in array:
            text = self.font.render(item[0], True, item[2])
            textrect = text.get_rect()
            textrect.y = item[1][1]
            self.screen.blit(text, textrect)
        pygame.display.update()


screen = pygame.display.set_mode((600, 480))
wrapper = TextWrapper("This is a very long string. So long, in fact, that it requires multiple lines. Yes, MULTIPLE LINES. And they were somewhat tricky to program.")#"Testing with a REALLY LONG STRING which will absolutely blow you away! It rocks! Yaaaaaay for David's superawesome text - wrapping! Where would we be without it? I'll tell you; we'd be splitting text into several different objects MANUALLY! Eek! Thank goodness David is a genius! Oh dear we're running out of space...")

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
