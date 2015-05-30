#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importer les librairies sqlite3, regex, sys et os
import os
import sys
import database
import subprocess
import wx

# Importer nos modules personnels
from uiManager import mainWindow

# Set root path
try:
    approot = os.path.dirname(os.path.abspath(__file__))
except NameError:
    approot = os.path.dirname(os.path.abspath(sys.argv[0]))


def main():
    # Chemins utilisés par LibreCast
    userDirectory = os.path.expanduser('~')
    librecastDirectory = os.path.join(userDirectory, 'LibreCast')
    databaseFile = os.path.join(librecastDirectory, 'database.db')
    downloadDirectory = os.path.join(librecastDirectory, 'Downloads')
    logFile = os.path.join(librecastDirectory, 'LibreCastlogs.log')
    aria2LogFile = os.path.join(librecastDirectory, 'aria2logs.log')

    # Si ce dossier n'existe pas
    if not os.path.exists(downloadDirectory):
        # Le créer
        os.makedirs(downloadDirectory)

    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = approot

    cwd = base_path

    # Si windows
    if sys.platform == 'win32':
        # Faire en sorte que la console soit cachée
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Créer un subprocess avec aria2c.exe en mode silencieux, avec un logfile
        proc = subprocess.Popen(
            ['./aria2c.exe', '--enable-rpc', '--dir=%s' % downloadDirectory, '--quiet=true', '--log=%s' % aria2LogFile],
            cwd=cwd,
            startupinfo=startupinfo,
        )
    else:
        # Créer un subprocess avec aria2c en mode silencieux, avec un logfile
        proc = subprocess.Popen(
            ['./aria2c', '--enable-rpc', '--dir=%s' % downloadDirectory, '--quiet=true', '--log=%s' % aria2LogFile],
            cwd=cwd,
        )

    # Connexion à la base de donnée
    database_instance = database.Database(databaseFile)
    database_instance.initDB()

    # Appeler la classe créant l'interface.
    # Note : Lorsqu'on entre dans la boucle principale de l'interface, on ne peut plus intéragir avec la console via input()
    app = wx.App(redirect=True, filename=logFile)
    app.SetAppName('LibreCast')
    main = mainWindow.mainUI(None, wx.ID_ANY, database_instance)
    aria2Manager = main.getDownloadEngine()
    app.MainLoop()

    # Fermeture de la base de donnée
    database_instance.close()

    # Fermer aria2 (qui tourne en tâche de fond)
    aria2Manager.kill()

"""
Condition pour vérifier que le fichier est directement executé
(par exemple depuis une ligne de commande)
et n'est pas importé depuis un autre fichier, ce qui ferait de lui un module
"""
if __name__ == '__main__':
    main()
