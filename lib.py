# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.gui.gui import cGui
from resources.lib.util import cUtil, QuotePlus
from resources.lib.comaddon import addon, dialog, xbmc
import xbmcvfs

import xbmcplugin, xbmcgui
import re, os, sys

SITE_IDENTIFIER = 'cLibrary'
SITE_NAME = 'Library'

# sources.xml


class cLibrary:
    ADDON = addon()
    DIALOG = dialog()

    def __init__(self):
        self.__sMovieFolder = self.ADDON.getSetting('Library_folder_Movies')
        self.__sTVFolder = self.ADDON.getSetting('Library_folder_TVs')

        if not self.__sMovieFolder:
            self.__sMovieFolder = 'special://userdata/addon_data/plugin.video.vstream/Films'
            self.ADDON.setSetting('Library_folder_Movies', self.__sMovieFolder)
        if not xbmcvfs.exists(self.__sMovieFolder):
            xbmcvfs.mkdir(self.__sMovieFolder)

        if not self.__sTVFolder:
            self.__sTVFolder = 'special://userdata/addon_data/plugin.video.vstream/Series'
            self.ADDON.setSetting('Library_folder_TVs', self.__sTVFolder)
        if not xbmcvfs.exists(self.__sTVFolder):
            xbmcvfs.mkdir(self.__sTVFolder)

        self.__sTitle = ''

    def setLibrary(self):
        oInputParameterHandler = cInputParameterHandler()
        sHosterIdentifier = oInputParameterHandler.getValue('sHosterIdentifier')
        sFileName = oInputParameterHandler.getValue('sFileName')
        sMediaUrl = oInputParameterHandler.getValue('sMediaUrl')

        ret = self.DIALOG.select('Sélectionner une catégorie', ['Film', 'Série'])
        if ret == 0:
            sCat = '1'
        elif ret == -1:
            return
        else:
            sCat = '2'

        sMediaUrl = QuotePlus(sMediaUrl)
        sFileName = QuotePlus(sFileName)

        sLink = 'plugin://plugin.video.vstream/?function=play&site=cHosterGui&sFileName=' + sFileName + '&sMediaUrl=' + sMediaUrl + '&sHosterIdentifier=' + sHosterIdentifier

        sTitle = sFileName

        if sCat == '1':  # film
            sTitle = cUtil().CleanName(sTitle)
            sTitle = self.showKeyBoard(sTitle, 'Nom du dossier et du fichier')

            try:
                sPath = '/'.join([self.__sMovieFolder, sTitle])

                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                self.MakeFile(sPath, sTitle, sLink)
            except:
                self.DIALOG.VSinfo('Rajout impossible')

        elif sCat == '2':  # serie
            sTitle = cUtil().CleanName(sTitle)
            sFTitle = self.showKeyBoard(sTitle, 'Recommandé Nomdeserie/Saison00')

            try:

                sPath = '/'.join([self.__sTVFolder, sFTitle])

                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                sTitle = self.showKeyBoard(sTitle, 'Recommandé NomdeserieS00E00')

                self.MakeFile(sPath, sTitle, sLink)
            except:
                self.DIALOG.VSinfo('Rajout impossible')

    def MakeFile(self, folder, name, content):
        stream = '/'.join([folder, str(name)]) + '.strm'
        f = xbmcvfs.File(stream, 'w')
        result = f.write(str(content))
        f.close()
        if result:
            self.DIALOG.VSinfo('Elément rajouté à la librairie')
        else:
            self.DIALOG.VSinfo('Rajout impossible')

    def getLibrary(self):
        #xbmc.executebuiltin("Container.Update(special://userdata/addon_data/plugin.video.vstream/)", True)
        #xbmc.executebuiltin('ActivateWindow(Videos,"special://userdata/addon_data/plugin.video.vstream/")', True)
        oGui = cGui()
        path = 'special://userdata/addon_data/plugin.video.vstream/'
        listDir = xbmcvfs.listdir(path)
        for i in listDir[0]:
            Year = os.path.basename(i)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('filePath', path+i)
            oGui.addDir(SITE_IDENTIFIER, 'openLibrary', Year, 'annees.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def openLibrary(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sFile = oInputParameterHandler.getValue('filePath')

        listDir = xbmcvfs.listdir(sFile)
        for i in listDir[0]:
            path = xbmc.translatePath(sFile+'/'+i) #Suppression du special: pour plus tard
            strmFile = xbmcvfs.listdir(path) #Ovrir le repertoire avec le fichier .strm
            Year = os.path.basename(''.join(strmFile[1])) #Titre du fichier .strm

            strmPath = path+'/'+Year

            if '.strm' in strmPath:
                sHosterUrl = strmPath
                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(Year)
                    oHoster.setFileName(Year)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

            else:
                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('filePath', path+i)
                oGui.addDir(SITE_IDENTIFIER, 'openLibrary', Year, 'annees.png', oOutputParameterHandler)
                
        oGui.setEndOfDirectory()

    def callPlugin(self):
        oInputParameterHandler = cInputParameterHandler()
        pluginDir = oInputParameterHandler.getValue('pluginDir')
        sTitle = oInputParameterHandler.getValue('sTitle')

    def Delfile(self):
        oInputParameterHandler = cInputParameterHandler()
        sFile = oInputParameterHandler.getValue('sFile')

        xbmcvfs.delete(sFile)

        runClean = self.DIALOG.VSyesno('Voulez vous mettre à jour la librairie maintenant (non conseillé)', 'Fichier supprimé')
        if not runClean:
            return

        xbmc.executebuiltin('CleanLibrary(video)')

    def ShowContent(self):
        oInputParameterHandler = cInputParameterHandler()
        sFolder = oInputParameterHandler.getValue('folder')
        xbmc.executebuiltin('Container.Update(' + sFolder + ')')

    def showKeyBoard(self, sDefaultText='', Heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(Heading)  # optional
        keyboard.doModal()
        if keyboard.isConfirmed():
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False
