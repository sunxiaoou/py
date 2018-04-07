#!/bin/sh

for i in `echo *.py`
do
	if [ "`head -1 $i`" != "#! /usr/bin/python3" ]
	then
		sed -i '1 i\#! /usr/bin/python3\n' $i
		chmod 755 $i
	fi
done
