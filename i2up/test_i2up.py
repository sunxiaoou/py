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

    def test_list_credentials(self):
        print("Test to list credentials")
        info_list = self.i2up.get_credentials()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_credential(self):
        print("Test to show credential")
        pprint(self.i2up.get_credential('guest_cred'))

    def test_list_inactive_nodes(self):
        print("Test to list inactive nodes")
        info_list = self.i2up.get_inactive_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_inactive_node(self):
        print("Test to show inactive node")
        pprint(self.i2up.get_inactive_node('hadoop3'))

    def test_list_active_nodes(self):
        print("Test to list active nodes")
        info_list = self.i2up.get_active_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_active_node(self):
        print("Test to show active node")
        pprint(self.i2up.get_active_node('hadoop3'))

    def test_activate_node(self):
        print("Test to activate node")
        pprint(self.i2up.activate_node('hadoop3', None, 'Info@1234', True, False))

    def test_delete_active_node(self):
        print("Test to delete active node")
        pprint(self.i2up.delete_active_node('hadoop3', True))

    def test_list_db_nodes(self):
        print("Test to list db nodes")
        info_list = self.i2up.get_db_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_db_node(self):
        print("Test to show db node")
        pprint(self.i2up.get_db_node('msq_u_auto'))

    def test_create_db_node(self):
        print("Test to create db node")
        pprint(self.i2up.create_db_node(I2UP.load_json_file('json/kfk_u_auto.json')))

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
        # pprint(self.i2up.get_mysql_rule('msq_u_c1_auto'))
        pprint(self.i2up.get_mysql_rule('msq_u_kfk_auto'))

    def test_create_mysql_rule(self):
        print("Test to create mysql rule")
        # pprint(self.i2up.create_mysql_rule('json/msq_u_c1_auto.json'))
        pprint(self.i2up.create_mysql_rule(I2UP.load_json_file('json/msq_u_kfk_auto.json')))

    def test_delete_mysql_rule(self):
        print("Test to delete mysql rule")
        # pprint(self.i2up.delete_mysql_rule('msq_test'))
        pprint(self.i2up.delete_mysql_rule('msq_u_kfk_auto'))


if __name__ == '__main__':
    unittest.main()
