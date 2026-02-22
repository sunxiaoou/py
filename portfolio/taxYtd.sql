DROP VIEW fx_rate_monthly;
CREATE VIEW fx_rate_monthly AS SELECT
    period_yyyymm,
    MAX(CASE WHEN currency = 'HKD' THEN cny_rate END)        AS hkd_cny_rate,
    MAX(CASE WHEN currency = 'USD' THEN usd_hkd_rate END)    AS usd_hkd_rate,
    MAX(CASE WHEN currency = 'USD' THEN cny_rate END)        AS usd_cny_rate
  FROM broker_statement_monthly
  GROUP BY period_yyyymm
  HAVING hkd_cny_rate IS NOT NULL
     AND usd_hkd_rate IS NOT NULL
     AND usd_cny_rate IS NOT NULL;

WITH net AS (
  -- 将月结单中的现金结余、个股市值、个基市值等按当月hkd/usd汇率统一折算为cny后求和,得到每月的cny资产净值
  SELECT
  b.period_yyyymm,
  SUM(
    CASE
      WHEN b.currency = 'HKD' THEN b.market_value * fx.hkd_cny_rate
      WHEN b.currency = 'USD' THEN b.market_value * fx.usd_cny_rate
      ELSE 0
    END
  ) AS cny_net
  FROM broker_statement_monthly b
  JOIN fx_rate_monthly fx ON fx.period_yyyymm = b.period_yyyymm
  GROUP BY b.period_yyyymm
),
cash AS (
  -- 将交易流水中的出入金记录按当月hkd/usd汇率统一折算为cny后求和,得到每月的cny出入金合计
  SELECT
  (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at)) AS period_yyyymm,
  SUM(
    CASE
      WHEN l.currency = 'HKD' THEN l.amount * fx.hkd_cny_rate
      WHEN l.currency = 'USD' THEN l.amount * fx.usd_cny_rate
      ELSE 0
    END
  ) AS cny_cash
  FROM trade_ledger l
  JOIN fx_rate_monthly fx ON fx.period_yyyymm = (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
  WHERE l.biz_type_code IN ('CASH_IN', 'CASH_OUT')
  GROUP BY (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
),
nd AS (
  -- 将交易流水中的派息及税费扣除记录按当月hkd/usd汇率统一折算为cny后求和,得到每月的cny净派息合计
  SELECT
  (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at)) AS period_yyyymm,
  SUM(
    CASE
      WHEN l.currency = 'HKD' THEN l.amount * fx.hkd_cny_rate
      WHEN l.currency = 'USD' THEN l.amount * fx.usd_cny_rate
      ELSE 0
    END
  ) AS cny_net_dividend
  FROM trade_ledger l
  JOIN fx_rate_monthly fx ON fx.period_yyyymm = (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
  WHERE l.biz_type_code IN ('DIVIDEND', 'DIVIDEND_ADJ', 'DIVIDEND_FEE', 'DIVIDEND_TAX', 'DIVIDEND_TAX_ADJ')
  GROUP BY (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
),
monthly_data AS (
  -- 将上述三个子查询的结果按月合并,得到每月的cny资产净值、cny资产净值月度变化 、cny出入金合计、cny净派息合计
  SELECT
    fx.period_yyyymm AS period_yyyymm,
    n.cny_net AS cny_net,
    n.cny_net - LAG(n.cny_net, 1) OVER (ORDER BY fx.period_yyyymm) AS cny_net_diff,
    COALESCE(c.cny_cash, 0) AS cny_cash,
    COALESCE(d.cny_net_dividend, 0) AS cny_net_dividend
  FROM fx_rate_monthly fx
  LEFT JOIN net n ON fx.period_yyyymm = n.period_yyyymm
  LEFT JOIN cash c ON fx.period_yyyymm = c.period_yyyymm
  LEFT JOIN nd d ON fx.period_yyyymm = d.period_yyyymm
)
-- 最后计算每月的cny盈亏(资产净值月度变化 - 出入金 - 净派息),以及每年盈亏累计, 每年盈亏累计只在12月显示,其他月份显示NULL
SELECT
  period_yyyymm,
  cny_net,
  cny_net_diff,
  cny_cash,
  cny_net_dividend,
  cny_net_diff - cny_cash - cny_net_dividend AS cny_profit,
  CASE
  	WHEN MOD(period_yyyymm, 100) = 12 THEN
  	  SUM(cny_net_diff - cny_cash - cny_net_dividend) OVER (
        PARTITION BY FLOOR(period_yyyymm / 100)
        ORDER BY period_yyyymm
      )
    ELSE NULL  
  END AS cny_profit_ytd
FROM monthly_data
ORDER BY period_yyyymm;

WITH dividend AS (
  -- 将交易流水中的派息记录按当月hkd/usd汇率统一折算为cny后求和,得到每月的cny派息合计
  SELECT
  (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at)) AS period_yyyymm,
  SUM(
    CASE
      WHEN l.currency = 'HKD' THEN l.amount * fx.hkd_cny_rate
      WHEN l.currency = 'USD' THEN l.amount * fx.usd_cny_rate
      ELSE 0
    END
  ) AS cny_dividend
  FROM trade_ledger l
  JOIN fx_rate_monthly fx ON fx.period_yyyymm = (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
  WHERE l.biz_type_code IN ('DIVIDEND', 'DIVIDEND_ADJ')
  GROUP BY (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
),
deduction AS (
  -- 将交易流水中的税扣除记录按当月hkd/usd汇率统一折算为cny后求和,得到每月的cny税扣除合计
  -- 不包括DIVIDEND_FEE, 因为它是手续费, 不属于税扣除
  SELECT
  (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at)) AS period_yyyymm,
  SUM(
    CASE
      WHEN l.currency = 'HKD' THEN -l.amount * fx.hkd_cny_rate
      WHEN l.currency = 'USD' THEN -l.amount * fx.usd_cny_rate
      ELSE 0
    END
  ) AS cny_deduction
  FROM trade_ledger l
  JOIN fx_rate_monthly fx ON fx.period_yyyymm = (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
  WHERE l.biz_type_code IN ('DIVIDEND_TAX', 'DIVIDEND_TAX_ADJ')
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