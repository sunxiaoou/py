#! /usr/bin/python3
import argparse
import json
import os
from pprint import pprint

import pandas as pd

from i2up import I2UP


class Excel:
    # sheet names
    WORK_NODE = 'work_node'
    MSQ_NODE = 'msq_node'
    HB_NODE = 'hb_node'
    KFK_NODE = 'kfk_node'
    MSQ_MSQ_RULE = 'msq_msq_rule'
    HB_HB_RULE = 'hb_hb_rule'
    MSQ_KFK_RULE = 'msq_kfk_rule'

    def __init__(self, name: str, template: str):
        self.name = name
        self.template = template

    def get_nodes(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
        df['节点类型'] = df['节点类型'].apply(lambda x: f"{1 if '源端节点' in x else 0}{1 if '备端节点' in x else 0}00")
        df = df.drop(columns=['序号'])
        df.columns = ['node_name', 'address', 'data_port', 'cache_dir', 'log_dir', 'password', 'node_type']
        return df.to_dict(orient='records')

    def get_dbs(self, sheet: str) -> list:
        try:
            df = pd.read_excel(self.name, sheet_name=sheet)
        except ValueError:
            return []
        data_list = []
        current_record = None
        for _, row in df.iterrows():
            if pd.notna(row['序号']):
                if current_record is not None:
                    data_list.append(current_record)
                roles = []
                for i in row['角色'].split('|') if pd.notna(row['角色']) else []:
                    if i in ['source', '源库']:
                        roles.append('source')
                    elif i in ['target', '备库']:
                        roles.append('target')
                    else:
                        assert False
                db_list = [{
                    "ip": row['IP地址'],
                    "port": int(row['端口'])
                }] if pd.notna(row['IP地址']) and pd.notna(row['端口']) else []
                zk_set = [{
                    "ip": row['zkIP'],
                    "port": int(row['zk端口']),
                    "zk_node": row['zk节点']
                }] if Excel.HB_NODE == sheet and pd.notna(row['zkIP']) and pd.notna(row['zk端口'] and row['zk节点'])\
                    else []
                zookeeper = {"set": zk_set}
                user_management = []
                if Excel.MSQ_NODE == sheet and pd.notna(row['凭据名称']):
                    user_management.append({
                        "cred_login": 1,
                        "cred_uuid": row['凭据名称'],
                        "default_db": row['默认数据库']
                    })
                elif Excel.MSQ_NODE == sheet and pd.notna(row['用户名']) and pd.notna(row['密码']):
                    user_management.append({
                        "user": row['用户名'],
                        "passwd": row['密码'],
                        "default_db": row['默认数据库']
                    })

                current_record = {
                    "config": {
                        "db_list": db_list,
                        "role": roles,
                        "user_management": user_management
                    },
                    "db_name": row['名称'],
                    "db_type": row['数据库类型'],
                    "node_uuid": row['工作节点'],
                    "username": row['所有者']
                }
                if Excel.HB_NODE == sheet:
                    current_record["config"]["zookeeper"] = zookeeper
            else:
                if pd.notna(row['IP地址']) and pd.notna(row['端口']):
                    current_record["db_list"].append({
                        "ip": row['IP地址'],
                        "port": int(row['端口'])
                    })
                if Excel.HB_NODE == sheet and pd.notna(row['zkIP']):
                    current_record["config"]["zookeeper"]["set"].append({
                        "ip": row['zkIP'],
                        "port": int(row['zk端口']),
                        "zk_node": row['zk节点']
                    })
                if Excel.MSQ_NODE == sheet and pd.notna(row['cred_name']) and row['cred_name'].strip() != "":
                    current_record["user_management"].append({
                        "cred_login": 1,
                        "cred_name": row['凭据名称'],
                        "default_db": row['默认数据库']
                    })
                elif Excel.MSQ_NODE == sheet and pd.notna(row['用户名']) and pd.notna(row['密码']):
                    current_record["user_management"].append({
                        "user": row['用户名'],
                        "passwd": row['密码'],
                        "default_db": row['默认数据库']
                    })
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_kfks(self, sheet: str) -> list:
        try:
            df = pd.read_excel(self.name, sheet_name=sheet)
        except ValueError:
            return []
        data_list = []
        current_record = None
        for _, row in df.iterrows():
            if pd.notna(row['序号']):
                if current_record is not None:
                    data_list.append(current_record)
                roles = []
                for i in row['角色'].split('|') if pd.notna(row['角色']) else []:
                    if i in ['source', '源库']:
                        roles.append('source')
                    elif i in ['target', '备库']:
                        roles.append('target')
                    else:
                        assert False
                auth = 'none'
                if pd.notna(row['kafka凭证']) and pd.notna('kafka服务名') and pd.notna('keytab路径'):
                    auth = 'kerberos'
                db_list = [{"ip": row['IP地址'], "port": int(row['端口'])}] \
                    if pd.notna(row['IP地址']) and pd.notna(row['端口']) else []
                user_management = []
                if pd.notna(row['kafka凭证']) and pd.notna(row['keytab路径'] and pd.notna(row['kafka服务名'])):
                    user_management.append({
                        "user": row['kafka凭证'],
                        "passwd": row['keytab路径'],
                        "default_db": row['kafka服务名']
                    })
                current_record = {
                    "config": {
                        "db_list": db_list,
                        "auth": auth,
                        "role": roles,
                        "user_management": user_management
                    },
                    "db_name": row['名称'],
                    "db_type": row['数据库类型'],
                    "node_uuid": row['工作节点'],
                    "username": row['所有者']
                }
            else:
                if pd.notna(row['IP地址']) and pd.notna(row['端口']):
                    current_record["db_list"].append({
                        "ip": row['IP地址'],
                        "port": int(row['端口'])
                    })
                if pd.notna(row['kafka凭证']) and pd.notna(row['keytab路径'] and pd.notna(row['kafka服务名'])):
                    current_record["user_management"].append({
                        "user": row['kafka凭证'],
                        "passwd": row['keytab路径'],
                        "default_db": row['kafka服务名']
                    })
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_msq_msq_rules(self, sheet: str) -> list:
        try:
            df = pd.read_excel(self.name, sheet_name=sheet)
        except ValueError:
            return []
        data_list = []
        current_record = None
        for _, row in df.iterrows():
            if pd.notna(row['序号']):
                if current_record is not None:
                    data_list.append(current_record)
                dm_track = {}
                if pd.notna(row['操作装载时间和日期']):
                    dm_track["date_time_column"] = row['操作装载时间和日期']
                if pd.notna(row['操作装载标记']):
                    dm_track["op_column"] = row['操作装载标记']
                full_sync_custom_cfg = [row['全量自定义配置']] if pd.notna(row['全量自定义配置']) else []
                incre_full_sync_custom_cfg = [row['增量自定义配置']] if pd.notna(row['增量自定义配置']) else []
                map_type = ''
                db_map = []
                tab_map = []
                if pd.notna(row['源端库名']):
                    if pd.notna(row['源端表名']):
                        map_type = 'table'
                        tab_map = [{
                            "dst_db": row['备端库名'],
                            "dst_table": row['备端表名'],
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名']
                        }]
                    else:
                        map_type = 'database'
                        db_map = [{
                            "dst_table": row['备端库名'],
                            "src_table": row['源端库名']
                        }]
                current_record = {
                    "db_map": db_map,
                    "full_sync": 1 if row['全量同步'] == 'yes' else 0,
                    "config": {
                        "full_sync_settings": {
                            "dump_thd": int(row['全量导出线程数']) if pd.notna(row['全量导出线程数']) else None,
                            "existing_table": row['全量表覆盖策略'],
                            "full_sync_custom_cfg": full_sync_custom_cfg,
                            "load_thd": int(row['全量装载线程数']) if pd.notna(row['全量装载线程数']) else None,
                        }
                    },
                    "dml_track": dm_track,
                    "incre_sync": 1 if row['增量同步'] == 'yes' else 0,
                    "mysql_name": row['规则名称'],
                    "map_type": map_type,
                    "other_settings": {
                        "dyn_thread": int(row['增量装载线程数']) if pd.notna(row['增量装载线程数']) else None,
                        "incre_full_sync_custom_cfg": incre_full_sync_custom_cfg
                    },
                    "src_db_uuid": row['源端数据库'],
                    "tab_map": tab_map,
                    "tgt_db_uuid": row['备端数据库'],
                    "username": row['所有者']
                }
            else:
                if pd.notna(row['全量自定义配置']):
                    current_record["full_sync_settings"]["full_sync_custom_cfg"].append(row['全量自定义配置'])
                if pd.notna(row['增量自定义配置']):
                    current_record["other_settings"]["incre_full_sync_custom_cfg"].append(row['增量自定义配置'])
                if pd.notna(row['源端库名']):
                    if pd.notna(row['源端表名']):
                        current_record["tab_map"].append({
                            "dst_db": row['备端库名'],
                            "dst_table": row['备端表名'],
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名']
                        })
                    else:
                        current_record["db_map"].append({
                            "dst_table": row['备端库名'],
                            "src_table": row['源端库名']
                        })
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_hb_hb_rules(self, sheet: str) -> list:
        try:
            df = pd.read_excel(self.name, sheet_name=sheet)
        except ValueError:
            return []
        data_list = []
        current_record = None
        for _, row in df.iterrows():
            if pd.notna(row['序号']):
                if current_record is not None:
                    data_list.append(current_record)
                map_type = ''
                db_map = []
                tab_map = []
                if pd.notna(row['源端库名']):
                    if pd.notna(row['源端表名']):
                        map_type = 'table'
                        tab_map = [{
                            "dst_db": row['备端库名'],
                            "dst_table": row['备端表名'],
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名']
                        }]
                    else:
                        map_type = 'database'
                        db_map = [{
                            "dst_table": row['备端库名'],
                            "src_table": row['源端库名']
                        }]
                current_record = {
                    "db_map": db_map,
                    "config": {
                        "full_sync_settings": {
                            "existing_table": row['全量表覆盖策略'],

                        },
                        "rpc_server": {
                            "peer": row['rpcSvrPeer'],
                            "zookeeper": {
                                "set": [{
                                    "port": int(row['rpcSvrZkPort']),
                                    "ip": row['rpcSvrZkAddress'],
                                    "zk_node": row['rpcSvrZkNode']
                                }]
                            }
                        }
                    },
                    "mysql_name": row['规则名称'],
                    "map_type": map_type,
                    "src_db_uuid": row['源端数据库'],
                    "tab_map": tab_map,
                    "tgt_db_uuid": row['备端数据库'],
                    "username": row['所有者']
                }
            else:
                if pd.notna(row['源端库名']):
                    if pd.notna(row['源端表名']):
                        current_record["tab_map"].append({
                            "dst_db": row['备端库名'],
                            "dst_table": row['备端表名'],
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名']
                        })
                    else:
                        current_record["db_map"].append({
                            "dst_table": row['备端库名'],
                            "src_table": row['源端库名']
                        })
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_msq_kfk_rules(self, sheet: str) -> list:
        try:
            df = pd.read_excel(self.name, sheet_name=sheet)
        except ValueError:
            return []
        data_list = []
        current_record = None
        for _, row in df.iterrows():
            if pd.notna(row['序号']):
                if current_record is not None:
                    data_list.append(current_record)
                full_sync_custom_cfg = [row['全量自定义配置']] if pd.notna(row['全量自定义配置']) else []
                incre_full_sync_custom_cfg = [row['增量自定义配置']] if pd.notna(row['增量自定义配置']) else []
                map_type = ''
                db_map = []
                tab_map = []
                if pd.notna(row['源端库名']):
                    if pd.notna(row['源端表名']):
                        map_type = 'table'
                        tab_map = [{
                            "dst_db": row['备端topic'],
                            "dst_table": row['备端topic'],
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名']
                        }]
                    else:
                        map_type = 'database'
                        db_map = [{
                            "dst_table": row['备端topic'],
                            "src_table": row['源端库名']
                        }]
                current_record = {
                    "db_map": db_map,
                    "full_sync": 1 if row['全量同步'] == 'yes' else 0,
                    "config": {
                        "full_sync_settings": {
                            "dump_thd": int(row['全量导出线程数']) if pd.notna(row['全量导出线程数']) else None,
                            "full_sync_custom_cfg": full_sync_custom_cfg,
                            "load_thd": int(row['全量装载线程数']) if pd.notna(row['全量装载线程数']) else None,
                        }
                    },
                    "incre_sync": 1 if row['增量同步'] == 'yes' else 0,
                    "mysql_name": row['规则名称'],
                    "map_type": map_type,
                    "other_settings": {
                        "dyn_thread": int(row['增量装载线程数']) if pd.notna(row['增量装载线程数']) else None,
                        "incre_full_sync_custom_cfg": incre_full_sync_custom_cfg
                    },
                    "src_db_uuid": row['源端数据库'],
                    "tab_map": tab_map,
                    "tgt_db_uuid": row['备端数据库'],
                    "username": row['所有者']
                }
            else:
                if pd.notna(row['全量自定义配置']):
                    current_record["full_sync_settings"]["full_sync_custom_cfg"].append(row['全量自定义配置'])
                if pd.notna(row['增量自定义配置']):
                    current_record["other_settings"]["incre_full_sync_custom_cfg"].append(row['增量自定义配置'])
                if pd.notna(row['源端库名']):
                    if pd.notna(row['源端表名']):
                        current_record["tab_map"].append({
                            "dst_db": row['备端topic'],
                            "dst_table": row['备端topic'],
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名']
                        })
                    else:
                        current_record["db_map"].append({
                            "dst_table": row['备端topic'],
                            "src_table": row['源端库名']
                        })
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    @staticmethod
    def merge_dict(default_dict: dict, subset_dict: dict):
        for key, value in subset_dict.items():
            if isinstance(value, dict) and isinstance(default_dict.get(key), dict):
                Excel.merge_dict(default_dict[key], value)
            else:
                default_dict[key] = value

    def generate_creation(self, t_sheet: str, obj_dict: dict) -> dict:
        df = pd.read_excel(self.template, sheet_name=t_sheet, header=None)
        json_str = ''
        for _, row in df.iterrows():
            row_str = " ".join(['null' if str(cell) == 'Null' else str(cell) for cell in row if pd.notna(cell)])
            json_str += row_str + "\n"
        json_data = json.loads(json_str)
        Excel.merge_dict(json_data, obj_dict)
        return json_data

    def generate_creation_json(self, t_sheet: str, obj_dict: dict, output: str):
        json_data = self.generate_creation(t_sheet, obj_dict)
        key = ''
        if t_sheet in [Excel.HB_NODE, Excel.KFK_NODE, Excel.MSQ_NODE]:
            key = 'db_name'
        elif t_sheet in [Excel.HB_HB_RULE, Excel.MSQ_KFK_RULE, Excel.MSQ_MSQ_RULE]:
            key = 'mysql_name'
        file = f"{output}/{obj_dict[key]}.json"
        with open(file, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"{file} generated according to {t_sheet} in {self.template}")

    def generate_csvs(self, output: str):
        excel_file = pd.ExcelFile(self.name)
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            csv_file_path = f"{output}/{sheet_name}.csv"
            df.to_csv(csv_file_path, index=False, header=False, encoding='utf-8')
            print(f"Sheet '{sheet_name}' saved to '{csv_file_path}'")


def generate_all_csv(output: str):
    os.makedirs(output, exist_ok=True)
    excel = Excel('excel/zx-test-env_2.xlsx', None)
    excel.generate_csvs(output)


def generate_all_json(excel: Excel, output: str):
    for node in excel.get_dbs(Excel.MSQ_NODE):
        excel.generate_creation_json(Excel.MSQ_NODE, node, output)
    for node in excel.get_dbs(Excel.HB_NODE):
        excel.generate_creation_json(Excel.HB_NODE, node, output)
    for node in excel.get_kfks(Excel.KFK_NODE):
        excel.generate_creation_json(Excel.KFK_NODE, node, output)
    for rule in excel.get_msq_msq_rules(Excel.MSQ_MSQ_RULE):
        excel.generate_creation_json(Excel.MSQ_MSQ_RULE, rule, output)
    for rule in excel.get_hb_hb_rules(Excel.HB_HB_RULE):
        excel.generate_creation_json(Excel.HB_HB_RULE, rule, output)
    for rule in excel.get_msq_kfk_rules(Excel.MSQ_KFK_RULE):
        excel.generate_creation_json(Excel.MSQ_KFK_RULE, rule, output)


def delete_all_objects(excel: Excel, i2up: I2UP):
    for rule in excel.get_msq_kfk_rules(Excel.MSQ_KFK_RULE):
        name = rule['mysql_name']
        print(f"Deleting rule {name} ...")
        pprint(i2up.delete_mysql_rule(name))
    for rule in excel.get_hb_hb_rules(Excel.HB_HB_RULE):
        name = rule['mysql_name']
        print(f"Deleting rule {name} ...")
        pprint(i2up.delete_mysql_rule(name))
    for rule in excel.get_msq_msq_rules(Excel.MSQ_MSQ_RULE):
        name = rule['mysql_name']
        print(f"Deleting rule {name} ...")
        pprint(i2up.delete_mysql_rule(name))
    for node in excel.get_kfks(Excel.KFK_NODE):
        name = node["db_name"]
        print(f"Deleting db_node {name} ...")
        pprint(i2up.delete_db_node(name))
    for node in excel.get_dbs(Excel.HB_NODE):
        name = node["db_name"]
        print(f"Deleting db_node {name} ...")
        pprint(i2up.delete_db_node(name))
    for node in excel.get_dbs(Excel.MSQ_NODE):
        name = node["db_name"]
        print(f"Deleting db_node {name} ...")
        pprint(i2up.delete_db_node(name))


def create_all_objects(excel: Excel, i2up: I2UP):
    for node in excel.get_dbs(Excel.MSQ_NODE):
        name = node["db_name"]
        print(f"Creating db_node {name} ...")
        json_data = excel.generate_creation(Excel.MSQ_NODE, node)
        if i2up.get_db_uuid(name) == '':
            pprint(i2up.create_db_node(json_data))
        else:
            print(f"db {name} exists already")
    for node in excel.get_dbs(Excel.HB_NODE):
        name = node["db_name"]
        print(f"Creating db_node {name} ...")
        json_data = excel.generate_creation(Excel.HB_NODE, node)
        if i2up.get_db_uuid(name) == '':
            pprint(i2up.create_db_node(json_data))
        else:
            print(f"db {name} exists already")
    for node in excel.get_kfks(Excel.KFK_NODE):
        name = node["db_name"]
        print(f"Creating db_node {name} ...")
        json_data = excel.generate_creation(Excel.KFK_NODE, node)
        if i2up.get_db_uuid(name) == '':
            pprint(i2up.create_db_node(json_data))
        else:
            print(f"db {name} exists already")
    for rule in excel.get_msq_msq_rules(Excel.MSQ_MSQ_RULE):
        name = rule['mysql_name']
        print(f"Creating rule {name} ...")
        json_data = excel.generate_creation(Excel.MSQ_MSQ_RULE, rule)
        if i2up.get_mysql_rule_uuid(name) == '':
            pprint(i2up.create_mysql_rule(json_data))
        else:
            print(f"rule {name} exists already")
    for rule in excel.get_hb_hb_rules(Excel.HB_HB_RULE):
        name = rule['mysql_name']
        print(f"Creating rule {name} ...")
        json_data = excel.generate_creation(Excel.HB_HB_RULE, rule)
        if i2up.get_mysql_rule_uuid(name) == '':
            pprint(i2up.create_mysql_rule(json_data))
        else:
            print(f"rule {name} exists already")
    for rule in excel.get_msq_kfk_rules(Excel.MSQ_KFK_RULE):
        name = rule['mysql_name']
        print(f"Creating rule {name} ...")
        json_data = excel.generate_creation(Excel.MSQ_KFK_RULE, rule)
        if i2up.get_mysql_rule_uuid(name) == '':
            pprint(i2up.create_mysql_rule(json_data))
        else:
            print(f"rule {name} exists already")


def main():
    parser = argparse.ArgumentParser(description='Parse dbNodes/rules in a excel and create them in i2up')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--excel2json', action='store_true', help='Convert dbNodes/rules in excel to json files')
    group.add_argument('--deleteObjects', action='store_true', help='Delete dbNodes/rules in excel from i2up')
    group.add_argument('--createObjects', action='store_true', help='Create dbNodes/rules in excel into i2up')
    parser.add_argument('--ip', required=False, help='IP address or hostname')
    parser.add_argument('--port', required=False, type=int, default=58086, help='Port number (default: 58086)')
    parser.add_argument('--ca', required=False, default='ca.crt', help='Path of ca file (default: ca.crt)')
    parser.add_argument('--ak', required=False, help='Path of AccessKey file')
    parser.add_argument('--user', required=False, default='admin', help='Username (default: admin)')
    parser.add_argument('--pwd', required=False, help='Password of the user')
    parser.add_argument('--excel', required=True, help='Excel file contains dbNodes/rules')
    parser.add_argument('--template', required=False, help='Excel file contains dbNodes/rules template')
    parser.add_argument('--output', required=False, default='output',
                        help='output path of json files (default: output)')
    args = parser.parse_args()
    excel = Excel(args.excel, args.template)
    if args.excel2json:
        assert args.template is not None
        os.makedirs(args.output, exist_ok=True)
        generate_all_json(excel, args.output)
    elif args.deleteObjects:
        assert args.ip is not None
        if args.ak is not None:
            i2up = I2UP(args.ip, args.port, args.ca, args.ak)
        elif args.user is not None and args.pwd is not None:
            i2up = I2UP(args.ip, args.port, args.ca, user=args.user, pwd=args.pwd)
        else:
            assert False
        delete_all_objects(excel, i2up)
    elif args.createObjects:
        assert args.ip is not None and args.template is not None
        if args.ak is not None:
            i2up = I2UP(args.ip, args.port, args.ca, args.ak)
        elif args.user is not None and args.pwd is not None:
            i2up = I2UP(args.ip, args.port, args.ca, user=args.user, pwd=args.pwd)
        else:
            assert False
        create_all_objects(excel, i2up)


if __name__ == "__main__":
    main()
