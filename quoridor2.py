import networkx as nx


class QuoridorError(BaseException):
    pass


class Quoridor:

    def __init__(self, joueurs, murs=None):
        """j'ai ecrit du n'importe quoi ici donc ne regarde pas ça"""
        self.joueurs = joueurs
        self.murs = murs
        self.état = joueurs

    def état_partie(self):
        """j'ai encore des amelioratons à faire"""
        return self.état

    def jouer_coup(self, joueur):
        """ à un niveau je ne compends plus ce que je fais donc laisse seulement"""
        if joueur != 1 or joueur != 2:
            raise QuoridorError
        if self.partie_terminée() != False:
            raise QuoridorError
        état = self.état_partie()
        graphe = construire_graphe(
            [joueur['pos'] for joueur in état['joueurs']],
            état['murs']['horizontaux'],
            état['murs']['verticaux'])
        if joueur == 0:
            path = nx.shortest_path(graphe, état['joueurs'][joueur]['pos'], (5, 10))
            return path[0]
        if joueur == 1:
            path = nx.shortest_path(graphe, état['joueurs'][joueur]['pos'], (5, 0))
            return path[0]


    def partie_terminée(self):
        """ ici je m'interesse seulement de savoir si le pion 1 est arrive à la position (x, 9) et donc il a gagne quel que soit x"""
        if self.état['joueurs'][0]['pos'][1] == 9:
            return self.état['joueurs'][0]['nom']
        # si le pion 2 est à la position (x, 1) alors c"est le serveur qui gagne
        elif self.état['joueurs'][1]['pos'][1] == 1:
            return self.état['joueurs'][1]['nom']
        else:
            return False


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe=nx.DiGraph()

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
            successeur=(2*joueur[0]-prédécesseur[0],
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