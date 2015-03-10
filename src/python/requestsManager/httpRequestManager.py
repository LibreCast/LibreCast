# -*- coding: utf-8 -*-

import urllib2
import httplib


def openUrl(url):
    # Initialiser la variable
    output = ''

    # Un bloc try/catch pour capturer les exceptions lors de la requête, s'il y en a
    try:
        # Télécharger le fichier situé à l'adresse indiquée
        output = urllib2.urlopen(url)

    # Si le téléchargement donne une erreur http (ex : 404)
    except urllib2.HTTPError, e:
        print '*** ERROR START ***'
        print 'Error for url: ' + url
        print 'HTTPError: ' + str(e.code)
        print '***  ERROR END  ***\n'

    # Si le téléchargement donne une erreur d'URL (ex : URL non conforme ou serveur indisponible)
    except urllib2.URLError, e:
        print '*** ERROR START ***'
        print 'Error for url: ' + url
        print 'URLError: ' + str(e.reason)
        print '***  ERROR END  ***\n'

    # Si le téléchargement donne une autre erreur (ex : protocole inconnu)
    except httplib.HTTPException, e:
        print '*** ERROR START ***'
        print 'Error for url: ' + url
        print 'HTTPException: ' + str(e)
        print '***  ERROR END  ***\n'

    return output
