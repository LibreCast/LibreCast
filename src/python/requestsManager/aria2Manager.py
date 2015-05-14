# -*- coding: utf-8 -*-

import xmlrpclib
import math

class Aria2Manager(object):
	def __init__(self):
		self.rpc = xmlrpclib.ServerProxy('http://localhost:6800/rpc')

	def addDownload(self,url):
		return self.rpc.aria2.addUri([url])

	def removeDownload(self,gid):
		self.rpc.aria2.remove(gid)

	def pause(self):
		self.rpc.aria2.pauseAll()

	def getInfos(self,gid):
		return self.rpc.aria2.tellStatus(gid)

	def getProgressPercentage(self,gid):
		infos = self.getInfos(gid)
		
		current = infos['completedLength']
		total = infos['totalLength']
		
		return math.trunc((float(current)/float(total)) * 100)
