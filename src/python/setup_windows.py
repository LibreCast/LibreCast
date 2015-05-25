# -*- coding: utf-8 -*-

"""
Usage:
    python setup.py py2exe

py2exe is necessary, or it won't run
"""
from distutils.core import setup
import py2exe

DATA_FILES = [('', ['aria2c.exe']),
              ('uiManager/resources', ['uiManager/resources/add.png']),
              ('uiManager/resources', ['uiManager/resources/cancel.png']),
              ('uiManager/resources', ['uiManager/resources/cancelPressed.png']),
              ('uiManager/resources', ['uiManager/resources/defaultChannelIcon.png']),
              ('uiManager/resources', ['uiManager/resources/defaultVideoImage.png']),
              ('uiManager/resources', ['uiManager/resources/Dnd.png']),
              ('uiManager/resources', ['uiManager/resources/downloads.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 1.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 2.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 3.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 4.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 5.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 6.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 7.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 8.png']),
              ('uiManager/resources', ['uiManager/resources/downloads - 9.png']),
              ('uiManager/resources', ['uiManager/resources/feeds.png']),
              ('uiManager/resources', ['uiManager/resources/fullScreen.png']),
              ('uiManager/resources', ['uiManager/resources/fullScreenSelected.png']),
              ('uiManager/resources', ['uiManager/resources/pause.png']),
              ('uiManager/resources', ['uiManager/resources/pauseSelected.png']),
              ('uiManager/resources', ['uiManager/resources/play.png']),
              ('uiManager/resources', ['uiManager/resources/playSelected.png']),
              ('uiManager/resources', ['uiManager/resources/playlists.png']),
              ('uiManager/resources', ['uiManager/resources/refresh.png']),
              ('uiManager/resources', ['uiManager/resources/remove.png']),
              ('uiManager/resources', ['uiManager/resources/reveal.png']),
              ('uiManager/resources', ['uiManager/resources/revealPressed.png']),
              ('uiManager/resources', ['uiManager/resources/windowed.png']),
              ('uiManager/resources', ['uiManager/resources/windowedSelected.png'])]

OPTIONS = {'includes': ['lxml', 'lxml._elementpath'],
           'dll_excludes': ['w9xpopen.exe', 'MSVCP90.dll', 'mswsock.dll', 'powrprof.dll', 'MPR.dll', 'MSVCR100.dll', 'mfc90.dll'],
           'optimize': 2,
           'skip_archive': True}

setup(name='LibreCast',
      version='0.8.2',
      author='LibreCast',
      data_files=DATA_FILES,
      options={'py2exe': OPTIONS},
      windows=[{'script': 'main.pyw',
                'icon_resources': [(0, 'uiManager/resources/icon.ico')]}])
