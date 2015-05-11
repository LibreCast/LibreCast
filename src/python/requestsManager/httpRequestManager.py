# -*- coding: utf-8 -*-

import urllib2
import httplib

# Liste de codes d'erreur qui pourraient suggérer qu'ajouter "/feed.xml" ou "/feed.rss" donne une URL valide
handledCodes = ['404', '410', '415', '418', '500']


def OpenUrl(url):
    # Initialiser les variables
    output = ''
    success = True

    # Un bloc try/catch pour capturer les exceptions lors de la requête, s'il y en a
    try:
        # Télécharger le fichier situé à l'adresse indiquée
        output = urllib2.urlopen(url,timeout=5)

    # Si le téléchargement donne une erreur http (ex : 404)
    except urllib2.HTTPError, e:
        print '*** ERROR START ***'
        print 'Error for url: ' + url
        print 'HTTPError: ' + str(e.code)
        print '***  ERROR END  ***\n'
        success = False

    return output, success
