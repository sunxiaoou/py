#! /usr/bin/python3
import requests


class WxPusher:
    @staticmethod
    def push(subject: str, body: str):
        with open('auth/wxpusher.txt', 'r') as file:
            token = file.readline().strip()
            uid = file.readline().strip()

        data = {
            'appToken': token,
            'contentType': 1,
            # 'topicIds': [123],
            'uids': [uid],
            'verifyPay': False,
            'summary': subject,
            'content': body
        }
        url = 'https://wxpusher.zjiecode.com/api/send/message'
        response = requests.post(url=url, json=data)
        # print(response.text)


def main():
    WxPusher.push('hello', 'Hello from WxPusher')


if __name__ == "__main__":
    main()
