# -*- coding: utf-8 -*-

import os
import sys
import wx
import wx.lib.scrolledpanel as scrolled
from converter import Converter

from requestsManager import aria2Manager

try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

if('.exe' in approot):
    approot = approot.replace('LibreCast.exe', '')

if('uiManager' in approot):
    approot = approot.replace('/uiManager', '')


class DownloadPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)

        self.download_number = 1
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.downloads = []

        # Créer un timer qui controle le temps écoulé
        self.timer = wx.Timer(self)
        # Ajouter un évenement qui se déclanche à chaque fois que le timer se termine
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        # Lancer le timer, qui se déclancher toutes les 100 ms
        self.timer.Start(100)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.SetAutoLayout(1)

        self.aria2 = aria2Manager.Aria2Manager()

    def OnTimer(self, event):
        for download in self.downloads:
            eta = self.aria2.getETA(download['gid'])
            percentage = self.aria2.getProgressPercentage(download['gid'])
            downloadSpeed = self.aria2.getDownloadSpeed(download['gid'])
            download['infoLabel'].SetLabel('%s of %s (%s/sec) - %s s remaining' % ('53.7', '195 MB', downloadSpeed, eta))
            download['gauge'].SetValue(percentage)

    def AddDownload(self, url, title):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titleLabel = wx.StaticText(panel, label=title)

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        infoLabel = wx.StaticText(panel, label='Waiting for informations')
        infoLabel.SetFont(font)

        progressSizer = wx.BoxSizer(wx.HORIZONTAL)
        gauge = wx.Gauge(panel, wx.ID_ANY, 100, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        cancelImage = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'cancel.png'))
        cancelImage.Rescale(12, 12)
        cancelImagePressed = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'cancel_pressed.png'))
        cancelImagePressed.Rescale(12, 12)
        cancelButton = wx.BitmapButton(panel, wx.ID_ANY, wx.BitmapFromImage(cancelImage), style=wx.NO_BORDER)
        cancelButton.SetBitmapSelected(wx.BitmapFromImage(cancelImagePressed))

        progressSizer.Add(gauge, 1, wx.RIGHT | wx.EXPAND, 10)
        progressSizer.Add(cancelButton, 0, wx.RIGHT | wx.LEFT | wx.TOP, 3)

        sizer.Add(titleLabel, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)
        sizer.Add(progressSizer, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)
        sizer.Add(infoLabel, 0, wx.ALL, 5)

        panel.SetSizer(sizer)
        self.mainSizer.Add(panel, 0, wx.EXPAND)
        self.SetSizer(self.mainSizer)

        self.Layout()
        self.SetupScrolling()

        self.downloads += [{
            'panel': panel,
            'infoLabel': infoLabel,
            'gauge': gauge,
            'gid': self.aria2.addDownload(url)
        }]

        self.alternateColors()

    def alternateColors(self):
        count = 0

        for download in self.downloads:
            if count % 2 == 0:
                download['panel'].SetBackgroundColour(wx.Colour(239, 245, 255))
            else:
                download['panel'].SetBackgroundColour(wx.Colour(255, 255, 255))

            count += 1


class DownloaderFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Downloader", size=(800, 400))

        self.SetMinSize((330, 83))
        self.downloadPanel = DownloadPanel(self)
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.Show(False)

    def AddDownload(self, url, title):
        self.downloadPanel.AddDownload(url, title)
