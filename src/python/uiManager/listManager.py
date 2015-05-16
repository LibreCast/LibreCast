# -*- coding: utf-8 -*-

import wx
import cPickle
from uiManager import videoManager

"""
TODO : Ajouter des vidéos aux Playlists avec le drag and drop (~ Done)
       Modifier l'icone de DnD, avec l'image "DnD.png"
       Changer la vidéo affichée lorsqu'on double click dessus
       Possibilité de renommer les playlists
       ...
"""

# Durée : 0:04:03
# URL = 'http://download.wavetlan.com/SVV/Media/HTTP/MP4/ConvertedFiles/Media-Convert/Unsupported/dw11222.mp4'
# Durée : 0:02:48
# URL = 'http://www.boisestatefootball.com/sites/default/files/videos/original/01%20-%20coach%20pete%20bio_4.mp4'
# Durée : 0:01:25
# URL = 'https://km.support.apple.com/library/APPLE/APPLECARE_ALLGEOS/HT1211/sample_iTunes.mov'
# Durée : 0:00:52
# URL = 'http://media.w3.org/2010/05/sintel/trailer.mp4'
# Durée : 27:25
# URL = 'http://samples.mplayerhq.hu/mov/quicktime.mov'
# Durée : 0:09:56
URL = 'http://download.blender.org/peach/bigbuckbunny_movies/big_buck_bunny_720p_h264.mov'


class pyList(wx.ListCtrl):
    def __init__(self, parent, id, videoList, onDnDStartMethod, downloadVideo, style=''):
        wx.ListCtrl.__init__(self, parent, id)

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

        # Ajouter 4 colonnes : Le titre, le créateur de la vidéo, la date et la durée de la vidéo
        self.InsertColumn(0, 'Title')
        self.InsertColumn(1, 'Author')
        self.InsertColumn(2, 'Date')
        self.InsertColumn(3, 'Length')

        self.URLsByIndex = []

        # On décompose les données délivrées avec la liste, et on les affiche dans celle-ci
        # Note : À étudier en même temps que la variable 'data', puisque c'est de là qu'on extrait les données
        if isinstance(videoList, list):
            for video in videoList:
                try:
                    self.AddLine(video[1], video[4], video[5], video[3])
                    self.URLsByIndex.append((video[2], video[1]))
                except Exception, e:
                    print e

        # Modifier la largeur des 4 colonnes afin que le contenu de chacune soit entièrement affiché
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        # Appeler la fonction PlayVideo lorsqu'une ligne est double cliquée, ou que l'utilisateur appuye sur entrée en ayant sélectionné une ligne
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.PlayVideo, self)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.startDrag)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClicked)

    def OnRightClicked(self, event):
        #TODO: Comments
        self.list_item_clicked = event.GetIndex()

        menu_titles = ['Download']

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

        if operation == 'Download':
            wx.CallAfter(self.DownloadURLAtIndex, index)

    def DownloadURLAtIndex(self, index):
        if index >= 0:
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

    def AddLine(self, title, author, date, length):
        # Ajouter le contenu dans chaque colone, en le décodant en utf-8 afin d'éviter les problèmes d'accents etc.
        # Note : self.index correspond à l'index après lequel la ligne est ajoutée
        self.InsertStringItem(self.index, title.decode('utf-8'))
        self.SetStringItem(self.index, 1, author.decode('utf-8'))
        self.SetStringItem(self.index, 2, date.decode('utf-8'))
        self.SetStringItem(self.index, 3, length.decode('utf-8'))

        # L'index de la dernière ligne doit être incrémenté
        self.index += 1

    def PlayVideo(self, event):
        print 'Lancer la vidéos à l\'index ' + str(event.GetIndex())
        # Afficher une fenêtre avec la vidéo située à l'URL donnée
        videoManager.videoWindow(self, wx.ID_ANY, self.URLsByIndex[event.GetIndex()][0])
