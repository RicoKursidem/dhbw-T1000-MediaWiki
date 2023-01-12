import requests
import random
import string

def getURL(language):
    return "https://" + language + ".wiki.server.azo/api.php"

def connect(mediawiki_url, login_Info):
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

def uploadFile(session, csrf_token, mediawiki_url, filename):
    return uploadFileRec(session, csrf_token, mediawiki_url, filename, filename)

def uploadFileRec(session, csrf_token, mediawiki_url, filename, file_safe):
    PARAMS = {
        "action": "upload",
        "filename": filename,
        "format": "json",
        "token": csrf_token,
    }
    file = {'file':(file_safe, open("_base/" + file_safe, 'rb'), 'multipart/form-data')}
    print("file    " + str(file))
    response = session.post(mediawiki_url, files=file, data=PARAMS)
    print(response.json())

    if response.json()["upload"]["result"] != "Success":
            print(" --- " + str(response.json()["upload"]["warnings"]))
            if "duplicate-archive" in str(response.json()["upload"]["warnings"]):
                #TODO: Hier liegt ein problem vor das ich nicht ganz verstehe. 
                return str(response.json()["upload"]["warnings"]["exists"])
            elif "duplicate" in str(response.json()["upload"]["warnings"]):
                #This File is already uploadet to the Server, maybe under an other name. It will be used
                return str(response.json()["upload"]["warnings"]["dublicate"])
            elif "exists" in str(response.json()["upload"]["warnings"]):
                #This Filename is alread used -> generating a new one
                return uploadFileRec(session, csrf_token, mediawiki_url, filenameGenerator(), file_safe)
            
    return filename

def filenameGenerator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) + ".pdf"

def tableLayout(text):
    layout_string = '''{| class="wikitable"\n'''
    return text.replace("{|", layout_string)

def convertCSV(csv_file):
    text = ""
    lines = csv_file.readlines()
    print(lines)
    for line in lines:
        line = line.replace(";", "\n|")
        text += line
    return text
    