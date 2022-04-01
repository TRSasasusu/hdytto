# coding: hdytto

import unittest

class TestIncrement(unittest.TestCase):
    def test_increment(self):
        a = 5
        self.assertEqual(5, a++)
        self.assertEqual(6, a)
        b = 3 + ++a
        self.assertEqual(10, b)
        self.assertEqual(9, b-- - 1)
        self.assertEqual(8, --b)

if __name__ == '__main__':
    unittest.main()
