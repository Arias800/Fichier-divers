import time, os
from resources.lib.comaddon import progress, addon, xbmc, xbmcgui, VSlog, dialog
from datetime import datetime

def service():
    ADDON = addon()
    enregistrementIsActif = ADDON.getSetting('enregistrement_activer')
    if enregistrementIsActif == 'false':
        return
    Debutpath  = os.path.dirname(os.path.realpath(__file__)).replace('\\','/').replace('addons','userdata').replace('plugin.video.vstream','addon_data')
    path = Debutpath + '/plugin.video.vstream/Enregistrement/'
    ADDON.setSetting('path_enregistrement_programmation', path)
    ListeEnregistrement = os.listdir(path)
    EnregistrementEnCours = False
    monitor = xbmc.Monitor()

    while not monitor.abortRequested() and not EnregistrementEnCours == True:
        if monitor.waitForAbort(1):
            break

        heure = datetime.now().strftime('%H-%M') + '.py'
        if heure in str(ListeEnregistrement):
            heure = path + heure
            VSlog(heure)
            xbmc.executebuiltin("System.Exec("+(heure)+")")
            EnregistrementEnCours = True

if __name__ == '__main__':
    service()
