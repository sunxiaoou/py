#!/bin/sh

for i in `echo *.py`
do
	sed -i 's/#! \/usr\/bin\/python3/#! \/usr\/local\/bin\/python3/' $i
done
