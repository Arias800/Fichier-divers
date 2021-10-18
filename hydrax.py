# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Arias800
from resources.lib.handler.requestHandler import cRequestHandler  # requete url
from resources.lib.parser import cParser  # recherche de code
from resources.hosters.hoster import iHoster
from resources.lib.comaddon import VSlog, isMatrix, VSPath
from resources.lib.jsparser import JsParser
from resources.lib.util import urlEncode
from ast import literal_eval

if isMatrix():
    import urllib.request as urllib
else:
    import urllib

import zlib
import re
import base64
import json
import requests

class cHoster(iHoster):

    def __init__(self):
        # Nom a afficher dans vStream
        self.__sDisplayName = 'Hydrax'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]' + self.__sDisplayName + '[/COLOR]'

    # facultatif mais a laisser pour compatibilitee
    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    # facultatif mais a laisser pour compatibilitee
    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        # Nom du fichier exact sans .py
        return 'hydrax'

    # facultatif mais a laisser pour compatibilitee
    def setHD(self, sHD):
        self.__sHD = ''

    # facultatif mais a laisser pour compatibilitee
    def getHD(self):
        return self.__sHD

    # Telechargement possible ou pas sur ce host ?
    def isDownloadable(self):
        return True

    # Ne sert plus
    def isJDownloaderable(self):
        return True

    # facultatif mais a laisser pour compatibilitee
    def getPattern(self):
        return ''

    # facultatif mais a laisser pour compatibilitee
    def __getIdFromUrl(self, sUrl):
        sPattern = "id=([^<]+)"
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]

        return ''

    # premiere fonction utilisee, memorise le lien
    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)
        # self.__sUrl = self.__sUrl.replace('https://', 'http://')

    # facultatif mais a laisser pour compatibilitee
    def checkUrl(self, sUrl):
        return True

    # facultatif mais a laisser pour compatibilitee
    def __getUrl(self, media_id):
        return

    # Fonction appelle par Vstream pour avoir le lien decode
    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    # Extraction du lien et decodage si besoin
    def __getMediaLinkForGuest(self):
        api_call = False

        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
            "Accept-Encoding":"gzip, deflate",
            "Origin": "https://geoip.redirect-ads.com"}

        req = urllib.Request(self.__sUrl, None, headers)
        with urllib.urlopen(req) as response:
            decomp = zlib.decompressobj(16 + zlib.MAX_WBITS)
            sHtmlContent = decomp.decompress(response.read())

        oParser = cParser()
        sPattern =  '<script src="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)

        urlJS = "https://geoip.redirect-ads.com" + aResult[1][-2]

        headers['Referer'] = self.__sUrl
        req = urllib.Request(urlJS, None, headers)
        with urllib.urlopen(req) as response:
            decomp = zlib.decompressobj(16 + zlib.MAX_WBITS)
            sHtmlContent = decomp.decompress(response.read()).decode('utf-8')

        #2ème partie des données.
        aResult1 = re.search('([^>]+)', sHtmlContent, re.DOTALL | re.UNICODE).group(1)
        data = CheckAADecoder(aResult1)
        dataPartOne = json.loads(re.search('SoTrymConfigDefault = ([^>]+)"',data).group(1))

        urlJS = "https://geoip.redirect-ads.com" + aResult[1][-1]

        req = urllib.Request(urlJS, None, headers)
        with urllib.urlopen(req) as response:
            decomp = zlib.decompressobj(16 + zlib.MAX_WBITS)
            sHtmlContent = decomp.decompress(response.read()).decode('utf-8')

        #1er partie des données
        aResult2 = re.search('\}([^>]+)', sHtmlContent, re.DOTALL | re.UNICODE).group(1)
        data = CheckAADecoder(aResult2)

        dataPartTwo = json.loads(base64.b64decode(re.search('atob\("(.+?)"',data).group(1)))

        from resources.lib.comaddon import dialog

        url = [dataPartOne["sd"],dataPartOne['hd']]
        qua = ["SD","HD"]

        # Affichage du tableau
        ID = dialog().VSselectqual(qua, url)

        pathfile = VSPath('special://userdata/addon_data/plugin.video.vstream/')

        HosterUrl = "https://cdn.heycdn21.xyz/{}/{}/{}/".format(dataPartTwo['md5_id'], ID[0],dataPartOne['pieceLength'])

        response = requests.get(HosterUrl + "0/",headers=headers).content
        b64response = base64.b64decode(response)

        with open(pathfile + "video.mp4", "wb") as fh:
            fh.write(b64response)

        duration = get_video_duration(pathfile + "video.mp4")
        splitDuration = str(duration / 79)

        data = '#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:%s\n#EXT-X-MEDIA-SEQUENCE:0\n' % str(duration)

        i = 0
        while i < 80:
            data += '#EXTINF:%s,\n' % splitDuration
            data += "http://127.0.0.1:2424?u="+HosterUrl + str(i)+ "@" + urlEncode(headers) + ' \n'
            i = i + 1

        data += '#EXT-X-ENDLIST'

        with open(pathfile + "playlist.m3u8", 'w') as file:
            file.write(data)

        api_call = pathfile + "playlist.m3u8"

        if (api_call):
            return True, api_call

        return False, False


def get_video_duration(file_path_name):
    #Based on https://github.com/ZhenningLang/python-video-info/blob/master/src/_video_info.py
    """获取视频时常

    Args:
        file_path_name:

    Returns: duration, or -1 fail to dectect

    """
    CONTENTS = ['ver_and_expand', 'ctime', 'mtime', 'time_scale', 'duration']
    with open(file_path_name, 'rb') as f:
        # find mvhd
        for i in range(1000):
            data = f.read(4)
            if data == b'\x6d\x76\x68\x64':
                break
        # find time_scale and duration
        time_scale = 0
        duration = 0
        for i in range(len(CONTENTS)):
            data = f.read(4)
            if CONTENTS[i] == 'time_scale':
                time_scale = int.from_bytes(data, byteorder='big')
            elif CONTENTS[i] == 'duration':
                duration = int.from_bytes(data, byteorder='big')
        return round(duration / time_scale, 3)

def CheckAADecoder(data):
    aResult = re.search('(ﾟωﾟ.+?\(\'_\'\);)', data, re.DOTALL | re.UNICODE)
    if (aResult):
        VSlog('AA encryption')

        JP = JsParser()
        data = JP.ProcessJS(aResult.group(1))
        data = literal_eval("b'{}'".format(data)).decode('unicode_escape')
        return data

    return data
