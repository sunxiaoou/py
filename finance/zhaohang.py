#! /usr/bin/python3
import re
import sys
from datetime import datetime
from pprint import pprint

import tesserocr
from PIL import Image

from save_to import save_to_spreadsheet


def recognize_image(image_name: str) -> str:
    image = Image.open(image_name)
    # image.show()
    return tesserocr.image_to_text(image, lang='eng+chi_sim', psm=tesserocr.PSM.SINGLE_BLOCK)


def zhaohang(text: str, cash: float, date: datetime):
    result = [{'name': '现金', 'risk': 0, 'market_value': cash, 'hold_gain': 0}]
    text = re.sub('[,‘]', '', text)
    amounts = re.findall(r'[-+]?\d*\.\d+', text)
    print(amounts)
    amounts = [float(i) for i in amounts]
    result += [
        {'name': '招赢尊享日日盈', 'risk': 0, 'market_value': amounts[1], 'hold_gain': amounts[2]},
        {'name': '招赢尊享日日盈', 'risk': 0, 'market_value': amounts[3], 'hold_gain': amounts[4]},
        {'name': '睿远平衡二十七期', 'risk': 1, 'market_value': amounts[5], 'hold_gain': amounts[6]},
        {'name': '卓远一年半定开8号', 'risk': 1, 'market_value': amounts[7], 'hold_gain': amounts[8]}]
    summary = sum([i['market_value'] for i in result[1:]])
    assert amounts[0] == summary, print("summary({}) != {}".format(summary, amounts[0]))
    for dic in result:
        dic['platform'] = '招商银行'
        dic['currency'] = 'rmb'
        dic['date'] = date
    return result


def main():
    # $ zhaohang.py zs_9605.08.png 9605.08 210318
    if len(sys.argv) < 4:
        print('Usage: {} img cash %y%m%d'.format(sys.argv[0]))
        sys.exit(1)

    text = recognize_image(sys.argv[1])
    result = zhaohang(text, float(sys.argv[2]), datetime.strptime(sys.argv[3], '%y%m%d'))
    pprint(result)
    save_to_spreadsheet('finance.xlsx', sys.argv[3], result)


if __name__ == "__main__":
    main()
