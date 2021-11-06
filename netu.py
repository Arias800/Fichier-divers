#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#test film strem vk 1er page dark higlands & tous ces enfants m'appartiennent
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib.tinyjsparser import JsParser
from collections import OrderedDict
import re, requests
import urllib.request
import gzip
import json
import ast

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
        self.__sUrl = sUrl.replace('/f/','/e/')

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

        oRequestHandler = cRequestHandler(self.__sUrl )
        oRequestHandler.addHeaderEntry('Host', "waaw.to")
        oRequestHandler.addHeaderEntry('Referer', self.__sUrl)
        oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Content-Type', "application/x-www-form-urlencoded")
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        oRequestHandler.addParametersLine("http_referer=https://wvv.33seriestreaming.com/")
        html = oRequestHandler.request()

        JScode = re.search(' = null;\s*}(.+?)var',html, re.MULTILINE|re.DOTALL).group(1)
        JP = JsParser()
        data = JP.ProcessJS(JScode)
        data = ast.literal_eval("b'{}'".format(data)).decode('unicode_escape')

        sh = re.search("shh*= *\'(.+?)\';", data).group(1)
        adb = re.search("adbn = \'(.+?)\'", html).group(1)

        oRequestHandler = cRequestHandler('https://waaw.to/player/get_player_image.php')
        oRequestHandler.setRequestType(1)
        oRequestHandler.addHeaderEntry('Host', "waaw.to")
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        oRequestHandler.addHeaderEntry('Referer', self.__sUrl + "?http_referer=https%3A%2F%2Fwvv.33seriestreaming.com%2F")
        oRequestHandler.addHeaderEntry('Accept', "*/*")
        oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
        oRequestHandler.addHeaderEntry('Content-Type', "application/json")
        oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip, deflate')
        oRequestHandler.addHeaderEntry('x-requested-with', 'XMLHttpRequest')
        oRequestHandler.addHeaderEntry("origin","https://waaw.to")
        oRequestHandler.addJSONEntry("videokey",self.__getIdFromUrl())
        oRequestHandler.addJSONEntry("width",799)
        oRequestHandler.addJSONEntry("height",450)                
        html = oRequestHandler.request(jsonDecode=True)

        data = {'adb': adb, 'adscore': '', 'click_hash': html['hash_image'], 'clickx': 321, 'clicky': 174, 'embed_from': '0', 'gt': '', 'htoken': '', 'secure': '0', 'sh': sh, 'token': '', 'v': self.__getIdFromUrl(), 'ver': '4', 'wasmcheck': 1}
        
        headers = OrderedDict({'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-length': str(len(str(data))),
            'content-type': 'application/json',
            'origin': 'https://waaw.tv',
            'pragma': 'no-cache',
            'referer': self.__sUrl + "?http_referer=https%3A%2F%2Fwvv.33seriestreaming.com%2F",
            'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': UA,
            'x-requested-with': 'XMLHttpRequest'})

        oRequestHandler = cRequestHandler('https://waaw.tv/player/get_md5.php')
        oRequestHandler.setRequestType(1)
        for h in headers:
            oRequestHandler.addHeaderEntry(h, headers[h])            
        for a in data:
            oRequestHandler.addJSONEntry(a, data[a])             
        html = oRequestHandler.request()
        VSlog(html)

        if (api_call):
            return True, api_call + '.mp4.m3u8' + '|User-Agent=' + UA

        return False, False
