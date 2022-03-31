import tokenize
from token import tok_name

from .util import Token


def increment(a):
    l = []
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
