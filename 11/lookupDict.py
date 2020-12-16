#! /usr/bin/python3
import os
import sys
import requests
from bs4 import BeautifulSoup


def lookup(word: str):
    url = 'http://www.iciba.com/' + word
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    print("生词：" + word)
    pronunciation = soup.find("ul", class_="Mean_symbols__5dQX7").getText()
    print("发音：" + pronunciation)
    paraphrase = soup.find("ul", class_="Mean_part__1RA2V").getText()
    print("释义: " + paraphrase)


def main():
    if len(sys.argv) < 2:
        print('Usage: {} vocabulary'.format(sys.argv[0]))
        sys.exit(1)
    # sys.stdout.flush()
    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as f:
            for w in f.read().splitlines():
                if w:
                    lookup(w)
    else:
        lookup(sys.argv[1])


if __name__ == "__main__":
    main()
