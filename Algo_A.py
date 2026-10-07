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

    MinH = 0 # Valeur minimale de l'heuristique dans la boucle principale
    Current = 0 # Index de l'état courrant à explorer dans la liste de la frontière
    Next = 0 # Index du prochain état à explorer dans la liste de la frontière (heuristique minimale)

    # Création d'un set() avec la matrice initiale sous forme d'octets afin de vérifier si un état a déjà été exploré de facon performante
    vus = set()
    vus.add(matriceinitiale.tobytes())

    # Ouverture en mode écriture ("w") du fichier de sortie des informations avec encodage UTF-8 (pour gérer les accents)
    with open("output_Ex1-" + str(Ex) + "/Algo_A_" + str(compteur) + "_stats.txt", "w", encoding="utf-8") as output:
        # Implémentation de l'algorithme A*
        while True:
            # Sécurité pour éviter un crash si aucune solution n'existe
            if it >= len(ListeFrontiere):
                # Code pour enregistrer les données dans le fichier de sortie
                # Écriture des informations dans le fichier
                output.write("***AUCUNE SOLUTION TROUVÉE, TOUTS LES ÉTATS ONT ÉTÉ EXPLORÉS***\n")
                output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                output.write("Nombre d'états explorés : " + str(it) + ".\n")
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
                print("Aucune solution trouvée (tous les états ont été explorés).") # Message de confirmation dans la console
                break

            xinit = np.where(ListeFrontiere[Current] == "*")[0][0]  # Coordonnée x de la case vide dans l'état courant de cet itération
            yinit = np.where(ListeFrontiere[Current] == "*")[1][0]  # Coordonnée y de la case vide dans l'état courant de cet itération

            if np.array_equal(ListeFrontiere[Current], matricevoulue):  # Vérifie si l'état courant correspond à l'état souhaité
                # Code pour enregistrer les données dans le fichier de sortie
                # Écriture des informations dans le fichier
                output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                output.write("Nombre d'états explorés : " + str(it) + ".\n")
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")

                # Code pour enregistrer la solution dans le fichier de sortie
                with open("output_Ex1-" + str(Ex) + "/Algo_Largeur_" + str(compteur) + "_chemin_solution.txt", "w", encoding="utf-8") as solution:
                    # Parcourir les parents pour reconstruire le chemin
                    chemin = [] # Liste pour stocker le chemin de la solution
                    index_courant = it # Index de l'état courant (solution) dans ListeFrontiere
                    while index_courant is not None: # Tant que l'on n'a pas atteint l'état initial (parent None)
                        chemin.append(ListeFrontiere[index_courant]) # Ajouter la matrice de l'état courant à la liste du chemin
                        index_courant = parents[index_courant]  # On remonte vers le parent suivant
                    chemin.reverse()  # Inverser pour avoir le chemin de l'état initial à la solution

                    # Écriture de la taille du chemin de la solution dans le fichier
                    solution.write("Taille du chemin de la solution : " + str(len(chemin)) + ".\n")

                    # Écriture du chemin de la solution dans le fichier
                    solution.write("Chemin de la solution (de l'état initial à l'état souhaité) :\n")
                    for etat in chemin: # Parcourir chaque état dans le chemin
                        # Écrire l'état dans le fichier de solution en transformant l'array en texte, en supprimant les caractères inutiles 
                        # et en ajoutant deux sauts de ligne entre chaque état pour une meilleure lisibilité 
                        solution.write(np.array2string(etat).replace("[", "").replace("]", "").replace(" ", "").replace("''", "\t").replace("'", "") + "\n\n") # Écrire l'état dans le fichier de solution

                print("Execution ", compteur, ": Solution trouvée !") # Message de confirmation dans la console
                break  # Sortir de la boucle si la solution est trouvée

            MinH = 10000 # Réinitialisation de la valeur minimale de l'heuristique pour cette itération (prends une très grande valeur pour s'assurer que toute nouvelle heuristique sera plus petite)
            
            # Écriture de l'état courant dans le fichier de sortie
            output.write("Itération " + str(it) + ". \t Taille de la frontière : " + str(len(ListeFrontiere)) + ".\n")

            # Option 1 = gauche
            if yinit > 0:  # Vérifie si on peut se déplacer vers la gauche
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état

                    # Vérifier maintenant si l'état fait diminuer l'heuristique
                    if MinH > H(matriceetat, matricevoulue):
                        MinH = H(matriceetat, matricevoulue) # Si l'heuristique diminue, on met à jour MinH
                        Next = len(ListeFrontiere) - 1 # Mettre à jour l'index du prochain état à explorer à celui-ci


            # Option 2 = droite
            if yinit < 2:  # Vérifie si on peut se déplacer vers la droite
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état

                    # Vérifier maintenant si l'état fait diminuer l'heuristique
                    if MinH > H(matriceetat, matricevoulue):
                        MinH = H(matriceetat, matricevoulue) # Si l'heuristique diminue, on met à jour MinH
                        Next = len(ListeFrontiere) - 1 # Mettre à jour l'index du prochain état à explorer à celui-ci


            # Option 3 = haut
            if xinit > 0:  # Vérifie si on peut se déplacer vers le haut
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état

                    # Vérifier maintenant si l'état fait diminuer l'heuristique
                    if MinH > H(matriceetat, matricevoulue):
                        MinH = H(matriceetat, matricevoulue) # Si l'heuristique diminue, on met à jour MinH
                        Next = len(ListeFrontiere) - 1 # Mettre à jour l'index du prochain état à explorer à celui-ci


            # Option 4 = bas
            if xinit < 2:  # Vérifie si on peut se déplacer vers le bas
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été exploré
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été exploré
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état

                    # Vérification si l'état fait diminuer l'heuristique
                    if MinH > H(matriceetat, matricevoulue):
                        MinH = H(matriceetat, matricevoulue) # Si l'heuristique diminue, on met à jour MinH
                        Next = len(ListeFrontiere) - 1 # Mettre à jour l'index du prochain état à explorer à celui-ci


            Current = Next # Mettre à jour l'état courant à l'état suivant choisi en fonction de l'heuristique
            it += 1  # Incrémenter le compteur d'itérations

            output.write("Current state index: " + str(Current) + "\n") # TEST
            output.write("Current state heuristic: " + str(MinH) + "\n") # TEST


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