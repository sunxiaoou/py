import unittest
from pprint import pprint

import pandas as pd

from json_tool import json_to_df, df_to_json


class JsonTestCase(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
