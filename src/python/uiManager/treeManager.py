# -*- coding: utf-8 -*-

import wx
import cPickle

localTree = None


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

        global localTree
        localTree = self

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

                if self.GetItemText(group) == "Playlists":
                    print "Drag target:", child.name.decode('utf-8')
                    self.SetDropTarget(ListDrop(child))

    def insert(self, title, x, y):
        index, flags = self.HitTest((x, y))
        # playlist = self.GetFirstChild(self.GetRootItem())

        if index.IsOk() and localTree.GetItemText(localTree.GetItemParent(localTree.GetSelection())) == "Playlists":
            # Should add video to playlist with index
            print 'Should add video "' + title[0] + '"' + ' to playlist "' + self.GetItemText(index) + '"'

    def SetOutput(self, output):
        """
        Permet d'ajouter la fonction permettant de modifier la
        liste située à droite de l'abre.
        """
        self.output = output


class ListDrop(wx.PyDropTarget):

    def __init__(self, source):
        wx.PyDropTarget.__init__(self)

        # specify the type of data we will accept
        self.data = wx.CustomDataObject("ListCtrlItems")
        self.SetDataObject(self.data)

    def OnDragOver(self, x, y, d):
        # provide visual feedback by selecting the item the mouse is over
        item, flags = localTree.HitTest((x, y))
        selections = localTree.GetSelections()

        if item:
            if selections != [item]:
                localTree.UnselectAll()
                localTree.SelectItem(item)
                selectedItem = localTree.GetSelection()

                if localTree.GetItemText(localTree.GetItemParent(selectedItem)) != "Playlists":
                    localTree.UnselectAll()

        elif selections:
            localTree.UnselectAll()

        return d

    # Called when OnDrop returns True.  We need to get the data and
    # do something with it.
    def OnData(self, x, y, d):
        # copy the data from the drag source to our data object
        if self.GetData():
            # convert it back to a list and give it to the viewer
            ldata = self.data.GetData()
            l = cPickle.loads(ldata)
            localTree.insert(l, x, y)

        # what is returned signals the source what to do
        # with the original data (move, copy, etc.)  In this
        # case we just return the suggested value given to us.
        return d
