# coding: hdytto

import unittest

class TestDowhile(unittest.TestCase):
    def test_dowhile(self):
        a = 5
        print(a)
        do:
            a += 5
            while a < 3

        self.assertEqual(10, a)

if __name__ == '__main__':
    unittest.main()
