import tokenize
from tokenize import TokenInfo
from token import tok_name
import codecs, encodings
from io import StringIO
from encodings import utf_8
from typing import NamedTuple

UTF8 = encodings.search_function('utf8')

class Token(NamedTuple):
    type: int
    name: str

def inject(a):
    l = []
    var = None
    one_plus = False
    for type, name, _, _, _ in a:
        #print(tok_name[type], name)
        l.append(Token(type, name))
        #print(l)
        if l[0].type == tokenize.NAME:
            if len(l) > 1:
                if l[1].name != '+' and l[1].name != '-':
                    for t, n in l:
                        yield t, n
                    l = []
                    continue
            if len(l) < 3:
                continue
            if l[1].name == '+' and l[2].name == '+':
                yield tokenize.OP, '('
                yield tokenize.OP, '('
                yield tokenize.NAME, l[0].name
                yield tokenize.OP, ':='
                yield tokenize.NAME, l[0].name
                yield tokenize.OP, '+'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                yield tokenize.OP, '-'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                l = []
                continue
            if l[1].name == '-' and l[2].name == '-':
                yield tokenize.OP, '('
                yield tokenize.OP, '('
                yield tokenize.NAME, l[0].name
                yield tokenize.OP, ':='
                yield tokenize.NAME, l[0].name
                yield tokenize.OP, '-'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                yield tokenize.OP, '+'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                l = []
                continue
            for t, n in l:
                yield t, n
            l = []
            continue
        elif l[0].name == '+':
            if len(l) > 1:
                if l[1].name != '+' and l[1].name != '-':
                    for t, n in l:
                        yield t, n
                    l = []
                    continue
            if len(l) < 3:
                continue
            if l[1].name == '+' and l[2].type == tokenize.NAME:
                yield tokenize.OP, '('
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, ':='
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, '+'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                l = []
                continue
            for t, n in l:
                yield t, n
            l = []
            continue
        elif l[0].name == '-':
            if len(l) > 1:
                if l[1].name != '+' and l[1].name != '-':
                    for t, n in l:
                        yield t, n
                    l = []
                    continue
            if len(l) < 3:
                continue
            if l[1].name == '-' and l[2].type == tokenize.NAME:
                yield tokenize.OP, '('
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, ':='
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, '-'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                l = []
                continue
            for t, n in l:
                yield t, n
            l = []
            continue

        for t, n in l:
            yield t, n
        l = []

    for t, n in l:
        yield t, n
    l = []

def transform(stream):
    #print("call transform")
    a = tokenize.generate_tokens(StringIO(stream).readline)
    return tokenize.untokenize(inject(a))

def decode(input, errors='strict'):
    #print('call decode')
    if isinstance(input, memoryview):
        input = input.tobytes().decode('utf-8')
    #return UTF8.decode(transform(StringIO(input)), errors)
    input = transform(input)
    return input, len(input)
    return UTF8.decode(transform(input), errors)

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

codecs.register(search_function)
