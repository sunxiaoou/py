#! /usr/bin/python3
import argparse
import json
from pprint import pprint

import requests


class I2UP:
    def __init__(self, ip: str, port: int, user: str, pwd: str, ca_path: str):
        self.ca_path = ca_path
        self.base_url = f"https://{ip}:{port}/api"
        self.token = None

        url = f"{self.base_url}/auth/token"
        payload = json.dumps({
            "username": user,
            "pwd": pwd
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

    @staticmethod
    def get_subset(objects: list, keys: list) -> list:
        return [{key: obj[key] for key in keys} for obj in objects]

    def get_activated_nodes(self) -> list:
        url = f"{self.base_url}/active/node"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        nodes = response.json()['data']['info_list']
        return I2UP.get_subset(nodes, ['address', 'node_name', 'node_uuid'])

    def get_node_uuid(self, name: str) -> str:
        for node in self.get_activated_nodes():
            if name == node['node_name']:
                return node['node_uuid']
        print(f'Cannot find {name}')
        return ''

    def get_activated_node(self, name: str) -> dict:
        url = f"{self.base_url}/active/node/{self.get_node_uuid(name)}"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['active_node']

    def get_db_nodes(self) -> list:
        url = f"{self.base_url}/active/db"
        headers = {
            'Authorization': self.token
        }
        response = requests.request("GET", url, headers=headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        dbs = response.json()['data']['info_list']
        return I2UP.get_subset(dbs, ['db_name', 'db_type', 'db_uuid'])

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
        rules = response.json()['data']['info_list']
        return I2UP.get_subset(rules, ['mysql_name', 'mysql_uuid', 'src_db_name', 'tgt_db_name'])

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
    parser = argparse.ArgumentParser(description='I2UP utilities')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--version', action='store_true', help='Show version')
    group.add_argument('--list-nodes', action='store_true', help='List activated nodes')
    group.add_argument('--show-node', action='store_true', help='Show an activated node (with --node)')
    group.add_argument('--list-dbs', action='store_true', help='List DB nodes')
    group.add_argument('--show-db', action='store_true', help='Show a DB node (with --db)')
    group.add_argument('--create-db', action='store_true', help='Create a DB node (with --json)')
    group.add_argument('--delete-db', action='store_true', help='Delete a DB node (with --db)')
    group.add_argument('--list-rules', action='store_true', help='List MySQL sync rules')
    group.add_argument('--show-rule', action='store_true', help='Show a MySQL sync rule (with --rule)')
    group.add_argument('--create-rule', action='store_true', help='Create a MySQL sync rule (with --json)')
    group.add_argument('--delete-rule', action='store_true', help='Delete a MySQL sync rule (with --rule)')

    parser.add_argument('--ip', required=True, help='IP address or hostname')
    parser.add_argument('--port', required=False, type=int, default=58086, help='Port number (default: 58086)')
    parser.add_argument('--user', required=False, default='admin', help='Username (default: admin)')
    parser.add_argument('--pwd', required=False, default='Info@1234', help='Password (default: Info@1234)')
    parser.add_argument('--ca', required=False, default='ca.crt', help='Path of ca file (default: ca.crt)')
    parser.add_argument('--node', required=False, help='Name of activated node')
    parser.add_argument('--db', required=False, help='Name of DB node')
    parser.add_argument('--rule', required=False, help='Name of MySQL sync rule')
    parser.add_argument('--json', required=False, help='Path of json file to create DB/rule')

    args = parser.parse_args()
    i2up = I2UP(args.ip, args.port, args.user, args.pwd, args.ca)

    if args.version:
        print(i2up.get_version())
    elif args.list_nodes:
        nodes = i2up.get_activated_nodes()
        print("count(%d)" % len(nodes))
        pprint(nodes)
    elif args.show_node:
        assert args.node is not None
        pprint(i2up.get_activated_node(args.node))
    elif args.list_dbs:
        dbs = i2up.get_db_nodes()
        print("count(%d)" % len(dbs))
        pprint(dbs)
    elif args.show_db:
        assert args.db is not None
        pprint(i2up.get_db_node(args.db))
    elif args.create_db:
        assert args.json is not None
        pprint(i2up.create_db_node(args.json))
    elif args.delete_db:
        assert args.db is not None
        pprint(i2up.delete_db_node(args.db))
    elif args.list_rules:
        rules = i2up.get_mysql_rules()
        print("count(%d)" % len(rules))
        pprint(rules)
    elif args.show_rule:
        assert args.rule is not None
        pprint(i2up.get_mysql_rule(args.rule))
    elif args.create_rule:
        assert args.json is not None
        pprint(i2up.create_mysql_rule(args.json))
    elif args.delete_rule:
        assert args.rule is not None
        pprint(i2up.delete_mysql_rule(args.rule))


if __name__ == "__main__":
    main()
