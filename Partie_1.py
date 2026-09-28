import sys
import numpy as np

from Algo_A import AlgoAstar

count = 1 # Variable globale pour compter les occurrences
Ex = 1 # Variable globale pour le numéro d'exemple
matriceinitiale = np.array([]) # matrice "initiale" du jeu
matricevoulue = np.array([]) # matrice voulue du jeu

def initialiser_application():
    """Préparation des ressources ou de la configuration."""
    print("Initialisation des composants...")

    # Lire le fichier .txt de l'exemple pour initialiser la matrice "initiale"
    # Mode "r" (read) : lit le contenu
    with open("input-Ex1/Ex1-" + str(Ex) + ".txt", "r", encoding="utf-8") as f:
        # Tout lire dans une seule chaîne
        JeuInitiale = f.read()
    print ("Contenu du fichier exemple du jeu :")
    print(JeuInitiale)

    # Initialisation de la matrice "initiale"
    global matriceinitiale
    matriceinitiale = np.array([[JeuInitiale[0], JeuInitiale[2], JeuInitiale[4]], 
                                [JeuInitiale[6], JeuInitiale[8], JeuInitiale[10]], 
                                [JeuInitiale[12], JeuInitiale[14], JeuInitiale[16]]])
    print("Matrice initiale :")
    print(matriceinitiale)

    # Initialisation de la matrice voulue
    global matricevoulue
    matricevoulue = np.array([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '*']])
    print("Matrice voulue :")
    print(matricevoulue)

def main():
    """Fonction principale contenant le flux d'exécution."""
    initialiser_application()

    # Logique principale du programme
    print("Application en cours d'exécution.")

    # Boucle d'application de l'algorithme A* pour résoudre le jeu
    global count
    while (count <= 10):
        print ("Execution A* #", count)
        # Appel de l'algorithme A*
        AlgoAstar(matriceinitiale, matricevoulue, count, Ex)
        count += 1
    
    # Retour d'un code de sortie (0 = succès)
    return 0

if __name__ == "__main__":
    # sys.exit assure que le script retourne un code d'erreur propre au système
    sys.exit(main())