import sys
import media_wiki
import bot_info

def main(args = None):
    print(args)
    filename = args[1]
    try:
        category = args[2].replace(";", "\n")
    except:
        category = ""
    title = filename.split(".")[0]
    
    
    language = "de"

    #connectToDatabase
    session_item = media_wiki.connect(media_wiki.getURL(language), bot_info.getInfo())
    #upload()
    #write on Page()
    media_wiki.overwriteWikiPage(session_item[0], session_item[1], media_wiki.getURL(language), title, category + media_wiki.tableLayout(readFile(filename, category)))

def readFile(filename, category):
    if "CSV" in category:
        return media_wiki.convertCSV(open(filename, "r"))
    else:
        return open(filename, "r").read()

if __name__ == '__main__':
    #This script needs a argument to run
    # 1 --- 'Filename of File to read'
    main(sys.argv)