import unittest
from main import *

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")


if __name__ == "__main__":
    unittest.main()


    