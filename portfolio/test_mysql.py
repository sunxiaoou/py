import unittest

import pandas as pd
from sqlalchemy import create_engine, text

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
                id,
                occurred_at,
                biz_type_code,
                amount,
                symbol,
                direction
            FROM trade_ledger
            WHERE occurred_at >= :start AND occurred_at < :end
            ORDER BY occurred_at, id
        """
        year = 2022
        start = f"{year}-01-01 00:00:00"
        end = f"{year+1}-01-01 00:00:00"
        print(self.db.to_frame_with_interval(sql, start, end))


if __name__ == '__main__':
    unittest.main()
