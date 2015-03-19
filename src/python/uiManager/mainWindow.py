# -*- coding: utf-8 -*-

import wx
import os
import sys
from uiManager import treeManager
from uiManager import listManager

"""
TODO : Découper le contenu en plusieurs fichiers, avec notamment un pour la recherche et un pour l'arbre (~ Done)
       Ajouter de réelles fonctionnalitées aux boutons
       Afficher du contenu récupéré d'autre part dans l'arbre (~ Done)
       ...
"""


def setWorkingDirectory():
    # On récupère l'adresse du dossier du fichier actuel (...LibreCast/python/)
    try:
        approot = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        approot = os.path.dirname(os.path.abspath(sys.argv[0]))

    # On cd à cette adresse pour créer le .db au bon endroit
    os.chdir(approot)


class mainUI(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(mainUI, self).__init__(*args, **kwargs)

        # Créer toute l'interface
        self.InitUI()

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

        # On créé "l'arbre" avec les playlistes, les abonnements etc.
        self.CreateTree()

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
        # Afficher la fenêtre
        self.Show(True)

    def CreateTree(self):
        # Créer un 'spliter' qui permet de couper l'écran en deux parties avec un style (la limite se déplace en temps réel)
        # Note : SP_NOSASH enpêche de redimensionner le spliter
        split = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_LIVE_UPDATE | wx.SP_NOBORDER)
        # Limiter la taille des deux parties de l'arbre à 150, pour des raison estétiques et pratiques
        split.SetMinimumPaneSize(150)
        # Créer un panel qui contient l'arbre et les bouttons ajouter/effacer
        panel = wx.Panel(split, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, style=wx.SP_BORDER)
        # Modifier la couleur d'arrière plan du panel en gris clair
        panel.SetBackgroundColour('#F0F0F0')

        # Créer l'arbre (grâce au module treeManager) avec un style (effacer le style pour commprendre les modifications apportées)
        mainTree = treeManager.pyTree(panel, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_NO_LINES)
        # Créer la liste de vidéos (grâce au module listManager) avec un style (effacer le style pour commprendre les modifications apportées)
        videoList = listManager.pyList(split, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.SUNKEN_BORDER)

        # Créer les images pour les boutons
        plusImage = wx.Image('resources/add.png')
        removeImage = wx.Image('resources/remove.png')
        # Modifier la taille des images
        plusImage.Rescale(8, 8)
        removeImage.Rescale(8, 8)
        # Créer les boutons
        addButton = wx.BitmapButton(panel, wx.ID_ANY, wx.BitmapFromImage(plusImage), style=wx.NO_BORDER)
        removeButton = wx.BitmapButton(panel, wx.ID_ANY, wx.BitmapFromImage(removeImage), style=wx.NO_BORDER)
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
        verticalPanelSizer.Add(mainTree, 1, wx.EXPAND | wx.ALL, 0)
        verticalPanelSizer.Add(horizontalButtonSizer, 0, wx.EXPAND | wx.ALL, 5)
        # Ajouter ce sizer au panel
        panel.SetSizer(verticalPanelSizer)

        # Couper l'écran en deux avec à gauche le panel (avec une taille par défaut de 200) et à droite la liste de vidéos
        split.SplitVertically(panel, videoList, 200)

    def CreateToolbar(self):
        # Créer la barre d'outils avec refresh et search (noter le 'B' majuscule dans 'Bar')
        toolbar = self.CreateToolBar()

        # Créer une variable qui contient l'image refresh.png dans le dossier resources
        refreshImage = wx.Image('resources/refresh.png')
        # Ajouter un bouton avec l'image refresh
        refreshTool = toolbar.AddLabelTool(wx.ID_ANY, 'Refresh', wx.BitmapFromImage(refreshImage), shortHelp='Refresh feeds')
        # Ajouter un évenement lorsque le bouton est cliqué (la fonction OnRefresh est appellée)
        self.Bind(wx.EVT_TOOL, self.OnRefresh, refreshTool)

        # Ajouter un séparateur
        toolbar.AddSeparator()

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

    def OnRefresh(self, event):
        print('Refreshing feeds...')

    def OnClickAddButton(self, event):
        print('Add a url!')

    def OnClickRemoveButton(self, event):
        print('Remove a url')

    def OnSearch(self, event):
        texte = self.searchbar.GetValue()
        if texte != '':
            print('Rechercher : ' + texte)
        else:
            print('Ne pas rechercher')

    def OnSearchTextChanged(self, event):
        texte = self.searchbar.GetValue()
        if texte != '':
            print('Nouvelle recherche : ' + texte)
        else:
            print('Aucune recherche')


# Méthode appelée depuis le fichier principale pour créer l'interface graphique
def main():
    setWorkingDirectory()
    ex = wx.App()
    ex.SetAppName("LibreCast")
    mainUI(None)
    ex.MainLoop()
