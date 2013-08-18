# -*- coding: utf-8 -*-
import urllib, urllib2, re, sys, xbmcplugin, xbmcgui
import cookielib, os, string, cookielib, StringIO
import os, time, base64, logging, calendar
import xbmcaddon


scriptID = 'plugin.video.mrknow'
scriptname = "Films online"
ptv = xbmcaddon.Addon(scriptID)

#BASE_RESOURCE_PATH = os.path.join( os.getcwd(), "resources" )
BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )
sys.path.append( os.path.join( ptv.getAddonInfo('path'), "host" ) )

import pLog, settings, Parser
import noobroom, iptak, wykop, meczyki, joemonster, tosiewytnie, drhtvcompl, milanos,filmbox,vodpl
import filmboxmoovie,filmmex,plej,cdapl,nextplus
import kinolive,tvpstream,kinoliveseriale,scs,netvi,filmsonline,mmtv
#import weebtv, ipla, stations, tvp, tvn, iplex, tvpvod, 
import iptak,goodcast,streamon,strefavod,wrzuta,tvppl

log = pLog.pLog()


MENU_TABLE = { #1000: "www.mrknow.pl [filmy online]",
               
               2100: "xbmcfilm.com"
}

class MrknowFilms:
  def __init__(self):
    log.info('xbmcfilm.com')
    self.settings = settings.TVSettings()
    self.parser = Parser.Parser()

  def showListOptions(self):
    params = self.parser.getParams()
    mode = self.parser.getIntParam(params, "mode")
    name = self.parser.getParam(params, "name")
    service = self.parser.getParam(params, 'service')    
    if mode == None and name == None and service == None:
        log.info('Wyświetlam kategorie')
        self.CATEGORIES()

        
    elif mode == 1 or service == 'xbmcfilm.com':
        tv = xbmcfilm.xbmcfilm()
        tv.handleService()

    elif mode == 20:
        log.info('Wyświetlam ustawienia')
        self.settings.showSettings()
        
  def CATEGORIES(self):

        self.addDir("xbmcfilm.com", 1, False, 'xbmcfilm.com', False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

  def listsTable(self, table):
    for num, val in table.items():
      nTab.append(val)
    return nTab


  def LIST(self, table = {}):
      valTab = []
      strTab = []
      for num, tab in table.items():
          strTab.append(num)
          strTab.append(tab[0])
	  strTab.append(tab[1])
          valTab.append(strTab)
          strTab = []
      valTab.sort(key = lambda x: x[1])      
      for i in range(len(valTab)):
          if valTab[i][2] == '': icon = False
          else: icon = valTab[i][2]
          self.addDir(valTab[i][1], valTab[i][0], False, icon, False)
      xbmcplugin.endOfDirectory(int(sys.argv[1]))


  def addDir(self, name, mode, autoplay, icon, isPlayable = True):
    #print("Dane",name, mode, autoplay, icon, isPlayable)
    u=sys.argv[0] + "?mode=" + str(mode)
    if icon != False:
      icon = os.path.join(ptv.getAddonInfo('path'), "images/") + icon + '.png'
    else:
      icon = "DefaultVideoPlaylists.png"
    liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage='')
    if autoplay and isPlayable:
      liz.setProperty("IsPlayable", "true")
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,listitem=liz, isFolder= not autoplay)

init = MrknowFilms()
init.showListOptions()
