# -*- coding: utf-8 -*-

import wx
from uiManager import videoManager

"""
Exemple de données possibles que l'on peut réccupérer du xml.
Il vaudrait mieux implémenter une fonction réccursive afin de
pourvoir avoir autant de sous-groupes que l'on veut, mais
les specs n'en prévoient qu'un nombre donné.
"""
data = [['TiBounise & co',  'TiBounise Official', '11 mars 2015', '1:50'],
        ['L\'année de la catastrophe', 'TF1', '13 février 2001', '1:34:28'],
        ['Merci d\'utiliser LibreCast !', 'LibreCast', '1er janvier 1970', '3:05'],
        ]
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
    def __init__(self, parent, id, style=''):
        wx.ListCtrl.__init__(self, parent, id)

        # Si au moins un style a été précisé dans la création de l'abre...
        if style != '':
            # ...on l'applique
            self.SetWindowStyle(style)
        else:
            self.SetWindowStyle(wx.LC_REPORT)

        # Variable stockant l'index du dernier élément de la liste, pour pouvoir ajouter une ligne à la fin de la liste
        self.index = 0

        # Ajouter 4 colonnes : Le titre, le créateur de la vidéo, la date et la durée de la vidéo
        self.InsertColumn(0, 'Title')
        self.InsertColumn(1, 'Author')
        self.InsertColumn(2, 'Date')
        self.InsertColumn(3, 'Length')

        # On décompose les données délivrées avec la liste, et on les affiche dans celle-ci
        # Note : À étudier en même temps que la variable 'data', puisque c'est de là qu'on extrait les données
        if isinstance(data, list):
            for video in data:
                try:
                    self.AddLine(video[0], video[1], video[2], video[3])
                except Exception, e:
                    print e

        # Modifier la largeur des 4 colonnes afin que le contenu de chacune soit entièrement affiché
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)

        # Appeler la fonction PlayVideo lorsqu'une ligne est double cliquée, ou que l'utilisateur appuye sur entrée en ayant sélectionné une ligne
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.PlayVideo, self)

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
        videoManager.videoWindow(self, wx.ID_ANY, URL)
