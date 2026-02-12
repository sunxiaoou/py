#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from pprint import pprint

import numpy as np
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

def pick_next_number_after(seq, key, alt=None):
    keys = [key]
    if alt is not None:
        if isinstance(alt, (list, tuple, set)):
            keys.extend(list(alt))
        else:
            keys.append(alt)
    for i, tok in enumerate(seq):
        if tok not in keys:
            continue
        i += 1
        if _num_re.match(seq[i]):
            return seq[i]
    assert False, f"Cannot find number after '{key}' (or alt '{alt}') in sequence"

def extract_unsettled_totals(tokens):
    sec = slice_between(tokens, "待结算交易", "持倉摘要")
    if not sec:
        sec = slice_between(tokens, "待結算交易", "持倉摘要")
    hkd_total = 0.0
    usd_total = 0.0
    i = 0
    while i < len(sec):
        tok = sec[i]
        if tok in ("HKD", "USD"):
            nums = []
            j = i + 1
            while j < len(sec) and len(nums) < 3:
                if not _num_re.match(sec[j]):
                    break
                nums.append(as_number(sec[j]))
                j += 1
            if len(nums) == 3 or 'SAFEKEEPING' == sec[j]:
                if tok == "HKD":
                    hkd_total += nums[-1]
                else:
                    usd_total += nums[-1]
            i = j
        else:
            i += 1
    return round(hkd_total, 2), round(usd_total, 2)

def parse_overview_old(tokens: list[str]) -> dict:
    subs = slice_between(tokens, "賬號：", "中央編號：")
    dic =  {
        "period_yyyymm": os.path.basename(sys.argv[1])[:6],
        "market_value": as_number(pick_next_number_after(subs, "投資組合價值：")),
        "net_equity": as_number(pick_next_number_after(subs, "資產淨值（不含利息）："))}
    if "hk" in sys.argv[1].lower():
        dic['hkd_cash'] = as_number(pick_next_number_after(subs, "未到期結餘："))
    elif "us" in sys.argv[1].lower():
        dic['usd_cash'] = as_number(pick_next_number_after(subs, "未到期結餘："))
    return dic

def parse_holding_summary_old(tokens) -> list[dict]:
    sec = slice_between(tokens, "投資總結", "總額：")
    rows = []
    i = 0
    while i < len(sec):
        tok = sec[i]
        if isinstance(tok, str) and tok.startswith("#"):
            symbol = tok[1:]
            j = i + 1
            while j < len(sec) and not _num_re.match(sec[j]):
                j += 1
            nums = []
            k = j
            while k < len(sec) and len(nums) < 6 and _num_re.match(sec[k]):
                nums.append(as_number(sec[k]))
                k += 1
            if len(nums) == 6:
                rows.append({"symbol": symbol,
                             "volume": nums[3],
                             "currency": "HKD" if "hk" in sys.argv[1].lower() else "USD",
                             "closing_price": nums[4],
                             "market_value": nums[5]})
            i = k
        else:
            i += 1
    return rows

def convert_holding_summary_old(tokens: list[str]) -> pd.DataFrame:
    overview = parse_overview_old(tokens)
    # pprint(overview)
    rows = parse_holding_summary_old(tokens)
    if 'hkd_cash' in overview:
        rows.append({"symbol": 'CASH_HKD', "currency": 'HKD', "market_value": overview["hkd_cash"]})
    elif 'usd_cash' in overview:
        rows.append({"symbol": 'CASH_USD', "currency": 'USD', "market_value": overview["usd_cash"]})
    df = pd.DataFrame(rows, columns=["symbol", "volume", "currency", "closing_price", "market_value"])
    total_mv = overview['net_equity']
    mv_sum = round(df['market_value'].sum(), 2)
    assert total_mv == mv_sum, print("total_mv({}) != mv_sum({})".format(total_mv, mv_sum))
    df['broker_name'] = "ValuableCapital"
    df['period_yyyymm'] = int(overview['period_yyyymm'])
    df['usd_hkd_rate'] = np.nan
    df['cny_rate'] = np.nan
    return df[["broker_name", "period_yyyymm", "symbol", "currency", "volume", "closing_price", "market_value",
               "usd_hkd_rate", "cny_rate"]]

def parse_overview(tokens) -> dict:
    subs = slice_between(tokens, "財務概況", "財務明細")
    return {
        "period_yyyymm": os.path.basename(sys.argv[1])[:6],
        "balance": as_number(pick_next_number_after(subs, "現金結餘：", ["現⾦結餘：", "現金結餘①："])),
        "unsettled": as_number(pick_next_number_after(subs, "待交收金額：", ["待交收⾦額：", "待交收金額②："])),
        "usd_hkd_rate": as_number(pick_kv(subs, "参考匯率：USD->HKD")),
        "cny_hkd_rate": as_number(pick_kv(subs, "CNY->HKD")),
        "market_value": as_number(pick_next_number_after(subs, "總市值：", ["總市值③："])),
        "net_equity": as_number(pick_next_number_after(subs, "資產淨值（不含利息）：", ["資產淨值（不含利息）④："])),
        "hkd_cash": as_number(pick_next_number_after(subs, "港元")),
        "usd_cash": as_number(pick_next_number_after(subs, "美元")),
        "hk_stock": as_number(pick_next_number_after(subs, "港股", ["股票"])),
        "us_stock": as_number(pick_next_number_after(subs, "美股", ["債券及結構性"])),
        "fund": as_number(pick_next_number_after(subs, "基金", ["基⾦"]))}

def parse_holding_summary(tokens) -> list[dict]:
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
                    if j + 1 < len(hold_sec):
                        closing_price = as_number(hold_sec[j+1])
                    if j + 2 < len(hold_sec):
                        market_value = as_number(hold_sec[j+2])
                    break
                elif hold_sec[j] in ("HKD", "USD", "CNY") and _num_re.match(hold_sec[j-1]):
                    vol = as_number(hold_sec[j-1])
                    ccy = hold_sec[j]
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
    return rows

def convert_holding_summary(tokens: list[str]) -> pd.DataFrame:
    overview = parse_overview(tokens)
    # pprint(overview)
    h, u = extract_unsettled_totals(tokens)
    rows = parse_holding_summary(tokens)
    rows.append({"symbol": 'CASH_HKD', "currency": 'HKD', "market_value": round(overview["hkd_cash"] + h, 2)})
    rows.append({"symbol": 'CASH_USD', "currency": 'USD', "market_value": round(overview["usd_cash"] + u, 2)})
    df = pd.DataFrame(rows, columns=["symbol", "volume", "currency", "closing_price", "market_value"])
    df['broker_name'] = "ValuableCapital"
    df['period_yyyymm'] = int(overview['period_yyyymm'])
    df['usd_hkd_rate'] = df['currency'].apply(lambda x: 1 if x == 'HKD' else overview['usd_hkd_rate'])
    total_mv = overview['net_equity']
    df['hkd_equivalent'] = df['market_value'] * df['usd_hkd_rate']
    mv_sum = round(df['hkd_equivalent'].sum(), 2)
    assert abs(total_mv - mv_sum) < 0.1, \
        print("total_mv({}) - mv_sum({}) = {}".format(total_mv, mv_sum, round(total_mv - mv_sum, 2)))
    hr = round(1 / overview['cny_hkd_rate'], 4)
    ur = round(overview['usd_hkd_rate'] / overview['cny_hkd_rate'], 4)
    df['cny_rate'] = df['currency'].apply(lambda x: hr if x == 'HKD' else ur)
    return df[["broker_name", "period_yyyymm", "symbol", "currency", "volume", "closing_price", "market_value",
             "usd_hkd_rate", "cny_rate"]]

def main():
    if len(sys.argv) < 3:
        print('Usage: {} "statement.pdf" "out_dir"'.format(sys.argv[0]))
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
    # pprint(tokens)
    basename = os.path.basename(sys.argv[1])
    out_dir = sys.argv[2].rstrip('/')
    os.makedirs(out_dir, exist_ok=True)
    if int(basename[:6]) < 202209:
        df = convert_holding_summary_old(tokens)
        csv = out_dir + '/' + basename[:6] + ('_hk.csv' if 'HK' in basename else '_us.csv')
    else:
        df = convert_holding_summary(tokens)
        csv = out_dir + '/' + basename[:6] + '.csv'
    df.to_csv(csv, index=False, encoding='utf-8-sig')
    print(f"Extracted {len(df)} rows from {sys.argv[1]} to {csv}")


if __name__ == "__main__":
    main()
