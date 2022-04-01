import tokenize
from tokenize import TokenInfo
from token import tok_name
import codecs, encodings
from io import StringIO
from encodings import utf_8

from .increment import increment
from .comment import comment

UTF8 = encodings.search_function('utf8')

def transform(stream):
    #print("call transform")

    stream = comment(stream)

    a = tokenize.generate_tokens(StringIO(stream).readline)

    a = increment(a)

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
