import sys
import numpy as np

from SudokuFilling import fill
from HillClimbing import HillClimbing
from Algo_Genetic_Copy import AlgoGenetic

count = 1 # Variable globale pour compter les occurrences
matricesinitiales = [] # Liste des matrices "initiales" des jeux
lockedindices = [list([]) for _ in range(10)]  # Liste de taille 10 (10 inputs) des indices verrouillés dans les matrices initiales (les cases déjà remplies dans l'exemple) 

def initialiser_application():
    """Préparation des ressources ou de la configuration."""
    print("Initialisation des composants...")

    for Ex in range(1, 11): # Boucle pour chaque exemple de Sudoku (Input_1.txt à Input_10.txt)
        # 1. Lire le fichier .txt de l'exemple pour initialiser la matrice "initiale" du jeu de Sudoku
        # Mode "r" (read) : lit le contenu
        with open("input-partie2/Input_" + str(Ex) + ".txt", "r", encoding="utf-8") as f:
            # Tout lire dans une seule chaîne
            JeuInitiale = f.read()
        print ("\n Input #", Ex, "Contenu du fichier exemple du jeu :")
        print(JeuInitiale)

        # 2. Initialisation de la matrice "initiale"
        global matricesinitiales
        matricesinitiales.append(np.array([[JeuInitiale[1], JeuInitiale[3], JeuInitiale[5], JeuInitiale[9], JeuInitiale[11], JeuInitiale[13],
                                    JeuInitiale[17], JeuInitiale[19], JeuInitiale[21]], 
                                    [JeuInitiale[24], JeuInitiale[26], JeuInitiale[28], JeuInitiale[32], JeuInitiale[34], JeuInitiale[36],
                                    JeuInitiale[40], JeuInitiale[42], JeuInitiale[44]],
                                    [JeuInitiale[47], JeuInitiale[49], JeuInitiale[51], JeuInitiale[55], JeuInitiale[57], JeuInitiale[59],
                                    JeuInitiale[63], JeuInitiale[65], JeuInitiale[67]],
                                    [JeuInitiale[94], JeuInitiale[96], JeuInitiale[98], JeuInitiale[102], JeuInitiale[104], JeuInitiale[106],
                                    JeuInitiale[110], JeuInitiale[112], JeuInitiale[114]],
                                    [JeuInitiale[117], JeuInitiale[119], JeuInitiale[121], JeuInitiale[125], JeuInitiale[127], JeuInitiale[129],
                                    JeuInitiale[133], JeuInitiale[135], JeuInitiale[137]],
                                    [JeuInitiale[140], JeuInitiale[142], JeuInitiale[144], JeuInitiale[148], JeuInitiale[150], JeuInitiale[152],
                                    JeuInitiale[156], JeuInitiale[158], JeuInitiale[160]],
                                    [JeuInitiale[187], JeuInitiale[189], JeuInitiale[191], JeuInitiale[195], JeuInitiale[197], JeuInitiale[199],
                                    JeuInitiale[203], JeuInitiale[205], JeuInitiale[207]],
                                    [JeuInitiale[210], JeuInitiale[212], JeuInitiale[214], JeuInitiale[218], JeuInitiale[220], JeuInitiale[222],
                                    JeuInitiale[226], JeuInitiale[228], JeuInitiale[230]],
                                    [JeuInitiale[233], JeuInitiale[235], JeuInitiale[237], JeuInitiale[241], JeuInitiale[243], JeuInitiale[245],
                                    JeuInitiale[249], JeuInitiale[251], JeuInitiale[253]]]))

        # 3. Initialisation de la liste des indices verrouillés
        global lockedindices
        for i in range(9): # Parcours des lignes
            for j in range(9): # Parcours des colonnes
                if matricesinitiales[Ex-1][i, j] != '.': # Vérifie si la case est remplie
                    lockedindices[Ex-1].append((i, j)) # Ajoute l'indice à la liste des indices verrouillés
        print("\n Input #", Ex, "Indices verrouillés :") # Affiche la liste des indices des cases verrouillées
        print(lockedindices[Ex-1])

        # 4. Remplissage des cases vides de la matrice initiale avec des chiffres par défaut (1 à 9)
        fill(matricesinitiales[Ex-1], lockedindices[Ex-1], 9) # Initialise la matrice initiale en remplissant les cases vides avec des chiffres aléatoires (1 à 9 dans chaque bloc)
        print("\n Input #", Ex, "Matrice initialisée :") # Affiche la matrice initiale après remplissage des cases vides
        print(matricesinitiales[Ex-1])

def main():
    """Fonction principale contenant le flux d'exécution."""
    initialiser_application()

    # Logique principale du programme
    print("Application en cours d'exécution.")

    for Ex in range(1, 11): # Boucle pour chaque exemple de Sudoku
        # Boucle d'application de l'algorithme Hill Climbing pour résoudre le Sudoku
        global count
        count = 1 # Réinitialisation du compteur au début de chaque exemple
        while (count <= 10):
            print ("Hill Climbing Input #", Ex, "; Execution #", count, )
            HillClimbing(matricesinitiales[Ex-1], lockedindices[Ex-1], count, Ex)
            count += 1

        # Boucle d'application de l'algorithme génétique pour résoudre le Sudoku
        count = 1 # Réinitialisation du compteur pour l'algorithme génétique
        while (count <= 10):
            print ("Algo Genetique Input #", Ex, "; Execution #", count)
            #AlgoGenetic(matricesinitiales[Ex-1], lockedindices[Ex-1], count, Ex)
            count += 1

    # Retour d'un code de sortie (0 = succès)
    return 0

if __name__ == "__main__":
    # sys.exit assure que le script retourne un code d'erreur propre au système
    sys.exit(main())