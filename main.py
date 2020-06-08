import sys #importation des modules
import os
import pygame
import time
import random
from pygame.locals import *

# pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()
# pygame.mixer.init()
pygame.font.init()

l,h= 1280,960

ecran = pygame.display.set_mode((l,h))

#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

jeu = True


# music_intro = pygame.mixer.Sound("data/music/intro")

def texte(text,size):
	f = pygame.font.Font(None,size)
	textFont = f.render(text,True,(255,255,255))
	return textFont

def intro():
	jeu = True

	leo = texte("Léo", 25)
	Lv = texte("Louis-Victor",25)
	presente = texte("Présente : ",25)

	t=0
	t1=10/3


	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False

		if t < t1:
			ecran.fill((0,0,0))
			ecran.blit(leo, (l/2,h/2)) 
		elif t<2*t1:
			ecran.fill((0,0,0))
			ecran.blit(Lv, (l/2,h/2)) 
		elif t<3*t1:
			ecran.fill((0,0,0))
			ecran.blit(presente, (l/2,h/2)) 
		else:
			jeu = False
		

		
		# ecran.blit(fond,(0,0))
		# ecran.blit(ballon, (x,y)) # perso
		time.sleep(0.002)
		
		pygame.display.flip()
		t+=0.02

	
	



x=400
y=1280/2
"""
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
"""

intro()
