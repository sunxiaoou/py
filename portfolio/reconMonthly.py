#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
from datetime import datetime
import pandas as pd

from mysql import MySql


def month_start(yyyymm: int) -> str:
    """Return month start timestamp string for given YYYYMM."""
    y = yyyymm // 100
    m = yyyymm % 100
    start = datetime(y, m, 1)
    return start.strftime("%Y-%m-%d %H:%M:%S")


def month_end_exclusive(yyyymm: int) -> str:
    """Return end-exclusive timestamp string for given YYYYMM."""
    return month_start(next_month(yyyymm))


def next_month(yyyymm: int) -> int:
    y = yyyymm // 100
    m = yyyymm % 100
    if m == 12:
        return (y + 1) * 100 + 1
    return y * 100 + (m + 1)


def prev_month(yyyymm: int) -> int:
    y = yyyymm // 100
    m = yyyymm % 100
    if m == 1:
        return (y - 1) * 100 + 12
    return y * 100 + (m - 1)


def validate_yyyymm(yyyymm: int) -> None:
    y = yyyymm // 100
    m = yyyymm % 100
    if y < 1900 or not (1 <= m <= 12):
        raise ValueError(f"Invalid YYYYMM: {yyyymm}")


# === SQL: 读取 trade_ledger 区间 [start, end) ===
TRADE_LEDGER_SQL = """
SELECT
  l.id,
  l.occurred_at,
  l.biz_type_code,
  l.amount,
  l.volume,
  l.symbol,
  l.currency
FROM trade_ledger l
WHERE l.occurred_at >= :start_time
  AND l.occurred_at < :end_time
  AND l.broker_name = :broker_name
ORDER BY l.occurred_at, l.id;
"""

# === SQL: 读取月结单 item ===
STMT_ITEMS_SQL = """
SELECT
  symbol,
  volume,
  currency,
  market_value
FROM broker_statement_monthly
WHERE broker_name = :broker_name
  AND period_yyyymm = :yyyymm;
"""


def compute_from_trade_ledger(trades: pd.DataFrame):
    """
    反推：
    - cash: currency, cash_balance_delta  （所有流水金额按 currency 累加）
    - pos : symbol, position_qty_delta    （BUY/SELL 等 volume 累加）
    """
    # 1) cash: 按币种汇总所有流水金额（不限制 symbol）
    if not trades.empty:
        cash = (trades.groupby("currency", as_index=False)["amount"]
                .sum()
                .rename(columns={"amount": "cash_balance"}))
    else:
        cash = pd.DataFrame(columns=["currency", "cash_balance"])

    # 2) positions
    trd = trades[trades["biz_type_code"]
        .isin(["TRADE_BUY", "TRADE_SELL", "FUND_SUBSCRIPTION", "FUND_REDEMPTION", "IPO_REFUND", "OTHER"])].copy()
    trd = trd[trd["volume"].notna()].copy()
    if not trd.empty:
        trd["signed_qty"] = trd.apply(
            lambda r: (r["volume"] if r["biz_type_code"] in ["TRADE_BUY", "FUND_SUBSCRIPTION", "IPO_REFUND", "OTHER"]
                       else -r["volume"]),
            axis=1
        )
        pos = (trd.groupby("symbol", as_index=False)["signed_qty"]
               .sum()
               .rename(columns={"signed_qty": "position_qty"}))
    else:
        pos = pd.DataFrame(columns=["symbol", "position_qty"])

    return cash, pos


def normalize_stmt_items(stmt_items: pd.DataFrame):
    """
    从 broker_statement_monthly 取：
    - CASH: currency, cash_balance （使用 market_value 字段作为现金余额）
    - POSITION: symbol, position_qty （使用 volume 字段作为持仓数量）
    """
    if stmt_items.empty:
        return (
            pd.DataFrame(columns=["currency", "cash_balance"]),
            pd.DataFrame(columns=["symbol", "position_qty"]),
        )

    # CASH
    cash = stmt_items[stmt_items["symbol"].str.startswith("CASH")].copy()
    if not cash.empty:
        stmt_cash = (cash.groupby("currency", as_index=False)["market_value"]
                     .sum()
                     .rename(columns={"market_value": "cash_balance"}))
    else:
        stmt_cash = pd.DataFrame(columns=["currency", "cash_balance"])

    # POSITION
    pos = stmt_items[~(stmt_items["symbol"].str.startswith("CASH"))].copy()
    if not pos.empty:
        stmt_pos = (pos.groupby("symbol", as_index=False)["volume"]
                    .sum()
                    .rename(columns={"volume": "position_qty"}))
    else:
        stmt_pos = pd.DataFrame(columns=["symbol", "position_qty"])

    return stmt_cash, stmt_pos


def add_tables(base: pd.DataFrame, delta: pd.DataFrame, key_cols, val_col):
    """
    base + delta，返回同结构表。
    """
    b = base.copy()
    d = delta.copy()

    for k in key_cols:
        b[k] = b[k].astype(str)
        d[k] = d[k].astype(str)

    merged = b.merge(d, on=key_cols, how="outer", suffixes=("_base", "_delta"))
    bcol = f"{val_col}_base"
    dcol = f"{val_col}_delta"
    merged[bcol] = merged[bcol].fillna(0)
    merged[dcol] = merged[dcol].fillna(0)
    merged[val_col] = merged[bcol] + merged[dcol]

    return merged[key_cols + [val_col]].sort_values(by=key_cols).reset_index(drop=True)


def diff_tables(left: pd.DataFrame, right: pd.DataFrame, key_cols, val_col,
                left_name="calc", right_name="stmt"):
    l = left.copy()
    r = right.copy()
    for k in key_cols:
        l[k] = l[k].astype(str)
        r[k] = r[k].astype(str)

    merged = l.merge(r, on=key_cols, how="outer", suffixes=(f"_{left_name}", f"_{right_name}"))

    lcol = f"{val_col}_{left_name}"
    rcol = f"{val_col}_{right_name}"
    merged[lcol] = merged[lcol].fillna(0)
    merged[rcol] = merged[rcol].fillna(0)
    merged["diff"] = merged[lcol] - merged[rcol]

    return merged.sort_values(by=key_cols).reset_index(drop=True)


def load_stmt_snapshot(db: MySql, broker: str, yyyymm: int):
    stmt_items = db.to_frame_with_params(
        STMT_ITEMS_SQL,
        {"broker_name": broker, "yyyymm": yyyymm}
    )
    return normalize_stmt_items(stmt_items)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--broker", default="ValuableCapital", help="broker_name, default ValuableCapital")
    ap.add_argument("--period", type=int, default=None,
                    help="legacy single-point mode: reconcile from beginning to this month-end snapshot, e.g. 202212")
    ap.add_argument("--start-period", type=int, default=None,
                    help="range mode start period_yyyymm (inclusive), must be used together with --end-period")
    ap.add_argument("--end-period", type=int, default=None,
                    help="range mode end period_yyyymm (exclusive). Example: --start-period 202301 --end-period 202302 means reconcile 202301 only")
    ap.add_argument("--out-dir", default=".", help="output dir for CSV diffs")
    ap.add_argument("--tolerance", type=float, default=0.1, help="tolerance for diff (e.g. 1e-6)")
    args = ap.parse_args()

    # mode validation
    legacy_mode = args.period is not None
    range_mode = args.start_period is not None or args.end_period is not None

    if legacy_mode and range_mode:
        raise ValueError("Use either legacy --period mode, or range mode --start-period + --end-period, but not both")

    if not legacy_mode and not range_mode:
        raise ValueError("Must specify either --period, or --start-period together with --end-period")

    if legacy_mode:
        validate_yyyymm(args.period)
    else:
        if args.start_period is None or args.end_period is None:
            raise ValueError("Range mode requires both --start-period and --end-period")
        validate_yyyymm(args.start_period)
        validate_yyyymm(args.end_period)
        if args.start_period >= args.end_period:
            raise ValueError(f"--start-period must be smaller than --end-period: {args.start_period} >= {args.end_period}")

    db = MySql()
    tol = float(args.tolerance)

    if legacy_mode:
        # 兼容旧行为：从“系统开始”累计到 args.period 月末，与该月月结单比较
        start_time = "1000-01-01 00:00:00"
        end_time = month_end_exclusive(args.period)

        trades = db.to_frame_with_params(
            TRADE_LEDGER_SQL,
            {"start_time": start_time, "end_time": end_time, "broker_name": args.broker}
        )
        stmt_cash, stmt_pos = load_stmt_snapshot(db, args.broker, args.period)

        calc_cash, calc_pos = compute_from_trade_ledger(trades)

        recon_label = f"{args.period}"
        print(f"[MODE] legacy snapshot mode: from beginning to month_end<{end_time}, compare statement {args.period}")
    else:
        # 区间校验 [start_period, end_period)
        start_time = month_start(args.start_period)
        end_time = month_start(args.end_period)
        base_period = prev_month(args.start_period)
        target_period = prev_month(args.end_period)

        trades = db.to_frame_with_params(
            TRADE_LEDGER_SQL,
            {"start_time": start_time, "end_time": end_time, "broker_name": args.broker}
        )

        base_cash, base_pos = load_stmt_snapshot(db, args.broker, base_period)
        delta_cash, delta_pos = compute_from_trade_ledger(trades)
        stmt_cash, stmt_pos = load_stmt_snapshot(db, args.broker, target_period)

        calc_cash = add_tables(base_cash, delta_cash, ["currency"], "cash_balance")
        calc_pos = add_tables(base_pos, delta_pos, ["symbol"], "position_qty")

        recon_label = f"{args.start_period}_{args.end_period}"
        print(
            f"[MODE] range mode: [{args.start_period}, {args.end_period}) => [{start_time}, {end_time}), "
            f"base statement={base_period}, target statement={target_period}"
        )

    cash_diff = diff_tables(calc_cash, stmt_cash, ["currency"], "cash_balance")
    pos_diff = diff_tables(calc_pos, stmt_pos, ["symbol"], "position_qty")

    cash_bad = cash_diff[cash_diff["diff"].abs() > tol]
    pos_bad = pos_diff[pos_diff["diff"].abs() > tol]

    os.makedirs(args.out_dir, exist_ok=True)
    cash_csv = os.path.join(args.out_dir, f"recon_cash_{args.broker}_{recon_label}.csv")
    pos_csv = os.path.join(args.out_dir, f"recon_pos_{args.broker}_{recon_label}.csv")

    cash_diff.to_csv(cash_csv, index=False, encoding="utf-8-sig")
    pos_diff = pos_diff[~((pos_diff['position_qty_calc'] < 0.0001) & (pos_diff['position_qty_stmt'] < 0.0001))]
    pos_diff.to_csv(pos_csv, index=False, encoding="utf-8-sig")

    print(f"[OK] Recon broker={args.broker} range=[{start_time}, {end_time})")
    print(f"[OUT] {cash_csv}  (diff rows={len(cash_bad)})")
    print(f"[OUT] {pos_csv}   (diff rows={len(pos_bad)})")

    if len(cash_bad) or len(pos_bad):
        print("[WARN] Differences found (see CSV).")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
