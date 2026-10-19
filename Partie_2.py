import argparse  # Permet de choisir l'entrée, le nombre d'essais et les limites dans la commande.
import sys  # Permet d'afficher les erreurs et de retourner un code de sortie au système.
from pathlib import Path  # Permet de construire des chemins à partir du dossier du programme.

import numpy as np  # Importe NumPy pour représenter le Sudoku comme une matrice.

from HillClimbing import HillClimbing, valider_matrice  # Importe la recherche et la vérification des grilles.
from Algo_Genetic import AlgoGenetic  # Importe la recherche par population pour le Sudoku.

count = 1  # Initialise le numéro d'exécution ; ce compteur est différent des itérations de recherche.
Ex = 3  # Choisit Input_3.txt lorsque la commande ne fournit aucun numéro.
matriceinitiale = np.array([])  # Prépare une matrice vide qui sera remplie pendant l'initialisation.
metadonnees = {}  # Prépare le dictionnaire des informations QQWing associées au Sudoku.
RACINE = Path(__file__).resolve().parent  # Retrouve le dossier contenant ce fichier Python.


def initialiser_application():  # Définit le chargement de l'entrée sélectionnée et de ses métadonnées.
    """Conserve votre lecture du format QQWing et construit la matrice NumPy."""
    global matriceinitiale, metadonnees  # Autorise la fonction à remplir les variables communes au programme.
    print("Initialisation des composants...")  # Annonce le début du chargement.
    fichier = RACINE / "input-partie2" / f"Input_{Ex}.txt"  # Construit le chemin du fichier correspondant à Ex.
    with fichier.open("r", encoding="utf-8-sig") as f:  # Ouvre le fichier en lecture et accepte un éventuel marqueur BOM.
        JeuInitiale = f.read()  # Lit tout le fichier dans une chaîne de caractères.
    print("Contenu du fichier exemple du jeu :")  # Annonce l'affichage du fichier d'entrée.
    print(JeuInitiale)  # Affiche la grille et les informations QQWing originales.

    # Vos positions correspondent au format exact des dix fichiers fournis.
    if len(JeuInitiale) < 254:  # Vérifie que le texte contient au moins les positions utilisées jusqu'à l'indice 253.
        raise ValueError("Le fichier est trop court pour le format QQWing utilisé.")  # Signale une entrée trop courte.
    matriceinitiale = np.array([  # Commence la construction de la matrice NumPy 9 x 9.
        [JeuInitiale[1], JeuInitiale[3], JeuInitiale[5], JeuInitiale[9], JeuInitiale[11], JeuInitiale[13],  # Lit les colonnes 1 à 6 de la première ligne.
         JeuInitiale[17], JeuInitiale[19], JeuInitiale[21]],  # Termine la première ligne avec les colonnes 7 à 9.
        [JeuInitiale[24], JeuInitiale[26], JeuInitiale[28], JeuInitiale[32], JeuInitiale[34], JeuInitiale[36],  # Lit les colonnes 1 à 6 de la deuxième ligne.
         JeuInitiale[40], JeuInitiale[42], JeuInitiale[44]],  # Termine la deuxième ligne avec les colonnes 7 à 9.
        [JeuInitiale[47], JeuInitiale[49], JeuInitiale[51], JeuInitiale[55], JeuInitiale[57], JeuInitiale[59],  # Lit les colonnes 1 à 6 de la troisième ligne.
         JeuInitiale[63], JeuInitiale[65], JeuInitiale[67]],  # Termine la troisième ligne avec les colonnes 7 à 9.
        [JeuInitiale[94], JeuInitiale[96], JeuInitiale[98], JeuInitiale[102], JeuInitiale[104], JeuInitiale[106],  # Lit les colonnes 1 à 6 de la quatrième ligne en sautant le séparateur du fichier.
         JeuInitiale[110], JeuInitiale[112], JeuInitiale[114]],  # Termine la quatrième ligne avec les colonnes 7 à 9.
        [JeuInitiale[117], JeuInitiale[119], JeuInitiale[121], JeuInitiale[125], JeuInitiale[127], JeuInitiale[129],  # Lit les colonnes 1 à 6 de la cinquième ligne.
         JeuInitiale[133], JeuInitiale[135], JeuInitiale[137]],  # Termine la cinquième ligne avec les colonnes 7 à 9.
        [JeuInitiale[140], JeuInitiale[142], JeuInitiale[144], JeuInitiale[148], JeuInitiale[150], JeuInitiale[152],  # Lit les colonnes 1 à 6 de la sixième ligne.
         JeuInitiale[156], JeuInitiale[158], JeuInitiale[160]],  # Termine la sixième ligne avec les colonnes 7 à 9.
        [JeuInitiale[187], JeuInitiale[189], JeuInitiale[191], JeuInitiale[195], JeuInitiale[197], JeuInitiale[199],  # Lit les colonnes 1 à 6 de la septième ligne en sautant le deuxième séparateur.
         JeuInitiale[203], JeuInitiale[205], JeuInitiale[207]],  # Termine la septième ligne avec les colonnes 7 à 9.
        [JeuInitiale[210], JeuInitiale[212], JeuInitiale[214], JeuInitiale[218], JeuInitiale[220], JeuInitiale[222],  # Lit les colonnes 1 à 6 de la huitième ligne.
         JeuInitiale[226], JeuInitiale[228], JeuInitiale[230]],  # Termine la huitième ligne avec les colonnes 7 à 9.
        [JeuInitiale[233], JeuInitiale[235], JeuInitiale[237], JeuInitiale[241], JeuInitiale[243], JeuInitiale[245],  # Lit les colonnes 1 à 6 de la neuvième ligne.
         JeuInitiale[249], JeuInitiale[251], JeuInitiale[253]],  # Termine la neuvième ligne avec les colonnes 7 à 9.
    ])  # Termine la matrice ; les chiffres restent des caractères et les vides restent des points.
    valider_matrice(matriceinitiale)  # Vérifie le format de la matrice et les règles applicables aux chiffres donnés.

    metadonnees = {}  # Réinitialise les métadonnées pour le fichier qui vient d'être lu.
    for ligne in JeuInitiale.splitlines():  # Parcourt séparément chaque ligne du texte original.
        if ":" in ligne:  # Repère les lignes de métadonnées, comme Difficulty: Easy.
            cle, valeur = ligne.split(":", 1)  # Sépare le nom de l'information et sa valeur au premier deux-points.
            metadonnees[cle.strip()] = valeur.strip()  # Retire les espaces aux extrémités et conserve l'information.
    if not metadonnees.get("Difficulty"):  # Vérifie que le niveau de difficulté est présent et renseigné.
        raise ValueError("La métadonnée QQWing 'Difficulty' est absente.")  # Signale l'absence du niveau demandé pour l'évaluation.
    if "Number of Givens" in metadonnees:  # Vérifie le nombre de chiffres donnés lorsque QQWing le fournit.
        if int(metadonnees["Number of Givens"]) != int(np.count_nonzero(matriceinitiale != ".")):  # Compare la métadonnée au nombre réel de cases remplies.
            raise ValueError("Le nombre de chiffres donnés ne correspond pas aux métadonnées.")  # Signale une incohérence dans le fichier.
    print("Matrice initiale :")  # Annonce l'affichage de la matrice construite.
    print(matriceinitiale)  # Affiche les neuf lignes de la matrice NumPy.


def texte_matrice(matrice):  # Convertit une matrice en texte pour les fichiers de résultats.
    """Prépare une grille lisible pour les fichiers de résultats."""
    lignes = []  # Prépare la liste des lignes de texte à produire.
    for r in range(9):  # Parcourt les neuf lignes de la matrice.
        if r in (3, 6):  # Repère le début de la quatrième et de la septième ligne.
            lignes.append("------+-------+------")  # Ajoute un séparateur horizontal entre les groupes de blocs.
        groupes = [" ".join(str(v) for v in matrice[r, c:c + 3]) for c in (0, 3, 6)]  # Forme les trois groupes de trois cases de la ligne.
        lignes.append(" | ".join(groupes))  # Sépare les groupes par des barres verticales.
    return "\n".join(lignes)  # Assemble les lignes avec des retours à la ligne et retourne le texte.
def enregistrer_resultats(resultat, compteur, parametres, algorithme):  # Enregistre les mesures et la grille d'un essai de la méthode choisie.
    """Écrit deux fichiers par essai, dans le dossier de l'algorithme choisi."""
    dossier = RACINE / "output_partie2" / algorithme / f"Input_{Ex}"  # Choisit hill ou genetique pour ranger les résultats de chaque méthode.
    dossier.mkdir(parents=True, exist_ok=True)  # Crée le dossier de résultats s'il n'existe pas encore.
    fichier_stats = dossier / f"execution_{compteur:02d}_stats.txt"  # Nomme le fichier des mesures avec un numéro à deux chiffres.
    fichier_grille = dossier / f"execution_{compteur:02d}_grille.txt"  # Nomme le fichier contenant la grille initiale et la meilleure grille.
    statut = "SOLUTION TROUVEE" if resultat["succes"] else "SOLUTION NON TROUVEE DANS LES LIMITES"  # Distingue une réussite d'un arrêt sans solution.

    if algorithme == "hill":  # Prépare la description des essais de recherche locale.
        nom = "Hill climbing avec mouvements lateraux et redemarrages aleatoires"  # Identifie la variante utilisée.
        details = [  # Prépare les paramètres et la définition des mesures du Hill climbing.
            f"Limite globale d'iterations : {parametres['max_iterations']}",  # Enregistre le budget commun à tous les redémarrages.
            f"Limite de redemarrages : {parametres['max_redemarrages']}",  # Enregistre la limite des nouveaux départs.
            f"Limite de mouvements lateraux consecutifs : {parametres['max_lateraux']}",  # Enregistre la limite des échanges à coût égal.
            "Une iteration examine tout le voisinage et effectue au plus un echange.",  # Définit précisément une itération de cette méthode.
            "Les iterations et le temps incluent les redemarrages de cette execution.",  # Précise que les redémarrages ne réinitialisent pas les mesures.
        ]  # Termine les informations propres au Hill climbing.
        mesures = [  # Prépare les compteurs propres à la recherche locale.
            f"Nombre de redemarrages effectues : {resultat['redemarrages']}",  # Conserve le nombre de nouveaux départs effectués.
            f"Nombre de voisins evalues : {resultat['evaluations']}",  # Conserve le nombre de voisins examinés.
        ]  # Termine la liste des compteurs du Hill climbing.
    else:  # Prépare la description des essais génétiques.
        nom = "Algorithme genetique avec elitisme et renouvellements en cas de stagnation"  # Identifie la variante génétique utilisée.
        details = [  # Prépare les paramètres et les opérateurs nécessaires à l'analyse du génétique.
            f"Taille de population : {parametres['taille_population']}",  # Enregistre le nombre de grilles dans une population.
            f"Limite globale de generations : {parametres['max_generations']}",  # Enregistre le budget de générations, renouvellements compris.
            f"Taille du tournoi : {parametres['taille_tournoi']}",  # Enregistre le nombre de candidats tirés par sélection d'un parent.
            f"Nombre d'elites : {parametres['nb_elites']}",  # Enregistre le nombre d'individus conservés dans une génération ordinaire.
            f"Probabilite de mutation par bloc et par enfant : {parametres['taux_mutation']}",  # Précise l'unité à laquelle s'applique le taux de mutation.
            f"Patience avant renouvellement : {parametres['patience']} (0 = desactive)",  # Enregistre la limite de générations sans amélioration.
            "Cout : somme de (9 - nombre de chiffres distincts) sur les lignes et colonnes.",  # Définit le même coût que pour le Hill climbing.
            "Fitness : 1 / (1 + cout), a maximiser ; une solution a une fitness de 1.",  # Décrit la fonction de qualité utilisée pour la sélection.
            "Selection : tournoi avec remise ; le candidat de meilleure fitness gagne.",  # Décrit le choix des parents.
            "Croisement : chaque bloc 3 x 3 vient de l'un des deux parents, avec probabilite 1/2.",  # Décrit le croisement qui conserve des blocs valides.
            "Mutation : echange de deux cases initialement vides dans un meme bloc.",  # Décrit la modification aléatoire appliquée aux enfants.
            "Premiere case : priorite aux conflits apres croisement ; seconde case : aleatoire et distincte.",  # Décrit le choix des cases de chaque mutation.
            "Une mutation est appliquee meme si elle augmente le cout.",  # Précise que la mutation n'est pas une recherche du meilleur voisin.
            "Les chiffres donnes restent fixes ; les blocs restent valides.",  # Précise les contraintes conservées par les opérateurs.
            "Elitisme : les meilleures grilles passent intactes a chaque generation ordinaire.",  # Explique la conservation des meilleurs individus.
            "Stagnation : population entierement renouvelee ; meilleur resultat global conserve a part.",  # Explique comment la recherche retrouve de la diversité.
            "Une iteration construit et evalue une nouvelle population, renouvellements compris.",  # Définit ce que compte une itération génétique.
            "La population initiale est la generation 0 ; son evaluation est comprise dans le temps.",  # Explique le traitement de la première population.
            "Tous les individus sont evalues a chaque generation, y compris les elites.",  # Précise le sens du compteur d'évaluations.
        ]  # Termine les informations propres à l'algorithme génétique.
        mesures = [  # Prépare les mesures propres à la recherche génétique.
            f"Fitness de la meilleure grille : {resultat['fitness']:.9f}",  # Enregistre la qualité de la meilleure grille obtenue.
            f"Nombre de renouvellements de population : {resultat['redemarrages']}",  # Enregistre le nombre de populations aléatoires recréées après stagnation.
            f"Nombre d'evaluations d'individus : {resultat['evaluations']}",  # Enregistre les évaluations de grilles, répétitions comprises.
        ]  # Termine la liste des mesures propres au génétique.

    lignes = [  # Assemble le contenu commun du fichier de statistiques.
        f"Algorithme : {nom}",  # Identifie la méthode et sa variante.
        f"Fichier : Input_{Ex}.txt",  # Identifie la grille initiale utilisée.
        f"Execution : {compteur}",  # Identifie le numéro de l'essai.
        "",  # Sépare visuellement les parties du fichier.
        "Metadonnees QQWing de l'entree (distinctes des mesures de notre recherche) :",  # Évite de confondre les mesures QQWing et celles de nos algorithmes.
        *[f"{cle}: {valeur}" for cle, valeur in metadonnees.items()],  # Recopie les métadonnées originales de l'entrée.
        "",  # Insère une séparation avant les paramètres de recherche.
        "Parametres et fonctionnement de notre recherche :",  # Introduit les réglages de cet essai.
        f"Graine aleatoire : {resultat['graine']}",  # Conserve la graine pour reproduire cet essai.
        *details,  # Insère les paramètres et les définitions propres à l'algorithme.
        "Le temps inclut la preparation et la recherche ; il exclut lecture, affichage et ecriture.",  # Précise le périmètre du chronométrage.
        "",  # Sépare les paramètres des résultats mesurés.
        f"Resultat : {statut}",  # Enregistre la réussite ou l'arrêt sans solution.
        f"Motif d'arret : {resultat['motif']}",  # Enregistre la raison exacte de la fin de recherche.
        f"Meilleur score de conflits : {resultat['score']}",  # Enregistre le coût de la meilleure grille.
        *mesures,  # Insère les compteurs propres à la méthode choisie.
        f"Nombre d'iterations : {resultat['iterations']}",  # Enregistre les examens du voisinage ou les générations selon la méthode.
        f"Temps d'execution (secondes) : {resultat['temps']:.9f}",  # Enregistre la durée de recherche avec neuf décimales.
    ]  # Termine la préparation du texte des statistiques.
    fichier_stats.write_text("\n".join(lignes) + "\n", encoding="utf-8")  # Écrit les mesures après l'arrêt du chronomètre.

    titre = "Matrice solution" if resultat["succes"] else "Meilleure matrice obtenue (non resolue)"  # Distingue une solution d'une grille encore en conflit.
    texte = (  # Prépare le fichier contenant les matrices.
        f"Algorithme : {nom}\nFichier : Input_{Ex}.txt\nDifficulty: {metadonnees['Difficulty']}\n"  # Identifie l'algorithme, l'entrée et sa difficulté.
        f"Graine : {resultat['graine']}\nResultat : {statut}\n"  # Enregistre la graine et le statut de l'essai.
        f"Score de conflits : {resultat['score']}\n\n"  # Indique le coût de la grille retournée.
        f"Matrice initiale :\n{texte_matrice(matriceinitiale)}\n\n"  # Affiche la grille initiale avec ses cases vides.
        f"{titre} :\n{texte_matrice(resultat['matrice'])}\n"  # Affiche la meilleure grille trouvée pendant l'essai.
    )  # Termine la construction du texte des matrices.
    if not resultat["succes"]:  # Ajoute une précision lorsqu'aucune solution n'a été trouvée dans le budget.
        texte += "\nCet arret ne prouve pas que le Sudoku est sans solution.\n"  # Évite de présenter une limite de recherche comme une preuve d'insolubilité.
    fichier_grille.write_text(texte, encoding="utf-8")  # Enregistre les matrices dans le dossier de la méthode choisie.
    return fichier_stats, fichier_grille  # Retourne les chemins pour les afficher dans le terminal.
def main():  # Organise le choix de la méthode et les exécutions sur un Sudoku.
    """Exécute dix essais par défaut ; les anciennes commandes lancent Hill climbing."""
    global count, Ex  # Permet de choisir l'entrée et de réinitialiser le compteur d'essais.
    parser = argparse.ArgumentParser(description="Partie 2 : Hill climbing ou algorithme genetique sur un Sudoku.")  # Prépare l'aide et la lecture des arguments.
    parser.add_argument("exemple", nargs="?", type=int, choices=range(1, 11), default=Ex)  # Choisit Input_1 à Input_10 ; conserve Input_3 comme valeur par défaut.
    parser.add_argument("--algo", choices=("hill", "genetique"), default="hill", help="methode a lancer (hill par defaut)")  # Ajoute le choix explicite de l'algorithme.
    parser.add_argument("--executions", type=int, default=10, help="nombre d'essais")  # Choisit combien de fois exécuter la méthode sur cette grille.
    parser.add_argument("--graine", type=int, default=2026, help="graine du premier essai")  # Choisit la première graine de la série.
    parser.add_argument("--max-iterations", type=int, default=100000, help="hill : budget global d'iterations")  # Conserve la limite utilisée pour le Hill climbing.
    parser.add_argument("--max-redemarrages", type=int, default=1000, help="hill : limite de redemarrages")  # Conserve la limite des nouveaux départs du Hill climbing.
    parser.add_argument("--max-lateraux", type=int, default=50, help="hill : limite de mouvements lateraux consecutifs")  # Conserve le réglage des plateaux du Hill climbing.
    parser.add_argument("--population", type=int, default=300, help="genetique : nombre d'individus")  # Fixe le nombre de grilles évoluant ensemble.
    parser.add_argument("--max-generations", type=int, default=5000, help="genetique : budget global de generations")  # Fixe une limite qui inclut les renouvellements de population.
    parser.add_argument("--mutation", type=float, default=0.15, help="genetique : probabilite de mutation par bloc et par enfant")  # Fixe la fréquence des échanges aléatoires.
    parser.add_argument("--tournoi", type=int, default=3, help="genetique : candidats par tournoi")  # Fixe la pression de sélection des parents.
    parser.add_argument("--elites", type=int, default=5, help="genetique : individus conserves sans modification")  # Fixe le nombre d'élites des générations ordinaires.
    parser.add_argument("--patience", type=int, default=50, help="genetique : stagnation avant renouvellement (0 = desactive)")  # Fixe le nombre de générations sans amélioration avant un nouveau départ.
    arguments = parser.parse_args()  # Lit les arguments saisis dans le terminal.
    if arguments.executions < 1:  # Refuse une série sans essai.
        parser.error("Le nombre d'executions doit etre positif.")  # Affiche le problème et quitte le programme.
    Ex = arguments.exemple  # Retient le numéro de grille pour l'initialisation.

    if arguments.algo == "hill":  # Prépare une série de recherches locales.
        fonction = HillClimbing  # Choisit la fonction déjà utilisée pour vos premiers tests.
        nom = "Hill Climbing"  # Prépare le nom à afficher dans le terminal.
        parametres = {  # Regroupe les paramètres du Hill climbing.
            "max_iterations": arguments.max_iterations,  # Transmet le budget total d'examens du voisinage.
            "max_redemarrages": arguments.max_redemarrages,  # Transmet la limite des redémarrages.
            "max_lateraux": arguments.max_lateraux,  # Transmet la limite des mouvements latéraux.
        }  # Termine la configuration de la recherche locale.
    else:  # Prépare une série de recherches génétiques.
        fonction = AlgoGenetic  # Choisit la fonction qui fait évoluer une population de grilles.
        nom = "Algorithme genetique"  # Prépare le nom à afficher pour cette méthode.
        parametres = {  # Regroupe les paramètres de l'algorithme génétique.
            "taille_population": arguments.population,  # Transmet le nombre d'individus.
            "max_generations": arguments.max_generations,  # Transmet le budget de nouvelles générations.
            "taux_mutation": arguments.mutation,  # Transmet la probabilité de mutation par bloc et par enfant.
            "taille_tournoi": arguments.tournoi,  # Transmet le nombre de candidats par sélection d'un parent.
            "nb_elites": arguments.elites,  # Transmet le nombre de meilleurs individus conservés.
            "patience": arguments.patience,  # Transmet la limite de stagnation avant renouvellement.
        }  # Termine la configuration de l'algorithme génétique.

    try:  # Gère les erreurs de fichier, de grille et de paramètres.
        initialiser_application()  # Charge le même fichier d'entrée pour tous les essais de cette commande.
        print("Application en cours d'execution.")  # Annonce le début des recherches.
        print(f"Algorithme : {nom} | Nombre d'executions : {arguments.executions}")  # Affiche la méthode et le nombre de répétitions.
        print(f"Parametres par execution : {parametres}")  # Affiche les réglages réellement transmis à la recherche.
        count = 1  # Recommence la numérotation à 1 pour la série choisie.
        solutions = 0  # Initialise le nombre d'essais réussis.
        while count <= arguments.executions:  # Répète la méthode jusqu'au nombre d'essais demandé.
            graine = arguments.graine + count - 1  # Utilise des graines successives pour des essais différents et reproductibles.
            print(f"\nExecution {nom} #{count} - Input_{Ex}.txt - graine {graine}", flush=True)  # Affiche immédiatement le début de l'essai.
            resultat = fonction(matriceinitiale, graine=graine, **parametres)  # Appelle uniquement la méthode sélectionnée avec sa configuration.
            fichier_stats, fichier_grille = enregistrer_resultats(resultat, count, parametres, arguments.algo)  # Enregistre les mesures dans le dossier de cette méthode.
            solutions += int(resultat["succes"])  # Compte les recherches qui ont obtenu un coût nul.
            print(resultat["motif"])  # Affiche une réussite ou la limite ayant arrêté la recherche.
            if not resultat["succes"]:  # Précise le sens d'un essai sans solution.
                print("Solution non trouvee dans ces limites ; cela ne signifie pas que le Sudoku est insoluble.")  # Évite toute conclusion incorrecte sur la grille initiale.
            print(f"Meilleur score de conflits : {resultat['score']}")  # Affiche le coût de la meilleure grille trouvée.
            if arguments.algo == "hill":  # Affiche les compteurs de la recherche locale.
                print(f"Nombre d'iterations : {resultat['iterations']}")  # Affiche le nombre d'examens du voisinage.
                print(f"Nombre de redemarrages : {resultat['redemarrages']}")  # Affiche le nombre de nouveaux remplissages.
            else:  # Affiche les compteurs de la recherche génétique.
                print(f"Meilleure fitness : {resultat['fitness']:.6f}")  # Affiche la qualité à maximiser ; 1 indique une solution.
                print(f"Nombre d'iterations (generations) : {resultat['iterations']}")  # Affiche le nombre de nouvelles populations évaluées.
                print(f"Nombre de renouvellements : {resultat['redemarrages']}")  # Affiche les nouveaux départs dus à la stagnation.
                print(f"Nombre d'evaluations d'individus : {resultat['evaluations']}")  # Affiche le travail d'évaluation, distinct du nombre de générations.
            print(f"Temps de recherche : {resultat['temps']:.4f} secondes")  # Affiche la durée de la recherche.
            print(f"Mesures : {fichier_stats}")  # Affiche le chemin du fichier de statistiques.
            print(f"Grille : {fichier_grille}")  # Affiche le chemin du fichier des matrices.
            count += 1  # Passe à l'essai suivant.
        print(f"\nSolutions trouvees : {solutions}/{arguments.executions}")  # Affiche le nombre de réussites sur la série complète.
    except (OSError, ValueError) as erreur:  # Intercepte un problème technique ou une valeur invalide.
        print(f"Erreur : {erreur}", file=sys.stderr)  # Affiche clairement la cause de l'arrêt.
        return 1  # Signale une erreur technique au système.
    return 0  # Signale que les essais ont été exécutés, même si certains n'ont pas trouvé de solution.
if __name__ == "__main__":  # Exécute le programme uniquement quand ce fichier est lancé directement.
    sys.exit(main())  # Retourne le code de fin d'exécution au système.
