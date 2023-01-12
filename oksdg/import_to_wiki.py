import requests
import sys
from requests.sessions import Session
from bot_info import getInfo as Bot_getInfo
from media_wiki_lib import *



def main(args = None):

    
    filename = args[1]

    fileextension = filename.split(".")[1]

    if not fileextension == "png" and not fileextension == "jpg":
        title = input("Title der Wiki-Seite: ")
        print("Wikipage: " + title, end = '')
    language = input("Sprache des Servers (de oder en): ")
    print(", Filename: " + filename + ", Language: " + language)

    session_item = connectToMediaWiki(getMediaWikiURL(language),Bot_getInfo())

    if fileextension == "pdf":
        #bei einem Dublicate zweier PDFs muss die schon vorhandene eingesetz werden.
        new_filename = uploadFileToMediaWiki(session_item[0], session_item[1], getMediaWikiURL(language), filename)
        if(new_filename != None):
            filename = new_filename
        overwriteWikiPage(session_item[0], session_item[1], getMediaWikiURL(language),  title, "<pdf>Datei:" + filename + "</pdf>")
        
    elif fileextension == "csv":
        text = tableLayout(convertCSV(openFile(filename)))
        overwriteWikiPage(session_item[0], session_item[1], getMediaWikiURL(language),  title, text)
    elif fileextension == "txt":
        overwriteWikiPage(session_item[0], session_item[1], getMediaWikiURL(language),  title, tableLayout(openFile(filename).read()))
    elif fileextension == "html":
        overwriteWikiPage(session_item[0], session_item[1], getMediaWikiURL(language),  title, openFile(filename).read())
    elif fileextension == "png" or fileextension == "jpg":
        #upload unter gleichem namen nicht möglich
        uploadFileToMediaWiki(session_item[0], session_item[1], getMediaWikiURL(language), filename)
    else:
        print("FileextensionError")
        return


if __name__ == '__main__':
    #This script needs a argument to run
    # 1 --- 'Filename of File to read'
    main(sys.argv)