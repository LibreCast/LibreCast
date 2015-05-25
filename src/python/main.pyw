#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importer les librairies sqlite3, regex, sys et os
import os
import sys
import database
import subprocess

# Importer nos modules personnels
from uiManager import mainWindow
from requestsManager import httpRequestManager
from requestsManager import xmlManager

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

    # Si ce dossier n'existe pas
    if not os.path.exists(downloadDirectory):
        # Le créer
        os.makedirs(downloadDirectory)

    try:
        cwd = os.path.dirname(os.path.realpath(__file__))
    except:
        cwd = os.path.dirname(sys.argv[0])

    # Si windows
    if sys.platform == 'win32':
        # Faire en sorte que la console soit cachée
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Créer un subprocess avec aria2c.exe en mode silencieux, avec un logfile
        proc = subprocess.Popen(
            ['./aria2c.exe', '--enable-rpc', '--dir=%s' % downloadDirectory, '--quiet=true', '--log=aria2logs.log'],
            cwd=cwd,
            startupinfo=startupinfo,
        )
    else:
        # Créer un subprocess avec aria2c en mode silencieux, avec un logfile
        proc = subprocess.Popen(
            ['./aria2c', '--enable-rpc', '--dir=%s' % downloadDirectory, '--quiet=true', '--log=aria2logs.log'],
            cwd=cwd,
        )

    # Connexion à la base de donnée
    database_instance = database.Database(databaseFile)
    database_instance.initDB()

    # Appeler la classe créant l'interface.
    # Note : Lorsqu'on entre dans la boucle principale de l'interface, on ne peut plus intéragir avec la console via input()
    mainWindow.main(database_instance)

    # Fermeture de la base de donnée
    database_instance.close()

    # Fermer le subprocess
    proc.terminate()
    # Et là, on a perdu la patience
    os.kill(proc.pid, signal.SIGINT)

"""
Condition pour vérifier que le fichier est directement executé
(par exemple depuis une ligne de commande)
et n'est pas importé depuis un autre fichier, ce qui ferait de lui un module
"""
if __name__ == '__main__':
    main()
