import tokenize
from token import tok_name
from keyword import iskeyword

from .util import Token


def increment(a):
    l = []
    for type, name, _, _, _ in a:
        #print(tok_name[type], name)
        l.append(Token(type, name))
        #print(l)
        if l[0].type == tokenize.NAME and not iskeyword(l[0].name):
            if len(l) > 1:
                if l[1].name != '+' and l[1].name != '-':
                    yield l.pop(0)
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
            yield l.pop(0)
            continue
        elif l[0].name == '+':
            if len(l) > 1:
                if l[1].name != '+' and l[1].name != '-':
                    yield l.pop(0)
                    continue
            if len(l) < 3:
                continue
            if l[1].name == '+' and l[2].type == tokenize.NAME and not iskeyword(l[2].name):
                yield tokenize.OP, '('
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, ':='
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, '+'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                l = []
                continue
            yield l.pop(0)
            continue
        elif l[0].name == '-':
            if len(l) > 1:
                if l[1].name != '+' and l[1].name != '-':
                    yield l.pop(0)
                    continue
            if len(l) < 3:
                continue
            if l[1].name == '-' and l[2].type == tokenize.NAME and not iskeyword(l[2].name):
                yield tokenize.OP, '('
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, ':='
                yield tokenize.NAME, l[2].name
                yield tokenize.OP, '-'
                yield tokenize.NUMBER, '1'
                yield tokenize.OP, ')'
                l = []
                continue
            yield l.pop(0)
            continue

        yield l.pop(0)

    for t, n in l:
        yield t, n
    l = []
