import requests
import glob
import os

URL = "http://localhost:3001/api.php"
bot_name = "Ava@bot"
bot_password = "me33b0la2iqr5q4ri2dqaqk9bgug5su0"
dateiliste = []

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def rm(val):
    try:
        dateiliste.remove(val.replace("rm ", ""))
    except:
        print("Could not find")

def upload(val):
    delet(val)
    #beginn upload
    file_path = val
    file_name = file_path[:file_path.rfind(".")]
    S = requests.Session()
    PARAMS_1 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_1)
    DATA = R.json()

    LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]

    # Step 2: Send a POST request to login. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_2 = {
        "action": "login",
        "lgname": bot_name,
        "lgpassword": bot_password,
        "format": "json",
        "lgtoken": LOGIN_TOKEN
    }

    R = S.post(URL, data=PARAMS_2)

    # Step 3: Obtain a CSRF token
    PARAMS_3 = {
        "action": "query",
        "meta":"tokens",
        "format":"json"
    }

    R = S.get(url=URL, params=PARAMS_3)
    DATA = R.json()

    CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]

    # Step 4: POST request to upload a file directly
    PARAMS_4 = {
        "action": "upload",
        "filename": file_path,
        "format": "json",
        "token": CSRF_TOKEN,
        "ignorewarnings": 1
    }
    #datei eingelesen
    FILE = {'file':(file_name, open(file_path, 'rb'), 'multipart/form-data')}

    R = S.post(URL, files=FILE, data=PARAMS_4)
    DATA = R.json()
    #end upload
    if ".pdf" in file_path:
        S = requests.Session()

        # Step 1: Retrieve a login token
        PARAMS_1 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_1)
        DATA = R.json()

        LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]
            
        # Step 2: Send a post request to log in. For this login 
        # method, Obtain credentials by first visiting
        # https://test.wikipedia.org/wiki/Special:BotPasswords/
        # See https://www.mediawiki.org/wiki/API:Login for more
        # information on log in methods.
        PARAMS_2 = {
            "action": "login",
            "lgname": bot_name,
            "lgpassword": bot_password,
            "format": "json",
            "lgtoken": LOGIN_TOKEN
        }

        R = S.post(URL, data=PARAMS_2)

        # Step 3: While logged in, retrieve a CSRF token
        PARAMS_3 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_3)
        DATA = R.json()

        CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]
        #pdf content
        pdf_file = open(file_path, 'rb')
        description = ""
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        for x in range(0, number_of_pages):
            page = read_pdf.getPage(x)
            page_content = page.extractText()
            description += str(page_content.encode('utf-8'))
        description =  description.replace("\\n", " ")
        #end pdf content

        # Step 4: Send a post request to edit a page
        PARAMS_4 = {
            "action": "edit",
            "title": file_name,
            "format": "json",
            "appendtext": "<div style=\"text-align:center\"><pdf height=\"807\"> Datei:" + file_path + "</pdf> </div> <div style=\"display:none;\">" + str(description) + "</div>",
            "token": CSRF_TOKEN,
        }
        R = S.post(URL, data=PARAMS_4)
        DATA = R.json()

    if ".md" in file_path:
        #get file content 
        content = file_get_contents(file_path)
        #convert to html; extras tables for Tabellen
        html = markdown2.markdown(content, extras=["tables"])

        title = html[html.find("<h1>") + 4:html.find("</h1>")]
        delet(file_name)
        S = requests.Session()

        # Step 1: Retrieve a login token
        PARAMS_1 = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_1)
        DATA = R.json()

        LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]
            
        # Step 2: Send a post request to log in. For this login 
        # method, Obtain credentials by first visiting
        # https://test.wikipedia.org/wiki/Special:BotPasswords/
        # See https://www.mediawiki.org/wiki/API:Login for more
        # information on log in methods.
        PARAMS_2 = {
            "action": "login",
            "lgname": bot_name,
            "lgpassword": bot_password,
            "format": "json",
            "lgtoken": LOGIN_TOKEN
        }

        R = S.post(URL, data=PARAMS_2)

        # Step 3: While logged in, retrieve a CSRF token
        PARAMS_3 = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        R = S.get(url=URL, params=PARAMS_3)
        DATA = R.json()

        CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]

        #edit html
        html = html.replace("<h1>" + title + "</h1>", "") #löscht die Überschrift
        html = html.replace("ä", "ae")  #entfernt spezial charactere
        html = html.replace("ö", "oe")
        html = html.replace("ü", "ue")
        html = html.replace("Ä", "Ae")
        html = html.replace("Ö", "Oe")
        html = html.replace("Ü", "Ue")
        html = html.replace("<thead>", "")  #entfernt nutzloses Tabellenzugs
        html = html.replace("</thead>", "")
        html = html.replace("<tbody>", "")
        html = html.replace("</tbody>", "")
        while 1:    #ändert links
            pos = html.find("<a ")  #sucht den Anfang
            if pos == -1:   #wenn nichts gefunden wurde wird die schleife beendet
                break
            substr = html[pos:] #Alles nach dem Fundort wird als string behalten
            pos2 = substr.find("\"") #sucht nach dem ersten " wo der  dateiname beginnt
            substr = substr[pos2+1:] #Alles nach dem Fundort wird als string behalten diesmal plus 1 damit das gefunden zeichen weg ist
            pos2 = substr.find("\"") # findet das ende der dateiname angabe
            substr = substr[:pos2] # der string hört mit ende der Pfadangabe auf
            substr = substr.replace(".md", "")  #Eine dateiendung wird ignoriert gegebenfalls weiter hinzufügen 
            substr = substr.replace(".html", "")
            page_link = substr # der name der Seite zu der Verlinkt werden soll
            substr = html[pos:] #stzt den sting auf den fundort von "<a " zurück
            pos2 = substr.find(">") # sucht das ende der anfangs kammer (bsp: <a href="hallo"> der Text der ein link ist</a>)
            substr = substr[pos2+1:] #geht hinter das  zeichen 
            pos2 = substr.find("</a>") #sucht das ende des Link textes
            page_link_alias = substr[:pos2] # der text, welcher linkt.
            substr = html[pos:]  #stzt den sting auf den fundort von "<a " zurück
            pos2 = substr.find("</a>") # das erste "</a>" 
            substr = substr[:pos2]  # det Text entspricht jetzt (bsp: <a href="hallo"> der Text der ein link ist) vgl oben
            html = html.replace(substr, "[[" + page_link + "|" + page_link_alias + "]]") #wird erstzt

        html = html.replace("</a>", "") # alle endteile werden entfernt

        while 1:
            pos = html.find("<img ") # sucht nach dem beginn des image tagges (bsp: <img src="Ordner eins/Ordner2/bild.png">)
            if pos == -1:   #hört auf wenn nichts mehr da
                break
            substr = html[pos:]
            pos2 = substr.find("\"") #findet den beginn des Pfades
            substr = substr[pos2+1:] #Alles nach dem Fundort wird als string behalten diesmal plus 1 damit das gefunden zeichen weg ist
            pos2 = substr.find("\"") #findet das ende des Pfades
            substr = substr[:pos2] 
            pos2 = substr.rfind("/") #sucht das letzt /  da wikimedia keine pfade hat entfällt er 
            imagename = substr[pos2+1:] # ignoriet alles bis nach dem /
            substr = html[pos:] # string zurücksetzten
            pos2 = substr.find(">") # ende des image tagges
            substr = substr[:pos2+1] # string setzten
            html = html.replace(substr, "[[File:" + imagename +"]]") #ersetzten
        
        #end edit
        PARAMS_4 = {
            "action": "edit",
            "title": file_name,
            "format": "json",
            "appendtext": html,
            "token": CSRF_TOKEN,
        }
        R = S.post(URL, data=PARAMS_4)
        DATA = R.json()

def delet(val):
    S = requests.Session()
    file_path = val
    pos = file_path.rfind(".")
    if pos != -1:
        file_name = file_path[:pos]
    else:
        file_name = file_path
    # Step 1: Retrieve login token
    PARAMS_0 = {
        'action':"query",
        'meta':"tokens",
        'type':"login",
        'format':"json"
    }

    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Step 2: Send a post request to login. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        'action':"login",
        'lgname':bot_name,
        'lgpassword':bot_password,
        'lgtoken':LOGIN_TOKEN,
        'format':"json"
    }

    R = S.post(URL, data=PARAMS_1)

    # Step 3: When logged in, retrieve a CSRF token
    PARAMS_2 = {
        'action':"query",
        'meta':"tokens",
        'format':"json"
    }

    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()

    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

    # Step 4: Send a post request to delete a page
    PARAMS_3 = {
        'action':"delete",
        'title':file_name,
        'token':CSRF_TOKEN,
        'format':"json"
    }

    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()

def linking(val):
    sitename = "__ERROR__"
    file_path = val
    file_name = file_path[:file_path.rfind(".")]
    while(sitename == "__ERROR__"):
        print("Wo soll die Datei " + file_name + " Verlinkt werden???\n")
        print("1: Baupläne\n2: Anlagendiagramm\n3: Elektropläne\n4: Anleitungen\n5: Diagnose\n6: Kontakt\n")
        eingabe = input("Auf welche Seite soll verlinkt werden\n")
        if "1" in eingabe:
            sitename = "Baupläne"
        elif "2" in eingabe:
            sitename = "Anlagendiagramme"
        elif "3" in eingabe:
            sitename = "Elektropläne"
        elif "4" in eingabe:
            sitename = "Anleitungen"
        elif "5" in eingabe:
            sitename = "Diagnose"
        elif "6" in eingabe:
            sitename = "Kontakt"
        else:
            print("Ungültige Eingabe bitte Erneut")
    S = requests.Session()

    # Step 1: Retrieve a login token
    PARAMS_1 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_1)
    DATA = R.json()

    LOGIN_TOKEN = DATA["query"]["tokens"]["logintoken"]
        
    # Step 2: Send a post request to log in. For this login 
    # method, Obtain credentials by first visiting
    # https://test.wikipedia.org/wiki/Special:BotPasswords/
    # See https://www.mediawiki.org/wiki/API:Login for more
    # information on log in methods.
    PARAMS_2 = {
        "action": "login",
        "lgname": bot_name,
        "lgpassword": bot_password,
        "format": "json",
        "lgtoken": LOGIN_TOKEN
    }

    R = S.post(URL, data=PARAMS_2)

    # Step 3: While logged in, retrieve a CSRF token
    PARAMS_3 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_3)
    DATA = R.json()

    CSRF_TOKEN = DATA["query"]["tokens"]["csrftoken"]
    if ".pdf" in file_path:
        content = "[[File:txt.png|30px|link="+file_name+"]]&nbsp;&nbsp;&nbsp;&nbsp;[[" + file_name + "| "+ file_name + "]]<br>"
    elif ".md" in file_path:
        content = "[[File:txt.png|30px|link="+file_name+"]]&nbsp;&nbsp;&nbsp;&nbsp;[[" + file_name + "]]<br>"
    else:
        content = "[[File:"+ icon(file_path) +"|30px]]&nbsp;&nbsp;&nbsp;&nbsp;[[:Media:" + file_path + "| " + file_name + "]]<br>"

    PARAMS_4 = {
        "action": "edit",
        "title": sitename,
        "format": "json",
        "appendtext": content,
        "token": CSRF_TOKEN,
    }
    R = S.post(URL, data=PARAMS_4)
    DATA = R.json()

def icon(val):
    if ".png" in val or ".jpg" in val:
        return "img.png"
    elif ".mp4" in val:
        return "vid.png"
    else:
        return "txt.png"

def clearlinks():
    print("Welche Seite soll gelöscht werden??")
    print("1: Baupläne\n2: Anlagendiagramm\n3: Elektropläne\n4: Anleitungen\n5: Diagnose\n6: Kontakt\n")
    eingabe = input("Wenn du eine eigene Seite löschenwillst kannst du auch den Namen eintippen")
    if "1" in eingabe:
        sitename = "Baupläne"
    elif "2" in eingabe:
        sitename = "Anlagendiagramme"
    elif "3" in eingabe:
        sitename = "Elektropläne"
    elif "4" in eingabe:
        sitename = "Anleitungen"
    elif "5" in eingabe:
        sitename = "Diagnose"
    elif "6" in eingabe:
        sitename = "Kontakt"
    else:
        sitename = eingabe
    delet(sitename)

def cd(eingabe):
    if len(dateiliste) == 0:
        try:
            os.chdir(eingabe.replace("cd ",""))
        except OSError:
            print("Wrong name!!")
    else:
        print("The List is not empty!! clear or push first")

def ls():
    thisList = glob.glob("*")
    print(thisList)

def add(eingabe):
    content = eingabe.replace("add ","")
    temp = glob.glob(content)
    if len(temp) == 0:
        print("No Item found")
    for val in temp:
        string = val
        dateiliste.append(string)

def get():
    print(dateiliste)

def push():
    print("Diese Dateien werden gepusht:\n")
    get()
    eingabe = input("Sollen die Dateien verlinkt werden? y/n\n")
    if "y" in eingabe:
        link = True
    else:
        link = False
    for val in dateiliste:
        strin = val
        delet(strin)
        upload(strin)
        if link:
            linking(strin)

print("Was willst du tun\n\"cd \" um das Verzeichniss zu ändern\n\"add \" um datei für upload zu markieren \n\"rm \" um einen eintrag zu löschen\n\"get\" um alle markierten datein zu sehen und \n\"push\" für den upload\n\"x\" um zu beenden\n\"ls\" for all files\n\"ClearSites\" for clearing the link list\n\"clear\" for clearing the get list\n\"help\" for help")
ls()
while 1:

    eingabe = input("EIngabe:\n")
    if eingabe=="x":
        break
    elif "cd " in eingabe:
        cd(eingabe)
    elif "add " in eingabe:
        add(eingabe)
    elif "rm " in eingabe:
        rm(eingabe)
    elif "ls" in eingabe:
        ls()
    elif "get" in eingabe:
        get()
    elif "push" in eingabe:
        push()
    elif "clear" in eingabe:
        dateiliste = []
    elif "ClearSites" in eingabe:
        clearlinks()
    elif "help" in eingabe:
        print("Was willst du tun\n\"cd \" um das Verzeichniss zu ändern\n\"add \" um datei für upload zu markieren \n\"rm \" um einen eintrag zu löschen\n\"get\" um alle markierten datein zu sehen und \n\"push\" für den upload\n\"x\" um zu beenden\n\"ls\" for all files\n\"ClearSites\" for clearing the link list\n\"clear\" for clearing the get list\n\"help\" for help")
    else:
        print("Unbekannter Input")
