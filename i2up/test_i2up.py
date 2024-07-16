import unittest
from pprint import pprint

from i2up import I2UP


class I2UPTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ca_path = "ca.crt"
        ip = 'centos1'
        port = 58086
        user = 'admin'
        pwd = 'Info@1234'
        cls.i2up = I2UP(ip, port, user, pwd, ca_path)

    def test_get_version(self):
        print("Test to get version")
        print("version(%s)" % self.i2up.get_version())

    def test_list_inactivated_nodes(self):
        print("Test to list inactivated nodes")
        info_list = self.i2up.get_inactivated_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_inactivated_node(self):
        print("Test to show inactivated node")
        pprint(self.i2up.get_inactivated_node('hadoop3'))

    def test_activate_node(self):
        print("Test to activate node")
        pprint(self.i2up.activate_node('hadoop3', 'Info@1234', True, False))

    def test_list_activated_nodes(self):
        print("Test to list activated nodes")
        info_list = self.i2up.get_activated_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_activated_node(self):
        print("Test to show activated node")
        pprint(self.i2up.get_activated_node('hadoop3'))

    def test_delete_activated_node(self):
        print("Test to delete activated node")
        pprint(self.i2up.delete_activated_node('hadoop3', True))

    def test_list_db_nodes(self):
        print("Test to list db nodes")
        info_list = self.i2up.get_db_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_db_node(self):
        print("Test to show db node")
        pprint(self.i2up.get_db_node('kfk_u'))

    def test_create_db_node(self):
        print("Test to create db node")
        pprint(self.i2up.create_db_node('json/kfk_u_auto.json'))

    def test_delete_db_node(self):
        print("Test to delete db node")
        pprint(self.i2up.delete_db_node('kfk_u_auto'))

    def test_list_mysql_rules(self):
        print("Test to list mysql rules")
        info_list = self.i2up.get_mysql_rules()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_mysql_rule(self):
        print("Test to show mysql rule")
        pprint(self.i2up.get_mysql_rule('msq_h1_h2'))

    def test_create_mysql_rule(self):
        print("Test to create mysql rule")
        # pprint(self.i2up.create_mysql_rule('json/msq_u_c1_auto.json'))
        pprint(self.i2up.create_mysql_rule('json/msq_u_kfk_auto.json'))

    def test_delete_mysql_rule(self):
        print("Test to delete mysql rule")
        # pprint(self.i2up.delete_mysql_rule('msq_test'))
        pprint(self.i2up.delete_mysql_rule('msq_u_kfk_auto'))


if __name__ == '__main__':
    unittest.main()
