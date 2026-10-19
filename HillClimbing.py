"""Recherche locale pour une matrice NumPy de Sudoku 9 x 9"""

from itertools import combinations  # Permet de former toutes les paires de cases modifiables d'un bloc.
from random import Random  # Fournit un générateur aléatoire dont les choix dépendent d'une graine.
from time import perf_counter  # Fournit un chronomètre précis pour mesurer la recherche.

import numpy as np  # Importe NumPy pour représenter et copier les matrices du Sudoku.


# Coordonnées des neuf cases de chacun des neuf blocs 3 x 3.
BLOCS = [  # Commence la liste qui contiendra les neuf blocs du Sudoku.
    [(r, c) for r in range(br, br + 3) for c in range(bc, bc + 3)]  # Énumère les neuf coordonnées du bloc courant.
    for br in (0, 3, 6)  # Choisit la première ligne du bloc : indice 0, 3 ou 6.
    for bc in (0, 3, 6)  # Choisit la première colonne du bloc : indice 0, 3 ou 6.
]  # Termine la liste des neuf blocs.


def valider_matrice(matrice, complete=False):  # Définit la vérification d'une entrée ou d'une solution complète.
    """Vérifie une matrice initiale ou une solution, avec '.' pour le vide."""
    if matrice.shape != (9, 9):  # Vérifie que la matrice possède exactement neuf lignes et neuf colonnes.
        raise ValueError("Le Sudoku doit avoir neuf lignes et neuf colonnes.")  # Signale des dimensions incorrectes.
    if not np.isin(matrice, list(".123456789")).all():  # Vérifie que chaque case contient un caractère autorisé.
        raise ValueError("Les cases doivent contenir les caractères 1 à 9 ou un point.")  # Refuse les autres caractères.
    if complete and np.any(matrice == "."):  # Lors du contrôle d'une solution, recherche une éventuelle case vide.
        raise ValueError("La solution contient encore des cases vides.")  # Refuse une solution incomplète.

    unites = [matrice[r, :] for r in range(9)]  # Place les neuf lignes parmi les unités à vérifier.
    unites += [matrice[:, c] for c in range(9)]  # Ajoute les neuf colonnes aux unités à vérifier.
    unites += [[matrice[r, c] for r, c in bloc] for bloc in BLOCS]  # Ajoute les neuf blocs 3 x 3.
    for unite in unites:  # Examine chaque ligne, chaque colonne et chaque bloc.
        chiffres = [v for v in unite if v != "."]  # Conserve les chiffres présents en ignorant les cases vides.
        if len(chiffres) != len(set(chiffres)):  # Un ensemble enlève les doublons : une différence de taille révèle une répétition.
            raise ValueError("Des chiffres donnés se répètent dans une ligne, une colonne ou un bloc.")  # Signale une règle violée.


def score_conflits(matrice):  # Définit le calcul du coût à diminuer pendant la recherche.
    """Coût d'une matrice remplie dont les blocs sont valides.

    Pour chaque ligne et colonne : 9 - nombre de chiffres différents.
    Les blocs restent valides pendant toute la recherche ; un coût nul
    correspond donc à un Sudoku entièrement résolu.
    """
    return sum(9 - len(set(matrice[r, :])) for r in range(9)) + sum(  # Additionne les répétitions en excès des neuf lignes.
        9 - len(set(matrice[:, c])) for c in range(9)  # Ajoute les répétitions en excès des neuf colonnes.
    )  # Termine le calcul et retourne le score total.


def _variation(compteurs, sortant, entrant):  # Calcule l'effet du remplacement d'un chiffre dans une ligne ou une colonne.
    """Calcule la variation du coût d'une ligne ou d'une colonne.

    Perdre un chiffre présent une seule fois augmente le coût de 1.
    Recevoir un chiffre absent diminue le coût de 1.
    Les deux chiffres sont différents : ils viennent d'un même bloc valide.
    """
    return int(compteurs[sortant] == 1) - int(compteurs[entrant] == 0)  # Retourne +1, 0 ou -1 selon l'effet sur le nombre de chiffres distincts.


def HillClimbing(matriceinitiale, *, graine=2026, max_iterations=100000,  # Reçoit la matrice ; les paramètres suivants sont fournis par leur nom.
                 max_redemarrages=1000, max_lateraux=50):  # Fixe les limites de redémarrages et d'échanges consécutifs à coût égal.
   
    initiale = np.array(matriceinitiale, dtype=str, copy=True)  # Copie l'entrée sous forme de caractères pour préserver la matrice reçue.
    valider_matrice(initiale)  # Vérifie les dimensions, les caractères et les chiffres donnés avant la recherche.
    if max_iterations < 1 or max_redemarrages < 0 or max_lateraux < 0:  # Refuse des limites incompatibles avec la recherche.
        raise ValueError("Itérations >= 1 ; redémarrages et mouvements latéraux >= 0.")  # Explique les valeurs permises.

    debut = perf_counter()  # Démarre la mesure du temps de préparation et de recherche.
    aleatoire = Random(graine)  # Initialise les choix aléatoires ; la même graine permet de reproduire l'essai.
    fixes = initiale != "."  # Crée un masque valant True pour chaque chiffre donné à conserver.
    # La recherche utilise une copie numérique NumPy ; les points deviennent des zéros.
    base = np.where(fixes, initiale, "0").astype(np.int8)  # Conserve les chiffres et transforme les cases vides en zéros entiers.

    preparations = []  # Prépare une liste associant les cases libres et les chiffres manquants de chaque bloc.
    echanges = []  # Prépare la liste de toutes les paires de cases qu'il sera permis d'échanger.
    for bloc in BLOCS:  # Parcourt les neuf blocs 3 x 3.
        libres = [(r, c) for r, c in bloc if not fixes[r, c]]  # Repère les cases initialement vides du bloc.
        presents = {int(base[r, c]) for r, c in bloc}  # Recense les valeurs déjà présentes, avec 0 pour le vide.
        manquants = [v for v in range(1, 10) if v not in presents]  # Détermine quels chiffres de 1 à 9 doivent compléter le bloc.
        preparations.append((libres, manquants))  # Mémorise les cases et leurs chiffres possibles pour les futurs remplissages.
        echanges.extend(combinations(libres, 2))  # Ajoute chaque paire de cases libres du bloc une seule fois.

    iterations = 0  # Initialise le nombre d'examens complets du voisinage.
    evaluations = 0  # Initialise le nombre total de grilles voisines évaluées.
    meilleur_score = float("inf")  # L'infini permet de retenir la première grille comme meilleure grille connue.
    meilleure_matrice = None  # Aucune grille remplie n'a encore été mémorisée.
    motif = "Limite de redémarrages atteinte"  # Prévoit le motif utilisé si tous les départs autorisés sont épuisés.

    # Le départ 0 est l'initialisation ; les suivants sont les redémarrages.
    for depart in range(max_redemarrages + 1):  # Autorise le premier remplissage, puis le nombre prévu de redémarrages.
        matrice = base.copy()  # Repart des chiffres donnés et des cases vides de la grille initiale.
        for libres, manquants in preparations:  # Récupère les informations préparées pour chaque bloc.
            valeurs = manquants[:]  # Copie les chiffres manquants pour préserver la liste de référence.
            aleatoire.shuffle(valeurs)  # Mélange leur ordre pour obtenir un remplissage aléatoire du bloc.
            for (r, c), valeur in zip(libres, valeurs):  # Associe chaque case libre à l'un des chiffres mélangés.
                matrice[r, c] = valeur  # Remplit la case sans toucher aux chiffres donnés.

        # Compteurs d'occurrences : lignes[r][v] = nombre de v dans la ligne r.
        # Ils servent à évaluer un échange sans recopier toute la matrice.
        lignes = [[0] * 10 for _ in range(9)]  # Crée les compteurs des chiffres 1 à 9 pour chaque ligne ; l'indice 0 est inutilisé.
        colonnes = [[0] * 10 for _ in range(9)]  # Crée les mêmes compteurs pour les neuf colonnes.
        for r in range(9):  # Parcourt les lignes de la grille remplie.
            for c in range(9):  # Parcourt les colonnes de la ligne courante.
                valeur = int(matrice[r, c])  # Récupère le chiffre de la case comme entier Python.
                lignes[r][valeur] += 1  # Compte une occurrence de ce chiffre dans sa ligne.
                colonnes[c][valeur] += 1  # Compte une occurrence de ce chiffre dans sa colonne.
        score = score_conflits(matrice)  # Évalue les conflits du nouveau remplissage.
        lateraux = 0  # Recommence le compteur d'échanges consécutifs à coût égal.
        if score < meilleur_score:  # Vérifie si ce remplissage améliore le meilleur résultat de toute l'exécution.
            meilleur_score = score  # Mémorise le nouveau meilleur score.
            meilleure_matrice = matrice.copy()  # Conserve une copie indépendante de la grille correspondante.

        if score == 0:  # Vérifie si le remplissage obtenu est déjà une solution.
            motif = "Solution trouvée"  # Enregistre la raison de l'arrêt.
            break  # Quitte la boucle des départs puisque le Sudoku est résolu.
        if not echanges:  # Vérifie s'il existe au moins deux cases modifiables dans un même bloc.
            motif = "Aucun échange possible entre cases modifiables"  # Explique pourquoi la recherche ne peut pas progresser.
            break  # Termine la boucle des départs faute de voisins accessibles par un échange.

        while iterations < max_iterations:  # Poursuit la recherche tant que le budget global d'itérations le permet.
            meilleure_variation = float("inf")  # Réinitialise la meilleure variation pour examiner les voisins de l'état courant.
            meilleurs_echanges = []  # Prépare la liste des échanges donnant cette meilleure variation.
            for (r1, c1), (r2, c2) in echanges:  # Examine chaque paire de cases modifiables appartenant au même bloc.
                a, b = int(matrice[r1, c1]), int(matrice[r2, c2])  # Lit les deux chiffres qui seraient échangés.
                variation = 0  # Commence le calcul de l'effet total de cet échange sur le coût.
                if r1 != r2:  # Calcule un effet sur les lignes seulement si les deux cases sont dans des lignes différentes.
                    variation += _variation(lignes[r1], a, b) + _variation(lignes[r2], b, a)  # Additionne les effets sur les deux lignes.
                if c1 != c2:  # Calcule un effet sur les colonnes seulement si les deux cases sont dans des colonnes différentes.
                    variation += _variation(colonnes[c1], a, b) + _variation(colonnes[c2], b, a)  # Additionne les effets sur les deux colonnes.
                if variation < meilleure_variation:  # Vérifie si cet échange est meilleur que ceux déjà examinés.
                    meilleure_variation = variation  # Retient la nouvelle meilleure variation du coût.
                    meilleurs_echanges = [((r1, c1), (r2, c2))]  # Remplace les anciens candidats par cet échange.
                elif variation == meilleure_variation:  # Détecte un autre échange donnant un résultat aussi bon.
                    meilleurs_echanges.append(((r1, c1), (r2, c2)))  # Conserve ce candidat pour le départage aléatoire.

            iterations += 1  # Compte l'examen complet du voisinage, même s'il conduit à un blocage.
            evaluations += len(echanges)  # Ajoute le nombre de voisins examinés pendant cette itération.
            if meilleure_variation > 0:  # Détecte un minimum local où tous les échanges augmenteraient les conflits.
                break  # Quitte la recherche courante pour permettre un nouveau départ.
            if meilleure_variation == 0 and lateraux >= max_lateraux:  # Détecte un plateau dont la limite de déplacements est atteinte.
                break  # Quitte la recherche courante pour permettre un nouveau remplissage.

            (r1, c1), (r2, c2) = aleatoire.choice(meilleurs_echanges)  # Choisit au hasard parmi les meilleurs échanges.
            a, b = int(matrice[r1, c1]), int(matrice[r2, c2])  # Récupère les valeurs avant de les permuter.
            matrice[r1, c1], matrice[r2, c2] = b, a  # Effectue l'échange en conservant les chiffres du bloc.
            if r1 != r2:  # Met à jour les compteurs des lignes si l'échange concerne deux lignes.
                lignes[r1][a] -= 1  # Retire une occurrence de a dans la première ligne.
                lignes[r1][b] += 1  # Ajoute une occurrence de b dans la première ligne.
                lignes[r2][b] -= 1  # Retire une occurrence de b dans la deuxième ligne.
                lignes[r2][a] += 1  # Ajoute une occurrence de a dans la deuxième ligne.
            if c1 != c2:  # Met à jour les compteurs des colonnes si l'échange concerne deux colonnes.
                colonnes[c1][a] -= 1  # Retire une occurrence de a dans la première colonne.
                colonnes[c1][b] += 1  # Ajoute une occurrence de b dans la première colonne.
                colonnes[c2][b] -= 1  # Retire une occurrence de b dans la deuxième colonne.
                colonnes[c2][a] += 1  # Ajoute une occurrence de a dans la deuxième colonne.
            score += meilleure_variation  # Actualise le coût de la grille après l'échange.
            lateraux = lateraux + 1 if meilleure_variation == 0 else 0  # Compte un déplacement sur le plateau ou remet le compteur à zéro après une amélioration.

            if score < meilleur_score:  # Vérifie si l'état courant est le meilleur rencontré, tous départs confondus.
                meilleur_score = score  # Enregistre le meilleur coût atteint.
                meilleure_matrice = matrice.copy()  # Sauvegarde la grille avant les prochains échanges.
            if score == 0:  # Vérifie si les lignes et les colonnes sont maintenant sans conflits.
                motif = "Solution trouvée"  # Enregistre la réussite de la recherche.
                break  # Quitte la boucle d'itérations du départ courant.

        if score == 0:  # Vérifie, après la boucle interne, si une solution a été trouvée.
            break  # Termine aussi la boucle des départs.
        if iterations >= max_iterations:  # Vérifie si le budget commun à tous les départs est épuisé.
            motif = "Limite d'itérations atteinte"  # Distingue cet arrêt d'une réussite ou d'une limite de redémarrages.
            break  # Termine l'exécution sans lancer un autre départ.

    temps = perf_counter() - debut  # Mesure la durée totale de préparation et de recherche.
    finale = meilleure_matrice.astype(str)  # Reconvertit la meilleure grille en matrice NumPy de caractères.
    if meilleur_score == 0:  # Effectue une vérification complète lorsqu'une solution est annoncée.
        valider_matrice(finale, complete=True)  # Vérifie les lignes, les colonnes, les blocs et l'absence de cases vides.
    if not np.array_equal(finale[fixes], initiale[fixes]):  # Vérifie que tous les chiffres donnés ont été conservés.
        raise ValueError("Une case donnée a été modifiée : résultat invalide.")  # Refuse un résultat qui modifierait l'énoncé du Sudoku.

    return {  # Retourne les résultats de cette exécution à Partie_2.py.
        "succes": meilleur_score == 0,  # Indique True si une solution a été trouvée, sinon False.
        "matrice": finale,  # Fournit la meilleure grille, qui peut rester non résolue si une limite a été atteinte.
        "score": meilleur_score,  # Fournit le coût de cette meilleure grille.
        "iterations": iterations,  # Fournit le nombre cumulé d'examens du voisinage.
        "evaluations": evaluations,  # Fournit le nombre cumulé de voisins évalués.
        "redemarrages": depart,  # Fournit le nombre de redémarrages effectués ; le départ initial porte le numéro 0.
        "temps": temps,  # Fournit la durée de recherche en secondes.
        "graine": graine,  # Fournit la graine utilisée pour pouvoir reproduire les choix aléatoires.
        "motif": motif,  # Fournit la raison exacte de l'arrêt.
    }  
