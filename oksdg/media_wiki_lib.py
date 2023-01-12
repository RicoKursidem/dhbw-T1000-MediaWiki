
import requests

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
            "lgtoken": login_token
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

def overwriteWikiPage(session, csrf_token, mediawiki_url, pSiteTitle, pText):
    PARAMS = {
        "action": "edit",
        "format":"json",
        "title": pSiteTitle,
        "text": pText,
        "token": csrf_token
    }
    response = session.post(mediawiki_url, data=PARAMS)
    print(response.json())

def uploadFileToMediaWiki(session, csrf_token, mediawiki_url, filename, filealias = None):
    PARAMS = {
        "action": "upload",
        "filename": filename,
        "format": "json",
        "token": csrf_token,
    }
    if filealias == None: 
        file = {'file':(filename, open(filename, 'rb'), 'multipart/form-data')}
    else:
        file = {'file':(filealias, open(filealias, 'rb'), 'multipart/form-data')}
    print("file    " + str(file))
    response = session.post(mediawiki_url, files=file, data=PARAMS)
    print(response.json())
    
    if response.json()["upload"]["result"] != "Success":
            print(" --- " + str(response.json()["upload"]["warnings"]))
            if "duplicate" in str(response.json()["upload"]["warnings"]):
                print("Your file already exists under the filename " + str(response.json()["upload"]["warnings"]["duplicate"])[2:-2] + ". It is getting used insted.")
                return str(response.json()["upload"]["warnings"]["duplicate"])[2:-2]
            elif "exists" in str(response.json()["upload"]["warnings"]):
                uploadFileToMediaWiki(session, csrf_token, mediawiki_url, input("There already is a file named " + filename + ". Enter an other filename: "), filealias=filename)
    return None

def openFile(filename):
    return open(filename, "r", encoding="utf8")

def convertCSV(file):
    text = "{|\n"
    lines = file.readlines()
    for line in lines:
        print("line:" + line)
        line = "|" + line
        line += "|-\n"
        line = line.replace(";", "\n|")
        text += line
    text += "|}"
    return text

def tableLayout(text):
    layout_string = '''{| class="wikitable"\n'''
    return text.replace("{|", layout_string)
