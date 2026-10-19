from time import perf_counter  # Importe le chronomètre utilisé pour mesurer la recherche.

import numpy as np  # Permet de représenter les grilles et de traiter plusieurs individus ensemble.

from HillClimbing import BLOCS, valider_matrice  # Réutilise les coordonnées des blocs et la validation des Sudokus.


def evaluer_population(population):  # Calcule le coût de chaque individu d'un tableau de forme (nombre, 9, 9).
    """Retourne les coûts ; chaque grille doit être remplie et ses blocs valides.

Après le tri d'une unité, chaque égalité entre voisins est une répétition
en excès : cela donne exactement 9 - nombre de chiffres distincts.
"""
    lignes_triees = np.sort(population, axis=2)  # Trie une copie de chaque ligne de chaque grille.
    colonnes_triees = np.sort(population, axis=1)  # Trie une copie de chaque colonne de chaque grille.
    cout_lignes = np.sum(lignes_triees[:, :, 1:] == lignes_triees[:, :, :-1], axis=(1, 2))  # Compte les répétitions des lignes pour chaque individu.
    cout_colonnes = np.sum(colonnes_triees[:, 1:, :] == colonnes_triees[:, :-1, :], axis=(1, 2))  # Compte les répétitions des colonnes pour chaque individu.
    return cout_lignes + cout_colonnes  # Retourne un tableau d'un coût par individu, à minimiser.


def creer_population(base, preparations, nombre, aleatoire):  # Construit le nombre demandé de grilles complètes aléatoires.
    population = np.repeat(base[np.newaxis, :, :], nombre, axis=0)  # Crée une copie de la grille initiale pour chaque individu.
    for lignes, colonnes, manquants in preparations:  # Parcourt les cases libres et les chiffres manquants de chaque bloc.
        for individu in range(nombre):  # Prépare un remplissage indépendant pour chaque grille.
            population[individu, lignes, colonnes] = aleatoire.permutation(manquants)  # Répartit les chiffres manquants sans répétition dans le bloc.
    return population  # Retourne un tableau contenant toutes les matrices de la population.


def selectionner_parents(fitness, nombre, taille_tournoi, aleatoire):  # Sélectionne des parents en favorisant les individus ayant la meilleure fitness.
    candidats = aleatoire.integers(0, len(fitness), size=(nombre, taille_tournoi))  # Tire des candidats avec remise pour chaque tournoi.
    gagnants = np.argmax(fitness[candidats], axis=1)  # Trouve la position du candidat ayant la plus grande fitness dans chaque tournoi.
    return candidats[np.arange(nombre), gagnants]  # Retourne les indices des gagnants ; un individu peut gagner plusieurs tournois.


def croiser_et_muter(parents1, parents2, preparations, taux_mutation, aleatoire):  # Produit un enfant par paire de parents.
    enfants = parents1.copy()  # Commence chaque enfant avec une copie indépendante du premier parent.
    nombre = len(enfants)  # Retient le nombre d'enfants à construire.
    for br in (0, 3, 6):  # Parcourt les premières lignes des groupes de blocs.
        for bc in (0, 3, 6):  # Parcourt les premières colonnes des groupes de blocs.
            prendre_parent2 = aleatoire.random(nombre) < 0.5  # Choisit indépendamment le deuxième parent avec une probabilité de 50 % par bloc et par enfant.
            enfants[prendre_parent2, br:br + 3, bc:bc + 3] = parents2[prendre_parent2, br:br + 3, bc:bc + 3]  # Copie les blocs complets sélectionnés du deuxième parent.

    doublons_lignes = np.sum(enfants[:, :, :, None] == enfants[:, :, None, :], axis=3) > 1  # Repère les cases dont le chiffre se répète dans leur ligne après le croisement.
    colonnes = enfants.transpose(0, 2, 1)  # Présente temporairement chaque colonne comme une ligne pour effectuer le même comptage.
    doublons_colonnes = np.sum(colonnes[:, :, :, None] == colonnes[:, :, None, :], axis=3) > 1  # Repère les chiffres répétés dans les colonnes.
    conflits = doublons_lignes | doublons_colonnes.transpose(0, 2, 1)  # Repère les cases en conflit au début de la phase de mutation.
    for lignes, colonnes, manquants in preparations:  # Parcourt les cases modifiables de chaque bloc pour les mutations.
        nombre_libres = len(manquants)  # Compte les cases initialement vides de ce bloc.
        if nombre_libres < 2:  # Un échange nécessite au moins deux cases libres.
            continue  # Passe au bloc suivant si aucune permutation n'est possible.
        individus = np.flatnonzero(aleatoire.random(nombre) < taux_mutation)  # Sélectionne les enfants à muter dans ce bloc.
        priorites = conflits[individus[:, None], lignes[None, :], colonnes[None, :]].astype(float)  # Donne une priorité de 1 aux cases libres en conflit et de 0 aux autres.
        priorites += aleatoire.random(priorites.shape)  # Départage aléatoirement les cases de même priorité sans inverser la priorité des conflits.
        premiere = np.argmax(priorites, axis=1)  # Choisit une case libre en conflit s'il y en a une, sinon une case libre quelconque.
        seconde = aleatoire.integers(0, nombre_libres - 1, size=len(individus))  # Tire la deuxième case parmi une position de moins.
        seconde += seconde >= premiere  # Saute la première position pour garantir deux cases distinctes.
        valeurs = enfants[individus, lignes[premiere], colonnes[premiere]].copy()  # Sauvegarde les chiffres des premières cases avant les échanges.
        enfants[individus, lignes[premiere], colonnes[premiere]] = enfants[individus, lignes[seconde], colonnes[seconde]]  # Place les seconds chiffres dans les premières cases.
        enfants[individus, lignes[seconde], colonnes[seconde]] = valeurs  # Termine les échanges sans changer les chiffres donnés ni le contenu des blocs.
    return enfants  # Retourne les grilles obtenues après le croisement et les mutations.
def AlgoGenetic(matriceinitiale, *, graine=2026, taille_population=300, max_generations=5000,  # Reçoit la grille et les principaux paramètres de l'exécution.
                taux_mutation=0.15, taille_tournoi=3, nb_elites=5, patience=50):  # Configure la mutation, la sélection, l'élitisme et la stagnation.
    
    initiale = np.array(matriceinitiale, dtype=str, copy=True)  # Copie la matrice pour préserver l'entrée de l'utilisateur.
    valider_matrice(initiale)  # Vérifie les dimensions, les caractères et les chiffres donnés avant le chronométrage.
    if taille_population < 2 or max_generations < 0:  # Vérifie le nombre d'individus et la limite de générations.
        raise ValueError("Population >= 2 et générations >= 0.")  # Explique les valeurs acceptées.
    if not 1 <= nb_elites < taille_population:  # Exige au moins une élite tout en gardant une place pour les enfants.
        raise ValueError("Le nombre d'élites doit être compris entre 1 et population - 1.")  # Signale une configuration sans évolution possible.
    if not 2 <= taille_tournoi <= taille_population:  # Vérifie le nombre de candidats par tournoi.
        raise ValueError("La taille du tournoi doit être comprise entre 2 et la population.")  # Explique les valeurs autorisées.
    if not 0 <= taux_mutation <= 1 or patience < 0:  # Vérifie la probabilité de mutation et la limite de stagnation.
        raise ValueError("Mutation entre 0 et 1 ; patience >= 0.")  # Refuse les paramètres incohérents.
    if graine < 0:  # Le générateur aléatoire NumPy attend ici une graine entière non négative.
        raise ValueError("La graine doit être positive ou nulle.")  # Signale une graine non acceptée.
    debut = perf_counter()  # Démarre le chronométrage de la préparation et de la recherche.
    aleatoire = np.random.default_rng(graine)  # Crée le générateur qui rend les choix reproductibles avec la même configuration.
    fixes = initiale != "."  # Repère les cases contenant les chiffres donnés à conserver.
    base = np.where(fixes, initiale, "0").astype(np.int8)  # Prépare une copie numérique dont les cases vides valent 0.
    preparations = []  # Prépare les informations nécessaires pour remplir et muter les neuf blocs.
    for bloc in BLOCS:  # Parcourt chaque bloc 3 x 3 du Sudoku.
        libres = [(r, c) for r, c in bloc if not fixes[r, c]]  # Repère uniquement les cases initialement vides.
        lignes = np.array([r for r, c in libres], dtype=int)  # Conserve les indices de ligne de ces cases.
        colonnes = np.array([c for r, c in libres], dtype=int)  # Conserve les indices de colonne correspondants.
        presents = {int(base[r, c]) for r, c in bloc}  # Recense les chiffres donnés et éventuellement le 0 des cases vides.
        manquants = np.array([v for v in range(1, 10) if v not in presents], dtype=np.int8)  # Détermine les chiffres qui doivent compléter le bloc.
        preparations.append((lignes, colonnes, manquants))  # Enregistre les coordonnées libres et leurs chiffres possibles.

    population = creer_population(base, preparations, taille_population, aleatoire)  # Construit la population initiale de grilles complètes.
    couts = evaluer_population(population)  # Évalue chaque individu de la génération 0.
    evaluations = taille_population  # Compte les évaluations déjà effectuées, y compris la population initiale.
    indice = int(np.argmin(couts))  # Retrouve l'indice de l'individu ayant le coût le plus faible.
    meilleur_score = int(couts[indice])  # Initialise le meilleur coût de toute l'exécution.
    meilleure_matrice = population[indice].copy()  # Conserve une copie de la meilleure grille rencontrée.
    score_reference = meilleur_score  # Initialise le meilleur coût de la population depuis son dernier renouvellement.
    stagnation = 0  # Initialise le nombre de générations consécutives sans amélioration de ce coût.
    iterations = 0  # Aucune nouvelle génération n'a encore été produite après la population initiale.
    redemarrages = 0  # Aucun renouvellement aléatoire de la population n'a encore été effectué.

    while meilleur_score > 0 and iterations < max_generations:  # Continue jusqu'à une solution ou à l'épuisement du budget global.
        if patience > 0 and stagnation >= patience:  # Détecte une stagnation prolongée lorsque cette option est activée.
            population = creer_population(base, preparations, taille_population, aleatoire)  # Remplace la population par de nouvelles grilles aléatoires.
            redemarrages += 1  # Compte ce renouvellement complet ; la meilleure grille globale reste sauvegardée.
            score_reference = float("inf")  # Réinitialise la référence d'amélioration pour la nouvelle population.
            stagnation = 0  # Recommence le compteur de stagnation.
        else:  # Produit une génération ordinaire par sélection, croisement, mutation et élitisme.
            indices_elites = np.argsort(couts, kind="stable")[:nb_elites]  # Sélectionne les individus de plus faible coût en gardant un ordre stable en cas d'égalité.
            elites = population[indices_elites].copy()  # Copie les élites pour les conserver sans mutation.
            nombre_enfants = taille_population - nb_elites  # Détermine combien d'enfants compléteront la prochaine population.
            fitness = 1.0 / (1.0 + couts)  # Transforme le coût en qualité à maximiser ; une solution a une fitness de 1.
            parents = selectionner_parents(fitness, 2 * nombre_enfants, taille_tournoi, aleatoire)  # Organise deux tournois indépendants par enfant.
            parents1 = population[parents[:nombre_enfants]]  # Récupère le premier parent de chaque paire.
            parents2 = population[parents[nombre_enfants:]]  # Récupère le deuxième parent de chaque paire.
            enfants = croiser_et_muter(parents1, parents2, preparations, taux_mutation, aleatoire)  # Combine les parents et applique les mutations aléatoires.
            population = np.concatenate((elites, enfants), axis=0)  # Forme une nouvelle population de taille constante.

        couts = evaluer_population(population)  # Évalue toute la nouvelle population, y compris les élites conservées.
        evaluations += taille_population  # Ajoute le nombre de grilles évaluées à ce passage.
        iterations += 1  # Compte la génération ordinaire ou le renouvellement qui vient d'être évalué.
        indice = int(np.argmin(couts))  # Retrouve le meilleur individu de cette population.
        score_courant = int(couts[indice])  # Récupère son coût sous forme d'entier Python.
        if score_courant < score_reference:  # Détecte une amélioration depuis le dernier renouvellement.
            score_reference = score_courant  # Enregistre le nouveau coût de référence de cette population.
            stagnation = 0  # Annule le compteur de stagnation après cette amélioration.
        else:  # Traite une génération qui ne diminue pas le meilleur coût de référence.
            stagnation += 1  # Compte une génération supplémentaire sans amélioration.
        if score_courant < meilleur_score:  # Vérifie si cette grille améliore le record de toute l'exécution.
            meilleur_score = score_courant  # Mémorise le nouveau meilleur coût global.
            meilleure_matrice = population[indice].copy()  # Sauvegarde la grille correspondante indépendamment de la population.
    temps = perf_counter() - debut  # Arrête le chronomètre avant les vérifications finales et l'écriture des résultats.
    finale = meilleure_matrice.astype(str)  # Retourne au format NumPy de caractères utilisé par Partie_2.py.
    if meilleur_score == 0:  # Vérifie complètement toute grille annoncée comme solution.
        valider_matrice(finale, complete=True)  # Contrôle les lignes, les colonnes, les blocs et l'absence de cases vides.
    if not np.array_equal(finale[fixes], initiale[fixes]):  # Vérifie la conservation de tous les chiffres donnés.
        raise ValueError("Une case donnée a été modifiée : résultat invalide.")  # Refuse une grille qui changerait le problème initial.

    return {  # Regroupe les résultats d'une exécution pour le programme principal.
        "succes": meilleur_score == 0,  # Indique si une solution complète a été trouvée.
        "matrice": finale,  # Fournit la meilleure grille de l'exécution, éventuellement non résolue.
        "score": meilleur_score,  # Fournit le nombre de répétitions en excès dans les lignes et les colonnes.
        "fitness": 1.0 / (1.0 + meilleur_score),  # Fournit la qualité de la meilleure grille.
        "iterations": iterations,  # Fournit le nombre de générations évaluées après la population initiale.
        "evaluations": evaluations,  # Fournit le nombre total d'évaluations d'individus, répétitions comprises.
        "redemarrages": redemarrages,  # Fournit le nombre de renouvellements complets de la population.
        "temps": temps,  # Fournit la durée de préparation et de recherche en secondes.
        "graine": graine,  # Fournit la graine utilisée pour cet essai.
        "motif": "Solution trouvée" if meilleur_score == 0 else "Limite de générations atteinte",  # Précise pourquoi la recherche s'est arrêtée.
    }  # Termine le dictionnaire transmis à Partie_2.py
