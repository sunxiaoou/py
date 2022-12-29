#!/bin/sh

if [ $# -lt 1 ]
then
    echo "Usage: $0 xlsx"
    exit 1
fi

~/learn/py/finance/cvtbone.py $1 20 > /tmp/cvt.txt
n1=`grep -n "代码" /tmp/cvt.txt | awk -F: '{print $1}' | sed -n '1p'`
n2=`grep -n "代码" /tmp/cvt.txt | awk -F: '{print $1}' | sed -n '2p'`
n5=`grep -n "代码" /tmp/cvt.txt | awk -F: '{print $1}' | sed -n '5p'`
n7=`grep -n "代码" /tmp/cvt.txt | awk -F: '{print $1}' | sed -n '7p'`
echo $n1 $n2 $n5 $n7
sed -n "$n1,${n2}p" /tmp/cvt.txt > /tmp/cvt2.txt
sed -n "$n5,${n7}p" /tmp/cvt.txt >> /tmp/cvt2.txt

for i in `grep "^\d" /tmp/cvt2.txt | awk '{print $2}' | sort | uniq`
do
    ~/learn/py/portfolio/grid.py $i 125 165 10 80 2022-01-01
done | sort -rn -k 8 > /tmp/cvt3.txt

