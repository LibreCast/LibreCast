# -*- coding: utf-8 -*-

import wx
import os
import sys
import cPickle
from cStringIO import StringIO
from uiManager import videoManager
from requestsManager import httpRequestManager
from email.utils import parsedate
import time
from datetime import datetime

"""
TODO : Ajouter des vidéos aux Playlists avec le drag and drop (~ Done)
       Modifier l'icone de DnD, avec l'image "DnD.png"
       Possibilité de renommer les playlists
       ...
"""


class pyList(wx.ListCtrl):
    def __init__(self, parent, id, videoList, onDnDStartMethod, downloadVideo, style=''):
        wx.ListCtrl.__init__(self, parent, id)

        # Set root path
        try:
            approot = os.path.dirname(os.path.abspath(__file__))
        except NameError:  # We are the main py2exe script, not a module
            approot = os.path.dirname(os.path.abspath(sys.argv[0]))

        if('.exe' in approot):
            approot = approot.replace('LibreCast.exe', '')

        if('uiManager' in approot):
            approot = approot.replace('/uiManager', '')

        self.onDnDStartMethod = onDnDStartMethod
        self.downloadVideo = downloadVideo

        # Si au moins un style a été précisé dans la création de l'abre...
        if style != '':
            # ...on l'applique
            self.SetWindowStyle(style)
        else:
            self.SetWindowStyle(wx.LC_REPORT)

        self.dropSource = wx.DropSource(self)

        # Variable stockant l'index du dernier élément de la liste, pour pouvoir ajouter une ligne à la fin de la liste
        self.index = 0

        # Ajouter 5 colonnes : une image, le titre, le créateur de la vidéo, la date et la durée de la vidéo
        self.InsertColumn(0, 'Titre')
        self.InsertColumn(1, 'Auteur')
        self.InsertColumn(2, 'Date')
        self.InsertColumn(3, 'Durée')

        self.imageList = wx.ImageList(72, 48)
        self.SetImageList(self.imageList, wx.IMAGE_LIST_SMALL)

        self.URLsByIndex = []

        # On décompose les données délivrées avec la liste, et on les affiche dans celle-ci
        # Note : À étudier en même temps que la variable 'data', puisque c'est de là qu'on extrait les données
        if isinstance(videoList, list):
            for video in videoList:
                try:
                    data = httpRequestManager.OpenUrl(video[6])[0].read()
                    bmp = wx.ImageFromStream(StringIO(data)).Scale(72, 48).ConvertToBitmap()
                except Exception, e:
                    print e
                    bmp = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'defaultVideoImage.png')).Scale(72, 48).ConvertToBitmap()
                try:
                    dateFR = datetime.fromtimestamp(time.mktime(parsedate(video[5]))).strftime("%d/%m/%Y")
                    self.AddLine(bmp, video[1], video[4], dateFR, video[3])
                    self.URLsByIndex.append((video[2], video[1]))
                except Exception, e:
                    print e

        # Modifier la largeur des 4 colonnes afin que le contenu de chacune soit entièrement affiché
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(0, self.GetColumnWidth(0) + 80)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        # Appeler la fonction PlayVideo lorsqu'une ligne est double cliquée, ou que l'utilisateur appuye sur entrée en ayant sélectionné une ligne
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.PlayVideo, self)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClicked)

    def OnRightClicked(self, event):
        #TODO: Comments
        self.list_item_clicked = event.GetIndex()

        if self.list_item_clicked >= 0:
            menu_titles = ['Télécharger la vidéo', 'Copier l\'adresse']

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
        index = self.list_item_clicked

        if operation == 'Télécharger la vidéo':
            wx.CallAfter(self.DownloadURLAtIndex, index)
        elif operation == 'Copier l\'adresse':
            clipdata = wx.TextDataObject()
            clipdata.SetText(self.URLsByIndex[index][0])
            wx.TheClipboard.Open()
            wx.TheClipboard.SetData(clipdata)
            wx.TheClipboard.Close()

    def DownloadURLAtIndex(self, index):
        self.downloadVideo(self.URLsByIndex[index][0], self.URLsByIndex[index][1])

    def startDrag(self, e):
        self.onDnDStartMethod()

        # Créer les données à transférer
        l = []
        idx = -1
        # Réccuppérer l'object de la liste sélectionné
        idx = self.GetFocusedItem()

        # Si idx n'a pas d'erreur
        if idx != -1:
            item = self.GetItem(idx, 0).GetText()

            # Sinon, ajouter l'objet à nos données
            l.append(item)

        # Convertir la liste de données en octets
        itemdata = cPickle.dumps(l, 1)

        # Créer un format de données personnalisé
        ldata = wx.CustomDataObject('ListCtrlItems')
        ldata.SetData(itemdata)

        # Créer les données qui vont être transférées
        data = wx.DataObjectComposite()
        data.Add(ldata)

        # Créer une source de Drag and Drop
        self.dropSource.SetData(data)

        # Commencer le drag and drop
        self.dropSource.DoDragDrop()

    def AddLine(self, bitmap, title, author, date, length):
        # Ajouter le contenu dans chaque colone
        # Note : self.index correspond à l'index après lequel la ligne est ajoutée
        imgId = self.imageList.Add(bitmap)
        self.InsertStringItem(self.index, title)
        self.SetItemImage(self.index, imgId)
        self.SetStringItem(self.index, 1, author)
        self.SetStringItem(self.index, 2, date)
        self.SetStringItem(self.index, 3, length)

        # L'index de la dernière ligne doit être incrémenté
        self.index += 1

    def PlayVideo(self, event):
        # Afficher une fenêtre avec la vidéo située à l'URL donnée
        videoManager.videoWindow(self, wx.ID_ANY, self.URLsByIndex[event.GetIndex()][0])
