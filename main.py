import sys #importation des modules
import os
import pygame
import time
import random
from pygame.locals import *

"""
------------------------------  INITIALISATION DE PYGAME  ------------------------------
"""
pygame.init()
pygame.font.init()


"""
------------------------------  INITIALISATION DU MODULE SONORE  ------------------------------
"""
try:
	pygame.mixer.pre_init(44100,-16,2,2048)
	pygame.mixer.init()
except pygame.error:
	()


"""
------------------------------  PARAMETRES  ------------------------------
"""
	## On récupère la taille de l'ecran
l,h = pygame.display.Info().current_w,pygame.display.Info().current_h  
	## On créer la fenêtre du jeu
ecran = pygame.display.set_mode((l,h- 100))

	## Ligne pour bloquer les messages dans le terminal
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

"""
------------------------------  FONCTIONS INTERMEDIAIRES  ------------------------------	
"""

def texte(text,size):
	"""
	Entrées :	- text : Texte à afficher
				- size : Taille du texte

	Sortie  :	- Le texte prêt à afficher  	
	"""
	f = pygame.font.Font(None,size)
	textFont = f.render(text,True,(255,255,255))
	return textFont

def dansBoite(box,x,y):
	"""
	Entrées	:	- box : Liste de tupple (représente les coordonées du coin haut gauche et bas droit d'un rectangle)
				- x : position x
				- y : possition y

	Sortie  : 	- Indique si le point (x,y) est dans le rectangle représentée par box
	"""
	if x>box[0][0] and x < box[1][0] and  y>box[0][1] and y < box[1][1]:
		return True
	else:
		return False

def music(chemin):
	"""
	Lance le son chemin et ne plante pas si il n'y a pas de carte son
	"""
	try:
		pygame.mixer.music.load(chemin)  
		pygame.mixer.music.play(-1)
	except pygame.error:
		()


"""
------------------------------  SCENES DU JEU  ------------------------------
"""

def intro():
	"""
	Affiche le générique d'introduction
	"""
	jeu = True
	music("data/music/intro.mp3")
		## Taille de la police
	size = 80
		## Génération des textes
	leo = texte("Léo ...", size)
	Lv = texte("... et Louis-Victor",size)
	presente = texte("Présentent ",size)
		## Variable temporelle
	t=0	
		## Temps par texte
	t1=1/3
		# Boucle de l'affichage
	while jeu:
			## Detection de la croix
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
		
def menu():
	"""
	Affiche le menu
	"""
	music("data/music/menu.mp3")
	jeu = True
		## Textes au repos
	optiontxt = texte("Options",80)
	Jouertxt = texte("Jouer",80)
	Quittertxt = texte("Quitter",80)
		## Textes quand la souris passe dessus
	optiontxtS = texte("Options",100)
	JouertxtS = texte("Jouer",100)
	QuittertxtS = texte("Quitter",100) 

		## Rectangles autour des textes
	jouerBox = [(l/2,(h/2)-100),((l/2+200,(h/2)))]
	optionBox = [(l/2,(h/2)),((l/2+200,(h/2)+100))]
	QuitterBox = [(l/2,(h/2)+100),((l/2+230,(h/2)+200))]

	while jeu:
			## On récupère la possition de la souris
		x,y = pygame.mouse.get_pos()

			## Detection de la croix
		for event in pygame.event.get():
				if event.type == QUIT:
					jeu = False
		
		ecran.fill((0,0,0))
		if dansBoite(jouerBox,x,y):
			ecran.blit(JouertxtS, jouerBox[0]) 
				## Récupère l'état des boutons sous la forme d'un tupple 0/1 (Gauche,molette,Droite)
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

