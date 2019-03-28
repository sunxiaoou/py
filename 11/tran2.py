#! /usr/local/bin/python3

# Get transcripts from http://animetranscripts.wikispaces.com
# It needs a url as:
# http://animetranscripts.wikispaces.com/Haibane%20Renmei%20-%20%E7%81%B0%E7%BE%BD%E9%80%A3%E7%9B%9F

import bs4

# title = 'FLCL'
title = 'thePlacePromised'
home = '/home/xixisun/Videos/Anime/animetranscripts/animetranscripts.wikispaces.com/'
# htmls = ['FLCL _ 1.html', 'FLCL _ 2.html', 'FLCL _ 3.html', 'FLCL _ 4.html']
for i in range(1):
    # html = '{}{} _ {}.html'.format(home, title, i + 1)
    html = home + 'The Place Promised in Our Early Days.html'
    fn = '{}{:02d}.txt'.format(title, i + 1)
    print(fn)
    resSoup = bs4.BeautifulSoup(open(html), "lxml")
    elems = resSoup.select('#content_view')
    txt = open(fn, 'w')
    txt.write(elems[0].getText())
    txt.close()
