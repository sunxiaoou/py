import unittest
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
    def traverse_print(data, indent=0):
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
        JsonTestCase.traverse_print(self.json_data)

    def test_traverse_save(self):
        df = traverse_save(self.json_data, 0, 0, pd.DataFrame(index=range(5), columns=range(5)))
        print(df)
        # df.to_excel("output.xlsx", index=False, header=False)


if __name__ == '__main__':
    unittest.main()
