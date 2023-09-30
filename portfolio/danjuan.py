#! /usr/bin/python3
from datetime import datetime

import pandas as pd
import requests


def dj_page(url: str, headers: dict) -> list:
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    result = []
    for i in response.json()['data']['items']:
        action_desc = i['action_desc']
        if action_desc.endswith('提现'):
            order_id = i['order_id']
            fd_code = i['fd_code']
            fd_name = i['fd_name']
            amount = float(i['amount'])
            bankcard_no = i['bankcard_no']
            bank_name = i['bank_name']
            created_at = datetime.fromtimestamp(int(i['created_at']) // 1000)
            status_desc = i['status_desc']
            result.append((action_desc, order_id, fd_code, fd_name, amount, bankcard_no, bank_name, created_at,
                           status_desc))
    return result


def danjuan(num: int) -> pd.DataFrame:
    with open('auth/dj_cookie.txt', 'r') as f:
        cookie = f.read()[:-1]  # delete last '\n'
    url_base = "https://danjuanfunds.com/djapi/moneyfund/orders"
    headers = {
        'Cookie': cookie,
        'Host': url_base.split('/')[2],
        'User-Agent': 'PostmanRuntime/7.32.2'}

    result = []
    for i in range(num):
        url = '{}?page={}&size=20&type=sale'.format(url_base, i + 1)
        # print(i, url)
        result += dj_page(url, headers)
    columns = ['交易类型', '流水号', '基金代码', '基金名称', '金额', '银行卡号', '银行名称', '生成时间', '状态']
    return pd.DataFrame(result, columns=columns)


def main():
    df = danjuan(3)
    df.index = range(1, len(df) + 1)
    print(df)
    print("金额合计： {}元".format(df['金额'].sum()))


if __name__ == "__main__":
    main()
