import pygame
import sys
import random

mode_propositions = '--mode-propositions' in sys.argv

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 800, 600
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Transformation")
temps_debut = pygame.time.get_ticks()  # Début du chronomètre
temps_limite = 360000  # 6 minutes en millisecondes
temps_message = 0
problemes_resolus = 0
jeu_termine = False

nb_transfo = 1
ind_transfo = 1
succes_consecutifs = 0
niveau = 1  # Niveau global


# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)

# Formes avec couleurs
def dessiner_carre(x, y):
    pygame.draw.rect(ecran, ROUGE, (x-25, y-25, 50, 50))

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

def generer_sequence(nb_transfo):
    formes = [dessiner_carre, dessiner_triangle, dessiner_etoile, dessiner_rond]
    random.shuffle(formes)
    sequence_initiale = formes[:]

    sequences = []
    for _ in range(nb_transfo):
        random.shuffle(formes)
        sequences.append(formes[:])

    # Appliquer les transformations pour obtenir la séquence cible
    sequence_entree = sequence_initiale[:]
    transfo = []
    for seq in sequences:
        transfo.append(transfo_seq(sequence_entree, seq))
        sequence_entree = seq

    return sequence_initiale, sequence_entree, transfo

def generer_transformation_incorrecte(transformation_correcte):
    transformation = list(transformation_correcte)  # Convertir en liste pour faciliter la permutation
    index_a, index_b = random.sample(range(len(transformation)), 2)  # Choisir deux indices au hasard

    # Échanger les éléments aux indices choisis
    transformation[index_a], transformation[index_b] = transformation[index_b], transformation[index_a]

    return ''.join(transformation)

def transfo_seq(sequence_entree, sequence_fin):
    correspondance = {forme: str(i+1) for i, forme in enumerate(sequence_entree)}
    transformation = ''.join([correspondance[forme] for forme in sequence_fin])
    return transformation

def verifier_transformation(reponse_utilisateur, transformation_attendue):
    return reponse_utilisateur == transformation_attendue

# Génération initiale des séquences
sequence_initiale, sequence_cible, transfo = generer_sequence(nb_transfo)
propositions = generer_transformation_incorrecte(transfo[ind_transfo - 1])

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
    temps_actuel = pygame.time.get_ticks()
    temps_ecoule = temps_actuel - temps_debut
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
                    if verifier_transformation(reponse_utilisateur, transfo[ind_transfo-1]):
                        message = "Correct! "
                        problemes_resolus+=1
                        succes_consecutifs += 1
                        if succes_consecutifs >= 4:
                            niveau+=1
                            message +='Passage niveau {}!!'.format(niveau)
                            succes_consecutifs = 0
                            if nb_transfo < 4:
                                if ind_transfo == 1:
                                    nb_transfo += 1
                                    ind_transfo = nb_transfo
                                else:
                                    ind_transfo -= 1
                        sequence_initiale, sequence_cible, transfo = generer_sequence(nb_transfo)
                        propositions = generer_transformation_incorrecte(transfo[ind_transfo - 1])
                    else:
                        succes_consecutifs = 0
                        message = "Incorrect.Essayez encore."
                    temps_message = temps_actuel  
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
    ecran.blit(temps_surface, (largeur - 175, 10))

    # Affichage du nombre de problèmes résolus et niveau
    resolus_texte = f"Résolus: {problemes_resolus}"
    resolus_surface = font.render(resolus_texte, True, NOIR)
    ecran.blit(resolus_surface, (10, 10))

    niveau_txt = font.render(f"Niveau: {niveau}", True, NOIR)
    ecran.blit(niveau_txt, (200, 10))

    for i, forme in enumerate(sequence_initiale):
        forme(80 + i * 80, 80)  # Ajustez les coordonnées selon vos besoins

    # Affichage de la séquence cible
    for i, forme in enumerate(sequence_cible):
        forme(80 + i * 80, 450)  # Ajustez les coordonnées selon vos besoins

    # Affichage des transformations connues, sauf celle à l'indice ind_transfo-1
    pas = (450-80)/(nb_transfo+1)
    for i, transfo_num in enumerate(transfo):
        if i != ind_transfo - 1:  # On saute la transformation que le joueur doit deviner
            text_surface = font.render(str(transfo_num), True, NOIR)
            ecran.blit(text_surface, (150, 80 + (i+1)*pas))  # Ajustez les coordonnées selon vos besoins
        else :
            if mode_propositions:
                 for j, proposition in enumerate(propositions):
                    print(len(propositions))
                    text_surface = font.render(proposition, True, NOIR)
                    ecran.blit(text_surface, (50 + j * 60, 80 + (i+1)*pas))
            else:
                text_surface = font.render("Transfo à trouver", True, NOIR)
                ecran.blit(text_surface, (100,80 + (i+1)*pas))  # Ajustez les coordonnées selon vos besoins


    # Zone de saisie et messages
    txt_surface = font.render(text, True, color)
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    ecran.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(ecran, color, input_box, 2)

    if temps_actuel - temps_message < 3000:  # 5000 millisecondes = 5 secondes
        msg_surface = font.render(message, True, VERT if "Correct" in message else ROUGE)
        ecran.blit(msg_surface, (300, 200))
    else:
        message = ''

    pygame.display.flip()

pygame.quit()