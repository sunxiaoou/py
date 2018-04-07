#! /usr/bin/python3

# You can learn about the requests module’s other features from
# http://requests.readthedocs.org/
# maybe need proxy as:
# $ https_proxy=http://cn-proxy.jp.oracle.com:80 reqGet.py

import requests, sys


res = requests.get('https://automatetheboringstuff.com/files/rj.txt')

"""
if res.status_code != requests.codes.ok:
    sys.exit()

try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
    sys.exit()

print(type(res))
print(len(res.text))

print(res.text[:250])
"""

res.raise_for_status()
playFile = open('RomeoAndJuliet.txt', 'wb')
for chunk in res.iter_content(100000):
    playFile.write(chunk)
playFile.close()
