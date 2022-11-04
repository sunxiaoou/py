#! /usr/bin/python3
import json
import re
import sys
from pprint import pprint

from requests import request


def login(host: str, username: str, password: str) -> dict:
    url = "http://" + host + ":8000/hue/accounts/login"
    headers = {
        'Response-type': 'application/json',
    }
    response = request("GET", url, headers=headers)
    assert response.status_code == 200
    dic = json.loads(response.text)
    dic['sessionid'] = response.cookies.get('sessionid')
    # print(dic)

    payload = {
        'username': username,
        'password': password,
        'next': '/'
        # 'csrfmiddlewaretoken': dic['csrfmiddlewaretoken']
    }
    headers = {
        'Response-type': 'application/json',
        'Cookie': 'csrftoken={}; sessionid={}'.format(dic['csrftoken'], dic['sessionid']),
        'X-CSRFToken': dic['csrfmiddlewaretoken']
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def logout(host: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/hue/accounts/logout"
    headers = {
        'Response-type': 'application/json',
        'Cookie': cookie
    }
    response = request("GET", url, headers=headers)
    assert response.status_code == 200
    return json.loads(response.text)


def list_users(host: str, cookie: str) -> []:
    url = "http://" + host + ":8000/useradmin/users?=&is_embeddable=true"
    headers = {
        'Response-type': 'application/json',
        'Cookie': cookie
    }
    response = request("GET", url, headers=headers)
    assert response.status_code == 200
    dic = json.loads(response.text)
    return dic['data'] if dic["status"] == 0 else []


def add_user(host: str, username: str, password: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/useradmin/users/new"
    payload = {'username': username,
               'password1': password,
               'password2': password,
               'ensure_home_directory': 'on',
               'first_name': '',
               'last_name': '',
               'email': '',
               'groups': '1',
               'is_active': 'on',
               'is_embeddable': 'true'}
    headers = {
        'Response-type': 'application/json',
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def delete_user(host: str, userid: str, cookie: str) -> dict:
    url = "http://" + host + ":8000/useradmin/users/delete"
    payload = {'is_embeddable': 'true',
               'is_delete': 'on',
               'user_ids': userid}
    headers = {
        'Response-type': 'application/json',
        'Cookie': cookie,
        'X-CSRFToken': re.search('csrftoken=(.+?);', cookie).group(1)
    }
    response = request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    return json.loads(response.text)


def main():
    with open('hue_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]

    if len(sys.argv) > 4:
        if sys.argv[1] == 'login':
            dic = login(sys.argv[2], sys.argv[3], sys.argv[4])
            print('csrftoken={}; sessionid={}'.format(dic['csrftoken'], dic['sessionid']))
        elif sys.argv[1] == 'add_user':
            print(add_user(sys.argv[2], sys.argv[3], sys.argv[4], cookie))
        else:
            assert False
    elif len(sys.argv) > 3:
        assert sys.argv[1] == 'delete_user' and sys.argv[3].isnumeric()
        print(delete_user(sys.argv[2], sys.argv[3], cookie))
    elif len(sys.argv) > 2:
        if sys.argv[1] == 'list_users':
            pprint(list_users(sys.argv[2], cookie))
        elif sys.argv[1] == 'logout':
            print(logout(sys.argv[2], cookie))
        else:
            assert False
    else:
        print('Usage: {} login host username password       # login'.format(sys.argv[0]))
        print('       {} logout host                        # logout'.format(sys.argv[0]))
        print('       {} list_users host                    # list users'.format(sys.argv[0]))
        print('       {} add_user host username password    # add user'.format(sys.argv[0]))
        print('       {} delete_user host userid            # delete user'.format(sys.argv[0]))


if __name__ == "__main__":
    main()
