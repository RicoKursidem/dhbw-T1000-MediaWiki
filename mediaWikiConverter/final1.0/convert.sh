#!/bin/bash

#python3 import_to_wiki.py $title $next


function use_Pandoc(){
    sudo docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/core -t mediawiki -i ${input_file} -o temp_output_file.txt
}

#get Input
echo "Filename mit Endung eingeben (beispiel.docx)"
read input_file

extension="${input_file##*.}"

found=0
for f in *; do
    if [ "$input_file" = "$f" ]; then
        found=1
        if [ $extension = "docx" ] || [ $extension = "md" ]; then
            use_Pandoc
            python3 import_to_wiki.py "temp_output_file.txt"
            rm temp_output_file.txt
        elif [ $extension = "pdf" ] || [ $extension = "csv" ] || [ $extension = "txt" ]; then
            python3 import_to_wiki.py $input_file
        elif [ $extension = "png" ] || [ $extension = "jpg" ]; then
            python3 import_to_wiki.py $input_file
        else 
            echo "Diese Fileextension " $extension " wird nicht unterstützt"
            echo "Unterstützte Formate sind: "
            echo ".docx, .md, .pdf, .csv, .txt(Mediawiki-Format), "
            echo ".png, .jpg"
        fi
    else
        echo .
    fi
    done
if [ "$found" = "0" ]; then
    #in case someone wants to implement a file witch already exists
    #if [ $extension = "pdf" ]; then 
        #python3 import_to_wiki.py $input_file
    #else
    echo File Not Found!
    #fi
fi