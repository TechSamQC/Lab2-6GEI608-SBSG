# Lab2-6GEI608-SBSG
Lab 2 - 6GEI608 - Intelligence artificielle et reconnaissance des formes

## Partie 1 : Algorithme A*
*Prendre note que, pour cette partie, nous avons repris le gabarit du fichier "Lab1.py" du laboratoire 1 afin d'effectuer les mêmes opérations sur le nouvel algorithme*
1. Choix de l'heuristique
    -> Nous avons repris les heuristiques du cours soit : 
    + H1 : nombre de carrés mal placés
    + H2 : somme de nombre de place qui sépare chaque carré de sa bonne place (distance de Manhattan)
    + Afin d'avoir l'heurstique dominante, nous utilisons **H3 = max(H1,H2)**
2. Temps d'exécution -> À voir dans le fichier Algo_A_x_stats.txt
3. Nombre d'itérations -> À voir dans le fichier Algo_A_x_stats.txt
4. Taille de la liste des états explorés dans chaque itération -> À voir dans le fichier Algo_A_x_stats.txt

### Explication du fonctionnement
L'algorithme fait les opérations suivantes :
1. 

**PARTICULARITÉS :**
+ 