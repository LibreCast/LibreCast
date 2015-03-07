#-*- coding: utf-8 -*-

# Importer les librairies sqlite3, urllib2 (et httplib), minidom et regex
import sqlite3
import httplib
import urllib2
import xml.dom.minidom
import re


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
    curseur.execute('DELETE FROM feeds WHERE url = :adresse',{'adresse':adresse})

# On sépare !
print '-----------------------------'

# On demande tous les feeds
curseur.execute('SELECT * FROM feeds')

# On récupère tous les résultats
resultats = curseur.fetchall()

# On affiche le fichier situé à chaque URL
for resultat in resultats:
    # Initialiser la variable
    resultat_de_la_requete = ''

    # Un bloc try/catch pour capturer les exceptions lors de la requête, s'il y en a
    try:
        # Télécharger le fichier situé à l'adresse indiquée
        resultat_de_la_requete = urllib2.urlopen(resultat[1])

    # Si le téléchargement donne une erreur http (ex : 404)
    except urllib2.HTTPError, e:
        print 'HTTPError: ' + str(e.code)

    # Si le téléchargement donne une erreur d'URL (ex : URL non conforme ou serveur indisponible)
    except urllib2.URLError, e:
        print 'URLError: ' + str(e.reason)

    # Si le téléchargement donne une autre erreur (ex : protocole inconnu)
    except httplib.HTTPException, e:
        print 'HTTPException: ' + str(e)

    # Si le téléchargement n'a pas donné d'erreur
    if resultat_de_la_requete != '':
        # Lire ce fichier
        flux = resultat_de_la_requete.read()
        # Parser le fichier
        flux_parser = xml.dom.minidom.parseString(flux)
        # Transformer le fichier parser en texte, et l'afficher
        print getText(flux_parser.getElementsByTagName("title")[0].childNodes)

# On enregistre les modifications
base.commit()

# On ferme la base
base.close()
