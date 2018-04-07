#! /usr/bin/python3

# lucky.py - Opens several Google search results.
# maybe need proxy as:
# $ http_proxy=http://cn-proxy.jp.oracle.com:80 lucky.py

import requests, sys, webbrowser, bs4

if len(sys.argv) < 2:
    print('Usage: ' + sys.argv[0] + ' topic')
    sys.exit(1)
print('Googling...') # display text while downloading the Google page
res = requests.get('http://google.com/search?q=' + ' '.join(sys.argv[1:]))
res.raise_for_status()

# Retrieve top search result links.
soup = bs4.BeautifulSoup(res.text, "lxml")

# Open a browser tab for each result.
linkElems = soup.select('.r a')

numOpen = min(4, len(linkElems))
for i in range(numOpen):
    webbrowser.open('http://google.com' + linkElems[i].get('href'))
