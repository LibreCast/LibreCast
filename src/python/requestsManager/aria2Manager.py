# -*- coding: utf-8 -*-

import xmlrpclib

class Aria2Manager(object):
	def __init__(self):
		self.rpc = xmlrpclib.ServerProxy('http://localhost:6800/rpc')

	def addDownload(self,url):
		return self.rpc.aria2.addUri([url])

	def removeDownload(self,gid):
		self.rpc.aria2.remove(gid)

	def pause(self):
		self.rpc.aria2.pauseAll()

	def getProgession(self,gid):
		self.rpc.aria2.tellStatus(gid)