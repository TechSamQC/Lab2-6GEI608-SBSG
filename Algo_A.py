import heapq  # Fournit une file de priorité pour choisir le plus petit coût f.
import time  # Permet de mesurer la durée de la recherche.
from pathlib import Path  # Permet de créer les dossiers et les chemins de sortie.

import numpy as np  # Permet de manipuler les matrices du 8-puzzle.


def H(matriceetat, matricevoulue, positionsvoulues=None):
    """Calcule H3 = max(H1, H2), sans compter la case vide."""

    H1 = int(np.sum((matriceetat != matricevoulue) & (matriceetat != "*")))  # Compte les cases mal placées.
    H2 = 0  # Initialise la somme des distances de Manhattan.

    if positionsvoulues is None:  # Permet aussi d'appeler H avec seulement deux arguments.
        positionsvoulues = {}  # Associe chaque valeur à sa position dans la matrice objectif.

        for i in range(3):  # Parcourt les lignes de la matrice objectif.
            for j in range(3):  # Parcourt les colonnes de la matrice objectif.
                positionsvoulues[matricevoulue[i, j]] = (i, j)  # Mémorise les coordonnées de chaque valeur.

    for i in range(3):  # Parcourt les lignes de l'état à évaluer.
        for j in range(3):  # Parcourt les colonnes de l'état à évaluer.

            if matriceetat[i, j] != "*":  # Ignore la case vide.
                x, y = positionsvoulues[matriceetat[i, j]]  # Retrouve la position souhaitée de la case.
                H2 += abs(x - i) + abs(y - j)  # Additionne les distances verticale et horizontale.

    return max(H1, H2)  # Retourne H3 ; pour ce puzzle, H2 est toujours supérieur ou égal à H1.


def AlgoAstar(matriceinitiale, matricevoulue, compteur, Ex):
    """
    Résout le 8-puzzle avec A* : f(n) = g(n) + H(n).

    Arguments :
        matriceinitiale : grille de départ.
        matricevoulue : grille objectif.
        compteur : numéro de l'exécution.
        Ex : numéro de l'exemple.

    Les matrices contiennent les caractères 1 à 8 et * pour la case vide.

    Retour :
        Liste des déplacements du vide si une solution est trouvée.
        Liste vide si la grille est déjà résolue.
        None si aucune solution n'existe.

    Fichier des statistiques :
        Une ligne par itération : numéro TAB nombre d'états distincts explorés.
        Avant-dernière ligne : nombre total d'états examinés.
        Dernière ligne : temps de recherche en secondes.

    Une itération correspond à un état effectivement examiné, objectif compris.
    Les anciennes entrées de la frontière devenues inutiles sont ignorées.
    Le chronométrage exclut la reconstruction et l'écriture des résultats.
    """

    matriceinitiale = np.asarray(matriceinitiale, dtype=str)  # Uniformise les valeurs de la grille initiale.
    matricevoulue = np.asarray(matricevoulue, dtype=str)  # Uniformise les valeurs de la grille objectif.
    valeursattendues = {"*", "1", "2", "3", "4", "5", "6", "7", "8"}  # Définit les neuf valeurs autorisées.

    for nom, matrice in (("initiale", matriceinitiale), ("objectif", matricevoulue)):  # Vérifie les deux grilles.
        if matrice.shape != (3, 3) or set(matrice.flat) != valeursattendues:  # Refuse une mauvaise dimension ou des valeurs incorrectes.
            raise ValueError(
                f"La matrice {nom} doit contenir une fois chaque valeur "
                "de 1 à 8 et un * dans une grille 3 x 3."
            )

    dossier_sortie = Path(__file__).resolve().parent / f"output_Ex1-{Ex}"  # Prépare le dossier des résultats.
    dossier_sortie.mkdir(parents=True, exist_ok=True)  # Crée ce dossier s'il n'existe pas.
    fichier_stats = dossier_sortie / f"Algo_A_{compteur}_stats.txt"  # Prépare le fichier des mesures.
    fichier_solution = dossier_sortie / f"Algo_A_{compteur}_chemin_solution.txt"  # Prépare le fichier du chemin.

    starttime = time.perf_counter()  # Démarre le chronomètre de la recherche.
    it = 0  # Compte les états effectivement examinés.
    ordre = 0  # Départage les états ayant le même coût f selon leur ordre d'ajout.

    ListeEtats = [np.copy(matriceinitiale)]  # Conserve les matrices des états découverts.
    parents = [None]  # L'état initial n'a pas de parent.
    actions = [None]  # Aucun déplacement n'a été effectué pour atteindre l'état initial.
    CoutsG = [0]  # Le coût du chemin jusqu'à l'état initial est zéro.

    indices = {ListeEtats[0].tobytes(): 0}  # Associe chaque état connu à son indice dans ListeEtats.
    explores = set()  # Mémorise les états distincts effectivement examinés.
    mesures = []  # Conserve les mesures pour les écrire après la recherche.
    indice_solution = None  # Indique qu'aucune solution n'a encore été trouvée.

    positionsvoulues = {}  # Prépare les positions souhaitées des cases.

    for i in range(3):  # Parcourt les lignes de la matrice objectif.
        for j in range(3):  # Parcourt les colonnes de la matrice objectif.
            positionsvoulues[matricevoulue[i, j]] = (i, j)  # Mémorise la position cible de chaque valeur.

    h_initial = H(ListeEtats[0], matricevoulue, positionsvoulues)  # Calcule l'heuristique de l'état initial.
    ListeFrontiere = [(h_initial, ordre, 0, 0)]  # Chaque entrée contient : f, ordre, indice de l'état et g enregistré.

    deplacements = [  # Définit les déplacements du vide dans votre ordre initial.
        ("gauche", 0, -1),  # Diminue la colonne de un.
        ("droite", 0, 1),  # Augmente la colonne de un.
        ("haut", -1, 0),  # Diminue la ligne de un.
        ("bas", 1, 0),  # Augmente la ligne de un.
    ]

    while ListeFrontiere:  # Continue tant qu'il reste une entrée à traiter.
        _, _, Current, cout_enregistre = heapq.heappop(ListeFrontiere)  # Retire le plus petit f de toute la frontière.

        if cout_enregistre != CoutsG[Current]:  # Repère une ancienne entrée remplacée par un meilleur chemin.
            continue  # Ignore cette entrée devenue inutile.

        it += 1  # Compte une nouvelle itération de recherche.
        explores.add(ListeEtats[Current].tobytes())  # Ajoute l'état aux états distincts examinés.
        mesures.append((it, len(explores)))  # Enregistre le numéro d'itération et la taille des états explorés.

        if np.array_equal(ListeEtats[Current], matricevoulue):  # Vérifie si l'état sélectionné est l'objectif.
            indice_solution = Current  # Retient l'indice réel de l'état solution.
            break  # Termine la recherche lorsque l'objectif est sélectionné.

        xinit, yinit = np.argwhere(ListeEtats[Current] == "*")[0]  # Repère les coordonnées du vide.

        for action, dx, dy in deplacements:  # Essaie les quatre déplacements possibles du vide.
            xsuivant, ysuivant = xinit + dx, yinit + dy  # Calcule la position après le déplacement.

            if not (0 <= xsuivant < 3 and 0 <= ysuivant < 3):  # Vérifie que cette position reste dans la grille.
                continue  # Ignore les déplacements hors de la grille.

            matriceetat = np.copy(ListeEtats[Current])  # Copie l'état courant pour créer un enfant.

            matriceetat[xinit, yinit], matriceetat[xsuivant, ysuivant] = (
                matriceetat[xsuivant, ysuivant],
                matriceetat[xinit, yinit],
            )  # Échange le vide avec la case voisine.

            cle = matriceetat.tobytes()  # Transforme la matrice en clé pour le dictionnaire.
            nouveau_g = CoutsG[Current] + 1  # Ajoute un déplacement au coût du chemin.

            if cle in indices:  # Vérifie si cette configuration est déjà connue.
                indice_enfant = indices[cle]  # Retrouve son indice.

                if nouveau_g >= CoutsG[indice_enfant]:  # Compare avec le meilleur coût déjà connu.
                    continue  # Ignore un chemin de même coût ou plus long.

                CoutsG[indice_enfant] = nouveau_g  # Enregistre le coût du meilleur chemin.
                parents[indice_enfant] = Current  # Met à jour le parent.
                actions[indice_enfant] = action  # Met à jour le déplacement depuis ce parent.

            else:  # Traite un état découvert pour la première fois.
                indice_enfant = len(ListeEtats)  # Détermine l'indice du nouvel état.
                indices[cle] = indice_enfant  # Associe la clé à cet indice.
                ListeEtats.append(matriceetat)  # Conserve la nouvelle matrice.
                CoutsG.append(nouveau_g)  # Conserve le coût du chemin jusqu'à cet état.
                parents.append(Current)  # Conserve l'indice du parent.
                actions.append(action)  # Conserve le déplacement effectué.

            h = H(matriceetat, matricevoulue, positionsvoulues)  # Estime le coût restant jusqu'à l'objectif.
            f = nouveau_g + h  # Calcule la priorité utilisée par A*.
            ordre += 1  # Attribue un numéro unique à cette entrée.
            heapq.heappush(ListeFrontiere, (f, ordre, indice_enfant, nouveau_g))  # Ajoute l'entrée à la file de priorité.

    temps_execution = time.perf_counter() - starttime  # Arrête le chronomètre avant l'écriture des résultats.

    with fichier_stats.open("w", encoding="utf-8") as output:  # Ouvre le fichier des mesures.
        for iteration, taille_explores in mesures:  # Parcourt les mesures de chaque itération.
            output.write(f"{iteration}\t{taille_explores}\n")  # Écrit les deux colonnes séparées par une tabulation.

        output.write(f"{it}\n")  # Écrit le total des états examinés sur l'avant-dernière ligne.
        output.write(f"{temps_execution:.9f}\n")  # Écrit le temps en secondes sur la dernière ligne.

    chemin = []  # Contiendra les indices des états du chemin solution.
    mouvements = None  # Indique par défaut qu'aucune solution n'a été trouvée.

    if indice_solution is not None:  # Reconstruit le chemin seulement si une solution existe.
        index_courant = indice_solution  # Commence à l'indice de l'état objectif.

        while index_courant is not None:  # Remonte jusqu'à l'état initial, dont le parent est None.
            chemin.append(index_courant)  # Ajoute l'indice de cet état au chemin inversé.
            index_courant = parents[index_courant]  # Passe à son parent.

        chemin.reverse()  # Replace les états dans l'ordre initial vers objectif.
        mouvements = [actions[indice] for indice in chemin[1:]]  # Récupère les déplacements sans inclure l'état initial.

    with fichier_solution.open("w", encoding="utf-8") as solution:  # Ouvre le fichier du bilan et du chemin.
        solution.write(f"A* - Exemple Ex1-{Ex} - Exécution {compteur}\n")  # Identifie cet essai.
        solution.write("H1 : nombre de cases mal placées, case vide exclue.\n")  # Décrit H1.
        solution.write("H2 : somme des distances de Manhattan, case vide exclue.\n")  # Décrit H2.
        solution.write("Heuristique utilisée : H3 = max(H1, H2). Pour ce puzzle, H3 = H2.\n")  # Précise H3.
        solution.write("Priorité de recherche : f(n) = g(n) + H3(n), coût de chaque mouvement = 1.\n")  # Décrit la priorité.
        solution.write(f"Nombre d'itérations : {it}\n")  # Écrit le nombre d'itérations.
        solution.write(f"Nombre d'états distincts explorés : {len(explores)}\n")  # Écrit le nombre d'états explorés différents.
        solution.write(f"Temps de recherche : {temps_execution:.9f} secondes\n")  # Écrit le temps mesuré.
        solution.write("Colonnes du fichier stats : itération TAB taille de l'ensemble des états explorés.\n\n")  # Explique les colonnes.

        if mouvements is None:  # Traite le cas sans solution.
            solution.write("Aucune solution : la frontière a été épuisée.\n")  # Enregistre la conclusion.

        else:  # Traite le cas où une solution existe.
            solution.write(f"Nombre de déplacements : {len(mouvements)}\n")  # Écrit le nombre de mouvements.
            solution.write(f"Nombre d'états dans le chemin : {len(chemin)}\n")  # Compte les états, état initial compris.
            solution.write(
                "Chemin du vide : "
                + (" -> ".join(mouvements) or "aucun déplacement")
                + "\n\n"
            )  # Écrit les directions successives.

            for etape, indice in enumerate(chemin):  # Parcourt chaque état du chemin.
                solution.write(f"Étape {etape}\n")  # Numérote l'étape à partir de zéro.

                for ligne in ListeEtats[indice]:  # Parcourt les trois lignes de la matrice.
                    solution.write("\t".join(ligne.tolist()) + "\n")  # Écrit les cases séparées par des tabulations.

                solution.write("\n")  # Sépare les matrices par une ligne vide.

    if mouvements is None:  # Affiche le résultat d'une recherche sans solution.
        print(f"Exécution {compteur} : aucune solution (frontière épuisée).")  # Informe l'utilisateur.

    else:  # Affiche le résultat d'une recherche réussie.
        print(f"Exécution {compteur} : solution trouvée !")  # Confirme la réussite.
        print(f"Nombre de déplacements : {len(mouvements)}")  # Affiche la longueur du chemin.
        print("Chemin du vide : " + (" -> ".join(mouvements) or "aucun déplacement"))  # Affiche les directions.

    print(f"Nombre d'itérations : {it}")  # Affiche le nombre d'états examinés.
    print(f"Nombre d'états distincts explorés : {len(explores)}")  # Affiche le nombre d'états explorés différents.
    print(f"Temps de recherche : {temps_execution:.4f} secondes")  # Affiche le temps de recherche.
    print(f"Mesures : {fichier_stats}")  # Indique le chemin du fichier des statistiques.
    print(f"Chemin et bilan : {fichier_solution}")  # Indique le chemin du fichier de la solution.

    return mouvements  # Retourne les déplacements, ou None si aucune solution n'existe.