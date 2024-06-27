import unittest
from pprint import pprint

import pandas as pd

from json_tool import json_to_df, df_to_json, df_to_excel, excel_to_df, json_to_excel, excel_to_json


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
    def traverse_count(data: dict, count=0) -> int:
        if isinstance(data, dict):
            for key, value in data.items():
                count = JsonTestCase.traverse_count(value, count)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                count = JsonTestCase.traverse_count(item, count)
        else:
            count += 1
        return count

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
        json_to_excel('msq_c2.json', 'test_json.xlsx', 'msq_c2')

    def test_excel_to_json(self):
        print("Test to excel to json_file")
        excel_to_json('test_json.xlsx', 'john_doe', 'john_doe.json')


if __name__ == '__main__':
    unittest.main()
