# -*- encoding: utf-8 -*-

import wx
import os
import sys
import treeManager

"""
TODO : Découper le contenu en plusieurs fichiers, avec notamment un pour la recherche et un pour l'arbre (~ Done)
       Ajouter de réelles fonctionnalitées aux boutons
       Afficher du contenu récupéré d'autre part dans l'arbre
       Ajouter les bouttons + et - pour l'arbre
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

        self.InitUI()

    def InitUI(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # On créé "l'arbre" avec les playlistes, les abonnements etc.
        self.CreateTree()

        # Créer la barre de menu
        self.CreateToolbar()

        # Récupérer la taille de l'écran
        displaySize = wx.DisplaySize()
        # Modifier la taille de la fenêtre pour qu'elle fasse 4/5 de l'écran
        self.SetSize((4*displaySize[0]/5, 4*displaySize[1]/5))
        # Modifier la taille minimale de la fenêtre, pour éviter que tout devienne trop moche par manque de place...
        self.SetMinSize((500, 500))
        # Modifier le titre de la fenêtre
        self.SetTitle('LibreCast')
        # Centrer la fenêtre
        self.Centre()
        # Afficher la fenêtre
        self.Show(True)

    """
    Code taken from the wxpython samples
    """
    def CreateTree(self):
        split = wx.SplitterWindow(self, -1)
        tree = treeManager.pyTree(split, -1, style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_NO_LINES)
        text = wx.TextCtrl(split, -1, "", style=wx.TE_MULTILINE)
        split.SplitVertically(tree, text, 200)
        tree.SetOutput(text.SetValue)
        tree.SelectItem(tree.root)

    def CreateToolbar(self):
        # Créer la barre de menus avec refresh et search
        toolbar = self.CreateToolBar()

        # Créer une variable qui contient l'image refresh.png dans le dossier resources
        refreshImage = wx.Image('resources/refresh.png')
        # Ajouter un boutton avec l'image refresh
        refreshTool = toolbar.AddLabelTool(wx.ID_ANY, 'Refresh', wx.BitmapFromImage(refreshImage), shortHelp='Refresh feeds')
        # Ajouter un évenement lorsque le boutton est cliqué (la fonction OnRefresh est appellée)
        self.Bind(wx.EVT_TOOL, self.OnRefresh, refreshTool)

        # Ajouter un séparateur
        toolbar.AddSeparator()

        # Créer une barre de recherche
        self.searchbar = wx.SearchCtrl(toolbar, wx.ID_ANY, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        # Afficher le boutton annuler dans la barre de recherche
        self.searchbar.ShowCancelButton(True)
        # Afficher 'Search online content' par défaut dans la barre de recherche
        self.searchbar.SetDescriptiveText('Search online content')
        # Ajouter la barre de recherche
        self.searchbarctrl = toolbar.AddControl(self.searchbar)
        # Ajouter un évenement lorsque le texte change
        self.Bind(wx.EVT_TEXT, self.OnSearchTextChanged, self.searchbarctrl)
        # Ajouter un évenement lorsque l'utilisateur appuye sur entrée (fonctionne pas sur OS X apparement...)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSearchTextChanged, self.searchbarctrl)

        # Afficher tous les éléments ajoutés ci-dessus
        toolbar.Realize()

        # Modifier la taille des icones de la barre de menus
        toolbar.SetToolBitmapSize((32, 32))

    def OnRefresh(self, event):
        print('Refreshing feeds...')

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