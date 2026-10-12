import sys
import numpy as np

#from HillClimbing import HillClimbing
#from Algo_Genetic import AlgoGenetic

count = 1 # Variable globale pour compter les occurrences
Ex = 3 # Variable globale pour le numéro d'exemple
matriceinitiale = np.array([]) # matrice "initiale" du jeu

def initialiser_application():
    """Préparation des ressources ou de la configuration."""
    print("Initialisation des composants...")

    # Lire le fichier .txt de l'exemple pour initialiser la matrice "initiale" du jeu de Sudoku
    # Mode "r" (read) : lit le contenu
    with open("input-partie2/Input_" + str(Ex) + ".txt", "r", encoding="utf-8") as f:
        # Tout lire dans une seule chaîne
        JeuInitiale = f.read()
    print ("Contenu du fichier exemple du jeu :")
    print(JeuInitiale)

    # Initialisation de la matrice "initiale"
    global matriceinitiale
    matriceinitiale = np.array([[JeuInitiale[1], JeuInitiale[3], JeuInitiale[5], JeuInitiale[9], JeuInitiale[11], JeuInitiale[13],
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
                                 JeuInitiale[249], JeuInitiale[251], JeuInitiale[253]]])
    print("Matrice initiale :")
    print(matriceinitiale)

def main():
    """Fonction principale contenant le flux d'exécution."""
    initialiser_application()

    # Logique principale du programme
    print("Application en cours d'exécution.")

    # Boucle d'application de l'algorithme Hill Climbing pour résoudre le Sudoku
    global count
    while (count <= 10):
        print ("Execution Hill Climbing #", count)
        # TODO: Appel de l'algorithme Hill Climbing
        
        count += 1

    # Boucle d'application de l'algorithme génétique pour résoudre le Sudoku
    while (count <= 10):
        print ("Execution Algo Genetique #", count)
        # TODO: Appel de l'algorithme Algo Genetique
        
        count += 1

    # Retour d'un code de sortie (0 = succès)
    return 0

if __name__ == "__main__":
    # sys.exit assure que le script retourne un code d'erreur propre au système
    sys.exit(main())