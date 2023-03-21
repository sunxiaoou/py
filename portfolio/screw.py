#! /usr/bin/python3
import os
import re
import sys
from datetime import datetime
from time import sleep
from urllib.parse import quote

import requests


def save_pic(date: str, url: str):
    path = 'pics' + os.path.sep + date[: 4]
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        resp = requests.get(url)
        if requests.codes.ok == resp.status_code:
            path = path + os.path.sep + '{}.jpg'.format(re.sub(r'-', '', date[: 10]))
            if not os.path.exists(path):
                with open(path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded pic:', path)
            else:
                print('Already Downloaded:', path)
    except Exception as e:
        print(e, 'none123')


def request_zsxq(url: str, headers: dict) -> str:
    response = requests.get(url, headers=headers)
    i = 0
    while i < 10 and not response.json().get('succeeded'):
        sleep(0.1)
        response = requests.get(url, headers=headers)
        i += 1
    assert response.status_code == 200, print('status_code({}) != 200'.format(response.status_code))
    items = response.json()['resp_data']['topics']
    create = ''
    for i in items:
        if 'images' in i['talk']:
            pic = i['talk']['images'][1]['original']['url']
            create = i['create_time']
            save_pic(create, pic)
            # for j in i['talk']['images']:
            #     if 'original' in j:
            #         pic = j['original']['url']
            #         create = i['create_time']
            #         save_pic(create, pic)
            #     elif 'large' in j:
            #         pic = j['large']['url']
            #         create = i['create_time']
            #         save_pic(create, pic)
    return create


def main():
    if len(sys.argv) < 2:
        print('Usage: {} num'.format(sys.argv[0]))
        print('       {} num [end_time(%Y%m%d)]'.format(sys.argv[0]))
        sys.exit(1)

    with open('auth/zsxq_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]      # delete last '\n'
    headers = {
        'Cookie': cookie,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'api.zsxq.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
    }
    url_base = 'https://api.zsxq.com/v2/hashtags/2425888411/topics?count=20'

    num = int(sys.argv[1])
    if len(sys.argv) == 2:
        end_time = ''
    else:
        date = datetime.strptime(sys.argv[2], '%Y%m%d')
        end_time = date.strftime('%Y-%m-%dT%H:%M:%S.%f')[: -3] + '+0800'

    for i in range(num):
        url = url_base + '&end_time=' + quote(end_time) if end_time else url_base
        print(i, url)
        end_time = request_zsxq(url, headers)
        if not end_time:
            break


if __name__ == "__main__":
    main()
