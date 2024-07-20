import unittest
from pprint import pprint

from excel_tool import Excel


class ExcelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        excel_file = 'excel/rule_auto.xlsx'
        cls.excel = Excel(excel_file)

    def test_list_nodes(self):
        print("Test to list nodes")
        nodes = self.excel.get_nodes('work_node')
        print("count(%d)" % len(nodes))
        pprint(nodes)

    def test_list_dbs(self):
        print("Test to list dbs")
        dbs = self.excel.get_dbs('db_node2')
        print("count(%d)" % len(dbs))
        pprint(dbs)


if __name__ == '__main__':
    unittest.main()
