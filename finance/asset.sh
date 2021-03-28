#!/bin/sh

usage()
{
echo "$0 usage:" && grep " .)\ #" $0;
exit 0;
}


[ $# -eq 0 ] && usage
while getopts ":b:c:d:e:f:p:" arg; do
  case $arg in
    b) # balance (float)
      balance=${OPTARG}
      options="$options --balance=${OPTARG}"
      ;;
    c) # currency ("rmb" | "hkd" | "usd")
      currency=${OPTARG}
      options="$options --currency=${OPTARG}"
      ;;
    d) # date (%y%m%d)
      date=${OPTARG}
      # options="$options --date=${OPTARG}"
      ;;
    e) # exchange_rate (float)
      # exchange_rate=${OPTARG}
      options="$options --exchange_rate=${OPTARG}"
      ;;
    p) # platform ("zsb" | "hsb" | "yh" | "hs" | "ft")
      platform=${OPTARG}
      # options="$options --platform=${OPTARG}"
      ;;
    h | *) # Display help.
      usage
      exit 0
      ;;
  esac
done

if [ -z ${date+x} ] || [ -z ${platform+x} ]; then
  echo "date, platform are both mandatory"
  exit 1
fi

mkdir -p $date
if [ $platform = 'dj' ] || [ $platform = 'ths' ]; then
  options="$platform $date"
elif [ $platform = "ft" ]; then
  if [ $currency = "usd" ]; then
    datafile=$date/${platform}_$balance
    echo $datafile
    if [ ! -f $datafile.csv ]; then
      cp -p ~/Desktop/"`ls -lrt ~/Desktop/*.csv | tail -1 | awk -F/ '{print $NF}'`" tmp.csv
      file -I tmp.csv
      iconv -f UTF-16LE -t utf-8 < tmp.csv > $datafile.csv
      rm tmp.csv
    fi
    options="--datafile=$datafile.csv $options $platform $date"
  else
    options="$options $platform $date"
  fi
else
  datafile=$date/${platform}_$balance
  echo $datafile
  if [ ! -f $datafile.png ]; then
    cp -p ~/Desktop/"`ls -lrt ~/Desktop/*.png | tail -1 | awk -F/ '{print $NF}'`" $datafile.png
  fi
  # tesseract $datafile.png $datafile -l eng+chi_sim --psm 6; cat $datafile.txt
  img2txt.py $datafile.png 2>&1 | tee $datafile.txt
  options="--datafile=$datafile.txt $options $platform $date"
fi

echo "asset.py $options" >> asset.log
# asset.py $options
# sh asset.log