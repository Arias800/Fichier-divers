# coding=utf-8
# https://github.com/Kodi-vStream/venom-xbmc-addons
#
#alors la j'ai pas le courage
from __future__ import division

import re,os
import urllib.request
import urllib.error
import urllib.parse
import time, json, random
from bs4 import BeautifulSoup

Mode_Debug = True

#---------------------------------------------------------
#Gros probleme, mais qui a l'air de passer
#Le headers "Cookie" apparait 2 fois, il faudrait lire la precedente valeur
#la supprimer et remettre la nouvelle avec les 2 cookies
#Non conforme au protocole, mais ca marche (pour le moment)
#-----------------------------------------------------------

#Cookie path
#C:\Users\BRIX\AppData\Roaming\Kodi\userdata\addon_data\plugin.video.vstream\

#Light method
#Ne marche que si meme user-agent
    # req = urllib.request.Request(sUrl,None,headers)
    # try:
        # response = urllib.request.urlopen(req)
        # sHtmlContent = response.read()
        # response.close()

    # except urllib.error.HTTPError as e:

        # if e.code == 503:
            # if CloudflareBypass().check(e.headers):
                # cookies = e.headers['Set-Cookie']
                # cookies = cookies.split(';')[0]
                # sHtmlContent = CloudflareBypass().GetHtml(sUrl,e.read(),cookies)

#Heavy method
# sHtmlContent = CloudflareBypass().GetHtml(sUrl)

PathCache = dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')+'/Cookie'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'


def GetPrevchar(string, pos):
    if (pos - 1) < 0:
        return ''
    return string[pos-1]

#Fonction to return only one parameter from a string with correct closed [] () "" and ''
def GetItemAlone(string,separator = ' '):

    l = len(string) - 1
    ret = ''

    i = -1
    p = 0 #parenthese
    a = 0 #accolade
    b = 0 #bracket
    c1 = 0 #chain with "
    c2 = 0 #chain with '
    n = False
    last_char = ''

    s = False

    while (i < l):
        i += 1
        ch = string[i]
        ret = ret + ch
        n = False

        #Return if the is complete and before the char wanted but not if it's the first one
        if (ch in separator)  and not p and not a and not b and  not c1 and not c2 and not n and (i>0):
            return ret[:-1]

        #Skip empty space
        if (ch.isspace()):
            continue

        if ch == '"' and not GetPrevchar(string,i) == '\\' and not c2:
            c1 = 1 - c1
        if ch == "'" and not GetPrevchar(string,i) == '\\' and not c1:
            c2 = 1 - c2

        if not c1 and not c2:
            if ch == '(':
                p += 1
            elif ch == ')':
                p -= 1
            elif ch == '{':
                a += 1
            elif ch == '}':
                a -= 1
            elif ch == '[':
                b += 1
            elif ch == ']':
                b -= 1

            if ch == '.' and not ((last_char in '0123456789') or (string[i+1] in '0123456789')):
                n = True

        #return if the chain is complete but with the char wanted
        if (ch in separator) and not p and not a and not b and  not c1 and not c2 and not n and (i>0):
            return ret

        last_char = ch

    return ret

def solvecharcode(chain,t):

    v = chain.find('t.charCodeAt') + 12
    dat = GetItemAlone(chain[v:],')')
    #print ('chain : ' + str(dat) )
    r = parseInt(dat)
    chain = chain.replace('t.charCodeAt' + dat, str(ord(t[int(r)])) )

    return chain

def parseIntOld(chain):

    chain = chain.replace(' ','')
    chain = re.sub(r'!!\[\]','1',chain) # !![] = 1
    chain = re.sub(r'\(!\+\[\]','(1',chain)  #si le bloc commence par !+[] >> +1
    chain = re.sub(r'(\([^()]+)\+\[\]\)','(\\1)*10)',chain)  # si le bloc fini par +[] >> *10

    #bidouilles a optimiser non geree encore par regex
    chain = re.sub(r'\(\+\[\]\)','0',chain)
    if chain.startswith('!+[]'):
        chain = chain.replace('!+[]','1')

    return eval(chain)

def checkpart(s,sens):
    number = 0
    p = 0
    if sens == 1:
        pos = 0
    else:
        pos = len(s) - 1

    try:
        while (1):
            c = s[pos]

            if ((c == '(') and (sens == 1)) or ((c == ')') and (sens == -1)):
                p = p + 1
            if ((c == ')') and (sens == 1)) or ((c == '(') and (sens == -1)):
                p = p - 1
            if (c == '+') and (p == 0) and (number > 1):
                break

            number +=1
            pos=pos + sens
    except:

        pass


    if sens == 1:
        return s[:number],number
    else:
        return s[-number:],number

def parseInt(s):

    offset=1 if s[0]=='+' else 0
    chain = s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]
    chain = chain.replace('(+str','(str')

    if '/' in chain:

        ##print('division ok ')
        ##print('avant ' + chain)

        val = chain.split('/')
        gauche,sizeg = checkpart(val[0],-1)
        droite,sized = checkpart(val[1],1)
        sign = ''

        chain = droite.replace(droite,'')

        if droite.startswith('+') or droite.startswith('-'):
            sign = droite[0]
            droite = droite[1:]

        ##print('debug1 ' + str(gauche))
        ##print('debug2 ' + str(droite))

        gg = eval(gauche)
        dd = eval(droite)

        chain = val[0][:-sizeg] + str(gg) + '/' + str(dd) + val[1][sized:]

        ##print('apres ' + chain)

    val = float( eval(chain))

    return val

def CheckIfActive(data):
    if 'Checking your browser before accessing' in str(data):
    #if ( "URL=/cdn-cgi/" in head.get("Refresh", "") and head.get("Server", "") == "cloudflare-nginx" ):
        return True
    return False

def showInfo(sTitle, sDescription, iSeconds=0):
    if (iSeconds == 0):
        iSeconds = 1000
    else:
        iSeconds = iSeconds * 1000
    #xbmc.executebuiltin("Notification(%s,%s,%s)" % (str(sTitle), (str(sDescription)), iSeconds))

class NoRedirection(urllib.request.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response

    https_response = http_response

class CloudflareBypass(object):

    def __init__(self):
        self.state = False
        self.HttpReponse = None
        self.Memorised_Headers = None
        self.Memorised_PostData = None
        self.Memorised_Cookies = None
        self.Header = None
        self.RedirectionUrl = None

    #Return param for head
    def GetHeadercookie(self,url):
        #urllib.parse.quote_plus()
        Domain = re.sub(r'https*:\/\/([^/]+)(\/*.*)','\\1',url)
        cook = GestionCookie().Readcookie(Domain.replace('.','_'))
        if cook == '':
            return ''

        return '|' + urllib.urlencode({'User-Agent':UA,'Cookie': cook })

    def ParseCookies(self,data):
        list = []

        sPattern = '(?:^|,) *([^;,]+?)=([^;,\/]+?)(?:$|;)'
        aResult = re.findall(sPattern,data)
        ##print(str(aResult))
        if (aResult):
            for cook in aResult:
                if 'deleted' in cook[1]:
                    continue
                list.append((cook[0],cook[1]))
                #cookies = cookies + cook[0] + '=' + cook[1]+ ';'

        ##print(str(list))

        return list

    def SetHeader(self):
        head=[]
        if not (self.Memorised_Headers):
            head.append(('User-Agent', UA))
            head.append(('Host' , self.host))
            head.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
            head.append(('Referer', self.url))
            head.append(('Content-Type', 'text/html; charset=utf-8'))
        else:
            for i in self.Memorised_Headers:
                #Remove cookies
                if ('Cookie' in i):
                    continue

        return head

    def GetResponse(self,htmlcontent):
        #print(htmlcontent)
        hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)','\\1',self.url)
        domain = re.sub(r'https*:\/\/','',hostComplet)

        #truc cache
        rq = re.search('<div style="display:none;visibility:hidden;" id="(.*?)">(.*?)<\/div>', str(htmlcontent),re.MULTILINE | re.DOTALL)
        id = rq.group(1)
        val = rq.group(2)
        #print (str(id) + ' ' + str(val))

        htmlcontent = re.sub(
            r'function\(p\){var p = eval\(eval\(atob\(".*?"\)\+\(undefined\+""\)\[1\]\+\(true\+""\)\[0\]\+\(\+\(\+!\+\[\]\+\[\+!\+\[\]\]\+\(!!\[\]\+\[\]\)\[!\+\[\]\+!\+\[\]\+!\+\[\]\]\+\[!\+\[\]\+!\+\[\]\]\+\[\+\[\]\]\)\+\[\]\)\[\+!\+\[\]\]\+\(false\+\[0\]\+String\)\[20\]\+\(true\+""\)\[3\]\+\(true\+""\)\[0\]\+"Element"\+\(\+\[\]\+Boolean\)\[10\]\+\(NaN\+\[Infinity\]\)\[10\]\+"Id\("\+\(\+\(20\)\)\["to"\+String\["name"\]\]\(21\)\+"\)."\+atob\(".*?"\)\)\); return \+\(p\)}\(\);',
            "{};".format(rq.group(2)),
            str(htmlcontent)
        )

        line1 = re.findall('var s,t,o,p,b,r,e,a,k,i,n,g,f, (.+?)={"(.+?)":\+*(.+?)};',str(htmlcontent))

        varname = line1[0][0] + '.' + line1[0][1]
        calcul = parseInt(line1[0][2])

        t = domain

        js = htmlcontent
        #Cleaning
        js = re.sub(r"a\.value = ((.+).toFixed\(10\))?", r"\1", js)
        #js = re.sub(r"\s{3,}[a-z](?: = |\.).+", "", js).replace("t.length", str(len(domain)))
        js = js.replace('; 121', '')
        js = js.replace('function(p){return eval((true+"")[0]+"."+([]["fill"]+"")[3]+(+(101))["to"+String["name"]](21)[1]+(false+"")[1]+(true+"")[1]+Function("return escape")()(("")["italics"]())[2]+(true+[]["fill"])[10]+(undefined+"")[2]+(true+"")[3]+(+[]+Array)[10]+(true+"")[0]+"("+p+")")}', 't.charCodeAt')
        js = re.sub(r"[\n\\']", "", js)
        js = solvecharcode(js,t)
        htmlcontent = js

        AllLines = re.findall(';' + varname + '([*\-+])=([^;]+)',str(htmlcontent))
        #print ('\nFirst line : ' + str(line1[0][2]) )

        for aEntry in AllLines:
            #print ('\nother lines : ' + str(aEntry))
            calcul = eval( format(calcul,'.17g') + str(aEntry[0]) + format(parseInt(aEntry[1]),'.17g'))
            ##print(">>>>>>>>>>>>>>>>: " + format(calcul,'.17g')+ '\n')

        rep = calcul + len(domain)
        ret = format(rep,'.10f')

        return (str(ret))

    def GetReponseInfo(self):
        return self.RedirectionUrl, self.Header

    def GetHtml(self,url,htmlcontent = '',cookies = '',postdata = None,Gived_headers = ''):

        #Memorise headers
        self.Memorised_Headers = Gived_headers

        #Memorise postdata
        self.Memorised_PostData = postdata

        #Memorise cookie
        self.Memorised_Cookies = cookies
        #print(cookies)

        #cookies in headers ?
        if Gived_headers != '':
            if Gived_headers.get('Cookie',None):
                if cookies:
                    self.Memorised_Cookies = cookies + '; ' + Gived_headers.get('Cookie')
                else:
                    self.Memorised_Cookies = Gived_headers['Cookie']

        #For debug
        if (Mode_Debug):
            print('Headers present ' + str(Gived_headers))
            print('url ' + url)
            print('Content : ' + str(htmlcontent))
            if (htmlcontent):
                print('code html ok')
            print('cookies passés' + self.Memorised_Cookies)
            print('post data :' + str(postdata))

        self.hostComplet = re.sub(r'(https*:\/\/[^/]+)(\/*.*)','\\1',url)
        self.host = re.sub(r'https*:\/\/','',self.hostComplet)
        self.url = url

        try:
            with open(PathCache +'/'+self.host.replace('.','_')+'.txt','r') as f:
                cookieMem = f.read()
                ##print('Cookie Deja Present')
        except FileNotFoundError:
            f = open(PathCache +'/'+self.host.replace('.','_')+'.txt','w')
            f.close()
            cookieMem = ''

        ##print(PathCache +'/'+self.host.replace('.','_')+'.txt')
        if not (cookieMem == ''):
            ##print('cookies present sur disque :' + cookieMem )
            if not (self.Memorised_Cookies):
                cookies = cookieMem
            else:
                cookies = self.Memorised_Cookies + '; ' + cookieMem

        #Max 3 loop
        loop = 3
        while (loop > 0):
            loop -= 1

            #Redirection possible ?
            if (True):
                opener = urllib.request.build_opener(NoRedirection)
            else:
                opener = urllib.request.build_opener()

            opener.addheaders = self.SetHeader()

            if ('cf_clearance' not in cookies) and htmlcontent and ('__cfduid=' in cookies):

                ##print("******  Decodage *****")
                #print(htmlcontent)
                #recuperation parametres
                hash = re.findall('<input type="hidden" name="jschl_vc" value="(.+?)"\/>',str(htmlcontent))[0]
                passe = re.findall('<input type="hidden" name="pass" value="(.+?)"\/>',str(htmlcontent))[0]
                s = re.findall('<input type="hidden" name="s" value="([^"]+)"',str(htmlcontent), re.DOTALL)[0]

                #calcul de la reponse
                rep = self.GetResponse(htmlcontent)

                #Temporisation
                #showInfo("Information", 'Decodage protection CloudFlare' , 5)
                time.sleep(8)

                url = self.hostComplet + '/cdn-cgi/l/chk_jschl?s=' + s + '&jschl_vc='+ hash +'&pass=' + passe + '&jschl_answer=' + rep

                #No post data here
                postdata = None

                #To avoid captcha
                if not "'Accept'" in str(opener.addheaders):
                    opener.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))
                if not 'Host' in str(opener.addheaders):
                    opener.addheaders.append(('Host',domain))
                #opener.addheaders.append(('Connection', 'keep-alive'))
                #opener.addheaders.append(('Accept-Encoding', 'gzip, deflate, br'))
                #opener.addheaders.append(('Cache-Control', 'max-age=0'))

            #Add cookies
            if cookies:
                opener.addheaders.append (('Cookie', cookies))

            if not 'Referer' in str(opener.addheaders):
                opener.addheaders.append(('Referer', self.url))
            #if not 'Accept' in str(opener.addheaders):
            #    opener.addheaders.append(('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'))

            #print("Url demandee " + str(url) )
            #print(str(opener.addheaders))

            if not url.startswith('http'):
                url = self.hostComplet+ url
            try:
                if postdata:
                    self.HttpReponse = opener.open(url,postdata)
                else:
                    self.HttpReponse = opener.open(url)
                htmlcontent = self.HttpReponse.read()
                self.Header = self.HttpReponse.headers
                print(self.Header)
                self.RedirectionUrl = self.HttpReponse.geturl()
                self.HttpReponse.close()
            except urllib.error.HTTPError as e:
                ##print("Error " + str(e.code))
                htmlcontent = e.read()
                self.Header = e.headers
                self.RedirectionUrl = e.geturl()

            url = self.RedirectionUrl
            postdata = self.Memorised_PostData

            #For debug
            if (Mode_Debug):
                print("Headers send " + str(opener.addheaders))
                print("cookie send " + str(cookies))
                print("header recu " + str(self.Header))
                print("Url obtenue " + str(self.RedirectionUrl))

            if 'Please complete the security check' in str(htmlcontent):
                fh = open('d:\\test.txt', "w")
                fh.write(htmlcontent)
                fh.close()
                print("Probleme protection Cloudflare : Protection captcha")
                #showInfo("Erreur", 'Probleme CloudFlare, pls Retry' , 5)
                return ''

            if not CheckIfActive(htmlcontent):
                # ok no more protection
                print("Page ok")
                #need to save cookies ?
                if not cookieMem:
                    with open(PathCache +'/'+self.host.replace('.','_')+'.txt','w') as f:
                        f.write(cookies)

                #fh = open('c:\\test.txt', "w")
                #fh.write(htmlcontent)
                #fh.close()

                url2 = self.Header.get('Location','')
                if url2:
                    url = url2
                else:
                    return htmlcontent

            else:

                #Arf, problem, cookies not working, delete them
                if cookieMem:
                    print('Cookies Out of date')
                    os.remove (PathCache +'/'+self.host.replace('.','_')+'.txt')
                    cookieMem = ''
                    #one more loop, and reset all cookies, event only cf_clearance is needed
                    loop += 1
                    cookies = self.Memorised_Cookies

            #Get new cookies
            if 'Set-Cookie' in self.Header:
                cookies2 = str(self.Header.get('Set-Cookie'))

                listcookie = self.ParseCookies(cookies2)
                listcookie2 = self.ParseCookies(cookies)

                cookies = ""

                #New cookies
                for a,b in listcookie:
                    if len(cookies) > 0:
                        cookies = cookies + '; '
                    cookies = cookies + str(a) + '=' + str(b)

                #old cookies only is needed
                for a,b in listcookie2:
                    if not str(a) in cookies:
                        if len(cookies) > 0:
                            cookies = cookies + '; '
                        cookies = cookies + str(a) + '=' + str(b)


        print("Probleme protection Cloudflare : Cookies manquants")
        return ''
