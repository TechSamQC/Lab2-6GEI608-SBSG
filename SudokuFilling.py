import random
import math

def fill(matrice, lockedindices, n):
    """
    Remplit les cases vides d'une matrice de Sudoku avec des chiffres aléatoires.
    Arguments:
        matrice (np.ndarray): La matrice représentant l'état actuel du Sudoku.
        lockedindices (list): Liste des indices verrouillés dans la matrice.
        n (int): Taille de la matrice (nombre de lignes/colonnes).
    """
    EtatsPossible = list(range(1, n + 1)) # Liste des chiffres possibles pour remplir les cases vides
    for bi in range(0, n, int(n/math.isqrt(n))): # Parcours des blocs par ligne
            for bj in range(0, n, int(n/math.isqrt(n))): # Parcours des blocs par colonne
                EtatsRestants = EtatsPossible.copy() # Copie de la liste des chiffres possibles pour suivre les chiffres restants disponibles dans un bloc
                
                # Premier parcours des cases du bloc pour vérifier les chiffres restants (retirer les chiffre des cases déjà remplies)
                for i in range(bi, bi + int(n/math.isqrt(n))): # Parcours des lignes du bloc actuel
                    for j in range(bj, bj + int(n/math.isqrt(n))): # Parcours des colonnes du bloc actuel
                        if (i, j) in lockedindices: # Vérifie si la case est verrouillée
                            EtatsRestants.remove(int(matrice[i, j])) # Supprime le chiffre verrouillé de la liste des chiffres restants
                
                # Deuxième parcours des cases du bloc pour remplir les cases vides avec les chiffres restants
                for i in range(bi, bi + int(n/math.isqrt(n))): # Parcours des lignes du bloc actuel
                    for j in range(bj, bj + int(n/math.isqrt(n))): # Parcours des colonnes du bloc actuel
                        if (i, j) not in lockedindices: # Vérifie si la case n'est pas verrouillée
                            matrice[i, j] = str(random.choice(EtatsRestants)) # Remplit la case avec un chiffre aléatoire parmi les chiffres restants
                            EtatsRestants.remove(int(matrice[i, j])) # Supprime le chiffre utilisé de la liste des chiffres restants