CREATE TABLE biz_type_dict (
  biz_type_code   VARCHAR(32) NOT NULL COMMENT '业务类型代码（机器用）',
  biz_type_name   VARCHAR(50) NOT NULL COMMENT '业务类型名称（展示用）',
  category ENUM(
              'ADR_FEE',                    -- ADR保管费
              'BONUS_SHARE_FEE',            -- 红股手续费
              'BONUS_SHARE_TRANSFER_FEE',   -- 红股过户费
              'CASH_IN',                    -- 资金转入/存入资金
              'CASH_OUT',                   -- 资金转出/取出资金
              'CURRENCY_EXCHANGE',          -- 换汇
              'DIVIDEND',                   -- 股息
              'DIVIDEND_ADJ',               -- 股息修正
              'DIVIDEND_FEE',               -- 股息手续费
              'DIVIDEND_TAX',               -- 股息税
              'DIVIDEND_TAX_ADJ',           -- 股息税修正
              'FUND_REDEMPTION',            -- 基金赎回
              'FUND_SUBSCRIPTION',          -- 基金申购
              'IPO_FEE',                    -- IPO手续费
              'IPO_REFUND',                 -- IPO退款
              'IPO_SUBSCRIPTION',           -- IPO认购
              'MARGIN_INTEREST_PRINCIPAL',  -- 融资利息归本
              'REBATE',                     -- 返佣
              'TRADE_BUY',                  -- 买入证券
              'TRADE_SELL',                 -- 卖出证券
              'TRADE_FEE',                  -- 证券交易费用
              'OTHER'
              ) NOT NULL COMMENT '业务类别',
  default_direction ENUM('IN','OUT') NOT NULL COMMENT '默认资金方向',
  affect_position  TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否影响持仓数量',
  taxable_flag     TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否计入应税项目',
  description      VARCHAR(255) NULL COMMENT '说明',
  is_active        TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否有效',
  PRIMARY KEY (biz_type_code),
  UNIQUE KEY uk_biz_type_name (biz_type_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易业务类型字典表';

CREATE TABLE security_master (
  symbol          VARCHAR(32) NOT NULL COMMENT '证券代码，如 GS / MSFT / TLT / CASH_USD',
  security_name   VARCHAR(200) NOT NULL COMMENT '证券或资金名称',
  currency        CHAR(3) NOT NULL COMMENT '币种：USD/CNY/HKD 等',
  security_type   ENUM(
                    'CASH',                 -- 现金
                    'COMMODITY',            -- 大宗商品
                    'US_TREASURY_BOND',     -- 美债
                    'US_EQ_INDEX',          -- 美股宽基
                    'US_EQ_VALUE',          -- 美股价值
                    'US_EQ_TECH',           -- 美股科技
                    'OTHER_EQ',             -- 其它市场股票
                    'CRYPTOCURRENCY',       -- 加密货币
                    'OTHER'
                  ) NOT NULL COMMENT '证券类型',
  risk_level      TINYINT NOT NULL DEFAULT 3 COMMENT '风险等级，0-4 级',
  -- exchange        VARCHAR(50) NULL COMMENT '交易所，如 NYSE/NASDAQ',
  -- issuer          VARCHAR(100) NULL COMMENT '发行方，如 iShares',
  is_active       TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否有效',
  PRIMARY KEY (symbol),
  INDEX idx_currency (currency),
  INDEX idx_type (security_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='证券/资金主数据表';

CREATE TABLE trade_ledger (
  id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '流水主键',
  -- 时间
  occurred_at     DATETIME(0) NOT NULL COMMENT '发生时间（券商时间，精确到秒）',
  -- 业务类型（字典表）
  biz_type_code   VARCHAR(32) NOT NULL COMMENT '业务类型代码，对应 biz_type_dict.biz_type_code',
  -- 金额（正入负出）
  amount          DECIMAL(18,2) NOT NULL COMMENT '金额（正为流入，负为流出）',
  -- 证券 / 资金标识
  symbol          VARCHAR(32) NOT NULL COMMENT '证券或资金代码，如 AAPL / TLT / CASH_USD',
  -- 冗余字段：方向（由 amount 推导，便于查询）
  direction       ENUM('IN','OUT')
                  GENERATED ALWAYS AS (
                    CASE WHEN amount >= 0 THEN 'IN' ELSE 'OUT' END
                  ) STORED COMMENT '资金方向（由 amount 自动生成）',
  -- 账户 / 券商信息（可选）
  account_id      VARCHAR(64) NULL COMMENT '账户标识（多账户场景）',
  broker_txn_id   VARCHAR(64) NULL COMMENT '券商流水号 / 订单号',
  -- OCR / 原始追溯
  raw_text        TEXT NULL COMMENT '原始文本（OCR 行，用于审计/人工校验）',
  note            VARCHAR(255) NULL COMMENT '备注',
  -- 主键
  PRIMARY KEY (id),
  -- 常用索引
  INDEX idx_occurred_at (occurred_at),
  INDEX idx_symbol_time (symbol, occurred_at),
  INDEX idx_biz_time (biz_type_code, occurred_at),
  -- 防重复（若券商流水号可用）
  UNIQUE KEY uk_broker_txn (account_id, broker_txn_id),
  -- 业务类型外键
  CONSTRAINT fk_trade_biz_type
    FOREIGN KEY (biz_type_code)
    REFERENCES biz_type_dict(biz_type_code)
  -- 如你希望强约束 symbol，可启用下面这条（前提是 security_master 已存在）
  -- ,CONSTRAINT fk_trade_symbol
  --   FOREIGN KEY (symbol)
  --   REFERENCES security_master(symbol)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COMMENT='交易流水事实表（证券/资金/税费等）';
