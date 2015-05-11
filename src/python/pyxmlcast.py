#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree

class PyXMLCast(object):
    def __init__(self, xmlFile):
        self.channel = etree.parse(xmlFile).find('channel')

    def getChannelName(self):
        return self.channel.find('title').text

    def getChannelDescription(self):
        return self.channel.find('description').text

    def getChannelURL(self):
        return self.channel.find('link').text

    def getAllVideos(self):
        items = self.channel.findall('item')
        videos = []
        
        for item in items:
            video = {
                'title':item.find('title').text,
                'description':item.find('itunes:summary',namespaces={
                    'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'
                }).text,
                'length':item.find('itunes:duration',namespaces={
                    'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'
                }).text,
                'author':item.find('itunes:author',namespaces={
                    'itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd'
                }).text,
                'pubdate':item.find('pubDate').text
            }

            if item.find('magnet') is not None:
                video['url'] = item.find('magnet').text
            else:
                video['url'] = item.find('enclosure').attrib['url']

            videos += [video]

        return videos

