# -*- coding: utf-8 -*-

# Permet de récupérer des float depuis une division
from __future__ import division
import wx
import wx.media
import os
import sys
from threading import Thread

MEDIASTATE_PLAYING = 2


def setWorkingDirectory():
    # On récupère l'adresse du dossier du fichier actuel (...LibreCast/python/)
    try:
        approot = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        approot = os.path.dirname(os.path.abspath(sys.argv[0]))

    # On cd à cette adresse pour accéder aux images directement via le dossier resources
    os.chdir(approot)


class videoWindow(wx.Frame):

    def __init__(self, parent, id, url):
        wx.Frame.__init__(self, parent, id)

        self.state = wx.media.MEDIASTATE_STOPPED
        self.InitialSize = (800, 600)

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

        # Dire quel backend utiliser en fonction de l'OS
        backend = None
        if sys.platform == 'linux2':
            backend = wx.media.MEDIABACKEND_GSTREAMER
        elif sys.platform == 'darwin':
            backend = wx.media.MEDIABACKEND_QUICKTIME
        elif sys.platform == 'win32':
            backend = wx.media.MEDIABACKEND_DIRECTSHOW
        if backend is not None:
            # Créer le médiaCtrl qui gère la vidéo en utilisant le backend choisit
            self.mc = wx.media.MediaCtrl(self, wx.ID_ANY, szBackend=backend)
        else:
            # Créer le médiaCtrl qui gère la vidéo
            self.mc = wx.media.MediaCtrl(self, wx.ID_ANY)

        # Si l'OS ne permet pas d'afficher des controles par défaut
        # Note : Pour l'instant, on affiche toujours nos controles
        #if not self.mc.ShowPlayerControls():
        if True:
            # Initaliser les images
            self.initImages()
            # Créer les boutons
            self.playButton = wx.BitmapButton(self, wx.ID_ANY, wx.BitmapFromImage(self.playImage), style=wx.NO_BORDER)
            self.fullScreenButton = wx.BitmapButton(self, wx.ID_ANY, wx.BitmapFromImage(self.fullScreenImage), style=wx.NO_BORDER)
            # Modifier l'image lorsque le bouton est sélectionné
            self.playButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedPlayImage))
            self.fullScreenButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedFullScreenImage))

            # Ajouter un évenement lorsque chaque bouton est cliqué
            self.Bind(wx.EVT_BUTTON, self.OnPlay, self.playButton)
            self.Bind(wx.EVT_BUTTON, self.OnFullScreen, self.fullScreenButton)

            # Créer les zones de texte
            self.totalTime = wx.StaticText(self, wx.ID_ANY, label='0:00:00', size=(55, -1))
            self.currentTime = wx.StaticText(self, wx.ID_ANY, label='0:00:00', size=(45, -1))
            # Changer la couleur du texte
            self.totalTime.SetForegroundColour('#7B7B7B')
            self.currentTime.SetForegroundColour('#ffffff')

            # Créer le slider du son
            self.soundSlider = wx.Slider(self, wx.ID_ANY, size=wx.Size(100, -1))
            # Modifier la valeur par défaut du slider
            self.soundSlider.SetValue(20)
            # Appeller self.soundSlider lorsque la valeur du slider est modifiée
            self.Bind(wx.EVT_SLIDER, self.OnVolume, self.soundSlider)

            # Créer la gauge de téléchargement de la vidéo
            self.downloadGauge = wx.Gauge(self, wx.ID_ANY, 100, size=(390, -1))
            # Créer le slider de l'avancement de la vidéo
            self.timeSlider = wx.Slider(self.downloadGauge, wx.ID_ANY, pos=(-2, 1.5), size=(390, -1))
            # Appeller self.OnTimeSlider lorsque la valeur du slider est modifiée
            self.Bind(wx.EVT_SLIDER, self.OnTimeSlider, self.timeSlider)

            # Ajouter un évenement lorsque la vidéo est mise en pause ou lancée
            self.mc.Bind(wx.media.EVT_MEDIA_STATECHANGED, self.OnStateChange)
            # Créer un timer qui controle le temps écoulé
            self.timer = wx.Timer(self)
            # Ajouter un évenement qui se déclanche à chaque fois que le timer se termine
            self.Bind(wx.EVT_TIMER, self.OnTimer)
            # Lancer le timer, qui se déclancher toutes les 100 ms
            self.timer.Start(100)

            # Créer un sizer qui empêche les deux boutons de se superposer
            horizontalButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
            # Ajouter un écart de 5 horizontalement avant les boutons
            horizontalButtonSizer.Add((5, -1), 0)
            # Ajouter le 1er boutton (bouton, resize, event, margin)
            horizontalButtonSizer.Add(self.playButton, 0, wx.ALL, 0)
            # Ajouter un écart de 10 horizontalement entre les élément
            horizontalButtonSizer.Add((10, -1), 0)
            # Ajouter le slider pour le son
            horizontalButtonSizer.Add(self.soundSlider, 0, wx.ALL, 0)
            # Ajouter un écart de 10 horizontalement entre les élément
            horizontalButtonSizer.Add((10, -1), 0)
            # Ajouter le texte affichant le temps écoulé
            horizontalButtonSizer.Add(self.currentTime, 0, wx.ALL, 0)
            # Ajouter un écart de 5 horizontalement entre les élément
            horizontalButtonSizer.Add((5, -1), 0)
            # Ajouter le texte affichant le temps total
            horizontalButtonSizer.Add(self.totalTime, 0, wx.ALL, 0)
            # Ajouter un écart de 5 horizontalement entre les élément
            horizontalButtonSizer.Add((5, -1), 0)
            # Ajouter le slider qui affiche le temps écoulé, et qui se resize automatiquement
            horizontalButtonSizer.Add(self.downloadGauge, 1, wx.ALL, 0)
            # Ajouter un écart de 5 horizontalement entre les élément
            horizontalButtonSizer.Add((5, -1), 0)
            # Ajouter le 3ème bouton
            horizontalButtonSizer.Add(self.fullScreenButton, 0, wx.ALL, 0)

            # Créer un sizer qui gère la vidéo et les boutons
            verticalPanelSizer = wx.BoxSizer(wx.VERTICAL)
            # Ajouter l'arbre et le sizer horizontal (qui contient les boutons) au sizer vertical
            verticalPanelSizer.Add(self.mc, 1, wx.EXPAND | wx.ALL, 0)
            verticalPanelSizer.Add(horizontalButtonSizer, 0, wx.EXPAND | wx.ALL, 5)
            # Ajouter ce sizer
            self.SetSizer(verticalPanelSizer)

        # Appeler la méthode OnSize lorsque l'utilisateur change la taille de la fenêtre
        self.Bind(wx.EVT_SIZE, self.OnSize)
        # Appeler la méthode OnMediaLoaded lorsque la vidéo a fini de charger
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded, self.mc)

        # Créer un thread pour tester si l'url est valide
        thread = Thread(target=self.TestUrl, args=[url])
        # Lancer le test de connection après 100 ms
        wx.CallLater(100, thread.run)

        # Modifier la couleur d'arrière plan de la fenêtre en gris foncé
        self.SetBackgroundColour('#2D2D2D')
        # Récupérer la taille de l'écran
        displaySize = wx.DisplaySize()
        # Modifier la taille de la fenêtre pour qu'elle fasse 4/5 de l'écran
        self.SetSize((9 * displaySize[0] / 10, 9 * displaySize[1] / 10))
        # Garder cette taille en mémoire
        self.InitialSize = self.GetSize()
        # Modifier le titre de la fenêtre
        self.SetTitle(url)
        # Centrer la fenêtre
        self.Centre()
        # Afficher la fenêtre
        self.Show(True)

    def OnStateChange(self, event=None):
        # Récupérer l'état de la vidéo (en pause, lancée...)
        st = self.mc.GetState()
        # Stocker cet état dans une variable
        self.state = st

        # Si la vidéo est en pause ou stoppée
        if st == wx.media.MEDIASTATE_STOPPED or st == wx.media.MEDIASTATE_PAUSED:
            # Changer les images du bouton play
            self.playButton.SetBitmapLabel(wx.BitmapFromImage(self.playImage))
            self.playButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedPlayImage))
            # Mettre le bouton play à jour
            self.playButton.Refresh()
        # Si la vidéo es lancée
        elif st == MEDIASTATE_PLAYING:
            # Mettre le taille du slider à jour lorsque la vidéo est lancée
            # Note : La modifier après avoir testé l'URL ne semble pas fonctionner sous windows (car trop lent ?), on l'ajoute donc ici
            self.timeSlider.SetRange(0, self.mc.Length())
            # Modifier la taille maximale de la gauge afin qu'elle vaille la quantité de données à télécharger
            self.downloadGauge.SetRange(self.mc.GetDownloadTotal())
            # Changer les images du bouton play
            self.playButton.SetBitmapLabel(wx.BitmapFromImage(self.pauseImage))
            self.playButton.SetBitmapSelected(wx.BitmapFromImage(self.selectedPauseImage))
            # Mettre le bouton play à jour
            self.playButton.Refresh()

    # Appelée lorsque la taille de la fenêtre change
    def OnSize(self, event):
        # Calculer le ratio de la fenêtre
        ratio = self.InitialSize[1]/self.InitialSize[0]
        # Calculer la hauteur correspondant à ce ration
        hsize = event.GetSize()[0]*ratio
        # Si la taille est compatible avec l'écran
        # Appliquer ce ratio à la hauteur de la fenêtre
        self.SetSizeHints(minW=-1, minH=hsize, maxH=hsize)
        # Modifier la taille du slider afichant le temps écoulé
        self.timeSlider.SetSize((self.downloadGauge.GetSize()[0] + 7, self.downloadGauge.GetSize()[1]))
        # Calculer la taille des éléments de la fenêtre avec les fonctions par défaut
        event.Skip()

    # Note : Cette fonction peut, dans certains cas, suspendre l'application (en mode 'ne répond plus' durant un certains temps)
    #        On la lance donc dans une thread différente afin de ne pas suspendre l'interface
    def TestUrl(self, url):
        # On récuppère la vidéo à l'URL donnée
        r = self.mc.LoadURI(url)
        # Si la vidéo n'est pas trouvée ou n'est pas lisible (mauvaise extension par exemple)
        if not r:
            print 'Failed to load video'
        else:
            print 'Loading video'
            try:
                # Modifier la taille maximale du slider afin qu'elle vaille le temps de la vidéo (en ms)
                self.timeSlider.SetRange(0, self.mc.Length())
                # Modifier la taille maximale de la gauge afin qu'elle vaille la quantité de données à télécharger
                self.downloadGauge.SetRange(self.mc.GetDownloadTotal())
            except:
                pass

    def OnMediaLoaded(self, event):
        # Modifier la taille de la fenêtre
        self.InitialSize = self.mc.GetBestSize()
        self.SetSizeHints(minW=-1, minH=self.mc.GetBestSize()[0], maxH=self.mc.GetBestSize()[0])
        # Lancer la vidéo après quelques ms
        wx.CallLater(100, self.OnPlay, event)

    def OnVolume(self, event):
        # Récupérer la valeur du slider pour le son
        offset = self.soundSlider.GetValue()
        # Modifier le volume en fonction de cette valeur
        self.mc.SetVolume(round(offset/10.0))

    def OnTimeSlider(self, event):
        # Récupérer la valeur du slider
        offset = self.timeSlider.GetValue()
        # Déplacer le temps de la vidéo à la valeur du slider
        self.mc.Seek(offset)

    def OnTimer(self, event):
        # Récupérer le temps (en ms) écoulé
        offset = self.mc.Tell()
        # Modifier la valeur du slider pour l'avancement afin qu'il présente cette valeur
        self.timeSlider.SetValue(offset)
        # Mettre à jour l'avancement du téléchargement
        self.downloadGauge.SetValue(self.mc.GetDownloadProgress())
        # Si le temps écoulé est défini (donc la vidéo est chargée)
        if offset != -1 and self.mc.Length() != -1:
            # Si l'état stocké est différent de l'état actuel
            # Note : On fait cela car la gestion de l'évenement 'Play' ne fonctionne pas sous OSX... :'(
            if self.mc.GetState() == MEDIASTATE_PLAYING and self.state != MEDIASTATE_PLAYING:
                # Appeler la fonction qui repère que l'état de la vidéo a changé
                self.OnStateChange()
            # Convertir les milisecondes du temps écoulé en heures, minutes et secondes
            m, s = divmod((offset / 1000.0), 60)
            h, m = divmod(m, 60)
            # Afficher ces valeurs dans la zone de texte
            self.currentTime.SetLabel('%d:%02d:%02d' % (h, m, s))

            # Convertir les milisecondes du temps total en heures, minutes et secondes
            m, s = divmod((self.mc.Length() / 1000.0), 60)
            h, m = divmod(m, 60)
            # Afficher ces valeurs dans la zone de texte
            self.totalTime.SetLabel('/ %d:%02d:%02d' % (h, m, s))

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
        # 0: En train de charger, 1: En pause, 2: Lancée
        if self.mc.GetState() == 2:
            # Pauser la vidéo
            self.mc.Pause()
        else:
            # Lancer la vidéo
            self.mc.Play()
