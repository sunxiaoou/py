#! /usr/bin/python3
import json

import requests


class I2UP:
    def __init__(self, ca_path: str, ip: str, port=58086):
        self.ca_path = ca_path
        self.base_url = f"https://{ip}:{port}/api"
        self.token = None

        url = f"{self.base_url}/auth/token"
        payload = json.dumps({
            "username": "admin",
            "pwd": "Info@4321"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        self.token = response.json()['data']['token']
        # print("token(%s)" % self.token)

    def get_version(self) -> str:
        url = f"{self.base_url}/version"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['version']

    def get_activated_nodes(self) -> list:
        url = f"{self.base_url}/active/node"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list']

    def get_db_nodes(self) -> list:
        url = f"{self.base_url}/active/db"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list']

    def get_node_uuid(self, name: str) -> str:
        for node in self.get_activated_nodes():
            if name == node['node_name']:
                return node['node_uuid']
        print(f'Cannot find {name}')
        return ''

    def get_db_uuid(self, name: str) -> str:
        for db in self.get_db_nodes():
            if name == db['db_name']:
                return db['db_uuid']
        print(f'Cannot find {name}')
        return ''

    def get_db_node(self, name: str) -> dict:
        url = f"{self.base_url}/active/db/{self.get_db_uuid(name)}"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['active_db']

    def get_lic_uuid(self) -> str:
        url = f"{self.base_url}/lic"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list'][0]['lic_uuid']

    @staticmethod
    def load_json_file(json_file: str) -> dict:
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        return json_data

    def create_db_node(self, file: str) -> dict:
        url = f"{self.base_url}/active/db"
        json_obj = I2UP.load_json_file(file)
        json_obj["bind_lic_list"] = [self.get_lic_uuid()]
        json_obj['node_uuid'] = self.get_node_uuid(json_obj['node_uuid'])
        payload = json.dumps(json_obj)
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def delete_db_node(self, dbname: str) -> dict:
        url = f"{self.base_url}/active/db"
        payload = json.dumps({
            "uuids": [
                self.get_db_uuid(dbname)
            ],
            "force": 0
        })
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def get_mysql_rules(self) -> list:
        url = f"{self.base_url}/stream/rule"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list']

    def get_mysql_rule_uuid(self, name: str) -> str:
        for node in self.get_mysql_rules():
            if name == node['mysql_name']:
                return node['mysql_uuid']
        print(f'Cannot find {name}')
        return ''

    def get_mysql_rule(self, name: str) -> dict:
        url = f"{self.base_url}/stream/rule/{self.get_mysql_rule_uuid(name)}"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list']

    def create_mysql_rule(self, file: str) -> dict:
        url = f"{self.base_url}/stream/rule"
        json_obj = I2UP.load_json_file(file)
        json_obj['src_db_uuid'] = self.get_db_uuid(json_obj['src_db_uuid'])
        json_obj['tgt_db_uuid'] = self.get_db_uuid(json_obj['tgt_db_uuid'])
        payload = json.dumps(json_obj)
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def delete_mysql_rule(self, name: str) -> dict:
        url = f"{self.base_url}/stream/rule"
        payload = json.dumps({
            "mysql_uuids": [
                self.get_mysql_rule_uuid(name)
            ],
            "force": False
        })
        headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json'
        }
        response = requests.request("DELETE", url, headers=headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']


def main():
    pass


if __name__ == "__main__":
    main()
