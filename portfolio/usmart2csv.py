#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import re
import csv
import argparse
from decimal import Decimal, InvalidOperation

MAP = {
    "买入股票": "TRADE_BUY",
    "卖出股票": "TRADE_SELL",
    "买入股票费用": "TRADE_FEE",
    "卖出股票费用": "TRADE_FEE",
    "红利额": "DIVIDEND",
    "美国税费": "DIVIDEND_TAX",
    "优惠券": "REBATE",
    "普通入金": "CASH_IN",
    "普通出金": "CASH_OUT",
    "融资利息": "MARGIN_INTEREST_PRINCIPAL"
}

RE_MONTH = re.compile(r"^\d{4}-\d{2}$")
RE_DATETIME = re.compile(r"\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2}")
RE_AMOUNT = re.compile(r"^[+-]?\d+(\.\d+)?$")


def is_month_line(line: str) -> bool:
    return bool(RE_MONTH.match(line.strip()))


def parse_amount(line: str):
    s = line.strip()
    try:
        return str(Decimal(s))
    except (InvalidOperation, ValueError):
        return None


def extract_symbol_and_time(line: str):
    """
    处理：
    - 'IBIT iShares Bitcoin Trust'
    - 'IBIT iShares Bitcoin Trust 2024-12-20 10:28:29'
    """
    line = line.strip()
    m = RE_DATETIME.search(line)

    if m:
        time = m.group(0)
        symbol_part = line[:m.start()].strip()
    else:
        time = None
        symbol_part = line

    # symbol 只取第一个 word
    symbol = symbol_part.split()[0] if symbol_part else "CASH_USD"
    return symbol, time


def parse_file(path: str):
    records = []

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]

    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]

        # 跳过月份行
        if is_month_line(line):
            i += 1
            continue

        # 1) type
        tx_type = line
        i += 1
        if i >= n:
            break

        # 2) amount
        amount = parse_amount(lines[i])
        if amount is None:
            raise SystemExit(f"[解析失败] 金额行异常: {lines[i]}")
        i += 1
        if i >= n:
            break

        # 3) symbol (+ maybe time)
        symbol, occurred_at = extract_symbol_and_time(lines[i])
        i += 1

        # 4) time（如果没在上一行拿到）
        if occurred_at is None:
            if i >= n or not RE_DATETIME.match(lines[i]):
                raise SystemExit(
                    f"[人工检查] 缺少时间行，type={tx_type}, symbol={symbol}"
                )
            occurred_at = lines[i]
            i += 1

        records.append({
            "occurred_at": occurred_at,
            "biz_type_code": MAP[tx_type],
            "amount": amount,
            "symbol": symbol,
        })

    return records


def write_csv(records, out_path: str):
    with open(out_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["occurred_at", "biz_type_code", "amount", "symbol"]
        )
        writer.writeheader()
        for r in records:
            writer.writerow(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="资金流水文本文件")
    ap.add_argument("-o", "--out", default="broker_cashflow.csv", help="输出CSV文件")
    args = ap.parse_args()

    records = parse_file(args.input)
    write_csv(records, args.out)

    print(f"OK: parsed {len(records)} records -> {args.out}")


if __name__ == "__main__":
    main()