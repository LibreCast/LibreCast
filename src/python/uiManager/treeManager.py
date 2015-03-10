# -*- encoding: utf-8 -*-

import wx


class pyTree(wx.TreeCtrl):
    """
    Code taken from the wxpython samples

    This wx.TreeCtrl derivative displays a tree view of a Python namespace.
    Anything from which the dir() command returns a non-empty list is a branch
    in this tree.
    """

    def __init__(self, parent, id, root):
        """
        Initialize function; because we insert branches into the tree
        as needed, we use the ITEM_EXPANDING event handler. The
        ITEM_COLLAPSED handler removes the stuff afterwards. The
        SEL_CHANGED handler attempts to display interesting
        information about the selected object.
        """
        wx.TreeCtrl.__init__(self, parent, id)
        self.root = self.AddRoot(str(root), -1, -1, wx.TreeItemData(root))

        if dir(root):
            self.SetItemHasChildren(self.root, True)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding, id=self.GetId())
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, id=self.GetId())
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=self.GetId())

        self.output = None
        self.Expand(self.root)

    def SetOutput(self, output):
        """
        Set output function (accepts single string). Used to display string
        representation of the selected object by OnSelChanged.
        """
        self.output = output

    def OnItemExpanding(self, event):
        """
        The real workhorse of this class. First we retrieve the object
        (parent) belonging to the branch that is to be expanded. This
        is done by calling GetPyData(parent), which is a short-cut for
        GetPyItemData(parent).Get().

        Then we get the dir() list of that object. For each item in
        this list, a tree item is created with associated
        wxTreeItemData referencing the child object. We get this
        object using child = getattr(parent, item).

        Finally, we check wether the child returns a non-empty dir()
        list. If so, it is labeled as 'having children', so that it
        may be expanded. When it actually is expanded, this function
        will again figure out what the offspring is.
        """
        item = event.GetItem()

        if self.IsExpanded(item):  # This event can happen twice in the self.Expand call
            return

        obj = self.GetPyData(item)
        lst = dir(obj)

        for key in lst:
            new_obj = getattr(obj, key)
            new_item = self.AppendItem(item, key, -1, -1,
                                       wx.TreeItemData(new_obj))

            if dir(new_obj):
                self.SetItemHasChildren(new_item, True)

    def OnItemCollapsed(self, event):
        """
        We need to remove all children here, otherwise we'll see all
        that old rubbish again after the next expansion.
        """
        item = event.GetItem()
        self.DeleteChildren(item)

    def OnSelChanged(self, event):
        """
        If an output function is defined, we try to print some
        informative, interesting and thought-provoking stuff to it.
        If it has a __doc__ string, we print it. If it's a function or
        unbound class method, we attempt to find the python source.
        """
        if not self.output:
            return

        obj = self.GetPyData(event.GetItem())
        msg = str(obj)

        apply(self.output, (msg,))
