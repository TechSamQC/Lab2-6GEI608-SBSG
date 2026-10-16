import numpy as np
import time

from SudokuFilling import fill

def AlgoGenetic(matriceinitiale, lockedindices, compteur, Ex):
    """
    Algorithme génétique pour résoudre le problème du jeu "Sudoku".
    
    Arguments:
        matriceinitiale (np.ndarray): La matrice représentant l'état initial du jeu Sudoku.
        lockedindices (list): La liste des indices des cases verrouillées dans la matrice initiale (les cases déjà remplies dans l'exemple).
        compteur (int): Le numéro de l'exécution (pour créer le fichier de sortie).
        Ex (int): Le numéro de l'exemple pour créer le dossier de sortie.
    """
    it = 0 # Compteur pour suivre le nombre d'itérations
    starttime = time.time() # Variable pour suivre le temps d'exécution
    matriceetat = np.copy(matriceinitiale)  # Copie de la matrice initiale pour manipulation
    max_it = 300_000 # Nombre maximum d'itérations pour l'algorithme génétique

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

    # Initialisation de la population pour l'algorithme génétique
    population = [np.copy(matriceetat)] # Liste pour stocker les individus de la population

    for _ in range(19): # Taille de la population de 20 (1 état initial + 19 nouveaux individus)
        nouvel_individu = np.copy(matriceetat) # Créer un nouvel individu en copiant l'état initial
        fill(nouvel_individu, lockedindices, 9) # Remplir les cases vides avec des chiffres aléatoires (1 à 9 dans chaque bloc)
        population.append(nouvel_individu) # Ajouter le nouvel individu à la population

    # Ouverture en mode écriture ("w") du fichier de sortie des informations avec encodage UTF-8 (pour gérer les accents)
    with open("output-partie2/output_" + str(Ex) + "/AlgoGenetic_" + str(compteur) + ".txt", "w", encoding="utf-8") as output:
        # Implémentation de l'algorithme génétique
        while True:
            # Vérification de la condition d'arrêt basée sur le nombre maximum d'itérations
            if it >= max_it:
                output.write("Nombre maximum d'itérations atteint. Aucun solution trouvée.\n")
                print("Execution ", compteur, ": Nombre maximum d'itérations atteint. Aucun solution trouvée.")
                break

            # 1. Évaluation de la fitness de chaque individu de la population
            fitness_scores = [fonction_fitness(individu) for individu in population]

            # Vérification de la condition d'arrêt (si un individu a une fitness parfaite)
            if 0 in fitness_scores: # Si un individu a une fitness parfaite (score de 0)
                # Écrire la grille résolue dans le fichier de sortie
                output.write("Grille résolue :\n")
                for i in range(9):
                    output.write(" ".join(str(population[fitness_scores.index(0)][i, j]) for j in range(9)) + "\n")
                # Écrire le temps d'exécution dans le fichier de sortie
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
                # Écrire le nombre d'itérations dans le fichier de sortie
                output.write("Nombre d'itérations : " + str(it) + "\n")
                print("Execution ", compteur, ": Solution trouvée !") # Message de confirmation dans la console
                break # Sortir de la boucle

            # 2. Tri des individus par fitness (du meilleur au pire)
            population = [individu for _, individu in sorted(zip(fitness_scores, population), key=lambda x: x[0])] # Tri des individus par fitness (du meilleur au pire)

            # 3. Application du crossover
            for i in range(0, len(population), 2): # Parcours des individus par paires
                if i + 1 < len(population): # S'assurer qu'il y a bien une paire d'individus pour le crossover
                    parent1 = population[i] # Sélection du premier parent pour le crossover
                    parent2 = population[i + 1] # Sélection du second parent pour le crossover
                    enfant1, enfant2 = crossover(parent1, parent2) # Appliquer le crossover pour générer deux enfants
                    population[i] = enfant1 # Remplacer le premier parent par le premier enfant
                    population[i + 1] = enfant2 # Remplacer le second parent par le second enfant

            # 4. Application de la mutation
            for i in range(len(population)): # Parcours de chaque individu de la population
                population[i] = mutation(population[i], paires_echangeables) # Appliquer la mutation à chaque individu

            ###########TESTS###########
            output.write("Itération : " + str(it) + "\n")
            for idx, indiv in enumerate(population):
                output.write("Individu " + str(idx) + " : " + str(fonction_fitness(indiv)) + "\n")
            output.write("\n") # Ajouter une ligne vide pour séparer les itérations

            # 5. Prochaine itération
            it += 1


def fonction_fitness(matrice):
    """
    Fonction de fitness pour évaluer la qualité d'un état du Sudoku.
    Arguments:
        matrice (np.ndarray): La matrice représentant l'état actuel du Sudoku.
    Retourne:
        int: Le score de fitness (plus le score est bas, meilleur est l'état).
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
    return nbdoublelignes + nbdoublecolonnes # Le score est la somme de tous les doublons

def crossover(parent1, parent2):
    """
    Fonction de crossover pour générer un enfant à partir de deux parents.
    Arguments:
        parent1 np.ndarray: Premier parent.
        parent2 np.ndarray: Second parent.
    Retourne:
        enfant1 np.ndarray: Premier enfant généré.
        enfant2 np.ndarray: Second enfant généré.
    """
    # Prendre 50% des blocs 3x3 de chaque parent pour créer les enfants
    enfant1 = np.copy(parent1) # Copier le premier parent pour créer le premier enfant
    enfant2 = np.copy(parent2) # Copier le second parent pour créer le second enfant
    for i in range(0, 9, 3): # Parcours des blocs 3x3 par ligne
        for j in range(0, 9, 3): # Parcours des blocs 3x3 par colonne
            if np.random.rand() < 0.5: # Avec une probabilité de 50%, échanger les blocs 3x3 entre les parents
                # Échanger les blocs 3x3 entre les parents
                temp = np.copy(enfant1[i:i+3, j:j+3]) # Copier le bloc 3x3 du premier enfant avant l'échange
                enfant1[i:i+3, j:j+3] = enfant2[i:i+3, j:j+3] # Échanger le bloc 3x3 avec le second enfant
                enfant2[i:i+3, j:j+3] = temp # Compléter l'échange des blocs 3x3 entre les enfants
    
    return enfant1, enfant2 # Retourner les deux enfants générés après le crossover

def mutation(individu, paires_echangeables):
    """
    Fonction de mutation pour modifier un individu.
    Arguments:
        individu np.ndarray: Individu représentant un état du Sudoku.
    Retourne:
        individu_muté np.ndarray: Individu après mutation.
    """
    individu_muté = np.copy(individu) # Copier l'individu avant de le muter

    # Selectionner aléatoirement trois paire de cases échangeables pour effectuer la mutation
    for _ in range(3): # Répéter trois fois pour sélectionner trois paires de cases échangeables
        paire = paires_echangeables[np.random.randint(len(paires_echangeables))] # Sélectionner une paire aléatoire
        (i1, j1), (i2, j2) = paire # Décomposer la paire en indices individuels
        individu_muté[i1, j1], individu_muté[i2, j2] = individu_muté[i2, j2], individu_muté[i1, j1] # Échanger les valeurs des cases sélectionnées

    return individu_muté # Retourner l'individu après mutation