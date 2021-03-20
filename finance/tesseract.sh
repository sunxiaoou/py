#!/bin/sh

if [ $# -lt 2 ]
then
    echo "Usage: $0 yh|hs balance"
    exit 1
fi

name=$1_$2
echo $1 $2 $name

cp -p ~/Desktop/"`ls -lrt ~/Desktop/*.png | tail -1 | awk -F/ '{print $NF}'`" $name.png
tesseract $name.png $name -l eng+chi_sim --psm 6; cat $name.txt

