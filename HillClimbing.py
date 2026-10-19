from collections import Counter

import numpy as np
import time
import random

def HillClimbing(matriceinitiale, lockedindices, compteur, Ex):
    """
    Algorithme de Hill Climbing pour résoudre le problème du jeu "Sudoku".
    
    Arguments:
        matriceinitiale (np.ndarray): La matrice représentant l'état initial du jeu Sudoku.
        lockedindices (list): La liste des indices des cases verrouillées dans la matrice initiale (les cases déjà remplies dans l'exemple).
        compteur (int): Le numéro de l'exécution (pour créer le fichier de sortie).
        Ex (int): Le numéro de l'exemple pour créer le dossier de sortie.
    """
    it = 0 # Compteur pour suivre le nombre d'itérations
    starttime = time.time() # Variable pour suivre le temps d'exécution
    matriceetat = np.copy(matriceinitiale)  # Copie de la matrice initiale pour manipulation
    max_it = 300_000 # Nombre maximum d'itérations pour l'algorithme Hill Climbing

    # Génération de toutes les paires de cases échangeables dans chaque bloc 3x3
    paires_echangeables = [] # Liste pour stocker toutes les paires de cases échangeables
    for bi in range(0, 9, 3): # Parcours des blocs 3x3 par ligne
        for bj in range(0, 9, 3): # Parcours des blocs 3x3 par colonne
            cases_libres = [ # Liste des cases libres (non verrouillées) dans le bloc 3x3 actuel
                (i, j)
                for i in range(bi, bi + 3) # Parcours des lignes du bloc 3x3 actuel
                for j in range(bj, bj + 3) # Parcours des colonnes du bloc 3x3 actuel
                if (i, j) not in lockedindices # Vérification que la case n'est pas verrouillée
            ]
            for index, premiere_case in enumerate(cases_libres): # Parcours des cases libres pour générer les paires échangeables
                for seconde_case in cases_libres[index + 1:]: # Génération des paires avec les cases suivantes
                    paires_echangeables.append((premiere_case, seconde_case)) # Ajout de la paire à la liste des paires échangeables

    # Ouverture en mode écriture ("w") du fichier de sortie des informations avec encodage UTF-8 (pour gérer les accents)
    with open("output-partie2/output_" + str(Ex) + "/HillClimbing_" + str(compteur) + ".txt", "w", encoding="utf-8") as output:
        # Vérifier s'il existe des paires de cases échangeables avant de continuer
        if not paires_echangeables:
            output.write("Aucun échange possible.\n")
            output.write("Score : " + str(Valeur) + "\n")
            print("Execution ", compteur, ": Aucun échange possible.") # Message de confirmation dans la console
            return # Sortir de la fonction si aucun échange n'est possible

        # Implémentation de l'algorithme Hill Climbing
        while True:
            # 1. Évaluer l'état actuel
            Valeur = evaluation(matriceetat) # Évaluer l'état actuel

            # Si la valeur d'évaluation est 0, cela signifie que l'état est parfait et l'algorithme peut s'arrêter
            if Valeur == 0:
                # Écrire la grille résolue dans le fichier de sortie
                output.write("Grille résolue :\n")
                for i in range(9):
                    # Formate chaque bloc de 3 colonnes séparé par " | "
                    ligne = " | ".join(" ".join(str(matriceetat[i, j]) for j in range(b * 3, (b + 1) * 3)) for b in range(3))
                    output.write(ligne + "\n")
                    # Ajoute les lignes de séparation horizontales après les lignes 2 et 5
                    if i == 2 or i == 5:
                        output.write("------|-------|-------\n")

                # Écrire le temps d'exécution dans le fichier de sortie
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
                # Écrire le nombre d'itérations dans le fichier de sortie
                output.write("Nombre d'itérations : " + str(it) + "\n")
                print("Execution ", compteur, ": Solution trouvée !") # Message de confirmation dans la console
                break # Sortir de la boucle

            # Vérifier si le nombre maximum d'itérations a été atteint
            if it >= max_it:
                output.write("Nombre maximum d'itérations atteint : " + str(max_it) + ", solution non trouvée.\n")
                output.write("Score final : " + str(Valeur) + " Temps d'exécution :" + str(round(time.time() - starttime, 4)) + " secondes.\n")
                print("Execution ", compteur, ": Nombre maximum d'itérations atteint, solution non trouvée.") # Message de confirmation dans la console
                break # Sortir de la boucle si le nombre maximum d'itérations est atteint

            # 2. Parcourir chaque carré de 3x3 PERMUTABLES et trouver le meilleur voisin : Trouver le meilleur voisin dans la grille et permutter les valeurs
            # 2.1 Initialiser les structures de données pour le parcours des voisins
            meilleurs_echanges = [] # Liste pour stocker les meilleurs échanges trouvés
            meilleur_voisin_val = Valeur # Initialiser la valeur du meilleur voisin vers la valeur actuelle
            compteurs_lignes = [Counter(matriceetat[i, :]) for i in range(9)] # Compteurs pour chaque ligne
            compteurs_colonnes = [Counter(matriceetat[:, j]) for j in range(9)] # Compteurs pour chaque colonne

            # 2.2 Parcourir toutes les paires échangeables et évaluer le delta pour chaque échange
            for case1, case2 in paires_echangeables: # Boucle pour parcourir toutes les paires échangeables
                i, j = case1 # Coordonnées de la première case de l'échange
                y, z = case2 # Coordonnées de la seconde case de l'échange
                valeur1 = matriceetat[i, j] # Valeur de la première case de l'échange
                valeur2 = matriceetat[y, z] # Valeur de la seconde case de l'échange
                delta = 0 # Initialiser le delta pour cet échange
                # Évaluer l'impact de l'échange sur les lignes et les colonnes
                if i != y: # SI les lignes des deux cases sont différentes, évaluer l'impact sur les lignes
                    delta += evaluation_delta(compteurs_lignes[i], valeur1, valeur2) # Évaluer l'impact sur la ligne i
                    delta += evaluation_delta(compteurs_lignes[y], valeur2, valeur1) # Évaluer l'impact sur la ligne y
                if j != z: # SI les colonnes des deux cases sont différentes, évaluer l'impact sur les colonnes
                    delta += evaluation_delta(compteurs_colonnes[j], valeur1, valeur2) # Évaluer l'impact sur la colonne j
                    delta += evaluation_delta(compteurs_colonnes[z], valeur2, valeur1) # Évaluer l'impact sur la colonne z
                valeurvoisin = Valeur + delta # Calculer la valeur du voisin en ajoutant le delta à la valeur actuelle
                if valeurvoisin < meilleur_voisin_val: # Si le voisin est meilleur que le meilleur voisin trouvé jusqu'à présent
                    meilleur_voisin_val = valeurvoisin # Mettre à jour la valeur du meilleur voisin trouvé jusqu'à présent
                    meilleurs_echanges = [(case1, case2)] # Réinitialiser la liste des meilleurs échanges avec le nouvel échange trouvé
                elif valeurvoisin == meilleur_voisin_val and valeurvoisin < Valeur: # Si le voisin a la même valeur que le meilleur voisin trouvé jusqu'à présent et qu'il est meilleur que l'état actuel
                    meilleurs_echanges.append((case1, case2)) # Ajouter l'échange à la liste des meilleurs échanges

            # 2.3 On met à jour l'état actuel avec le meilleur voisin trouvé (meilleure permutation)
            if meilleurs_echanges: # SI un meilleur voisin a été trouvé
                premiere_case, seconde_case = random.choice(meilleurs_echanges) # Choisir un échange aléatoire parmi les meilleurs échanges trouvés
                i, j = premiere_case # Coordonnées de la première case de l'échange choisie aléatoirement
                y, z = seconde_case # Coordonnées de la seconde case de l'échange choisie aléatoirement
                matriceetat[i, j], matriceetat[y, z] = matriceetat[y, z], matriceetat[i, j] # Mettre à jour la matrice d'état avec le meilleur échange trouvé

            # 3. SINON, aucun changement n'a été effectué. Lancer l'échappement d'un plateau local
            else: # Si aucun changement n'a été effectué lors de cette itération, on tente des swaps aléatoires, cela permet d'échapper à un plateau local
                for _ in range(8): # Boucle pour échapper au plateau local, 8 swaps aléatoires
                    premiere_case, seconde_case = random.choice(paires_echangeables) # Choisir un échange aléatoire parmi les paires échangeables
                    i, j = premiere_case # Coordonnées de la première case de l'échange aléatoire
                    y, z = seconde_case # Coordonnées de la seconde case de l'échange aléatoire
                    matriceetat[i, j], matriceetat[y, z] = matriceetat[y, z], matriceetat[i, j] # Échanger les valeurs pour échapper au plateau local

            # 4. Prochaine itération
            it += 1 # Incrémenter le compteur d'itérations

def evaluation(matrice):
    """
    Fonction d'évaluation pour mesurer la qualité d'un état du Sudoku (0 = état parfait résolu).
    Arguments:
        matrice (np.ndarray): La matrice représentant l'état actuel du Sudoku.
    Retourne:
        int: Le score d'évaluation (plus le score est bas, meilleur est l'état).
    """
    # 1. Compter le nombre de doublons dans les lignes
    nbdoublelignes = 0 # Compteur pour suivre le nombre de doublons dans les lignes
    for i in range(9): # Parcours des lignes
        ligne = [] # Liste pour suivre les éléments déjà vus dans la ligne
        for j in range(9): # Parcours des colonnes de la ligne actuelle
            if matrice[i, j] in ligne: # Si l'élément est déjà dans la ligne, c'est un doublon
                nbdoublelignes += 1 # Incrémenter le compteur de doublons dans les lignes
            ligne.append(matrice[i, j]) # Ajouter l'élément à la liste des éléments déjà vus dans la ligne

    # 2. Compter le nombre de doublons dans les colonnes
    nbdoublecolonnes = 0 # Compteur pour suivre le nombre de doublons dans les colonnes
    for j in range(9): # Parcours des colonnes
        colonne = [] # Liste pour suivre les éléments déjà vus dans la colonne
        for i in range(9): # Parcours des lignes de la colonne actuelle
            if matrice[i, j] in colonne: # Si l'élément est déjà dans la colonne, c'est un doublon
                nbdoublecolonnes += 1 # Incrémenter le compteur de doublons dans les colonnes
            colonne.append(matrice[i, j]) # Ajouter l'élément à la liste des éléments déjà vus dans la colonne
     
    # 3. Calcul du score final basé sur le nombre total de doublons
    score = nbdoublelignes + nbdoublecolonnes # Le score est la somme de tous les doublons
    return score

def evaluation_delta(counts, old_value, new_value):
    """
    Calcule le changement de score d'évaluation lorsqu'une valeur dans une ligne ou une colonne est remplacée.
    Arguments:
        counts (Counter): Compteur des occurrences des valeurs dans la ligne ou la colonne.
        old_value (int): La valeur actuelle.
        new_value (int): La nouvelle valeur.
    Retourne:
        int: La différence de score d'évaluation résultant du remplacement.
    """
    if old_value == new_value: # Aucun changement si l'ancienne valeur est identique à la nouvelle.
        return 0
    added_duplicate = int(counts[new_value] > 0) # Vérifie si l'ajout de la nouvelle valeur crée un doublon
    removed_duplicate = int(counts[old_value] > 1) # Vérifie si la suppression de l'ancienne valeur réduit un doublon
    return added_duplicate - removed_duplicate # Retourne la différence de score d'évaluation résultant du remplacement