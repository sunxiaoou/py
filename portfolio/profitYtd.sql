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
dividend AS (
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
  WHERE l.biz_type_code IN ('DIVIDEND', 'DIVIDEND_ADJ', 'DIVIDEND_TAX', 'DIVIDEND_TAX_ADJ')
  GROUP BY (YEAR(l.occurred_at) * 100 + MONTH(l.occurred_at))
),
monthly_data AS (
  SELECT
    fx.period_yyyymm,
    n.cny_net AS cny_net,
    n.cny_net - LAG(n.cny_net, 1) OVER (ORDER BY fx.period_yyyymm) AS cny_net_diff,
    COALESCE(c.cny_cash, 0) AS cny_cash,
    COALESCE(d.cny_dividend, 0) AS cny_dividend
  FROM fx_rate_monthly fx
  LEFT JOIN net n ON fx.period_yyyymm = n.period_yyyymm
  LEFT JOIN cash c ON fx.period_yyyymm = c.period_yyyymm
  LEFT JOIN dividend d ON fx.period_yyyymm = d.period_yyyymm
)
SELECT
  period_yyyymm,
  cny_net,
  cny_net_diff,
  cny_cash,
  cny_dividend,
  cny_net_diff - cny_cash - cny_dividend AS cny_profit,
  CASE
  	WHEN MOD(period_yyyymm, 100) = 12 THEN
  	  SUM(cny_net_diff - cny_cash - cny_dividend) OVER (
        PARTITION BY FLOOR(period_yyyymm / 100)
        ORDER BY period_yyyymm
      )
    ELSE NULL  
  END AS cny_profit_ytd
FROM monthly_data
ORDER BY period_yyyymm;
ORDER BY fx.period_yyyymm;