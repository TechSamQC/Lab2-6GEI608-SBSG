from ast import Index

import numpy as np
import time

def AlgoAstar(matriceinitiale, matricevoulue, compteur, Ex):
    """
    Algorithme informée A* pour résoudre le problème du jeu "8-puzzle".
    
    Arguments:
        matriceinitiale (np.ndarray): La matrice représentant l'état initial du jeu.
        matricevoulue (np.ndarray): La matrice représentant l'état souhaité du jeu.
        compteur (int): Le numéro de l'exécution (pour créer le fichier de sortie).
        Ex (int): Le numéro de l'exemple pour créer le dossier de sortie.
    """
    # Définition des variables nécessaires pour l'algorithme
    it = 0 # Compteur pour suivre le nombre d'itérations
    starttime = time.time() # Variable pour suivre le temps d'exécution
    matriceetat = np.copy(matriceinitiale)  # Copie de la matrice initiale pour manipulation
    ListeFrontiere = []  # Liste des états à explorer
    ListeFrontiere.append(matriceetat)  # Ajouter l'état initial à la liste des états à explorer
    parents = [None] # Liste pour garder l'index du parent de chaque état dans ListeFrontiere. L'état initial (index 0) n'a pas de parent (None)

    # Création d'un set() avec la matrice initiale sous forme d'octets afin de vérifier si un état a déjà été exploré de facon performante
    vus = set()
    vus.add(matriceinitiale.tobytes())


# Fonction H (Heuristique) :
def H(matriceetat, matricevoulue):
    """
    Calcul de l'heuristique pour l'état actuel. Ici, nous utilisons le max entre H1 (nombre de cases mal placées) et H2 (distance de Manhattan).

    Arguments:
        matriceetat (np.ndarray): La matrice représentant l'état actuel du jeu.
        matricevoulue (np.ndarray): La matrice représentant l'état souhaité du jeu.
    """
    # H1 : Nombre de cases mal placées
    H1 = np.sum((matriceetat != matricevoulue) & (matriceetat != '*')) # Fait le calcul du nombre de case qui ne sont pas à la bonne position en ne prenant pas en compte la case vide (*)

    # H2 : Distance de Manhattan
    H2 = 0 # Initialisation de la distance de Manhattan
    # Parcours de chaque case de la matrice pour calculer la distance de Manhattan
    for i in range(3): # Parcours des lignes de la matrice
        for j in range(3): # Parcours des colonnes de la matrice
            if matriceetat[i, j] != '*': # Ignorer la case vide (*) pour le calcul de la distance de Manhattan
                x = np.where(matricevoulue == matriceetat[i, j])[0][0]  # Coordonnée x voulue de la case
                y = np.where(matricevoulue == matriceetat[i, j])[1][0]  # Coordonnée y voulue de la case
                H2 += abs(x - i) + abs(y - j) # La distance de Manhattan pour cette case est la différence entre sa position actuelle et sa position souhaitée

    # Retourne H3 : la valeur maximale entre H1 et H2
    return max(H1, H2) # H3