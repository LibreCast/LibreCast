import wx


class AScrolledWindow(wx.ScrolledWindow):

    def __init__(self, parent):
        self.parent = parent
        wx.ScrolledWindow.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL)
        gb = wx.GridBagSizer(vgap=0, hgap=3)
        self.sizer = gb
        self._labels = []
        self._show_but = wx.Button(self, -1, "Show")
        self._hide_but = wx.Button(self, -1, "Hide")
        gb.Add(self._show_but, (0, 0), (1, 1))
        gb.Add(self._hide_but, (0, 1), (1, 1))
        for y in xrange(1, 30):
            self._labels.append(wx.StaticText(self, -1, "Label #%d" % (y,)))
            gb.Add(self._labels[-1], (y, 1), (1, 1))
        self._show_but.Bind(wx.EVT_BUTTON, self.OnShow)
        self._hide_but.Bind(wx.EVT_BUTTON, self.OnHide)
        self.SetSizer(self.sizer)
        fontsz = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT).GetPixelSize()
        self.SetScrollRate(fontsz.x, fontsz.y)
        self.EnableScrolling(True, True)

    def OnShow(self, event):
        for lab in self._labels:
            self.sizer.Show(lab, True)
        self.OnInnerSizeChanged()

    def OnHide(self, event):
        for lab in self._labels:
            self.sizer.Show(lab, False)
        self.OnInnerSizeChanged()

    def OnInnerSizeChanged(self):
        w, h = self.sizer.GetMinSize()
        self.SetVirtualSize((w, h))


class TestFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Programmatic size change')
        sz = wx.BoxSizer(wx.VERTICAL)
        pa = AScrolledWindow(self)
        sz.Add(pa, 1, wx.EXPAND)
        self.SetSizer(sz)


def main():
    wxapp = wx.App()
    fr = TestFrame()
    fr.Show(True)
    wxapp.MainLoop()

if __name__ == '__main__':
    main()
