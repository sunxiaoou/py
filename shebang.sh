#!/bin/sh

for i in `echo *.py`
do
	if [ "`head -1 $i`" != "#! /usr/local/bin/python3" ]
	then
		gsed -i '1 i\#! /usr/local/bin/python3\n' $i
		chmod 755 $i
	fi
done
