import tokenize
from token import tok_name
from keyword import iskeyword
import traceback
import sys
import inspect

from .util import Token, syntax_error_util


def const(a):
    const_vars = []

    lineno = 1
    l = []
    for type, name in a:
        #print(tok_name[type], name)
        l.append(Token(type, name))
        print(l)
        if l[0].name == 'const':
            if len(l) == 1:
                continue
            if l[1].type != tokenize.NAME:
                yield l.pop(0)
                continue
            if len(l) == 2:
                continue
            if l[2].name != '=':
                syntax_error_util.raise_error('missing = in const declaration', lineno=lineno, offset=len(l[0].name) + 1 + len(l[1].name), line=l[0].name + ' ' + l[1].name)
            if l[-1].name != '\n' and l[-1].type != tokenize.ENDMARKER:
                continue
            if l[1].name in const_vars:
                syntax_error_util.raise_error(f'redeclaration of const {l[1].name}', lineno=lineno, offset=sum([len(each_l.name) for each_l in l[:-1]]) + len(l) - 2, line=' '.join([each_l.name for each_l in l[:-1]]))
            lineno += 1
            const_vars.append(l[1].name)
            print(const_vars)
            l.pop(0) # remove const
            while len(l) > 0:
                yield l.pop(0)
            continue
        if l[0].type == tokenize.NAME:
            if l[0].name not in const_vars:
                yield l.pop(0)
                continue
            if len(l) == 1:
                continue
            if l[1].name != '=':
                yield l.pop(0)
                continue
            if l[-1].name != '\n' and l[-1].type != tokenize.ENDMARKER:
                continue
            syntax_error_util.raise_error(f'invalid assignment to const {l[0].name}', lineno=lineno, offset=sum([len(each_l.name) for each_l in l[:-1]]) + len(l) - 2, line=' '.join([each_l.name for each_l in l[:-1]]))

        if l[0].name == '\n':
            lineno += 1
        yield l.pop(0)

    for t, n in l:
        yield t, n
    l = []
