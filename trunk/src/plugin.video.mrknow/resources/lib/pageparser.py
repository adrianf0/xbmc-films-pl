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

import pLog, Parser, settings, pCommon


log = pLog.pLog()
sets = settings.TVSettings()


class pageparser:
  def __init__(self):
    self.cm = pCommon.common()


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
    if host == 'www.drhtv.com.pl':
        nUrl = self.drhtv(url)
 
    return nUrl
#www.liveleak.com


  def livemecz(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe frameborder="0" height="480" marginheight="0px" marginwidth="0px" name="livemecz.com" scrolling="no" src="(.+?)" width="640"></iframe>').findall(link)
    query_data = { 'url': match[0], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match=re.compile('<iframe marginheight="0" marginwidth="0" name="livemecz.com" src="(.*?)" frameborder="0" height="480" scrolling="no" width="640">').findall(link)
    print ("Match",match)
    query_data = { 'url': match[0], 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)    
    match=re.compile('<script type="text/javascript"> channel="(.*?)"; width="640"; height="480";</script><script type="text/javascript" src="http://yukons.net/share.js"></script>').findall(link)
    print ("Match",match)
    query_data = { 'url': 'http://yukons.net/lb.php', 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link1 = self.cm.getURLRequestData(query_data)
    link1 = link1.replace("srv=", "");
    videolink = 'rtmp://' +link1 + '/kuyo/' + match[0] 
    videolink += ' pageUrl=http://yukons.net/watch/' + match[0] + ' live=true'
    videolink += ' swfVfy=http://yukons.net/yukplay.swf '
    print ("videolink", videolink)
    return videolink
    #
     

  def drhtv(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
#    print ("link", link)
    match=re.compile('<script type="text/javascript"> channel="(.*?)"').findall(link)
    print ("Match",match)
    query_data = { 'url': 'http://yukons.net/lb.php', 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link1 = self.cm.getURLRequestData(query_data)
    link1 = link1.replace("srv=", "");
    videolink = 'rtmp://' +link1 + '/kuyo/' + match[0] 
    videolink += ' pageUrl=http://yukons.net/watch/' + match[0] + ' live=true'
    videolink += ' swfVfy=http://yukons.net/yukplay.swf '
    print ("videolink", videolink)
    return videolink


  def parserHD3D(self,url):
    username = ptv.getSetting('hd3d_login')
    password = ptv.getSetting('hd3d_password')
    urlL = 'http://hd3d.cc/login.html'
    self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "hd3d.cookie"
    query_dataL = { 'url': urlL, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
    postdata = {'user_login': username, 'user_password': password}
    data = self.cm.getURLRequestData(query_dataL, postdata)
    query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match = re.compile("""url: ["'](.+?)["'],.+?provider:""").findall(link)
    if len(match) > 0:
      ret = match[0]
    else:
     ret = False
    return ret


  def parserSPROCKED(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match = re.search("""url: ['"](.+?)['"],.*\nprovider""",link)
    if match:    
      return match.group(1)
    else: 
      return False


  def parserODSIEBIE(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    try:
      (v_ext, v_file, v_dir, v_port, v_host) = re.search("\|\|.*SWFObject",link).group().split('|')[40:45]
      url = "http://%s.odsiebie.pl:%s/d/%s/%s.%s" % (v_host, v_port, v_dir, v_file, v_ext);
    except:
      url = False
    return url


  def parserWGRANE(self,url):
    hostUrl = 'http://www.wgrane.pl'            
    playlist = hostUrl + '/html/player_hd/xml/playlist.php?file='
    key = url[-32:]
    nUrl = playlist + key
    query_data = { 'url': nUrl, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match = re.search("""<mainvideo url=["'](.+?)["']""",link)
    if match:
      ret = match.group(1).replace('&amp;','&')
      return ret
    else: 
      return False


  def parserCDA(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match = re.search("""file: ['"](.+?)['"],""",link)
    if match:   
      return match.group(1)
    else: 
      return False


  def parserDWN(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match = re.search("""<iframe src="(.+?)&""",link)
    if match:
      query_data = { 'url': match.group(1), 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)
    else: 
      return False


  def parserANYFILES(self,url):
    self.anyfiles = anyfiles.serviceParser()
    retVal = self.anyfiles.getVideoUrl(url)
    return retVal
  
  
  def parserWOOTLY(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    c = re.search("""c.value="(.+?)";""",link)
    if c:
      cval = c.group(1)   
    else: 
      return False    
    match = re.compile("""<input type=['"]hidden['"] value=['"](.+?)['"].+?name=['"](.+?)['"]""").findall(link)
    if len(match) > 0:
      postdata = {};
      for i in range(len(match)):
        if (len(match[i][0])) > len(cval):
          postdata[cval] = match[i][1]
        else:
          postdata[match[i][0]] = match[i][1]
      self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
      self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "wootly.cookie"
      query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
      link = self.cm.getURLRequestData(query_data, postdata)
      match = re.search("""<video.*\n.*src=['"](.+?)['"]""",link)
      if match:
        return match.group(1)
      else: 
        return False
    else: 
      return False


  def parserMAXVIDEO(self, url):
      self.api = maxvideo.API()
      
      self.servset = sets.getSettings('maxvideo')
      if self.servset['maxvideo_notify'] == 'true': notify = True
      else: notify = False

      videoUrl = ''
      videoHash = url.split('/')[-1]
      login = self.api.Login(self.servset['maxvideo_login'], self.servset['maxvideo_password'], notify)
      if (login):
	  self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
	  cookiefile = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "maxvideo.cookie"	
      else: 
	  cookiefile = ''	
      videoUrl = self.api.getVideoUrl(videoHash, cookiefile, notify)
      return videoUrl
    
      
  def parserVIDEOWEED(self, url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match_domain = re.compile('flashvars.domain="(.+?)"').findall(link)
    match_file = re.compile('flashvars.file="(.+?)"').findall(link)
    match_filekey = re.compile('flashvars.filekey="(.+?)"').findall(link)
    if len(match_domain) > 0 and len(match_file) > 0 and len(match_filekey) > 0:
        get_api_url = ('%s/api/player.api.php?user=undefined&codes=1&file=%s&pass=undefined&key=%s') % (match_domain[0], match_file[0], match_filekey[0])
        link_api = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
        if 'url' in link_api:
              parser = Parser.Parser()
              params = parser.getParams(link_api)
              return parser.getParam(params, "url")
        else:
              return False
    else:
        return False
	
      
  def parserNOVAMOV(self, url):
      query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)
      match_file = re.compile('flashvars.file="(.+?)";').findall(link)
      match_key = re.compile('flashvars.filekey="(.+?)";').findall(link)
      if len(match_file) > 0 and len(match_key) > 0:
          get_api_url = ('http://www.novamov.com/api/player.api.php?key=%s&user=undefined&codes=1&pass=undefined&file=%s') % (match_key[0], match_file[0])
	  link_api = link_api = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
          match_url = re.compile('url=(.+?)&title').findall(link_api)
          if len(match_url) > 0:
              return match_url[0]
          else:
              return False


  def parserNOWVIDEO(self, url):
      query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)
      match_file = re.compile('flashvars.file="(.+?)";').findall(link)
      match_key = re.compile('flashvars.filekey="(.+?)";').findall(link)
      if len(match_file) > 0 and len(match_key) > 0:
          get_api_url = ('http://www.nowvideo.eu/api/player.api.php?codes=1&key=%s&user=undefined&pass=undefined&file=%s') % (match_key[0], match_file[0])
	  query_data = { 'url': get_api_url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
	  link_api = self.cm.getURLRequestData(query_data)
          match_url = re.compile('url=(.+?)&title').findall(link_api)
          if len(match_url) > 0:
              return match_url[0]
          else:
              return False


  def parserSOCKSHARE(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data) 
    r = re.search('value="(.+?)" name="fuck_you"', link)
    if r:
      self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
      self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "sockshare.cookie"
      postdata = {'fuck_you' : r.group(1), 'confirm' : 'Close Ad and Watch as Free User'}
      query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
      link = self.cm.getURLRequestData(query_data, postdata) 
      match = re.compile("playlist: '(.+?)'").findall(link)
      if len(match) > 0:
        url = "http://www.sockshare.com" + match[0]
        query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE, 'use_post': False, 'return_data': True }
        link = self.cm.getURLRequestData(query_data) 
        match = re.compile('</link><media:content url="(.+?)" type="video').findall(link)
        if len(match) > 0:
          url = match[0].replace('&amp;','&')
          return url
        else:
          return False
      else:
        return False
    else:
      return False


  def parserRAPIDVIDEO(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)
    match = re.search("""'(.+?)','720p'""",link)
    if match:    
      return match.group(1)
    else: 
      return False


  def parserVIDEOSLASHER(self, url):
    self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "videoslasher.cookie"
    query_data = { 'url': url.replace('embed', 'video'), 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
    postdata = {'confirm': 'Close Ad and Watch as Free User', 'foo': 'bar'}
    data = self.cm.getURLRequestData(query_data, postdata)
    
    match = re.compile("playlist: '/playlist/(.+?)'").findall(data)
    if len(match)>0:
      query_data = { 'url': 'http://www.videoslasher.com//playlist/' + match[0], 'use_host': False, 'use_cookie': True, 'save_cookie': False, 'load_cookie': True, 'cookiefile': self.COOKIEFILE,  'use_post': True, 'return_data': True }
      data = self.cm.getURLRequestData(query_data)
      match = re.compile('<title>Video</title><media:content url="(.+?)"').findall(data)
      if len(match)>0:
	sid = self.cm.getCookieItem(self.COOKIEFILE,'authsid')
	if sid != '':
	  streamUrl = match[0] + '|Cookie="authsid=' + sid + '"'
	  return streamUrl	
	else:
	  return False
      else:
	return False
    else:
      return False




          
