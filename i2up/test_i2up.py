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


if __name__ == '__main__':
    unittest.main()
