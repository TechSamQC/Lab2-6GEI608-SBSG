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

### Statistiques
#### Ex1-1 :
+ Frontière : 452
+ Nb états explorés : 282
+ Taille du chemin : 21
+ Moyenne du temps d'exécution : 0,96088 secondes
#### Ex1-2 :
+ Frontière : 363
+ Nb états explorés : 232
+ Taille du chemin : 18
+ Moyenne du temps d'exécution : 0,65436 secondes
#### Ex1-3 : NON EXÉCUTÉ (Aucune solution) !
#### Ex1-4 : 
+ Frontière : 1085
+ Nb états explorés : 726
+ Taille du chemin : 29
+ Moyenne du temps d'exécution : 5,31069 secondes
#### GLOBAL :
+ Moy. Frontière : 633,33
+ Moy. Nb états explorés : 413,33
+ Moy. Taille du chemin : 22,67
+ Moy. du temps d'exécution : 2,3086 secondes

### Conclusion de la partie 1
On observe qu'avec cet algorithme, on obtient des temps d'exécution très semblables aux meilleurs temps d'exécution obtenus avec les autres algorithmes pour ce même puzzle. De plus, on constate qu'il permet d'avoir le chemin de plus petite taille, égale à celui de l'algorithme de recherche en largeur, tout en explorant beaucoup moins d'états. En effet, si on prend l'exemple 4 et que l’on compare les deux algorithmes, on voit que la recherche en largeur nécessitait 178 223 états explorés avant de trouver un chemin de taille 29, alors que l'algorithme A* a nécessité uniquement 726 états explorés pour retrouver ce chemin. De plus, la taille de la frontière fut nettement plus petite, 1085 contre 180 899. On peut donc déduire que l'algorithme A* est beaucoup moins gourmand en termes de mémoire, tout en retrouvant le chemin le plus court et en un temps similaire au meilleur des algorithmes précédemment testés. Il nous semble ainsi le meilleur choix pour résoudre ce puzzle.

## Partie 2 - Problème d’optimisation - Sudoku
### Implémentation de la recherche locale (Hill climbing)

Pour cette partie, nous utilisons une recherche locale pour résoudre le Sudoku. La grille est représentée par une matrice NumPy de 9 lignes et 9 colonnes. La liste lockedindices contient les coordonnées des chiffres donnés au départ, qui ne doivent jamais être modifiés.

La fonction HillClimbing suppose que la grille reçue est déjà remplie et que chaque bloc 3 × 3 contient les chiffres de 1 à 9 sans répétition. Cette préparation doit donc être effectuée avant son appel. La recherche vise ensuite à éliminer les répétitions dans les lignes et les colonnes.

### Explication du fonctionnement

L’algorithme fait les opérations suivantes :

1. Copie la matrice reçue pour obtenir la grille courante et initialise les compteurs d’itérations ainsi que le chronomètre.

2. Construit la liste de toutes les paires de cases échangeables. Une paire contient deux cases non verrouillées appartenant au même bloc 3 × 3.

3. Évalue la grille en comptant les répétitions dans les lignes et les colonnes. Plus le score est faible, meilleure est la grille. Un score de 0 correspond à une solution lorsque les blocs sont valides et les chiffres donnés sont conservés.

4. Examine tous les échanges possibles afin de trouver celui qui réduit le plus le score. Pour éviter de recalculer entièrement le score de chaque voisin, utilise des compteurs d’occurrences et la fonction evaluation_delta, qui calcule uniquement l’effet de l’échange sur les lignes et les colonnes concernées.

5. Effectue le meilleur échange trouvé. Lorsque plusieurs échanges donnent la même amélioration, en choisit un aléatoirement.

6. Si aucun échange ne réduit le score, effectue 8 échanges aléatoires consécutifs entre des cases échangeables. Ces perturbations peuvent augmenter les conflits, mais elles permettent de quitter la configuration où la recherche était bloquée.

7. Lorsque le compteur de reprise it_restart atteint 200 000, repart d’une copie de la matrice reçue au début de la fonction. Le nombre total d’itérations et le chronomètre continuent de s’accumuler.

8. Lorsque le score atteint 0, enregistre la grille résolue, le temps d’exécution et le nombre total d’itérations, puis termine la recherche.

### PARTICULARITÉS :

- Les chiffres donnés sont protégés par lockedindices.
- Les échanges se font uniquement à l’intérieur d’un même bloc. Ils préservent donc la validité des blocs lorsqu’ils sont valides au départ.
- La phase d’amélioration accepte uniquement les voisins ayant un score strictement inférieur. Les 8 échanges aléatoires servent à sortir des situations sans amélioration immédiate.
- La reprise utilise la même matrice de départ. Elle ne génère pas un nouveau remplissage aléatoire.
- Le seuil de 200 000 déclenche une reprise et ne constitue pas une limite globale d’exécution. Le programme peut donc dépasser plusieurs millions d’itérations.
- Une itération correspond à un examen du voisinage suivi d’un meilleur échange ou d’une perturbation de 8 échanges. Chaque voisin examiné n’est pas compté comme une itération distincte.
- Les choix aléatoires peuvent produire des temps et des nombres d’itérations différents pour une même grille.
- Les résultats sont écrits dans output-partie2/output_X/HillClimbing_N.txt, où X représente le numéro de l’exemple et N celui de l’exécution.

Le fichier contient également une fonction bare_HillClimbing. Cette version effectue seulement les améliorations locales et retourne la grille lorsqu’elle atteint un score de 0 ou lorsqu’aucun meilleur voisin n’existe. Elle ne réalise ni perturbation aléatoire, ni reprise, ni écriture de résultats. La grille qu’elle retourne n’est donc pas nécessairement résolue.

### Statistiques

Nous avons regroupé 10 exécutions pour chacune des 10 grilles, soit 100 exécutions. Le nombre de chiffres donnés correspond aux cases déjà remplies dans le Sudoku d’origine. Les niveaux de difficulté sont ceux indiqués dans les fichiers provenant de QQWing.

| Exemple | Difficulté | Chiffres donnés | Temps moyen (s) | Nombre moyen d’itérations |
| :--- | :--- | ---: | ---: | ---: |
| Input_1 | Intermediate | 24 | 98,62 | 371 240 |
| Input_2 | Easy | 23 | 294,14 | 1 100 498 |
| Input_3 | Easy | 25 | 50,72 | 179 655 |
| Input_4 | Intermediate | 23 | 219,12 | 633 423 |
| Input_5 | Intermediate | 26 | 38,63 | 140 944|
| Input_6 | Easy | 25 | 14,16 | 50 603 |
| Input_7 | Intermediate | 25 | 84,35 | 286 084|
| Input_8 | Easy | 25 | 40,25 | 138 393 |
| Input_9 | Simple | 28 | 6,99 | 25 940 |
| Input_10 | Easy | 25 | 45,26 | 161 298 |
| **Moyenne globale (100 exécutions)** | — | — | **89,56** | **313 658** |

La moyenne globale est calculée en donnant le même poids à chacune des 100 exécutions.

### Conclusion Sur le Hill Climbing

On observe que le temps d’exécution dépend beaucoup de la grille et des choix effectués pendant la recherche. L’exemple 9 présente le temps moyen le plus faible, avec 6,99 secondes, tandis que l’exemple 2 présente le temps moyen le plus élevé, avec 294,14 secondes.

Les variations sont également importantes entre les exécutions d’une même grille. Pour l’exemple 4, les temps vont de 26,22 à 1 186,51 secondes. Sa moyenne atteint 219,12 secondes, alors que sa médiane est de 109,31 secondes. Certaines exécutions longues augmentent donc fortement la moyenne. Cela montre pourquoi il est utile de répéter les essais et de considérer aussi la médiane.

Le niveau de difficulté indiqué par QQWing ne suffit pas à prévoir les performances du Hill climbing. Par exemple, l’entrée 2, classée « Easy », demande en moyenne plus de temps que l’entrée 5, classée « Intermediate ». Le nombre de chiffres donnés ne suffit pas non plus : les entrées 6 et 7 possèdent chacune 25 chiffres donnés, mais leurs temps moyens sont respectivement de 14,16 et 84,35 secondes.

Notre méthode peut ainsi progresser rapidement sur certaines configurations et demander beaucoup plus de travail sur d’autres. Les perturbations aléatoires et les reprises donnent de nouvelles possibilités de progression, mais cette version ne garantit pas de trouver une solution dans un temps limité.
### Implémentation de l'algorithme génétique
