#! /usr/bin/python3
import json

import requests


def login_hue(username: str, password: str):
    url = "http://localhost:8000/hue/accounts/login"
    headers = {
        'Response-type': 'application/json',
    }
    response = requests.request("GET", url, headers=headers)
    assert response.status_code == 200
    dic = json.loads(response.text)
    dic['sessionid'] = response.cookies.get('sessionid')
    print(dic)

    payload = {
        'username': username,
        'password': password,
        'next': '/'
        # 'csrfmiddlewaretoken': dic['csrfmiddlewaretoken']
    }
    files = []
    headers = {
        'Response-type': 'application/json',
        'Cookie': 'csrftoken={}; sessionid={}'.format(dic['csrftoken'], dic['sessionid']),
        'X-CSRFToken': dic['csrfmiddlewaretoken']
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 200
    return json.loads(response.text)


def main():
    dic = login_hue('sun_xo', 'sun_xo')
    print('csrftoken={}; sessionid={}'.format(dic['csrftoken'], dic['sessionid']))


if __name__ == "__main__":
    main()
