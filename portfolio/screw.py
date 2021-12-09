#! /usr/bin/python3
import os
import re
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


def zsxq():
    with open('zsxq_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]      # delete last '\n'
    url_base = 'https://api.zsxq.com/v2/hashtags/2425888411/topics?count=20'
    headers = {
        'Cookie': cookie,
        # 'Host': url.split('/')[2],
        # 'Origin': 'https://wx.zsxq.com',
        # 'Referer': 'https://wx.zsxq.com/',
        # 'Sec-Fetch-Dest': 'empty',
        # 'Sec-Fetch-Mode': 'cors',
        # 'Sec-Fetch-Site': 'same-site',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) '
        #               'AppleWebKit/537.36 (KHTML, like Gecko) '
        #               'Chrome/88.0.4324.192 Safari/537.36'
        # # X-Request-Id': '284bd31d4-75f1-1242-228a-eeb2ae40681',
        # X-Signature': '70395b502fd7e1944843823176f1688be3e038d2',
        # X-Timestamp': '1638756631',
        # X-Version': '2.14.0'
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

    end_time = ''
    # for j in range(2):
    while True:
        print(end_time)
        url = url_base + '&end_time=' + quote(end_time) if end_time else url_base
        response = requests.get(url, headers=headers)
        i = 0
        while i < 10 and not response.json().get('succeeded'):
            sleep(0.1)
            response = requests.get(url, headers=headers)
            i += 1
        assert response.status_code == 200, print('status_code({}) != 200'.format(response.status_code))
        items = response.json()['resp_data']['topics']
        for i in items:
            # id = i['topic_id']
            create = i['create_time']
            pic = i['talk']['images'][1]['original']['url']
            # print(create, pic)
            save_pic(create, pic)
        end_time = create
    # return df


def main():
    # print(get_cookies())
    zsxq()


if __name__ == "__main__":
    main()
