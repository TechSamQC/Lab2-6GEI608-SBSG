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
    g_costs = [0] # Liste pour garder le coût g(n) de chaque état dans ListeFrontiere. L'état initial a un coût de 0.

    Current = 0 # Index de l'état courrant à explorer dans la liste de la frontière

    # Création d'un set() avec la matrice initiale sous forme d'octets afin de vérifier si un état a déjà été vu de facon performante
    vus = set() # Évite les doublons
    vus.add(matriceinitiale.tobytes())

    explored = set() # Set pour les états explorés

    # Ouverture en mode écriture ("w") du fichier de sortie des informations avec encodage UTF-8 (pour gérer les accents)
    with open("output_Ex1-" + str(Ex) + "/Algo_A_" + str(compteur) + "_stats.txt", "w", encoding="utf-8") as output:
        # Implémentation de l'algorithme A*
        while True:
            # 1. Sélectionner dans la frontière (non fermée) l'état qui minimise f(n) = g(n) + h(n)
            min_f = float('inf') # Initialisation de la valeur minimale de f(n) à l'infini
            Current = None # Index de l'état courant à explorer dans la liste de la frontière à NONE
            
            for index, etat in enumerate(ListeFrontiere): # Parcourir tous les états dans la frontière
                if etat.tobytes() not in explored: # SI l'état n'a pas encore été exploré
                    f = g_costs[index] + H(etat, matricevoulue) # Calcul de f(n) = g(n) + h(n) pour cet état
                    if f < min_f: # SI f(n) est plus petit que min_f, mettre à jour la valeur minimale de f(n) et l'état courant
                        min_f = f
                        Current = index

            # Sécurité pour éviter un crash si aucune solution n'existe (le courrant reste None)
            if Current is None:
                # Code pour enregistrer les données dans le fichier de sortie
                # Écriture des informations dans le fichier
                output.write("***AUCUNE SOLUTION TROUVÉE, TOUTS LES ÉTATS ONT ÉTÉ EXPLORÉS***\n")
                output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                output.write("Nombre d'états explorés : " + str(it) + ".\n")
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")
                print("Aucune solution trouvée (tous les états ont été explorés).") # Message de confirmation dans la console
                break

            # Marquer l'état courant comme exploré
            explored.add(ListeFrontiere[Current].tobytes())

            # 2. Vérifier si l'état courant correspond à l'état souhaité
            if np.array_equal(ListeFrontiere[Current], matricevoulue):
                # Code pour enregistrer les données dans le fichier de sortie
                # Écriture des informations dans le fichier
                output.write("Execution " + str(compteur) + ". \t Taille de la frontière finale : " + str(len(ListeFrontiere)) + ".\n")
                output.write("Nombre d'états explorés : " + str(it) + ".\n")
                output.write("Temps d'exécution : " + str(round(time.time() - starttime, 4)) + " secondes.\n")

                # Code pour enregistrer la solution dans le fichier de sortie
                with open("output_Ex1-" + str(Ex) + "/Algo_Largeur_" + str(compteur) + "_chemin_solution.txt", "w", encoding="utf-8") as solution:
                    # Parcourir les parents pour reconstruire le chemin
                    chemin = [] # Liste pour stocker le chemin de la solution
                    index_courant = Current # Index de l'état courant (solution) dans ListeFrontiere
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
            
            # Écriture de l'état courant dans le fichier de sortie
            output.write("Itération " + str(it) + ". \t Taille de la frontière : " + str(len(ListeFrontiere)) + ".\n")

            xinit = np.where(ListeFrontiere[Current] == "*")[0][0]  # Coordonnée x de la case vide dans l'état courant de cet itération
            yinit = np.where(ListeFrontiere[Current] == "*")[1][0]  # Coordonnée y de la case vide dans l'état courant de cet itération

            # 3. Génération des mouvements possibles (gauche, droite, haut, bas)

            # Option 1 = gauche
            if yinit > 0:  # Vérifie si on peut se déplacer vers la gauche
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit, yinit - 1] = matriceetat[xinit, yinit - 1], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été ajouté à la liste
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été ajouté à la liste
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état
                    g_costs.append(g_costs[Current] + 1) # Incrémentation du coût g(n)

            # Option 2 = droite
            if yinit < 2:  # Vérifie si on peut se déplacer vers la droite
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit, yinit + 1] = matriceetat[xinit, yinit + 1], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été ajouté à la liste
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été ajouté à la liste
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état
                    g_costs.append(g_costs[Current] + 1) # Incrémentation du coût g(n)

            # Option 3 = haut
            if xinit > 0:  # Vérifie si on peut se déplacer vers le haut
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit - 1, yinit] = matriceetat[xinit - 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été ajouté à la liste
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été ajouté à la liste
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état
                    g_costs.append(g_costs[Current] + 1) # Incrémentation du coût g(n)

            # Option 4 = bas
            if xinit < 2:  # Vérifie si on peut se déplacer vers le bas
                matriceetat = np.copy(ListeFrontiere[Current])  # Copie de l'état courant
                matriceetat[xinit, yinit], matriceetat[xinit + 1, yinit] = matriceetat[xinit + 1, yinit], matriceetat[xinit, yinit]  # Échange des valeurs

                # Transformation de la matrice en 'bytes' pour tester dans le set() efficacement si l'état a déjà été ajouté à la liste
                cle = matriceetat.tobytes()
                if cle not in vus: # Si l'état n'a pas encore été ajouté à la liste
                    vus.add(cle)  # On l'ajoute au set
                    ListeFrontiere.append(matriceetat)  # Et à la liste d'origine
                    parents.append(Current)  # L'état courant (Current) est le parent de ce nouvel état
                    g_costs.append(g_costs[Current] + 1) # Incrémentation du coût g(n)

            it += 1  # Incrémenter le compteur d'itérations


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