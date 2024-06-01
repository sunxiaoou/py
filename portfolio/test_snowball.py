import unittest

from snowball import Snowball


class TestSnowball(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.snowball = Snowball()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_last_close(self):
        print(self.snowball.last_close('SZ127007'))

    def test_my_cvt_bones(self):
        print(self.snowball.my_cvt_bones())


if __name__ == '__main__':
    unittest.main()
