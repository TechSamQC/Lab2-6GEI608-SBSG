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
## Explication du "SudokuFilling.py" : Fonction "fill()"
Nous avons commencé par créer une fonction qui permet de remplir la grille de sudoku pour commencer avec une grille déjà pleine. Pour alléger légèrement la tâche des algorithmes et trouver des solutions plus rapidement, la fonction de remplissage remplit les grilles de manière à ce que chaque bloc 3x3 contienne les chiffres de 1 à 9 sans répétition\. Elle est ainsi utilisée par l'algorithme génétique pour faire une nouvelle population et par le programme principal qui passe la matrice initiale déjà remplie.

## Explication du "Partie_2.py" : Fonction "main"
Dans le "main" de la partie 2, nous initialisons les matrices représentant les grilles de Sudoku en lisant le fichier "input" correspondant aux différents exemples. Pour chaque exemple, nous identifions les indices verrouillés correspondant aux chiffres donnés, et utilisons la fonction fill() pour remplir les cases vides. Ensuite, nous appliquons les deux algorithmes de la partie 2 10 fois sur chaque exemple afin de mesurer leurs performances et comparer les résultats obtenus.

## Implémentation de la recherche locale (Hill climbing)
Pour cette partie, nous utilisons une recherche locale pour résoudre le Sudoku. La grille est représentée par une matrice NumPy de 9 lignes et 9 colonnes. La liste lockedindices contient les coordonnées des chiffres donnés au départ, qui ne doivent jamais être modifiés.

La fonction HillClimbing suppose que la grille reçue est déjà remplie et que chaque bloc 3 × 3 contient les chiffres de 1 à 9 sans répétition (assuré par la fonction fill() dans le main de la partie 2). La recherche vise ensuite à éliminer les répétitions dans les lignes et les colonnes.

### Explication du fonctionnement
L’algorithme fait les opérations suivantes :

1. Copie la matrice reçue pour obtenir la grille courante et initialise les compteurs d’itérations ainsi que le chronomètre.
2. Construis la liste de toutes les paires de cases échangeables. Une paire contient deux cases non verrouillées appartenant au même bloc 3 × 3.
3. Évalue la grille en comptant les répétitions dans les lignes et les colonnes. Plus le score est faible, meilleure est la grille. Un score de 0 correspond à une solution lorsque les blocs sont valides et les chiffres donnés sont conservés.
4. Examine tous les échanges possibles afin de trouver celui qui réduit le plus le score. Pour éviter de recalculer entièrement le score de chaque voisin, utilise des compteurs d’occurrences et la fonction evaluation_delta, qui calcule uniquement l’effet de l’échange sur les lignes et les colonnes concernées.
5. Effectue le meilleur échange trouvé. Lorsque plusieurs échanges donnent la même amélioration, il en choisit un aléatoirement.
6. Si aucun échange ne réduit le score, effectue 8 échanges aléatoires consécutifs entre des cases échangeables. Ces perturbations peuvent augmenter les conflits, mais elles permettent de quitter la configuration où la recherche était bloquée (plateau local).
7. Lorsque le compteur de reprise it_restart atteint 200 000, repars d’une copie de la matrice reçue au début de la fonction. Le nombre total d’itérations et le chronomètre continuent de s’accumuler. Cela permet de relancer la recherche à partir d’une configuration initiale si la recherche est bloquée dans un état de plateau local.
8. Lorsque le score atteint 0, enregistre la grille résolue, le temps d’exécution et le nombre total d’itérations, puis termine la recherche.

**PARTICULARITÉS :**
- Les chiffres donnés sont protégés par "lockedindices".
- Les échanges se font uniquement à l’intérieur d’un même bloc. Ils préservent donc la validité des blocs, vu qu’ils sont valides au départ.
- La phase d’amélioration (recherche du meilleur voisin) accepte uniquement les voisins ayant un score strictement inférieur.
- Les 8 échanges aléatoires servent à sortir des situations sans amélioration immédiate (plateau local). Nous avons choisi le chiffre 8 après quelques expérimentations pour trouver un compromis entre perturbation suffisante et stabilité de la recherche.
- Le seuil de 200 000 itérations déclenche une reprise et ne constitue pas une limite globale d’exécution. Le programme peut donc dépasser plusieurs millions d’itérations. Cela permet d'assurer que la recherche ne reste pas bloquée indéfiniment dans un plateau local et aussi d'assurer qu'une solution finira par être trouvée si elle existe. Nous avons choisi ce seuil par approximation après quelques expérimentations pour trouver un compromis entre fréquence des reprises et efficacité de la recherche.
- La reprise utilise la même matrice de départ. Elle ne génère pas un nouveau remplissage aléatoire. Ce choix a été pris pour éviter de repartir d'une configuration initiale différente, ce qui aurait faussé les statistiques de performance.
- Une itération correspond à un examen du voisinage suivi d’un meilleur échange ou d’une perturbation de 8 échanges. Chaque voisin examiné n’est pas compté comme une itération distincte.
- Les choix aléatoires peuvent produire des temps et des nombres d’itérations différents pour une même grille, ce qui rend les performances non déterministes d’une exécution à l’autre.
- Les résultats sont écrits dans output-partie2/output_X/HillClimbing_N.txt, où X représente le numéro de l’exemple et N celui de l’exécution.

*Le fichier contient également une fonction bare_HillClimbing. Cette version effectue seulement les améliorations locales et retourne la grille lorsqu’elle atteint un score de 0 ou lorsqu’aucun meilleur voisin n’existe. Elle ne réalise ni perturbation aléatoire, ni reprise, ni écriture de résultats. La grille qu’elle retourne n’est donc pas nécessairement résolue. Elle est utilisée en conjonction de l’algorithme génétique pour initialiser la population avec des individus déjà partiellement optimisés.*

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

*La moyenne globale est calculée en donnant le même poids à chacune des 100 exécutions.*

Voici les moyennes par niveau de difficulté :
| Difficulté | Temps moyen (s) | Nombre moyen d’itérations |
| :--- | ---: | ---: |
| Simple | 6,99 | 25 940 |
| Easy | 88,91 | 326 089 |
| Intermediate | 110,18 | 357 923 |

Voici les moyennes par nombre de chiffres donnés :
| Nombre de chiffres | Temps moyen (s) | Nombre moyen d’itérations |
| :--- | ---: | ---: |
| 23 | 256,63 | 866 961 |
| 24 | 98,62 | 371 240 |
| 25 | 46,95 | 163 206 |
| 26 | 38,63 | 140 944 |
| 28 | 6,99 | 25 940 |

### Conclusion Sur le Hill Climbing
Premièrement, on observe que le temps d’exécution dépend beaucoup de la grille, notamment de la difficulté et du nombre de chiffres donnés dès le départ. L’exemple 9 présente le temps moyen le plus faible, avec 6,99 secondes, mais c'est aussi l'exemple avec la difficulté la plus simple (le seul à "Simple"), et celui qui fournit le plus de données initiales (le seul à 28). Inversement, l’exemple 2 présente le temps moyen le plus élevé, avec 294,14 secondes.

Deuxièmement, on remarque que les variations sont importantes entre les résolutions d’une même grille. Pour l’exemple 4 (difficulté intermédiaire et 23 chiffres donnés), les temps vont de 26,22 à 1 186,51 secondes. Sa moyenne atteint 219,12 secondes, alors que sa médiane est de 109,31 secondes. Certaines exécutions longues augmentent donc fortement la moyenne. Cela montre pourquoi il est utile de répéter les essais et de considérer aussi la médiane.

Troisièmement, dans les statistiques, on voit très clairement la corrélation entre la difficulté et le temps d’exécution : les grilles plus difficiles tendent à nécessiter plus de temps en moyenne. Même chose pour le nombre de chiffres donnés : plus il y en a, plus le temps moyen tend à être faible. Cependant, malgré une forte corrélation, le niveau de difficulté indiqué par QQWing ne suffit pas à prévoir les performances du Hill climbing. Par exemple, l’entrée 2, classée « Easy », demande en moyenne plus de temps que l’entrée 5, classée « Intermediate ». Même constat pour le nombre de chiffres donnés : les entrées 6 et 7 possèdent chacune 25 chiffres donnés, mais leurs temps moyens sont respectivement de 14,16 et 84,35 secondes.

Finalement, on constate que notre méthode peut progresser rapidement sur certaines configurations et demander beaucoup plus de travail sur d’autres. Les perturbations aléatoires et les reprises donnent de nouvelles possibilités de progression, mais cette version ne garantit pas de trouver une solution dans un temps limité.

## Implémentation de l'algorithme génétique
Pour cette partie, l'algorithme génétique a été implémenté afin de résoudre le problème du Sudoku en faisant évoluer une population de solutions candidates. Contrairement à une approche qui travaille sur une seule grille, cette méthode manipule plusieurs individus simultanément et utilise des mécanismes inspirés de l'évolution naturelle pour améliorer progressivement leur qualité. 

Comme pour la partie précédente, la grille est représentée par une matrice NumPy de 9 lignes et 9 colonnes. La liste lockedindices contient les coordonnées des chiffres donnés au départ, qui ne doivent jamais être modifiés. On suppose encore ici que la grille reçue est déjà remplie et que chaque bloc 3 × 3 contient les chiffres de 1 à 9 sans répétition (assuré par la fonction fill() dans le main de la partie 2). La recherche vise ensuite à éliminer les répétitions dans les lignes et les colonnes.

L'implémentation repose sur une population de 40 individus, dont chacun représente une grille de Sudoku. Elle combine l'algorithme génétique avec une recherche locale de type Hill Climbing afin d'améliorer les individus avant leur évaluation.

### Explication du fonctionnement et particularités
Le fonctionnement de l'algorithme peut être divisé en plusieurs étapes.

1. Copie la matrice reçue pour obtenir la grille courante et initialise les compteurs d’itérations ainsi que le chronomètre.

2. Génération des paires de cases échangeables : Avant de commencer les itérations, l'algorithme identifie les cases qui peuvent être échangées sans modifier les valeurs initiales du Sudoku.

3. Initialisation de la population : La population initiale contient 40 individus, chacun représentant une grille de Sudoku. Le premier individu est une copie de la grille initiale, alors que les 39 autres individus sont créés avec la fonction fill. Le nombre de 40 individus a été choisi de manière logique et aléatoire pour assurer une diversité suffisante dans la population sans surcharger le calcul.

4. Optimisation locale avec Hill Climbing : À chaque itération, l'algorithme applique la fonction bare_HillClimbing à chacun des individus de la population. Nous avons choisi d'utiliser cette approche pour permettre à chaque individu de s'améliorer localement avant d'être évalué et potentiellement combiné avec d'autres individus. Cela permet également de converger vers une solution beaucoup plus rapidement en réduisant les conflits dans les lignes et les colonnes au maximum dès les premières étapes. L'algorithme génétique et Hill Climbing remplissent ainsi des rôles complémentaires : la recherche locale améliore chaque candidat, tandis que les opérations génétiques permettent de diversifier les solutions et d'explorer de nouvelles configurations.

5. Évaluation de la fitness : La fonction fonction_fitness mesure la qualité d'une grille en comptant les doublons présents dans ses lignes et ses colonnes (équivalent de la fonction de score utilisée dans la partie précédente). Un score faible indique une meilleure grille. Un score de 0 signifie qu'aucun doublon n'est présent dans les lignes ou les colonnes.

6. Sélection des meilleurs individus et élitisme : Les individus sont triés par ordre croissant de leur score de fitness. Les quatre premiers sont ensuite préservés des opérations de croisement et de mutation (élitisme).

7. Croisement (crossover) : Le croisement prend deux individus parents et génère deux enfants. Pour chacun des neuf blocs de 3 × 3, une décision aléatoire détermine si les blocs des deux parents sont échangés. Chaque bloc a ainsi une probabilité de 50 % d'être échangé. Cette opération permet de combiner différentes configurations issues des parents.

8. Mutation : Après le croisement, la mutation est appliquée à tous les individus qui ne font pas partie des quatre meilleurs individus préservés. Pour chaque individu muté, trois paires de cases échangeables sont sélectionnées aléatoirement. Les valeurs des deux cases de chaque paire sont ensuite interverties. Cette opération introduit de nouvelles variations dans la population. Elle permet d'explorer des configurations différentes et de limiter la stagnation de l'algorithme.

9. Redémarrage de la population : Afin de renouveler la recherche lorsque l'évolution de la population se prolonge, l'algorithme utilise un compteur de redémarrage. Lorsque ce compteur atteint le seuil de 150 (choisi par expérimentations), la population est reconstruite à partir de la grille initiale : un individu reprend la grille de départ et 39 nouveaux individus sont générés avec fill. Ce mécanisme permet de réintroduire de la diversité dans la recherche lorsque les générations successives ne suffisent pas à trouver une solution (plateau de fitness).

10. Condition d'arrêt et enregistrement des résultats : L'algorithme s'arrête lorsqu'un individu atteint une fitness égale à 0. La grille résolue, le temps d'exécution et le nombre d'itérations sont alors inscrits dans un fichier de sortie associé à l'exécution et à l'exemple traité.
*Les résultats sont écrits dans output-partie2/output_X/AlgoGenetic_N.txt, où X représente le numéro de l’exemple et N celui de l’exécution.*

### Statistiques
Nous avons regroupé 10 exécutions pour chacune des 10 grilles, soit 100 exécutions. Le nombre de chiffres donnés correspond aux cases déjà remplies dans le Sudoku d’origine. Les niveaux de difficulté sont ceux indiqués dans les fichiers provenant de QQWing.

| Exemple | Difficulté | Chiffres donnés | Temps moyen (s) | Nombre moyen d’itérations |
| :--- | :--- | ---: | ---: | ---: |
| Input_1 | Intermediate | 24 | 11,01 | 34 |
| Input_2 | Easy | 23 | 69,00 | 665 |
| Input_3 | Easy | 25 | 3,66 | 41 |
| Input_4 | Intermediate | 23 | 3,52 | 36 |
| Input_5 | Intermediate | 26 | 12,69 | 173 |
| Input_6 | Easy | 25 | 3,23 | 36 |
| Input_7 | Intermediate | 25 | 56,59 | 398 |
| Input_8 | Easy | 25 | 8,27 | 55 |
| Input_9 | Simple | 28 | 3,21 | 18 |
| Input_10 | Easy | 25 | 67,21 | 535 |
| **Moyenne globale (100 exécutions)** | — | — | **23,84** | **199** |

*La moyenne globale est calculée en donnant le même poids à chacune des 100 exécutions.*

Voici les moyennes par niveau de difficulté :
| Difficulté | Temps moyen (s) | Nombre moyen d’itérations |
| :--- | ---: | ---: |
| Simple | 3,21 | 18 |
| Easy | 30,28 | 266 |
| Intermediate | 20,95 | 160 |

Voici les moyennes par nombre de chiffres donnés :
| Nombre de chiffres | Temps moyen (s) | Nombre moyen d’itérations |
| :--- | ---: | ---: |
| 23 | 36,26 | 350 |
| 24 | 11,01 | 34 |
| 25 | 27,79 | 213 |
| 26 | 12,69 | 173 |
| 28 | 3,21 | 18 |

*Important de prendre en considération que le nombre d'itération ne prends pas en compte le nombre d'itérations faites dans la recherche locale. Cela signifie que le nombre réel d'opérations effectuées par l'algorithme est en réalité plus élevé que celui indiqué dans les tableaux.*

### Conclusion sur l'algorithme génétique
L'algorithme génétique développé combine la recherche locale, le croisement, la mutation et l'élitisme afin de résoudre le Sudoku tout en préservant les contraintes des blocs de 3 × 3. Cette approche permet d'explorer plusieurs solutions candidates simultanément et de les améliorer progressivement.

Les 100 exécutions réalisées sur dix grilles différentes montrent toutefois que les performances varient considérablement selon l'exemple traité. La difficulté attribuée par QQWing et le nombre de chiffres donnés au départ peuvent notamment influencer les performances observées. Par exemple, la grille numéro 9, classée comme simple et comportant 28 chiffres donnés, est résolue en moyenne en 3,21 secondes, tandis que la grille numéro 5, classée comme intermédiaire et comportant 26 chiffres donnés, nécessite en moyenne 12,69 secondes.

Cependant, la difficulté attribuée par QQWing et le nombre de chiffres donnés ne suffisent pas, à eux seuls, à prédire le temps de résolution. La grille numéro 2, classée « Easy » et comportant 23 chiffres donnés, nécessite en moyenne 69,00 secondes, tandis que la grille numéro 4, classée « Intermediate » et comportant également 23 chiffres donnés, est résolue en moyenne en seulement 3,52 secondes. Les moyennes calculées par niveau de difficulté et par nombre de chiffres donnés illustrent également cette variabilité : les grilles de niveau « Easy » prennent davantage de temps à résoudre en moyenne que celles de niveau « Intermediate », tandis que les grilles comportant 25 chiffres donnés présentent un temps moyen supérieur à celles qui en comportent 24. Ces observations doivent néanmoins être interprétées avec prudence, puisque chaque catégorie ne comprend qu'un nombre limité de grilles.

Les résultats montrent également que les temps de résolution peuvent varier considérablement d'une exécution à l'autre pour une même grille. Pour l'exemple 10, classé « Easy » et comportant 25 chiffres donnés, les temps observés s'étendent de 3,23 à 163,17 secondes, pour une moyenne de 67,21 secondes. Cette variation souligne l'importance de répéter les exécutions afin d'obtenir une estimation plus représentative des performances de l'algorithme.

Dans l'ensemble, les résultats montrent que l'approche hybride combinant l'algorithme génétique et la recherche locale par Hill Climbing permet de résoudre la majorité des grilles assez rapidement en moyenne. La recherche locale contribue à améliorer les individus de la population, tandis que le croisement et la mutation favorisent l'exploration de nouvelles configurations. L'élitisme permet, quant à lui, de conserver les meilleurs individus d'une génération à l'autre.

Le redémarrage périodique de la population fut également un mécanisme important visant à diversifier les configurations explorées lorsque la recherche progresse difficilement. En réinitialisant la population à partir de la grille initiale et de nouvelles configurations candidates, cette stratégie aide l'algorithme à sortir de certaines situations défavorables.

En conclusion, la méthode développée peut résoudre certaines grilles rapidement, mais ses performances demeurent sensibles à la configuration du problème et aux variations entre les exécutions. La combinaison du croisement, de la mutation, de l'élitisme et de la recherche locale offre une stratégie d'exploration intéressante. Les résultats obtenus permettent d'en évaluer le comportement sur les dix grilles testées, sans toutefois généraliser ces conclusions à l'ensemble des grilles de Sudoku.

## Comparaison des algorithmes de la partie 2
On constate clairement que l'algorithme génétique, de la façon dont nous l'avons implémenté et optimisé, permet de résoudre plus rapidement les grilles de Sudoku que l'algorithme de recherche locale seul. En effet, on a eu comme résultat que l'exécution globale moyenne de l'algorithme HillClimbing fut de 89,56 secondes sur les 100 exécutions, tandis que celle de l'algorithme génétique fut de 23,84 secondes. On peut également dire que, peu importe la grille de départ, sa difficulté ou le nombre de chiffres donnés, l'algorithme génétique est plus efficace que l'algorithme de recherche locale. Cela montre donc l'intérêt de combiner la recherche locale avec l'algorithme génétique pour améliorer l'efficacité de la résolution des grilles telle que nous l'avons fait.

## Ce que nous avons appris
Ce laboratoire nous a permis de mieux comprendre le fonctionnement de différents algorithmes de recherche et d'optimisation, ainsi que les compromis associés à chacun d'entre eux. Nous avons notamment constaté que les performances d'un algorithme ne dépendent pas uniquement de sa complexité théorique, mais également de la représentation du problème, des stratégies utilisées pour explorer les solutions et des paramètres choisis lors de son implémentation.

Dans la première partie, consacrée à la résolution du 8-puzzle à l'aide de l'algorithme A*, nous avons appris l'importance du choix de l'heuristique. Celle-ci permet d'orienter la recherche vers les états qui semblent les plus prometteurs et de réduire le nombre d'états explorés. Nos résultats montrent que l’algorithme A* peut trouver un chemin de longueur minimale en explorant beaucoup moins d’états que la recherche en largeur dans les exemples traités. Nous avons également constaté que la gestion efficace des états déjà visités et de la liste frontière joue un rôle important dans les performances, notamment en limitant les explorations inutiles et l'utilisation de la mémoire.

La deuxième partie nous a permis d'étudier un problème d'optimisation plus complexe avec la résolution de grilles de Sudoku. Nous avons ainsi pu comparer deux approches différentes, soit l'algorithme de Hill Climb et l'algorithme génétique.

Nous avons constaté les limites de la recherche locale par Hill Climbing. Même si elle permet d'améliorer rapidement une grille en choisissant les échanges qui réduisent le plus le nombre de conflits, elle peut atteindre une configuration dans laquelle aucun échange individuel ne permet d'améliorer le score (un plateau/max local). Les perturbations aléatoires et les redémarrages constituent alors des moyens de diversifier la recherche et de tenter de sortir de ces situations. Nos expérimentations nous ont permis de mieux comprendre l'importance du choix des paramètres, comme le nombre d'échanges aléatoires et le seuil de redémarrage.

L'implémentation de l'algorithme génétique nous a permis de comprendre l'intérêt de combiner plusieurs stratégies de recherche. La recherche locale améliore individuellement les solutions candidates, tandis que le croisement et la mutation permettent d'explorer de nouvelles configurations. L'élitisme permet de préserver les meilleurs individus, alors que le redémarrage de la population réintroduit de la diversité. Cette combinaison offre une approche complémentaire à celle du Hill Climbing utilisé seul, même si les performances restent variables selon la grille et l'exécution.

Un autre apprentissage important concerne l'évaluation expérimentale des algorithmes. Les résultats obtenus montrent qu'une même grille peut nécessiter des temps de résolution très différents d'une exécution à l'autre, notamment en raison des choix aléatoires. Il est donc important de répéter les essais et d'analyser plusieurs indicateurs, comme le temps d'exécution, le nombre d'itérations et le nombre d'états explorés, lorsque ces mesures sont disponibles. Nous avons également appris qu'il faut interpréter les statistiques avec prudence : le nombre de chiffres donnés et la difficulté attribuée à une grille ne suffisent pas, à eux seuls, à prédire le comportement d'un algorithme.

En conclusion, ce laboratoire nous a permis de constater qu'il n'existe pas une seule stratégie de recherche adaptée à tous les problèmes. Le choix de l'algorithme, la conception de la représentation, les mécanismes d'exploration et le réglage des paramètres influencent directement les résultats. Nous retenons surtout l'importance d'expérimenter, de comparer les approches et d'analyser leurs limites afin de concevoir des solutions plus efficaces et mieux adaptées au problème traité.