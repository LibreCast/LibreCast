# -*- coding: utf-8 -*-

import xmlrpclib
import math


class Aria2Manager(object):
    def __init__(self):
        self.rpc = xmlrpclib.ServerProxy('http://localhost:6800/rpc')

    def setSystemProxy(self):
        import urllib2
        proxies = urllib2.getproxies()

        for proxy in proxies:
            if proxy == 'http':
                print "aria2c --http-proxy='%s'" % proxies[proxy]
            elif proxy == 'https':
                print "aria2c --https-proxy='%s'" % proxies[proxy]
            elif proxy == 'ftp':
                print "aria2c --http-proxy='%s'" % proxies[proxy]

    def addDownload(self, url):
        return self.rpc.aria2.addUri([url])

    def removeDownload(self, gid):
        self.rpc.aria2.remove(gid)

    def pause(self):
        self.rpc.aria2.pauseAll()

    def getInfos(self, gid):
        return self.rpc.aria2.tellStatus(gid)

    def getProgress(self, gid):
        infos = self.getInfos(gid)

        current = infos['completedLength']
        total = infos['totalLength']

        if (int(total) == 0):
            return 0

        return math.trunc((float(current)/float(total)) * 1000)

    def getDownloadSpeed(self, gid):
        infos = self.getInfos(gid)

        return int(infos['downloadSpeed'])

    def remove(self, gid):
        self.rpc.aria2.remove(gid)

    def getSize(self, gid):
        infos = self.getInfos(gid)

        return int(infos['totalLength']), int(infos['completedLength'])

    def getETA(self, gid):
        infos = self.getInfos(gid)

        remainingSize = int(infos['totalLength']) - int(infos['completedLength'])

        if int(infos['downloadSpeed']) == 0:
            return -1

        return math.trunc(float(remainingSize)/float(infos['downloadSpeed']))

    def getDownloadedPath(self, gid):
        infos = self.getInfos(gid)

        return infos['files'][0]['path']

    def kill(self):
        self.rpc.aria2.shutdown()
