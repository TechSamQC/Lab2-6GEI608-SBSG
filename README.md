# Lab2-6GEI608-SBSG
Lab 2 - 6GEI608 - Intelligence artificielle et reconnaissance des formes

## Partie 1 - Algorithme A*
*Prendre note que, pour cette partie, nous avons repris le gabarit du fichier "Lab1.py" du laboratoire 1 afin d'effectuer les mêmes opérations sur le nouvel algorithme*
1. Choix de l'heuristique
    -> Nous avons repris les heuristiques du cours, soit : 
    + H1 : nombre de carrés mal placés
    + H2 : somme de nombre de place qui sépare chaque carré de sa bonne place (distance de Manhattan)
    + Afin d'avoir l'heuristique dominante, nous utilisons **H3 = max(H1,H2)**
2. Temps d'exécution -> À voir dans le fichier Algo_A_x_stats.txt
3. Nombre d'itérations -> À voir dans le fichier Algo_A_x_stats.txt
4. Taille de la liste des états explorés dans chaque itération -> À voir dans le fichier Algo_A_x_stats.txt

### Explication du fonctionnement
L'algorithme fait les opérations suivantes :
1. Initialise l'index courant à "None" puis trouve l'index du nœud à explorer dans la liste frontière en calculant la fonction f = g + h et en prenant le minimum disponible.
2. Ajoute itérativement les enfants d'un état (haut, bas, gauche, droite) dans la liste frontière sous forme de matrice.
3. Après avoir ajouté tous les enfants possibles, l'itération augmente de 1, on recommence alors à l'étape 1.
4. Pour retrouver le chemin de la solution, l'algorithme remonte les parents à partir de l'état final jusqu'à l'état initial.

**PARTICULARITÉS :**
+ L'exemple 3 n'a pas été traité, car il est trop long de passer tous les états possibles
+ SI l'index courant reste à "NONE", c'est qu'il n'y a aucun état non exploré, tous les états ont été explorés et on n’a pas de solution.
+ Les états déjà ajoutés ne reviennent pas dans la liste frontière, permettant d'éviter les boucles.
+ Les états déjà explorés ne sont pas pris en compte pour calculer le minimum de la fonction f.
+ Le coût g est conservé dans une liste qui correspond aux mêmes index que dans la liste frontière.
+ La vérification d'états vue/exploré se fait à l'aide d'un "set". Le "set" permet d'avoir une liste de suite d'octets, plutôt que de matrice. Lors de la comparaison et vérification si un état a déjà été vu, c'est beaucoup plus rapide de comparer des suites d'octets que des matrices complètes\.
+ Une liste de parents est maintenue pour chaque état afin de pouvoir reconstruire le chemin de la solution. Cette liste contient le numéro de l'index de l'état parent de l'état à l'index courant, ce qui permet de retrouver le parent dans la liste frontière.

### Conclusion de la partie 1
On observe qu'avec cet algorithme, on n’obtient pas les meilleurs temps d'exécution de tous les algorithmes à cause évidemment de l'augmentation des opérations de comparaison à réaliser dans celui-ci. Cependant, on remarque qu'il permet d'avoir le chemin de plus petite taille, égale à celui de l'algorithme de recherche en largeur, tout en explorant beaucoup moins d'états. En effet, si on prend l'exemple 4 et que l’on compare les deux algorithmes, on voit que la recherche en largeur nécessitait 178 223 états explorés avant de trouver un chemin de taille 29, alors que l'algorithme A* a nécessité uniquement 726 états explorés pour retrouver ce chemin. De plus, la taille de la frontière fut nettement plus petite, 1085 contre 180 899. On peut donc déduire que l'algorithme A* est beaucoup moins gourmand en termes de mémoire.

## Partie 2 - Problème d’optimisation - Sudoku
### Implémentation de la recherche locale (Hill climbing)

### Implémentation de l'algorithme génétique
