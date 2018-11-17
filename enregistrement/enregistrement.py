from resources.lib.gui.gui import cGui
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog
import xbmcvfs, datetime, time, _strptime

SITE_IDENTIFIER = 'Enregistrement'
SITE_NAME = 'enregistrement'

class cEnregistremement:

    def programmation_enregistrement(self, sUrl):
        oGui = cGui()
        ADDON = addon()
        if 'firstonetv' in sUrl or 'bouygtel' in sUrl:
            sUrl = sUrl.replace('|Referer=','" -headers "Referer: ').replace('&User-Agent=Mozilla/5.0+(X11;+Linux+i686)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Ubuntu+Chromium/48.0.2564.116+Chrome/48.0.2564.116+Safari/537.36&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.net','" -headers "User-Agent: Mozilla/5.0+(X11;+Linux+i686)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Ubuntu+Chromium/48.0.2564.116+Chrome/48.0.2564.116+Safari/537.36" -headers "X-Requested-With: ShockwaveFlash/28.0.0.137" -headers "Origin: https://www.firstonetv.net" -c:v libx264 -preset veryslow -crf 0 -c:a copy')
            header = sUrl
        else:
            header = sUrl+'" -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 2 -c:v libx264 -preset veryslow -crf 0 -c:a copy'

        pathEnregistrement = ADDON.getSetting('path_enregistrement_programmation')
        currentPath = ADDON.getSetting('path_enregistrement').replace('\\','/')
        ffmpeg = ADDON.getSetting('path_ffmpeg').replace('\\','/')

        heureDebut = oGui.showKeyBoard(None,"Heure du debut d\'enregistrement au format Date-Heure-Minute")
        durer = oGui.showKeyBoard(None,"Durer de l\'enregistrement au format Heure:Minute:Seconde")
        titre = oGui.showKeyBoard(None,"Titre de l\'enregistrement").replace("'","\\'")

        marge = ADDON.getSetting('marge_auto')
        formats = '%H:%M:%S'
        try:
            res = datetime.datetime.strptime(durer, formats).time()
        except TypeError:
            res = datetime.datetime(*time.strptime(durer, formats)[0:6]).time()
            timedelta = datetime.timedelta(minutes=int(marge))
            tmp_datetime = datetime.datetime.combine(datetime.date(1, 1, 1), res)
            durer = (tmp_datetime + timedelta).time()

        f = xbmcvfs.File(pathEnregistrement + '/' + heureDebut + '.py','w')
        f = f.write('''from subprocess import Popen, PIPE
command = '"'''+ffmpeg+'''" -y -i "'''+header+''' -t '''+str(durer)+''' "'''+currentPath+'''/'''+titre+'''.mkv"'
proc = Popen(command, shell=True, stdout=PIPE)
p_status = proc.wait()
f = open("'''+currentPath+'''/test.txt",'w')
f.write('Finit avec code erreur ' + str(p_status))
f.close()''')
        oDialog = dialog().VSinfo('Redemarrer Kodi pour prendre en compte la planification','Vstream',10)
        oGui.setEndOfDirectory()
