import tokenize

from .util import Token

def comment(a):
    l = []
    in_comment = False
    for type, name in a:
        l.append(Token(type, name))
        if not in_comment:
            if l[0].name == '/':
                if len(l) == 1:
                    continue
                if l[1].name == '*':
                    in_comment = True
                    l = []
                    continue
                else:
                    yield l.pop(0)
            else:
                yield l.pop(0)
        else:
            if l[0].name == '*':
                if len(l) == 1:
                    continue
                if l[1].name == '/':
                    in_comment = False
                    l = []
                    continue
                else:
                    l.pop(0)
            else:
                l.pop(0)
    for t, n in l:
        yield t, n
    l = []
