# -*- coding: utf-8 -*-

import os
import sys
import wx
import wx.lib.scrolledpanel as scrolled

from wx.lib.pubsub import pub

try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))

if('.exe' in approot):
    approot = approot.replace('LibreCast.exe', '')

if('uiManager' in approot):
    approot = approot.replace('/uiManager', '')


class Gauge(wx.Gauge):
    def __init__(self, parent, range, num):
        wx.Gauge.__init__(self, parent, range=range)

        pub.subscribe(self.updateProgress, "update_%s" % num)

    def updateProgress(self, progress):
        self.SetValue(progress)


class DownloadPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)

        self.download_number = 1
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        self.downloads = [
            {
                "gid": "1234",
                "title": "XViD.NyXD.avi"
            },
            {
                "gid": "1274",
                "title": "LOL.Scout.avi"
            }
        ]

        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.SetAutoLayout(1)

    def AddDownload(self, url, title):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titleLabel = wx.StaticText(panel, label='title')

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        infoLabel = wx.StaticText(panel, label="%s of %s (%s/sec) - %s remaining" % ("53.7", "195 MB", "21.6 MB", "6 seconds"))
        infoLabel.SetFont(font)

        progressSizer = wx.BoxSizer(wx.HORIZONTAL)
        gauge = Gauge(panel, 100, self.download_number)
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

        panel.SetBackgroundColour(wx.Colour(239, 245, 255))

        panel.SetSizer(sizer)
        self.mainSizer.Add(panel, 0, wx.EXPAND)
        self.SetSizer(self.mainSizer)

        self.Layout()
        self.SetupScrolling()


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
