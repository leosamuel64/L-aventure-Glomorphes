# Jeu IPT

Ce jeu a été réalisé dans le cadre de mini projet d'informatique en MPSI

Testé avec python 3.5.3

## Installation
``` Bash
>> sudo apt-get update
>> sudo apt-get upgrade
```
- Installation des dépendances :

```Bash 
>> sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev
```
- Installation du gestionnaire de paquet Python :
```Bash
>> sudo apt-get install python3-pip  
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

Pour jouer : 
```Bash
>> cd MiniProjetIPT
>> python3 main.py
```

## Erreur et Avertissement
- Erreur :
	- #1 : Un fichier audio n'a pas été trouvé. Vérifier qu'il est bien présent dans le dossier /data/music.
    - #3 : Un fichier image n'a pas été trouvé. Vérifier qu'il est bien présent dans le dossier /data/picture.

- Avertissement :
	- #2 : Aucune interface audio trouvé. Le jeu sera alors muet.  