#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#test film strem vk 1er page dark higlands & tous ces enfants m'appartiennent
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib.tinyjsparser import JsParser
import re, requests
import urllib.request
import gzip
import json

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

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
        self.__sUrl = sUrl

    def __getIdFromUrl(self):
        sPattern = 'https*:\/\/waaw\.(?:tv|player|watch)\/player\/embed_player\.php\?vid=([0-9A-Za-z]+)'
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

    def __getMediaLinkForGuest(self):
        api_call = ''

        headers = { 
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate",
            "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://www.4kstreamz.net/",
            "sec-ch-ua": 'Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "iframe",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": UA,
        }

        req = urllib.request.Request(self.__sUrl, None, headers)
        with urllib.request.urlopen(req) as response:
           html = gzip.decompress(response.read()).decode('unicode-escape')

        JScode = re.search(' = null;\s*}(.+?)var',html, re.MULTILINE|re.DOTALL).group(1).encode('latin1').decode('utf-8')
        JP = JsParser()
        data = JP.ProcessJS(JScode).encode('latin1').decode('unicode-escape')

        sh = re.search("shh*= *\'(.+?)\';", data).group(1)
        adb = re.search("adbn = \'(.+?)\'", html).group(1)

        data = {"videokey":self.__getIdFromUrl(),"width":693,"height":480}
        headers["accept"] = "application/json, text/javascript, */*; q=0.01"
        headers['Content-Type'] = 'application/json'
        headers['Content-Length'] = len(str(data))

        req = urllib.request.Request('https://waaw.tv/player/get_player_image.php', json.dumps(data).encode('utf-8'), headers)
        with urllib.request.urlopen(req) as response:
           html = json.loads(gzip.decompress(response.read()).decode('unicode-escape'))

        data = {'adb': adb, 'adscore': '', 'click_hash': html['hash_image'], 'clickx': 321, 'clicky': 174, 'embed_from': '0', 'gt': '', 'htoken': '', 'secure': '0', 'sh': sh, 'token': '', 'v': self.__getIdFromUrl(), 'ver': '4', 'wasmcheck': 1}

        headers = {'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-length': len(str(data)),
            'content-type': 'application/json',
            'origin': 'https://waaw.tv',
            'pragma': 'no-cache',
            'referer': self.__sUrl,
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': UA,
            'x-requested-with': 'XMLHttpRequest'}

        req = urllib.request.Request('https://waaw.tv/player/get_md5.php', json.dumps(data).encode('utf-8'), headers)
        with urllib.request.urlopen(req) as response:
           html = gzip.decompress(response.read())
           VSlog(html)

        if (api_call):
            return True, api_call + '.mp4.m3u8' + '|User-Agent=' + UA

        return False, False
