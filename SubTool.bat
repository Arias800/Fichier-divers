@ECHO OFF
@title SubTool
chcp 65001
:Begin
CLS
@echo ┌───────────────MENU PRINCIPAL───────────────█
@echo │Aide contient des informations importantes. █
@echo │Choix :                                     █
@echo │ 0. Aide                                    █
@echo │ 1. Extrait les sous-titres (batch)         █
@echo │ 2. Convertir sous-titres en .srt (batch)   █
@echo │ 3. Ajouter les sous-titres au mkv(batch)   █
@echo │ 4. Quitter                                 █
@echo └▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█

set /p choice="Choississez l'option voulue : "
IF %choice% == 0 GOTO Aide
IF %choice% == 1 GOTO ExtractSub
IF %choice% == 2 GOTO ConvertSub
IF %choice% == 3 GOTO MergeSub
IF %choice% == 4 GOTO End


:ExtractSub
set /p format="Type de fichier qui comporte les sous-titres ? "
for %%i in (*.%format%) do (
	ffmpeg -i "%%i" -map 0:s:0  "%%~ni.srt"
)|| pause
GOTO Begin


:ConvertSub
set /p format="Format des sous-titres a convertir ? "
for %%i in (*.%format%) do (
	ffmpeg -i "%%i" -c:s srt  "%%~ni.srt"
)|| pause
GOTO Begin


:MergeSub
IF not exist "Final" (mkdir "Final")

if exist *.ass set format=ass
if exist *.srt set format=srt

echo "Format choisit :" %format%

for %%i in (*.mkv) do (
	ffmpeg -y -i "%%i" -i "%%~ni."%format% -c:v copy -c:a copy -c:s copy  -map 0:v -map 0:a -map 1 -metadata:s:s:0 language=fre "Final/%%~ni.mkv"
)|| pause

GOTO Begin


:Aide
echo Ce script nécessite FFMPEG, ce dernier doit être inscrit dans les variables d'environnement.
echo.
echo Pour ajouter les sous-titres dans les vidéos, il faut que les noms des fichiers sois identiques.
echo.
echo Puisque que c'est là-dessus que le script va s'appuyer pour detecter les bons fichiers.
echo.
pause
GOTO Begin

:End
