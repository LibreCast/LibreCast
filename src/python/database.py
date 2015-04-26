#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3


class Database(object):
    def __init__(self, dbfile):
        super(Database, self).__init__()
        self.base = sqlite3.connect(dbfile)

    def initDB(self):
        cursor = self.base.cursor()

        # Création de la table des flux
        cursor.execute('CREATE TABLE IF NOT EXISTS feeds (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            url text\
        )')

        # Création de la table des vidéos
        cursor.execute('CREATE TABLE IF NOT EXISTS videos (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            name text,\
            urls text,\
            length int,\
            publisher text,\
            pubdate date\
        )')

        # Création de la table des vidéos
        cursor.execute('CREATE TABLE IF NOT EXISTS playlists (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            name text\
        )')

        # Création de la table des vidéos
        cursor.execute('CREATE TABLE IF NOT EXISTS playlistsVideos (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            videoId int,\
            playlistId int\
        )')

        self.base.commit()

    def insertFeed(self, url):
        cursor = self.base.cursor()

        # Insertion du flux dans la table feeds
        cursor.execute('INSERT INTO feeds (url) VALUES (:url)', {"url": url})

        self.base.commit()

    def removeFeed(self, fluxId):
        cursor = self.base.cursor()

        # Délétion du flux dans la table feeds
        cursor.execute('DELETE FROM feeds WHERE id = :id', {'id': fluxId})

        self.base.commit()

    def createPlaylist(self, name):
        cursor = self.base.cursor()

        # Création de la playlist
        cursor.execute('INSERT INTO playlists (name) VALUES (:name)', {"name": name})

        self.base.commit()

    def getPlaylists(self):
        cursor = self.base.cursor()

        # On séléctionne toutes les playlists
        cursor.execute('SELECT (name) FROM playlists')

        return cursor.fetchall()

    def getPlaylistIDFromName(self, name):
        cursor = self.base.cursor()

        cursor.execute('SELECT * FROM playlists WHERE name=(:name)', {"name": name})

        allRows = cursor.fetchall()
        return allRows[0][0]

    def removePlaylist(self, playlistId):
        cursor = self.base.cursor()

        # Délétion de la playlist dans la table playlists
        cursor.execute('DELETE FROM playlists WHERE id = :id', {'id': playlistId})

        self.base.commit()

    def getVideosFromPlaylist(self, playlistId):
        cursor = self.base.cursor()

        # On séléctionne toutes les playlists
        cursor.execute('SELECT * FROM playlistsVideos WHERE playlistId = :id', {'id': playlistId})

        return cursor.fetchall()

    def getAllVideos(self):
        #TODO
        cursor = self.base.cursor()

        #cursor.execute('SELECT () FROM')

    def insertVideoInPlaylist(self, videoId, playlistId):
        cursor = self.base.cursor()

        cursor.execute('INSERT INTO playlistsVideos (playlistId,videoId) VALUES (:playlistId,:videoId)', {
            'playlistId': playlistId,
            'videoId': videoId
        })

        self.base.commit()

    def removeVideoInPlaylist(self, videoId, playlistId):
        cursor = self.base.cursor()

        # Délétion de la playlist dans la table playlists
        cursor.execute('DELETE FROM playlistsVideos WHERE playlistId = :playlistId AND videoId = :videoId', {
            'playlistId': playlistId,
            'videoId': videoId
        })

        self.base.commit()

    def close(self):
        cursor = self.base.cursor()
        self.base.close()
