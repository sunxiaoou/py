#! /usr/bin/python3
import pandas as pd


class Excel:
    def __init__(self, name: str):
        self.name = name

    def get_nodes(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
        df.columns = ['NO', 'node_name', 'address', 'data_port', 'cache_dir', 'log_dir', 'password', 'node_type']
        df['node_type'] = df['node_type'].apply(lambda x: f"{1 if 'src' in x else 0}{1 if 'tgt' in x else 0}00")
        df = df.drop(columns=['NO'])
        return df.to_dict(orient='records')

    def get_dbs(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
        df.columns = ["NO", "db_name", "node_name", "db_type", "role", "ip", "port", "cred_name", "user", "passwd",
                      "default_db"]
        data_list = []
        current_record = None
        for _, row in df.iterrows():
            if pd.notna(row['NO']):
                if current_record is not None:
                    data_list.append(current_record)
                roles = row['role'].split('|') if pd.notna(row['role']) else []
                db_list = [{"ip": row['ip'], "port": int(row['port'])}] \
                    if pd.notna(row['ip']) and pd.notna(row['port']) else []
                user_management = []
                if pd.notna(row['cred_name']):
                    user_management.append({
                        "cred_name": row['cred_name'],
                        "default_db": row['default_db']
                    })
                elif pd.notna(row['user']) and pd.notna(row['passwd']):
                    user_management.append({
                        "user": row['user'],
                        "passwd": row['passwd'],
                        "default_db": row['default_db']
                    })
                current_record = {
                    "db_list": db_list,
                    "role": roles,
                    "user_management": user_management,
                    "db_name": row['db_name'],
                    "db_type": row['db_type'],
                    "node_uuid": row['node_name']
                }
            else:
                if pd.notna(row['ip']) and pd.notna(row['port']):
                    current_record["db_list"].append({
                        "ip": row['ip'],
                        "port": int(row['port'])
                    })
                if pd.notna(row['cred_name']) and row['cred_name'].strip() != "":
                    current_record["user_management"].append({
                        "cred_name": row['cred_name'],
                        "default_db": row['default_db']
                    })
                elif pd.notna(row['user']) and pd.notna(row['passwd']):
                    current_record["user_management"].append({
                        "user": row['user'],
                        "passwd": row['passwd'],
                        "default_db": row['default_db']
                    })
        if current_record is not None:
            data_list.append(current_record)
        return data_list

    def get_mysql_rules(self, sheet: str) -> list:
        df = pd.read_excel(self.name, sheet_name=sheet)
        df.columns = ["NO", "mysql_name", "src_db_name", "tgt_db_name", "src_db", "dst_db", "src_table", "dst_table",
                      "full_sync", "dump_thd", "load_thd", "existing_table", "full_sync_custom_cfg",
                      "incre_sync", "dyn_thread", "incre_full_sync_custom_cfg"]
        data_list = []
        current_record = None
        for _, row in df.iterrows():
            if pd.notna(row['NO']):
                if current_record is not None:
                    data_list.append(current_record)
                full_sync_custom_cfg = [row['full_sync_custom_cfg']] if pd.notna(row['full_sync_custom_cfg']) else []
                incre_full_sync_custom_cfg = [row['incre_full_sync_custom_cfg']] \
                    if pd.notna(row['incre_full_sync_custom_cfg']) else []
                tab_map = [{
                    "src_db": row['src_db'],
                    "src_table": row['src_table'],
                    "dst_db": row['dst_db'],
                    "dst_table": row['dst_table']}] \
                    if pd.notna(row['src_db']) and pd.notna(row['src_table']) else []
                current_record = {
                    "full_sync": 1 if row['full_sync'] == 'yes' else 0,
                    "full_sync_settings": {
                        "dump_thd": int(row['dump_thd']) if pd.notna(row['dump_thd']) else None,
                        "existing_table": row['existing_table'],
                        "full_sync_custom_cfg": full_sync_custom_cfg
                    },
                    "incre_sync": 1 if row['incre_sync'] == 'yes' else 0,
                    "mysql_name": row['mysql_name'],
                    "other_settings": {
                        "dyn_thread": int(row['dyn_thread']) if pd.notna(row['dyn_thread']) else None,
                        "incre_full_sync_custom_cfg": incre_full_sync_custom_cfg
                    },
                    "src_db_name": row['src_db_name'],
                    "tab_map": tab_map,
                    "tgt_db_name": row['tgt_db_name']
                }
            else:
                if pd.notna(row['full_sync_custom_cfg']):
                    current_record["full_sync_settings"]["full_sync_custom_cfg"].append(row['full_sync_custom_cfg'])
                if pd.notna(row['incre_full_sync_custom_cfg']):
                    current_record["other_settings"]["incre_full_sync_custom_cfg"].\
                        append(row['incre_full_sync_custom_cfg'])
                if pd.notna(row['src_db']) and pd.notna(row['src_table']):
                    current_record["tab_map"].append({
                        "src_db": row['src_db'],
                        "src_table": row['src_table'],
                        "dst_db": row['dst_db'],
                        "dst_table": row['dst_table']})
        if current_record is not None:
            data_list.append(current_record)
        return data_list


def main():
    excel_file = 'excel/i2up_data.xlsx'
    excel = Excel(excel_file)
    excel.get_nodes('workNode')


if __name__ == "__main__":
    main()
