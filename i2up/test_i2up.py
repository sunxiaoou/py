import json
import unittest
from pprint import pprint

import requests

from i2up import I2UP


class I2UPTestCase(unittest.TestCase):
    base_url = "https://centos1:58086/api"
    ca_path = "ca.crt"
    token = None
    rule_name = "msq_test"

    @classmethod
    def setUpClass(cls):
        cls.i2up = I2UP()

    def test_get_version(self):
        print("Test to get version")
        print("version(%s)" % self.i2up.get_version())

    def test_list_activated_nodes(self):
        print("Test to list activated nodes")
        info_list = self.i2up.get_activated_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_list_db_nodes(self):
        print("Test to list db nodes")
        info_list = self.i2up.get_db_nodes()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_db_node(self):
        print("Test to show db node")
        db_node = self.i2up.get_db_node('msq_u')
        pprint(db_node)

    def test_create_db_node(self):
        print("Test to create db node")
        pprint(self.i2up.create_db_node('centos1', 'msq_c2.json'))

    def test_delete_db_node(self):
        print("Test to create db node")
        pprint(self.i2up.delete_db_node('msq_c2'))

    def test_list_mysql_rules(self):
        print("Test to list mysql rules")
        url = f"{self.base_url}/stream/rule"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        info_list = response.json()['data']['info_list']
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_mysql_rule(self):
        print("Test to show mysql rule")
        uuid = '6980B753-B134-4D17-A634-FD748F7E9AA6'
        url = f"{self.base_url}/stream/rule/{uuid}"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        info_list = response.json()['data']['info_list']
        pprint(info_list)

    @staticmethod
    def load_json_file(json_file: str) -> str:
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        return json.dumps(json_data)

    def test_create_mysql_rule(self):
        print("Test to create mysql rule")
        url = f"{self.base_url}/stream/rule"
        payload = I2UPTestCase.load_json_file(f"{self.rule_name}.json")
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        pprint(response.json()['data'])

    def test_delete_mysql_rule(self):
        print("Test to delete mysql rule")
        url = f"{self.base_url}/stream/rule"
        uuid = 'A310E048-E7A0-4F5E-9FD1-864E73E59539'
        payload = json.dumps({
            "mysql_uuids": [
                uuid
            ],
            "force": False
        })
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        pprint(response.json()['data'])


if __name__ == '__main__':
    unittest.main()
