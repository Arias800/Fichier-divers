#Pour lancer la boucle tr = Threading()
class Threading(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        oGui = cGui()
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sTitle = oInputParameterHandler.getValue('sMovieTitle')
        DebutEnregistrement = 0
        DebutEnregistrement = oGui.showKeyBoard()
        while True:
            heure = datetime.now().strftime('%H:%M')
            if DebutEnregistrement == heure:
                currentPath = ADDON.getSetting('pathEnregistrement')
                #currentPath = 'D:/film/' + str(Titre)
                durer = oGui.showKeyBoard()
                command = ADDON.getSetting('pathFFMPEG')+' -y -i "'+sUrl+'" -c:v libx264 -preset slow -crf 22 -c:a copy -t '+durer+' "'+currentPath+'/enregistrement.mkv"'
                VSlog(command)
                proc = Popen(command, shell=True, stdout=PIPE)
                dialog().VSinfo('L\'enregistrement de '+sTitle+' a commencer', "vStream", 15)
                p_status = proc.wait()
                if p_status == 0:
                    dialog().VSinfo('Enregistrement finis sans probleme')
                else:
                    dialog().VSinfo('Une erreur est survenu code erreur ' + str(p_status))
                VSlog("Command exit status/return code : " + str(p_status))
                return
            else:
                time.sleep(1)
