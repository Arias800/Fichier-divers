#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Votre nom ou pseudo
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress, dialog, xbmc, xbmcgui, VSlog

import re, base64, random, time, os, xbmcaddon, xbmcvfs

UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
__addon__ = xbmcaddon.Addon('plugin.video.vstream')

SITE_IDENTIFIER = 'time2watch'
SITE_NAME = '[COLOR violet]Time2Watch[/COLOR]'
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent'

URL_MAIN = 'https://time2watch.io/'

URL_SEARCH = (URL_MAIN + 'search/?q=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_MISC = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'

DERNIER_AJOUT = (URL_MAIN + 'last/', 'showMovies')
MOVIE_NEWS = (URL_MAIN + 'film/last/', 'showMovies')
MOVIE_MOVIE = ('http://', 'showMenuFilms')
MOVIE_POPULAIRE = (URL_MAIN + "film/popular/", 'showMovies')
MOVIE_HD1080 = (URL_MAIN + 'film/bluray/', 'showMovies')
MOVIE_VOSTFR = (URL_MAIN + 'film/vostfr/', 'showMovies')
MOVIE_VFR = (URL_MAIN + 'film/vfr/', 'showMovies')
MOVIE_NOTE = (URL_MAIN + 'film/loved/', 'showMovies')
MOVIE_GENRES = (URL_MAIN + 'film/genre/', 'showGenre')
MOVIE_ANNEES = (URL_MAIN + 'film/date/', 'showYears')

SERIE_NEWS = (URL_MAIN + 'serie/last/', 'showMovies')
SERIE_SERIES = ('http://', 'showMenuSeries')
SERIE_POPULAIRE = (URL_MAIN + "serie/popular/", 'showMovies')
SERIE_HD1080 = (URL_MAIN + 'serie/bluray/', 'showMovies')
SERIE_VOSTFR = (URL_MAIN + 'serie/vostfr/', 'showMovies')
SERIE_VFR = (URL_MAIN + 'serie/vfr/', 'showMovies')
SERIE_NOTE = (URL_MAIN + 'serie/loved/', 'showMovies')
SERIE_GENRES = (URL_MAIN + 'serie/genre/', 'showGenre')
SERIE_ANNEES = (URL_MAIN + 'serie/date/', 'showYears')

ANIM_NEWS = (URL_MAIN + 'anime/last/', 'showMovies')
ANIM_ANIMS = ('http://', 'showMenuAnimes')
ANIM_POPULAIRE = (URL_MAIN + "anime/popular/", 'showMovies')
ANIM_HD1080 = (URL_MAIN + 'anime/bluray/', 'showMovies')
ANIM_VOSTFR = (URL_MAIN + 'anime/vostfr/', 'showMovies')
ANIM_VFR = (URL_MAIN + 'anime/vfr/', 'showMovies')
ANIM_NOTE = (URL_MAIN + 'anime/loved/', 'showMovies')
ANIM_GENRES = (URL_MAIN + 'anime/genre/', 'showGenre')
ANIM_ANNEES = (URL_MAIN + 'anime/date/', 'showYears')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies')
SPECTACLE_NEWS =  (URL_MAIN + 'theatre/', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', DERNIER_AJOUT[0])
    oGui.addDir(SITE_IDENTIFIER, DERNIER_AJOUT[1], 'Derniers Ajouts', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Animés', 'animes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuAutre', 'Autres', 'tv.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD1080[1], 'Bluray 1080P', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_POPULAIRE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_POPULAIRE[1], 'Films les plus populaire', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'Films (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VFR[1], 'Film (VFR)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTE[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTE[1], 'Film les mieux notés', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NEWS[1], 'Series (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Series (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Series (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD1080[1], 'Bluray 1080P', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_POPULAIRE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_POPULAIRE[1], 'Series les plus populaire', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFR[1], 'Series (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VFR[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VFR[1], 'Series (VFR)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_NOTE[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_NOTE[1], 'Series les mieux notés', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NEWS[1], 'Animes (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_GENRES[1], 'Animes (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_ANNEES[1], 'Animes (Années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_HD1080[1], 'Bluray 1080P', 'hd.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_POPULAIRE[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_POPULAIRE[1], 'Animes les plus populaire', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFR[1], 'Animes (VOSTFR)', 'vostfr.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFR[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFR[1], 'Animes (VFR)', 'vf.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_NOTE[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_NOTE[1], 'Animes les mieux notés', 'notes.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch(): #fonction de recherche
    oGui = cGui()

    sSearchText = oGui.showKeyBoard() #appelle le clavier xbmc
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText #modifie l'url de recherche
        showMovies(sUrl) #appelle la fonction qui pourra lire la page de resultats
        oGui.setEndOfDirectory()
        return

def showGenre():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    html = re.search('<section id="section_genre">(.+?)</section>',sHtmlContent,re.DOTALL).group(1)
    sPattern = '<a href="([^"]+)">([^"]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(html, sPattern)

    for genre in aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + genre[0])
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', genre[1], 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showYears():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    html = re.search('<section id="section_genre">(.+?)</section>',sHtmlContent,re.DOTALL).group(1)
    sPattern = '<a href="([^"]+)">([^"]+)</a>'

    oParser = cParser()
    aResult = oParser.parse(html, sPattern)

    for Years in aResult[1]:
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + Years[0])
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Years[1], 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui() #ouvre l'affichage
    if sSearch: #si une url et envoyer directement grace a la fonction showSearch
      sUrl = sSearch.replace(' ', '+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl') #recupere l'url sortie en parametre

    oRequestHandler = cRequestHandler(sUrl) #envoye une requete a l'url
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="col-lg-4.+?<a href="([^"]+)">.+?affiche_liste" src="([^"]+)".+?alt="([^"]+)".+?<i class="fa fa-tv"></i>([^<]+)<.+?div class="synopsis_hover".+?>([^<]+)<'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    #affiche une information si aucun resulat
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        #dialog barre de progression
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) #dialog update
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + aEntry[0]
            sThumb = URL_MAIN + aEntry[1]
            sTitle = aEntry[2]
            #sLang = aEntry[3]
            sQual = aEntry[3]
            #sHoster = aEntry[5]
            sDesc = aEntry[4]

            sTitle = sTitle.replace('En streaming', '')

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumb', sThumb) #sortie du poster

            if '/serie/' in sUrl2 or '/anime/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showMoviesLink', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

    if not sSearch:
        sNextPage = __checkForNextPage(sHtmlContent) #cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        oGui.setEndOfDirectory() #ferme l'affichage

def __checkForNextPage(sHtmlContent): #cherche la page suivante
    oParser = cParser()
    sPattern = '<a class="light_pagination" href="([^"]+)" aria-label="Next">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return URL_MAIN + aResult[1][0]

    return False

def showMoviesLink():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sPattern = '<i class="fa fa-download fa-fw"></i>.+?<b>(.+?)</b></a>'
    var = re.search('var hash = (.+?);',sHtmlContent).group(1).replace('"',"").strip('][').split(',')
    url = re.search("document\.getElementById\(\'openlink_\'\+n\).href = '(.+?)';",sHtmlContent).group(1)

    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        #dialog barre de progression
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry, VAR in zip(aResult[1], var):
            progress_.VSupdate(progress_, total) #dialog update
            if progress_.iscanceled():
                break

            sUrl2 = URL_MAIN + url.replace("'+nhash+'",VAR)
            sTitle = ('%s [%s]') % (sMovieTitle, aEntry)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addMovie(SITE_IDENTIFIER, 'DecryptTime', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def ShowSerieSaisonEpisodes():
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    url = re.search("document\.getElementById\(\'openlink_\'\+n\).href = '(.+?)';",sHtmlContent).group(1)
    oParser = cParser()
    sPattern = '<span style="margin-left: 20px;">(.+?)</span>|<span style="margin-left: 35px;">(.+?)<.+?<span class="fa arrow">|onmousedown.+?<b>(.+?)</b>.+?var hash_.+?= "(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])
        #dialog barre de progression
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total) #dialog update
            if progress_.iscanceled():
                break

            if aEntry[0]:
                ses = aEntry[0]

            elif aEntry[1]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + ses + ' ' + aEntry[1] + '[/COLOR]')

            else:
                sUrl2 = URL_MAIN + url.replace("'+nhash+'",aEntry[3])
                sDisplayTitle = ('%s [%s]') % (sMovieTitle, aEntry[2])

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl2)
                oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)

                oGui.addMovie(SITE_IDENTIFIER, 'DecryptTime', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def getLinkHtml(sHtmlContent):
    oParser = cParser()
    sPattern = '<div class="panel panel-s4i panel-no-border".+?>(.+?)<span style='
    aResult = oParser.parse(sHtmlContent, sPattern)
    return aResult[1][0]

def DecryptTime():
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    result = re.search('<img src="(.+?)" style="min-height: 300px; height: 300px; background: #333333;">.+?<input type="hidden" name="challenge" value="(.+?)">',sHtmlContent, re.MULTILINE|re.DOTALL)
    challenge = result.group(1)
    challengeTok = result.group(2)

    oParser = cParser()
    sPattern = '<label for="(.+?)".+?onclick="ie_click.+?<img src=".+?base64,(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    dialogs = dialog()
    Filename = []
    i = 0

    oRequestHandler = cRequestHandler(challenge)
    sHtmlContent = oRequestHandler.request()

    downloaded_image = xbmcvfs.File("special://home/userdata/addon_data/plugin.video.vstream/challenge.png", 'wb')
    downloaded_image.write(sHtmlContent)
    downloaded_image.close()

    for base64_string in aResult[1]:
        imgdata = base64.b64decode(base64_string[1])

        downloaded_image = xbmcvfs.File("special://home/userdata/addon_data/plugin.video.vstream/test"+str(i)+".png", 'wb')
        downloaded_image.write(imgdata)
        downloaded_image.close()
        Filename.append("special://home/userdata/addon_data/plugin.video.vstream/test"+str(i)+".png")
        i = i + 1

    oSolver = cInputWindow(captcha = Filename, challenge = "special://home/userdata/addon_data/plugin.video.vstream/challenge.png")
    retArg = oSolver.get()

    data = "challenge="+challengeTok+"&g-recaptcha-response="+aResult[1][int(retArg)][0]

    oRequestHandler = cRequestHandler(sUrl)
    oRequestHandler.setRequestType(1)
    oRequestHandler.addHeaderEntry('User-Agent', UA)
    oRequestHandler.addHeaderEntry('Content-Type',  "application/x-www-form-urlencoded")
    oRequestHandler.addHeaderEntry('Content-Length', len(str(data)))
    oRequestHandler.addParametersLine(data)
    sHtmlContent = oRequestHandler.request()
    sHtmlContent = getLinkHtml(sHtmlContent)

    oParser = cParser()
    sPattern = '<img src=.+?<a href="([^"]+)">'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if aResult[0] == True:
        for aEntry in aResult[1]:

            oHoster = cHosterGui().checkHoster(aEntry)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, aEntry, sThumb)

    oGui.setEndOfDirectory()

class cInputWindow(xbmcgui.WindowDialog):
    def __init__(self, *args, **kwargs):

        self.cptloc = kwargs.get('captcha')
        # self.img = xbmcgui.ControlImage(250, 110, 780, 499, '')
        # xbmc.sleep(500)
        i = 0
        u = 100
        pos = []

        self.img = [0]*6
        for img in self.cptloc:
            self.img[i] = xbmcgui.ControlImage(u, 400, 200, 200, img)
            i = i + 1
            pos.append(u)
            u = u + 200

        self.img[5] = xbmcgui.ControlImage(500, 0, 300, 499, kwargs.get('challenge'))

        bg_image = os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + 'background.png'
        check_image = os.path.join( __addon__.getAddonInfo('path'), 'resources/art/' ) + 'trans_checked.png'

        self.ctrlBackground = xbmcgui.ControlImage(0, 0, 1280, 720, bg_image)
        self.cancelled = False
        self.addControl (self.ctrlBackground)

        self.addControl(self.img[0])
        self.addControl(self.img[1])
        self.addControl(self.img[2])
        self.addControl(self.img[3])
        self.addControl(self.img[4])
        self.addControl(self.img[5])

        self.chk = [0]*5
        self.chkbutton = [0]*5
        self.chkstate = [False]*5

        if 1 == 2:
            self.chk[0] = xbmcgui.ControlCheckMark(pos[0], 400, 200, 200, '1', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[1] = xbmcgui.ControlCheckMark(pos[1], 400, 200, 200, '2', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[2] = xbmcgui.ControlCheckMark(pos[2], 400, 200, 200, '3', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[3] = xbmcgui.ControlCheckMark(pos[3], 400, 200, 200, '4', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)
            self.chk[4] = xbmcgui.ControlCheckMark(pos[4], 400, 200, 200, '5', font = 'font14', focusTexture = check_image, checkWidth = 260, checkHeight = 166)

        else:
            self.chk[0] = xbmcgui.ControlImage(pos[0], 400, 200, 200, check_image)
            self.chk[1] = xbmcgui.ControlImage(pos[1], 400, 200, 200, check_image)
            self.chk[2] = xbmcgui.ControlImage(pos[2], 400, 200, 200, check_image)
            self.chk[3] = xbmcgui.ControlImage(pos[3], 400, 200, 200, check_image)
            self.chk[4] = xbmcgui.ControlImage(pos[4], 400, 200, 200, check_image)

            self.chkbutton[0] = xbmcgui.ControlButton(pos[0], 400, 200, 200, '1', font = 'font1')
            self.chkbutton[1] = xbmcgui.ControlButton(pos[1], 400, 200, 200, '2', font = 'font1')
            self.chkbutton[2] = xbmcgui.ControlButton(pos[2], 400, 200, 200, '3', font = 'font1')
            self.chkbutton[3] = xbmcgui.ControlButton(pos[3], 400, 200, 200, '4', font = 'font1')
            self.chkbutton[4] = xbmcgui.ControlButton(pos[4], 400, 200, 200, '5', font = 'font1')

        for obj in self.chk:
            self.addControl(obj)
            obj.setVisible(False)
        for obj in self.chkbutton:
            self.addControl(obj)

        self.cancelbutton = xbmcgui.ControlButton(250 + 260 - 70, 620, 140, 50, 'Cancel', alignment = 2)
        self.okbutton = xbmcgui.ControlButton(250 + 520 - 50, 620, 100, 50, 'OK', alignment = 2)
        self.addControl(self.okbutton)
        self.addControl(self.cancelbutton)

        self.chkbutton[0].controlDown(self.cancelbutton);   self.cancelbutton.controlUp(self.chkbutton[0])
        self.chkbutton[1].controlDown(self.cancelbutton);   self.okbutton.controlUp(self.chkbutton[4])
        self.chkbutton[2].controlDown(self.okbutton);
        self.chkbutton[3].controlDown(self.okbutton);
        self.chkbutton[4].controlDown(self.okbutton);

        self.chkbutton[0].controlLeft(self.chkbutton[4]);  self.chkbutton[0].controlRight(self.chkbutton[1]);
        self.chkbutton[1].controlLeft(self.chkbutton[0]);  self.chkbutton[1].controlRight(self.chkbutton[2]);
        self.chkbutton[2].controlLeft(self.chkbutton[1]);  self.chkbutton[2].controlRight(self.chkbutton[3]);
        self.chkbutton[3].controlLeft(self.chkbutton[2]);  self.chkbutton[3].controlRight(self.chkbutton[4]);
        self.chkbutton[4].controlLeft(self.chkbutton[3]);  self.chkbutton[4].controlRight(self.chkbutton[0]);        

        self.cancelled = False
        self.setFocus(self.okbutton)
        self.okbutton.controlLeft(self.cancelbutton);      self.okbutton.controlRight(self.cancelbutton);
        self.cancelbutton.controlLeft(self.okbutton);      self.cancelbutton.controlRight(self.okbutton);
        self.okbutton.controlDown(self.chkbutton[4]);      self.okbutton.controlUp(self.chkbutton[4]);
        self.cancelbutton.controlDown(self.chkbutton[0]);  self.cancelbutton.controlUp(self.chkbutton[0]);

    def get(self):
        self.doModal()
        self.close()
        if not self.cancelled:
            retval = ""
            for objn in range(5):
                if self.chkstate[objn]:
                    retval += ("" if retval == "" else ",") + str(objn)
            return retval

        else:
            return ""

    def anythingChecked(self):
        for obj in self.chkstate:
            if obj:
                return True
        return False

    def onControl(self, control):
        if control == self.okbutton:
            if self.anythingChecked():
                self.close()
        elif control == self.cancelbutton:
            self.cancelled = True
            self.close()
        try:
            if 'xbmcgui.ControlButton' in repr(type(control)):
                index = control.getLabel()
                if index.isnumeric():
                    self.chkstate[int(index)-1] = not self.chkstate[int(index)-1]
                    self.chk[int(index)-1].setVisible(self.chkstate[int(index)-1])

        except:
            pass

    def onAction(self, action):
        if action == 10:
            self.cancelled = True
            self.close()
