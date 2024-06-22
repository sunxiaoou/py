import unittest

import pandas as pd


class DataFrameTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.max_rows = 5
        cls.max_cols = 5
        cls.df = pd.DataFrame(index=range(cls.max_rows), columns=range(cls.max_cols))

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
        self.df.to_excel("df.xlsx", index=False)


if __name__ == '__main__':
    unittest.main()
