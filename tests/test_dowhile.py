# coding: hdytto

import unittest

class TestDowhile(unittest.TestCase):
    def test_dowhile(self):
        a = 5
        do:
            a += 5
            while a < 3

        self.assertEqual(10, a)

        do:
            b = -5
            while a < 25:
                a += 10
            while b != -5

        self.assertEqual(30, a)
        self.assertEqual(-5, b)

        do:
            b *= 2
            do:
                a += b
                c = a * 2
                while c > 20
            b += c
            while b < 0

        self.assertEqual(10, a)
        self.assertEqual(10, b)
        self.assertEqual(20, c)

if __name__ == '__main__':
    unittest.main()
