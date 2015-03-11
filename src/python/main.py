#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importer les librairies sqlite3, regex, sys et os
import sqlite3
import re
import os
import sys

from uiManager import mainWindow
from requestsManager import httpRequestManager
from requestsManager import xmlManager


def getText(nodeList):
    rc = []
    for node in nodeList:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def setWorkingDirectory():
    # On récupère l'adresse du dossier du fichier actuel (...LibreCast/python/)
    try:
        approot = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        approot = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Depuis cette adresse, on récupère le dossier dans lequel notre dossier est situé (.../LibreCast)
    approot = os.path.dirname(approot)

    # On cd à cette adresse pour créer le .db au bon endroit
    os.chdir(approot)


def main():
    # Modifier le dossier dans lequel la base de donnée sera utilisée
    setWorkingDirectory()

    # Connexion à la base de donnée
    base = sqlite3.connect('librecast.db')

    # On crée un curseur (qui va agir sur la base)
    curseur = base.cursor()

    # On crée la table "feeds" uniquement si elle n'existe pas
    curseur.execute('CREATE TABLE IF NOT EXISTS feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, url text)')

    # On demande une adresse de flux
    adresse = raw_input("Une adresse siouplé monsieur : ")

    if (adresse != ""):
        # Si l'adresse ne commence pas par "http://", "https://" ou "ftp://", on ajoute "http://"
        if (not re.match('(?:http|ftp|https)://', adresse)):
            adresse = 'http://' + adresse

        # On compte le nombre d'élément qui ont pour url la variable adresse
        curseur.execute('SELECT COUNT(*) FROM feeds WHERE url = :adresse', {"adresse": adresse})
        resultat = curseur.fetchone()[0]

        if (resultat > 0):
            print 'Cette adresse existe déjà'
        else:
            print 'Cette adresse est nouvelle, je vais l\'ajouter !'
            curseur.execute('INSERT INTO feeds (url) VALUES (:adresse)', {"adresse": adresse})

    # On sépare !
    print '-----------------------------'

    # On demande tous les feeds
    curseur.execute('SELECT * FROM feeds')

    # On récupère tous les résultats
    resultats = curseur.fetchall()

    # On les affiche
    for resultat in resultats:
        print resultat[1]

    if (raw_input("Voulez-vous supprimer une URL (oui/NON) ? ") == "oui"):
        adresse = raw_input("Quelle adresse : ")
        curseur.execute('DELETE FROM feeds WHERE url = :adresse', {'adresse': adresse})

    # On sépare !
    print '-----------------------------'

    # On demande tous les feeds
    curseur.execute('SELECT * FROM feeds')

    # On récupère tous les résultats
    resultats = curseur.fetchall()

    # On affiche le fichier situé à chaque URL
    for resultat in resultats:
        # Initialiser la variable
        resultat_de_la_requete = httpRequestManager.OpenUrl(resultat[1])

        # Si le téléchargement n'a pas donné d'erreur
        if resultat_de_la_requete != '':
            # Lire ce fichier
            titre = xmlManager.ParseXml(resultat_de_la_requete.read())

            if titre != '':
                print titre

        # Si le téléchargement a donné une erreur
        else:
            pass

    # On enregistre les modifications
    base.commit()

    # On ferme la base
    base.close()

    # Appeler la classe créant l'interface.
    # Note : Lorsqu'on entre dans la boucle principale de l'interface, on ne peut plus intéragir avec la console via input()
    mainWindow.main()

"""
Condition pour vérifier que le fichier est directement executé
(par exemple depuis une ligne de commande)
et n'est pas importé depuis un autre fichier, ce qui ferait de lui un module
"""
if __name__ == '__main__':
    main()
