#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP


def is_na(x) -> bool:
    try:
        return pd.isna(x)
    except Exception:
        return x is None


def to_decimal_fee(x):
    """
    Convert excel fee cell to Decimal with 2 decimals.
    Return None if empty/invalid.
    Accepts: 24.23, "24.23", "24.23 ", "1,234.56", "-24.23" (we'll abs later)
    """
    if is_na(x):
        return None

    if isinstance(x, Decimal):
        d = x
    elif isinstance(x, (int, float)):
        # pandas may give float; keep as string to avoid binary float issues
        d = Decimal(str(x))
    else:
        s = str(x).strip()
        if not s:
            return None
        s = s.replace(",", "")
        # tolerate currency symbols or stray chars if any (basic)
        s = s.replace("HKD", "").replace("USD", "").strip()
        try:
            d = Decimal(s)
        except Exception:
            return None

    # fee should be stored as positive number per your rule (>0),
    # if excel has negative fee, normalize to positive.
    d = abs(d)

    # 2 decimals
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def generate_updates_from_excel(
        xlsx_path: str,
        out_sql_path: str,
        table: str = "trade_ledger",
        id_col: str = "id",
        fee_col: str = "fee",
):
    xl = pd.ExcelFile(xlsx_path)
    id_to_fee = {}
    conflicts = []

    for sheet in xl.sheet_names:
        df = xl.parse(sheet_name=sheet)

        # 容错：列名大小写/空格
        cols = {str(c).strip().lower(): c for c in df.columns}
        if id_col.lower() not in cols or fee_col.lower() not in cols:
            continue

        id_real = cols[id_col.lower()]
        fee_real = cols[fee_col.lower()]

        for _, row in df[[id_real, fee_real]].iterrows():
            rid = row[id_real]
            fee = row[fee_real]

            if is_na(rid):
                continue
            # try:
            #     rid_int = int(str(rid).strip())
            # except Exception:
            #     continue

            rid = row[id_real]
            # ---- 安全解析 Excel 里的 id（可能是 int / float / str）----
            if is_na(rid):
                continue

            # 1) 数值型（Excel 最常见：212.0）
            if isinstance(rid, (int,)):
                rid_int = rid
            elif isinstance(rid, float):
                if rid.is_integer():
                    rid_int = int(rid)
                else:
                    # 像 212.5 这种，直接视为脏数据
                    continue
            # 2) 字符串兜底
            else:
                s = str(rid).strip()
                if not s:
                    continue
                # 允许 "212" / "212.0"
                if s.isdigit():
                    rid_int = int(s)
                else:
                    try:
                        f = float(s)
                        if f.is_integer():
                            rid_int = int(f)
                        else:
                            continue
                    except Exception:
                        continue
            if rid_int is None:
                continue

            fee_dec = to_decimal_fee(fee)
            if fee_dec is None:
                continue

            # 只输出 fee > 0
            if fee_dec <= 0:
                continue

            # 去重冲突检测
            if rid_int in id_to_fee and id_to_fee[rid_int] != fee_dec:
                conflicts.append((rid_int, id_to_fee[rid_int], fee_dec, sheet))
            else:
                id_to_fee[rid_int] = fee_dec

    if conflicts:
        lines = ["[ERROR] Conflicting tax_and_fee values found for same id:"]
        for rid, f1, f2, sheet in conflicts[:20]:
            lines.append(f"  id={rid}: {f1} vs {f2} (sheet={sheet})")
        if len(conflicts) > 20:
            lines.append(f"  ... and {len(conflicts)-20} more")
        raise SystemExit("\n".join(lines))

    # 生成 SQL
    with open(out_sql_path, "w", encoding="utf-8") as f:
        f.write("START TRANSACTION;\n\n")
        for rid in sorted(id_to_fee.keys()):
            fee_dec = id_to_fee[rid]
            # 只更新 TRADE_BUY / TRADE_SELL
            f.write(
                f"UPDATE {table} "
                f"SET tax_and_fee = {fee_dec} "
                f"WHERE id = {rid} "
                f"AND biz_type_code IN ('TRADE_BUY','TRADE_SELL');\n"
            )
        f.write("\nCOMMIT;\n")

    print(f"Generated {len(id_to_fee)} UPDATE statements into: {out_sql_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="tradeLedger.xlsx path")
    ap.add_argument("-o", "--out", default="update_fee.sql", help="output sql file path")
    ap.add_argument("--table", default="trade_ledger")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--fee-col", default="tax_and_fee")
    args = ap.parse_args()

    generate_updates_from_excel(
        xlsx_path=args.input,
        out_sql_path=args.out,
        table=args.table,
        id_col=args.id_col,
        fee_col=args.fee_col,
    )


if __name__ == "__main__":
    main()
