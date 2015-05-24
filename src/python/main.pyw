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


def callHttpManager(urlList):
    # On affiche le fichier situé à chaque URL
    for resultat in urlList:

        # Initialiser la variable
        resultat_de_la_requete, tryNewPath = httpRequestManager.OpenUrl(resultat[1])

        # Si le téléchargement n'a pas donné d'erreur
        if resultat_de_la_requete != '':
            # Lire ce fichier
            titre = xmlManager.ParseXml(resultat_de_la_requete.read())

            # Si le "parsage" du xml n'a pas donné d'erreur
            if titre != '':
                print(titre)
            # Si le "parsage" du xml a donné une erreur
            else:
                pass

        # Si le téléchargement a donné une erreur
        elif tryNewPath:
            # Si l'url ne se termine pas par .xml
            if not resultat[1].endswith('.xml') and not resultat[1].endswith('.rss'):
                urlList.append(['0', str(resultat[1] + '/flux.xml')])
                urlList.append(['0', str(resultat[1] + '/feed.rss')])


def main():
    # Chemin où sont stockés les téléchargements
    downloadDirectory = os.path.join(os.path.dirname(approot), 'Downloads')

    # Si ce dossier n'existe pas
    if not os.path.exists(downloadDirectory):
        # Le créer
        os.makedirs(downloadDirectory)

    try:
        cwd = os.path.dirname(__file__)
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
    database_instance = database.Database(os.path.join(os.environ.get('RESOURCEPATH', approot), 'database.db'))
    database_instance.initDB()

    # Appeler la classe créant l'interface.
    # Note : Lorsqu'on entre dans la boucle principale de l'interface, on ne peut plus intéragir avec la console via input()
    mainWindow.main(database_instance)

    # Fermeture de la base de donnée
    database_instance.close()

    # Fermer le subprocess
    proc.terminate()
    # Attendre que ce soit terminé
    proc.wait()

"""
Condition pour vérifier que le fichier est directement executé
(par exemple depuis une ligne de commande)
et n'est pas importé depuis un autre fichier, ce qui ferait de lui un module
"""
if __name__ == '__main__':
    main()
