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
            url text,\
            icon text\
        )')

        # Création de la table des vidéos
        cursor.execute('CREATE TABLE IF NOT EXISTS videos (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            name text,\
            urls text,\
            length text,\
            publisher text,\
            pubdate text,\
            image BLOB,\
            fluxid int\
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
        cursor.execute('INSERT INTO feeds (url, icon) VALUES (:url, :icon)', {'url': url, 'icon': ''})

        self.base.commit()

    def insertIconInFeed(self, feedID, icon):
        cursor = self.base.cursor()

        cursor.execute('UPDATE feeds SET icon = :icon WHERE id = :feedID', {
            'feedID': feedID,
            'icon': icon
        })

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

    def removePlaylist(self, playlistId):
        cursor = self.base.cursor()

        # Délétion de la playlist dans la table playlists
        cursor.execute('DELETE FROM playlists WHERE id = :id', {'id': playlistId})

        self.base.commit()

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

    def renamePlaylist(self, playlistID, newPlaylistName):
        cursor = self.base.cursor()

        cursor.execute('UPDATE playlists SET name = :newName WHERE id = :playlistId', {
            'playlistId': playlistID,
            'newName': newPlaylistName
        })

        self.base.commit()

    def getFeeds(self):
        cursor = self.base.cursor()

        # On séléctionne toutes les playlists
        cursor.execute('SELECT * FROM feeds')

        return cursor.fetchall()

    def getFeedIDFromURL(self, url):
        cursor = self.base.cursor()

        cursor.execute('SELECT * FROM feeds WHERE url=(:url)', {"url": url})
        allRows = cursor.fetchall()

        if allRows:
            return allRows[0][0]
        else:
            return -1

    def getPlaylistIDFromName(self, name):
        cursor = self.base.cursor()

        cursor.execute('SELECT * FROM playlists WHERE name=(:name)', {"name": name})
        allRows = cursor.fetchall()

        if allRows:
            return allRows[0][0]
        else:
            return -1

    def getVideoIDFromName(self, name):
        cursor = self.base.cursor()

        cursor.execute('SELECT * FROM videos WHERE name=(:name)', {"name": name})
        allRows = cursor.fetchall()

        if allRows:
            return allRows[0][0]
        else:
            return -1

    def getPlaylists(self):
        cursor = self.base.cursor()

        # On séléctionne toutes les playlists
        cursor.execute('SELECT (name) FROM playlists')

        return cursor.fetchall()

    def getVideosFromPlaylist(self, playlistId):
        cursor = self.base.cursor()

        # On séléctionne toutes les playlists
        cursor.execute('SELECT * FROM playlistsVideos WHERE playlistId = :id', {'id': playlistId})

        return cursor.fetchall()

    def insertVideo(self, name, urls, length, author, pubdate, image, fluxId):
        cursor = self.base.cursor()

        cursor.execute('INSERT INTO videos (name,urls,length,publisher,pubdate,image,fluxid) VALUES (:name,:urls,:length,:publisher,:pubdate,:image,:fluxid)', {
                "urls": urls,
                "name": name,
                "length": length,
                "publisher": author,
                "pubdate": pubdate,
                "image": image,
                "fluxid": fluxId,
            })

        self.base.commit()

    def getAllVideos(self):
        cursor = self.base.cursor()

        cursor.execute('SELECT * FROM videos')

        return cursor.fetchall()

    def getVideosFromFeed(self, fluxId):
        cursor = self.base.cursor()

        cursor.execute('SELECT * FROM videos WHERE fluxid = :id', {"id": fluxId})

        return cursor.fetchall()

    def removeAllVideos(self):
        cursor = self.base.cursor()

        cursor.execute('DELETE FROM videos')

        self.base.commit()

    def close(self):
        cursor = self.base.cursor()
        self.base.close()
