#! /usr/bin/python3
import argparse
import json
from pprint import pprint

import requests


class I2UP:
    def __init__(self, ip: str, port: int, ca_path: str, ak_path: str = None, user: str = None, pwd: str = None):
        self.ca_path = ca_path
        self.base_url = f"https://{ip}:{port}/api"
        self.headers = {
            'Content-Type': 'application/json'
        }
        if ak_path is not None:
            with open(ak_path, 'r') as f:
                self.headers['ACCESS-KEY'] = f.readline().strip()
        elif user is not None and pwd is not None:
            url = f"{self.base_url}/auth/token"
            payload = json.dumps({
                "username": user,
                "pwd": pwd
            })
            response = requests.request("POST", url, headers=self.headers, data=payload, verify=self.ca_path)
            response.raise_for_status()
            token = response.json()['data']['token']
            # print("token(%s)" % token)
            self.headers['Authorization'] = token
        else:
            assert False

    def get_version(self) -> str:
        url = f"{self.base_url}/version"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['version']

    def get_credentials(self) -> list:
        url = f"{self.base_url}/credential"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list']

    def get_credential(self, name: str) -> dict:
        for credential in self.get_credentials():
            if name == credential['cred_name']:
                return credential
        return {}

    @staticmethod
    def get_subset(objects: list, keys: list) -> list:
        return [{key: obj[key] for key in keys} for obj in objects]

    def get_inactive_nodes(self) -> list:
        url = f"{self.base_url}/active/node/inactive_list"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        nodes = response.json()['data']['info_list']
        return I2UP.get_subset(nodes, ['address', 'node_name', 'node_uuid'])

    def get_inactive_node(self, name: str) -> dict:
        url = f"{self.base_url}/active/node/inactive_list"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        for node in response.json()['data']['info_list']:
            if name == node['node_name']:
                return node
        return {}

    def activate_node(self, node: dict) -> dict:
        url = f"{self.base_url}/active/node"
        node2 = self.get_inactive_node(node['hostname'])
        assert node2
        if 'address' in node:
            assert node2['address'].split(',')[0] == node['address']
        payload = json.dumps({
            "active_flag": "active",
            "address": node2['address'],
            "cache_dir": node['cache_dir'],
            "data_port": "26804" if 'data_port' not in node else str(node['data_port']),
            "log_dir": node['log_dir'],
            "node_name": node['node_name'],
            "node_type": node['node_type'],
            "node_uuid": node2['node_uuid'],
            "password": node['password'],
            "web_uuid": "00000000-0000-0000-0000-000000000000"
        })
        response = requests.request("POST", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def activate_node2(self, name: str, name2: str, password: str, source: bool, target: bool, data_path='/var/iadata')\
            -> dict:
        dic = {
            "hostname": name,
            "cache_dir": f"{data_path}/cache/",
            "log_dir": f"{data_path}/log/",
            "node_name": name if name2 is None else name2,
            "node_type": f"{1 if source else 0}{1 if target else 0}00",
            "password": password,
        }
        return self.activate_node(dic)

    def get_active_nodes(self) -> list:
        url = f"{self.base_url}/active/node"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        nodes = response.json()['data']['info_list']
        return I2UP.get_subset(nodes, ['address', 'node_name', 'node_uuid'])

    def get_node_uuid(self, name: str) -> str:
        for node in self.get_active_nodes():
            if name == node['node_name']:
                return node['node_uuid']
        print(f'Cannot find node "{name}"')
        return ''

    def get_active_node(self, name: str) -> dict:
        uuid = self.get_node_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/active/node/{uuid}"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['active_node']

    def delete_active_node(self, name: str, force: bool) -> dict:
        uuid = self.get_node_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/active/node"
        payload = json.dumps({
            "uuids": [
                uuid
            ],
            "force": 1 if force else 0
        })
        response = requests.request("DELETE", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def get_db_nodes(self) -> list:
        url = f"{self.base_url}/active/db"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        dbs = response.json()['data']['info_list']
        return I2UP.get_subset(dbs, ['db_name', 'db_type', 'db_uuid'])

    def get_db_uuid(self, name: str) -> str:
        for db in self.get_db_nodes():
            if name == db['db_name']:
                return db['db_uuid']
        print(f'Cannot find db "{name}"')
        return ''

    def get_db_node(self, name: str) -> dict:
        uuid = self.get_db_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/active/db/{uuid}"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['active_db']

    def get_lic_uuid(self) -> str:
        url = f"{self.base_url}/lic"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list'][0]['lic_uuid']

    @staticmethod
    def load_json_file(json_file: str) -> dict:
        with open(json_file, 'r') as f:
            json_data = json.load(f)
        return json_data

    def create_db_node(self, json_data: dict) -> dict:
        url = f"{self.base_url}/active/db"
        if json_data['db_type'] != 'kafka':
            json_data["bind_lic_list"] = [self.get_lic_uuid()]
        json_data['node_uuid'] = self.get_node_uuid(json_data['node_uuid'])
        for user in json_data['config']['user_management']:
            if 'cred_uuid' in user:
                user['cred_uuid'] = self.get_credential(user['cred_uuid'])['cred_uuid']
        payload = json.dumps(json_data)
        response = requests.request("POST", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def delete_db_node(self, name: str) -> dict:
        uuid = self.get_db_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/active/db"
        payload = json.dumps({
            "uuids": [
                uuid
            ],
            "force": 0
        })
        response = requests.request("DELETE", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def get_mysql_rules(self) -> list:
        rules = []
        for url in [f"{self.base_url}/stream/rule", f"{self.base_url}/hbase/rule"]:
            response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
            response.raise_for_status()
            rules += response.json()['data']['info_list']
        return I2UP.get_subset(rules, ['mysql_name', 'mysql_uuid', 'src_db_name', 'tgt_db_name'])

    def get_mysql_rule_uuid(self, name: str) -> str:
        for node in self.get_mysql_rules():
            if name == node['mysql_name']:
                return node['mysql_uuid']
        print(f'Cannot find rule "{name}"')
        return ''

    def get_mysql_rule(self, name: str) -> dict:
        uuid = self.get_mysql_rule_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/stream/rule/{uuid}"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['info_list']

    def create_mysql_rule(self, json_data: dict) -> dict:
        url = f"{self.base_url}/stream/rule"
        if 'src_type' in json_data and 'hbase' == json_data['src_type']:
            url = f"{self.base_url}/hbase/rule"
        json_data['src_db_uuid'] = self.get_db_uuid(json_data['src_db_uuid'])
        json_data['tgt_db_uuid'] = self.get_db_uuid(json_data['tgt_db_uuid'])
        payload = json.dumps(json_data)
        response = requests.request("POST", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def delete_mysql_rule(self, name: str) -> dict:
        uuid = self.get_mysql_rule_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/stream/rule"
        payload = json.dumps({
            "mysql_uuids": [
                uuid
            ],
            "force": False
        })
        response = requests.request("DELETE", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def get_offline_rules(self) -> list:
        url = f"{self.base_url}/offline_rule"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        rules = response.json()['data']['info_list']
        result = []
        for rule in rules:
            keys = ['rule_name', 'rule_uuid', 'src_db_name',
                    'tgt_db_name' if rule['tgt_type'] != 'dump_format_file' else 'tgt_file_path']
            result.append({key: rule[key] for key in keys})
        return result

    def get_offline_rule_uuid(self, name: str) -> str:
        for node in self.get_offline_rules():
            if name == node['rule_name']:
                return node['rule_uuid']
        print(f'Cannot find rule "{name}"')
        return ''

    def get_offline_rule(self, name: str) -> dict:
        uuid = self.get_offline_rule_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/offline_rule/{uuid}"
        response = requests.request("GET", url, headers=self.headers, data={}, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']['offline_rule']

    def create_offline_rule(self, json_data: dict) -> dict:
        url = f"{self.base_url}/offline_rule"
        if json_data['src_type'] != 'dump_format_file':
            json_data['src_db_uuid'] = self.get_db_uuid(json_data['src_db_uuid'])
        else:
            json_data['src_node_uuid'] = self.get_node_uuid(json_data['src_node_uuid'])
        if json_data['tgt_type'] != 'dump_format_file':
            json_data['tgt_db_uuid'] = self.get_db_uuid(json_data['tgt_db_uuid'])
        else:
            json_data['node_uuid'] = self.get_node_uuid(json_data['node_uuid'])
        payload = json.dumps(json_data)
        response = requests.request("POST", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']

    def delete_offline_rule(self, name: str) -> dict:
        uuid = self.get_offline_rule_uuid(name)
        if uuid == '':
            return {}
        url = f"{self.base_url}/offline_rule"
        payload = json.dumps({
            "rule_uuids": [
                uuid
            ],
            "force": False
        })
        response = requests.request("DELETE", url, headers=self.headers, data=payload, verify=self.ca_path)
        response.raise_for_status()
        return response.json()['data']


def main():
    parser = argparse.ArgumentParser(description='I2UP utilities')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--version', action='store_true', help='Show version')
    group.add_argument('--list-inactive-nodes', action='store_true', help='List inactive nodes')
    group.add_argument('--show-inactive-node', action='store_true', help='Show a inactive node (with --node)')
    group.add_argument('--list-nodes', action='store_true', help='List active nodes')
    group.add_argument('--show-node', action='store_true', help='Show an active node (with --node)')
    group.add_argument('--activate-node', action='store_true',
                       help='Activate a inactive node (with --node [--pwd] [--src] [--tgt] [--path])')
    group.add_argument('--delete-node', action='store_true', help='Delete an active node (with --node)')
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
    parser.add_argument('--ca', required=False, default='ca.crt', help='Path of ca file (default: ca.crt)')
    parser.add_argument('--ak', required=False, help='Path of AccessKey file')
    parser.add_argument('--user', required=False, default='admin', help='Username (default: admin)')
    parser.add_argument('--pwd', required=False, help='Password of the user')
    parser.add_argument('--node', required=False, help='Name of active/inactive node')
    parser.add_argument('--node2', required=False, help='New name assigns to an activating node')
    parser.add_argument('--pwd2', required=False, default='Info@1234',
                        help='Password to activate node (default: Info@1234)')
    parser.add_argument('--src', required=False, action='store_true',
                        help='Is a source node (just a flag without argument)')
    parser.add_argument('--tgt', required=False, action='store_true',
                        help='Is a target node (just a flag without argument)')
    parser.add_argument('--path', required=False, default='/var/iadata',
                        help='Parent dir of cache & log (default: /var/iadata)')
    parser.add_argument('--db', required=False, help='Name of DB node')
    parser.add_argument('--rule', required=False, help='Name of MySQL sync rule')
    parser.add_argument('--json', required=False, help='Path of json file to create DB/rule')

    args = parser.parse_args()
    if args.ak is not None:
        i2up = I2UP(args.ip, args.port, args.ca, args.ak)
    elif args.user is not None and args.pwd is not None:
        i2up = I2UP(args.ip, args.port, args.ca, user=args.user, pwd=args.pwd)
    else:
        assert False

    if args.version:
        print(i2up.get_version())
    elif args.list_inactive_nodes:
        nodes = i2up.get_inactive_nodes()
        print("count(%d)" % len(nodes))
        pprint(nodes)
    elif args.show_inactive_node:
        assert args.node is not None
        pprint(i2up.get_inactive_node(args.node))
    elif args.list_nodes:
        nodes = i2up.get_active_nodes()
        print("count(%d)" % len(nodes))
        pprint(nodes)
    elif args.show_node:
        assert args.node is not None
        pprint(i2up.get_active_node(args.node))
    elif args.activate_node:
        assert args.node and (args.src or args.tgt)
        pprint(i2up.activate_node2(args.node, args.node2, args.pwd2, args.src, args.tgt))
    elif args.delete_node:
        assert args.node is not None
        pprint(i2up.delete_active_node(args.node, True))
    elif args.list_dbs:
        dbs = i2up.get_db_nodes()
        print("count(%d)" % len(dbs))
        pprint(dbs)
    elif args.show_db:
        assert args.db is not None
        pprint(i2up.get_db_node(args.db))
    elif args.create_db:
        assert args.json is not None
        pprint(i2up.create_db_node(I2UP.load_json_file(args.json)))
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
        pprint(i2up.create_mysql_rule(I2UP.load_json_file(args.json)))
    elif args.delete_rule:
        assert args.rule is not None
        pprint(i2up.delete_mysql_rule(args.rule))


if __name__ == "__main__":
    main()
