import tokenize
from token import tok_name

from .util import Token


def dowhile(a):
    stack = []
    l = []

    checking_while_start_index = None
    while_condition_tokens = []

    for type, name in a:
        #print(tok_name[type], name)
        l.append(Token(type, name))
        #print(l)
        #print(stack)
        if checking_while_start_index is not None:
            if l[-1].name == ':':
                checking_while_start_index = None
            elif l[-1].name == '\n':
                dowhile_condition_tokens = [Token(tokenize.NAME, 'if'), Token(tokenize.NAME, f'_HDYTTO_DOWHILE_COUNTER_{len(stack)}'), Token(tokenize.NAME, 'and'), Token(tokenize.NAME, 'not'), Token(tokenize.OP, '(')] + l[checking_while_start_index + 1:-1] + [Token(tokenize.OP, ')'), Token(tokenize.OP, ':'), Token(tokenize.NEWLINE, '\n'), Token(tokenize.INDENT, l[8].name + '    '), Token(tokenize.NAME, 'break'), Token(tokenize.NEWLINE, '\n'), Token(tokenize.DEDENT, ''), Token(tokenize.NAME, f'_HDYTTO_DOWHILE_COUNTER_{len(stack)}'), Token(tokenize.VBAREQUAL, '|='), Token(tokenize.NAME, 'True'), Token(tokenize.NEWLINE, '\n')]
                for i, token in enumerate(dowhile_condition_tokens):
                    l.insert(9 + i, token)
                while len(l) > checking_while_start_index + len(dowhile_condition_tokens):
                    del l[checking_while_start_index + len(dowhile_condition_tokens)]
                checking_while_start_index = None
                if len(stack) > 1:
                    stack[-2].extend(stack.pop(-1))
                    l = stack[-1]
                else:
                    print('######')
                    print(l)
                    print('######')
                    for t, n in l:
                        yield t, n
                    l = []
                    stack = []

        if len(l) <= 1:
            continue
        if l[-2].name == 'do' and l[-1].name == ':':
            l.pop(-1)
            l.pop(-1)
            l = []
            stack.append(l)
            l.append(Token(tokenize.NAME, f'_HDYTTO_DOWHILE_COUNTER_{len(stack)}'))
            l.append(Token(tokenize.OP, '='))
            l.append(Token(tokenize.NAME, 'False'))
            l.append(Token(tokenize.NEWLINE, '\n'))
            l.append(Token(tokenize.NAME, 'while'))
            l.append(Token(tokenize.NAME, 'True'))
            l.append(Token(tokenize.OP, ':'))
            continue
        if len(stack) == 0:
            yield l.pop(0)
            continue
        if l[-1].name == 'while':
            checking_while_start_index = len(l) - 1
            continue
    for t, n in l:
        yield t, n
    l = []
