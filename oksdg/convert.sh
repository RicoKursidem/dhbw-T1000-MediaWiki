#!/bin/bash

#noch unabhängig von Speicherort von convert.sh machen
FILES=$(find _base -type f)
FOLDERS=$(ls -d */)

for FILE in ${FILES}; do
    #Ermittle den Dateinamen
    FILENAME=${FILE##*/}

    echo FILENAME: $FILENAME
    #Ermittle die Kategorien welche hinzugefügt werden sollen
    CATAGORIE_STRING=" "
    echo -n "CATEGORIE: "
    for CATEGORIE in ${FOLDERS}; do
        
        if [ $CATEGORIE != "_base/" ] && [ $CATEGORIE != "_script/" ]; then
            if [ -f $CATEGORIE$FILENAME ]; then
                echo -n " - ${CATEGORIE%/*}"
                CATAGORIE_STRING+="[[Category:${CATEGORIE%/*}]];"
            fi
        fi
    done
    echo $CATAGORIE_STRING
    #Ermittle den Dateityp
    EXTENSIONTYPE=$(file --mime-type _base/$FILENAME)
    echo EXTENSIONTYPE: $EXTENSIONTYPE
    #Entscheide was mit der Datei passieren soll -> pythonscripts aufrufen

    #pdf muss Upload und Einbindung erfolgen
    #plaintext muss pandoc zur konvertierung genutzt und dann Eingebunden erfolgen
    #docx dateien muss pandoc zur konvertierung genutzt und dann Eingebunden erfolgen
    #       -> Für Zukünftige Versionen Bilder hinzufügen durch Upload und Tabellen fixen
    #csv muss manuell convertirt werden und dann Eingebunden werden(Problem: CSV hat Dateityp plain)

    if [ "$EXTENSIONTYPE" = "_base/$FILENAME: application/pdf" ]; then
        echo -n "loading to MediaWiki ... " 
        python3 _script/upload_PDF.py $FILENAME $CATAGORIE_STRING
        echo -e "\033[32mdone\033[0m"
    elif [ "$EXTENSIONTYPE" = "_base/$FILENAME: text/plain" ]; then
        sudo docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/core -t mediawiki -i $FILE -o ${FILENAME%.*}.txt
        if [ ${FILENAME##*.} = "csv" ]; then
            CATAGORIE_STRING+="[[Category:CSV]];"
        fi
        python3 _script/upload_txt.py ${FILENAME%.*}.txt $CATAGORIE_STRING
        rm ${FILENAME%.*}.txt 
        echo -e "\033[32mdone\033[0m"
    elif [ "$EXTENSIONTYPE" = "_base/$FILENAME: application/vnd.openxmlformats-officedocument.wordprocessingml.document" ]; then
        sudo docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/core -t mediawiki -i $FILE -o ${FILENAME%.*}.txt
        python3 _script/upload_txt.py ${FILENAME%.*}.txt $CATAGORIE_STRING
        rm ${FILENAME%.*}.txt
        echo -e "\033[32mdone\033[0m"
    else
        echo -e "\033[31mNicht unterstützer Datentyp\033[0m"
    fi
    echo ------------------------------------------------
done