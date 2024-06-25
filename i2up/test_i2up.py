import json
import unittest
from pprint import pprint

import requests


class I2UPTestCase(unittest.TestCase):
    base_url = "https://centos1:58086/api"
    ca_path = "ca.crt"
    token = None

    @classmethod
    def setUpClass(cls):
        url = f"{cls.base_url}/auth/token"
        payload = json.dumps({
            "username": "admin",
            "pwd": "Info@4321"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=cls.ca_path)
        response.raise_for_status()
        cls.token = response.json()['data']['token']
        print("token(%s)" % cls.token)

    def test_get_version(self):
        print("Test get version")
        url = f"{self.base_url}/version"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        print("version(%s)" % response.json()['data']['version'])

    def test_list_activated_nodes(self):
        print("Test list activated nodes")
        url = f"{self.base_url}/active/node"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        data = response.json()['data']
        print("count(%d)" % data['total'])
        pprint(data['info_list'])

    def test_list_db_nodes(self):
        print("Test list db nodes")
        url = f"{self.base_url}/active/db"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        info_list = response.json()['data']['info_list']
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def test_show_db_node(self):
        print("Test show db node")
        uuid = 'C96EDD72-A2D2-4C83-B2A0-91A4D84B13C5'
        url = f"{self.base_url}/active/db/{uuid}"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        info_list = response.json()['data']['active_db']
        pprint(info_list)

    def test_create_db_node(self):
        print("Test create db node")
        url = f"{self.base_url}/lic"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        lic = response.json()['data']['info_list'][0]['lic_uuid']
        print("lic(%s)" % lic)

        url = f"{self.base_url}/active/db"
        payload = json.dumps({
            "db_type": "mysql",
            "db_name": "msq_c2",
            "node_uuid": "A230C1E6-C68E-4F4E-A2AB-8E81C3D3288D",
            "file_open_type": "DIRECT",
            "deploy_mode": "single",
            "log_read_type": "file",
            "config": {
                "transport": {
                    "sslmode": "disabled",
                    "auth": "gmssl",
                    "ssl_mode": "",
                    "certificate": ""
                },
                "auth": "pass",
                "db_list": [
                    {
                        "ip": "192.168.55.12",
                        "port": 3306
                    }
                ],
                "user_management": [
                    {
                        "user": "manga",
                        "passwd": "manga",
                        "default_db": "manga",
                        "url": "",
                        "cred_login": 0,
                        "cred_uuid": "",
                        "auth_uuid": "",
                        "enable": True
                    }
                ],
                "role": [
                    "source",
                    "target"
                ]
            },
            "db_encryed": 2,
            "db_mode": "normal",
            "cdb": "",
            "maintenance": 0,
            "comment": "",
            "bind_lic_list": [
                f"{lic}"
            ]
        })
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        pprint(response.json()['data'])

    def test_delete_db_node(self):
        print("Test create db node")
        url = f"{self.base_url}/active/db"
        uuid = "C766462E-1DC5-4A06-B325-35951A8738EF"
        payload = json.dumps({
            "uuids": [
                uuid
            ],
            "force": 0
        })
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        pprint(response.json()['data'])

    def test_list_mysql_rules(self):
        print("Test list mysql rules")
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
        print("Test show mysql rule")
        uuid = '6980B753-B134-4D17-A634-FD748F7E9AA6'
        url = f"{self.base_url}/stream/rule/{uuid}"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        info_list = response.json()['data']['info_list']
        pprint(info_list)

    def test_delete_mysql_rule(self):
        print("Test delete mysql rule")
        url = f"{self.base_url}/stream/rule"
        uuid = 'C1598D48-622D-4BC6-A845-E224DE66AB83'
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
