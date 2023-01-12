#!/bin/bash
echo "Filename mit Endung eingeben (beispiel.docx): "
read input_file

# Check if valid datatype for pandoc (md, html, docx)
# if not check if csv or pdf, start special cases
function use_Pandoc(){
    sudo docker run --rm --volume "`pwd`:/data" --user `id -u`:`id -g` pandoc/core -t mediawiki -i ${input_file} -o temp_output_file.txt
}
found=0
for f in *; do
    if [ "$input_file" = "$f" ]; then
        found=1
        echo "$input_file" gets processed
        #Use pandoc Container to parse from .md to .txt(MediaWiki)
        echo Converting Text to MediaWiki
        
        use_Pandoc

        #strt python to upload Text
        echo "Loading text to MediaWiki page"
        python3 loadToMMediaWiki.py
        rm temp_output_file.txt
        echo "completed"
        break
    else
        echo .
    fi
done
if [ "$found" = "0" ]; then
    echo File Not Found!
fi