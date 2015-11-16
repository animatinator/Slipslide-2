import pygame
print "Started!"
pygame.mixer.init()
print "Loading sound..."
music = pygame.mixer.Sound("Main theme.ogg")
print "Sound loaded."
music.play(-1)
print "Now playing test sound!"
print "Press return now to stop playback and exit."
raw_input()
music.stop()
