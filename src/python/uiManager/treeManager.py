# -*- coding: utf-8 -*-

import wx


# Classe permettant la création d'un arbre avec autant d'enfants que l'on veut, qui conserve sont ordre et qui peut avoir plusieurs enfants avec les même noms
class treeData(object):
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def getString(self):
        ret = repr(self.value)
        return ret


# Données servants d'example
data = treeData('Root', [
    treeData('Playlist', [
        treeData('Vidéo'),
        treeData('Vidéo'),
        treeData('Encore une vidéo')]),
    treeData('Abonnements', [
        treeData("¡Chaîne!"),
        treeData('"Chaîne"')])
])


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

        # On créer la racine de l'arbre, c'est ce qui contiendra toutes nos playlistes etc. On choisit de ne pas l'afficher, mais uniquement son contenu (cf. styles)
        self.root = self.AddRoot('Data')

        # On décompose les données délivrées avec l'arbre, et on les affiche dans ce dernier
        # Note : À étudier en même temps que la variable 'data', puisque c'est de là qu'on extrait les données
        self.addData(data, group=self.root)

        # Lorsqu'on élément de l'abre est sélectionné, on appelle la fonction OnSelChanged
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=self.GetId())

        # Par défaut, on ne sait pas s'il y a une zone de texte modifiable
        self.output = None

    def addData(self, data, level=0, group=False):
        if not group:
            group = self.AppendItem(self.root, group.decode('utf-8'))
        for child in data.children:
            if len(child.children) > 0:
                newSubGroup = self.AppendItem(group, child.value.decode('utf-8'))
                self.addData(child, level+1, newSubGroup)
            else:
                self.AppendItem(group, child.value.decode('utf-8'))

    def SetOutput(self, output):
        """
        Permet d'ajouter la fonction permettant de modifier la
        liste située à droite de l'abre.
        """
        self.output = output

    def OnSelChanged(self, event):
        # Si on n'a pas ajouté la zone de texte avec SetOutput, on ne peut pas modifier le texte
        if not self.output:
            return

        # Sinon, on affiche le texte
        apply(self.output, ('Not done yet'))
