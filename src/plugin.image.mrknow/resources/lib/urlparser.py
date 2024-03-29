# -*- coding: utf-8 -*-
import cookielib, os, string, StringIO
import os, time, base64, logging, calendar
import urllib, urllib2, re, sys, math
import xbmcaddon, xbmc, xbmcgui, simplejson
import urlparse
import httplib 

scriptID = 'plugin.video.polishtv.live'
scriptname = "Polish Live TV"
ptv = xbmcaddon.Addon(scriptID)

import pLog, Parser, settings, pCommon,xppod
#import maxvideo, anyfiles

log = pLog.pLog()
sets = settings.TVSettings()


class urlparser:
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


  def getVideoLink(self, url,referer=''):
    nUrl=''
    host = self.getHostName(url)
    log.info("video hosted by: " + host)
    log.info('URL: '+url + ' ' +referer)
    
    if host == 'www.putlocker.com':
        nUrl = self.parserPUTLOCKER(url)
    if host == 'www.sockshare.com':
        nUrl = self.parserSOCKSHARE(url)
    if host == 'megustavid.com' or host == 'www.megustavid.com':
        nUrl = self.parserMEGUSTAVID(url)
    if host == 'hd3d.cc':
        nUrl = self.parserHD3D(url)
    if host == 'sprocked.com':
        nUrl = self.parserSPROCKED(url)
    if host == 'odsiebie.pl':
        nUrl = self.parserODSIEBIE(url) 
    if host == 'www.wgrane.pl':
        nUrl = self.parserWGRANE(url)
    if host == 'www.cda.pl':
        nUrl = self.parserCDA(url)
    if host == 'maxvideo.pl' or host == 'nextvideo.pl':
        nUrl = self.parserMAXVIDEO(url)
    if host == 'video.anyfiles.pl':
        nUrl = self.parserANYFILES(url)
    if host == 'www.videoweed.es' or host == 'www.videoweed.com' or host == 'videoweed.es' or host == 'videoweed.com':
        nUrl = self.parserVIDEOWEED(url)
    if host== 'www.novamov.com':
        nUrl = self.parserNOVAMOV(url)
    if host== 'www.nowvideo.eu':
        nUrl = self.parserNOWVIDEO(url)
    if host== 'www.rapidvideo.com':
        nUrl = self.parserRAPIDVIDEO(url)
    if host== 'www.videoslasher.com':
        nUrl = self.parserVIDEOSLASHER(url)	
    if host== 'www.youtube.com':
        nUrl = self.parserYOUTUBE(url)	
    if host== 'stream.streamo.tv':
        nUrl = self.parserSTREAMO(url)	
    if host== 'tosiewytnie.pl':
        nUrl = self.parsertosiewytnie(url)	
    if host== 'www.liveleak.com':
        nUrl = self.parserliveleak(url)	
    if host== 'vimeo.com':
        nUrl = self.parserVIMEO(url)	
    if host== 'yukons.net':
        nUrl = self.parserYUKONS(url)
    if host== 'www.reyhq.com':
        nUrl = self.parserREYHQ(url)      
    if host== 'www.sawlive.tv':
        nUrl = self.parserSAWLIVE(url,referer)  
    if host== 'www.ilive.to':
        nUrl = self.parserILIVE(url,referer)      
    if host== 'mips.tv':
        nUrl = self.parserMIPS(url,referer)      
    if host== 'www.ukcast.tv':
        nUrl = self.parserUKCAST(url,referer)              
    return nUrl
    
  def parserUKCAST(self,url,referer):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link22 = self.cm.getURLRequestData(query_data)
    match22=re.compile("SWFObject\('(.*?)','mpl','','','9'\);").findall(link22)
    match23=re.compile("so.addVariable\('file', '(.*?)'\);").findall(link22)
    match24=re.compile("so.addVariable\('streamer', '(.*?)'\);").findall(link22)
    videolink = match24[0] + ' playpath=' +match23[0] + ' swfUrl=' + match22[0] + ' pageUrl=http://www.ukcast.tv live=true swfVfy=true'
    print ("Link",videolink)
    return videolink

  def parserMIPS(self,url,referer):
    query = urlparse.urlparse(url)
    channel = query.path
    channel=channel.replace("/embed/","")
    params = query.path.split("/")
    print ("Query",query,params)
    return False
#    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
#    link21 = self.cm.getURLRequestData(query_data)
#    match21=re.compile("<iframe src='(.*?)'").findall(link21)
#    req = urllib2.Request(match21[0])
#    req.add_header('Referer', referer)
#    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#    response = urllib2.urlopen(req)
#    link22=response.read()
#    response.close()
     #file\': \'http://mobilestreaming.ilive.to:1935/edge/0vs62vldjnkjfrl/playplist.m3u8\',
#    match22=re.compile("'file': '(.*?)',").findall(link22)
    
    print ("AAAA",match22)
    print ("BBBB",link22)
    if len(match22[1]) > 0:
        videolink = match22[1]
        print ("videolink", match22[1])
        return match22[1]
    else:
        return False
    
  def parserILIVE(self,url,referer):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link21 = self.cm.getURLRequestData(query_data)
    match21=re.compile("<iframe src='(.*?)'").findall(link21)
    req = urllib2.Request(match21[0])
    req.add_header('Referer', referer)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link22=response.read()
    response.close()
    match22=re.compile("'file': '(.*?)',").findall(link22)
    if len(match22[1]) > 0:
        videolink = match22[1]
        return match22[1]
    else:
        return False

    
  def parserSAWLIVE(self,url,referer):
    def decode(tmpurl):
        host = self.getHostName(tmpurl)
        result = ''
        for i in host:
            result += hex(ord(i)).split('x')[1]
        return result
 
    query = urlparse.urlparse(url)
    channel = query.path
    channel=channel.replace("/embed/","")
    query_data = { 'url': 'http://www.sawlive.tv/embed/' + channel, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link21 = self.cm.getURLRequestData(query_data)
    match21=re.compile("var escapa = unescape\('(.*?)'\);").findall(link21)
    start= urllib.unquote(match21[0]).find('src="')
    end = len(urllib.unquote(match21[0]))
#    print("SAW:",link21,match21)
    url =  urllib.unquote(match21[0])[start+5:end] + '/' + decode(referer)
#        url =  urllib.unquote(match21[0])[start+5:end] +'/7777772e64726874762e636f6d2e706c'
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link22 = self.cm.getURLRequestData(query_data)
    match22=re.compile("SWFObject\('(.*?)','mpl','100%','100%','9'\);").findall(link22)
    match23=re.compile("so.addVariable\('file', '(.*?)'\);").findall(link22)
    match24=re.compile("so.addVariable\('streamer', '(.*?)'\);").findall(link22)
    print ("Match",match22,match23,match24,link22)
    videolink = match24[0] + ' playpath=' +match23[0] + ' swfUrl=' + match22[0] + ' pageUrl=http://sawlive.tv/embed/' +channel + ' live=true swfVfy=true'
    return videolink

  def parserREYHQ(self,url):
    query = urlparse.urlparse(url)
    channel = query.path
    channel=channel.replace("/","")
    videolink = 'rtmp://' + '89.248.172.239:1935/live' 
    videolink += ' pageUrl=http://www.reyhq.com live=true playpath='+channel
    videolink += ' swfVfy=http://www.reyhq.com/player/player-licensed.swf'
    print ("videolink", videolink)
    return videolink

  def parserYUKONS(self,url):
    query = urlparse.urlparse(url)
    channel = query.path
    channel=channel.replace("/","")
    query_data = { 'url': 'http://yukons.net/lb.php', 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link1 = self.cm.getURLRequestData(query_data)
    link1 = link1.replace("srv=", "");
    videolink = 'rtmp://' +link1 + '/kuyo/' + channel 
    videolink += ' pageUrl=http://yukons.net/watch/' + channel + ' live=true'
    videolink += ' swfVfy=http://yukons.net/yukplay.swf '
    print ("videolink", videolink)
    return videolink


  def parserVIMEO(self,url):
    query = urlparse.urlparse(url)
    p = urlparse.parse_qs(query.query)
    print p
    if len(p) > 0:
        link = "plugin://plugin.video.vimeo/?action=play_video&videoid=" + p['clip_id'][0]
    else:
        tmp = query.path.split("/")
        link = link = "plugin://plugin.video.vimeo/?action=play_video&videoid=" +tmp[1]
    return link

  def parserliveleak(self,url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('file: "(.+?)",').findall(link)
    print match
    for url in match:
      return url
          
        
  def check_url(self,url):
    def _head(url):
        (scheme, netloc, path, params, query, fragment) = urlparse.urlparse(url)
        #print ("URL:", scheme, netloc, path, params, query, fragment)
        connection = httplib.HTTPConnection(netloc)
        connection.request('HEAD',  path  +'?'+ query ) 
        return connection.getresponse()
    # redirection limit, default of 10
    redirect = 10
    # Perform HEAD
    resp = _head(url)

    while (resp.status >= 300) and (resp.status <= 399):
        # tick the redirect
        redirect -= 1
        # if redirect is 0, we tried :-(
        if redirect == 0:
            # we hit our redirection limit, raise exception
            return False
        # Perform HEAD
        url = resp.getheader('location')
        resp = _head(url)
    if resp.status >= 200 and resp.status <= 299:
        # horray!  We found what we were looking for.
        return True
    else:
        # Status unsure, might be, 404, 500, 401, 403, raise error with actual status code.
        return False

    
  def parsertosiewytnie(self,url):
    movlink = url
    movlink = movlink.replace('/m3', '/h')
    if (self.check_url(movlink)):
        return movlink
    else:
        movlink = movlink.replace('mp4', 'mov')
        return movlink
 
  def parserSTREAMO(self,url):
    return url

  def parserYOUTUBE(self,url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse.urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = urlparse.parse_qs(query.query)
            print p
            return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + p['v'][0]
        if query.path[:7] == '/embed/':
            print query
            print query.path.split('/')[2]
            return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return 'plugin://plugin.video.youtube/?action=play_video&videoid=' + query.path.split('/')[2]
    # fail?
    return None        

    
  def parserPUTLOCKER(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)    
    r = re.search('value="(.+?)" name="fuck_you"', link)
    if r:
      self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
      self.COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "putlocker.cookie"
      query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'save_cookie': True, 'load_cookie': False, 'cookiefile': self.COOKIEFILE, 'use_post': True, 'return_data': True }
      postdata = {'fuck_you' : r.group(1), 'confirm' : 'Close Ad and Watch as Free User'}
      link = self.cm.getURLRequestData(query_data, postdata)
      match = re.compile("playlist: '(.+?)'").findall(link)
      if len(match) > 0:
        url = "http://www.putlocker.com" + match[0]
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


  def parserMEGUSTAVID(self,url):
    query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
    link = self.cm.getURLRequestData(query_data)    
    match = re.compile('value="config=(.+?)">').findall(link)
    if len(match) > 0:
      p = match[0].split('=')
      url = "http://megustavid.com/media/nuevo/player/playlist.php?id=" + p[1]
      query_data = { 'url': url, 'use_host': False, 'use_cookie': False, 'use_post': False, 'return_data': True }
      link = self.cm.getURLRequestData(query_data)      
      match = re.compile('<file>(.+?)</file>').findall(link)
      if len(match) > 0:
        return match[0]
      else:
        return False
    else: 
      return False


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
    COOKIEFILE = ptv.getAddonInfo('path') + os.path.sep + "cookies" + os.path.sep + "anyfiles.cookie"
    self.cm.checkDir(ptv.getAddonInfo('path') + os.path.sep + "cookies")
    self.cm.addCookieItem(COOKIEFILE, {'name': 'AnyF18', 'value': 'mam18', 'domain': 'video.anyfiles.pl'}, False)
    query_data = { 'url': url, 'use_host': False, 'use_cookie': True, 'cookiefile': COOKIEFILE, 'load_cookie': True, 'save_cookie': True, 'use_post': False, 'return_data': True }
    data = self.cm.getURLRequestData(query_data)
    #var flashvars = {"uid":"player-vid-8552","m":"video","st":"c:1LdwWeVs3kVhWex2PysGP45Ld4abN7s0v4wV"};
    match = re.search("""var flashvars = {.+?"st":"(.+?)"}""",data)
    if match:
        nUrl = xppod.Decode(match.group(1)[2:]).encode('utf-8').strip()
        if 'http://' in nUrl: url2 = nUrl
        else: url2 = 'http://video.anyfiles.pl' + nUrl
                
        query_data = { 'url': url2+ "&ref=" +urllib.quote_plus(url), 'use_host': False, 'use_cookie': True, 'cookiefile': COOKIEFILE, 'load_cookie': True, 'save_cookie': False, 'use_post': False, 'return_data': True }
        data = self.cm.getURLRequestData(query_data)
        data = xppod.Decode(data).encode('utf-8').strip()

        #json cleanup
        while data[-2:] != '"}': data = data[:-1]
        result = simplejson.loads(data)
        if (result['ytube']=='0'):
            vUrl = result['file'].split("or")
            print ("Dasta",vUrl[0])
            vUrl = vUrl[0].encode('utf-8').split(' ')
            return vUrl[0]
        else:
            p = result['file'].split("/")
            if 'watch' in p[3]: videoid = p[3][8:19]
            else: videoid = p[3]
            plugin = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + videoid
            return plugin
            return False 

  
  
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




          
