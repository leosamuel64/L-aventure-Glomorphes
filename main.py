import sys #importation des modules
import os
import pygame
import time
import random
from pygame.locals import *

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
pygame.mixer.init()
pygame.font.init()


ecran = pygame.display.set_mode((1280,960))

#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

jeu = True




ptsvent = 10
x=400
y=1280/2

while jeu:
	for event in pygame.event.get():
		if event.type == QUIT:
			jeu = False
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				jeu = False
			if event.key == K_z:
				print("Z")
			if event.key == K_s:
				print("S")
			if event.key == K_d:
				print("D")
			if event.key == K_q:
				print("Q")

	# ecran.blit(fond,(0,0))
	# ecran.blit(ballon, (x,y)) # perso
	time.sleep(0.002)
	pygame.display.flip()
