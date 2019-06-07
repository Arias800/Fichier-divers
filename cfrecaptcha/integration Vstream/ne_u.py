#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import unwise
from resources.lib.util import cUtil
from resources.lib.comaddon import VSlog, xbmcgui, xbmc
import urllib, urllib2
import re
import base64
import requests, xbmcvfs, os, xbmcaddon

__addon__ = xbmcaddon.Addon('plugin.video.vstream')
__sLang__ = 'fr'

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
#UA = 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'

def GetIp():
    if (False):
        oRequest = cRequestHandler('http://hqq.tv/player/ip.php?type=json')
        oRequest.addHeaderEntry
        sHtmlContent = oRequest.request()
        ip = re.search('"ip":"([^"]+)"', sHtmlContent, re.DOTALL).group(1)
    else:
        import random
        for x in xrange(1,100):
            ip = "192.168."
            ip += ".".join(map(str, (random.randint(0, 255) for _ in range(2))))
        ip = base64.b64encode(ip)

    return ip

def _decode2(file_url):
    def K12K(a, typ='b'):
        codec_a = ["G", "L", "M", "N", "Z", "o", "I", "t", "V", "y", "x", "p", "R", "m", "z", "u",
                   "D", "7", "W", "v", "Q", "n", "e", "0", "b", "="]
        codec_b = ["2", "6", "i", "k", "8", "X", "J", "B", "a", "s", "d", "H", "w", "f", "T", "3",
                   "l", "c", "5", "Y", "g", "1", "4", "9", "U", "A"]
        if 'd' == typ:
            tmp = codec_a
            codec_a = codec_b
            codec_b = tmp
        idx = 0
        while idx < len(codec_a):
            a = a.replace(codec_a[idx], "___")
            a = a.replace(codec_b[idx], codec_a[idx])
            a = a.replace("___", codec_b[idx])
            idx += 1
        return a

    def _xc13(_arg1):
        _lg27 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        _local2 = ""
        _local3 = [0, 0, 0, 0]
        _local4 = [0, 0, 0]
        _local5 = 0
        while _local5 < len(_arg1):
            _local6 = 0
            while _local6 < 4 and (_local5 + _local6) < len(_arg1):
                _local3[_local6] = _lg27.find(_arg1[_local5 + _local6])
                _local6 += 1
            _local4[0] = ((_local3[0] << 2) + ((_local3[1] & 48) >> 4))
            _local4[1] = (((_local3[1] & 15) << 4) + ((_local3[2] & 60) >> 2))
            _local4[2] = (((_local3[2] & 3) << 6) + _local3[3])

            _local7 = 0
            while _local7 < len(_local4):
                if _local3[_local7 + 1] == 64:
                    break
                _local2 += chr(_local4[_local7])
                _local7 += 1
            _local5 += 4
        return _local2

    return _xc13(K12K(file_url, 'e'))

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Netu'
        self.__sFileName = self.__sDisplayName

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def setUrl(self, sUrl):
        self.__sUrl = sUrl.replace('https', 'http')
        self.__sUrl = self.__sUrl.replace('http://netu.tv/', 'http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://waaw.tv/', 'http://hqq.tv/')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/player/hash.php?hash=', 'http://hqq.tv/player/embed_player.php?vid=')
        self.__sUrl = self.__sUrl.replace('http://hqq.tv/watch_video.php?v=', 'http://hqq.tv/player/embed_player.php?vid=')

    def __getIdFromUrl(self):
        sPattern = 'https*:\/\/hqq\.(?:tv|player|watch)\/player\/embed_player\.php\?vid=([0-9A-Za-z]+)'
        oParser = cParser()
        aResult = oParser.parse(self.__sUrl, sPattern)

        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def getPluginIdentifier(self):
        return 'netu'

    def isDownloadable(self):
        return False

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def GetHost(self,sUrl):
        oParser = cParser()
        sPattern = 'https*:\/\/(.+?)\/'
        aResult = oParser.parse(sUrl, sPattern)
        if aResult[0]:
            return aResult[1][0]
        return ''

    def ResolveCaptcha(self):
        urlBase  = 'https://www.google.com/recaptcha/api/fallback?k=6LfCmh4TAAAAAKog9f8wTyEOc0U8Ms2RTuDFyYP_'
        oRequestHandler = cRequestHandler(urlBase)
        oRequestHandler.addHeaderEntry('User-Agent',UA)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        oRequestHandler.addHeaderEntry('Referer', self.__sUrl)
        body = oRequestHandler.request()

        #Recuperer le liens du payload
        captchaScrap = re.findall('value="8"><img class="fbc-imageselect-payload" src="(.+?)"',str(body))

        #Recuperer le texte du captcha
        text = re.search('<div class="rc-imageselect.+?">.+?<strong>(.+?)</strong>',str(body)).group(1)

        #Recuperer les 2 parametre necessaire pour acceder au captcha
        c = re.search('method="POST"><input type="hidden" name="c" value="(.+?)"',str(body)).group(1)
        k = re.search('k=(.+?)" alt=',str(body)).group(1)
        params = {
            "c": c,
            "k": k,
        }
        query_string = urllib.urlencode( params )

        #Requete pour le captcha
        url = 'https://www.google.com'+str(captchaScrap[0]) + "?" + query_string

        filePath = "special://home/userdata/addon_data/plugin.video.vstream/Captcha.raw"

        oRequestHandler = cRequestHandler(url)
        htmlcontent = oRequestHandler.request()

        downloaded_image = xbmcvfs.File(filePath, 'wb')
        downloaded_image.write(htmlcontent)
        downloaded_image.close()

        oSolver = cInputWindow(captcha = filePath, msg = text,roundnum=1)
        retArg = oSolver.get()
        VSlog('>>>>>>>> Captcha response [%s]' % (retArg))

        #Format la reponse
        allNumber = [int(s) for s in re.findall('([0-9])',str(retArg))]
        responseFinal = ""
        for rep in allNumber:
            responseFinal = responseFinal + '&response='+str(rep)
        VSlog(responseFinal)

        headers = {
            'Host': 'www.google.com',
            'User-Agent': UA,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': url,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length':str(len(params)),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
            }

        #Requete pour valider le captcha
        r = requests.post(urlBase, data='c='+c+responseFinal, headers=headers)

        #Recupere le token du captcha
        return re.search('<textarea dir="ltr" readonly>(.+?)<',str(r.text)).group(1)

    def __getMediaLinkForGuest(self):

        api_call = ''

        id = self.__getIdFromUrl()

        self.__sUrl = 'http://hqq.tv/player/embed_player.php?vid=' + id + '&autoplay=no'

        headers = {'User-Agent': UA ,
                   #'Host': 'hqq.tv',
                   'Referer': 'http://hqq.tv/',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   #'Accept-Encoding': 'gzip, deflate, br',
                   #'Content-Type': 'text/html; charset=utf-8'
                   }

        player_url = self.__sUrl

        req = urllib2.Request(player_url, None, headers)
        try:
            response = urllib2.urlopen(req)
            html = response.read()
            response.close()
        except urllib2.URLError, e:
            VSlog(e.read())
            VSlog(e.reason)
            html = e.read()

        Host = 'https://' + self.GetHost(player_url) + '/'

        data = ''
        data = DecodeAllThePage(html)

        #data = ''
        #code_crypt = re.search('(;eval\(function\(w,i,s,e\){.+?\)\);)\s*<', html, re.DOTALL)
        #if code_crypt:
        #    data = unwise.unwise_process(code_crypt.group(1))
        #else:
        #    VSlog('prb1')

        if data:
            http_referer = ''
            _pass = ''

            iss = GetIp()
            vid = re.search("videokeyorig=\'(.+?)\'", data, re.DOTALL).group(1)
            at = re.search("attoken=\'(.+?)\'", data, re.DOTALL).group(1)
            r = re.search('var referer = "([^"]+)"', data, re.DOTALL)
            if r:
                http_referer = r.group(1)

            import string, random
            _BOUNDARY_CHARS = string.digits
            boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(17))

            gToken = self.ResolveCaptcha()
            VSlog(gToken)

            url2 = "https://hqq.tv/sec/player/embed_player_"+boundary+".php?iss="+iss+"=&vid="+vid+"&at="+at+"&autoplayed=yes&referer=on&http_referer="+http_referer+"&pass=&embed_from=&need_captcha=0&secure=0&g-recaptcha-response="+gToken
            VSlog(url2)

            req = urllib2.Request(url2, None, headers)

            try:
                response = urllib2.urlopen(req)
                data = response.read()
                VSlog(data)
                response.close()
            except urllib2.URLError, e:
                VSlog(e.read())
                VSlog(e.reason)
                data = e.read()

            data = urllib.unquote(data)

            data = DecodeAllThePage(data)

            at = re.search(r'var\s*at\s*=\s*"([^"]*?)"', data)

            l = re.search(r'\.get\( *"/player/get_md5.php",.+?link_1: *(.+?), *server_2: *(.+?), *vid: *"([^"]+)"}\)', data)
            if l:
               vid_server = re.search(r'var ' + l.group(2) + ' = "([^"]+)"', data).group(1)

               vid_link = re.search(r'var ' + l.group(1) + ' = "([^"]+)"', data).group(1)

               vid_key = l.group(3)
            else:
                VSlog("prob 3")

            #new video id, not really usefull
            # m = re.search(r' vid: "([a-zA-Z0-9]+)"}', data)
            # if m:
                # id = m.group(1)

            if vid_server and vid_link and at and vid_key:

                #get_data = {'server': vid_server.group(1), 'link': vid_link.group(1), 'at': at.group(1), 'adb': '0/','b':'1','vid':id} #,'iss':'MzEuMz'
                get_data = {'server_2': vid_server, 'link_1': vid_link, 'at': at.group(1), 'adb': '0/','b':'1','vid':vid_key}

                headers['x-requested-with'] = 'XMLHttpRequest'

                req = urllib2.Request(Host + "/player/get_md5.php?" + urllib.urlencode(get_data), None, headers)
                try:
                    response = urllib2.urlopen(req)
                except urllib2.URLError, e:
                    VSlog(str(e.read()))
                    VSlog(str(e.reason))

                data = response.read()
                #VSlog(data)
                response.close()

                file_url = re.search(r'"obf_link"\s*:\s*"([^"]*?)"', data)

                if file_url:
                    list_url = decodeUN(file_url.group(1).replace('\\', ''))

                #Hack, je sais pas si ca va durer longtemps, mais indispensable sur certains fichiers
                #list_url = list_url.replace("?socket", ".mp4.m3u8")

            else:
                VSlog('prb2')
        #bricolage
        api_call = list_url + '.mp4.m3u8'


        #use a fake headers
        #Header = 'User-Agent=' + UA
        api_call = api_call #+ '|' + Header >> pas besoin pour l'instant

        if not (api_call == False):
            return True, api_call

        return False, False

#*******************************************************************************
def decodeUN(a):
    a = a[1:]
    s2 = ""

    i = 0
    while i < len(a):
      s2 += ('\u0' + a[i:i+3])
      i = i + 3

    s3 = s2.decode('unicode-escape')
    if not s3.startswith('http'):
        s3 = 'http:' + s3

    return s3

def DecodeAllThePage(html):

    #html = urllib.unquote(html)

    Maxloop = 10

    #unescape
    while (Maxloop > 0):
        Maxloop = Maxloop - 1

        r = re.search(r'unescape\("([^"]+)"\)', html, re.DOTALL | re.UNICODE)
        if not r:
            break

        tmp = cUtil().unescape(r.group(1))
        html = html[:r.start()] + tmp + html[r.end():]

    #unwise
    while (Maxloop > 0):
        Maxloop = Maxloop - 1

        r = re.search(r'(;eval\(function\(w,i,s,e\){.+?\)\);)\s*<', html, re.DOTALL | re.UNICODE)
        if not r:
            break

        tmp = data = unwise.unwise_process(r.group(1))
        html = html[:r.start()] + tmp + html[r.end():]

    return html

class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):

        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,200,624,400,"")
        xbmc.sleep(500)
        self.img = xbmcgui.ControlImage(335,200,624,400,self.cptloc)
        xbmc.sleep(500)

        bg_image =  os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + "background.png"
        check_image =  os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + "trans_checked.png"
        uncheck_image =  os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + "trans_unchecked1.png"

        self.ctrlBackgound = xbmcgui.ControlImage(
            0,0,
            1280, 720,
            bg_image
        )
        self.cancelled=False
        self.addControl (self.ctrlBackgound)
        self.msg = kwargs.get('msg')+'\nNormalement il devrai y avoir en 3 ou 4 selection'
        self.roundnum=kwargs.get('roundnum')
        self.strActionInfo = xbmcgui.ControlLabel(335, 120, 700, 300, "Le theme est : " + self.msg, 'font13', '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.strActionInfo = xbmcgui.ControlLabel(335, 20, 724, 400, 'Captcha round %s'%(str(self.roundnum)), 'font40', '0xFFFF00FF')
        self.addControl(self.strActionInfo)

        self.addControl(self.img)

        self.chk=[0]*9
        self.chkbutton=[0]*9
        self.chkstate=[False]*9

        if 1==2:
            self.chk[0]= xbmcgui.ControlCheckMark(335, 190, 220, 150, '1', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[1]= xbmcgui.ControlCheckMark(335+200, 190, 220, 150, '2', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[2]= xbmcgui.ControlCheckMark(335+400, 190, 220, 150, '3', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)

            self.chk[3]= xbmcgui.ControlCheckMark(335, 190+130, 220, 150, '4', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[4]= xbmcgui.ControlCheckMark(335+200, 190+130, 220, 150, '5', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[5]= xbmcgui.ControlCheckMark(335+400, 190+130, 220, 150, '6', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)

            self.chk[6]= xbmcgui.ControlCheckMark(335, 190+260, 220, 150, '7', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[7]= xbmcgui.ControlCheckMark(335+200, 190+260, 220, 150, '8', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
            self.chk[8]= xbmcgui.ControlCheckMark(335+400, 190+260, 220, 150, '9', font='font14',focusTexture=check_image ,noFocusTexture=uncheck_image,checkWidth=220,checkHeight=150)
        else:

            self.chk[0]= xbmcgui.ControlImage(335, 190, 220, 150,check_image)
            self.chk[1]= xbmcgui.ControlImage(335+200, 190, 220, 150,check_image)
            self.chk[2]= xbmcgui.ControlImage(335+400, 190, 220, 150,check_image)

            self.chk[3]= xbmcgui.ControlImage(335, 190+130, 220, 150,check_image)
            self.chk[4]= xbmcgui.ControlImage(335+200, 190+130, 220, 150,check_image)
            self.chk[5]= xbmcgui.ControlImage(335+400, 190+130, 220, 150,check_image)

            self.chk[6]= xbmcgui.ControlImage(335, 190+260, 220, 150,check_image)
            self.chk[7]= xbmcgui.ControlImage(335+200, 190+260, 220, 150,check_image)
            self.chk[8]= xbmcgui.ControlImage(335+400, 190+260, 220, 150,check_image)

            self.chkbutton[0]= xbmcgui.ControlButton(335, 190, 210, 150, '1', font='font1');
            self.chkbutton[1]= xbmcgui.ControlButton(335+200, 190, 220, 150, '2', font='font1');
            self.chkbutton[2]= xbmcgui.ControlButton(335+400, 190, 220, 150, '3', font='font1');

            self.chkbutton[3]= xbmcgui.ControlButton(335, 190+130, 210, 150, '4', font='font1');
            self.chkbutton[4]= xbmcgui.ControlButton(335+200, 190+130, 220, 150, '5', font='font1');
            self.chkbutton[5]= xbmcgui.ControlButton(335+400, 190+130, 220, 150, '6', font='font1');

            self.chkbutton[6]= xbmcgui.ControlButton(335, 190+260, 210, 150, '7', font='font1');
            self.chkbutton[7]= xbmcgui.ControlButton(335+200, 190+260, 220, 150, '8', font='font1');
            self.chkbutton[8]= xbmcgui.ControlButton(335+400, 190+260, 220, 150, '9', font='font1');

        for obj in self.chk:
            self.addControl(obj )
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj )

        self.cancelbutton = xbmcgui.ControlButton(335+312-100,610,100,40,'Cancel',alignment=2)
        self.okbutton = xbmcgui.ControlButton(335+312+50,610,100,40,'OK',alignment=2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        self.chkbutton[6].controlDown(self.cancelbutton);  self.chkbutton[6].controlUp(self.chkbutton[3])
        self.chkbutton[7].controlDown(self.cancelbutton);  self.chkbutton[7].controlUp(self.chkbutton[4])
        self.chkbutton[8].controlDown(self.okbutton);      self.chkbutton[8].controlUp(self.chkbutton[5])

        self.chkbutton[6].controlLeft(self.chkbutton[8]);self.chkbutton[6].controlRight(self.chkbutton[7]);
        self.chkbutton[7].controlLeft(self.chkbutton[6]);self.chkbutton[7].controlRight(self.chkbutton[8]);
        self.chkbutton[8].controlLeft(self.chkbutton[7]);self.chkbutton[8].controlRight(self.chkbutton[6]);

        self.chkbutton[3].controlDown(self.chkbutton[6]);  self.chkbutton[3].controlUp(self.chkbutton[0])
        self.chkbutton[4].controlDown(self.chkbutton[7]);  self.chkbutton[4].controlUp(self.chkbutton[1])
        self.chkbutton[5].controlDown(self.chkbutton[8]);  self.chkbutton[5].controlUp(self.chkbutton[2])

        self.chkbutton[3].controlLeft(self.chkbutton[5]);self.chkbutton[3].controlRight(self.chkbutton[4]);
        self.chkbutton[4].controlLeft(self.chkbutton[3]);self.chkbutton[4].controlRight(self.chkbutton[5]);
        self.chkbutton[5].controlLeft(self.chkbutton[4]);self.chkbutton[5].controlRight(self.chkbutton[3]);

        self.chkbutton[0].controlDown(self.chkbutton[3]);  self.chkbutton[0].controlUp(self.cancelbutton)
        self.chkbutton[1].controlDown(self.chkbutton[4]);  self.chkbutton[1].controlUp(self.cancelbutton)
        self.chkbutton[2].controlDown(self.chkbutton[5]);  self.chkbutton[2].controlUp(self.okbutton)

        self.chkbutton[0].controlLeft(self.chkbutton[2]);self.chkbutton[0].controlRight(self.chkbutton[1]);
        self.chkbutton[1].controlLeft(self.chkbutton[0]);self.chkbutton[1].controlRight(self.chkbutton[2]);
        self.chkbutton[2].controlLeft(self.chkbutton[1]);self.chkbutton[2].controlRight(self.chkbutton[0]);

        self.cancelled=False
        self.setFocus(self.okbutton)
        self.okbutton.controlLeft(self.cancelbutton);self.okbutton.controlRight(self.cancelbutton);
        self.cancelbutton.controlLeft(self.okbutton); self.cancelbutton.controlRight(self.okbutton);
        self.okbutton.controlDown(self.chkbutton[2]);self.okbutton.controlUp(self.chkbutton[8]);
        self.cancelbutton.controlDown(self.chkbutton[0]); self.cancelbutton.controlUp(self.chkbutton[6]);

    def get(self):
        self.doModal()
        self.close()
        if not self.cancelled:
            retval=""
            for objn in range(9):
                if self.chkstate[objn]:
                    retval+=("" if retval=="" else ",")+str(objn)
            return  retval

        else:
            return ""

    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:
                return True
        return False

    def onControl(self,control):
        if   control==self.okbutton:
            if self.anythingChecked():
                self.close()
        elif control== self.cancelbutton:
            self.cancelled=True
            self.close()
        try:
            if 'xbmcgui.ControlButton' in repr(type(control)):
                index=control.getLabel()
                if index.isnumeric():
                    self.chkstate[int(index)-1]= not self.chkstate[int(index)-1]
                    self.chk[int(index)-1].setVisible(self.chkstate[int(index)-1])

        except: pass

    def onAction(self, action):
        if action == 10:
            self.cancelled=True
            self.close()
