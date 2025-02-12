import json
import unittest
from pprint import pprint

import pandas as pd

from json_tool import json_to_df, df_to_json, df_to_excel, excel_to_df, json_to_excel, excel_to_json, merge_json, \
    sort_json, process_uuid


class JsonTestCase(unittest.TestCase):
    """
    +-----------------------------------------------------------+
    |  |      0       |    1       |     2          |     3     |
    +-----------------------------------------------------------+
    |0 |name         ｜"John Doe"  |                |           |
    |1 |age          ｜30          |                |           |
    |2 |is_employee  ｜True        |                |           |
    |3 |address      ｜street      |"123 Main St"   |           |
    |4 |             ｜city        |"Anytown"       |           |
    |5 |             ｜postal_code |"12345"         |           |
    |6 |phone_numbers｜[0]         |type            |"home"     |
    |7 |             ｜            |number          |"555-1234" |
    |8 |             ｜[1]         |type            |"work"     |
    |9 |             ｜            |number          |"555-5678" |
    |10|skills       ｜[0]         |"Python"        |           |
    |11|             ｜[1]         |"Excel"         |           |
    |12|             ｜[2]         |"Data Analysis" |           |
    +-----------------------------------------------------------+
    """
    json_data = {
        "name": "John Doe",
        "age": 30,
        "is_employee": True,
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "postal_code": "12345"
        },
        "phone_numbers": [
            {
                "type": "home",
                "number": "555-1234"
            },
            {
                "type": "work",
                "number": "555-5678"
            }
        ],
        "skills": ["Python", "Excel", "Data Analysis"]
    }

    df_data = [
        ['{', None, None, None, None],
        ['"name":', '"John Doe"', ',', None, None],
        ['"age":', '30', ',', None, None],
        ['"is_employee":', 'true', ',', None, None],
        ['"address":', '{', None, None, None],
        [None, '"street":', '"123 Main St"', ',', None],
        [None, '"city":', '"Anytown"', ',', None],
        [None, '"postal_code":', '"12345"', None, None],
        [None, '}', ',', None, None],
        ['"phone_numbers":', '[', None, None, None],
        [None, '{', None, None, None],
        [None, '"type":', '"home"', ',', None],
        [None, '"number":', '"555-1234"', None, None],
        [None, '}', ',', None, None],
        [None, '{', None, None, None],
        [None, '"type":', '"work"', ',', None],
        [None, '"number":', '"555-5678"', None, None],
        [None, '}', None, None, None],
        [None, ']', ',', None, None],
        ['"skills":', '[', None, None, None],
        [None, '"Python"', ',', None, None],
        [None, '"Excel"', ',', None, None],
        [None, '"Data Analysis"', None, None, None],
        [None, ']', None, None, None],
        ['}', None, None, None, None]
    ]

    @staticmethod
    def traverse_print(data: dict, indent=0):
        if isinstance(data, dict):
            for key, value in data.items():
                print(' ' * indent + str(key) + ":")
                JsonTestCase.traverse_print(value, indent + 4)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                print(' ' * indent + f"[{index}]:")
                JsonTestCase.traverse_print(item, indent + 4)
        else:
            print(' ' * indent + str(data))

    def test_traverse_print(self):
        print("Test traverse print")
        JsonTestCase.traverse_print(self.json_data)

    @staticmethod
    def traverse_count(data: dict, count=0, x=0, max_x=0) -> (int, int):
        if isinstance(data, dict):
            for key, value in data.items():
                max_x = max(max_x, x + 1)
                count, max_x = JsonTestCase.traverse_count(value, count, x + 1, max_x)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                max_x = max(max_x, x + 1)
                count, max_x = JsonTestCase.traverse_count(item, count, x + 1, max_x)
        else:
            count += 1
        return count, max_x

    def test_traverse_count(self):
        print("Test traverse count")
        print(JsonTestCase.traverse_count(self.json_data))

    def test_json_to_df(self):
        print("Test to json to df")
        print(json_to_df(self.json_data))

    def test_df_to_json(self):
        print("Test to df to json")
        pprint(df_to_json(pd.DataFrame(self.df_data)))

    def test_compare(self):
        print("Test to compare")
        data = df_to_json(pd.DataFrame(self.df_data))
        self.assertEqual(self.json_data, data)
        df = json_to_df(self.json_data)
        self.assertEqual(self.json_data, df_to_json(df))

    def test_df_to_excel(self):
        print("Test to df to excel")
        df_to_excel(pd.DataFrame(self.df_data), 'test_json.xlsx', 'john_doe', True)

    def test_excel_to_df(self):
        print("Test to excel to df")
        print(excel_to_df('test_json.xlsx', 'john_doe'))

    def test_json_to_excel(self):
        print("Test to json_file to excel")
        json_to_excel('json/hb_ht_h2_sort.json', 'excel/test_json.xlsx', 'hb_ht_h2')

    def test_excel_to_json(self):
        print("Test to excel to json_file")
        # excel_to_json('test_json.xlsx', 'john_doe', 'john_doe.json')
        excel_to_json('excel/test_json.xlsx', 'msq_u_kfk_auto', 'tmp/msq_u_kfk_auto.json')

    def test_merge_json(self):
        print("Test to merge json")
        # merge_json('json/msqdb_tpl.json', 'json/msq_u.json', 'tmp/msq_u_all.json')
        merge_json('json/msq_kfk_tpl.json', 'json/msq_u_kfk.json', 'tmp/msq_u_kfk_all.json')

    def test_sort_json(self):
        print("Test to sort json")
        sort_json('json/hb_ht_h2.json', 'json/hb_ht_h2_sort.json')

    def test_process_uuid(self):
        print("Test to process uuid")
        json_data = {
            "id": "12345678-1234-1234-1234-1234567890ab",
            "name": "Example",
            "items": [
                "abcdef12-1234-1234-1234-abcdef123456",
                "not-a-uuid"
            ],
            "nested": {
                "uuid": "87654321-4321-4321-4321-abcdef123456",
                "list": [
                    "12345678-1234-1234-1234-1234567890ab",
                    "another-uuid"
                ]
            }
        }

        json_data = process_uuid(json_data)
        print(json.dumps(json_data, indent=4))

    def test_process_uuid2(self):
        json_file = 'rules/test显示_bak.json'
        json_file2 = 'rules/test显示_bak2.json'
        with open(json_file, 'r') as f:
            json_data = process_uuid(json.load(f))
        with open(json_file2, 'w') as f:
            json.dump(json_data, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    unittest.main()
