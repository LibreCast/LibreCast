# -*- coding: utf-8 -*-

import urllib2
import httplib

# Liste de codes d'erreur qui pourraient suggérer qu'ajouter "/feed.xml" ou "/feed.rss" donne une URL valide
handledCodes = ['404', '410', '415', '418', '500']


def OpenUrl(url):
    # Initialiser les variables
    output = ''
    tryNewPath = False

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

        if str(e.code) in handledCodes:
            tryNewPath = True

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

    return output, tryNewPath
