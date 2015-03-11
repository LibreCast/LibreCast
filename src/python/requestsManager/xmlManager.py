# -*- coding: utf-8 -*-

import xml.dom.minidom
from xml.parsers.expat import ExpatError


def GetText(nodeList):
    rc = []
    for node in nodeList:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def ParseXml(file):
    # Initialiser la variable
    output = ''

    # Un bloc try/catch pour capturer les exceptions lorsqu'on parse le xml
    try:
        # Parser le fichier
        flux_parser = xml.dom.minidom.parseString(file)
        # Transformer le fichier parser en texte
        output = GetText(flux_parser.getElementsByTagName("title")[0].childNodes)

    # Si le fichier xml est mal formé
    except ExpatError, e:
        print '*** ERROR START ***'
        print 'XML Error: ', e
        print '***  ERROR END  ***\n'

    return output
