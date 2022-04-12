# coding: hdytto

import unittest
import subprocess

class TestConst(unittest.TestCase):
    def test_const(self):
        sp = subprocess.run(['python', 'tests/test_const/a.py'], encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertIn('hdytto/tests/test_const/a.py', sp.stderr)
        self.assertIn('line 4', sp.stderr)
        self.assertIn('a = 10', sp.stderr)
        self.assertIn('SyntaxError: invalid assignment to const a', sp.stderr)

        sp = subprocess.run(['python', 'tests/test_const/b.py'], encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual('10\n', sp.stdout)

        sp = subprocess.run(['python', 'tests/test_const/c.py'], encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertIn('hdytto/tests/test_const/c.py', sp.stderr)
        self.assertIn('line 4', sp.stderr)
        self.assertIn('b += 20', sp.stderr)
        self.assertIn('SyntaxError: invalid assignment to const b', sp.stderr)

        sp = subprocess.run(['python', 'tests/test_const/d.py'], encoding='utf8', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertIn('hdytto/tests/test_const/d.py', sp.stderr)
        self.assertIn('line 2', sp.stderr)
        self.assertIn('const a', sp.stderr)
        self.assertIn('SyntaxError: missing = in const declaration', sp.stderr)

        const a = 5
        self.assertEqual(5, a)

if __name__ == '__main__':
    unittest.main()
