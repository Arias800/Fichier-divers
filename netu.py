#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
#test film strem vk 1er page dark higlands & tous ces enfants m'appartiennent
from resources.hosters.hoster import iHoster
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import VSlog
from resources.lib.tinyjsparser import JsParser
import re, requests

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:72.0) Gecko/20100101 Firefox/72.0'

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

    def __getMediaLinkForGuest(self):
        api_call = ''

        data = {"width":1198,"height":600}

        headers = {"Host": "hqq.tv",
            "User-Agent": UA,
            "Accept": "*/*",
            "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": self.__sUrl,
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://hqq.tv",
            "Cookie": "__cfduid=d4f620f4791cc05648c7c0b48a4347aed1610273987; _ym_uid=1610867611576756944; _ym_d=1610867611",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "TE": "Trailers"}

        click_hash = requests.post('https://hqq.tv/player/get_player_image.php', json=data, headers=headers).json()
    
        oRequestHandler = cRequestHandler(self.__sUrl)
        oRequestHandler.addHeaderEntry('User-Agent', UA)
        html = oRequestHandler.request()

        JScode = re.search(' = null;\s*}(.+?)hcaptchatbl',html, re.MULTILINE|re.DOTALL).group(1).split('//(functio')[0].encode('latin1').decode('utf-8')
        JP = JsParser()
        data = (JP.ProcessJS(JScode).encode('latin1').decode('unicode-escape'))

        sh = re.search("shh*= *\'(.+?)\';", data).group(1)
        adb = re.search("adbn = \'(.+?)\'", html).group(1)

        data = {"htoken":"","sh":sh,"ver":"4","secure":"0","adb":adb,"v":self.__sUrl.split('/')[4],"token":"","gt":"","embed_from":"0","wasmcheck":1,"adscore":"","click_hash":click_hash["hash_image"],"clickx":387,"clicky":401}
        html = requests.post('https://hqq.tv/player/get_md5.php', json=data, headers=headers).json()

        if int(html["need_captcha"]) == 1:
            captcha = "https://hqq.tv/player/embed_player.php?vid=" + self.__sUrl.split('/')[4] + "&need_captcha=1&pop=0"

            oRequestHandler = cRequestHandler(captcha)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
            sHtmlContent = oRequestHandler.request()
            cookies = oRequestHandler.GetCookies()
            VSlog(oRequestHandler.getResponseHeader())

            from resources.lib import librecaptcha
            test = librecaptcha.get_token(api_key="6LfCmh4TAAAAAKog9f8wTyEOc0U8Ms2RTuDFyYP_", site_url=captcha,
                                          user_agent=UA, gui=False, debug=False)

            data = 'g-recaptcha-response=' + test
            oRequestHandler = cRequestHandler(captcha + 'g-recaptcha-response=' + test)
            oRequestHandler.addHeaderEntry('User-Agent', UA)
            oRequestHandler.addHeaderEntry('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            oRequestHandler.addHeaderEntry('Accept-Language', 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3')
            oRequestHandler.addHeaderEntry('Accept-Encoding', 'gzip')
            oRequestHandler.addHeaderEntry('Referer', captcha)
            oRequestHandler.addHeaderEntry('Cookie', cookies)
            sHtmlContent = oRequestHandler.request()
            VSlog(oRequestHandler.getResponseHeader())
            VSlog(sHtmlContent)

            data = {"htoken":"","sh":sh,"ver":"4","secure":"0","adb":adb,"v":self.__sUrl.split('/')[4],"token":"","gt":"","embed_from":"0","wasmcheck":1,"adscore":"","click_hash":click_hash["hash_image"],"clickx":387,"clicky":401}
            html = requests.post('https://hqq.tv/player/get_md5.php', json=data, headers=headers).json()
            VSlog(html)

        api_call = oRequestHandler.getRealUrl()

        if (api_call):
            return True, api_call + '.mp4.m3u8' + '|User-Agent=' + UA

        return False, False
