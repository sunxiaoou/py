#! /usr/bin/python3

# Get transcripts from http://animetranscripts.wikispaces.com
# It needs a url as:
# http://animetranscripts.wikispaces.com/Haibane%20Renmei%20-%20%E7%81%B0%E7%BE%BD%E9%80%A3%E7%9B%9F

import bs4, re, requests, sys

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' url')
    sys.exit(1)

url = sys.argv[1]
reg = re.compile(r'http://.*/(\w+).*')
title = reg.search(url).group(1)

res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")

linkElems = soup.select('.wiki_table a')

for i in range(len(linkElems)):
    fn = title + '{:02d}.txt'.format(i + 1)
    print(fn)
    res = requests.get('http://animetranscripts.wikispaces.com' + linkElems[i].get('href'))
    resSoup = bs4.BeautifulSoup(res.text, "lxml")
    elems = resSoup.select('#content_view')
    txt = open(fn, 'w')
    txt.write(elems[0].getText())
    txt.close()
