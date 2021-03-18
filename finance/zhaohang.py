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


def zhaohang(text: str, cash: float):
    text = re.sub('[,‘]', '', text)
    amounts = re.findall(r'[-+]?\d*\.\d+', text)
    print(amounts)
    amounts = [float(i) for i in amounts]
    result = [
        {'platform': '招商银行', 'name': '招赢尊享日日盈', 'market_value': amounts[1], 'hold_gain': amounts[2]},
        {'platform': '招商银行', 'name': '招赢尊享日日盈', 'market_value': amounts[3], 'hold_gain': amounts[4]},
        {'platform': '招商银行', 'name': '睿远平衡二十七期', 'market_value': amounts[5], 'hold_gain': amounts[6]},
        {'platform': '招商银行', 'name': '卓远一年半定开8号', 'market_value': amounts[7], 'hold_gain': amounts[8]}]
    summary = sum([i['market_value'] for i in result])
    assert amounts[0] == summary, print("summary({}) != {}".format(summary, amounts[0]))
    return [{'platform': '招商银行', 'name': '现金', 'market_value': cash, 'hold_gain': 0}] + result


def main():
    # $ zhaohang.py zs_9605.08.png 9605.08 210318
    if len(sys.argv) < 4:
        print('Usage: {} img cash %y%m%d'.format(sys.argv[0]))
        sys.exit(1)

    text = recognize_image(sys.argv[1])
    result = zhaohang(text, float(sys.argv[2]))
    pprint(result)
    save_to_spreadsheet('finance.xlsx', datetime.strptime(sys.argv[3], '%y%m%d'), result)


if __name__ == "__main__":
    main()
