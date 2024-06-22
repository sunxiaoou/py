import unittest


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

    # def test_traverse_print(self):
    #     JsonTestCase.traverse_print(self.json_data)

    @staticmethod
    def save(string: str, x: int, y: int):
        print("save %s at(%d,%d)" % (string, y, x))

    @staticmethod
    def traverse_save(data, x=1, y=1):
        if isinstance(data, dict):
            for key, value in data.items():
                JsonTestCase.save(key, x, y)
                JsonTestCase.traverse_save(value, x + 1, y)
                if isinstance(value, dict):
                    y += len(value)
                elif isinstance(value, list):
                    y += len(value[0]) * len(value)
                else:
                    y += 1
        elif isinstance(data, list):
            JsonTestCase.save("set", x, y)
            for index, item in enumerate(data):
                JsonTestCase.traverse_save(item, x + 1, y)
                if isinstance(item, dict):
                    y += len(item)
                else:
                    y += 1
        else:
            JsonTestCase.save(str(data), x, y)

    def test_traverse_save(self):
        JsonTestCase.traverse_save(self.json_data)


if __name__ == '__main__':
    unittest.main()
