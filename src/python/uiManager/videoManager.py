# -*- coding: utf-8 -*-

import wx
import wx.media
import os
import sys


def setWorkingDirectory():
    # On récupère l'adresse du dossier du fichier actuel (...LibreCast/python/)
    try:
        approot = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        approot = os.path.dirname(os.path.abspath(sys.argv[0]))

    # On cd à cette adresse pour créer le .db au bon endroit
    os.chdir(approot)


class videoWindow(wx.Frame):

    def __init__(self, parent, id, url):
        wx.Frame.__init__(self, parent, id)

        # Créer toute l'interface
        self.InitUI(url)

    def initImages(self):
        # Créer les images pour les boutons
        self.pauseImage = wx.Image('resources/pause.png')
        self.playImage = wx.Image('resources/play.png')
        self.fullScreenImage = wx.Image('resources/fullScreen.png')
        self.windowedImage = wx.Image('resources/windowed.png')
        self.selectedPauseImage = wx.Image('resources/pauseSelected.png')
        self.selectedPlayImage = wx.Image('resources/playSelected.png')
        self.selectedFullScreenImage = wx.Image('resources/fullScreenSelected.png')
        self.selectedWindowedImage = wx.Image('resources/windowedSelected.png')

        # Modifier la taille des images
        self.pauseImage.Rescale(22, 22)
        self.playImage.Rescale(22, 22)
        self.fullScreenImage.Rescale(22, 22)
        self.windowedImage.Rescale(22, 22)
        self.selectedPauseImage.Rescale(22, 22)
        self.selectedPlayImage.Rescale(22, 22)
        self.selectedFullScreenImage.Rescale(22, 22)
        self.selectedWindowedImage.Rescale(22, 22)

    def InitUI(self, url):
        # Créer la barre de menus
        menubar = wx.MenuBar()
        # Créer un menu appelé 'File'
        fileMenu = wx.Menu()
        # Ajouter dans ce menu une option pour quitter. Sur Mac OSX, elle n'y
        # sera pas car l'option est déjà présente par défaut dans un autre menu
        fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        # Ajouter le menu 'File' à la barre de menus
        menubar.Append(fileMenu, '&File')

        # Initaliser les images
        self.initImages()
        # Créer les boutons
        pauseButton = wx.BitmapButton(self, wx.ID_ANY, wx.BitmapFromImage(self.pauseImage), style=wx.NO_BORDER)
        playButton = wx.BitmapButton(self, wx.ID_ANY, wx.BitmapFromImage(self.playImage), style=wx.NO_BORDER)
        self.fullScreenButton = wx.BitmapButton(self, wx.ID_ANY, wx.BitmapFromImage(self.fullScreenImage), style=wx.NO_BORDER)
        # Modifier l'image lorsque le bouton est sélectionné
        pauseButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedPauseImage))
        playButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedPlayImage))
        self.fullScreenButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedFullScreenImage))

        # Ajouter un évenement lorsque chaque bouton est cliqué
        self.Bind(wx.EVT_BUTTON, self.OnPause, pauseButton)
        self.Bind(wx.EVT_BUTTON, self.OnPlay, playButton)
        self.Bind(wx.EVT_BUTTON, self.OnFullScreen, self.fullScreenButton)

        # Créer un sizer qui empêche les deux boutons de se superposer
        horizontalButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Ajouter un écart de 5 horizontalement avant les boutons
        horizontalButtonSizer.Add((5, -1), 0)
        # Ajouter le 1er boutton (bouton, resize, event, margin)
        horizontalButtonSizer.Add(playButton, 0, wx.ALL, 0)
        # Ajouter un écart de 10 horizontalement entre les boutons
        horizontalButtonSizer.Add((10, -1), 0)
        # Ajouter le 2ème bouton
        horizontalButtonSizer.Add(pauseButton, 0, wx.ALL, 0)
        # Ajouter un écart décalant le prochain bouton à droit de la fenêtre
        horizontalButtonSizer.Add((0, 0), 1)
        # Ajouter le 3ème bouton
        horizontalButtonSizer.Add(self.fullScreenButton, 0, wx.ALL, 0)

        # Créer le médiaCtrl qui gère la vidéo
        self.mc = wx.media.MediaCtrl(self, wx.ID_ANY, style=wx.SIMPLE_BORDER)
        # Créer un sizer qui gère la vidéo et les boutons
        verticalPanelSizer = wx.BoxSizer(wx.VERTICAL)
        # Ajouter l'arbre et le sizer horizontal (qui contient les boutons) au sizer vertical
        verticalPanelSizer.Add(self.mc, 1, wx.EXPAND | wx.ALL, 0)
        verticalPanelSizer.Add(horizontalButtonSizer, 0, wx.EXPAND | wx.ALL, 5)
        # Ajouter ce sizer au panel
        self.SetSizer(verticalPanelSizer)
        # Appeler la méthode OnMediaLoaded lorsque la vidéo a fini de charger
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded, self.mc)
        # Lancer le test de connection après 100 ms
        wx.CallLater(100, self.TestUrl, url)

        # Modifier la couleur d'arrière plan de la fenêtre en gris foncé
        self.SetBackgroundColour('#2D2D2D')
        # Récupérer la taille de l'écran
        displaySize = wx.DisplaySize()
        # Modifier la taille de la fenêtre pour qu'elle fasse 4/5 de l'écran
        self.SetSize((9 * displaySize[0] / 10, 9 * displaySize[1] / 10))
        # Modifier la taille minimale de la fenêtre, pour éviter que tout
        # devienne trop moche par manque de place...
        self.SetMinSize((250, 250))
        # Modifier le titre de la fenêtre
        self.SetTitle('Video name')
        # Centrer la fenêtre
        self.Centre()
        # Afficher la fenêtre
        self.Show(True)

    def TestUrl(self, url):
        print "Loading..."
        # On récuppère la vidéo à l'URL donnée
        r = self.mc.LoadURI(url)
        # Si la vidéo n'est pas trouvée ou n'est pas lisible (mauvaise extension par exemple)
        if not r:
            print "Failed to load"

    def OnMediaLoaded(self, event):
        # Lancer la vidéo après quelques ms
        wx.CallLater(100, self.OnPlay, event)
        print "Playing video"

    def OnFullScreen(self, event):
        # Si la fenêtre est en plein écran
        if self.IsFullScreen():
            # La mettre en taille normale
            self.ShowFullScreen(False)
            # Changer les images du bouton plein écran
            self.fullScreenButton.SetBitmapLabel(wx.BitmapFromImage(self.fullScreenImage))
            self.fullScreenButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedFullScreenImage))
            # Mettre le bouton plein écran à jour
            self.fullScreenButton.Refresh()
        # Si la fenêtre n'est pas en plein écran
        else:
            # La mettre en plein écran
            self.fullScreenButton.SetBitmapLabel(wx.BitmapFromImage(self.windowedImage))
            # Changer les images du bouton plein écran
            self.fullScreenButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedWindowedImage))
            self.fullScreenButton.Refresh()
            # Mettre le bouton plein écran à jour
            self.ShowFullScreen(True)

    def OnPlay(self, event):
        # Lancer la vidéo
        self.mc.Play()

    def OnPause(self, event):
        # Mettre la vidéo en pause
        self.mc.Pause()
