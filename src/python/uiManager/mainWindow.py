# -*- coding: utf-8 -*-

import wx
import os
import sys
from uiManager import treeManager
from uiManager import listManager
from pyxmlcast import *
from threading import Thread
from requestsManager import httpRequestManager
from uiManager import downloadManager

"""
TODO : Afficher du contenu récupéré d'autre part dans l'arbre (~ Done)
       Ajouter des vidéos aux Playlists avec le drag and drop (~ Done)
       Possibilité d'ajouter des chaînes
       Regarder les TODO en commentaire : ajouter une fonctionnalité au bouton refresh...
       ...
"""

# Set root path
try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

if('.exe' in approot):
    approot = approot.replace('LibreCast.exe', '')

if('uiManager' in approot):
    approot = approot.replace('/uiManager', '')


class AddAnUrl(wx.Dialog):

    def __init__(self, *args, **kw):
        super(AddAnUrl, self).__init__(*args, **kw)

        ws = self.GetWindowStyle()
        self.SetWindowStyle(ws & wx.STAY_ON_TOP)

        self.isDnD = False
        self.InstancesToDestroy = []

        # Initialisation du dialogue d'ajout
        self.InitUI()
        self.SetSize((300, 165))
        self.SetTitle('Add an URL')

    def InitUI(self):
        # Création du panel et des boxSizer associés
        pnl = wx.Panel(self)
        panelVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        mainVerticalBox = wx.BoxSizer(wx.VERTICAL)

        radioVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        # On créé les boutons radio et on créé des variables propres à l'objet, on peut donc y accéder dans la méthode OnChangeDepth
        createNewText = wx.StaticText(pnl, -1, 'Create a new ', style=wx.EXPAND)
        self.radioPlaylist = wx.RadioButton(pnl, label='Playlist', style=wx.RB_GROUP)
        self.radioURL = wx.RadioButton(pnl, label='URL')

        # On sélectionne le premier bouton  par défaut
        self.radioURL.SetValue(1)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioGroupSelected, self.radioPlaylist)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioURLSelected, self.radioURL)

        # On créé le texte. Même note que pour les boutons radio
        self.selectUrl = wx.TextCtrl(pnl)
        self.Text = wx.StaticText(pnl, -1, 'Select the URL\'s name: ', style=wx.EXPAND | wx.ALIGN_LEFT)

        # Ajouter les éléments aux différents sizer
        radioVerticalSizer.Add(createNewText, wx.ALIGN_TOP)
        radioVerticalSizer.Add(self.radioURL)
        radioVerticalSizer.Add(self.radioPlaylist)

        URLVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        URLVerticalSizer.Add(self.Text, 0, wx.ALIGN_BOTTOM)
        URLVerticalSizer.Add(self.selectUrl, 0, wx.EXPAND)

        # On ajoute les Sizer des boutons radio et du texte URL au Sizer du panel
        panelVerticalSizer.Add(radioVerticalSizer, 1, wx.LEFT | wx.EXPAND, 1)
        panelVerticalSizer.Add(URLVerticalSizer, 1, wx.LEFT | wx.EXPAND)

        # On applique le sizer au panel
        pnl.SetSizer(panelVerticalSizer)

        # Créer les boutons Ok et Cancel, et un sizer les contenant
        endButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Cancel')
        endButtonsSizer.Add(okButton)
        endButtonsSizer.Add(closeButton, flag=wx.LEFT, border=5)

        # Ajouter au sizer tous les élements de la fenêtre (panel et boutons de fin)
        mainVerticalBox.Add(pnl, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        mainVerticalBox.Add(endButtonsSizer, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Appliquer ce sizer à la fenêtre
        self.SetSizer(mainVerticalBox)

        # Appeler les fonction OnOk et OnClose aux boutons ok et cancel
        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnOk(self, event):
        # Fermer la fenêtre en renvoyant l'information que l'utilisateur a cliqué sur Ok
        self.EndModal(wx.ID_OK)

    def OnClose(self, event):
        # Fermer la fenêtre en renvoyant l'information que l'utilisateur a cliqué sur Annuler
        self.EndModal(wx.ID_ABORT)

    def OnRadioGroupSelected(self, event):
        # Changer le texte disant quel élément est créé (nouvelle playlist)
        self.Text.SetLabel('Select the Playlist\'s name : ')

    def OnRadioURLSelected(self, event):
        # Changer le texte disant quel élément est créé (nouvelle URL)
        self.Text.SetLabel('Select the URL\'s name : ')


class mainUI(wx.Frame):

    def __init__(self, parent, id, database):
        wx.Frame.__init__(self, parent, id)

        self.setDatabase(database)

        # Créer toute l'interface utilisateur
        self.InitUI()

    def setDatabase(self, database):
        self.database = database

    def InitUI(self):
        # Créer la barre de menus
        menubar = wx.MenuBar()
        # Créer un menu appelé 'File'
        fileMenu = wx.Menu()
        # Ajouter dans ce menu une option pour quitter. Sur Mac OSX, elle n'y sera pas car l'option est déjà présente par défaut dans un autre menu
        fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        # Ajouter le menu 'File' à la barre de menus
        menubar.Append(fileMenu, '&File')
        # Afficher la barre de menus dans l'application
        self.SetMenuBar(menubar)

        self.videosList = []

        # On ajoute une barre de menu edit
        editMenu = wx.Menu()
        menubar.Append(editMenu, '&Edit')

        # On lui ajoute une option refresh avec raccourci
        refreshItem = editMenu.Append(wx.ID_ANY, 'Refresh\tCtrl+R', 'Refresh feeds')
        self.Bind(wx.EVT_MENU, self.OnRefresh, refreshItem)

        # On ajoute un raccourci pour ajouter une playlist ou une URL
        addItem = editMenu.Append(wx.ID_ANY, 'Add new...\tCtrl+=', 'Add playlist or URL')
        self.Bind(wx.EVT_MENU, self.OnClickAddButton, addItem)

        # On ajoute un raccourci pour ajouter une playlist ou une URL
        removeItem = editMenu.Append(wx.ID_ANY, 'Remove\tCtrl+-', 'Remove selected item')
        self.Bind(wx.EVT_MENU, self.OnClickRemoveButton, removeItem)

        self.SetMenuBar(menubar)

        # On créé "l'arbre" avec les playlistes, les abonnements etc.
        self.CreateSplitter()

        # Créer la barre d'outils via la fonction locale (noter le 'b' minuscule dans 'bar')
        self.CreateToolbar()

        # Récupérer la taille de l'écran
        displaySize = wx.DisplaySize()
        # Modifier la taille de la fenêtre pour qu'elle fasse 4/5 de l'écran
        self.SetSize((9*displaySize[0]/10, 9*displaySize[1]/10))
        # Modifier la taille minimale de la fenêtre, pour éviter que tout devienne trop moche par manque de place...
        self.SetMinSize((500, 500))
        # Modifier le titre de la fenêtre
        self.SetTitle('LibreCast')
        # Centrer la fenêtre
        self.Centre()
        # Création de la fenêtre de téléchargement
        self.downloadManager = downloadManager.DownloaderFrame()
        self.downloadManager.Show(False)
        # Afficher la fenêtre
        self.Show(True)

    def CreateTree(self):
        # Créer un panel qui contient l'arbre et les bouttons ajouter/effacer
        self.panel = wx.Panel(self.split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, style=wx.SP_BORDER)
        # Modifier la couleur d'arrière plan du panel en gris clair
        self.panel.SetBackgroundColour('#F0F0F0')

        # Créer la racine principale de l'arbre
        sidebar_tree = treeManager.Tree()
        sidebar_tree.name = 'root'

        # Ajouter une branche playlists affiliée à sidebar_tree (racine)
        playlists_tree = sidebar_tree.add()
        playlists_tree.name = 'Playlists'

        # Ajouter une branche channels affiliée à sidebar_tree (racine)
        channels_tree = sidebar_tree.add()
        channels_tree.name = 'Abonnements'

        # Afficher les playlists de la base de données
        playlists = self.database.getPlaylists()
        print playlists

        feeds = self.database.getFeeds()
        print feeds

        for i in playlists:
            playlist = playlists_tree.add()
        # Vérifier l'encodage du nom des playlists (utf-8)
            playlist.name = i[0].encode('utf-8')

        for i in feeds:
            feed = channels_tree.add()
            feed.name = i[1].encode('utf-8')

        #for i in channelsContent:
        #    channel = channels.add()
        #    channel.name = i

        # Créer l'arbre (grâce au module treeManager) avec un style (effacer le style pour commprendre les modifications apportées)
        self.mainTree = treeManager.pyTree(sidebar_tree, self.panel, self.database, wx.ID_ANY, self.OnDragAndDropEnd, self.OnDragAndDropLeftTarget, self.OnDragAndDropEnteredTarget, self.OnClickRemoveButton, style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_NO_LINES | wx.TR_EDIT_LABELS)
        self.mainTree.ExpandAll()

        # Lorsqu'on élément de l'abre est sélectionné, on appelle la fonction
        self.mainTree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.mainTree)

        # Créer les images pour les boutons
        plusImage = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'add.png'))
        removeImage = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'remove.png'))
        # Modifier la taille des images
        plusImage.Rescale(12, 12)
        removeImage.Rescale(12, 12)
        # Créer les boutons
        addButton = wx.BitmapButton(self.panel, wx.ID_ANY, wx.BitmapFromImage(plusImage), style=wx.NO_BORDER)
        removeButton = wx.BitmapButton(self.panel, wx.ID_ANY, wx.BitmapFromImage(removeImage), style=wx.NO_BORDER)
        # Ajouter un évenement lorsque chaque bouton est cliqué
        self.Bind(wx.EVT_BUTTON, self.OnClickAddButton, addButton)
        self.Bind(wx.EVT_BUTTON, self.OnClickRemoveButton, removeButton)

        # Créer un sizer qui empêche les deux boutons de se superposer
        horizontalButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Ajouter un écart de 10 horizontalement avant les boutons
        horizontalButtonSizer.Add((10, -1), 0)
        # Ajouter le 1er boutton (bouton, resize, event, margin)
        horizontalButtonSizer.Add(addButton, 0, wx.ALL, 0)
        # Ajouter un écart de 20 horizontalement entre les boutons
        horizontalButtonSizer.Add((20, -1), 0)
        # Ajouter le 2ème bouton
        horizontalButtonSizer.Add(removeButton, 0, wx.ALL, 0)

        # Créer un sizer qui gère l'arbre et les boutons sous l'arbre
        verticalPanelSizer = wx.BoxSizer(wx.VERTICAL)
        # Ajouter l'arbre et le sizer horizontal (qui contient les boutons) au sizer vertical
        verticalPanelSizer.Add(self.mainTree, 1, wx.EXPAND | wx.ALL, 0)
        verticalPanelSizer.Add(horizontalButtonSizer, 0, wx.EXPAND | wx.ALL, 5)
        # Ajouter ce sizer au panel
        self.panel.SetSizer(verticalPanelSizer)

    def CreateVideoList(self, videoList):
        self.videoList = None
        # Créer la liste de vidéos (grâce au module listManager) avec un style (effacer le style pour commprendre les modifications apportées)
        self.videoList = listManager.pyList(self.split, wx.ID_ANY, videoList, self.OnDragAndDropStart, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.SUNKEN_BORDER)

    def CreateSplitter(self):
        # Créer un 'spliter' qui permet de couper l'écran en deux parties avec un style (la limite se déplace en temps réel)
        # Note : SP_NOSASH enpêche de redimensionner le spliter
        self.split = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_LIVE_UPDATE | wx.SP_NOBORDER)
        # Limiter la taille des deux parties de l'arbre à 150, pour des raison estétiques et pratiques
        self.split.SetMinimumPaneSize(150)
        self.CreateTree()
        self.CreateVideoList(self.videosList)
        # Couper l'écran en deux avec à gauche le panel (avec une taille par défaut de 200) et à droite la liste de vidéos
        self.split.SplitVertically(self.panel, self.videoList, 210)

    def CreateToolbar(self):
        # Créer la barre d'outils avec refresh et search (noter le 'B' majuscule dans 'Bar')
        toolbar = self.CreateToolBar()

        # Créer une variable qui contient l'image refresh.png dans le dossier resources
        refreshImage = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'refresh.png'))
        # Ajouter un bouton avec l'image refresh
        refreshTool = toolbar.AddLabelTool(wx.ID_ANY, 'Refresh', wx.BitmapFromImage(refreshImage), shortHelp='Refresh feeds')
        # Ajouter un évenement lorsque le bouton est cliqué (la fonction OnRefresh est appellée)
        self.Bind(wx.EVT_TOOL, self.OnRefresh, refreshTool)

        # Créer une variable qui contient l'image refresh.png dans le dossier resources
        downloadImage = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'downloads.png'))
        # Ajouter un bouton avec l'image refresh
        downloadTool = toolbar.AddLabelTool(wx.ID_ANY, 'Downloads', wx.BitmapFromImage(downloadImage), shortHelp='Downloads window')
        # Ajouter un évenement lorsque le bouton est cliqué (la fonction OnRefresh est appellée)
        self.Bind(wx.EVT_TOOL, self.OnShowDownloadWindow, downloadTool)

        # Ajouter un séparateur
        toolbar.AddSeparator()
        # AddStrechableSpace()

        # Créer une barre de recherche
        self.searchbar = wx.SearchCtrl(toolbar, wx.ID_ANY, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        # Afficher le bouton annuler dans la barre de recherche
        self.searchbar.ShowCancelButton(True)
        # Afficher 'Search online content' par défaut dans la barre de recherche
        self.searchbar.SetDescriptiveText('Search online content')
        # Ajouter la barre de recherche
        searchbarctrl = toolbar.AddControl(self.searchbar)
        # Ajouter un évenement lorsque le texte change
        self.Bind(wx.EVT_TEXT, self.OnSearchTextChanged, searchbarctrl)
        # Ajouter un évenement lorsque l'utilisateur appuye sur entrée (fonctionne pas sur OS X apparement...)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearchTextChanged, searchbarctrl)

        # Afficher tous les éléments ajoutés ci-dessus
        toolbar.Realize()

        # Modifier la taille des icones de la barre d'outils
        toolbar.SetToolBitmapSize((32, 32))

    def RebuildTree(self):
        # Sauvegarde et suppression de l'ancien panel; remplacement par le nouvel panel
        oldPanel = self.panel
        self.CreateTree()
        self.split.ReplaceWindow(oldPanel, self.panel)
        oldPanel.Destroy()

    def RebuildList(self):
        #TODO: Comments
        oldList = self.videoList

        self.CreateVideoList(self.videosList)
        self.split.ReplaceWindow(oldList, self.videoList)
        wx.CallAfter(oldList.Destroy)

    def OnDragAndDropStart(self):
        # Fonction appelée lorsque l'utilisateur commence un glisser-déposer
        self.isDnD = True
        self.InstancesToDestroy = []

        # Lorsque l'on sort de la zone de dépot du glisser-déposer
    def OnDragAndDropLeftTarget(self):
        self.isDnD = False

        # Lorsque l'on entre dans la zone de dépot du glisser-déposer
    def OnDragAndDropEnteredTarget(self):
        self.isDnD = True

    def OnDragAndDropEnd(self):
        self.isDnD = False

    def OnSelChanged(self, e):
        if not hasattr(self, 'isDnD'):
            self.isDnD = False

        if not self.isDnD:
            item = self.mainTree.GetSelection()

            if self.mainTree.GetItemText(self.mainTree.GetItemParent(item)) == 'Playlists':
                playlistID = self.database.getPlaylistIDFromName(self.mainTree.GetItemText(item))
                self.videosList = self.database.getVideosFromPlaylist(playlistID)
                self.RebuildList()
            elif self.mainTree.GetItemText(self.mainTree.GetItemParent(item)) == 'Abonnements':
                fluxID = self.database.getFeedIDFromURL(self.mainTree.GetItemText(item))
                self.videosList = self.database.getVideosFromFeed(fluxID)
                self.RebuildList()

    def OnRefresh(self, event):
        # Rafraîchissement de la fenêtre, dans une thread séparée
        # pour éviter de bloquer l'interface
        thread = Thread(target=self.refreshFlux, args=[])
        wx.CallAfter(thread.run)

    def refreshFlux(self):
        feeds = self.database.getFeeds()

        for feed in feeds:
            url = feed[1]
            xmlContent = httpRequestManager.OpenUrl(url+"/flux.xml")

            # URL invalide
            if not xmlContent[1]:
                pass

            parsedCast = PyXMLCast(xmlContent[0])
            videos = parsedCast.getAllVideos()
            for video in videos:
                self.database.insertVideo(
                    video['title'],
                    video['url'],
                    video['length'],
                    video['author'],
                    video['pubdate'],
                    feed[0]
                )
        print self.database.getAllVideos()

    def OnClickAddButton(self, event):
        # Creation du dialogue
        addurl = AddAnUrl(None, title='Add an URL')
        # On affiche le dialogue
        modal = addurl.ShowModal()

        # Si le résultat est le bouton 'ok'
        if modal == wx.ID_OK and addurl.selectUrl.GetValue():
            # Si le bouton radio des playlist est sélectionné
            if addurl.radioPlaylist.GetValue():
                # Si une playlist ne porte pas déjà ce nom
                if self.database.getPlaylistIDFromName(addurl.selectUrl.GetValue()) == -1:
                    self.database.createPlaylist(addurl.selectUrl.GetValue())
            else:
                if self.database.getFeedIDFromURL(addurl.selectUrl.GetValue()) == -1:
                    self.database.insertFeed(addurl.selectUrl.GetValue())

            self.RebuildTree()

    def OnClickRemoveButton(self, event):
        # Fonction de suppression d'items/feeds de l'arbre sélectionnés
        item = self.mainTree.GetSelection()

        if self.mainTree.GetItemParent(item) == self.mainTree.GetRootItem():
            print('Cannot remove this item')
        else:
            if self.mainTree.GetItemText(self.mainTree.GetItemParent(item)) == 'Playlists':
                playlistID = self.database.getPlaylistIDFromName(self.mainTree.GetItemText(item))
                self.database.removePlaylist(playlistID)
            else:
                feedID = self.database.getFeedIDFromURL(self.mainTree.GetItemText(item))
                self.database.removeFeed(feedID)
        # Application des changements à l'arbre
            self.RebuildTree()

    def OnSearch(self, event):
        # Fonction de la barre de recherche
        texte = self.searchbar.GetValue()

        if texte != '':
            print('Rechercher : ' + texte)
        else:
            print('Ne pas rechercher')

    def OnSearchTextChanged(self, event):
        # Si le texte recherché n'est pas vide, récupérer la valeur de la recherche
        texte = self.searchbar.GetValue()

        if texte != '':
            print('Nouvelle recherche : ' + texte)
        else:
            print('Aucune recherche')

    def OnShowDownloadWindow(self, event):
        self.downloadManager.Show(True)
        self.downloadManager.AddDownload('lol', 'lol2')
        self.downloadManager.AddDownload('lol', 'lol2')
        self.downloadManager.AddDownload('lol', 'lol2')


# Méthode appelée depuis le fichier principal pour créer l'interface graphique
def main(database_instance):
    ex = wx.App(0)
    ex.SetAppName('LibreCast')
    mainUI(None, wx.ID_ANY, database_instance)
    ex.MainLoop()
