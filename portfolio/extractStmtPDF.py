#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
from pprint import pprint

import pdfplumber
import pandas as pd
import re


def idx_of(seq, needle) -> int:
    """返回 needle 在 seq 中首次出现的位置，不存在返回 -1"""
    try:
        return seq.index(needle)
    except ValueError:
        return -1

def slice_between(seq, start_token, end_token) -> list:
    """截取 seq 中 (start_token 之后) 到 (end_token 之前) 的子序列；找不到则返回空"""
    s = idx_of(seq, start_token)
    if s < 0:
        return []
    e = idx_of(seq, end_token)
    if e < 0 or e <= s:
        return seq[s+1:]
    return seq[s+1: e]

_num_re = re.compile(r"^\(?-?[\d,]+(?:\.\d+)?\)?$")  # 允许 (32,385.45)

def as_number(s):
    """把 '1,360,011.66' '(32,385.45)' 转成 float；转不了返回原字符串"""
    if not isinstance(s, str):
        return s
    s = s.strip()
    if not _num_re.match(s):
        return s
    neg = s.startswith("(") and s.endswith(")")
    s2 = s.strip("()").replace(",", "")
    try:
        v = float(s2)
        return -v if neg else v
    except ValueError:
        return s

def pick_kv(seq, key, default=None):
    """在 seq 中找 key，返回其后第一个 token（通常就是 value）"""
    i = idx_of(seq, key)
    if i >= 0 and i + 1 < len(seq):
        return seq[i+1]
    return default

def pick_next_number_after(seq, key, default=None):
    """在 seq 中找 key，返回其后第一个“像数字”的 token"""
    i = idx_of(seq, key)
    if i < 0:
        return default
    for j in range(i+1, min(i+20, len(seq))):
        if isinstance(seq[j], str) and _num_re.match(seq[j].strip()):
            return seq[j]
    return default

def parse_holding_summary(tokens):
    vol_ccy_re = re.compile(r"^([\d,]+(?:\.\d+)?)(HKD|USD|CNY)$")
    hold_sec = slice_between(tokens, "持倉摘要", "備註")
    rows = []
    i = 0
    while i < len(hold_sec):
        tok = hold_sec[i]
        if isinstance(tok, str) and tok.startswith("#"):
            symbol = tok[1:]
            # 从 symbol 后开始扫，直到找到 vol+ccy
            j = i + 1
            vol = ccy = None
            closing_price = market_value = None

            while j < len(hold_sec):
                m = vol_ccy_re.match(hold_sec[j]) if isinstance(hold_sec[j], str) else None
                if m:
                    vol = as_number(m.group(1))
                    ccy = m.group(2)
                    # 期望后面两个是 price / value
                    if j + 1 < len(hold_sec):
                        closing_price = as_number(hold_sec[j+1])
                    if j + 2 < len(hold_sec):
                        market_value = as_number(hold_sec[j+2])
                    break
                # 如果遇到下一个 symbol，说明本行异常/缺字段，跳出
                if isinstance(hold_sec[j], str) and hold_sec[j].startswith("#"):
                    break
                j += 1

            if vol is not None and ccy is not None:
                rows.append({
                    "symbol": symbol,
                    "volume": vol,
                    "currency": ccy,
                    "closing_price": closing_price,
                    "market_value": market_value,
                })
            i = j  # 跳到当前行处理结束附近
        else:
            i += 1
    return pd.DataFrame(rows, columns=["symbol", "volume", "currency", "closing_price", "market_value"])

def main():
    if len(sys.argv) < 2:
        print('Usage: {} "statement.pdf"'.format(sys.argv[0]))
        sys.exit(1)

    password = None
    with open('auth/stmt.txt', 'r') as f:
        password = f.read()[:-1]
    tokens = []
    with pdfplumber.open(sys.argv[1], password=password) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            page_lines = [l.strip() for l in text.splitlines() if l.strip()]
            for ln in page_lines:
                tokens.extend(re.sub('；', ' ', ln).split())

    statement_at = pick_kv(tokens, "結單日期：")
    subs = slice_between(tokens, "財務概況", "財務明細")
    overview = {
        "statement_at": statement_at,
        "balance": as_number(pick_next_number_after(subs, "現金結餘：")),
        "unsettled": as_number(pick_next_number_after(subs, "待交收金額：")),
        "usd_hkd_rate": as_number(pick_kv(subs, "参考匯率：USD->HKD")),
        "market_value": as_number(pick_next_number_after(subs, "總市值：")),
        "net_equity": as_number(pick_next_number_after(subs, "資產淨值（不含利息）：")),
        "hkd_cash": as_number(pick_next_number_after(subs, "港元")),   # 4,253.27
        "usd_cash": as_number(pick_next_number_after(subs, "美元")),   # 21,903.78（原币种金额）
        "hk_stock": as_number(pick_next_number_after(subs, "港股")),   # 128,726.82
        "us_stock": as_number(pick_next_number_after(subs, "美股")),   # 670,035.52
        "fund": as_number(pick_next_number_after(subs, "基金")),   # 561,249.32
    }
    pprint(overview)
    print(parse_holding_summary(tokens))


if __name__ == "__main__":
    main()
