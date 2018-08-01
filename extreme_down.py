#-*- coding: utf-8 -*-
#
# Votre nom ou pseudo
#
#
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog

import xbmc
import urllib
import xbmcgui, xbmcvfs

#Si vous créez une source et la deposez dans le dossier "sites" elle sera directement visible sous xbmc

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
headers = { 'User-Agent' : UA }

SITE_IDENTIFIER = 'extreme_down' #identifant (nom de votre fichier) remplacez les espaces et les . par _ AUCUN CARACTERE SPECIAL
SITE_NAME = 'Extreme-Download' #nom que xbmc affiche
SITE_DESC = 'films en streaming, streaming hd, streaming 720p, Films/séries, récent' #description courte de votre source

URL_MAIN = 'https://www.extreme-d0wn.com/' #url de votre source

#definis les url pour les catégories principale, ceci est automatique, si la definition est présente elle sera affichee.
#LA RECHERCHE GLOBAL N'UTILE PAS showSearch MAIS DIRECTEMENT LA FONCTION INSCRITE DANS LA VARIABLE URL_SEARCH_*
URL_SEARCH = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + 'index.php?', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN  + 'index.php?', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

# menu films existant dans l'acceuil (Home)
MOVIE_NEWS = (URL_MAIN, 'showMovies') #films (derniers ajouts = trie par date)
MOVIE_MOVIE = ('http://', 'load') #films (load source)
MOVIE_HD1080 = (URL_MAIN + 'films-hd/bluray-1080p', 'showMovies') #films HD
MOVIE_GENRES = (True, 'showGenres') #films genres
MOVIE_ANNEES = (True, 'showMovieYears') #films (par années)
#menu supplementaire non gerer par l'acceuil
MOVIE_VOSTFR = (URL_MAIN + 'films-sd/dvdrip-vostfr', 'showMovies') #films VOSTFR
MOVIE_4K = (URL_MAIN + 'films-hd/ultrahd-4k', 'showMovies')
MOVIE_720 = (URL_MAIN + 'films-hd/bluray-720p', 'showMovies')
MOVIE_1080X265 = (URL_MAIN + 'films-hd/films-1080p-x265', 'showMovies')
MOVIE_BLURAYVOSTFR = (URL_MAIN + 'films-hd/bluray-vostfr', 'showMovies')
MOVIE_3D = (URL_MAIN + 'films-hd/bluray-3d', 'showMovies')
MOVIE_FULL1080P = (URL_MAIN + 'films-hd/full-bluray', 'showMovies')
MOVIE_FULL3D = (URL_MAIN + 'films-hd/full-bluray-3d', 'showMovies')
MOVIE_FULL4K = (URL_MAIN + 'films-hd/full-bluray-ultrahd-4k', 'showMovies')
MOVIE_LIGHT720 = (URL_MAIN + 'films-hdlight/hdlight-720p', 'showMovies')
MOVIE_LIGHT1080 = (URL_MAIN + 'films-hdlight/hdlight-1080p', 'showMovies')
MOVIE_LIGHTBDRIP = (URL_MAIN + 'films-hd/bdrip-720p', 'showMovies')
MOVIE_BDRIP = (URL_MAIN + 'films-sd/dvdrip', 'showMovies')
MOVIE_OLDDVD = (URL_MAIN + 'films-sd/ancien-dvdrip', 'showMovies')
MOVIE_FILMO = (URL_MAIN + 'films-sd/filmographie', 'showMovies')

# menu serie existant dans l'acceuil (Home)
SERIE_SERIES = ('http://', 'load') #séries (load source)
SERIE_HD = (URL_MAIN + 'series-hd/1080p-series-vf', 'showMovies') #series_hd.png | séries HD
SERIE_GENRES = (True, 'showGenres') #séries genres
SERIE_ANNEES = (True, 'showSerieYears') #séries (par années)
SERIE_VOSTFRS = (URL_MAIN + 'series-hd/1080p-series-vostfr/', 'showMovies') #séries Vostfr
SERIE_720VO = (URL_MAIN + 'series-hd/hd-series-vostfr', 'showMovies')
SERIE_720VF = (URL_MAIN + 'series-hd/hd-series-vf', 'showMovies')
SERIE_4K = (URL_MAIN + 'series-hd/hd-x265-hevc/', 'showMovies')
SERIE_MULTI = (URL_MAIN + 'series-hd/hd-series-multi/', 'showMovies')
SERIE_SDVO = (URL_MAIN + 'series/vostfr/', 'showMovies')
SERIE_SDVF = (URL_MAIN + 'series/vf/', 'showMovies')


ANIM_ANIMS = ('http://', 'load') #animés (load source)
ANIM_FILM = (URL_MAIN + 'mangas/manga-films/', 'showMovies') #animés (derniers ajouts = trie par date)
ANIM_VOSTFRS =  (URL_MAIN + 'mangas/series-vostfr/', 'showMovies') #animes_views.png #animés (les plus vus = populaire)
ANIM_VFS = (URL_MAIN + 'mangas/series-vf/', 'showMovies') #animés VF
ANIM_MULTI = (URL_MAIN + 'mangas/series-multi/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'documentaires/', 'showMovies') #Documentaire
DOC_DOCS = ('http://', 'load') #Documentaire Load
DOC_GENRES = (True, 'showGenres') # Documentaires Genres

SPORT_SPORTS = (URL_MAIN + 'url', 'showMovies') #sport

NETS_NETS = ('http://' , 'load') #video du net load
NETS_NEWS =  (URL_MAIN + 'top-video.php', 'showMovies') #video du net (derniers ajouts = trie par date)
NETS_VIEWS =  (URL_MAIN + 'url', 'showMovies') #videos (les plus vus = populaire)
NETS_GENRES = (True, 'showGenres') #video du net (genre)

REPLAYTV_REPLAYTV = ('http://', 'load') #Replay load
REPLAYTV_NEWS = (URL_MAIN, 'showMovies') #Replay trie par date
REPLAYTV_GENRES = (True, 'showGenres') #Replay Genre

def load():
    oGui = cGui()

    oGui.addText(SITE_IDENTIFIER, "[COLOR red]Cette source est compatible avec Chrome Launcher[/COLOR]")

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuFilms', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuSeries', 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showMenuMangas', 'Anime', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuFilms():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_HD1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_HD1080[1], 'bluray 1080P', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_4K[1], 'bluray 4K', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VOSTFR[1], 'films VOSTFR', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_720[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_720[1], 'bluray 720P', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_1080X265[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_1080X265[1], 'bluray 1080P H265/HEVC', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BLURAYVOSTFR[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BLURAYVOSTFR[1], 'bluray VOSTFR', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_3D[1], 'bluray 3D', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL1080P[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL1080P[1], 'REMUX 1080P', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL3D[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL3D[1], 'REMUX 3D', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FULL4K[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FULL4K[1], 'REMUX 4K', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHT720[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHT720[1], 'HD light 720P', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHT1080[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHT1080[1], 'HD light 1080P', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_LIGHTBDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_LIGHTBDRIP[1], 'HD light BDRIP', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_BDRIP[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_BDRIP[1], 'films BDRIP/DVDRIP', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_OLDDVD[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_OLDDVD[1], 'ancien DVDRIP', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_FILMO[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_FILMO[1], 'filmographie', 'films_news.png', oOutputParameterHandler)
    oGui.setEndOfDirectory()

def showMenuSeries():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_HD[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_HD[1], 'series 1080p VF', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_VOSTFRS[1], 'series 1080p VOSTFR', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_720VF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_720VF[1], 'series 720p VF', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_720VO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_720VO[1], 'series 720p VOSTFR', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_4K[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_4K[1], 'series 4K H265/HEVC', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_MULTI[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_MULTI[1], 'series multilangue', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVF[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SDVF[1], 'serie VF', 'films_news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SDVO[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SDVO[1], 'serie VOSTFR', 'films_news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMenuMangas():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_FILM[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_FILM[1], "Film d'animation japonais (Derniers ajouts)", 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VOSTFRS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VOSTFRS[1], "Anime Vostfr (Derniers ajouts)", 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_VFS[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_VFS[1], "Anime Vf (Derniers ajouts)", 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', ANIM_MULTI[0])
    oGui.addDir(SITE_IDENTIFIER, ANIM_MULTI[1], "Anime multilangue (Derniers ajouts)", 'news.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres(): #affiche les genres
    oGui = cGui()

    #juste a entrer les categories et les liens qui vont bien
    liste = []
    liste.append( ['Action', URL_MAIN + 'action/'] )
    liste.append( ['Animation', URL_MAIN + 'animation/'] )
    liste.append( ['Arts Martiaux', URL_MAIN + 'arts-martiaux/'] )
    liste.append( ['Aventure', URL_MAIN + 'aventure/'] )
    liste.append( ['Biopic', URL_MAIN + 'biopic/'] )
    liste.append( ['Comédie', URL_MAIN + 'comedie/'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'comedie-dramatique/'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'comedie-musicale/'] )
    liste.append( ['Documentaire', URL_MAIN + 'documentaire/'] )
    liste.append( ['Drame', URL_MAIN + 'drame/'] )
    liste.append( ['Epouvante Horreur', URL_MAIN + 'epouvante-horreur/'] )
    liste.append( ['Erotique', URL_MAIN + 'erotique'] )
    liste.append( ['Espionnage', URL_MAIN + 'espionnage/'] )
    liste.append( ['Famille', URL_MAIN + 'famille/'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique/'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'historique/'] )
    liste.append( ['Musical', URL_MAIN + 'musical/'] )
    liste.append( ['Policier', URL_MAIN + 'policier/'] )
    liste.append( ['Péplum', URL_MAIN + 'peplum/'] )
    liste.append( ['Romance', URL_MAIN + 'romance/'] )
    liste.append( ['Science Fiction', URL_MAIN + 'science-fiction/'] )
    liste.append( ['Spectacle', URL_MAIN + 'spectacle/'] )
    liste.append( ['Thriller', URL_MAIN + 'thriller/'] )
    liste.append( ['Western', URL_MAIN + 'western/'] )
    liste.append( ['Divers', URL_MAIN + 'divers/'] )

    for sTitle, sUrl in liste: #boucle

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl) #sortie de l'url en parametre
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
        #ajouter un dossier vers la fonction showMovies avec le titre de chaque categorie.

    oGui.setEndOfDirectory()


def showMovieYears():#creer une liste inversée d'annees
    oGui = cGui()

    for i in reversed (xrange(1913, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showSerieYears():
    oGui = cGui()

    for i in reversed (xrange(1936, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'series/annee-' + Year)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()


def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    Nextpagesearch = oInputParameterHandler.getValue('Nextpagesearch')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    bGlobal_Search = False

    if Nextpagesearch:
        sSearch = sUrl

    if sSearch:

        if URL_SEARCH[0] in sSearch:
            bGlobal_Search = True
            sSearch=sSearch.replace(URL_SEARCH[0],'')

        if Nextpagesearch:
            query_args = (('do', 'search'), ('subaction', 'search') ,('search_start', Nextpagesearch),('story', sSearch) , ('titleonly', '3') )
        else:
            query_args = (('do', 'search'), ('subaction', 'search'), ('story', sSearch), ('titleonly', '3'))

        data = urllib.urlencode(query_args)

        oRequestHandler = cRequestHandler(URL_SEARCH[0])
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParametersLine(data)
        oRequestHandler.addParameters('User-Agent', UA)
        sHtmlContent = oRequestHandler.request()
        sHtmlContent = oParser.abParse(sHtmlContent,'de la recherche','Nous contacter')
    else:
        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

    sPattern = '<a class="top-last thumbnails" href="(.+?)"><img class="img-post" src="(.+?)" style="" alt="(.+?) - (.+?)"'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #le plus simple et de faire un  cConfig().log(str(aResult))
    #dans le fichier log d'xbmc vous pourrez voir un array de ce que recupere le script
    #et modifier sPattern si besoin

    #affiche une information si aucun resulat
    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            #L'array affiche vos info dans l'orde de sPattern en commencant a 0, attention dans ce cas la on recupere 6 information
            #Mais selon votre regex il ne peut y en avoir que 2 ou 3.
            sTitle = str(aEntry[2])
            sUrl2 = str(aEntry[0])
            sThumb = str(aEntry[1])
            sDesc = ''

            #Si recherche et trop de resultat, on nettoye
            #31/12/17 Ne fonctionne plus ?
            if sSearch and total > 2:
                if cUtil().CheckOccurence(sSearch, sTitle) == 0:
                    continue

            sDisplayTitle = ('%s [%s]') % (sTitle, str(aEntry[3]))

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumb', sThumb) #sortie du poster

            if 'mangas' in sUrl:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, sDesc, oOutputParameterHandler)
            else:
                oGui.addTV(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            #addMovies pour sortir les films (identifiant, function, titre, icon, poster, description, sortie parametre)

            #il existe aussi addMisc(identifiant, function, titre, icon, poster, description, sortie parametre)
            #la difference et pour les metadonner serie, films ou sans

        progress_.VSclose(progress_) #fin du dialog

        if sSearch:
            sPattern = '<a name="nextlink" id="nextlink" onclick="javascript:list_submit\(([0-9]+)\); return\(false\)" href="#">Suivant'
            aResult = oParser.parse(sHtmlContent, sPattern)
            if (aResult[0] == True):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sSearch)
                oOutputParameterHandler.addParameter('Nextpagesearch', aResult[1][0])
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

        else:
            sNextPage = __checkForNextPage(sHtmlContent)
            if (sNextPage != False):
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sNextPage)
                oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if Nextpagesearch:
        oGui.setEndOfDirectory()

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent): #cherche la page suivante
    oParser = cParser()
    sPattern = '<a href="(.+?)">Suivant.+?</a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False

def showLinks():
    #VSlog('mode serie')
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #Mise àjour du titre
    sPattern = '<title>(.+?) - (.+?)</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        sMovieTitle = aResult[1][0][0]

    oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Qualités disponibles pour cette saison :[/COLOR]')

    #on recherche d'abord la qualité courante
    sPattern = '<title>(.+?) - (.+?)</title>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult

    sQual = ''
    if (aResult[1]):
        sQual = aResult[1][0][1]

    sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', sUrl)
    oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
    oOutputParameterHandler.addParameter('sThumb', sThumb)
    oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

    #on regarde si dispo dans d'autres qualités
    sHtmlContent1 = CutQual(sHtmlContent)
    sPattern1 = '<a class="btn-other" href="([^"]+)">([^"]+)</a>'

    aResult1 = oParser.parse(sHtmlContent1, sPattern1)
    #print aResult1

    if (aResult1[0] == True):
        total = len(aResult1[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult1[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = aEntry[0]
            sQual = aEntry[1]
            sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    #on regarde si dispo d'autres saisons
    sHtmlContent2 = CutSais(sHtmlContent)
    sPattern2 = '<a class="btn-other" href="([^"]+)">([^"]+)</a>'

    aResult2 = oParser.parse(sHtmlContent2, sPattern2)
    #print aResult2

    if (aResult2[0] == True):
        oGui.addText(SITE_IDENTIFIER,'[COLOR olive]Autres Saisons disponibles pour cette série :[/COLOR]')

        for aEntry in aResult2[1]:

            sUrl = str(aEntry[0])
            sTitle = sMovieTitle + '[COLOR skyblue]'+ aEntry[1] + '[/COLOR]'

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addTV(SITE_IDENTIFIER, 'showLinks', sTitle, 'series.png', sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters(): #recherche et affiche les hotes
    oGui = cGui()

    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sThumb = oInputParameterHandler.getValue('sThumb')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if 'series' in sUrl:
        sPattern = '<div class="prez_7">([^"]+)</div>\s*<div style="padding.+?">|<a title=".+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<>]+)*</strong>'
    else:
        sPattern = '<a title="T.+?" href="([^"]+)" target="_blank"><strong class="hebergeur">*([^<>]+)*</strong>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        total = len(aResult[1])

        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            if 'series' in sUrl:
                if ('Episode' in aEntry[0]):
                    oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + str(aEntry[0]) + '[/COLOR]')

                sTitle = str(aEntry[2]) + str(aEntry[1])
                sUrl2 = str(aEntry[1])
            else:
                sTitle = str(aEntry[1]) + str(aEntry[0])
                sUrl2 = str(aEntry[0])

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            oGui.addTV(SITE_IDENTIFIER, 'RecapchaBypass', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def RecapchaBypass():
    oGui = cGui() #ouvre l'affichage
    oInputParameterHandler = cInputParameterHandler() #apelle l'entree de parametre
    sUrl = oInputParameterHandler.getValue('siteUrl') #apelle siteUrl
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle') #appelle le titre
    sThumb = oInputParameterHandler.getValue('sThumb') #appelle le poster

    sPath = "special://home/addons/plugin.program.chrome.launcher/default.py"

    if xbmcvfs.exists(sPath):
        sUrl2 = urllib.quote_plus(sUrl)
        xbmc.executebuiltin('RunPlugin("plugin://plugin.program.chrome.launcher/?url='+sUrl2+'&mode=showSite&stopPlayback=yes")')

    getHoster()

def getHoster(): #fonction de recherche
    oGui = cGui()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sThumb = ''
    sSearchText = oGui.showKeyBoard("Mettre ici le liens du hoster apres avoir passer les Recaptcha manuellement") #appelle le clavier xbmc
    if (sSearchText != False):
        sUrl = sSearchText #modifie l'url de recherche

        sHosterUrl = str(sUrl)
        oHoster = cHosterGui().checkHoster(sHosterUrl) #recherche l'hote dans l'addon
        if (oHoster != False):
            oHoster.setDisplayName(sMovieTitle) #nom affiche
            oHoster.setFileName(sMovieTitle) #idem
            cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory() #fin

def CutQual(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="other-qualities">&Eacute;galement disponible en :</span>(.+?)<span class="other-qualities">Autres saisons :</span>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    else:
        return sHtmlContent

    return ''

def CutSais(sHtmlContent):
    oParser = cParser()
    sPattern = '<span class="other-qualities">Autres saisons :</span>(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    #print aResult
    if (aResult[0]):
        return aResult[1][0]
    return ''
