from typing import NamedTuple
import traceback
import sys
import os
import re

class Token(NamedTuple):
    type: int
    name: str


def isrepl():
    return hasattr(sys, 'ps1')


class SyntaxErrorUtil:
    def raise_error(self, msg, lineno, offset, line):
        try:
            raise SyntaxError(msg, (self.filepath, lineno, offset, line))
        except:
            err = sys.exc_info()
        print(''.join(traceback.format_exception(*err)[2:]), file=sys.stderr)

        if isrepl():
            sys.tracebacklimit = -1
            raise Exception
        sys.exit(2) # 2 means SyntaxError in Unix.

    def find_filepath(self, file_content):
        if isrepl():
            self.filepath = '<stdin>'
            return

        if not self._find_filepath(sys.argv[0], file_content):
            self.filepath = '<some script>'

    def _find_filepath(self, filename, file_content):
        if not os.path.exists(filename):
            return False

        with open(filename, 'r') as f:
            f_content = f.read()
            f_content = '\n' + '\n'.join(f_content.split('\n')[1:])
            if f_content == file_content:
                self.filepath = os.path.abspath(filename)
                return True
            for line in sum([tmp_line.split(';') for tmp_line in f_content.split('\n')], []):
                froms = re.findall(r'from (\w+)', line)
                imports = re.findall(r'^\s*import ([\w,\s]+)', line)
                imports = sum([each_import.replace(' ', '').split(',') for each_import in imports], [])
                modules = froms + imports
                for module in modules:
                    if self._find_filepath(module, file_content):
                        return True
syntax_error_util = SyntaxErrorUtil()
