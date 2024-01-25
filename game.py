import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 800, 600
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Transformation")
temps_debut = pygame.time.get_ticks()  # Début du chronomètre
temps_limite = 360000  # 6 minutes en millisecondes
problemes_resolus = 0
jeu_termine = False

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)

# Formes avec couleurs
def dessiner_carre(x, y):
    pygame.draw.rect(ecran, ROUGE, (x, y, 50, 50))

def dessiner_rond(x, y):
    pygame.draw.circle(ecran, VERT, (x, y), 25)

def dessiner_etoile(x, y):
    points = [(x, y-30), (x+10, y-10), (x+30, y-10), (x+15, y+5), 
              (x+20, y+25), (x, y+10), (x-20, y+25), (x-15, y+5), 
              (x-30, y-10), (x-10, y-10)]
    pygame.draw.polygon(ecran, BLEU, points)

def dessiner_triangle(x, y):
    points = [(x, y-25), (x-25, y+25), (x+25, y+25)]
    pygame.draw.polygon(ecran, JAUNE, points)

# Fonctions utilitaires
def generer_sequences():
    formes = [dessiner_carre, dessiner_triangle, dessiner_etoile, dessiner_rond]
    random.shuffle(formes)
    sequence_initiale = formes[:]
    random.shuffle(formes)
    sequence_cible = formes[:]
    return sequence_initiale, sequence_cible

def generer_sequences_niveau2():
    formes = [dessiner_carre, dessiner_triangle, dessiner_etoile, dessiner_rond]
    random.shuffle(formes)
    sequence_initiale = formes[:]
    random.shuffle(formes)
    sequence_intermediaire = formes[:]
    random.shuffle(formes)
    sequence_cible = formes[:]
    return sequence_initiale, sequence_intermediaire, sequence_cible


def verifier_transformation(reponse_utilisateur, sequence_initiale, sequence_cible):
    correspondance = {forme: str(i+1) for i, forme in enumerate(sequence_initiale)}
    transformation_attendue = ''.join([correspondance[forme] for forme in sequence_cible])
    return reponse_utilisateur == transformation_attendue

# Génération initiale des séquences
sequence_initiale, sequence_cible = generer_sequences()

# Entrée utilisateur
font = pygame.font.Font(None, 36)
input_box = pygame.Rect(100, 550, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
message = ''

# Boucle principale
en_cours = True
while en_cours:
    temps_ecoule = pygame.time.get_ticks() - temps_debut
    temps_restant = max(0, temps_limite - temps_ecoule)
    if temps_ecoule >= temps_limite and not jeu_termine:
        message = f"Temps écoulé! Problèmes résolus : {problemes_resolus}"
        jeu_termine = True

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            # Si l'utilisateur clique sur la zone de saisie
            if input_box.collidepoint(evenement.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if evenement.type == pygame.KEYDOWN and not jeu_termine:
            if active:
                if evenement.key == pygame.K_RETURN:
                    reponse_utilisateur = text
                    if verifier_transformation(reponse_utilisateur, sequence_initiale, sequence_cible):
                        message = "Correct! Nouvelle séquence générée."
                        sequence_initiale, sequence_cible = generer_sequences()
                        problemes_resolus+=1
                    else:
                        message = "Incorrect. Essayez encore."
                    text = ''
                elif evenement.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += evenement.unicode
    ecran.fill(BLANC)

    # Affichage du temps restant
    minutes_restantes, secondes_restantes = divmod(temps_restant // 1000, 60)
    temps_texte = f"Temps: {minutes_restantes:02d}:{secondes_restantes:02d}"
    temps_surface = font.render(temps_texte, True, NOIR)
    ecran.blit(temps_surface, (largeur - 150, 10))

    # Affichage du nombre de problèmes résolus
    resolus_texte = f"Résolus: {problemes_resolus}"
    resolus_surface = font.render(resolus_texte, True, NOIR)
    ecran.blit(resolus_surface, (10, 10))

    # Dessiner les séquences
    for i, forme in enumerate(sequence_initiale):
        forme(100 + i * 100, 100)

    for i, forme in enumerate(sequence_cible):
        forme(100 + i * 100, 300)

    # Zone de saisie et messages
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    ecran.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(ecran, color, input_box, 2)

    msg_surface = font.render(message, True, VERT if "Correct" in message else ROUGE)
    ecran.blit(msg_surface, (100, 450))

    pygame.display.flip()

pygame.quit()
