#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui #systeme de recherche pour l'hote
from resources.lib.gui.gui import cGui #systeme d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entree des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortie des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.parser import cParser #recherche de code
from resources.lib.comaddon import progress, VSlog #import du dialog progress

SITE_IDENTIFIER = 'pikachu_streaming'
SITE_NAME = 'Pikachu Streaming'
SITE_DESC = '¨Pokemon en streaming'

URL_MAIN = 'http://pikachu-streaming.eklablog.com/'

POKEMON_FILMS = (URL_MAIN, 'showSaison')
POKEMON_SAISON = (URL_MAIN, 'showSaison')
POKEMON_SPINF_OFF = (URL_MAIN, 'showSaison')
POKEMON_TELEFILM = (URL_MAIN, 'showSaison')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', POKEMON_FILMS[0])
    oGui.addDir(SITE_IDENTIFIER, POKEMON_FILMS[1], 'Les films', 'pikachu.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', POKEMON_SAISON[0])
    oGui.addDir(SITE_IDENTIFIER, POKEMON_SAISON[1], 'Les Saison', 'pikachu.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', POKEMON_SPINF_OFF[0])
    oGui.addDir(SITE_IDENTIFIER, POKEMON_SPINF_OFF[1], 'Les Spin-off', 'pikachu.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', POKEMON_TELEFILM[0])
    oGui.addDir(SITE_IDENTIFIER, POKEMON_TELEFILM[1], 'Les Telefilm', 'pikachu.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSaison(sSearch = ''):
    oGui = cGui()
    if sSearch:
      sUrl = sSearch
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<span style="font-size: 10pt;"><a href="(.+?)">Saison (.+?)</a></span>'

    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    #le plus simple et de faire un  VSlog(str(aResult))
    #dans le fichier log d'xbmc vous pourrez voir un array de ce que recupere le script
    #et modifier sPattern si besoin
    VSlog(str(aResult)) #Commenter ou supprimer cette ligne une fois fini

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

            #L'array affiche vos info dans l'orde de sPattern en commencant a 0, attention dans ce cas la on recupere 6 information
            #Mais selon votre regex il ne peut y en avoir que 2 ou 3.
            sTitle = aEntry[1]
            sUrl2 = aEntry[0]
            sThumb = ''
            sDesc = ''

            sTitle = sTitle.replace('En streaming', '')

            #Si vous avez des information dans aEntry Qualiter lang organiser un peux vos titre exemple.
            #Si vous pouvez la langue et la Qualite en MAJ ".upper()" vostfr.upper() = VOSTFR
            #sTitle = ('%s [%s] (%s) [COLOR coral]%s[/COLOR]') % (sTitle, sQual, sLang.upper(), sHoster)
            #mettre les information de streaming entre [] et le reste entre () vstream s'occupe de la couleur automatiquement.

            #Utile que si les liens recupere ne commencent pas par (http://www.nomdusite.com/)
            #sUrl2 = URL_MAIN + sUrl2

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2) #sortie de l'url
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle) #sortie du titre
            oOutputParameterHandler.addParameter('sThumb', sThumb) #sortie du poster

            if '/series' in sUrl:
                oGui.addTV(SITE_IDENTIFIER, 'ShowSerieSaisonEpisodes', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #addTV pour sortir les series tv (identifiant, function, titre, icon, poster, description, sortie parametre)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle, '', sThumb, sDesc, oOutputParameterHandler)
                #addMovies pour sortir les films (identifiant, function, titre, icon, poster, description, sortie parametre)

            #il existe aussi addMisc(identifiant, function, titre, icon, poster, description, sortie parametre)
            #la difference et pour les metadonner serie, films ou sans

        progress_.VSclose(progress_) #fin du dialog

        sNextPage = __checkForNextPage(sHtmlContent) #cherche la page suivante
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)
            #Ajoute une entree pour le lien Next | pas de addMisc pas de poster et de description inutile donc

    if not sSearch:
        oGui.setEndOfDirectory() #ferme l'affichage


def __checkForNextPage(sHtmlContent):
    oParser = cParser()

    sPattern = '<div class="pagination">.*<a href="([^"]+)" rel="nofollow" onmouseover="Help\.bubble\(this, &quot;Page suivante&quot;\)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        return aResult[1][0]

    return False
