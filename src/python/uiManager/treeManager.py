# -*- coding: utf-8 -*-

import wx


class Tree(object):

    def __init__(self):
        # Initialiser le nom, les enfants et le parent
        self.name = None
        self.children = []
        self.parent = None

    def next(self, child):
        # Récupérer l'enfant à un certain numéro
        return self.children[child]

    def parent(self):
        # Récupérer le parent
        return self.parent

    def goto(self, data):
        # Récupérer un enfant avec un certain nom
        for child in range(0, len(self.children)):
            if(self.children[child].name == data):
                return self.children[child]

    def add(self):
        # Ajouter un enfant
        node1 = Tree()
        self.children.append(node1)
        node1.parent = self
        return node1


class pyTree(wx.TreeCtrl):

    def __init__(self, tree, parent, id, style=''):
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
        # Pour chaque enfant de l'arbre
        for child in tree.children:
            # Si cet enfant à lui même des enfants
            if len(child.children) > 0:
                # Créer un nouveau groupe, et appeler cette même fonction avec un nouveau père
                newSubGroup = self.AppendItem(group, child.name.decode('utf-8'))
                self.addData(child, newSubGroup, level + 1)
            # Si cet enfant n'a pas d'enfants
            else:
                # L'ajouter au groupe actuel
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
