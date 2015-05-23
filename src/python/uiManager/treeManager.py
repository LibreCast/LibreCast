# -*- coding: utf-8 -*-

import wx
import os
import sys
import cPickle
from threading import Thread
from cStringIO import StringIO
from requestsManager import httpRequestManager

"""
TODO : Sauvegarder le fait qu'une playlist est renommée
       ...
"""


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

# Set root path
try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

if('.exe' in approot):
    approot = approot.replace('LibreCast.exe', '')

if('uiManager' in approot):
    approot = approot.replace('/uiManager', '')


class pyTree(wx.TreeCtrl):

    def __init__(self, tree, parent, database, id, onDnDEndMethod, onDnDLeftTargetMethod, OnDnDEnteredTarget, RemoveMethod, style=''):
        """
        Initialize function
        """
        wx.TreeCtrl.__init__(self, parent, id)

        self.database = database
        self.onDnDEndMethod = onDnDEndMethod
        self.onDnDLeftTargetMethod = onDnDLeftTargetMethod
        self.OnDnDEnteredTarget = OnDnDEnteredTarget
        self.OnClickRemoveButton = RemoveMethod

        # Si au moins un style a été précisé dans la création de l'abre...
        if style:
            # ...on l'applique
            self.SetWindowStyle(style)

        # On créer la racine de l'arbre, c'est ce qui contiendra toutes nos
        # playlistes etc. On choisit de ne pas l'afficher, mais uniquement son
        # contenu (cf. styles)
        self.root = self.AddRoot('Data')

        self.feeds = []
        self.imageList = wx.ImageList(16, 16)
        self.AssignImageList(self.imageList)

        # On décompose les données délivrées avec l'arbre, et on les affiche dans ce dernier
        # Note : À étudier en même temps que la variable 'data', puisque c'est
        # de là qu'on extrait les données
        self.addData(tree, self.root)

        wx.CallAfter(self.startThread)

        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnPlaylistRenamed)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnPlaylistWillBeRenamed)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClicked)

    def startThread(self):
        feedsList = []
        for feed in self.database.getFeeds():
            feedsList.append(feed[2])

        self.thread = Thread(target=self.loadImages, args=[feedsList, self.feeds, 0])
        self.thread.setDaemon(False)
        wx.CallLater(100, self.thread.start)

    def OnPlaylistRenamed(self, event):
        #TODO: Save changes in database
        if event.GetLabel() != '':
            playlistID = self.database.getPlaylistIDFromName(self.GetItemText(event.GetItem()))
            self.database.renamePlaylist(playlistID, event.GetLabel())

    def OnPlaylistWillBeRenamed(self, event):
        #TODO: Comments

        if self.GetItemText(self.GetItemParent(self.GetSelection())) != 'Playlists':
            event.Veto()

    def OnRightClicked(self, event):
            #TODO: Comments
            self.list_item_clicked = event.GetItem()

            if self.GetItemText(self.GetItemParent(self.GetSelection())) == 'Playlists':
                menu_titles = ['Rename', 'Delete']
            elif self.GetItemParent(self.GetSelection()) != self.GetRootItem():
                menu_titles = ['Delete']

            menu = wx.Menu()
            self.menu_title_by_id = {}
            for title in menu_titles:
                itemId = wx.NewId()
                self.menu_title_by_id[itemId] = title
                menu.Append(itemId, title)
                wx.EVT_MENU(menu, itemId, self.OnMenuSelected)

            self.PopupMenu(menu, event.GetPoint())
            menu.Destroy()

    def OnMenuSelected(self, event):
        #TODO: Comments
        operation = self.menu_title_by_id[event.GetId()]
        target = self.list_item_clicked

        if operation == 'Delete':
            wx.CallAfter(self.OnClickRemoveButton, event)
        elif operation == 'Rename':
            self.EditLabel(target)

    def addData(self, tree, group, level=0):
        self.SetDropTarget(ListDrop(self, self.onDnDEndMethod, self.onDnDLeftTargetMethod, self.OnDnDEnteredTarget))

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
                newItem = self.AppendItem(group, child.name.decode('utf-8'))
                if self.GetItemText(group) == 'Abonnements':
                    self.feeds.append(newItem)
                    image = self.imageList.Add(wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'defaultChannelIcon.png')).Scale(16, 16).ConvertToBitmap())
                    self.SetItemImage(newItem, image, wx.TreeItemIcon_Normal)

    def loadImages(self, feedUrls, feeds, index):
        if index < len(feedUrls):
            try:
                data = httpRequestManager.OpenUrl(feedUrls[index])[0].read()
                bmp = self.imageList.Add(wx.ImageFromStream(StringIO(data)).Scale(16, 16).ConvertToBitmap())
            except:
                print 'except: download failed'

            try:
                self.SetItemImage(feeds[index], bmp, wx.TreeItemIcon_Normal)
                self.loadImages(feedUrls, feeds, index + 1)
            except:
                print 'self does not exist'
                return

    def insert(self, title, x, y):
        # Récuppérer l'élément dans lequel il faut ajouter la vidéo
        index, flags = self.HitTest((x, y))

        # Si l'élément existe, et que c'est bien une playlist
        if index.IsOk() and self.GetSelection() and self.GetItemText(self.GetItemParent(self.GetSelection())) == 'Playlists':
            #TODO
            playlistID = self.database.getPlaylistIDFromName(self.GetItemText(index))
            videoID = self.database.getVideoIDFromName(title[0])
            if playlistID != -1 and videoID != -1:
                self.database.insertVideoInPlaylist(videoID, playlistID)


class ListDrop(wx.PyDropTarget):

    def __init__(self, source, onDnDEndMethod, onDnDLeftTargetMethod, OnDnDEnteredTarget):
        wx.PyDropTarget.__init__(self)

        self.source = source
        self.onDnDEndMethod = onDnDEndMethod
        self.onDnDLeftTargetMethod = onDnDLeftTargetMethod
        self.OnDnDEnteredTarget = OnDnDEnteredTarget

        # Dire quel type de données sont acceptées
        self.data = wx.CustomDataObject('ListCtrlItems')
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
                    if self.source.GetItemText(self.source.GetItemParent(selectedItem)) != 'Playlists':
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

    def OnLeave(self):
        self.onDnDLeftTargetMethod()

    def OnEnter(self, x, y, d):
        self.OnDnDEnteredTarget()

    def OnData(self, x, y, d):
        self.onDnDEndMethod()

        # Si le Drag and Drop contient des données
        if self.GetData():
            # Réccupérer ces données, et les convertir d'octets en une liste
            # Note : Évènement contraire de ce qu'il se passe dans "startDrag" de "listManager.py"
            ldata = self.data.GetData()
            l = cPickle.loads(ldata)

            # Dire à l'arbre qu'il faut insérer ces données dans une playlist
            self.source.insert(l, x, y)

        return d
