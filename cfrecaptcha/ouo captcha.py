import requests
from io import BytesIO
from PIL import Image
import re
import urllib.request
import urllib.parse
import CloudflareScraper

urlOuo = input('Url ouo : ')
if not '/fbc/' in urlOuo:
    urlOuo = urlOuo.replace('io/','io/fbc/').replace('press/','press/fbc/')
print(urlOuo)

UA = ''
head = {'Host': 'www.google.com',
'User-Agent': UA,
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'DNT': '1',
'Connection': 'keep-alive',
'Referer': urlOuo,
'Upgrade-Insecure-Requests': '1',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'TE': 'Trailers'}
    
def ResolveCaptcha(body):
    headers = {UA}

    #Recuperer le liens du payload
    captchaScrap = re.findall('value="8"><img class="fbc-imageselect-payload" src="(.+?)"',str(body))

    #Recuperer le texte du captcha
    text = re.search('<div class="rc-imageselect.+?">.+?<strong>(.+?)</strong>',str(body)).group(1)

    #Recuperer les 2 parametre necessaire pour acceder au captcha
    c = re.search('method="POST"><input type="hidden" name="c" value="(.+?)"',str(body)).group(1)
    k = re.search('k=(.+?)" alt=',str(body)).group(1)
    params = {
        "c": c,
        "k": k,
    }
    query_string = urllib.parse.urlencode( params )

    #Requete pour le captcha
    url = 'https://www.google.com'+str(captchaScrap[0]) + "?" + query_string
    print('\n' + url)

    headers = {
        'Host': 'www.google.com',
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length':str(len(params)),
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers'
        }

    #Recuperation et ouverture de l'image (uniquement utile pour fonctionner hors Kodi)
    file = BytesIO(requests.get(url).content)
    img = Image.open(file)
    img.show()

    #En attente de la saisie des resultat
    response = input('Select all images representing '+text+'. Type from 0 to 8 : ')

    #Format la reponse
    allNumber = [int(s) for s in response.split() if s.isdigit()]
    responseFinal = ""
    for rep in allNumber:
        responseFinal = responseFinal + '&response='+str(rep)


    #Requete pour valider le captcha
    r = requests.post(urlBase, data='c='+c+responseFinal, headers=headers)

    #Recupere le token du captcha
    return re.search('<textarea dir="ltr" readonly>(.+?)<',str(r.text)).group(1)

#1er connection pour recuperer la cle du site
s = requests.Session()
r = s.get(urlOuo)
key = re.search('sitekey: "(.+?)"',str(r.text)).group(1)

#Pour plus tard
OuoToken = re.search('<input name="_token" type="hidden" value="(.+?)">',str(r.text)).group(1)

#Requete vers les serveur de Google pour recuperer le captcha
urlBase  = 'https://www.google.com/recaptcha/api/fallback?k='+key+'&hl=fr&v=v1558333958099&t=5&ff=true'
r = requests.get(urlBase, headers=head)

gToken = ResolveCaptcha(r.text)
print('Token final de Recaptcha : '+gToken)
print('\n payload : '+'_token='+OuoToken+'&g-recaptcha-response='+gToken)

#Requete pour valider le captcha du coter de ouo
url = urlOuo.replace('/fbc/','/go/')
print(url.split('/')[2])
params = '_token='+OuoToken+'&g-recaptcha-response='+gToken
headers = {
    'Host': url.split('/')[2],
    'User-Agent': UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': urlOuo,
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length':str(len(params)),
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
    }

r = requests.post(url,data=params, headers=headers,cookies=s.cookies)
print(r.headers)
try:
    if r.headers['Content-Encoding'] == 'br':
        import brotli
        content = brotli.decompress(r.content)
    else:
        content = r.text
except KeyError:
    content = r.text    

print(content)
#Recuperer le token et la derniere url de ouo
final = re.search('<form method="POST" action="(.+?)" accept-charset="UTF-8"><input name="_token" type="hidden" value="(.+?)">',str(content))

#Derniere requete pour recuperer le liens du hoster
r = requests.post(final.group(1),data='_token='+final.group(2), headers=headers,cookies=s.cookies)
print("Url final : " + r.url)
