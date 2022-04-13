# coding: hdytto

import unittest

class TestComment(unittest.TestCase):
    def test_comment(self):
        def foo():
            return 1
        /*def foo():
            return 0*/
        self.assertEqual(1, foo())/*
        self.assertEqual(1, 2)*/

        a = /* 100 */10 + 5/* - foo()*/
        self.assertEqual(15, a)
        def bar():
            b = 5
            /* return b
        a = 20 # ignored
        */
        self.assertEqual(15, a)

        self.assertEqual('/' + '* bar *' + '/', '/* bar */')
        self.assertEqual('/' + '* baz *' + '/', "/* baz */")

if __name__ == '__main__':
    unittest.main()
