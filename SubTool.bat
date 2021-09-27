@ECHO OFF
@title SubTool
chcp 65001
:Begin
CLS
@echo ┌───────────────MENU PRINCIPAL────────────────█
@echo │Aide contient des informations importantes.  █
@echo │Choix :                                      █
@echo │ 0. Aide                                     █
@echo │ 1. Extrait les sous-titres (batch)          █
@echo │ 2. Convertir sous-titres en .srt (batch)    █
@echo │ 3. Ajouter les sous-titres au mkv(batch)    █
@echo │ 4. Supprimer une piste de sous-titres(batch)█
@echo │ 5. Quitter                                  █
@echo └▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

set /p choice="Choississez l'option voulue : "
IF %choice% == 0 GOTO Aide
IF %choice% == 1 GOTO ExtractSub
IF %choice% == 2 GOTO ConvertSub
IF %choice% == 3 GOTO MergeSub
IF %choice% == 4 GOTO RemoveTrack
IF %choice% == 5 GOTO End


:ExtractSub
if exist *.mp4 set format=mp4
if exist *.mkv set format=mkv

for %%i in (*.%format%) do (
    ffmpeg -i "%%i" -map 0:s:0  "%%~ni.srt"
)|| pause
GOTO Begin


:ConvertSub
if exist *.vtt set format=vtt

for %%i in (*.%format%) do (
    ffmpeg -i "%%i" -c:s srt  "%%~ni.srt"
)|| pause
GOTO Begin


:MergeSub
IF not exist "Final" (mkdir "Final")
if exist *.mp4 set formatVid=mp4
if exist *.mkv set formatVid=mkv

if exist *.ass set format=ass
if exist *.srt set format=srt

for %%i in (*.mkv) do (
    ffmpeg -y -i "%%i" -i "%%~ni."%format% -c:v copy -c:a copy -c:s copy  -map 0:v -map 0:a -map 1 -metadata:s:s:0 language=fre "Final/%%~ni."%formatVid%
)|| pause

GOTO Begin

:RemoveTrack
IF not exist "Final" (mkdir "Final")
set /p Num="Numéro de la piste a supprimer ? "
if exist *.mp4 set format=mp4
if exist *.mkv set format=mkv

for %%i in (*.%format%) do (
    ffmpeg -i "%%i" -map 0 -map -0:s:%Num% -c copy "Final/%%~ni."%format%
)|| pause
GOTO Begin


:Aide
echo Ce script nécessite FFMPEG, ce dernier doit être inscrit dans les variables d'environnement.
echo.
echo Pour ajouter les sous-titres dans les vidéos, il faut que les noms des fichiers sois identiques.
echo Puisque que c'est là-dessus que le script va s'appuyer pour detecter les bons fichiers.
echo.
echo Pour supprimer une piste de sous-titres, le numéro 0 est pris en compte.
echo Pour retirer la piste 1, il faut taper 0. Pour la 2, il faut taper 1...
echo.
pause
GOTO Begin
:End
