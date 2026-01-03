import unittest

from mysql import MySql

class MySqlTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MySql(database='portfolio')

    def test_last_row(self):
        print(self.db.last_row('cvtbond_daily', 'date', 'code = "%s"' % 'SZ127007'))

    def test_to_frame(self):
        print(self.db.to_frame('cvtb_rank_daily', None,
                               'date = (select max(`date`) from cvtb_rank_daily)'))

    def test_sql(self):
        sql = """
            SELECT
                l.id,
                l.occurred_at,
                l.biz_type_code,
                l.amount,
                l.symbol,
                l.direction,
                s.security_name,
                b.affect_position,
                b.taxable_flag
            FROM trade_ledger l
            JOIN security_master s ON l.symbol = s.symbol
            JOIN biz_type_dict b ON l.biz_type_code = b.biz_type_code
            WHERE
                l.occurred_at >= :start AND l.occurred_at < :end AND s.currency = :currency
            ORDER BY
                l.occurred_at, l.id;
        """
        year = 2022
        start = f"{year}-01-01 00:00:00"
        end = f"{year+1}-01-01 00:00:00"
        print(self.db.to_frame_with_interval(sql, start, end, 'USD'))


if __name__ == '__main__':
    unittest.main()
