#! /usr/bin/python3
import argparse
import json
import os
import time
from pprint import pprint

from i2up import I2UP
from json_tool import process_uuid


class Offline:
    def __init__(self, i2up: I2UP):
        self.i2up = i2up

    def list_offline_rules(self):
        info_list = self.i2up.get_offline_rules()
        print("count(%d)" % len(info_list))
        pprint(info_list)

    def dump_offline_rule(self, path: str, name: str, suffix: str):
        dic = self.i2up.get_offline_rule(name)
        dic['rule_name'] = name.strip() + suffix
        dic.pop('state', None)
        dic.pop('status', None)

        dic = process_uuid(dic)
        if dic['src_type'] == "dump_format_file":
            dic['src_node_uuid'] = dic['src_node_name']
        else:
            dic['src_db_uuid'] = dic['src_db_name']
        if dic['tgt_type'] == "dump_format_file":
            dic['node_uuid'] = dic['node_name']
        else:
            dic['tgt_db_uuid'] = dic['tgt_db_name']
        os.makedirs(path, exist_ok=True)
        file = f"{path}/{dic['rule_name']}.json"
        print("write to %s" % file)
        with open(file, 'w') as f:
            json.dump(dic, f, indent=4, sort_keys=True)

    def dump_offline_rules(self, path: str, suffix):
        info_list = self.i2up.get_offline_rules()
        idx = -1
        for idx, rule in enumerate(info_list):
            self.dump_offline_rule(path, rule['rule_name'], suffix)
            time.sleep(0.1)
        print("count(%d)" % (idx + 1))    

    def load_offline_rule(self, json_file: str):
        print(f"load {json_file}")
        pprint(self.i2up.create_offline_rule(I2UP.load_json_file(json_file)))

    def load_offline_rules(self, path: str, suffix: str):
        files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(suffix + '.json')]
        idx = -1
        for idx, file in enumerate(files):
            self.load_offline_rule(file)
            time.sleep(0.1)
        print("count(%d)" % (idx + 1))

    def delete_offline_rule(self, name: str):
        print(f"delete {name}")
        pprint(self.i2up.delete_offline_rule(name))

    def delete_offline_rules(self, path: str, suffix: str):
        idx = -1
        for idx, file in enumerate(os.listdir(path)):
            if file.endswith(suffix + '.json'):
                name = file.rstrip('.json')
                self.delete_offline_rule(name)
            time.sleep(0.1)
        print("count(%d)" % (idx + 1))


# offline.py --ip 172.20.73.231 --pwd Info2020! --list-offline-rules
# offline.py --ip 172.20.73.231 --pwd Info2020! --dump-offline-rule --rule 新方案gdb238-informix --suffix _bak
# offline.py --ip 172.20.73.231 --pwd Info2020! --dump-offline-rules --suffix _bak
# offline.py --ip 172.20.73.231 --pwd Info2020! --load-offline-rule --json rules/新方案gdb238-informix_bak.json
# offline.py --ip 172.20.73.231 --pwd Info2020! --delete-offline-rule --rule 新方案gdb238-informix_bak
# offline.py --ip 172.20.73.231 --pwd Info2020! --load-offline-rules --path rules --suffix _bak
# offline.py --ip 172.20.73.231 --pwd Info2020! --delete-offline-rules --path rules --suffix _bak

def main():
    parser = argparse.ArgumentParser(description='Offline utilities')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list-offline-rules', action='store_true', help='list offline rules')
    group.add_argument('--dump-offline-rule', action='store_true', help='dump offline rule to json file')
    group.add_argument('--dump-offline-rules', action='store_true', help='dump offline rules to json files')
    group.add_argument('--load-offline-rule', action='store_true', help='load json file to offline rule')
    group.add_argument('--load-offline-rules', action='store_true', help='load json files to offline rules')
    group.add_argument('--delete-offline-rule', action='store_true', help='delete offline rule')
    group.add_argument('--delete-offline-rules', action='store_true', help='delete offline rules')

    parser.add_argument('--ip', required=True, help='IP address or hostname')
    parser.add_argument('--port', required=False, type=int, default=58086, help='Port number (default: 58086)')
    parser.add_argument('--ca', required=False, default='ca.crt', help='Path of ca file (default: ca.crt)')
    parser.add_argument('--user', required=False, default='admin', help='Username (default: admin)')
    parser.add_argument('--pwd', required=True, help='Password of the user')
    parser.add_argument('--path', required=False, default='rules',
                        help='Path to dump/load json file(s) (default: rules)')
    parser.add_argument('--json', required=False, help='Path of json file to load')
    parser.add_argument('--rule', required=False, help='Name of rule')
    parser.add_argument('--suffix', required=False, default='', help='suffix of rule name (default: \'\')')

    args = parser.parse_args()
    offline = Offline(I2UP(args.ip, args.port, args.ca, user=args.user, pwd=args.pwd))

    if args.list_offline_rules:
        offline.list_offline_rules()
    elif args.dump_offline_rule:
        assert args.rule is not None
        offline.dump_offline_rule(args.path, args.rule, args.suffix)
    elif args.dump_offline_rules:
        offline.dump_offline_rules(args.path, args.suffix)
    elif args.load_offline_rule:
        assert args.json is not None
        offline.load_offline_rule(args.json)
    elif args.load_offline_rules:
        offline.load_offline_rules(args.path, args.suffix)
    elif args.delete_offline_rule:
        assert args.rule
        offline.delete_offline_rule(args.rule)
    elif args.delete_offline_rules:
        offline.delete_offline_rules(args.path, args.suffix)


if __name__ == "__main__":
    main()
