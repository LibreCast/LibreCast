# -*- coding: utf-8 -*-

import wx


class Tree(object):

    def __init__(self):
        self.name = None
        self.children = []
        self.parent = None

    def nex(self, child):
        "Gets a child by number"
        return self.children[child]

    def parent(self):
        return self.parent

    def goto(self, data):
        "Gets the children by name"
        for child in range(0, len(self.children)):
            if(self.children[child].name == data):
                return self.children[child]

    def add(self):
        node1 = Tree()
        self.children.append(node1)
        node1.parent = self
        return node1

"""
On créé l'arbre à partir des listes de chaînes et des playlists données.
"""

tree = Tree()
tree.name = "root"

playlists = tree.add()
playlists.name = 'Playlists'

channels = tree.add()
channels.name = 'Abonnements'

playlistContent = ['Vidéo', 'Vidéo', 'Encore une vidéo']
channelsContent = ['"Vidéo"', '¿Vidéo?', '¡Vidéo!']

for i in playlistContent:
    playlist = playlists.add()
    playlist.name = i

for i in channelsContent:
    channel = channels.add()
    channel.name = i


class pyTree(wx.TreeCtrl):

    def __init__(self, parent, id, style=''):
        """
        Initialize function
        """
        wx.TreeCtrl.__init__(self, parent, id)

        # Si au moins un style a été précisé dans la création de l'abre...
        if style:
            # ...on l'applique
            self.SetWindowStyle(style)

        # On créer la racine de l'arbre, c'est ce qui contiendra toutes nos
        # playlistes etc. On choisit de ne pas l'afficher, mais uniquement son
        # contenu (cf. styles)
        self.root = self.AddRoot('Data')

        # On décompose les données délivrées avec l'arbre, et on les affiche dans ce dernier
        # Note : À étudier en même temps que la variable 'data', puisque c'est
        # de là qu'on extrait les données
        self.addData(tree, self.root)

        # Lorsqu'on élément de l'abre est sélectionné, on appelle la fonction
        # OnSelChanged
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=self.GetId())

        # Par défaut, on ne sait pas s'il y a une zone de texte modifiable
        self.output = None

    def addData(self, tree, group, level=0):
        for child in tree.children:
            if len(child.children) > 0:
                newSubGroup = self.AppendItem(group, child.name.decode('utf-8'))
                self.addData(child, newSubGroup, level + 1)
            else:
                self.AppendItem(group, child.name.decode('utf-8'))

    def SetOutput(self, output):
        """
        Permet d'ajouter la fonction permettant de modifier la
        liste située à droite de l'abre.
        """
        self.output = output

    def OnSelChanged(self, event):
        # Si on n'a pas ajouté la zone de texte avec SetOutput, on ne peut pas
        # modifier le texte
        if not self.output:
            return

        # Sinon, on affiche le texte
        apply(self.output, ('Not done yet'))
