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
        dic = {
            'config': {
                'db_list': [{
                    'ip': '192.168.55.250',
                    'port': 3306}],
                'role': ['source', 'target'],
                'user_management': [{
                    'cred_uuid': 'manga',
                    'default_db': 'manga'}]},
            'db_name': 'msq_u_auto',
            'db_type': 'mysql',
            'node_uuid': 'centos1'}
        self.excel.generate_creation_json('msq', dic)

    def test_generate_msq_rule_json(self):
        print("Test to list mysql rules")
        dic = {
            'config': {
                'full_sync_settings': {
                    'dump_thd': 2,
                    'existing_table': 'drop_purge',
                    'full_sync_custom_cfg': ['targetjdbc.extra.column.value=auto']}
            },
            'db_map': [],
            'full_sync': 1,
            'incre_sync': 1,
            'map_type': 'table',
            'mysql_name': 'msq_u_c1_auto',
            'other_settings': {
                'dyn_thread': 1,
                'incre_full_sync_custom_cfg': []},
            'src_db_uuid': 'msq_u_auto',
            'tab_map': [
                {
                    'dst_db': 'manga',
                    'dst_table': 'fruit',
                    'src_db': 'manga',
                    'src_table': 'fruit'
                },
                {
                    'dst_db': 'manga',
                    'dst_table': 'export',
                    'src_db': 'manga',
                    'src_table': 'export'
                }],
            'tgt_db_uuid': 'msq_c1_auto'}
        self.excel.generate_creation_json('msq', dic)


if __name__ == '__main__':
    unittest.main()
