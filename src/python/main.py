#-*- coding: utf-8 -*-

# Importer la librairie sqlite3
import sqlite3
import urllib2
import xml.dom.minidom

def getText(nodeList):
    rc = []
    for node in nodeList:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

# Connexion à la base de donnée
base = sqlite3.connect('librecast.db')

# On crée un curseur (qui va agir sur la base)
curseur = base.cursor()

# On crée la table "feeds" uniquement si elle n'existe pas
curseur.execute('CREATE TABLE IF NOT EXISTS feeds (id INTEGER PRIMARY KEY AUTOINCREMENT, url text)')

# On demande une adresse de flux
adresse = raw_input("Une adresse siouplé monsieur : ")

if (adresse != ""):
    # On compte le nombre d'élément qui ont pour url la variable adresse
    curseur.execute('SELECT COUNT(*) FROM feeds WHERE url = :adresse',{"adresse":adresse})
    resultat = curseur.fetchone()[0]

    if (resultat > 0):
        print 'Cette adresse existe déjà'
    else:
        print 'Cette adresse est nouvelle, je vais l\'ajouter !'
        curseur.execute('INSERT INTO feeds (url) VALUES (:adresse)',{"adresse":adresse})
    
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
    # Télécharher le fichier situé à l'adresse indiquée
    resultat_de_la_requete = urllib2.urlopen(resultat[1])
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
