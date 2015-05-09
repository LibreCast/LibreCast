"""
Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']

DATA_FILES = [('requestsManager', ['requestsManager/__init__.py']),
              ('requestsManager', ['requestsManager/httpRequestManager.py']),
              ('requestsManager', ['requestsManager/xmlManager.py']),

              ('uiManager', ['uiManager/__init__.py']),
              ('uiManager', ['uiManager/listManager.py']),
              ('uiManager', ['uiManager/mainWindow.py']),
              ('uiManager', ['uiManager/treeManager.py']),
              ('uiManager', ['uiManager/videoManager.py']),

              ('uiManager/resources', ['uiManager/resources/add.png']),
              ('uiManager/resources', ['uiManager/resources/Dnd.png']),
              ('uiManager/resources', ['uiManager/resources/fullScreen.png']),
              ('uiManager/resources', ['uiManager/resources/fullScreenSelected.png']),
              ('uiManager/resources', ['uiManager/resources/pause.png']),
              ('uiManager/resources', ['uiManager/resources/pauseSelected.png']),
              ('uiManager/resources', ['uiManager/resources/play.png']),
              ('uiManager/resources', ['uiManager/resources/playSelected.png']),
              ('uiManager/resources', ['uiManager/resources/refresh.png']),
              ('uiManager/resources', ['uiManager/resources/remove.png']),
              ('uiManager/resources', ['uiManager/resources/windowed.png']),
              ('uiManager/resources', ['uiManager/resources/windowedSelected.png'])]

OPTIONS = {'argv_emulation': False,
           'iconfile': 'uiManager/resources/icon.icns',
           'includes': ['wx', 'wx.media', 'cPickle', 'threading.Thread', '__future__.division']}

setup(
    name='LibreCast',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
