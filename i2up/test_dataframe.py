import unittest

import pandas as pd


class DataFrameTestCase(unittest.TestCase):
    data = [
        ["name", "John Doe", None, None],
        ["age", 30, None, None],
        ["is_employee", True, None, None],
        ["address", "street", "123 Main St", None],
        ["", "city", "Anytown", None],
        ["", "postal_code", "12345", None],
        ["phone_numbers", "[0]", "type", "home"],
        ["", "", "number", "555-1234"],
        ["", "[1]", "type", "work"],
        ["", "", "number", "555-5678"],
        ["skills", "[0]", "Python", None],
        ["", "[1]", "Excel", None],
        ["", "[2]", "Data Analysis", None]
    ]

    @classmethod
    def setUpClass(cls):
        cls.max_rows = 5
        cls.max_cols = 5
        cls.df = pd.DataFrame(index=range(cls.max_rows), columns=range(cls.max_cols))
        columns = [0, 1, 2, 3]
        cls.df2 = pd.DataFrame(DataFrameTestCase.data, columns=columns)

    def save(self, string: str, x: int, y: int):
        if 0 <= x < self.max_cols and 0 <= y < self.max_rows:
            self.df.iat[y, x] = string
            print("save %s at(%d,%d)" % (string, y, x))
        else:
            print("Error: Index out of bounds")

    def test_save(self):
        self.save("哈罗", 1, 1)
        self.save("World", 2, 1)
        self.save("Pandas", 0, 0)
        self.save("Error", 10, 10)
        print(self.df)
        # self.df.to_excel("df.xlsx", index=False)

    @staticmethod
    def get_indent_level(row):
        for i, val in enumerate(row):
            if pd.notna(val) and val != '':
                return i
        return len(row)

    def test_indent(self):
        for _, row in self.df2.iterrows():
            print("indent(%d)" % DataFrameTestCase.get_indent_level(row))


if __name__ == '__main__':
    unittest.main()
