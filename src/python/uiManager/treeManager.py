# -*- encoding: utf-8 -*-

import wx

"""
Exemple de données possibles que l'on peut réccupérer du xml.
Il vaudrait mieux implémenter une fonction réccursive afin de
pourvoir avoir autant de sous-groupes que l'on veut, mais
les specs n'en prévoient qu'un nombre donné.
"""
data = {
    'Programmer': {
        'Operating Systems': ['Linux', 'FreeBSD', 'OpenBSD', 'NetBSD', 'Solaris'],
        'Programming Languages': ['Java', 'C++', 'C', 'Pascal', 'Python', 'Ruby', 'Tcl', 'PHP'],
        'Toolkits': ['Qt', 'MFC', 'wxPython', 'GTK+', 'Swing'],
    },
    'Other': {
        'Operating Systems': ['Windows'],
        'Programming Languages': [],
        'Toolkits': ['Paint']
    },
    'List': ['Hello', 'I\'m a list', 'How about you?', 'Who are you?']
}


class pyTree(wx.TreeCtrl):
    def __init__(self, parent, id, style=''):
        """
        Initialize function
        """
        wx.TreeCtrl.__init__(self, parent, id)

        if style:
            self.SetWindowStyle(style)

        self.root = self.AddRoot('Data')

        for group in data.keys():
            newGroup = self.AppendItem(self.root, group)
            if isinstance(data[group], dict):
                for subGroup in data[group]:
                    newSubGroup = self.AppendItem(newGroup, subGroup)
                    if isinstance(data[group][subGroup], list):
                        for item in data[group][subGroup]:
                            self.AppendItem(newSubGroup, item)
            elif isinstance(data[group], list):
                for item in data[group]:
                    self.AppendItem(newGroup, item)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=self.GetId())

        self.output = None

    def SetOutput(self, output):
        """
        Set output function (accepts single string). Used to display string
        representation of the selected object by OnSelChanged.
        """
        self.output = output

    def OnSelChanged(self, event):
        """
        If an output function is defined, we try to print some
        informative, interesting and thought-provoking stuff to it.
        """
        if not self.output:
            return

        apply(self.output, ('Not done yet',))
