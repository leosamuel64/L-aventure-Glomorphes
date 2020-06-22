import os
import time
import random
import math
import pygame
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
	print("Avertissement #2 : Aucune interface audio trouvée  ")

pygame.display.set_caption("Glomorphe Adventure")


"""
------------------------------  PARAMETRES  ------------------------------
"""
	## Ligne pour bloquer les messages dans le terminal
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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

def HitBox(x,y,sizeX,sizeY):
	""" Créer une Hitbox rectangulaire de coin gauche supérieur x,y"""
	return 	[	(x-sizeX,y-sizeY),
				(x+sizeX,y+sizeY)
			]		

def dansBoite(box,x,y):
	"""
	Entrées	:	- box : Liste de tupple (représente les coordonées du coin haut gauche et bas droit d'un rectangle)
				- x : position x
				- y : possition y

	Sortie  : 	- Indique si le point (x,y) est dans le rectangle représentée par box
	"""
	if (x>box[0][0] and x < box[1][0]) and  (y>box[0][1] and y < box[1][1]):
		return True
	else:
		return False

def music(chemin):
	"""
	Lance le son chemin et ne plante pas si il n'y a pas de moyen de lire le son
	"""
	try:
		pygame.mixer.music.load(chemin)  
		pygame.mixer.music.play(-1)
	except pygame.error:
		v = os.path.exists(chemin)	## Vérifie si le fichier existe
		if not v:
			raise Exception("Erreur #1 : Le fichier audio n'a pas été trouvé -> {}".format(chemin))
		
def image(chemin,x,y):
	"""Creer une instance image de dimension x*y """
	try:
		img = pygame.image.load(chemin)
		img = pygame.transform.scale(img, (x, y))
		return img
	except pygame.error :
		v = os.path.exists(chemin)	## Vérifie si le fichier existe
		if not v:
			raise Exception("Erreur #3 : Le fichier image n'a pas été trouvé -> {}".format(chemin))

def sautY(y,t,tmax,incr):
	
	if t<tmax/2:
		y-=incr
		State=True
	elif t>tmax/2 and t<tmax: 
		y+=incr
		State=True
	else:
		State=False

	return y, State
	

"""
------------------------------  SCENES DU JEU  ------------------------------
"""

def select_taille_ecran(x,y):
	"""
	Ouvre un menu pour ajuster la taille de l'écran avec Z-S et Q-D
	"""
	incr = 100
	ecran = pygame.display.set_mode((x,y))
	t = texte("Haut/Bas et Droite/Gauche puis valider",int(x/14))
	jeu = True
	
	while jeu:		
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jeu = False

				if event.key == Tz:
					y+=incr
					ecran = pygame.display.set_mode((x,y))
				if event.key == Ts and (y-incr > 0):
					y-=incr
					ecran = pygame.display.set_mode((x,y))
				if event.key == Td:
					x+=incr
					ecran = pygame.display.set_mode((x,y))
				if event.key == Tq and  (y-incr > 0):
					x-=incr
					ecran = pygame.display.set_mode((x,y))
				if event.key == Tv :
					return x,y
			
		ecran.fill((0,0,0))
		ecran.blit(t, (0,0))
		time.sleep(0.002)
		pygame.display.flip()

def select_key():
	"""
	Renvoie le codes des touches selectionnée par l'utilisateur 
	"""
	z=texte("Touche pour aller en haut",20)
	s=texte("Touche pour aller en bas",20)
	q=texte("Touche pour aller à gauche",20)
	d=texte("Touche pour aller à droite",20)
	v=texte("Touche pour valider",20)
	listdetexte=[z,s,q,d,v]
	push=[]
	jeu = True
	num =0
	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				push.append(event.key)
				num+=1		
		ecran.fill((0,0,0))
		try:
			ecran.blit(listdetexte[num],(10,10))
		except IndexError:
			jeu=False

			return push[0],push[1],push[2],push[3],push[4]
				
		time.sleep(0.016)
		pygame.display.flip()

def transition(txt,suite):
	jeu=True
	lfont = []
	size = 30

	for i in txt:
		lfont.append(texte(i,size))

	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				if event.key == Tv:
					jeu=False
					suite()

		ecran.fill((0,0,0))
		for i in range (len(lfont)):
			ecran.blit(lfont[i], (10,size*(i+1)))
		time.sleep(0.002)
		pygame.display.flip()
			


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
			ecran.blit(leo, (l/2-100,h/2)) 
		elif t<2*t1:
			ecran.fill((0,0,0))
			ecran.blit(Lv, (l/2-100,h/2)) 
		elif t<3*t1:
			ecran.fill((0,0,0))
			ecran.blit(presente, (l/2-100,h/2)) 
		else:
			menu()
			jeu = False

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
	optiontxt = texte("Infos",80)
	Jouertxt = texte("Jouer",80)
	Quittertxt = texte("Quitter",80)
		## Textes quand la souris passe dessus
	optiontxtS = texte("Infos",100)
	JouertxtS = texte("Jouer",100)
	QuittertxtS = texte("Quitter",100) 
	Merci = texte("Merci d'avoir joué !",100)

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
				jeuEspace()
				jeu=False
		else:
			ecran.blit(Jouertxt, jouerBox[0])

		if dansBoite(optionBox,x,y):
			ecran.blit(optiontxtS, optionBox[0]) 
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				info()
				jeu = False
		else:		
			ecran.blit(optiontxt, optionBox[0]) 

		if dansBoite(QuitterBox,x,y):	
			ecran.blit(QuittertxtS, QuitterBox[0]) 
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				ecran.fill((0,0,0))
				ecran.blit(Merci, (l/2-200,h/2)) 
				pygame.display.flip()
				time.sleep(1)
				jeu = False
		else:
			ecran.blit(Quittertxt, QuitterBox[0]) 

		time.sleep(0.002)
		pygame.display.flip()


		

def info():
	"""
	Scene du menu info avec la version ...
	"""
	jeu = True
	flecheNorm = image("data/picture/Back_Arrow.png",100,100)
	flecheBig = image("data/picture/Back_Arrow.png",150,150)
	# flecheNorm = pygame.image.load("data/picture/Back_Arrow.png")
	# flecheNorm = pygame.transform.scale(flecheNorm, (100, 100))
	# flecheBig = pygame.image.load("data/picture/Back_Arrow.png")
	# flecheBig = pygame.transform.scale(flecheBig, (150, 150))

	Titre = texte("Titre",100)
	create = texte("Jeu Créé par Louis-Victor et Léo",50)
	version = texte("Version : 0.1",50)
	Annee = texte("MPSI - 2019/2020",50)

	flecheBox = [(50,50),(150,150)]

	while jeu:
			## On récupère la possition de la souris
		x,y = pygame.mouse.get_pos()
		ecran.fill((0,0,0))
			## Detection de la croix
		for event in pygame.event.get():
				if event.type == QUIT:
					jeu = False
		if dansBoite(flecheBox,x,y):
			ecran.blit(flecheBig, (flecheBox[0][0],flecheBox[0][1]))
			press = pygame.mouse.get_pressed()
			if press[0] == 1:
				menu()
				jeu=False
		else:
			ecran.blit(flecheNorm, (flecheBox[0][0],flecheBox[0][1]))

		ecran.blit(Titre, (l/2,50))
		ecran.blit(create, (l/2,200))
		ecran.blit(version, (l/2,300)) 
		ecran.blit(Annee, (l/2,400))

		time.sleep(0.002)
		pygame.display.flip()

def jeuEspace():
	"""
	Lance le jeu spatial 
	"""
	music("data/music/Purple.mp3")

	fusée = image("data/picture/fusee.png",100,100)
	fuséeflamme = image("data/picture/fuseeflamme.png",100,100)
	fond = image("data/picture/fondEspace.jpg",l,h)

	asteroide = image("data/picture/asteroide.png",100,100)
	asteroide2 = image("data/picture/asteroide.png",100,100)

	vitesse=0.3
	PointsVie = 10
	Distance = 30000
	
	x,y= l/2,h/2
	xast1,yast1 = 100,100
	xast2,yast2 = l-1,h-1
	
	momentumX=0
	momentumY=0
	momentumXast1,momentumYast1 = random.randint(1,3),random.randint(-3,3)
	momentumXast2,momentumYast2 = random.randint(-3,3),random.randint(1,3)

	invstate = False

	txtPV = texte("Etat du fuselage : "+str(PointsVie)+" /10",30)
	txtVitesse=texte("Vitesse de la fusée : "+str(abs(momentumX)+abs(momentumY))+" m/s",30)
	txtDistance = texte("Distance vers l'objectif : "+str(Distance)+" m",30)
	
	pygame.key.set_repeat(1,20)	
	jeu = True

	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jeu = False

				if event.key == Tz:
					momentumY-=vitesse
				if event.key == Ts:
					momentumY+=vitesse
				if event.key == Td:
					momentumX+=vitesse
				if event.key == Tq:
					momentumX-=vitesse
		
		# Test pour empecher la fusée de sortir de l'image
		if x>l or x<0:
			x=l/2
			momentumX=0
		if y>h or y<0:
			y=h/2
			momentumY=0

		# Calcul des coords pour la fusée et les astéroides
		x+= momentumX
		y+=momentumY
		xast1+= momentumXast1
		yast1+=momentumYast1
		xast2+= momentumXast2
		yast2+=momentumYast2
		
		# Replace les astéroides
		if xast1>l or yast1>h or xast1<0 or yast1<0:
			rand = random.random()
			if rand < 0.25:
				xast1,yast1 = int(l/2),1
				momentumXast,momentumYast = random.randint(-3,3),random.randint(1,3)
			elif rand < 0.50:
				xast1,yast1 = 1,int(h/2)
				momentumXast,momentumYast = random.randint(-3,3),random.randint(1,3)
			elif rand < 0.75:
				xast1,yast1 = int(l/2),h-1
				momentumXast,momentumYast = random.randint(-3,3),random.randint(-3,-1)
			else:
				xast1,yast1 = l-1,int(h/2)
				momentumXast,momentumYast = random.randint(-3,-1),random.randint(-3,-1)

		if xast2>l or yast2>h or xast2<0 or yast2<0:
			rand = random.random()
			if rand < 0.25:
				xast2,yast2 = int(l/2),1
				momentumXast2,momentumYast2 = random.randint(-3,3),random.randint(1,3)
			elif rand < 0.50:
				xast2,yast2 = 1,int(h/2)
				momentumXast2,momentumYast2 = random.randint(-3,3),random.randint(1,3)
			elif rand < 0.75:
				xast2,yast2 = int(l/2),h-1
				momentumXast2,momentumYast2 = random.randint(-3,3),random.randint(-3,-1)
			else:
				xast2,yast2 = l-1,int(h/2)
				momentumXast2,momentumYast2 = random.randint(-3,-1),random.randint(-3,-1)
		# On vérifie les collisions
		BoxAst1 = HitBox(xast1,yast1,50,50)
		BoxAst2 = HitBox(xast2,yast2,50,50)

		if (dansBoite(BoxAst1,x,y) or dansBoite(BoxAst2,x,y)) and (not invstate):
			PointsVie-=1
			invstate = True
		elif not (dansBoite(BoxAst1,x,y) or dansBoite(BoxAst2,x,y)):
			invstate = False
		if PointsVie==0:
			jeu=False

		# On update la distance avec la vitesse de la fusée
		Distance -= ((abs(momentumX)+abs(momentumY))*1000)*0.002
		if Distance < 10:
			# TODO : LANCER LA SUITE
			jeu = False

		# On update les textes
		txtPV = texte("Etat du fuselage : "+str(PointsVie),30)
		txtVitesse=texte("Vitesse de la fusée : "+str((int(abs(momentumX)+abs(momentumY)))*1000)+" m/s",30)
		txtDistance = texte("Distance vers l'objectif : "+str(int(Distance))+" m",30)

		# On verifie les touches enfoncées pour l'animation de la fusée

		pressed = pygame.key.get_pressed()

		if pressed[Tz] or pressed[Ts] or pressed[Tq] or pressed[Td]:
			feu = True
		else:
			feu = False

		# On affiche nos images 
		ecran.blit(fond,(0,0))
		ecran.blit(txtPV,(20,20))
		ecran.blit(txtVitesse,(20,40))
		ecran.blit(txtDistance,(20,60))
		ecran.blit(asteroide,(xast1,yast1))
		ecran.blit(asteroide2,(xast2,yast2))

		if feu:
			ecran.blit(fuséeflamme, (x,y))
		else:
			ecran.blit(fusée, (x,y)) 

		time.sleep(0.002)
		pygame.display.flip()

def plateforme():
	persoD = image("data/picture/persoD.png",30,30)
	persoG = image("data/picture/persoG.png",30,30)
	persoDJump = image("data/picture/persoDJump.png",30,30)
	persoGJump = image("data/picture/persoGJump.png",30,30)
	jeu = True
	JumpState = False
	tsaut = 0
	vitesse = 5
	incr = 0.002
	head="D"

	x,y = 10, h-50
	pygame.key.set_repeat(1,20)
	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jeu = False

				if event.key  == Tz and JumpState==False:
					JumpState = True
				if event.key == Ts:
					()
				if event.key == Td:
					x+=vitesse
					head = "D"
				if event.key == Tq:
					x-=vitesse
					head = "G"

		if JumpState:
			y, JumpState = sautY(y,tsaut,0.5,0.2)
			tsaut+=incr
		else:
			tsaut=0
		
		

		
		ecran.fill((0,0,0))

		if head == "D" and not JumpState:
			ecran.blit(persoD,(x,y))
		elif head == "G" and not JumpState:
			ecran.blit(persoG,(x,y))
		elif head == "G" and JumpState:
			ecran.blit(persoGJump,(x,y))
		elif head =="D" and JumpState:
			ecran.blit(persoDJump,(x,y))


		pygame.display.flip()




"""
------------------------------  LANCEMENT DU JEU ------------------------------
"""

ecran = pygame.display.set_mode((1080,500))
Tz,Ts,Tq,Td,Tv = select_key()
l , h = select_taille_ecran(1080,500)
ecran = pygame.display.set_mode((l,h))

## Appeller la fonction ici
# transition(["Le brave M. X à perdu ses 4 glomorphes !! Il doit les retrouver !", 
# 			"Qui les a donc volée ?! Il trouve un indice, une base de données SQL. ",
# 			"Après maintes requêtes et sous requêtes, toutes les pistes mène vers une planète,", 
# 			"au fin fond de l'espace “euclidien” !",
# 			" ",
# 			"       Appuyez sur la touche valider pour continuer ..."],print)


plateforme()




