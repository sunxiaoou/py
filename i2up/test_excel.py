import unittest
from pprint import pprint

from excel_tool import Excel


class ExcelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        excel_file = 'excel/rule_auto.xlsx'
        template = 'excel/template.xlsx'
        output_dir = 'output'
        cls.excel = Excel(excel_file, template, output_dir)

    def test_list_nodes(self):
        print("Test to list nodes")
        nodes = self.excel.get_nodes('work_node')
        print("count(%d)" % len(nodes))
        pprint(nodes)

    def test_list_dbs(self):
        print("Test to list dbs")
        dbs = self.excel.get_dbs('db_node')
        print("count(%d)" % len(dbs))
        pprint(dbs)

    def test_list_mysql_rules(self):
        print("Test to list mysql rules")
        rules = self.excel.get_mysql_rules('msq_rule')
        print("count(%d)" % len(rules))
        pprint(rules)

    def test_generate_db_json(self):
        print("Test to list mysql rules")
        dic = {'config': {'db_list': [{'ip': '192.168.55.250', 'port': 3306}],
                          'role': ['source', 'target'],
                          'user_management': [{'cred_uuid': 'manga',
                                               'default_db': 'manga'}]},
               'db_name': 'msq_u_auto',
               'db_type': 'mysql',
               'node_uuid': 'centos1'}
        self.excel.generate_db_json('msq', dic)


if __name__ == '__main__':
    unittest.main()
