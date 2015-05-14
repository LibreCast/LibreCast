# -*- coding: utf-8 -*-

import requests
import os
import sys
import wx
import wx.lib.scrolledpanel as scrolled

from threading import Thread
from wx.lib.pubsub import pub


class DownloadThread(Thread):

    def __init__(self, gnum, url, fsize):
        Thread.__init__(self)
        self.fsize = fsize
        self.gnum = gnum
        self.url = url
        self.start()

    def run(self):
        local_fname = os.path.basename(self.url)
        count = 1
        while True:
            if os.path.exists(local_fname):
                tmp, ext = os.path.splitext(local_fname)
                cnt = "(%s)" % count
                local_fname = tmp + cnt + ext
                count += 1
            else:
                break
        req = requests.get(self.url, stream=True)
        total_size = 0
        print local_fname
        with open(local_fname, "wb") as fh:
            for byte in req.iter_content(chunk_size=1024):
                if byte:
                    fh.write(byte)
                    fh.flush()
                total_size += len(byte)
                if total_size < self.fsize:
                    wx.CallAfter(pub.sendMessage,
                                 "update_%s" % self.gnum,
                                 msg=total_size)
        print "DONE!"
        wx.CallAfter(pub.sendMessage,
                     "update_%s" % self.gnum,
                     msg=self.fsize)


class Gauge(wx.Gauge):
    def __init__(self, parent, range, num):
        wx.Gauge.__init__(self, parent, range=range)

        pub.subscribe(self.updateProgress, "update_%s" % num)

    def updateProgress(self, msg):
        self.SetValue(msg)


class DownloadPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)

        self.data = []
        self.download_number = 1

        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        # Create the sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        dlSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create the widgets
        lbl = wx.StaticText(self, label="Download URL:")
        self.dl_txt = wx.TextCtrl(self)
        btn = wx.Button(self, label="Download")
        btn.Bind(wx.EVT_BUTTON, self.onDownload)

        # Layout the widgets
        dlSizer.Add(lbl, 0, wx.ALL | wx.CENTER, 5)
        dlSizer.Add(self.dl_txt, 1, wx.EXPAND | wx.ALL, 5)
        dlSizer.Add(btn, 0, wx.ALL, 5)
        self.mainSizer.Add(dlSizer, 0, wx.EXPAND)

        self.SetSizer(self.mainSizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()

    def onDownload(self, event):
        url = self.dl_txt.GetValue()

        # Set root path
        try:
            approot = os.path.dirname(os.path.abspath(__file__))
        except NameError:  # We are the main py2exe script, not a module
            approot = os.path.dirname(os.path.abspath(sys.argv[0]))

        if('.exe' in approot):
            approot = approot.replace('LibreCast.exe', '')

        if('uiManager' in approot):
            approot = approot.replace('/uiManager', '')

        try:
            header = requests.head(url)
            fsize = int(header.headers["content-length"]) / 1024

            panel = wx.Panel(self)
            sizer = wx.BoxSizer(wx.VERTICAL)
            fname = os.path.basename(url)
            lbl = wx.StaticText(panel, label="Downloading %s" % fname)
            self.infoLabel = wx.StaticText(panel, label="%s of %s (%s/sec) — %s remaining" % ("53.7", "195 MB", "21.6 MB", "6 seconds"))
            font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
            self.infoLabel.SetFont(font)

            progressSizer = wx.BoxSizer(wx.HORIZONTAL)
            gauge = Gauge(panel, fsize, self.download_number)
            cancelImage = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'cancel.png'))
            cancelImage.Rescale(15, 15)
            cancelButton = wx.BitmapButton(panel, wx.ID_ANY, wx.BitmapFromImage(cancelImage), style=wx.NO_BORDER)

            progressSizer.Add(gauge, 1, wx.RIGHT | wx.EXPAND, 10)
            progressSizer.Add(cancelButton, 0, wx.RIGHT | wx.LEFT, 5)

            sizer.Add(lbl, 0, wx.TOP | wx.RIGHT | wx.LEFT, 5)
            sizer.Add(progressSizer, 1, wx.RIGHT | wx.LEFT | wx.EXPAND, 10)
            sizer.Add(self.infoLabel, 0, wx.RIGHT | wx.LEFT | wx.BOTTOM, 5)

            if self.download_number % 2 != 0:
                panel.SetBackgroundColour(wx.Colour(255, 255, 255))
            else:
                panel.SetBackgroundColour(wx.Colour(239, 245, 255))
            panel.SetSizer(sizer)
            self.mainSizer.Add(panel, 0, wx.EXPAND)

            self.Layout()

            # start thread
            DownloadThread(self.download_number, url, fsize)
            self.dl_txt.SetValue("")
            self.download_number += 1
        except Exception, e:
            print "Error: ", e

        self.SetupScrolling()


class DownloaderFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Downloader", size=(800, 400))

        self.SetMinSize((330, 110))
        DownloadPanel(self)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = DownloaderFrame()
    app.MainLoop()
