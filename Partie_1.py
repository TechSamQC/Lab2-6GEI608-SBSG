import argparse  # Permet de choisir le numéro de l'exemple dans la commande.
import sys  # Permet de retourner un code de sortie au système.
from pathlib import Path  # Permet de retrouver les fichiers à partir du dossier du programme.

import numpy as np  # Permet de représenter les grilles sous forme de matrices.

from Algo_A import AlgoAstar  # Importe votre fonction de recherche A*.

count = 1  # Variable globale pour compter les exécutions.
Ex = 1  # Numéro de l'exemple utilisé si aucun numéro n'est indiqué dans la commande.
matriceinitiale = np.array([])  # Matrice initiale du jeu, remplie pendant l'initialisation.
matricevoulue = np.array([])  # Matrice objectif du jeu, remplie pendant l'initialisation.


def initialiser_application():
    """Charge la grille de l'exemple choisi et prépare la matrice objectif."""
    global matriceinitiale, matricevoulue  # Permet de remplir les deux matrices utilisées par main.
    print("Initialisation des composants...")  # Annonce le chargement de la grille.
    fichier = Path(__file__).resolve().parent / "input-Ex1" / f"Ex1-{Ex}.txt"  # Retrouve l'entrée à côté du programme.
    with fichier.open("r", encoding="utf-8-sig") as f:  # Accepte aussi les fichiers UTF-8 comportant un BOM.
        JeuInitiale = f.read()  # Lit l'intégralité du fichier de l'exemple.
    print("Contenu du fichier exemple du jeu :")  # Annonce l'affichage du texte d'entrée.
    print(JeuInitiale)  # Affiche la grille telle qu'elle est enregistrée.

    lignes = [ligne.split() for ligne in JeuInitiale.splitlines() if ligne.strip()]  # Accepte les espaces, les tabulations et les lignes vides.
    if len(lignes) != 3 or any(len(ligne) != 3 for ligne in lignes):  # Vérifie que le fichier contient trois lignes de trois cases.
        raise ValueError("Le fichier doit contenir une grille de 3 lignes et 3 colonnes, avec * pour le vide.")
    matriceinitiale = np.array(lignes, dtype=str)  # Construit la grille sans dépendre de la position des caractères dans le texte.
    matricevoulue = np.array([["1", "2", "3"], ["4", "5", "6"], ["7", "8", "*"]])  # Conserve votre matrice objectif.
    print("Matrice initiale :")  # Annonce la matrice chargée.
    print(matriceinitiale)  # Affiche l'état initial sous forme de matrice.
    print("Matrice voulue :")  # Annonce la matrice objectif.
    print(matricevoulue)  # Affiche l'état final recherché.


def main():
    """Choisit l'exemple et exécute A* dix fois sur la même grille."""
    global count, Ex  # Permet de mettre à jour le numéro de l'exemple et le compteur.
    parser = argparse.ArgumentParser(description="Exécute A* dix fois sur un exemple du 8-puzzle.")  # Prépare l'aide de la commande.
    parser.add_argument("exemple", nargs="?", type=int, choices=(1, 2, 3, 4), default=Ex, help="numéro de l'exemple : 1, 2, 3 ou 4")  # Rend le numéro facultatif.
    arguments = parser.parse_args()  # Lit le numéro fourni dans le terminal.
    Ex = arguments.exemple  # Sélectionne le fichier Ex1-X.txt correspondant.
    count = 1  # Recommence la numérotation à un pour cette série de dix essais.

    try:  # Permet d'afficher clairement une erreur de fichier ou de grille.
        initialiser_application()  # Prépare les matrices initiale et objectif.
        print("Application en cours d'exécution.")  # Annonce le début des essais.
        print("Heuristique : H3 = max(H1, H2), case vide exclue.")  # Précise l'heuristique utilisée pour ces essais.
        while count <= 10:  # Répète la recherche dix fois sur le même exemple.
            print(f"\nExécution A* #{count} - Ex1-{Ex}.txt")  # Affiche le numéro de l'essai et de l'exemple.
            AlgoAstar(matriceinitiale, matricevoulue, count, Ex)  # Conserve votre appel avec les quatre arguments d'origine.
            count += 1  # Passe au numéro d'exécution suivant.
    except (OSError, ValueError) as erreur:  # Intercepte un fichier inaccessible ou une entrée invalide.
        print(f"Erreur : {erreur}", file=sys.stderr)  # Affiche la cause de l'erreur dans le terminal.
        return 1  # Signale au système que le programme a rencontré une erreur.

    return 0  # Signale que les dix exécutions se sont terminées correctement.


if __name__ == "__main__":  # Lance main seulement lorsque ce fichier est exécuté directement.
    sys.exit(main())  # Retourne au système le code de sortie de l'application.
