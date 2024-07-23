#! /usr/bin/python3
import json
import os

import pandas as pd


class Excel:
    def __init__(self, name: str, template: str, output: str):
        self.name = name
        self.template = template
        self.output = output
        os.makedirs(output, exist_ok=True)

    def get_nodes(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
        df['节点类型'] = df['节点类型'].apply(lambda x: f"{1 if '源端节点' in x else 0}{1 if '备端节点' in x else 0}00")
        df = df.drop(columns=['序号'])
        df.columns = ['node_name', 'address', 'data_port', 'cache_dir', 'log_dir', 'password', 'node_type']
        return df.to_dict(orient='records')

    def get_dbs(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
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
                db_list = [{"ip": row['IP地址'], "port": int(row['端口'])}] \
                    if pd.notna(row['IP地址']) and pd.notna(row['端口']) else []
                user_management = []
                if pd.notna(row['凭据名称']):
                    user_management.append({
                        "cred_uuid": row['凭据名称'],
                        "default_db": row['默认数据库']
                    })
                elif pd.notna(row['用户名']) and pd.notna(row['密码']):
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
            else:
                if pd.notna(row['IP地址']) and pd.notna(row['端口']):
                    current_record["db_list"].append({
                        "ip": row['IP地址'],
                        "port": int(row['端口'])
                    })
                if pd.notna(row['cred_name']) and row['cred_name'].strip() != "":
                    current_record["user_management"].append({
                        "cred_name": row['凭据名称'],
                        "default_db": row['默认数据库']
                    })
                elif pd.notna(row['用户名']) and pd.notna(row['密码']):
                    current_record["user_management"].append({
                        "user": row['用户名'],
                        "passwd": row['密码'],
                        "default_db": row['默认数据库']
                    })
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_kfks(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
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
                auth = ''
                kerberos_keytab_path = ''
                kerberos_principal = ''
                kerberos_service_name = ''
                if pd.notna(row['kafka凭证']) and pd.notna('kafka服务名') and pd.notna('keytab路径'):
                    auth = 'kerberos'
                    kerberos_keytab_path = row['keytab路径']
                    kerberos_principal = row['kafka凭证']
                    kerberos_service_name = row['kafka服务名']
                db_list = [{"ip": row['IP地址'], "port": int(row['端口'])}] \
                    if pd.notna(row['IP地址']) and pd.notna(row['端口']) else []
                current_record = {
                    "config": {
                        "db_list": db_list,
                        "auth": auth,
                        "kerberos_keytab_path": kerberos_keytab_path,
                        "kerberos_principal": kerberos_principal,
                        "kerberos_service_name": kerberos_service_name,
                        "role": roles,
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
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_msq_msq_rules(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
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
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名'],
                            "dst_db": row['备端库名'],
                            "dst_table": row['备端表名']}]
                    else:
                        map_type = 'database'
                        db_map = [{
                            "src_table": row['源端库名'],
                            "dst_table": row['备端库名']
                        }]
                current_record = {
                    "db_map": db_map,
                    "full_sync": 1 if row['全量同步'] == 'yes' else 0,
                    "config": {
                        "full_sync_settings": {
                            "dump_thd": int(row['全量导出线程数']) if pd.notna(row['全量导出线程数']) else None,
                            "existing_table": row['表覆盖策略'],
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
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名'],
                            "dst_db": row['备端库名'],
                            "dst_table": row['备端表名']})
                    else:
                        current_record["db_map"].append({
                            "src_table": row['源端库名'],
                            "dst_table": row['备端库名']})
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_msq_kfk_rules(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
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
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名'],
                            "dst_db": row['备端topic'],
                            "dst_table": row['备端topic']}]
                    else:
                        map_type = 'database'
                        db_map = [{
                            "src_table": row['源端库名'],
                            "dst_table": row['备端topic']
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
                            "src_db": row['源端库名'],
                            "src_table": row['源端表名'],
                            "dst_db": row['备端topic'],
                            "dst_table": row['备端topic']})
                    else:
                        current_record["db_map"].append({
                            "src_table": row['源端库名'],
                            "dst_table": row['备端topic']})
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

    def generate_creation_json(self, t_sheet: str, obj_dict: dict):
        df = pd.read_excel(self.template, sheet_name=t_sheet, header=None)
        json_str = ''
        for _, row in df.iterrows():
            row_str = " ".join(['null' if str(cell) == 'Null' else str(cell) for cell in row if pd.notna(cell)])
            json_str += row_str + "\n"
        json_data = json.loads(json_str)
        Excel.merge_dict(json_data, obj_dict)
        key = ''
        if t_sheet in ['kfk', 'msq']:
            key = 'db_name'
        elif t_sheet in ['msq_kfk', 'msq_msq']:
            key = 'mysql_name'
        file = f"{self.output}/{obj_dict[key]}.json"
        with open(file, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"{file} generated according to {t_sheet} in {self.template}")

    def generate_csvs(self):
        excel_file = pd.ExcelFile(self.name)
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            csv_file_path = f"{self.output}/{sheet_name}.csv"
            df.to_csv(csv_file_path, index=False, header=False, encoding='utf-8')
            print(f"Sheet '{sheet_name}' saved to '{csv_file_path}'")


def main():
    excel = Excel('excel/zx-test-env_2.xlsx', None, 'output')
    excel.generate_csvs()


if __name__ == "__main__":
    main()
