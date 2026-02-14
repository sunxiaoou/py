#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import argparse
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text


def month_end_exclusive(yyyymm: int) -> str:
    """Return end-exclusive timestamp string for given YYYYMM."""
    y = yyyymm // 100
    m = yyyymm % 100
    if m == 12:
        end = datetime(y + 1, 1, 1)
    else:
        end = datetime(y, m + 1, 1)
    return end.strftime("%Y-%m-%d %H:%M:%S")


# === SQL: 读取 trade_ledger 到月末（< next month 1st day）===
TRADE_LEDGER_SQL = """
SELECT
  l.id,
  l.occurred_at,
  l.biz_type_code,
  l.amount,
  l.volume,
  l.symbol,
  s.currency
FROM trade_ledger l
JOIN security_master s ON l.symbol = s.symbol
WHERE l.occurred_at < :month_end AND l.broker_name = :broker_name
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
    - cash: currency, cash_balance  （CASH_* 的 amount 累加）
    - pos : symbol, position_qty    （BUY/SELL 的 volume 累加）
    """
    # 1) cash
    # cash_tr = trades[trades["symbol"].astype(str).str.startswith("CASH_")].copy()
    # if not cash_tr.empty:
    #     cash = (cash_tr.groupby("currency", as_index=False)["amount"]
    #             .sum()
    #             .rename(columns={"amount": "cash_balance"}))
    # else:
    #     cash = pd.DataFrame(columns=["currency", "cash_balance"])
    # 1) cash: 按币种汇总所有流水金额（不限制 symbol）
    if not trades.empty:
        cash = (trades.groupby("currency", as_index=False)["amount"]
                .sum()
                .rename(columns={"amount": "cash_balance"}))
    else:
        cash = pd.DataFrame(columns=["currency", "cash_balance"])

    # 2) positions
    trd = trades[trades["biz_type_code"].isin(["TRADE_BUY", "TRADE_SELL", "IPO_REFUND", "OTHER"])].copy()
    trd = trd[trd["volume"].notna()].copy()
    if not trd.empty:
        trd["signed_qty"] = trd.apply(
            lambda r: (r["volume"] if r["biz_type_code"] in ["TRADE_BUY", "IPO_REFUND", "OTHER"] else -r["volume"]),
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
    从 broker_statement_monthly_item 取：
    - CASH: currency, cash_balance （使用 volume 字段作为现金余额）
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
        # 允许一币种多行：groupby 汇总（通常你是 unique(symbol)，但这里更稳）
        stmt_cash = (cash.groupby("currency", as_index=False)["market_value"]
                     .sum()
                     .rename(columns={"market_value": "cash_balance"}))
    else:
        stmt_cash = pd.DataFrame(columns=["currency", "cash_balance"])

    # POSITION
    pos = stmt_items[~(stmt_items["symbol"].str.startswith("CASH") | stmt_items["symbol"].str.startswith("HK0"))].copy()
    if not pos.empty:
        stmt_pos = (pos.groupby("symbol", as_index=False)["volume"]
                    .sum()
                    .rename(columns={"volume": "position_qty"}))
    else:
        stmt_pos = pd.DataFrame(columns=["symbol", "position_qty"])

    return stmt_cash, stmt_pos


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mysql-url", default=os.getenv("MYSQL_URL"),
                    help="SQLAlchemy URL, e.g. mysql+pymysql://user:pass@host:3306/db?charset=utf8mb4")
    ap.add_argument("--broker", default="ValuableCapital", help="broker_name, default DEFAULT")
    ap.add_argument("--period", type=int, required=True, help="period_yyyymm, e.g. 202012")
    ap.add_argument("--out-dir", default=".", help="output dir for CSV diffs")
    ap.add_argument("--tolerance", type=float, default=0.0, help="tolerance for diff (e.g. 1e-6)")
    args = ap.parse_args()

    if not args.mysql_url:
        raise SystemExit("Missing --mysql-url or env MYSQL_URL")

    month_end = month_end_exclusive(args.period)
    engine = create_engine(args.mysql_url, pool_pre_ping=True)

    with engine.connect() as conn:
        trades = pd.read_sql(text(TRADE_LEDGER_SQL), conn, params={"month_end": month_end, "broker_name": args.broker})
        stmt_items = pd.read_sql(text(STMT_ITEMS_SQL), conn, params={"broker_name": args.broker, "yyyymm": args.period})

    calc_cash, calc_pos = compute_from_trade_ledger(trades)
    stmt_cash, stmt_pos = normalize_stmt_items(stmt_items)

    cash_diff = diff_tables(calc_cash, stmt_cash, ["currency"], "cash_balance")
    pos_diff = diff_tables(calc_pos, stmt_pos, ["symbol"], "position_qty")

    tol = float(args.tolerance)

    cash_bad = cash_diff[cash_diff["diff"].abs() > tol]
    pos_bad = pos_diff[pos_diff["diff"].abs() > tol]

    os.makedirs(args.out_dir, exist_ok=True)
    cash_csv = os.path.join(args.out_dir, f"recon_cash_{args.broker}_{args.period}.csv")
    pos_csv = os.path.join(args.out_dir, f"recon_pos_{args.broker}_{args.period}.csv")

    cash_diff.to_csv(cash_csv, index=False, encoding="utf-8-sig")
    pos_diff.to_csv(pos_csv, index=False, encoding="utf-8-sig")

    print(f"[OK] Recon period={args.period} broker={args.broker} month_end<{month_end}")
    print(f"[OUT] {cash_csv}  (diff rows={len(cash_bad)})")
    print(f"[OUT] {pos_csv}   (diff rows={len(pos_bad)})")

    if len(cash_bad) or len(pos_bad):
        print("[WARN] Differences found (see CSV).")
        raise SystemExit(2)


if __name__ == "__main__":
    main()
