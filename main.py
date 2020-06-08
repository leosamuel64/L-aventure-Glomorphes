import sys #importation des modules
import os
import pygame
import time
import random
from pygame.locals import *

pygame.init()
# pygame.mixer.pre_init(44100,-16,2,2048)
# pygame.mixer.init()
pygame.font.init()

l,h = pygame.display.Info().current_w,pygame.display.Info().current_h



ecran = pygame.display.set_mode((l,h- 100))

#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

jeu = True


def texte(text,size):
	f = pygame.font.Font(None,size)
	textFont = f.render(text,True,(255,255,255))
	return textFont

def intro():
	jeu = True
	# pygame.mixer.music.load("data/music/intro.mp3")
	# pygame.mixer.music.play(-1)
	size = 80
	leo = texte("Léo ...", size)
	Lv = texte("... et Louis-Victor",size)
	presente = texte("Présentent ",size)
	t=0
	t1=1/3
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
			menu()

		time.sleep(0.002)
		
		pygame.display.flip()
		t+=0.002

def dansBoite(box,x,y):
	if x>box[0][0] and x < box[1][0] and  y>box[0][1] and y < box[1][1]:
		return True
	else:
		return False
		


def menu():
	jeu = True

	optiontxt = texte("Options",80)
	Jouertxt = texte("Jouer",80)
	Quittertxt = texte("Quitter",80)

	optiontxtS = texte("Options",100)
	JouertxtS = texte("Jouer",100)
	QuittertxtS = texte("Quitter",100) 

	jouerBox = [(l/2,(h/2)-100),((l/2+200,(h/2)))]
	optionBox = [(l/2,(h/2)),((l/2+200,(h/2)+100))]
	QuitterBox = [(l/2,(h/2)+100),((l/2+230,(h/2)+200))]

	while jeu:

		x,y = pygame.mouse.get_pos()
		
		for event in pygame.event.get():
				if event.type == QUIT:
					jeu = False
		
		ecran.fill((0,0,0))
		if dansBoite(jouerBox,x,y):
			ecran.blit(JouertxtS, jouerBox[0]) 
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				print("Jouer")
		else:
			ecran.blit(Jouertxt, jouerBox[0])


		if dansBoite(optionBox,x,y):
			ecran.blit(optiontxtS, optionBox[0]) 
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				print("Options")
		else:		
			ecran.blit(optiontxt, optionBox[0]) 


		if dansBoite(QuitterBox,x,y):	
			ecran.blit(QuittertxtS, QuitterBox[0]) 
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				print("Quitter")
		else:
			ecran.blit(Quittertxt, QuitterBox[0]) 

		
		time.sleep(0.002)
		pygame.display.flip()

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

# intro()
menu()

