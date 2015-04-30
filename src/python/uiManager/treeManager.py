# -*- coding: utf-8 -*-

import wx
import cPickle


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

        # Par défaut, on ne sait pas s'il y a une zone de texte modifiable
        self.output = None

    def addData(self, tree, group, level=0):
        self.SetDropTarget(ListDrop(self))

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

    def insert(self, title, x, y):
        # Récuppérer l'élément dans lequel il faut ajouter la vidéo
        index, flags = self.HitTest((x, y))

        # Si l'élément existe, et que c'est bien une playlist
        if index.IsOk() and self.GetSelection() and self.GetItemText(self.GetItemParent(self.GetSelection())) == "Playlists":
            #TODO
            print 'Should add video "' + title[0] + '"' + ' to playlist "' + self.GetItemText(index) + '"'


class ListDrop(wx.PyDropTarget):

    def __init__(self, source):
        wx.PyDropTarget.__init__(self)

        self.source = source

        # Dire quel type de données sont acceptées
        self.data = wx.CustomDataObject("ListCtrlItems")
        self.SetDataObject(self.data)

    def OnDragOver(self, x, y, d):
        # Montrer sur quel objet le Drag and Drop se fait
        item, flags = self.source.HitTest((x, y))
        selections = self.source.GetSelections()

        # Si l'objet sur lequel la souris se situe appartiens bien à cette classe
        if item:
            # Si l'objet n'est pas actuellement sélectionné
            if selections != [item]:
                # Déselectionner tous les éléments de l'arbre puis sélectionner cet élément
                self.source.UnselectAll()
                self.source.SelectItem(item)

                # Réccupérer l'élément sélectionné (pas sous forme d'index, contrairement à HitTest)
                selectedItem = self.source.GetSelection()

                try:
                    # Si l'élément n'a pas pour parent "Playlists"
                    if self.source.GetItemText(self.source.GetItemParent(selectedItem)) != "Playlists":
                        # Le désélectionner
                        self.source.UnselectAll()
                except wx.PyAssertionError:
                    # Le group acutel est root, crash sous windows
                    self.source.UnselectAll()

        # Sinon
        elif selections:
            # Tout déselectionner dans l'arbre
            self.source.UnselectAll()

        return d

    def OnData(self, x, y, d):
        # Si le Drag and Drop contient des données
        if self.GetData():
            # Réccupérer ces données, et les convertir d'octets en une liste
            # Note : Évènement contraire de ce qu'il se passe dans "startDrag" de "listManager.py"
            ldata = self.data.GetData()
            l = cPickle.loads(ldata)

            # Dire à l'arbre qu'il faut insérer ces données dans une playlist
            self.source.insert(l, x, y)

        return d
