from resources.lib.gui.gui import cGui
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog

SITE_IDENTIFIER = 'Enregistrement'
SITE_NAME = 'enregistrement'


class cEnregistremement:

    def programmation_enregistrement(self, sUrl):
        oGui = cGui()
        ADDON = addon()
        if 'firstonetv' in sUrl or 'bouygtel' in sUrl:
            sUrl = sUrl.replace('|Referer=',' -headers "Referer:').replace('&User-Agent=Mozilla/5.0+(X11;+Linux+i686)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Ubuntu+Chromium/48.0.2564.116+Chrome/48.0.2564.116+Safari/537.36&X-Requested-With=ShockwaveFlash/28.0.0.137&Origin=https://www.firstonetv.net',' -headers "User-Agent:Mozilla/5.0+(X11;+Linux+i686)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Ubuntu+Chromium/48.0.2564.116+Chrome/48.0.2564.116+Safari/537.36" -headers "X-Requested-With:ShockwaveFlash/28.0.0.137" -headers "Origin:https://www.firstonetv.net" -c:v copy -c:a copy')
            header = sUrl
        else:
            header = sUrl+'" -c:v copy -c:a copy'

        pathEnregistrement = ADDON.getSetting('path_enregistrement_programmation')
        currentPath = ADDON.getSetting('path_enregistrement').replace('\\','/')
        ffmpeg = ADDON.getSetting('path_ffmpeg').replace('\\','/')

        heureDebut = oGui.showKeyBoard("Heure du debut d\'enregistrement au format Heure-Minute ")
        durer = oGui.showKeyBoard("Durer de l\'enregistrement au format Heure:Minute:Seconde")
        titre = oGui.showKeyBoard("Titre de l\'enregistrement")

        f = open(pathEnregistrement + heureDebut + '.py','w')
        f.write('''from subprocess import Popen, PIPE
command = '"'''+ffmpeg+'''" -y -i "'''+header+''' -t '''+durer+''' "'''+currentPath+'''/'''+titre+'''.mkv"'
proc = Popen(command, shell=True, stdout=PIPE)
p_status = proc.wait()
f = open("'''+currentPath+'''/test.txt",'w')
f.write('Finit avec code erreur ' + str(p_status))
f.close()''')
        oDialog = dialog().VSinfo('Redemarrer Kodi pour prendre en compte la planification','Vstream',10)
        oGui.setEndOfDirectory()
