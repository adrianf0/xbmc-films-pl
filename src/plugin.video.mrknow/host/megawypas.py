# -*- coding: utf-8 -*-
import urllib, urllib2, re, os, sys, math
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlparser
import json


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - megawypas"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, pCommon, Parser, settings

log = pLog.pLog()

mainUrl = 'http://www.megawypas.pl/'

HOST = 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3'

MENU_TAB = {1: "Wszystkie",
            3: "Szukaj" }


class megawypas:
    def __init__(self):
        log.info('Starting megawypas.pl')
        self.cm = pCommon.common()
        self.parser = Parser.Parser()
        self.up = urlparser.urlparser()
        self.cm = pCommon.common()
        self.settings = settings.TVSettings()
        self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "megawypas.cookie"


    def listsMainMenu(self):
        query_data = { 'url': mainUrl, 'use_host': True, 'host': HOST, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        print ("LLLL",link)
        match = re.compile("<br><img src='bullet.gif'></script>\r\n<a href='(.*?)'>(.*?)</a>", re.DOTALL).findall(link)
        print match
        for o in range(len(match)):
            self.add('megawypas', 'playSelectedMovie', 'None', match[o][1], 'None', match[o][0], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

       
    def getMovieLinkFromXML(self, url):
        #print ("URL",url)
        query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data)
        match = re.compile("file: '(.*?)',", re.DOTALL).findall(link)
        #print ("AAAAAAAAAAAAAA",match,url,link)
        if len(match)>0:
            linkVideo = match[0]
            linkVideo = linkVideo + ' pageUrl='+url+' swfUrl=http://megawypas.tv/jwplayer/jwplayer.flash.swf'
            return linkVideo
        else:
            return False
        

    

    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)
        #log.info(str(u))
        if name == 'main-menu' or name == 'categories-menu':
            title = category 
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
            

    def LOAD_AND_PLAY_VIDEO(self, videoUrl, title, icon):
        ok=True
        if videoUrl == '':
                d = xbmcgui.Dialog()
                d.ok('Nie znaleziono streamingu.', 'Może to chwilowa awaria.', 'Spróbuj ponownie za jakiś czas')
                return False
        liz=xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
        liz.setInfo( type="Video", infoLabels={ "Title": title, } )
        try:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoUrl, liz)
            
           # if not xbmc.Player().isPlaying():
           #     xbmc.sleep( 10000 )
                #xbmcPlayer.play(url, liz)
            
        except:
            d = xbmcgui.Dialog()
            d.ok('Błąd przy przetwarzaniu.', 'Problem')        
        return ok


    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        print(name,category,url,title)
        if name == None:
            self.listsMainMenu()
        elif name == 'main-menu' and category == 'Wszystkie':
            log.info('Jest Wszystkie: ')
            self.listsCategoriesMenu(chanels)
        if name == 'playSelectedMovie':
            self.LOAD_AND_PLAY_VIDEO(self.getMovieLinkFromXML(url), title, icon)
        
  