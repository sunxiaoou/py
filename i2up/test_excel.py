import json
import os
import unittest

from excel_tool import df_to_sheet, duplicate_last_sheet
from json_tool import json_to_df


class ExcelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('tmp/msq_u_auto.json', 'r') as f:
            cls.msq_u = json.load(f)
        with open('tmp/msq_c1_auto.json', 'r') as f:
            cls.msq_c1 = json.load(f)
        cls.xlsx = 'test_excel.xlsx'

    def test_create_excel(self):
        print("Test to create excel with a sheet")
        if os.path.exists(self.xlsx):
            os.remove(self.xlsx)
        df_to_sheet(json_to_df(self.msq_u), self.xlsx, 'msq_u', header=False)

    def test_copy_last_sheet(self):
        print("Test to duplicate last sheet")
        duplicate_last_sheet(self.xlsx, 'msq_c1')

    def test_overlap_sheet(self):
        print("Test to overlap sheet")
        df_to_sheet(json_to_df(self.msq_c1), self.xlsx, 'msq_c1', overlay=True, header=False)


if __name__ == '__main__':
    unittest.main()
