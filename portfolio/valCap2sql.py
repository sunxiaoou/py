#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# 业务类型映射
BIZ_MAP = {
    "股息": "DIVIDEND",
    "股息税": "DIVIDEND_TAX",

    "买入证券": "BUY",
    "卖出证券": "SELL",

    "证券交易费用": "TRADE_FEE",

    # OCR里出现“资金转入 / 存入资金”
    "资金转入": "CASH_IN",
    "存入资金": "CASH_IN",
    "资金转出": "CASH_OUT",

    # 港股部分出现
    "股息手续费": "DIVIDEND_FEE",
    "紅股手续费": "BONUS_SHARE_FEE",

    # 美股里出现
    "ADR保管费": "ADR_FEE",
}

# --- 正则 ---
RE_PAGE_NOISE = re.compile(r"^\s*(第\d+页|文字识别结果)\s*$")

RE_MONTH = re.compile(r"^\s*(\d{4})年(\d{1,2})月\s*$")

# “流入10,036.44 USD” 或 “流出 5,349.67 USD” 或 “流出30,000.73 USD”
RE_SUMMARY_ONE_LINE = re.compile(
    r"^\s*(流入|流出)\s*([\d,]+(?:\.\d+)?)\s*([A-Z]{3})\s*$"
)

# “流出”单独一行（金额被OCR到下一行）
RE_SUMMARY_SPLIT_HEAD = re.compile(r"^\s*(流入|流出)\s*$")
RE_SUMMARY_SPLIT_TAIL = re.compile(r"^\s*([\d,]+(?:\.\d+)?)\s*([A-Z]{3})\s*$")

# 金额行：＋25.00 / －2.50 / -5,344.00
RE_AMOUNT = re.compile(r"^\s*([＋\+－-])\s*([\d,]+(?:\.\d+)?)\s*$")

# 时间行：12-30 16:04:03
RE_DT = re.compile(r"^\s*(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})\s*$")

# 证券行：允许 symbol 与名称之间没空格（AAPL苹果 / GS高盛 / 00388香港交易所）
# 规则：开头一段作为symbol（字母/数字/._-），后面剩余作为名字（可为空）
RE_SEC = re.compile(r"^\s*([A-Za-z0-9._-]+)\s*(.*)\s*$")


def _skip_blanks_and_noise(lines, idx):
    n = len(lines)
    while idx < n:
        s = lines[idx].strip()
        if not s:
            idx += 1
            continue
        if RE_PAGE_NOISE.match(s):
            idx += 1
            continue
        # 你文件里也可能出现“...”占位
        if s == "..." or s == "…":
            idx += 1
            continue
        return idx
    return idx


def _to_decimal_amount(line: str) -> Decimal:
    m = RE_AMOUNT.match(line)
    if not m:
        raise ValueError(f"Bad amount line: {line!r}")
    sign = m.group(1)
    num = m.group(2).replace(",", "")
    val = Decimal(num)
    if sign in ("－", "-"):
        val = -val
    # 保留2位
    return val.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _parse_datetime_with_year(line: str, year: int) -> str:
    m = RE_DT.match(line)
    if not m:
        raise ValueError(f"Bad datetime line: {line!r}")
    month, day, hh, mm, ss = map(int, m.groups())
    dt = datetime(year, month, day, hh, mm, ss)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _read_month_summary(lines, idx):
    """
    读取 “流入/流出 汇总 + 币种”
    允许：
      - 一行式：流入10,036.44 USD
      - 拆行式：流出 \n 60.00 HKD
    返回 (in_total, out_total, currency, new_idx)
    """
    idx = _skip_blanks_and_noise(lines, idx)
    if idx >= len(lines):
        raise ValueError("Unexpected EOF when reading monthly summary")

    in_total = None
    out_total = None
    currency = None

    # 需要读到同时拿到流入和流出
    while idx < len(lines) and (in_total is None or out_total is None):
        idx = _skip_blanks_and_noise(lines, idx)
        if idx >= len(lines):
            break

        line = lines[idx].strip()

        # 如果遇到下个月标题，说明本月summary不完整（OCR坏了）
        if RE_MONTH.match(line):
            raise ValueError(f"Monthly summary incomplete before next month header at line {idx+1}")

        m1 = RE_SUMMARY_ONE_LINE.match(line)
        if m1:
            kind, amt, cur = m1.group(1), m1.group(2), m1.group(3)
            amt_d = Decimal(amt.replace(",", "")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if currency is None:
                currency = cur
            elif currency != cur:
                raise ValueError(f"Mixed currency in one month summary: {currency} vs {cur} at line {idx+1}")

            if kind == "流入":
                in_total = amt_d
            else:
                out_total = amt_d
            idx += 1
            continue

        mhead = RE_SUMMARY_SPLIT_HEAD.match(line)
        if mhead:
            kind = mhead.group(1)
            idx += 1
            idx = _skip_blanks_and_noise(lines, idx)
            if idx >= len(lines):
                raise ValueError("EOF after summary head line")
            mtail = RE_SUMMARY_SPLIT_TAIL.match(lines[idx].strip())
            if not mtail:
                raise ValueError(f"Bad split summary tail line: {lines[idx]!r} (after {kind})")
            amt, cur = mtail.group(1), mtail.group(2)
            amt_d = Decimal(amt.replace(",", "")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            if currency is None:
                currency = cur
            elif currency != cur:
                raise ValueError(f"Mixed currency in one month summary: {currency} vs {cur} at line {idx+1}")

            if kind == "流入":
                in_total = amt_d
            else:
                out_total = amt_d
            idx += 1
            continue

        # 可能是OCR噪声行：跳过
        idx += 1

    if in_total is None or out_total is None or currency is None:
        raise ValueError(f"Failed to read complete monthly summary (in/out/currency). Got in={in_total}, out={out_total}, cur={currency}")

    return in_total, out_total, currency, idx


def parse_records(lines: list[str], default_cash_symbol_prefix: str = "CASH_", strict_month_check: bool = True):
    """
    按月解析：每月结构
      YYYY年MM月
      流入xxx CUR
      流出yyy CUR
      ... 若干条流水

    校验：本月流水正数求和 == 流入；负数绝对值求和 == 流出（允许误差）
    若对不上：raise SystemExit 退出（转人工）
    """
    records = []
    idx = 0
    n = len(lines)

    # 金额校验容差：考虑OCR把 0.60 -> 0.6 / 细小误差；这里给 0.01 容差
    TOL = Decimal("0.01")

    while True:
        idx = _skip_blanks_and_noise(lines, idx)
        if idx >= n:
            break

        # 找月标题
        mmonth = RE_MONTH.match(lines[idx].strip())
        if not mmonth:
            # 不是月标题就跳过（比如页眉、杂行）
            idx += 1
            continue

        year = int(mmonth.group(1))
        month = int(mmonth.group(2))
        idx += 1

        # 读取本月汇总(流入/流出/币种)
        in_total, out_total, cur, idx = _read_month_summary(lines, idx)

        # 本月累计
        month_in_sum = Decimal("0.00")
        month_out_sum = Decimal("0.00")

        # 解析本月流水直到下一个月标题或EOF
        while True:
            idx = _skip_blanks_and_noise(lines, idx)
            if idx >= n:
                break

            line = lines[idx].strip()
            # 下个月标题 -> 结束本月
            if RE_MONTH.match(line):
                break

            # 业务类型
            biz_name = line
            if biz_name not in BIZ_MAP:
                # OCR可能把“股息税”识别成近似字：这里宁可失败转人工
                raise SystemExit(f"[人工检查] 未识别的业务类型: {biz_name!r} (行 {idx+1})，月份 {year}-{month:02d}")

            biz_type_code = BIZ_MAP[biz_name]
            idx += 1

            # 金额行
            idx = _skip_blanks_and_noise(lines, idx)
            if idx >= n:
                raise SystemExit(f"[人工检查] {biz_name} 后缺少金额行，月份 {year}-{month:02d}")
            try:
                amount = _to_decimal_amount(lines[idx].strip())
            except Exception as e:
                raise SystemExit(f"[人工检查] 金额行解析失败(行 {idx+1}): {lines[idx]!r}，月份 {year}-{month:02d}，错误: {e}")
            idx += 1

            # 更新本月汇总
            if amount >= 0:
                month_in_sum += amount
            else:
                month_out_sum += (-amount)

            # 下一行：可能是证券行，也可能直接是时间行（资金进出）
            idx = _skip_blanks_and_noise(lines, idx)
            if idx >= n:
                raise SystemExit(f"[人工检查] {biz_name} 后缺少时间/证券行，月份 {year}-{month:02d}")

            symbol = None
            security_name = None

            if RE_DT.match(lines[idx].strip()):
                occurred_at = _parse_datetime_with_year(lines[idx].strip(), year)
                idx += 1
            else:
                msec = RE_SEC.match(lines[idx].strip())
                if not msec:
                    raise SystemExit(f"[人工检查] 预期证券行或时间行，但得到(行 {idx+1}): {lines[idx]!r}，月份 {year}-{month:02d}")
                symbol = msec.group(1).strip()
                security_name = (msec.group(2) or "").strip() or None
                idx += 1

                idx = _skip_blanks_and_noise(lines, idx)
                if idx >= n or not RE_DT.match(lines[idx].strip()):
                    raise SystemExit(f"[人工检查] 证券行后缺少时间行(行 {idx+1})，月份 {year}-{month:02d}")
                occurred_at = _parse_datetime_with_year(lines[idx].strip(), year)
                idx += 1

            # 没有证券的流水（资金进出），用 CASH_<CUR>
            if symbol is None:
                symbol = f"{default_cash_symbol_prefix}{cur}"

            records.append({
                "occurred_at": occurred_at,
                "biz_type_code": biz_type_code,
                "amount": amount,          # Decimal
                "symbol": symbol,
                "currency": cur,           # 可选保留，便于调试
                "security_name": security_name,
                "biz_name": biz_name,
                "month": f"{year}-{month:02d}",
            })

        # 本月结束：做校验
        if strict_month_check:
            in_diff = (month_in_sum - in_total).copy_abs()
            out_diff = (month_out_sum - out_total).copy_abs()

            if in_diff > TOL or out_diff > TOL:
                raise SystemExit(
                    "[人工检查] 月度汇总校验失败："
                    f"月份 {year}-{month:02d} {cur}；"
                    f"汇总流入={in_total}，解析流入={month_in_sum}，差={month_in_sum - in_total}；"
                    f"汇总流出={out_total}，解析流出={month_out_sum}，差={month_out_sum - out_total}。"
                )

    return records


def sql_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "''")


def records_to_inserts(records, table="trade_ledger") -> str:
    out = []
    for r in records:
        amt = r["amount"].quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        out.append(
            f"INSERT INTO {table} (occurred_at, biz_type_code, amount, symbol) VALUES ("
            f"'{sql_escape(r['occurred_at'])}', "
            f"'{sql_escape(r['biz_type_code'])}', "
            f"{amt}, "
            f"'{sql_escape(r['symbol'])}'"
            f");"
        )
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="OCR text file")
    ap.add_argument("--table", default="trade_ledger")
    ap.add_argument("--cash-prefix", default="CASH_",
                    help="symbol prefix for cash flows without security line, e.g. CASH_ => CASH_USD/CASH_HKD")
    ap.add_argument("--no-month-check", action="store_true",
                    help="disable monthly in/out validation (not recommended)")
    args = ap.parse_args()

    text = open(args.input, "r", encoding="utf-8").read()
    lines = [ln.rstrip("\n") for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]

    records = parse_records(
        lines,
        default_cash_symbol_prefix=args.cash_prefix,
        strict_month_check=(not args.no_month_check),
    )

    print(records_to_inserts(records, table=args.table))


if __name__ == "__main__":
    main()
