# -*- coding: utf-8 -*-

import wx
import os
import sys
from threading import Thread
from requestsManager import httpRequestManager
from cStringIO import StringIO

# Set root path
try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))


class TransparentText(wx.StaticText):
    def __init__(self, parent, id=wx.ID_ANY, label='', pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TRANSPARENT_WINDOW, name=''):
        wx.StaticText.__init__(self, parent, id, label, pos, size, style, name)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda event: None)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnPaint(self, event):
        bdc = wx.PaintDC(self)
        dc = wx.GCDC(bdc)

        font_face = self.GetFont()
        font_color = self.GetForegroundColour()

        dc.SetFont(font_face)
        dc.SetTextForeground(font_color)
        dc.DrawText(self.GetLabel(), 0, 0)

    def OnSize(self, event):
        self.Refresh()
        event.Skip()


class ChannelHeader(wx.Panel):
    def __init__(self, parent, id, description, name, coverURL, iconURL, style=''):
        wx.Panel.__init__(self, parent, id)

        # Si au moins un style a été précisé dans la création de l'abre...
        if style != '':
            # ...on l'applique
            self.SetWindowStyle(style)
        else:
            self.SetWindowStyle(wx.SP_BORDER)

        # Modifier la couleur d'arrière plan
        self.SetBackgroundColour('#F1F1F1')

        if iconURL == '':
            self.CreateSimplePanel(name)
        else:
            self.CreateCompletePanel(description, name, iconURL, coverURL)

    def OnEraseBackground(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)

        dc.Clear()
        dc.DrawBitmap(self.banner, 0, 0)

    def CreateSimplePanel(self, name):
        font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        channelName = wx.StaticText(self, wx.ID_ANY, name, pos=(10, 7))
        channelName.SetFont(font)

        self.SetMinSize((150, 30))

    def CreateCompletePanel(self, description, name, imageURL, coverURL):
        # Créer un sizer qui gère la tout le panel
        panelSizer = wx.BoxSizer(wx.VERTICAL)

        # Créer un sizer qui gère l'incone et le nom de la chaîne
        iconSizer = wx.BoxSizer(wx.HORIZONTAL)

        image = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'resources', 'defaultChannelIcon.png')).Scale(48, 48).ConvertToBitmap()
        self.channelIcon = wx.StaticBitmap(self, wx.ID_ANY, image, (10, 5), (48, 48))

        font = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        if sys.platform == 'win32':
            channelName = TransparentText(self, wx.ID_ANY, name)
        else:
            channelName = wx.StaticText(self, wx.ID_ANY, name)
        channelName.SetFont(font)
        channelName.SetForegroundColour((255, 255, 255))

        iconSizer.Add(self.channelIcon, 0, wx.ALL, 5)
        iconSizer.Add(channelName, 1, wx.TOP, 20)

        if sys.platform == 'win32':
            channelDescription = TransparentText(self, wx.ID_ANY, description, style=wx.TE_MULTILINE | wx.TRANSPARENT_WINDOW)
        else:
            channelDescription = wx.StaticText(self, wx.ID_ANY, description, style=wx.TE_MULTILINE)
        channelDescription.SetForegroundColour((255, 255, 255))

        panelSizer.Add(iconSizer, 0, wx.EXPAND)
        panelSizer.Add(channelDescription, 1, wx.EXPAND | wx.BOTTOM | wx.RIGHT | wx.LEFT, 5)
        self.SetMinSize((150, 150))
        self.SetSizer(panelSizer)

        dc = wx.ClientDC(self)
        rect = self.GetUpdateRegion().GetBox()
        dc.SetClippingRect(rect)

        dc.Clear()
        self.banner = wx.Image(os.path.join(os.environ.get('RESOURCEPATH', approot), 'resources', 'defaultCoverImage.png')).Scale(2000, 150).Blur(5).AdjustChannels(0.4, 0.4, 0.4).ConvertToBitmap()
        dc.DrawBitmap(self.banner, 0, 0)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

        self.thread = Thread(target=self.loadImage, args=[imageURL, coverURL])
        self.thread.setDaemon(False)
        wx.CallLater(100, self.thread.start)

    def loadImage(self, iconURL, bannerURL):
        try:
            data = httpRequestManager.OpenUrl(iconURL)[0].read()
            bmp = wx.ImageFromStream(StringIO(data)).Scale(48, 48).ConvertToBitmap()
            self.channelIcon.SetBitmap(bmp)
        except:
            print('except: download failed')

        try:
            data = httpRequestManager.OpenUrl(bannerURL)[0].read()
            bmp = wx.ImageFromStream(StringIO(data)).Scale(2000, 150).Blur(5).AdjustChannels(0.4, 0.4, 0.4).ConvertToBitmap()
            self.banner = bmp
            self.Refresh()
        except:
            print('except: download failed')
