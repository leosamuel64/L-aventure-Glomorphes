# Jeu IPT

Ce jeu a été réalisé dans le cadre de mini projet d'informatique en MPSI

Testé avec python 3.5.3

## Installation
``` Bash
>> sudo apt update
>> sudo apt upgrade
```
- Installation des dépendances :

```Bash 
>> sudo apt install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev
```
- Installation du gestionnaire de paquet Python :
```Bash
>> sudo apt install python3-pip  
```
- Installation de la bibliothèque :
```Bash
>> sudo pip3 install pygame
```
- Téléchargement du jeu :
```Bash
>> sudo git clone https://github.com/leosamuel64/MiniProjetIPT.git
```
## Utilisation

### Pour jouer : 
```Bash
>> cd MiniProjetIPT
>> ./Aventure_Glomorphes.py
```
### Commandes
- Le jeu va vous demandez d'appuyer sur les touches dans l'ordre pour :  
	- Avancer  
	- Reculer  
	- Aller à gauche 
	- Aller à droite  
	- Valider  

### Pour le jeu Flappymorphe

- Voler : ESPACE
- Recommencer : R


Ensuite, reglez la taille de la fenêtre du jeu avec les touches définies précédemment.  

Utilisez maintenant la souris et les touches sélectionnées pour jouer !

## Musique du jeu
 La musique du jeu est une réalisation personnelle : 
[Vers la musique ...](https://soundcloud.com/leo-samuel-331075331/sets/laventure-glomorphes)

## Erreur et Avertissement
- Erreur :
	- #1 : Un fichier audio n'a pas été trouvé. Vérifier qu'il est bien présent dans le dossier /data/music.
    - #3 : Un fichier image n'a pas été trouvé. Vérifier qu'il est bien présent dans le dossier /data/picture.

- Avertissement :
	- #2 : Aucune interface audio trouvé. Le jeu sera alors muet.  