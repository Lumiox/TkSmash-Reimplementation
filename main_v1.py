#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Version 1 :
        - Déplacement d'un personnage horizontalement et vers le haut (saut)
        - Chargement de plusieurs sprites pour un même mouvement (fluidité)
        - Évolution du personnage dans un environnement spécifique, avec des bordures bien définies (collisions aux bords)
"""
""" Version 2 :
        - [EN COURS] Affichage des coups (animation)
        - [EN ATTENTE] Gestion des points de vie (perte)
        - [EN ATTENTE] Affichage des points de vie (barre de vie)
"""

from tkinter import *

def clavier(evenement):
    """Gère les événements clavier correspondant à l'appui sur une touche"""
    touche = evenement.keysym.upper()
    if touche == "Q":
        if deplacement_possible(GAUCHE):
            deplacer(GAUCHE)
        else:
            avancer_au_maximum(GAUCHE)
    elif touche == "D":
        if deplacement_possible(DROITE):
            deplacer(DROITE)
        else:
            avancer_au_maximum(DROITE)
    elif touche == "Z":
        if deplacement_possible(HAUT):
            deplacer(HAUT)
    elif touche == "SPACE":
        frappe()

def clavier_relachement(evenement):
    """Gère les événements clavier correspondant au relâchement d'une touche"""
    global joueur1
    global sprite_a_charger, imagesGauche, imagesDroite
    if evenement.keysym.upper() != "SPACE":     # Si le personnage n'est pas en train d'attaquer
        if not en_l_air:    # Si le personnage n'est pas en l'air mais bien sur terre
            if sprite_a_charger in imagesGauche:
                sprite_a_charger = imagesGauche[0]
            else:
                sprite_a_charger = imagesDroite[0]
            # Lorsque le personnage est à l'arrêt, ne pas laisser le dernier sprite chargé (= en pleine marche),
            # mais le remplacer par le premier sprite de la direction dans laquelle se déplace le personnage
            canvas.itemconfigure(joueur1, image=sprite_a_charger)

def deplacer(direction):
    """Déplace le personnage en fonction de la direction choisie"""
    global joueur1
    global sprite_a_charger, imagesGauche, imagesDroite
    if direction == GAUCHE or direction == DROITE:
        if direction == GAUCHE:
            # Chargement du bon sprite
            if sprite_a_charger in imagesGauche:    # Si le déplacement se faisait vers la gauche
                indice_sprite = imagesGauche.index(sprite_a_charger)
                sprite_a_charger = imagesGauche[indice_sprite+1] if indice_sprite+1 < len(imagesGauche) else imagesGauche[0]
            else:
                sprite_a_charger = imagesGauche[0]
            canvas.itemconfigure(joueur1, image=sprite_a_charger)
            # Déplacement du personnage
            val_dep = -DEP_H
            canvas.move(joueur1, val_dep, 0)
        else:
            # Chargement du bon sprite
            if sprite_a_charger in imagesDroite:    # Si le déplacement se faisait vers la droite
                indice_sprite = imagesDroite.index(sprite_a_charger)
                sprite_a_charger = imagesDroite[indice_sprite+1] if indice_sprite+1 < len(imagesDroite) else imagesDroite[0]
            else:
                sprite_a_charger = imagesDroite[0]
            canvas.itemconfigure(joueur1, image=sprite_a_charger)
            # Déplacement du personnage
            val_dep = DEP_H
            canvas.move(joueur1, val_dep, 0)
    elif direction == HAUT:
        sauter()
    

def avancer_au_maximum(direction):
    global DIM_FEN
    global joueur1
    pos = [int(coord) for coord in canvas.coords(joueur1)]  # Coordonnées du perso
    if direction == GAUCHE:
        val_dep = -pos[0]    # La valeur de déplacement correspond à l'opposé de l'abscisse du perso (distance entre l'extrêmité gauche et le perso = son abscisse)
        canvas.move(joueur1, val_dep, 0)
    elif direction == DROITE:
        val_dep = DIM_FEN[0] - (pos[0] + DIM_PERSO[0])  # La valeur de déplacement est la distance (1080 - abscisse du perso)
        canvas.move(joueur1, val_dep, 0)

def sauter():
    global joueur1
    global en_l_air
    global sprite_a_charger, imagesGauche, imagesDroite, imagesSautGauche, imagesSautDroite
    # Si le personnage n'est pas en l'air
    if not en_l_air:
        # Détermination de la direction avant le saut
        direction_precedente = GAUCHE if (sprite_a_charger in imagesGauche) else DROITE
        # Déplacement du personnage
        canvas.move(joueur1, 0, -DEP_V)
        en_l_air = True
        # Chargement du sprite de saut
        sprite_a_charger = imagesSautGauche[1] if direction_precedente == GAUCHE else imagesSautDroite[1]
        canvas.itemconfigure(joueur1, image=sprite_a_charger)
        
    fenetre.after(200, redescendre) # Appel de la fonction "redescendre" au bout de 200ms

def redescendre():
    global joueur1
    global en_l_air
    global sprite_a_charger, imagesGauche, imagesDroite, imagesSautGauche, imagesSautDroite
    # Si le personnage est en l'air
    if en_l_air:
        # Déplacement du personnage
        canvas.move(joueur1, 0, DEP_V)
        en_l_air = False
        # Détermination de la direction avant le saut
        direction_precedente = GAUCHE if (sprite_a_charger in imagesSautGauche) else DROITE    # Attention : le sprite précédent était un sprite de saut -> imagesSaut(Gauche ou Droite)
        # Chargement du bon sprite
        sprite_a_charger = imagesGauche[0] if direction_precedente == GAUCHE else imagesDroite[0]
        canvas.itemconfigure(joueur1, image=sprite_a_charger)

def deplacement_possible(direction):
    """Vérifie que le mouvement dans la direction choisie est possible"""
    global joueur1
    pos = [int(coord) for coord in canvas.coords(joueur1)]
    if (direction == GAUCHE and pos[0] - DEP_H < 0) \
    or (direction == DROITE and pos[0] + DIM_PERSO[0] + DEP_H > DIM_JOUABLE[0]) \
    or (direction == HAUT and pos[1] - DEP_V < 0):
        return False
    return True

def frappe():
    global joueur1
    global sprite_a_charger, imagesGauche, imagesDroite, imagesFrappeGauche, imagesFrappeDroite

    # On récupère la direction du personnage avant le coup
    if (sprite_a_charger in imagesGauche) or (sprite_a_charger in imagesFrappeGauche):
        direction_precedente = GAUCHE
    elif (sprite_a_charger in imagesDroite) or (sprite_a_charger in imagesFrappeDroite):
        direction_precedente = DROITE

    # On vérifie si le sprite qui était à charger est un sprite de coup
    # -> si c'est le cas, on récupère l'indice de ce sprite dans la liste d'images de coups correspondante
    # -> on ajoute 1 à l'indice pour avoir l'image suivante
    indice_sprite = 0
    if sprite_a_charger in imagesFrappeGauche:
        indice_sprite = imagesFrappeGauche.index(sprite_a_charger) + 1
    elif sprite_a_charger in imagesFrappeDroite:
        indice_sprite = imagesFrappeDroite.index(sprite_a_charger) + 1

    # Si l'indice du sprite à afficher est bien inférieur à la taille de la liste des images de coups (-> s'il reste des images de coup à afficher)
    if indice_sprite < len(imagesGauche):
        if direction_precedente == GAUCHE:
            sprite_a_charger = imagesFrappeGauche[ indice_sprite ]
        elif direction_precedente == DROITE:
            sprite_a_charger = imagesFrappeDroite[ indice_sprite ]
    # Sinon si toutes les images ont été affichées, on affiche l'image de départ (au repos) dans la direction du personnage
    else:
        if direction_precedente == GAUCHE:
            sprite_a_charger = imagesGauche[0]
        elif direction_precedente == DROITE:
            sprite_a_charger = imagesDroite[0]

    # Chargement du bon sprite
    canvas.itemconfigure(joueur1, image=sprite_a_charger)

    # Si toutes les images ont été affichées
    if indice_sprite < len(imagesFrappeGauche):
        # -> on rappelle la fonction après 140ms
        fenetre.after(140, frappe)
    
    
# CONSTANTES
DIM_FEN = (1080, 720)
DIM_PERSO = (35, 60)
DIM_JOUABLE = (1080, 571)

GAUCHE = 0
DROITE = 1
HAUT = 2
BAS = 3

DEP_H = 14
DEP_V = 60

# Création de la fenêtre principale
fenetre = Tk()
fenetre.title("TkSmash - Fight for Glory")
fenetre.geometry("{}x{}".format(DIM_FEN[0], DIM_FEN[1]))
fenetre.resizable(width=False, height=False)

# Création du canvas
canvas = Canvas(fenetre, width=DIM_FEN[0], height=720, bg="white")
canvas.pack()

# Affichage du fond
fond = PhotoImage(file=("background.gif"))
canvas.create_image(0, 0, anchor="nw", image=fond)

# Affichage du sol
sol = PhotoImage(file=("sol.gif"))
for i in range(4):
    canvas.create_image(i * 270, 571, anchor="nw", image=sol)

# Chargement des sprites
    # Sprites vers la gauche
cheminImagesGauche = ["img/perso/1/marche/G/{}.gif".format(i+1) for i in range(6)]
imagesGauche = list()
for chemin in cheminImagesGauche:
    imagesGauche.append( PhotoImage(file=chemin) )

    # Sprites vers la droite
cheminImagesDroite = ["img/perso/1/marche/D/{}.gif".format(i+1) for i in range(6)]
imagesDroite = list()
for chemin in cheminImagesDroite:
    imagesDroite.append( PhotoImage(file=chemin) )

    # Sprites vers le haut
cheminImagesSautGauche = ["img/perso/1/saut/G/{}.gif".format(i+1) for i in range(2)]
cheminImagesSautDroite = ["img/perso/1/saut/D/{}.gif".format(i+1) for i in range(2)]
imagesSautGauche, imagesSautDroite = list(), list()
for chemin in cheminImagesSautGauche:
    imagesSautGauche.append( PhotoImage(file=chemin) )
for chemin in cheminImagesSautDroite:
    imagesSautDroite.append( PhotoImage(file=chemin) )

    # Sprites d'attaques
cheminImagesFrappeGauche = ["img/perso/1/frappe/G/FG{}.gif".format(i+1) for i in range(6)]
cheminImagesFrappeDroite = ["img/perso/1/frappe/D/{}.gif".format(i+1) for i in range(6)]
imagesFrappeGauche, imagesFrappeDroite = list(), list()
for chemin in cheminImagesFrappeGauche:
    imagesFrappeGauche.append(PhotoImage(file=chemin))
for chemin in cheminImagesFrappeDroite:
    imagesFrappeDroite.append(PhotoImage(file=chemin))

# Variables globales
en_l_air = False
sprite_a_charger = imagesDroite[0]

# Affichage du personnage
joueur1 = canvas.create_image(20, DIM_JOUABLE[1]-DIM_PERSO[1], image=sprite_a_charger, anchor="nw")

# Gestion des événements
fenetre.bind_all("<KeyPress>", clavier)
fenetre.bind_all("<KeyRelease>", clavier_relachement)

# Boucle principale
fenetre.mainloop()
