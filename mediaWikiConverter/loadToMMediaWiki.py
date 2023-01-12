import requests
from requests.sessions import Session
from botInfo import getInfo as Bot_getInfo
    
def main():
    input_title = "Test"
    input_language = "de"
    #input_title = input("Title: ")
    #input_language = input("Language('de' or 'en'): ")
    #while input_language != "de" and input_language != "en":
    #    print("Language can only be 'en' or 'de'")
    #    input_language = input("Language(de/en): ")
    loadTOMediaWiki(input_language, input_title)

def getMediaWikiURL(language):
    return "https://" + language + ".wiki.server.azo/api.php"

def connectToMediaWiki(mediawiki_url, login_Info):
    session = requests.Session()
    params_1 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }
    #TODO: verify per ssl einrichten
    #https://de.wiki.server.azo/api.php?action=query&meta=tokens&type=login&format=json
    response = session.get(url=mediawiki_url, params=params_1, verify=False)
    print(response)
    if response.status_code != 200:
        return None
    data = response.json()
    print(data)
    login_token = data["query"]["tokens"]["logintoken"]

    # Step 2: Send a POST request to login. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    try:
        params_2 = {
            "action": "login",
            "lgname": login_Info[0],
            "lgpassword": login_Info[1],
            "format": "json",
            "lgtoken": login_token,
        }

        response = session.post(mediawiki_url, data=params_2)
    except Exception as e:
        print(str(e) + "   ---   1")
        return None
    try:
        params_3 = {
            "action": "query",
            "meta":"tokens",
            "format":"json"
        }

        response = session.get(url=mediawiki_url, params=params_3)
        DATA = response.json()

        csrf_token = DATA["query"]["tokens"]["csrftoken"]
    except Exception as e:
        print(str(e) + "   ---   2")
        return None

    return [session, csrf_token]

def overwriteWikiSite(session, csrf_token, mediawiki_url, pSiteTitle, pText):
    PARAMS = {
        "action": "edit",
        "format":"json",
        "title": pSiteTitle,
        "text": pText,
        "token": csrf_token
    }
    response = session.post(mediawiki_url, data=PARAMS)
    print(response.json())

def readTxt():
    return open("temp_output_file.txt", "r", encoding="utf8")

def fixTables(pText):
    text = ""
    lines = pText.readlines()
    for line in lines:
        if line == '{|\n':
            line = '''{| class="wikitable"\n'''
        text += line
    return text

def loadTOMediaWiki(input_language, input_title):
    mediawiki_url = getMediaWikiURL(input_language)

    session_item = connectToMediaWiki(mediawiki_url, Bot_getInfo())
    if session_item != None:
        print(session_item)
        text = fixTables(readTxt())
        overwriteWikiSite(session_item[0], session_item[1], mediawiki_url,  input_title, text)
    else:
        print("Connection Failure")

if __name__ == '__main__':
    main()