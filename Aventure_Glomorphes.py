#! /usr/bin/python3

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

pygame.display.set_caption("L'aventure Glomorphes")


"""
------------------------------  PARAMETRES  ------------------------------
"""
	## Ligne pour bloquer les messages dans le terminal
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# On initialise la matrice pour le jeu de plateforme
tableau = [	[0,0,0,0,0,0,0,0,0,0],
			[3,0,0,0,0,0,0,0,0,0],
			[1,1,0,0,0,0,0,0,0,0],
			[1,0,1,0,1,0,1,0,1,2],
			[0,0,0,0,0,0,0,0,0,2],
			[0,0,0,0,0,0,0,0,0,2],
			[0,0,0,0,0,0,0,0,1,1],
			[0,0,0,0,0,1,1,1,0,0],
			[0,0,0,1,1,0,0,0,0,1],
			[1,1,0,1,1,1,1,1,1,0]
]

# On initialise la matrice pour les lynx
lynx = [	[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0,0,0,0,0,0],
]

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
	"""
	Creer une instance image de dimension x*y 
	"""
	try:
		img = pygame.image.load(chemin)
		img = pygame.transform.scale(img, (x, y))
		return img
	except pygame.error :
		v = os.path.exists(chemin)	## Vérifie si le fichier existe
		if not v:
			raise Exception("Erreur #3 : Le fichier image n'a pas été trouvé -> {}".format(chemin))

def sautY(y,t,tmax,incr):
	"""
	Fonction qui gère le saut du personnage
	"""
	if t<tmax/2:
		y-=incr
		State=True
	else:
		State=False

	return y, State
	
def MatrixToMap(Mat,calc):
	"""
	Decoupe l'écran et affiche 	de la roche si Mat[i][j]=1
								des echelles si Mat[i][j]=2
								un portail si Mat[i][j]=3
	Créer aussi les Hitbox associées
	"""
	xUnit = l/len(Mat)
	yUnit = h/len(Mat[0])
	supportHit = []
	for i in range (len(Mat)):
		for j in range (len(Mat[0])):
			if Mat[i][j]==1:
				if calc:
					supportHit.append([(j*xUnit,i*yUnit),((j+1)*xUnit,(i+1)*yUnit)])
				ecran.blit(image("data/picture/roche.png",int(xUnit),int(yUnit)),(j*xUnit,i*yUnit))
			elif Mat[i][j]==2:
				if calc:
					supportHit.append([(j*xUnit,i*yUnit),((j+1)*xUnit,(i+1)*yUnit)])
				ecran.blit(image("data/picture/echelle.png",int(xUnit),int(yUnit)),(j*xUnit,i*yUnit))
			elif Mat[i][j]==3:
				if calc:
					supportHit.append([(j*xUnit,i*yUnit),((j+1)*xUnit,(i+1)*yUnit)])
				ecran.blit(image("data/picture/portail.png",int(xUnit),int(yUnit)),(j*xUnit,i*yUnit))
	return supportHit



def MatrixToLynx(Mat,calc):
	"""
	Decoupe l'écran et affiche des lynx si Mat[i][j]=1.
	Créer aussi les Hitbox associées
	"""
	xUnit = l/len(Mat)
	yUnit = h/len(Mat[0])
	supportHit = []
	for i in range (len(Mat)):
		for j in range (len(Mat[0])):
			if Mat[i][j]==1:
				if calc:
					supportHit.append([(j*xUnit,i*yUnit),((j+1)*xUnit,(i+1)*yUnit)])
				ecran.blit(image("data/picture/lynx.png",int(xUnit),int(yUnit)),(j*xUnit,i*yUnit))
			
	return supportHit

def vide():
	"""
	Ne fait rien
	"""
	()

"""
------------------------------  SCENES DU JEU  ------------------------------
"""

def select_taille_ecran(x,y):
	"""
	Ouvre un menu pour ajuster la taille de l'écran avec Z-S et Q-D
	"""
	incr = 100
	ecran = pygame.display.set_mode((x,y))
	
	# On initialise le texte  
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
		
		# Afffichage
		ecran.fill((0,0,0))
		ecran.blit(t, (0,0))
		time.sleep(0.002)
		pygame.display.flip()

def select_key():
	"""
	Renvoie le codes des touches selectionnée par l'utilisateur 
	"""
	# On initialise les textes
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
	"""
	Affiche un texte, attend que l'utilisateur valide et passe à la suite

	txt : Liste des textes (chaque element du tableau correspond à une ligne)
	suite : Procédure qui ne prend pas d'argument
	"""
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
				## Appeller la suite ici
				music("data/music/GoinOn.mp3")
				transition(["Le brave M. X à perdu ses 4 glomorphes !! Il doit les retrouver !", 
							"Qui les a donc volée ?! Il trouve un indice, une base de données SQL. ",
							"Après maintes requêtes et sous requêtes, toutes les pistes mène vers une planète,", 
							"au fin fond de l'espace “euclidien” !",
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],jeuEspace)
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

	# On charge les images
	flecheNorm = image("data/picture/Back_Arrow.png",100,100)
	flecheBig = image("data/picture/Back_Arrow.png",150,150)

	# On charge les textes
	Titre = texte("L'aventure Glomorphes",100)
	create = texte("Jeu Créé par Louis-Victor et Léo",50)
	version = texte("Version : 0.1",50)
	Annee = texte("MPSI - 2019/2020",50)

	# Hitbox de la flèche de retour
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
	# On charge les images
	fusée = image("data/picture/fusee.png",100,100)
	fuséeflamme = image("data/picture/fuseeflamme.png",100,100)
	fond = image("data/picture/fondEspace.jpg",l,h)

	asteroide = image("data/picture/asteroide.png",100,100)
	asteroide2 = image("data/picture/asteroide.png",100,100)

	# On définie les paramètres
	vitesse=0.3
	PointsVie = 10
	Distance = 30000
	
	x,y= l/2,h/2
	xast1,yast1 = 100,100
	xast2,yast2 = l-1,h-1
	
	# Variables pour simuler l'inertie des objets
	momentumX=0
	momentumY=0
	momentumXast1,momentumYast1 = random.randint(1,3),random.randint(-3,3)
	momentumXast2,momentumYast2 = random.randint(-3,3),random.randint(1,3)

	# Variable qui définie si le joueur est touchable ou non 
	invstate = False

	# On charge les textes
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
		
		# Replace les astéroides si besoin
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

		# On gère les points de vie
		if (dansBoite(BoxAst1,x,y) or dansBoite(BoxAst2,x,y)) and (not invstate):
			PointsVie-=1
			invstate = True
		elif not (dansBoite(BoxAst1,x,y) or dansBoite(BoxAst2,x,y)):
			invstate = False
		if PointsVie==0:
			jeu=False
			jeuEspace()

		# On update la distance avec la vitesse de la fusée
		Distance -= ((abs(momentumX)+abs(momentumY))*1000)*0.002
		if Distance < 10:
			# On lance la Suite
			transition(["Victoire ! je viens de retrouver Arthur, le glomorphe à rayure !", 
							"Il me prévient que ses camarades sont retenus  par une entité barbare",
							"Je me met alors en route vers cette horreur sans nom !", 
							"Il se pose sur la planète et se retrouve face à une falaise qu’il doit escalader",
							"pour continuer son aventure ! Mais où peut bien mener ce portail ?",
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],plateforme)
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

## -------- AFFICHAGE --------

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
	"""
	Lance le jeu de Plateforme
	"""
	# Dimension du personnage
	persodimX =  int(l/10)
	persodimY =	 int(h/10)

	# Chargement des images
	persoD = image("data/picture/persoD.png",persodimX,persodimY)
	persoG = image("data/picture/persoG.png",persodimX,persodimY)
	persoDJump = image("data/picture/persoDJump.png",persodimX,persodimY)
	persoGJump = image("data/picture/persoGJump.png",persodimX,persodimY)

	# Variable de jeu
	jeu = True

	# Indique si le personnage est en train de sauter
	JumpState = False

	#Indique l'avancement du saut
	tsaut = 0
	
	#Vitesse de marche
	vitesse = 5

	#Vitesse de saut
	incr = 0.002

	# Direction de la vision ("G"/"D")
	head="D"

	# Indique si le pesronnage est sur/dans un support
	supportbool = False

	# On définit la position initiale du personnage
	x,y = 5, 8*(h/10)+5

	# On calcul les hitbox des supports
	Support = MatrixToMap(tableau,True)

	# Gestion de la répétition des touches
	pygame.key.set_repeat(1,20)

	## Boucle du jeu
	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jeu = False

				# Detection du saut
				if event.key  == Tz and JumpState==False and supportbool==True:
					JumpState = True

		# Detection de la marche
		pressed = pygame.key.get_pressed()
		if pressed[Td] and x < l-1-persodimX:
			x+=vitesse
			head = "D"
		if pressed[Tq] and x >5:
			x-=vitesse
			head = "G"

		# Gestion du saut
		if JumpState:
			y, JumpState = sautY(y,tsaut,0.1,(h*0.4)*8/500)
			tsaut+=incr
		else:
			tsaut=0

		# On calcul si le joueur est sur un support (## TODO : rprogrammer avec une while)
		supportbool = False
		for i in range (len(Support)):
			if head == "D":
				if dansBoite(Support[i],x+(2*x/21),y+persodimY):
					supportbool = True
			elif head == "G":
				if dansBoite(Support[i],x+(2*x/21)+persodimX-(3*x/21),y+persodimY):
					supportbool = True

		# On gère la chute si le personnage n'est pas sur un support
		if not supportbool and not JumpState:
			y+=(h*0.4)*5/500

		# On gère la fin du jeu si on touche le portail
		if dansBoite(Support[0],x+(2*x/21)+persodimX/2,y):
			transition(["Vous trouvez Maurice le glomorphe à pois ! Mais votre agresseur", 
							" a plus d’un tour dans son sac ! Il a fuit avec son dirigeable en plomb  ",
							" Heureusement, qu’il en reste un ! Vous le prenez et le pourchassez !", 
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],flappymorphe)
			jeu=False

		# On gère le respawn du personnage si il tombe dans un trou
		if y> h:
			jeu=False
			plateforme()

## -------- AFFICHAGE --------

		ecran.fill((0,0,0))

		# On affiche les supports
		MatrixToMap(tableau,False)

		# On gère l'animation du personnage
		if head == "D" and not JumpState:
			ecran.blit(persoD,(x,y))
		elif head == "G" and not JumpState:
			ecran.blit(persoG,(x,y))
		elif head == "G" and JumpState:
			ecran.blit(persoGJump,(x,y))
		elif head =="D" and JumpState:
			ecran.blit(persoDJump,(x,y))

		time.sleep(0.002)
		pygame.display.flip()

def flappymorphe():
	"""
	Lance le jeu FlappyMorphe 
	"""
	fond = image("data/picture/fondFlappy.png",l,h)
	oiseau = image("data/picture/flappybird.png",60, 60)
	poteau1 = image("data/picture/Tuyeau.png", 70, 500)
	poteau2 = image("data/picture/Tuyeau_2.png", 70, 500)

	pygame.display.set_caption("Flappy Bird")  # Nom de la fenêtre

	Score = 0
	txtScore = texte("Score : " + str(Score), 30)
	jumpCount = 10 # Pour augmenter la vitesse de chute

	jeu = False

	txtrecommencer = texte("Appuyer sur R pour recommencer", 30)
	txtfin = texte("Félicitations !", 60)
	det = True
	
	ecran.blit(fond, (0, 0))
	ecran.blit(txtrecommencer, (400, 20))
	pygame.display.flip()

	while det:
		for event in pygame.event.get([KEYDOWN, QUIT]):
			if event.type == QUIT:  # Si l'évènement est de type quitter alors on arrête le programme
				menu()
				jeu=False
			elif event.key == K_r:  # Si l'évènement est l'appui sur la touche "r" on joue au jeu
				jeu = True
				det = False

	x_poteau = 1000  # Position du poteau
	y_poteau = 450

	x_poteau2 = x_poteau
	y_poteau2 = y_poteau - 600  # Position du poteau2 (à l'envers)

	x = 100  # Position de l'oiseau
	y = 100

	passed = False #Est que l'oiseau a dépassé le poteau
	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False

		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE]:
			jumpCount = 11
			y -= (jumpCount * abs(jumpCount)) * 0.05
			jumpCount -= 1
		elif jumpCount > -20:
			y -= (jumpCount * abs(jumpCount)) * 0.03
			jumpCount -= 1
		else:
			y -= (jumpCount * abs(jumpCount)) * 0.03

		if x_poteau <=-70:
			x_poteau = 1000
			x_poteau2 = 1000
			y_poteau = random.randint(210,450)
			y_poteau2 = y_poteau - 600
			passed = False
		else:
			x_poteau -= 4
			x_poteau2 -= 4

		if x>x_poteau and not passed:
			Score += 1
			passed = True

		BoxPoteau1 = HitBox(x_poteau, y_poteau, 50,35)
		BoxPoteau1_plus = HitBox(x_poteau+50, y_poteau+35, 50, 300)
		BoxPoteau2 = HitBox(x_poteau2, y_poteau2, 50,460)

		if (dansBoite(BoxPoteau1,x,y) or dansBoite(BoxPoteau2,x,y)):
			jeu=False

		txtScore = texte("Score : " + str(Score), 30) #Mis à jour du texte

		ecran.blit(fond, (0, 0))
		ecran.blit(oiseau, (x, y))
		ecran.blit(poteau1, (x_poteau, y_poteau))
		ecran.blit(poteau2, (x_poteau2, y_poteau2))
		ecran.blit(txtScore, (20,20))
		ecran.blit(txtrecommencer, (400, 20))

		if y > 450:
			jeu = False

		if Score == 5:
			ecran.blit(txtfin, (400, 400))
			time.sleep(2)
			transition(["Je suis trop rapide pour lui ! il a eu besoin de se délesté. ", 
							"Vous trouvez “Syracuse” le glomorphe aillé (connu pour son temps de vol  !).",
							"Mais je n’ai pas dit mon dernier mot ! Il est ralentit mais ses sbires, ", 
							"les lynx à collier de Mélanésie me barrent la route !",
							"Je dois m’en occuper !!",
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],jeuTir)
			jeu=False

		time.sleep(0.002)
		pygame.display.flip()
		if not jeu and Score < 5:
			flappymorphe()

def jeuTir():
	"""
	Lance le jeu de tir
	"""

	jeu = True

	# Dimension du viseur (qui suivra la souris)
	viseurdimX = int(l/20)
	viseurdimY = int(h/20)

	# On charge les images
	viseur = image("data/picture/viseur.png",viseurdimX,viseurdimY)
	fond = image("data/picture/Melanesiefond.png",l,h)
	
	# Variable qui correspond au nombre d'ennemies à éliminer
	reste = 30

	# On charge le texte
	resteTexte = texte("Il y a encore "+str(reste)+" lynx",30)

	# Variable qui indique si une cible est présente sur l'écran
	lynxState = False

	# Variable qui définie le temps que la cible reste à sa position
	tmax = random.random()*(2*h)/10*1080

	# Calcul la disposition des cibles
	cibleHit = MatrixToLynx(lynx,True)

	while jeu:
		for event in pygame.event.get():
			if event.type == QUIT:
				jeu = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					jeu = False

		# On affiche une cible si il n'y en a pas
		if not lynxState:
			randx = random.randint(1,len(lynx[0])-1)
			randy = random.randint(1,len(lynx)-1)
			lynx[randx][randy] = 1
			tmax = random.random()*5
			lynxState = True

		# On recupère la position de la souris
		x,y = pygame.mouse.get_pos()
		
		# On verifie si le viseur/la souris est dans une hitbox et enleve la cible si le joueur clique
		# On met une boucle for pour pouvoir gèrer plusieurs cibles dans le futur
		for i in range (len(cibleHit)):
			if dansBoite(cibleHit[i], x-viseurdimX/2, y-viseurdimY/2):
				press = pygame.mouse.get_pressed()
				if press[0] == 1:
					lynxState = False
					lynx[randx][randy] = 0
					reste-=1
					ecran.fill((255,0,0))
					time.sleep(0.1)
					pygame.display.flip()
			
		# On gère la fin 
		if reste == 0:
			transition(["Il est dos au mur, je peux enfin le discerner mais … horreur ! ", 
							" C’est le plus mauvais des systèmes d’exploitation !  ",
							" Windows !!! ", 
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],fin)
			jeu=False

		# On retire du temps d'affichage de la cible à l'écran
		tmax-= 0.02

		# Si le temps est négatif alors on enlève la cible
		if tmax < 0:
			lynxState=False
			lynx[randx][randy] = 0

		# On charge le nouveau texte
		resteTexte = texte("Il y a encore "+str(reste)+" lynx",30)
## -------- AFFICHAGE --------

		ecran.blit(fond,(0,0))
		ecran.blit(resteTexte,(20,20))
		cibleHit = MatrixToLynx(lynx,True)
		ecran.blit(viseur,(x-viseurdimX/2,y-viseurdimY/2))
		time.sleep(0.002)
		pygame.display.flip()

def fin():
	"""
	Lance la fin
	"""
	transition(["Il est dos au mur, je peux enfin le discerner mais … horreur ! ", 
							" C’est le plus mauvais des systèmes d’exploitation !  ",
							" Windows !!! ", 
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],vide)

	# On charge les images
	windows = image("data/picture/windows.png",int(2*l/10),int(2*h/10))
	fond= image("data/picture/donjon.png",l,h)

	# Affichage
	ecran.blit(fond,(0,0))
	ecran.blit(windows,(int((l/2)-int(2*l/10)/2),int(h/3)))	
	pygame.display.flip()
	time.sleep(3)

	transition(["Mais il ne se laissera pas faire et est trop fort !!! ", 
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],vide)
	
	# On charge l'image
	explo = image("data/picture/explosion.png",int(3*l/10),int(3*h/10))

	# Affichage
	ecran.blit(fond,(0,0))
	ecran.blit(windows,(int((l/2)-int(2*l/10)/2),int(h/3)))	
	pygame.display.flip()

	for i in range(0,8):
		# On charge le nouveau texte
		tpdv = texte("Vos points de vie : "+str(10-i),30)

		# Affichage
		ecran.blit(fond,(0,0))
		ecran.blit(windows,(int((l/2)-int(2*l/10)/2),int(h/3)))	
		ecran.blit(explo,(random.randint(0,l),random.randint(0,h)))
		ecran.blit(tpdv,(30,30))
		pygame.display.flip()
		time.sleep(1)

	transition(["Je ne pourrai pas le vaincre seul !! ", 
							" Il me faut de l'aide !  ",
							" Mais qui est assez fort ?! ", 
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],vide)
	tux = image("data/picture/TuxVide.png",int(4*l/10),int(4*h/10))
	
	for x in range (0,l//6):
		# Affichage
		ecran.blit(fond,(0,0))
		ecran.blit(windows,(int((l/2)-int(2*l/10)/2),int(h/3)))	
		ecran.blit(tux,(x,h/2))
		pygame.display.flip()
	
	# On charge l'image
	tux = image("data/picture/tux1.png",int(4*l/10),int(4*h/10))

	# Affichage
	ecran.blit(fond,(0,0))
	ecran.blit(windows,(int((l/2)-int(2*l/10)/2),int(h/3)))	
	ecran.blit(tux,(l//6,h/2))
	pygame.display.flip()
	time.sleep(3)
	
	# On charge l'image
	tux = image("data/picture/tux2.png",int(4*l/10),int(4*h/10))

	# Affichage
	ecran.blit(fond,(0,0))
	ecran.blit(windows,(int((l/2)-int(2*l/10)/2),int(h/3)))	
	ecran.blit(tux,(l//6,h/2))
	pygame.display.flip()
	time.sleep(3)
	
	# On charge l'image
	fond= image("data/picture/blue.jpg",l,h)
	
	jeu=True

	# On lance la musique de fin
	music("data/music/Purple.mp3")

	# Boucle pour attendre que le joueur valide
	while jeu:
		for event in pygame.event.get():
				if event.type == QUIT:
					jeu = False
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						jeu = False
					if event.key == Tv:
						jeu=False

		# Affichage
		ecran.blit(fond,(0,0))
		pygame.display.flip()
		time.sleep(0.002)

	# Fin du jeu et retour au menu !
	time.sleep(0.5)
	transition(["Félicitation ! ", 
							"Vous avez gagné !!! ",
							"Vous retrouvez enfin votre dernier glomorphe ! ", 
							"Le brave complexomorphe en O(n) !!! ",
							" ",
							"       Appuyez sur la touche valider pour continuer ..."],menu)
	
"""
------------------------------  LANCEMENT DU JEU ------------------------------
"""

ecran = pygame.display.set_mode((1080,500))
Tz,Ts,Tq,Td,Tv = select_key()
l , h = select_taille_ecran(1080,500)
ecran = pygame.display.set_mode((l,h))
music("data/music/menu.mp3")

intro()