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
                # if pd.notna(row['cred_name']) and row['cred_name'].strip() != "":
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


def main():
    excel_file = 'excel/i2up_data.xlsx'
    excel = Excel(excel_file)
    excel.get_nodes('workNode')


if __name__ == "__main__":
    main()
