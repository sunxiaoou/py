import unittest
from pprint import pprint

from excel_tool import Excel


class ExcelTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # excel_file = 'excel/samples.xlsx'
        excel_file = 'excel/sample2.xlsx'
        template = 'excel/template.xlsx'
        cls.excel = Excel(excel_file, template)
        cls.output = 'output'

    def test_list_nodes(self):
        print("Test to list nodes")
        nodes = self.excel.get_nodes(Excel.WORK_NODE)
        print("count(%d)" % len(nodes))
        pprint(nodes)

    def test_list_dbs(self):
        print("Test to list dbs")
        dbs = self.excel.get_dbs(Excel.MSQ_NODE)
        print("count(%d)" % len(dbs))
        pprint(dbs)

    def test_list_hbs(self):
        print("Test to list hbs")
        dbs = self.excel.get_dbs(Excel.HB_NODE)
        print("count(%d)" % len(dbs))
        pprint(dbs)

    def test_list_kfks(self):
        print("Test to list kfks")
        dbs = self.excel.get_kfks(Excel.KFK_NODE)
        print("count(%d)" % len(dbs))
        pprint(dbs)

    def test_list_msq_msq_rules(self):
        print("Test to list msq_msq rules")
        rules = self.excel.get_msq_msq_rules(Excel.MSQ_MSQ_RULE)
        print("count(%d)" % len(rules))
        pprint(rules)

    def test_list_hb_hb_rules(self):
        print("Test to list hb_hb rules")
        rules = self.excel.get_hb_hb_rules(Excel.HB_HB_RULE)
        print("count(%d)" % len(rules))
        pprint(rules)

    def test_list_msq_kfk_rules(self):
        print("Test to list msq_kfk rules")
        rules = self.excel.get_msq_kfk_rules(Excel.MSQ_KFK_RULE)
        print("count(%d)" % len(rules))
        pprint(rules)

    def test_generate_db_json(self):
        print("Test to generate msq json")
        dic = {
            'config': {
                'db_list': [
                    {
                        'ip': '192.168.55.250',
                        'port': 3306
                    }
                ],
                'role': ['source', 'target'],
                'user_management': [
                    {
                        'cred_login': 1,
                        'cred_uuid': 'manga',
                        'default_db': 'manga'
                    }
                ]
            },
            'db_name': 'msq_u_auto',
            'db_type': 'mysql',
            'node_uuid': 'centos1'
        }
        self.excel.generate_creation_json(Excel.MSQ_NODE, dic, self.output)

    def test_generate_hb_json(self):
        print("Test to generate hb json")
        dic = {
            'config': {
                'db_list': [
                    {'ip': '10.1.125.203', 'port': 8020}
                ],
                'role': ['source', 'target'],
                'user_management': [],
                'zookeeper': {
                    'set': [
                        {'ip': '10.1.125.203', 'port': 2181, 'zk_node': '/hbase'},
                        {'ip': '10.1.125.204', 'port': 2181, 'zk_node': '/hbase'},
                        {'ip': '10.1.125.205', 'port': 2181, 'zk_node': '/hbase'}
                    ]
                }
            },
            'db_name': 'hb_triple',
            'db_type': 'hbase',
            'node_uuid': 'hadoop1',
            'username': 'admin'
        }
        self.excel.generate_creation_json(Excel.HB_NODE, dic, self.output)

    def test_generate_kfk_json(self):
        print("Test to generate kfk json")
        dic = {
            'config': {
                'auth': 'kerberos',
                'db_list': [
                    {
                        'ip': '192.168.55.250',
                        'port': 9092
                    }
                ],
                'role': ['target'],
                'user_management': [
                    {
                        'default_db': 'kfk_svc',
                        'passwd': 'manga',
                        'user': 'manga'
                    }
                ]
            },
            'db_name': 'kfk_u_auto',
            'db_type': 'kafka',
            'node_uuid': 'centos1',
            'username': 'admin'
        }
        dic = {'config': {'auth': 'none',
                          'db_list': [{'ip': '192.168.55.250', 'port': 9092}],
                          'role': ['target'],
                          'user_management': []},
               'db_name': 'kfk_u_auto',
               'db_type': 'kafka',
               'node_uuid': 'centos1',
               'username': 'admin'}
        self.excel.generate_creation_json(Excel.KFK_NODE, dic, self.output)

    def test_generate_msq_msq_json(self):
        print("Test to generate msq_msq json")
        dic = {
            'config': {
                'full_sync_settings': {
                    'dump_thd': 2,
                    'existing_table': 'drop_purge',
                    'full_sync_custom_cfg': ['targetjdbc.extra.column.value=auto'],
                    'load_thd': 2}
            },
            'db_map': [],
            'dml_track': {
                'date_time_column': 'cdc_upd_tmstamp',
                'op_column': 'cdc_upd_type'},
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
                }
            ],
            'tgt_db_uuid': 'msq_c1_auto'
        }
        self.excel.generate_creation_json(Excel.MSQ_MSQ_RULE, dic, self.output)

    def test_generate_hb_hb_json(self):
        print("Test to generate hb_hb json")
        dic = {
            'config': {
                'full_sync_settings': {'existing_table': 'drop_purge'},
                'rpc_server': {
                    'peer': 'rs_h1',
                    'zookeeper': {
                        'set': [
                            {'ip': 'hadoop1', 'port': 2181.0, 'zk_node': 2181.0}
                        ]
                    }
                }
            },
            'db_map': [],
            'map_type': 'table',
            'mysql_name': 'hb_ht_h2',
            'src_db_uuid': 'hb_triple',
            'tab_map': [
                {
                    'dst_db': 'default',
                    'dst_table': 'peTable',
                    'src_db': 'default',
                    'src_table': 'peTable'
                },
                {
                    'dst_db': 'manga',
                    'dst_table': 'fruit',
                    'src_db': 'manga',
                    'src_table': 'fruit'
                }
            ],
            'tgt_db_uuid': 'hb_h2',
            'username': 'admin'
        }
        self.excel.generate_creation_json(Excel.HB_HB_RULE, dic, self.output)

    def test_generate_msq_kfk_json(self):
        print("Test to list msq_kfk json")
        dic = {
            'config': {
                'full_sync_settings': {
                    'dump_thd': 1,
                    'full_sync_custom_cfg': ['dump.no.data=true'],
                    'load_thd': 1
                }
            },
            'db_map': [],
            'full_sync': 1,
            'incre_sync': 0,
            'map_type': 'table',
            'mysql_name': 'msq_u_kfk_auto',
            'other_settings': {
                'dyn_thread': 1,
                'incre_full_sync_custom_cfg': []
            },
            'src_db_uuid': 'msq_u_auto',
            'tab_map': [
                {
                    'dst_db': 'fruit',
                    'dst_table': 'fruit',
                    'src_db': 'manga',
                    'src_table': 'fruit'
                },
                {
                    'dst_db': 'export',
                    'dst_table': 'export',
                    'src_db': 'manga',
                    'src_table': 'export'
                }
            ],
            'tgt_db_uuid': 'kfk_u_auto',
            'username': 'admin'
        }
        self.excel.generate_creation_json(Excel.MSQ_KFK_RULE, dic, self.output)


if __name__ == '__main__':
    unittest.main()
