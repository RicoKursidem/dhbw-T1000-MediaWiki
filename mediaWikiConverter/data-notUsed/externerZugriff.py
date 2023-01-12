import requests
from requests.sessions import Session
from botInfo import getInfo as Bot_getInfo

MEDIAWIKI_URL = "https://de.wiki.server.azo/api.php"


def connectToMediaWiki(login_Info):
    try:
        S = requests.Session()
        PARAMS_1 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }
        #TODO: verify per ssl einrichten
        R = S.get(url=MEDIAWIKI_URL, params=PARAMS_1, verify=False)
        DATA = R.json()

        LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]
    except Exception as e:
        print(str(e) + "\n0")
        return None

    # Step 2: Send a POST request to login. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    try:
        PARAMS_2 = {
            "action": "login",
            "lgname": login_Info[0],
            "lgpassword": login_Info[1],
            "format": "json",
            "lgtoken": LOGIN_TOKEN
        }

        R = S.post(MEDIAWIKI_URL, data=PARAMS_2)
    except Exception as e:
        print(str(e) + "\n1")
        return None
    try:
        PARAMS_3 = {
            "action": "query",
            "meta":"tokens",
            "format":"json"
        }

        R = S.get(url=MEDIAWIKI_URL, params=PARAMS_3)
        DATA = R.json()

        CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]
    except Exception as e:
        print(str(e) + "\n2")
        return None

    return [S, CSRF_TOKEN]

def overwriteWikiSite(pSession,CSRFToken, pSiteTitle, pText):
    PARAMS = {
        "action": "edit",
        "format":"json",
        "title": pSiteTitle,
        "text": pText,
        "token": CSRFToken
    }
    R = pSession.post(MEDIAWIKI_URL, data=PARAMS)
    print(R.json())

def readTxt():
    return open("OUT_FILE.txt", "r", encoding="utf8")


#Test Code. Writes the Page "Test" with the "inhalt.txt"
print(" ")
aSessionItems = connectToMediaWiki(Bot_getInfo())
if aSessionItems != None:
#index.php/Test seite löschen
    print(aSessionItems)
    text = readTxt().read()
    #print(text)
    overwriteWikiSite(aSessionItems[0], aSessionItems[1], "Test", text)
else:
    print("Connection Failture")