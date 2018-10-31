from subprocess import Popen, PIPE
command = '"FFMPEG_CHEMIN" -y -i "URL_CHAINE" -c:v libx264 -preset slow -crf 22 -c:a copy -t TEMPS_ENREGISTREMENT "ENREGISTREMENT_CHEMIN/enregistrement.mkv"'
proc = Popen(command, shell=True, stdout=PIPE)
p_status = proc.wait()
f = open("ENREGISTREMENT_CHEMIN/test.txt",'w')
f.write('Finit avec code erreur ' + str(p_status))
f.close()
