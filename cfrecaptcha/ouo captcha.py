import requests
from io import BytesIO
from PIL import Image
import re
import urllib.request
import urllib.parse

def ResolveCaptcha(body):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}
    captchaScrap = re.findall('value="8"><img class="fbc-imageselect-payload" src="(.+?)"',str(body))
    text = re.search('<div class="rc-imageselect.+?">.+?<strong>(.+?)</strong>',str(body)).group(1)
    c = re.search('method="POST"><input type="hidden" name="c" value="(.+?)"',str(body)).group(1)
    print(c)
    k = re.search('k=(.+?)" alt=',str(body)).group(1)
    print(k)
    params = {
        "c": c,
        "k": k,
    }
    query_string = urllib.parse.urlencode( params )
    url = 'https://www.google.com'+str(captchaScrap[0]) + "?" + query_string
    print(url)

    file = BytesIO(requests.get(url, headers=headers).content)
    img = Image.open(file)
    img.show()
    response = input('Select all images representing '+text+'. Type from 0 to 8 : ')
    allNumber = [int(s) for s in response.split() if s.isdigit()]
    responseFinal = ""
    for rep in allNumber:
        responseFinal = responseFinal + '&response='+str(rep)

    print('c='+c+responseFinal)

    headers = {
        'Host': 'www.google.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
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

    r = requests.post(urlBase, data='c='+c+responseFinal, headers=headers)
    return re.search('<textarea dir="ltr" readonly>(.+?)<',str(r.text)).group(1)


urlBase  = 'https://www.google.com/recaptcha/api/fallback?k=6LegWQETAAAAAIIaaAhEnrkimbuOF5QJb0ZiYEK7&hl=fr&v=v1558333958099&t=5&ff=true'

head = {'Host': 'www.google.com',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'DNT': '1',
'Connection': 'keep-alive',
'Referer': 'https://ouo.io/fbc/GJRHYi',
'Cookie': '1P_JAR=2019-06-03-08; NID=184=uJrYqzJzgGe6RZmX8gY_dsl5Xe3EmEh9vAY1eWrtn4nSkj08E-JzZKtuNg2apnaKtAWVi1PV9bMhOVd-krJgfvUD4e-QVV-yMi2-rEEdj5wXOlwj7wSzj0rWlGJydEToe_vYNi9_Z8miOkZkB4-DaOORlha2ZesXwq3P7NvFsGkgj9QDFxHCd45MVO0V3pzx9YEBhmnT_M06NBfxG6kYggArzpfE; CONSENT=YES+FR.fr+20161218-19-0; ANID=OPT_OUT; SID=egc604rtjznXJCIq9vFtTP2cgoYU2JcGOM-viIUjRSLtJEJdWWaxQi_yrZsK67Nu4gXhuA.; HSID=ApkBOVVTshWmTv3ZP; SSID=AopFjfL6iHejpKAZ7; APISID=INXpDeSCPvnjd-Up/A3G4ncpBAY6ITM29W; SAPISID=GfT_-0mPCmAOD2s2/AzPnmL9qR6YSCm8s9; SIDCC=AN0-TYutJx9MkbvWQZRS9-cFmHGVJDqzVDVGlAQ8SEVIP6sXCN0TRsR4r8K1XaJfP7jI_trtIKA; DV=M3mD2hVj1HUTQP_f7OZE3e5NYibHsRY',
'Upgrade-Insecure-Requests': '1',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache',
'TE': 'Trailers'}
r = requests.get(urlBase, headers=head)
token = ResolveCaptcha(r.text)
print('Token final de Recaptcha : '+token)
