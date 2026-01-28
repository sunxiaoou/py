#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
from decimal import Decimal


def is_na(x) -> bool:
    try:
        return pd.isna(x)
    except Exception:
        return x is None


def to_int_volume(x):
    """Convert excel volume cell to int; return None if empty/invalid."""
    if is_na(x):
        return None
    # 有些Excel会把数字读成 float/Decimal/str
    if isinstance(x, (int,)):
        return x
    if isinstance(x, float):
        if x != x:  # NaN
            return None
        return int(x)
    if isinstance(x, Decimal):
        return int(x)
    s = str(x).strip()
    if not s:
        return None
    # 去掉可能的逗号千分位
    s = s.replace(",", "")
    # 防止 "4000.0"
    if "." in s:
        try:
            return int(float(s))
        except Exception:
            return None
    if s.isdigit() or (s.startswith("-") and s[1:].isdigit()):
        return int(s)
    return None


def generate_updates_from_excel(
    xlsx_path: str,
    out_sql_path: str,
    table: str = "trade_ledger",
    id_col: str = "id",
    volume_col: str = "volume",
    safe_trade_only: bool = True,
):
    xl = pd.ExcelFile(xlsx_path)
    id_to_volume = {}
    conflicts = []

    for sheet in xl.sheet_names:
        df = xl.parse(sheet_name=sheet)

        # 容错：列名可能有大小写/空格
        cols = {c.strip().lower(): c for c in df.columns if isinstance(c, str)}
        if id_col.lower() not in cols or volume_col.lower() not in cols:
            # 这个sheet不是你要的结构就跳过
            continue

        id_real = cols[id_col.lower()]
        vol_real = cols[volume_col.lower()]

        for _, row in df[[id_real, vol_real]].iterrows():
            rid = row[id_real]
            vol = row[vol_real]

            if is_na(rid):
                continue
            try:
                rid_int = to_int_volume(rid)
            except Exception:
                continue

            vol_int = to_int_volume(vol)
            if vol_int is None:
                continue

            # 去重与冲突检测
            if rid_int in id_to_volume and id_to_volume[rid_int] != vol_int:
                conflicts.append((rid_int, id_to_volume[rid_int], vol_int, sheet))
            else:
                id_to_volume[rid_int] = vol_int

    if conflicts:
        lines = ["[ERROR] Conflicting volume values found for same id:"]
        for rid, v1, v2, sheet in conflicts[:20]:
            lines.append(f"  id={rid}: {v1} vs {v2} (sheet={sheet})")
        if len(conflicts) > 20:
            lines.append(f"  ... and {len(conflicts)-20} more")
        raise SystemExit("\n".join(lines))

    # 生成 SQL
    with open(out_sql_path, "w", encoding="utf-8") as f:
        f.write("START TRANSACTION;\n\n")
        for rid in sorted(id_to_volume.keys()):
            vol = id_to_volume[rid]
            if vol <= 0:
                continue

            if safe_trade_only:
                f.write(
                    f"UPDATE {table} "
                    f"SET volume = {vol} "
                    f"WHERE id = {rid} "
                    f"AND biz_type_code IN ('TRADE_BUY','TRADE_SELL');\n"
                )
            else:
                f.write(
                    f"UPDATE {table} "
                    f"SET volume = {vol} "
                    f"WHERE id = {rid};\n"
                )

        f.write("\nCOMMIT;\n")

    print(f"Generated {len(id_to_volume)} UPDATE statements into: {out_sql_path}")


def generate_updates2(
        xlsx_path: str,
        out_sql_path: str,
        table: str = "trade_ledger",
):
    xl = pd.ExcelFile(xlsx_path)
    tuples = []
    for sheet in xl.sheet_names:
        df = xl.parse(sheet_name=sheet)
        for _, row in df[['occurred_at', 'biz_type_code', 'volume']].iterrows():
            vol = row['volume']
            vol_int = to_int_volume(vol)
            if vol_int is None:
                continue
            tuples.append((row['occurred_at'], row['biz_type_code'], vol_int))
        break

    # 生成 SQL
    with open(out_sql_path, "w", encoding="utf-8") as f:
        f.write("START TRANSACTION;\n\n")
        for occurred_at, biz_type_code, vol_int in tuples:
            f.write(
                f"UPDATE {table} "
                f"SET volume = {vol_int} "
                f"WHERE occurred_at = '{occurred_at}' AND biz_type_code = '{biz_type_code}' "
                f"AND broker_name = 'uSmart';\n"
            )
        f.write("\nCOMMIT;\n")
    print(f"Generated {len(tuples)} UPDATE statements into: {out_sql_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="tradeLedger.xlsx path")
    ap.add_argument("-o", "--out", default="update_volume.sql", help="output sql file path")
    ap.add_argument("--table", default="trade_ledger")
    ap.add_argument("--id-col", default="id")
    ap.add_argument("--volume-col", default="volume")
    ap.add_argument("--no-trade-only", action="store_true",
                    help="do not restrict updates to TRADE_BUY/TRADE_SELL")
    args = ap.parse_args()

    generate_updates2(
        xlsx_path=args.input,
        out_sql_path=args.out,
        table=args.table
        # id_col=args.id_col,
        # volume_col=args.volume_col,
        # safe_trade_only=(not args.no_trade_only),
    )


if __name__ == "__main__":
    main()
