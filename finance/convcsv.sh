#!/bin/sh

if [ $# -lt 1 ]
then
    echo "Usage: $0 balance"
    exit 1
fi

cp -p ~/Desktop/"`ls -lrt ~/Desktop/*.csv | tail -1 | awk -F/ '{print $NF}'`" tmp.csv
file -I tmp.csv
name=$1
iconv -f UTF-16LE -t utf-8 < tmp.csv > $name.csv
rm tmp.csv
