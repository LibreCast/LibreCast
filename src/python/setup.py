# -*- coding: utf-8 -*-

"""
Usage:
    python setup.py py2app
"""

from setuptools import setup


APP = ['main.pyw']

DATA_FILES = [('', ['aria2c']),
              ('', ['pyxmlcast.py']),
              ('', ['database.py']),
              ('', ['converter.py']),

              ('requestsManager', ['requestsManager/__init__.py']),
              ('requestsManager', ['requestsManager/aria2Manager.py']),
              ('requestsManager', ['requestsManager/httpRequestManager.py']),
              ('requestsManager', ['requestsManager/xmlManager.py']),

              ('uiManager', ['uiManager/__init__.py']),
              ('uiManager', ['uiManager/listManager.py']),
              ('uiManager', ['uiManager/mainWindow.py']),
              ('uiManager', ['uiManager/treeManager.py']),
              ('uiManager', ['uiManager/videoManager.py']),

              ('resources', ['uiManager/resources/add.png']),
              ('resources', ['uiManager/resources/cancel.png']),
              ('resources', ['uiManager/resources/cancelPressed.png']),
              ('resources', ['uiManager/resources/defaultChannelIcon.png']),
              ('resources', ['uiManager/resources/defaultCoverImage.png']),
              ('resources', ['uiManager/resources/defaultVideoImage.png']),
              ('resources', ['uiManager/resources/Dnd.png']),
              ('resources', ['uiManager/resources/downloads.png']),
              ('resources', ['uiManager/resources/downloads - 1.png']),
              ('resources', ['uiManager/resources/downloads - 2.png']),
              ('resources', ['uiManager/resources/downloads - 3.png']),
              ('resources', ['uiManager/resources/downloads - 4.png']),
              ('resources', ['uiManager/resources/downloads - 5.png']),
              ('resources', ['uiManager/resources/downloads - 6.png']),
              ('resources', ['uiManager/resources/downloads - 7.png']),
              ('resources', ['uiManager/resources/downloads - 8.png']),
              ('resources', ['uiManager/resources/downloads - 9.png']),
              ('resources', ['uiManager/resources/feeds.png']),
              ('resources', ['uiManager/resources/fullScreen.png']),
              ('resources', ['uiManager/resources/fullScreenSelected.png']),
              ('resources', ['uiManager/resources/pause.png']),
              ('resources', ['uiManager/resources/pauseSelected.png']),
              ('resources', ['uiManager/resources/play.png']),
              ('resources', ['uiManager/resources/playSelected.png']),
              ('resources', ['uiManager/resources/playlists.png']),
              ('resources', ['uiManager/resources/refresh.png']),
              ('resources', ['uiManager/resources/remove.png']),
              ('resources', ['uiManager/resources/reveal.png']),
              ('resources', ['uiManager/resources/revealPressed.png']),
              ('resources', ['uiManager/resources/windowed.png']),
              ('resources', ['uiManager/resources/windowedSelected.png'])]

OPTIONS = {'argv_emulation': False,
           'excludes': ['setup.py', 'setup_windows.py'],
           'iconfile': 'uiManager/resources/icon.icns'}

setup(
    name='LibreCast',
    version='0.8.2',
    author='LibreCast',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
