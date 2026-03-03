#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
import csv
import os
import re
import sys

import pdfplumber

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

def idx_of(seq, needle) -> int:
    """返回 needle 在 seq 中首次出现的位置，不存在返回 -1"""
    try:
        return seq.index(needle)
    except ValueError:
        return -1

def slice_between(seq: list, start_token: str, end_token: str, end_token2=None) -> list:
    """截取 seq 中 (start_token 之后) 到 (end_token 之前) 的子序列；找不到则返回空"""
    s = idx_of(seq, start_token)
    if s < 0:
        return []
    e = idx_of(seq[s+1:], end_token)
    if e < 0:
        e = idx_of(seq[s+1:], end_token2) if end_token2 else -1
        if e < 0:
            return []
    return seq[s+1: s+1+e]

def parse_settled_funds(tokens):
    sec = slice_between(tokens, 'SETTLED', 'UNSETTLED', 'HOLDING')
    rows = []
    i = 0
    while i < len(sec) and sec[i] != 'Funds':
        i += 1
    i += 1
    while i < len(sec):
        if sec[i].startswith('#HK'):
            symbol = sec[i][1:]
            j = i + 1
            while j < len(sec) and not re.compile(r"^\d\d\d\d-\d\d-\d\d$").match(sec[j]):
                j += 1
            date = sec[j]
            j += 1
            while j < len(sec) and not sec[j] in ['HKD', 'USD']:
                j += 1
            volume = as_number(sec[j + 1])
            price = as_number(sec[j + 2])
            market_value = as_number(sec[j + 3])
            mv = round(volume * price, 2)
            diff = abs(market_value) - mv
            assert diff < 0.1, print("market_value({}) - mv({}) = {}".format(abs(market_value), mv, diff))
            rows.append({"occurred_at": date, "symbol": symbol, "volume": volume, "market_value": market_value})
            i = j + 4
        else:
            i += 1
    return rows

def get_tokens_from_pdf(pdf_path: str) -> list[str]:
    auth = 'auth/' + ('stmt_futu' if '1771' in pdf_path.lower() else 'stmt') + '.txt'
    password = None
    with open(auth, 'r') as f:
        password = f.read()[:-1]
    tokens = []
    with pdfplumber.open(pdf_path, password=password) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            page_lines = [l.strip() for l in text.splitlines() if l.strip()]
            for ln in page_lines:
                tokens.extend(re.sub('；', ' ', ln).split())
    return tokens

def extract_numeric_prefix(s: str) -> str:
    match = re.match(r'^\d+', s)
    if match:
        return match.group()
    raise ValueError(f"Cannot extract numeric prefix from '{s}'")

def save_rows_to_csv(rows: list, filename: str):
    fieldnames = list(rows[0].keys())
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    if len(sys.argv) < 3:
        print('Usage: {} "statement.pdf" "out_dir"'.format(sys.argv[0]))
        sys.exit(1)

    tokens = get_tokens_from_pdf(sys.argv[1])
    basename = os.path.basename(sys.argv[1])
    out_dir = sys.argv[2].rstrip('/')
    os.makedirs(out_dir, exist_ok=True)

    if int(basename[:6]) >= 202209:
        rows = parse_settled_funds(tokens)
        if rows:
            file = out_dir + '/' + extract_numeric_prefix(basename) + '.csv'
            save_rows_to_csv(rows, file)
            print(f"Saved {len(rows)} rows to {file}")
        else:
            print("No settled funds found in the statement.")
    else:
        print("Statement date is before 2022-09, skipping.")

if __name__ == "__main__":
    main()
