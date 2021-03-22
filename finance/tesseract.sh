#!/bin/sh

if [ $# -lt 3 ]
then
    echo "Usage: $0 zsb|hsb|yh|hs balance %y%m%d"
    exit 1
fi

name=$3/$1_$2
echo $name
mkdir -p $3

cp -p ~/Desktop/"`ls -lrt ~/Desktop/*.png | tail -1 | awk -F/ '{print $NF}'`" $name.png
# tesseract $name.png $name -l eng+chi_sim --psm 6; cat $name.txt
img2txt.py $name.png 2>&1 | tee $name.txt
