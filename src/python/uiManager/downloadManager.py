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
        self.ticks = 0

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
        converter = Converter()

        for download in self.downloads:
            if not download['done']:
                percentage = self.aria2.getProgress(download['gid'])
                if percentage < 1000:
                    download['gauge'].SetValue(percentage)
                    if (self.ticks == 0):
                        size = self.aria2.getSize(download['gid'])
                        eta = self.aria2.getETA(download['gid'])
                        downloadSpeed = self.aria2.getDownloadSpeed(download['gid'])
                        download['infoLabel'].SetLabel('%s sur %s (%s/sec) - %s' % (converter.ConvertSize(size[1]), converter.ConvertSize(size[0]), converter.ConvertSize(downloadSpeed), converter.ConvertTime(eta)))
                else:
                    download['done'] = True
                    size = self.aria2.getSize(download['gid'])
                    download['infoLabel'].SetLabel('%s' % converter.ConvertSize(size[0]))

                    sizer = download['panel'].GetSizer()
                    font = wx.Font(10, wx.DEFAULT, wx.ITALIC, wx.NORMAL)
                    doneLabel = wx.StaticText(download['panel'], label='Téléchargement terminé')
                    doneLabel.SetFont(font)
                    doneLabel.SetForegroundColour((109, 109, 109))
                    sizer.Replace(download['gauge'], doneLabel, True)
                    download['gauge'].Destroy()
                    download['gauge'] = None
                    self.Layout()

        self.ticks += 1
        if self.ticks > 5:
            self.ticks = 0

    def AddDownload(self, url, title):
        gid = self.aria2.addDownload(url)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titleLabel = wx.StaticText(panel, label=title)

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        infoLabel = wx.StaticText(panel, label='En attente d\'informations')
        infoLabel.SetFont(font)

        progressSizer = wx.BoxSizer(wx.HORIZONTAL)
        gauge = wx.Gauge(panel, wx.ID_ANY, 1000, style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        cancelImage = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'cancel.png'))
        cancelImage.Rescale(12, 12)
        cancelImagePressed = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'uiManager', 'resources', 'cancel_pressed.png'))
        cancelImagePressed.Rescale(12, 12)
        cancelButton = wx.BitmapButton(panel, wx.ID_ANY, wx.BitmapFromImage(cancelImage), style=wx.NO_BORDER, name=gid)
        cancelButton.SetBitmapSelected(wx.BitmapFromImage(cancelImagePressed))
        cancelButton.Bind(wx.EVT_BUTTON, self.OnStopDownload)

        progressSizer.Add(gauge, 1, wx.RIGHT | wx.EXPAND, 10)
        progressSizer.Add(cancelButton, 0, wx.RIGHT | wx.LEFT | wx.TOP, 3)

        sizer.Add(titleLabel, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)
        sizer.Add(progressSizer, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 5)
        sizer.Add(infoLabel, 0, wx.ALL, 5)

        panel.SetSizer(sizer)
        self.mainSizer.Add(panel, 0, wx.EXPAND)
        self.SetSizer(self.mainSizer)

        self.Layout()
        self.SetupScrolling()

        self.downloads += [{
            'panel': panel,
            'infoLabel': infoLabel,
            'titleLabel': titleLabel,
            'gauge': gauge,
            'gid': gid,
            'done': False
        }]

        panel.Bind(wx.EVT_LEFT_DOWN, self.OnPanelClick)

        self.alternateColors()

    def alternateColors(self):
        count = 0

        for download in self.downloads:
            if count % 2 == 0:
                download['panel'].SetBackgroundColour(wx.Colour(255, 255, 255))
            else:
                download['panel'].SetBackgroundColour(wx.Colour(239, 245, 255))

            count += 1

    def OnStopDownload(self, event):
        button = event.GetEventObject()
        gid = button.GetName()
        delindex = -1

        for index, download in enumerate(self.downloads):
            if download['gid'] == gid:
                if not download['done']:
                    self.aria2.remove(gid)
                download['panel'].Destroy()
                delindex = index
                break

        self.downloads.pop(delindex)
        self.SetSizer(self.mainSizer)

        self.Layout()
        self.SetupScrolling()

        self.alternateColors()

    def OnPanelClick(self,event):
        print "EVENT"
        self.alternateColors()

        panel = event.GetEventObject()
        panel.SetBackgroundColour(wx.Colour(81, 116, 212))


class DownloaderFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Téléchargements', size=(800, 400))

        self.SetMinSize((330, 83))
        self.downloadPanel = DownloadPanel(self)
        self.Show()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.Show(False)

    def AddDownload(self, url, title):
        self.downloadPanel.AddDownload(url, title)
