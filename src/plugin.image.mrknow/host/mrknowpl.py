# -*- coding: utf-8 -*-

#from resources.lib.gui.gui import cGui
from urlparse import urlparse, parse_qs


import urllib, urllib2, re, os, sys, math, time
import xbmcgui, xbmc, xbmcaddon, xbmcplugin
from urlparse import urlparse, parse_qs
import urlresolver
import cookielib
from cookielib import CookieJar


scriptID = 'plugin.video.mrknow'
scriptname = "Filmy online www.mrknow.pl - iptak"
ptv = xbmcaddon.Addon(scriptID)

BASE_RESOURCE_PATH = os.path.join( ptv.getAddonInfo('path'), "../resources" )
sys.path.append( os.path.join( BASE_RESOURCE_PATH, "lib" ) )

import pLog, settings, Parser

log = pLog.pLog()
HOST = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
mainUrl = 'http://www.mrknow.pl/'
cj = cookielib.CookieJar()

class MyHTTPErrorProcessor(urllib2.HTTPErrorProcessor):

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        if not (200 <= code < 300):
            response = self.parent.error(
                'http', request, response, code, msg, hdrs)
        return response

    https_response = http_response


MENU_TAB = {1: "Filmy HD",
            2: "Ostatnio Dodane",
            3: "Kategorie", 
            4: "Rok produkcji",
            5: "Aktorzy",
            6: "Dobre",
            7: "Szukaj"}

            
class mrknowpl:
    def __init__(self):
        log.info('Starting Mrknow.PL')
        self.settings = settings.TVSettings()
        self.parser = Parser.Parser()
        
    def listsMainMenu(self, table):
        for num, val in table.items():
            self.add('mrknowpl', 'main-menu', val, 'None', 'None', 'None', 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def CATYEAR(self):
        req = urllib2.Request(mainUrl)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        #match = re.compile('<h3> <a href="(.*?)" >(.*?)</a> </h3>(.*?)<a class="video_thumb" href="(.*?)" rel="bookmark" title="">(.*?)<img src="(.*?)" alt="" title=""  />(.*?)</a>', re.DOTALL).findall(readURL)
        match = re.compile("<a href='http://www.mrknow.pl/prodyear/([0-9]+)/' class='tag-link-(.+?)' title='(.+?)' style='font-size: (.+?)'>(.+?)</a>", re.DOTALL).findall(readURL)
        #self.add('mrknowpl', 'categories-menu', 'Filmy HD','None',"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg", "http://www.mrknow.pl/videostags/hd/", 'None', 'None', True, False)
        print match
        if len(match) > 0:
            for i in range(len(match)):
                self.add('mrknowpl', 'categories-menu', match[i][0],'None','None', mainUrl+ 'prodyear/' + match[i][0], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def CATACTORS(self):
        req = urllib2.Request(mainUrl+'/aktorzy')
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        #match = re.compile('<h3> <a href="(.*?)" >(.*?)</a> </h3>(.*?)<a class="video_thumb" href="(.*?)" rel="bookmark" title="">(.*?)<img src="(.*?)" alt="" title=""  />(.*?)</a>', re.DOTALL).findall(readURL)
        match = re.compile("<a href='(.+?)' class='tag-link-(.+?)' title='(.+?)' style='font-size: (.+?)'>(.+?)</a>", re.DOTALL).findall(readURL)
        #self.add('mrknowpl', 'categories-menu', 'Filmy HD','None',"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg", "http://www.mrknow.pl/videostags/hd/", 'None', 'None', True, False)
        print match
        if len(match) > 0:
            for i in range(len(match)):
                self.add('mrknowpl', 'categories-menu', match[i][4],'None','None', match[i][0], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

        
    def CATEGORIES(self):
        req = urllib2.Request(mainUrl)
        req.add_header('User-Agent', HOST)
        openURL = urllib2.urlopen(req)
        readURL = openURL.read()
        openURL.close()
        #match = re.compile('<h3> <a href="(.*?)" >(.*?)</a> </h3>(.*?)<a class="video_thumb" href="(.*?)" rel="bookmark" title="">(.*?)<img src="(.*?)" alt="" title=""  />(.*?)</a>', re.DOTALL).findall(readURL)
        match = re.compile('class="menu-item menu-item-type-taxonomy menu-item-object-videoscategory menu-item-(.+?)"><a href="(.*?)">(.*?)</a></li>', re.DOTALL).findall(readURL)
        #self.add('mrknowpl', 'categories-menu', 'Filmy HD','None',"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg", "http://www.mrknow.pl/videostags/hd/", 'None', 'None', True, False)
        print match
        if len(match) > 0:
            for i in range(len(match)):
                self.add('mrknowpl', 'categories-menu', match[i][2],'None','None', match[i][1], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def searchInputText(self):
        text = None
        k = xbmc.Keyboard()
        k.doModal()
        if (k.isConfirmed()):
            text = k.getText()
        return text

    def listsItemss(self,url):
        log.info('URL: '+ url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link=response.read()
        #log.info('LINK: '+ link)
        response.close()
        #match=re.compile('<a class="widget-title" href="(.*?)"><img src="(.*?)" alt="(.*?)" title="(.*?)"  /> </a>').findall(link)
        match=re.compile('<img src="(.+?)"  />	</a>	<h3><a href="(.+?)/">(.+?)</a></h3>').findall(link)
        #print match
        if len(match) > 0:
            for i in range(len(match)):
                self.add('mrknowpl','playSelectedMovie', 'None', match[i][2], match[i][0], match[i][1], 'None', 'None', True, False) 
            match1=re.compile('<a href="(.*?)" ><strong>next</strong></a>').findall(link)
            print match1
            if len(match1) > 0:
                self.add('mrknowpl', 'szukaj', 'Nast�pna strona','None',"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg", match1[0], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def movieinfo(self,txt):
        log.info('URL: '+ txt)
        req = urllib2.Request(txt)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link=response.read()
        #log.info('LINK: '+ link)
        response.close()
        #match=re.compile(' <a class="video_thumb" href="(.+?)" rel="bookmark" title="(.+?)">(.\s+)<img src="(.+?)" alt="(.+?)" title="(.+?)"  /> ').findall(link)
        match=re.compile('<p>(.*)</p>\n<div class="sharedaddy sd-sharing-enabled"').findall(link)
        match1=re.compile('<p><center>\n\n(.*)<img src="(.*)"  /></center>').findall(link)
        
        print "match"
        print match
        print "match1"
        print match1
        print "match -- "
        
        
    def unescape(self,s):
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        # this has to be last:
        s = s.replace("&amp;", "&")
        return s 
            
    def listsItems(self,url):
        log.info('URL: '+ url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', HOST)
        response = urllib2.urlopen(req)
        link=response.read()
        #log.info('LINK: '+ link)
        response.close()
        #match=re.compile(' <a class="video_thumb" href="(.+?)" rel="bookmark" title="(.+?)">(.\s+)<img src="(.+?)" alt="(.+?)" title="(.+?)"  /> ').findall(link)
        match=re.compile('<img src="(.+?)"  />	</a>	<h3><a href="(.+?)/">(.+?)</a></h3>').findall(link)
        print match
        #add(  service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True):
        if len(match) > 0:
            for i in range(len(match)):
                #self.movieinfo(match[i][1])
                link_txt1 = self.unescape(match[i][0])
                link_txt2 = link_txt1.replace("w=120", "w=400");
                link_txt3 = link_txt2.replace("h=160", "w=550");
                self.add('mrknowpl','playSelectedMovie', 'None', urllib.unquote_plus(match[i][2]), link_txt3, urllib.unquote_plus(match[i][1]), 'None', 'None', True, False) 
            match1=re.compile('<a href="(.+?)" class="nextpostslink">').findall(link)
            if len(match1) > 0:
                print match1
                self.add('mrknowpl', 'categories-menu', 'Natepna strona','None',"http://a3.sphotos.ak.fbcdn.net/hphotos-ak-prn1/527643_381614815229671_28469409_n.jpg", match1[0], 'None', 'None', True, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def getMovieLinkFromXML(self,url):
            req = urllib2.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            match=re.compile('<IFRAME SRC="(.+?)" SCROLLING=no></IFRAME>').findall(link)
            print 'MATCH'
            print match
            o = parse_qs(urlparse('http;//www.mrknow.pl/'+match[0]).query)
            stream_url = [''] * 2

            if o['t'][0] == 'p':
                 txthost = 'putlocker.com'
            elif o['t'][0] == 'v':
                txthost = 'videoslasher.com'
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), MyHTTPErrorProcessor)
                opener.addheaders = [('User-agent', HOST)]
                urllib2.install_opener(opener)
                page = urllib2.urlopen('http://www.videoslasher.com/video/' + o['page'][0])
                #page = urllib2.urlopen(url)
                link =  page.read()
                match1=re.compile('user: (.+?),').findall(link)
                match2=re.compile('code: \'(.+?)\',').findall(link)
                match3=re.compile('hash: \'(.+?)\'').findall(link)
                match4=re.compile('playlist: \'/playlist/(.+?)\'').findall(link)  
#                print match1[0]
#                print match2[0]
##                print match3[0]
                print match4[0]
                formdata = { "user" : match1[0], "code": match2[0], "hash" : match3[0] }
                data_encoded = urllib.urlencode(formdata)
                request = urllib2.Request('http://www.videoslasher.com/service/player/on-start', data_encoded) # lub urllib2.Request(url, data=data)
                response = urllib2.urlopen(request)
                link = response.read()
                page.close()
                page = urllib2.urlopen('http://www.videoslasher.com//playlist/' + match4[0])
                link2 =  page.read()
                page.close()
                match5=re.compile('url="(.+?)"').findall(link2)  
                cookies = []
                for cookie in cj:
                    cookies.append( "%s=%s" % (cookie.name, cookie.value) )
                ckStr = ';'.join(cookies)
                stream_url[0] = ( '%s|Cookie="%s"' % (match5[1],ckStr) )
                log.info(stream_url)

                 
            elif o['t'][0] == 'y':
                 txthost = 'youtube.com'

            if o['t'][0] == 'p' or o['t'][0] == 'y' :
                 sources = []
                 hosted_media = urlresolver.HostedMediaFile(host=txthost, media_id=o['page'][0])
                 sources.append(hosted_media)
                 source = urlresolver.choose_source(sources)
                 if source:
                      stream_url[0] = source.resolve()
                 else:
                      return

            elif o['t'][0] == 'a':  
                req = urllib2.Request('http://video.anyfiles.pl///video/'+o['page'][0])
                req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<source type="video/mp4" src="(.+?)">').findall(link)
                stream_url[0] = match[0]

            elif o['t'][0] == 'n':
                wybierz = ['Serwer 1 - zalecany','Serwer 2', 'Serwer 3', 'Serwer 4']
                d = xbmcgui.Dialog()
                item = d.select("Wybierz serwer", wybierz)
                if item == 0:
                    stream_url[0] = 'http://96.47.226.90/index.php?file=' + o['page'][0]+ '&start=0&hd=0&auth=0&type=flv&tv=0'
                    #http://178.159.0.84/index.php?file=1387&start=0&hd=0&auth=0&type=flv
                elif item == 1:
                    stream_url[0] = 'http://31.7.59.242/index.php?file=' + o['page'][0] + '&start=0&hd=0&auth=0&type=flv&tv=0'
                elif item == 2:
                    stream_url[0] = 'http://108.61.83.186/index.php?file=' + o['page'][0] + '&start=0&hd=0&auth=0&type=flv&tv=0'
                elif item == 3:
                    stream_url[0] = 'http://213.163.64.203/index.php?file=' + o['page'][0] + '&start=0&hd=0&auth=0&type=flv&tv=0'
                    #http://96.44.147.140/index.php?file=1387&start=0&hd=0&auth=0&type=flv
                
                #http://37.128.191.200/views.php?f=1387&_=1351550963808
                urlhelo = 'http://72.8.190.49/views.php?f='+o['page'][0]+'&_='+ str(int(time.time()*1000))
                log.info(urlhelo)
                req = urllib2.Request(urlhelo)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                
                if o.has_key('sub'):
                    stream_url[1] = o['sub'][0]
            return stream_url

    def playVideo(self,url,title, icon):
        movielink = self.getMovieLinkFromXML(url)
        liz=xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
        liz.setInfo( type="Video", infoLabels={ "Title": title, } )
        xbmcPlayer = xbmc.Player()
        log.info(movielink)
        if len(movielink[1])>0:
            subsdir = os.path.join(ptv.getAddonInfo('path'), "subs")
            if not os.path.isdir(subsdir):
                os.mkdir(subsdir)
            srtfile = urllib2.urlopen(movielink[1])
            output = open((os.path.join(subsdir, "napisy.txt" )),"w+")
            output.write(srtfile.read())
            output.close()
            time.sleep(1)
            xbmc.Player().setSubtitles((os.path.join(subsdir, "napisy.txt" )))
            xbmc.Player().showSubtitles(True)

            
            xbmcPlayer.play(movielink[0], liz)
            time.sleep(10)
            xbmc.Player().setSubtitles((os.path.join(subsdir, "napisy.txt" )))
            xbmc.Player().showSubtitles(True)
            if not xbmc.Player().isPlaying():
                xbmc.sleep( 10 )
                xbmc.Player().setSubtitles((os.path.join(subsdir, "napisy.txt" )))
                xbmc.Player().showSubtitles(True)
            return True
            
        else:
            xbmcPlayer.play(movielink[0], liz)
           # print 'xbmc.isPlaying() %s' % xbmc.isPlaying()
            return True
    
    def add(self, service, name, category, title, iconimage, url, desc, rating, folder = True, isPlayable = True):
        u=sys.argv[0] + "?service=" + service + "&name=" + name + "&category=" + category + "&title=" + title + "&url=" + urllib.quote_plus(url) + "&icon=" + urllib.quote_plus(iconimage)
        if name == 'main-menu' or name == 'categories-menu':
            title = category 
        if iconimage == '':
            iconimage = "DefaultVideo.png"
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        if isPlayable:
            liz.setProperty("IsPlayable", "true")
        liz.setInfo( type="Video", infoLabels={ "Title": title } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)        

    def getSearchURL(self, key):
        url = mainUrl + '/?s=' + urllib.quote_plus(key) 
        return url

        
    def handleService(self):
    	params = self.parser.getParams()
        name = self.parser.getParam(params, "name")
        category = self.parser.getParam(params, "category")
        url = self.parser.getParam(params, "url")
        title = self.parser.getParam(params, "title")
        icon = self.parser.getParam(params, "icon")
        sub = self.parser.getParam(params, "sub")
        
        if name == None:
            self.listsMainMenu(MENU_TAB)
        elif name == 'main-menu' and category == 'Kategorie':
            log.info('Jest Kategoria: ' + str(url))
            self.CATEGORIES()
        elif name == 'main-menu' and category == 'Rok produkcji':
            log.info('Jest Year: ' + str(url))
            self.CATYEAR()
        elif name == 'main-menu' and category == 'Aktorzy':
            log.info('Jest Year: ' + str(url))
            self.CATACTORS()
            
        elif name == 'main-menu' and category == 'Ostatnio Dodane':
            log.info('Jest Ostatnio Dodane: ')
            self.listsItems(mainUrl+ '/filmy')
        elif name == 'main-menu' and category == 'Filmy HD':
            log.info('Jest HD: ')
            self.listsItems(mainUrl + 'videostags/hd/')
        elif name == 'main-menu' and category == 'Dobre':
            log.info('Jest Dobre: ')
            self.listsItems(mainUrl + 'filmy/?sortby=voting&sortdir=desc')
        
#http://www.mrknow.pl/filmy/?sortby=voting&sortdir=desc
        
        
        elif name == 'main-menu' and category == "Szukaj":
            log.info('Jest Szukaj: ')
            key = self.searchInputText()
            log.info(self.getSearchURL(key))
            self.listsItemss(self.getSearchURL(key))
        elif name == 'szukaj':
            log.info('Jest Szukaj next: ')
            self.listsItemss(url)
            
            
        elif name == 'categories-menu' and category != 'None':
            log.info('url: ' + str(url))
            self.listsItems(url)
        if name == 'playSelectedMovie':
            log.info('URL: '+url)
            self.playVideo(url, title, icon)
            
