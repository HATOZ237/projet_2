"""
Ce module est la deuxième partie du projet,
 à savoir le projet 2 du quoridor
"""
from copy import deepcopy
import networkx as nx


class QuoridorError(Exception):
    """
    Cette classe retourne des erreurs
    lorsque la classe Quoridor a des problèmes
    """


class Quoridor:
    """
    Cette classe dÉfinit les élements de type Quoridor
    """

    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.
        """
        # -----------------conditions--------------------

        # si joueurs n'est pas itérable
        if(not isinstance(joueurs, list) and not isinstance(joueurs, tuple)
           and not isinstance(joueurs, dict)):
            raise QuoridorError

        # si l'itérable de joueurs en contient plus de deux.
        if len(joueurs) > 2:
            raise QuoridorError

        for joueur in joueurs:
            if isinstance(joueur, dict):
                # si le nombre de murs qu'un joueur peut placer est >10, ou négatif
                if joueur['murs'] > 10 or joueur['murs'] < 0:
                    raise QuoridorError

                # si la position d'un joueur est invalide
                for coord_pos in joueur['pos']:
                    if not coord_pos in range(1, 10):
                        raise QuoridorError

        # si murs n'est pas un dictionnaire lorsque présent.
        if murs.values != [] and not isinstance(murs, dict):
            raise QuoridorError

        # si le total des murs placés et plaçables n'est pas égal à 20
        count = 0
        for joueur in joueurs:
            if isinstance(joueur, str):
                count += 10
            elif isinstance(joueur, dict):
                count += int(joueur['murs'])
        if murs != {}:
            count += len(murs['horizontaux'])
            count += len(murs['verticaux'])
        if count != 20:
            raise QuoridorError

        # si la position d'un mur est invalide.
        if murs.values != {}:
            for coord_pos in murs['horizontaux']:
                if not coord_pos[0] in range(1, 9) or not coord_pos[1] in range(2, 10):
                    raise QuoridorError
            for coord_pos in murs['verticaux']:
                if not coord_pos[0] in range(2, 10) or not coord_pos[1] in range(1, 9):
                    raise QuoridorError

        # si un element est inséré deux fois
        for i in murs['horizontaux']:
            count = 0
            for j in murs['horizontaux']:
                if i == j:
                    count += 1
            if count > 1:
                raise QuoridorError
        for i in murs['verticaux']:
            count = 0
            for j in murs['verticaux']:
                if i == j:
                    count += 1
            if count > 1:
                raise QuoridorError

        # ------------------------initialisation---------------

        partie = {}
        # initialisation des joueurs
        if isinstance(joueurs, list):
            pass
        if isinstance(joueurs, tuple):
            joueurs = list(joueurs)
        if isinstance(joueurs, dict):
            joueurs = list(joueurs[i] for i in joueurs.keys())

        partie_joueurs = []
        for indice, joueur in enumerate(joueurs):
            if isinstance(joueur, str):
                if indice == 0:
                    j = {'nom': joueur, 'murs': 10, 'pos': [5, 1]}
                else:
                    j = {'nom': joueur, 'murs': 10, 'pos': [5, 9]}
            elif isinstance(joueur, dict):
                j = {'nom': joueur['nom'],
                     'murs': joueur['murs'], 'pos': joueur['pos']}
            partie_joueurs.append(j)

        # initialisation des murs
        mur_horizontaux = mur_verticaux = []
        if murs.values != {}:
            mur_horizontaux = murs['horizontaux']
            mur_verticaux = murs['verticaux']

        # initialisation de l'état de la partie
        partie['état'] = {'joueurs': partie_joueurs,
                          'murs': {'horizontaux': mur_horizontaux, 'verticaux': mur_verticaux}}

        self.partie = partie

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état
        actuel de la partie.
        Cette représentation est la même que celle du TP précédent.
        retourner : la chaîne de caractères de la représentation.
        """
        état_partie = deepcopy(self.partie['état'])
        # creation d'une matrice vide
        ligne = 21
        colone = 39
        num = 9
        matrice = []
        place1 = état_partie["joueurs"][0]['nom']
        place2 = état_partie["joueurs"][1]['nom']
        matrice.append(['Légende: 1={}, 2={}'.format(place1, place2)])
        matrice.append(['   -----------------------------------'])
        for i in range(2, ligne-2):
            matrice.append([' ']*colone)
        matrice.append(['--|-----------------------------------'])
        matrice.append(['  | 1   2   3   4   5   6   7   8   9'])
        for i in range(2, ligne-2):
            matrice[i][2] = '|'
            matrice[i][38] = '|'
            if (i % 2) == 0:
                matrice[i][0] = str(num)
                num -= 1
                for j in range(1, 10):
                    matrice[i][4*j] = '.'
        # déchiffrage du json
        j1 = état_partie["joueurs"][0]["pos"]
        j2 = état_partie["joueurs"][1]["pos"]
        mh = état_partie["murs"]["horizontaux"]
        mv = état_partie["murs"]["verticaux"]

        # incorporation des élements du jeu : joueurs et murs
        # convertit les coordonnées des joueurs
        for i in [j1, j2]:
            i[0], i[1] = 2*(10-i[1]), i[0]*4
            # convertit les coordonnées des murs horizontaux
        for i in mh:
            i[0], i[1] = 2*(10-i[1])+1, 4*i[0]-1
            # convertit les coordonnées des murs verticaux
        for i in mv:
            i[0], i[1] = 2*(10-i[1])-2, 4*i[0]-2
            # insère les murs horizontaux
        for i in mh:
            for j in range(i[1], i[1]+7):
                matrice[i[0]][j] = '-'
            # insère les murs verticaux
        for i in mv:
            for j in range(i[0], i[0]+3):
                matrice[j][i[1]] = '|'

            # insère les joueurs
        matrice[j1[0]][j1[1]] = '1'
        matrice[j2[0]][j2[1]] != '2'
        # convertit la matrice en chaine
        for indice, mat1 in enumerate(matrice):
            matrice[indice] = ''.join(mat1)
        return '\n'.join(matrice)

    def état_partie(self):
        """Produire l'état actuel de la partie."""
        return self.partie['état']

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.
        """
        état = self.état_partie()
        graphe = construire_graphe(
            [player['pos'] for player in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux'])

        # si le numéro du joueur est autre que 1 ou 2
        if not(joueur in [1, 2]):
            raise QuoridorError

        # si la position est invalide(en dehors du damier)
        for coord_pos in position:
            if not coord_pos in range(1, 10):
                raise QuoridorError

        # si la position est invalide pour l'état actuel du jeu
        possibilité = list(graphe.successors(
            tuple(self.partie['état']["joueurs"][joueur-1]["pos"])))
        if not position in possibilité:
            raise QuoridorError
        else:
            self.partie['état']["joueurs"][joueur-1]["pos"] = list(position)

    def jouer_coup(self, joueur):
        """ à un niveau je ne comprends plus ce que je fais donc
        laisse seulement"""
        # si le numéro du joueur est autre que 1 ou 2
        if not(joueur in [1, 2]):
            raise QuoridorError

        # si la partie est terminée
        if self.partie_terminée() != False:
            raise QuoridorError

        état = self.état_partie()
        graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux'])
        path = [nx.shortest_path(
            graphe, état['joueurs'][joueur-1]['pos'], (5, 0)), nx.shortest_path(
            graphe, état['joueurs'][joueur-1]['pos'], (5, 10))]
        self.déplacer_jeton(joueur, path[joueur-1][1])

    def partie_terminée(self):
        """ Déterminer si la partie est terminée.
        """
        # si le joueur 1 est à la position (x, 9)
        if self.partie['état']['joueurs'][0]['pos'][1] == 9:
            return self.partie['état']['joueurs'][0]['nom']
            # si le joueur 2 est à la position (x, 1)
        if self.partie['état']['joueurs'][1]['pos'][1] == 1:
            return self.partie['état']['joueurs'][1]['nom']
        # si personne ne gagne
        return False

    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.
        """
        # si le numéro du joueur est autre que 1 ou 2
        a, b = position
        if not(joueur in [1, 2]):
            raise QuoridorError

        # si un mur occupe déjà cette position
        if position in self.partie['état']['murs']['horizontaux'] and orientation == 'horizontal':
            raise QuoridorError
        if position in self.partie['état']['murs']['verticaux'] and orientation == "vertical":
            raise QuoridorError
        if orientation == 'horizontal' and (a+1, b) in self.partie['état']['murs']['horizontaux']:
            raise QuoridorError

        # si la position est invalide pour cette orientation
        if not((2 <= a <= 9) and (1 <= b <= 8)) and orientation == 'vertical':
            raise QuoridorError
        if not((1 <= a <= 8) and (2 <= b <= 9)) and orientation == 'horizontal':
            raise QuoridorError

        # si le joueur a déjà placé tous ses murs
        if self.partie['état']['joueurs'][joueur-1]['murs'] == 0:
            raise QuoridorError

        # insertion des murs horizontaux et verticaux
        if orientation == 'vertical':
            self.partie['état']['murs']['verticaux'].append(position)
            self.partie['état']['joueurs'][joueur-1]['murs'] -= 1
        if orientation == 'horizontal':
            self.partie['état']['murs']['horizontaux'].append(position)
            self.partie['état']['joueurs'][joueur-1]['murs'] -= 1


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0],
                          2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe