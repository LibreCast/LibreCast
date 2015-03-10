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

        # Si au moins un stule a été précisé dans la création de l'abre...
        if style:
            # ...on l'applique
            self.SetWindowStyle(style)

        # On créer la racine de l'arbre, c'est ce qui contiendra toutes nos playlistes etc. On choisit de ne pas l'afficher, mais uniquement son contenu (cf. styles)
        self.root = self.AddRoot('Data')

        # On décompose les données délivrées avec l'arbre, et on les affiche dans ce dernier
        # Note : À étudier en même temps que la variable 'data', puisque c'est de là qu'on extrait les données
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

        # Lorsqu'on élément de l'abre est sélectionné, on appelle la fonction OnSelChanged
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=self.GetId())

        # Par défaut, on ne sait pas s'il y a une zone de texte modifiable
        self.output = None

    def SetOutput(self, output):
        """
        Permet d'ajouter la fonction permettant de modifier la
        zone de texte située à droite de l'abre.
        """
        self.output = output

    def OnSelChanged(self, event):
        # Si on n'a pas ajouté la zone de texte avec SetOutput, on ne peut pas modifier le texte
        if not self.output:
            return

        # Sinon, on affiche le texte
        apply(self.output, ('Not done yet',))
