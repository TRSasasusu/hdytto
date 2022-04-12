import tokenize
from tokenize import TokenInfo
from token import tok_name
import codecs, encodings
from io import StringIO
from encodings import utf_8
import sys

from .increment import increment
from .comment import comment
from .dowhile import dowhile
from .const import const
from .util import Token, isrepl, syntax_error_util

UTF8 = encodings.search_function('utf8')

def recalculate_3tuples(a):
    l = []
    indent_num = 0
    indent_stack = []
    row = 1
    for type, name in a:
        l.append(Token(type, name))
        #print(l)
        if l[-1].type == tokenize.INDENT:
            indent_num += 1
            indent_stack.append(l[-1].name)
        elif l[-1].type == tokenize.DEDENT:
            if indent_num > 0:
                indent_num -= 1
                indent_stack.pop(-1)
        elif l[-1].type == tokenize.NEWLINE or l[-1].type == tokenize.NL or l[-1].type == tokenize.ENDMARKER:
            physical_line = ' '.join([n for _, n in l])
            if l[0].type != tokenize.INDENT and len(indent_stack) > 0:
                col = len(indent_stack[-1])
                physical_line = indent_stack[-1] + physical_line
            else:
                col = 0
            for t, n in l:
                yield t, n, (row, col), (row, (col := col + len(n))), physical_line
                if t != tokenize.INDENT and t != tokenize.DEDENT:
                    col += 1
            l = []
            row += 1


def check_a(a):
    for t, n, x, y, z in a:
        print(f'{t}{n} ({x},{y},{z})', end='')
        yield t, n, x, y, z

def transform(stream):
    #print("call transform")
    syntax_error_util.find_filepath(stream)
    sys.tracebacklimit = None

    stream = comment(stream)

    a = tokenize.generate_tokens(StringIO(stream).readline)

    a = increment(a)
    a = const(a)
    a = dowhile(a)
    a = recalculate_3tuples(a)
    #a = check_a(a)

    #a = list(tokenize.untokenize(a))
    #print(''.join(a))
    #return iter(a)

    return tokenize.untokenize(a)

def decode(input, errors='strict'):
    #print('call decode')
    if isinstance(input, memoryview):
        input = input.tobytes().decode('utf-8')
    input = transform(input)
    return input, len(input)

class IncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        #print('decode in incrementaldecoder')
        return transform(super().decode(input, final))

class StreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = StringIO(transform(self.stream))

def search_function(s):
    #print('call search_function')
    if s != 'hdytto':
        return None

    #print('hdytto is used')
    return codecs.CodecInfo(
        name='hdytto',
        encode=UTF8.encode,
        decode=decode,
        incrementalencoder=UTF8.incrementalencoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=UTF8.streamwriter)

def register_hdytto():
    codecs.register(search_function)
