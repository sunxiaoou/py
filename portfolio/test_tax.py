import os
import unittest

from mysql import MySql

class TestTax(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MySql(database='portfolio')

    @staticmethod
    def get_exchange_rate(currency: str) -> tuple:
        if currency.lower() == 'hkd':
            hkd_rate = '1'
            usd_rate = 'fx.usd_hkd_rate'
        elif currency.lower() == 'cny':
            hkd_rate = 'fx.hkd_cny_rate'
            usd_rate = 'fx.usd_cny_rate'
        else:
            raise ValueError("Unsupported currency: {}".format(currency))
        return hkd_rate, usd_rate

    def run_tax_sql(self, currency: str, broker_name: str = ''):
        hkd_rate, usd_rate = self.get_exchange_rate(currency)
        comment_out = '' if broker_name else '--'
        sql = f"""
            WITH net AS (
              -- 将月结单中的现金结余、个股市值、个基市值等按当月hkd/usd汇率统一折算为{currency}后求和,得到每月资产净值合计
              SELECT
              b.period_yyyymm,
              SUM(
                CASE
                  WHEN b.currency = 'HKD' THEN b.market_value * {hkd_rate}
                  WHEN b.currency = 'USD' THEN b.market_value * {usd_rate}
                  ELSE 0
                END
              ) AS {currency}_net
              FROM broker_statement_monthly b
              JOIN fx_rate_monthly fx ON fx.period_yyyymm = b.period_yyyymm
              {comment_out} WHERE b.broker_name = '{broker_name}'
              GROUP BY b.period_yyyymm
            ),
            cash_dividend AS (
              -- 将交易流水中的出入金和派息及派息税费记录按当月hkd/usd汇率统一折算为{currency}后求和,得到每月出入金合计 + 净派息合计
              SELECT
              (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at)) AS period_yyyymm,
              SUM(
                CASE
                  WHEN l.currency = 'HKD' THEN l.amount * {hkd_rate}
                  WHEN l.currency = 'USD' THEN l.amount * {usd_rate}
                  ELSE 0
                END
              ) AS {currency}_cash_dividend
              FROM trade_ledger l
              JOIN fx_rate_monthly fx ON fx.period_yyyymm = (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
              WHERE l.biz_type_code IN
               ('CASH_IN', 'CASH_OUT', 'DIVIDEND', 'DIVIDEND_ADJ', 'DIVIDEND_FEE', 'DIVIDEND_TAX', 'DIVIDEND_TAX_ADJ')
              {comment_out} AND l.broker_name = '{broker_name}'
              GROUP BY (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
            ),
            monthly_data AS (
              -- 将上述2个子查询的结果按月合并,得到每月资产净值、资产净值月度变化 、出入金合计 + 净派息合计
              SELECT
                fx.period_yyyymm AS period_yyyymm,
                n.{currency}_net AS {currency}_net,
                n.{currency}_net - COALESCE(LAG(n.{currency}_net, 1) OVER (ORDER BY fx.period_yyyymm), 0)
                 AS {currency}_net_diff,
                COALESCE(cd.{currency}_cash_dividend, 0) AS {currency}_cash_dividend
              FROM fx_rate_monthly fx
              LEFT JOIN net n ON fx.period_yyyymm = n.period_yyyymm
              LEFT JOIN cash_dividend cd ON fx.period_yyyymm = cd.period_yyyymm
            )
            -- 最后计算每月盈亏(资产净值月度变化 - (出入金 + 净派息)), 以及每年盈亏累计, 每年盈亏累计只在12月显示,其他月份显示NULL
            SELECT
              period_yyyymm,
              {currency}_net,
              {currency}_net_diff,
              {currency}_cash_dividend,
              {currency}_net_diff - {currency}_cash_dividend AS {currency}_profit,
              CASE
                WHEN MOD(period_yyyymm, 100) = 12 THEN
                  SUM({currency}_net_diff - {currency}_cash_dividend) OVER (
                    PARTITION BY FLOOR(period_yyyymm / 100)
                    ORDER BY period_yyyymm
                  )
                ELSE NULL
              END AS {currency}_profit_ytd
            FROM monthly_data
            ORDER BY period_yyyymm;
        """
        df = self.db.to_frame_with_params(sql, {})
        print(df)
        csv = os.path.join('tmp/test', f"tax_{currency}_{broker_name}.csv")
        df.to_csv(csv, index=False, encoding="utf-8-sig")
        print(f"Saved tax data to: {csv}")

    def test_tax_sql(self):
        # self.run_tax_sql('hkd', 'ValuableCapital')
        self.run_tax_sql('cny', 'ValuableCapital')
        self.run_tax_sql('cny', 'uSmart')
        self.run_tax_sql('cny', 'Futu')
        self.run_tax_sql('cny')

    def run_dividend_sql(self, currency: str, broker_name: str = ''):
        hkd_rate, usd_rate = self.get_exchange_rate(currency)
        comment_out = '' if broker_name else '--'
        sql = f"""
            WITH dividend AS (
              -- 将交易流水中的派息记录按当月hkd/usd汇率统一折算为cny后求和,得到每月的cny派息合计
              SELECT
              (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at)) AS period_yyyymm,
              SUM(
                CASE
                  WHEN l.currency = 'HKD' THEN l.amount * {hkd_rate}
                  WHEN l.currency = 'USD' THEN l.amount * {usd_rate}
                  ELSE 0
                END
              ) AS cny_dividend
              FROM trade_ledger l
              JOIN fx_rate_monthly fx ON fx.period_yyyymm = (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
              WHERE l.biz_type_code IN ('DIVIDEND', 'DIVIDEND_ADJ')
              {comment_out} AND l.broker_name = '{broker_name}'
              GROUP BY (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
            ),
            deduction AS (
              -- 将交易流水中的税扣除记录按当月hkd/usd汇率统一折算为cny后求和,得到每月的cny税扣除合计
              -- 不包括DIVIDEND_FEE, 因为它是手续费, 不属于税扣除
              SELECT
              (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at)) AS period_yyyymm,
              SUM(
                CASE
                  WHEN l.currency = 'HKD' THEN -l.amount * {hkd_rate}
                  WHEN l.currency = 'USD' THEN -l.amount * {usd_rate}
                  ELSE 0
                END
              ) AS cny_deduction
              FROM trade_ledger l
              JOIN fx_rate_monthly fx ON fx.period_yyyymm = (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
              WHERE l.biz_type_code IN ('DIVIDEND_TAX', 'DIVIDEND_TAX_ADJ')
              {comment_out} AND l.broker_name = '{broker_name}'
              GROUP BY (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
            ),
            dividend_monthly AS (
              -- 将上述两个子查询的结果按月合并,得到每月的cny派息合计和cny税扣除合计
              SELECT
                fx.period_yyyymm AS period_yyyymm,
                COALESCE(td.cny_dividend, 0) AS cny_dividend,
                COALESCE(de.cny_deduction, 0) AS cny_deduction
              FROM fx_rate_monthly fx
              LEFT JOIN dividend td ON fx.period_yyyymm = td.period_yyyymm
              LEFT JOIN deduction de ON fx.period_yyyymm = de.period_yyyymm
            )
            -- 最后计算每月的cny派息合计、cny税扣除合计,以及每年派息累计和每年税扣除累计, 每年累计只在12月显示,其他月份显示NULL
            SELECT
              period_yyyymm,
              cny_dividend,
              CASE
                WHEN MOD(period_yyyymm, 100) = 12 THEN
                  SUM(cny_dividend) OVER (
                    PARTITION BY FLOOR(period_yyyymm / 100)
                    ORDER BY period_yyyymm
                  )
                ELSE NULL
              END AS cny_dividend_ytd,
              cny_deduction,
              CASE
                WHEN MOD(period_yyyymm, 100) = 12 THEN
                  SUM(cny_deduction) OVER (
                    PARTITION BY FLOOR(period_yyyymm / 100)
                    ORDER BY period_yyyymm
                  )
                ELSE NULL
              END AS cny_deduction_ytd
            FROM dividend_monthly
            ORDER BY period_yyyymm;
        """
        df = self.db.to_frame_with_params(sql, {})
        print(df)
        csv = os.path.join('tmp/test', f"dividend_{currency}_{broker_name}.csv")
        df.to_csv(csv, index=False, encoding="utf-8-sig")
        print(f"Saved dividend data to: {csv}")

    def test_dividend_sql(self):
        self.run_dividend_sql('cny', 'ValuableCapital')
        self.run_dividend_sql('cny', 'uSmart')
        self.run_dividend_sql('cny')


if __name__ == '__main__':
    unittest.main()
