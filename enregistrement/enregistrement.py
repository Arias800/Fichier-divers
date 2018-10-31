from resources.lib.gui.gui import cGui
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog

SITE_IDENTIFIER = 'Enregistrement'
SITE_NAME = 'enregistrement'

class cEnregistremement:

    def programmation_enregistrement(self, sUrl):
        oGui = cGui()
        ADDON = addon()
        pathEnregistrement = ADDON.getSetting('path_enregistrement_programmation')
        currentPath = ADDON.getSetting('path_enregistrement').replace('\\','/')
        ffmpeg = ADDON.getSetting('path_ffmpeg').replace('\\','/')

        heureDebut = oGui.showKeyBoard("Heure du debut d\'enregistrement au format Heure-Minute ")
        durer = oGui.showKeyBoard("Durer de l\'enregistrement au format Heure:Minute:Seconde")

        f = open(pathEnregistrement + heureDebut + '.py','w')
        f.write('''from subprocess import Popen, PIPE
command = '"'''+ffmpeg+'''" -y -i "'''+sUrl+'''" -c:v copy -c:a copy -t '''+durer+''' "'''+currentPath+'''/enregistrement.mkv"'
proc = Popen(command, shell=True, stdout=PIPE)
p_status = proc.wait()
f = open("'''+currentPath+'''/test.txt",'w')
f.write('Finit avec code erreur ' + str(p_status))
f.close()''')
        oDialog = dialog().VSinfo('Redemarrer Kodi pour prendre en compte la planification','Vstream',10)
        oGui.setEndOfDirectory()
