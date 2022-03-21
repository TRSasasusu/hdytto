import tokenize
from tokenize import TokenInfo
from token import tok_name
import codecs, encodings
from io import StringIO
from encodings import utf_8

UTF8 = encodings.search_function('utf8')

print('hoge')

def inject(a):
    var = None
    one_plus = False
    for type, name, _, _, _ in a:
        print(tok_name[type],name)
        if var is not None:
            print('foo')
            if name != '+':
                yield tokenize.NAME, var
                if one_plus:
                    yield tokenize.OP, '+'
                yield type, name
                var = None
                one_plus = False
                continue
            if not one_plus:
                one_plus = True
                continue
            print('var++ found')
            yield tokenize.OP, '('
            yield tokenize.OP, '('
            yield tokenize.NAME, var
            yield tokenize.OP, ':='
            yield tokenize.NAME, var
            yield tokenize.OP, '+'
            yield tokenize.NUMBER, '1'
            print('hmm')
            yield tokenize.OP, ')'
            yield tokenize.OP, '-'
            yield tokenize.NUMBER, '1'
            yield tokenize.OP, ')'
            var = None
            one_plus = False
            continue
        if type == tokenize.NAME:
            var = name
            continue
        yield type, name
        if name == '+':
            one_plus = True
            yield type, name
            if type == tokenize.OP and name == '+':
                yield
    if var is not None:
        yield tokenize.NAME, var

def transform(stream):
    print("call transform")
    #import pdb; pdb.set_trace()
    #a = tokenize.tokenize(lambda: (StringIO(stream).readline()).encode('utf8'))
    a = tokenize.generate_tokens(StringIO(stream).readline)
    return tokenize.untokenize(inject(a))

def decode(input, errors='strict'):
    print('hogehoge')
    if isinstance(input, memoryview):
        input = input.tobytes().decode('utf-8')
    return UTF8.decode(transform(StringIO(input)), errors)

class IncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        print('decode in incrementaldecoder')
        #import pdb; pdb.set_trace()
        return transform(super().decode(input, final))
        #self.buffer += input
        #if final:
        #    buff = self.buffer
        #    self.buffer = ''
        #    print('final decode in incrementaldecoder')
        #    return super().decode(transform(StringIO(buff)), final=True)

class StreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = StringIO(transform(self.stream))

def search_function(s):
    print(s)
    if s != 'hdytto':
        return None

    print("piyo")
    return codecs.CodecInfo(
        name='hdytto',
        encode=UTF8.encode,
        decode=decode,
        incrementalencoder=UTF8.incrementalencoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=UTF8.streamwriter)

codecs.register(search_function)

"""
def translate(readline):
    print('translate')
    var = None
    one_plus = False
    for type, name, _, _, _ in tokenize.generate_tokens(readline):
        print(type,name)
        if var is not None:
            print('foo')
            if name != '+':
                yield tokenize.NAME, var
                var = None
                one_plus = False
                continue
            if not one_plus:
                one_plus = True
                continue
            yield tokenize.OP, '('
            yield tokenize.OP, '('
            yield tokenize.NAME, var
            yield tokenize.OP, ':='
            yield tokenize.NAME, var
            yield tokenize.OP, '+'
            yield tokenize.NUMBER, 1
            yield tokenize.OP, ')'
            yield tokenize.OP, '-'
            yield tokenize.NUMBER, 1
            yield tokenize.OP, ')'
            var = None
            one_plus = False
            continue
        if type == tokenize.NAME:
            var = name
            continue
        yield type, name
        if name == '+':
            one_plus = True
            yield type, name
            if type == tokenize.OP and name == '+':
                yield
    if var is not None:
        yield tokenize.NAME, var

class StreamReader(utf_8.StreamReader):
    #def __init__(self, *args, **kwargs):
    def __init__(self, stream, errors='strict'):
        print('__init__ of StreamReader')
        #codecs.StreamReader.__init__(self, *args, **kwargs)
        codecs.StreamReader.__init__(self, stream, errors)
        data = tokenize.untokenize(translate(self.stream.readline))
        self.stream = io.StringIO(data)

class StreamWriter(utf_8.StreamWriter):
    def __init__(self, *args, **kwargs):
        print('__init__ of StreamWriter')
        codecs.StreamWriter.__init__(self, *args, **kwargs)

def search_function(s):
    print(s)
    if s != 'hdytto':
        return None

    print("piyo")
    utf8 = encodings.search_function('utf8')
    print("prev return")
    import pdb; pdb.set_trace()
    return codecs.CodecInfo(
        name='hdytto',
        encode=utf8.encode,
        decode=utf8.decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=utf8.incrementaldecoder,
        streamreader=StreamReader,
        streamwriter=utf8.streamwriter)

codecs.register(search_function)
"""
