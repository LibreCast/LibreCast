# -*- coding: utf-8 -*-

import wx

class BigMessagePanel(wx.Panel):
    def __init__(self, parent, message):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(200, 200), style=wx.ALIGN_CENTER)
        
        self.SetBackgroundColour('#F0F0F0')

        innerBox = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        text = wx.StaticText(self, id=wx.ID_ANY, label=message, style=wx.ALIGN_CENTER)
        text.SetFont(font)
        innerBox.Add(text, 0, wx.CENTER | wx.TOP, border=100)

        self.SetSizer(innerBox)