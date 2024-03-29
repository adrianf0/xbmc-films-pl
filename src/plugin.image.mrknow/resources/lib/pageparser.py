# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcaddon, xbmc, xbmcgui, simplejson
import urlparse
import httplib 

scriptID = 'plugin.video.mrknow'
scriptname = "Wtyczka XBMC www.mrknow.pl"
ptv = xbmcaddon.Addon(scriptID)

import pLog, Parser, settings, pCommon, urlparser


log = pLog.pLog()
sets = settings.TVSettings()


class pageparser:
  def __init__(self):
    self.cm = pCommon.common()
    self.up = urlparser.urlparser()
    


  def hostSelect(self, v):
    hostUrl = False
    d = xbmcgui.Dialog()
    if len(v) > 0:
      valTab = []
      for i in range(len(v)):
	valTab.append(str(i+1) + '. ' + self.getHostName(v[i], True))
      item = d.select("Wybor hostingu", valTab)
      if item >= 0: hostUrl = v[item]
    else: d.ok ('Brak linkow','Przykro nam, ale nie znalezlismy zadnego linku do video.', 'Sproboj ponownie za jakis czas')
    return hostUrl


  def getHostName(self, url, nameOnly = False):
    hostName = ''       
    match = re.search('http://(.+?)/',url)
    if match:
      hostName = match.group(1)
      if (nameOnly):
	n = hostName.split('.')
	hostName = n[-2]
    return hostName


  def getVideoLink(self, url):
    nUrl=''
    host = self.getHostName(url)
    log.info("video hosted by: " + host)
    log.info(url)
    
    if host == 'livemecz.com':
        nUrl = self.livemecz(url)
    elif host == 'www.drhtv.com.pl':
        nUrl = self.drhtv(url)
    elif host == 'www.realtv.com.pl':
        nUrl = self.realtv(url)
    elif host == 'www.transmisje.info':
        nUrl = self.transmisjeinfo(url)
    elif host == '79.96.137.217' or host == 'http://178.216.200.26':
        nUrl = self.azap(url)
    else:
        nUrl = self.pageanalyze(url)
#http://www.transmisje.info/kanal-3
    return nUrl
  
  def azap(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match1=re.compile('<meta http-equiv="Refresh" content="0; url=(.*?)" />').findall(link)
    if len(match1)>0:
        url = match1[0]
    query_data = { 'url': match1[0], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('file: "(.*?)"').findall(link)
    print ("Match",url,match,link)
    if len(match)>0:
        return match[0]
    else:
        return False
    
  
  def transmisjeinfo(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe width="(.*?)" height="(.*?)" src="(.*?)" scrolling="no" frameborder="0" style="border: 0px none transparent;">').findall(link)
    print ("Match",match)
    return self.pageanalyze('http://www.transmisje.info'+match[0][2],'http://www.transmisje.info')

  def realtv(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe frameborder="0" height="420" marginheight="0px" marginwidth="0px" name="RealTV.com.pl" scrolling="no" src="(.*?)" width="650">').findall(link)
    print ("Match",match)
    return self.pageanalyze(match[0],'http://www.realtv.com.pl')

 
  def livemecz(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe frameborder="0" height="480" marginheight="0px" marginwidth="0px" name="livemecz.com" scrolling="no" src="(.+?)" width="640"></iframe>').findall(link)
    query_data = { 'url': match[0], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe marginheight="0" marginwidth="0" name="livemecz.com" src="(.*?)" frameborder="0" height="480" scrolling="no" width="640">').findall(link)
    print ("Match",match)
    return self.pageanalyze(match[0],'http://livemecz.com/')

  def drhtv(self,url):
    return self.pageanalyze(url,'http://www.drhtv.com.pl/')

  def pageanalyze(self,url,referer=''):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<script type="text/javascript"> channel="(.*?)"; width="(.*?)"; height="(.*?)";</script><script type="text/javascript" src="http://yukons.net/share.js"></script>').findall(link)
    match1=re.compile("<script type='text/javascript'>fid='(.*?)'; v_width=(.*?); v_height=(.*?);</script><script type='text/javascript' src='http://www.reyhq.com/player.js'></script>").findall(link)
    match2=re.compile("<script type='text/javascript' src='http://www.sawlive.tv/embed/(.*?)'>").findall(link)
    match3=re.compile("<script type='text/javascript' src='http://sawlive.tv/embed/(.*?)'>").findall(link)
    match4=re.compile('<script type="text/javascript" src="http://www.ilive.to/embed/(.*?)&width=640&height=400&autoplay=true">').findall(link)
    match5=re.compile("<script type='text/javascript'> channel='(.*?)'; user='(.*?)'; width='640'; height='400';</script><script type='text/javascript' src='http://jimey.tv/player/jimeytv_embed.js'>").findall(link)
    match6=re.compile("<script type='text/javascript'> width=(.*?), height=(.*?), channel='(.*?)', e='(.*?)';</script><script type='text/javascript' src='http://www.mips.tv/content/scripts/mipsEmbed.js'>").findall(link)
    match7=re.compile('<script type="text/javascript">fid="(.*?)"; v_width=(.*?); v_height=(.*?);</script><script type="text/javascript" src="http://www.ukcast.tv/embed.js"></script>').findall(link)
    
    print ("Match",match2,match1,match,match3,match4,match5)
    if len(match) > 0:
        return self.up.getVideoLink('http://yukons.net/'+match[0][0])
    elif len(match1) > 0:
        return self.up.getVideoLink('http://www.reyhq.com/'+match1[0][0])
    elif len(match2) > 0:
        print ("Match2",match2)
        return self.up.getVideoLink('http://www.sawlive.tv/embed/'+match2[0],url)
    elif len(match3) > 0:
        return self.up.getVideoLink('http://www.sawlive.tv/embed/'+match3[0],url)
    elif len(match4) > 0:
        print ("Match4",match4)
        return self.up.getVideoLink('http://www.ilive.to/embed/'+match4[0],referer)
    elif len(match6) > 0:
        print ("Match6",match6[0])
        return self.up.getVideoLink('http://mips.tv/embedplayer/'+match6[0][2]+'/'+match6[0][3]+'/'+match6[0][0]+'/'+match6[0][1])
    elif len(match7) > 0:
        print ("Match7",match7)
        return self.up.getVideoLink('http://www.ukcast.tv/embed.php?u='+match7[0][0]+'&amp;vw='+match7[0][1]+'&amp;vh='+match7[0][2])


    else:
        return False





          
