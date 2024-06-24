import json
import unittest
from pprint import pprint

import pandas as pd

from json_excel import traverse_save


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

    def test_traverse_save(self):
        print("Test traverse save")
        count, df = traverse_save(self.json_data, 0, 0, pd.DataFrame(index=range(5), columns=range(5)))
        print("count(%d)" % count)
        print(df)
        # df.to_excel("output.xlsx", index=False, header=False)

    def test_restore_json(self):
        print("Test restore json")
        _, df = traverse_save(self.json_data, 0, 0, pd.DataFrame(index=range(5), columns=range(5)), True)
        json_string = ''
        for _, row in df.iterrows():
            row_string = " ".join([str(cell) for cell in row if pd.notna(cell)])
            json_string += row_string + "\n"
        print(json_string)
        pprint(json.loads(json_string))


if __name__ == '__main__':
    unittest.main()
