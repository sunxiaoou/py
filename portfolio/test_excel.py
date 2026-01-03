import unittest

import pandas as pd
import numpy as np
import random
import string
import os

from excel_tool import df_to_sheet, duplicate_last_sheet


class ExcelTestCase(unittest.TestCase):
    @staticmethod
    def random_df(rows=4, cols=3, seed=None):
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)
        col_names = [
            ''.join(random.choices(string.ascii_uppercase, k=3))
            for _ in range(cols)
        ]
        data = np.random.randint(1, 100, size=(rows, cols))
        return pd.DataFrame(data, columns=col_names)

    @classmethod
    def setUpClass(cls):
        cls.df = ExcelTestCase.random_df()
        cls.df2 = ExcelTestCase.random_df()
        cls.xlsx = 'test_excel.xlsx'

    def test_create_excel(self):
        print("Test to create excel with a sheet")
        if os.path.exists(self.xlsx):
            os.remove(self.xlsx)
        df_to_sheet(self.df, self.xlsx, 'df', header=True)
        df_to_sheet(self.df2, self.xlsx, 'df2', header=True)

    def test_copy_last_sheet(self):
        print("Test to duplicate last sheet")
        duplicate_last_sheet(self.xlsx, 'df3', 10)

    def test_overlap_sheet(self):
        print("Test to overlap sheet")
        df_to_sheet(ExcelTestCase.random_df(), self.xlsx, 'df3', overlay=True, header=True)


if __name__ == '__main__':
    unittest.main()
