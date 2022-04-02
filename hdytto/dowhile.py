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
        print(l)
        print(stack)
        if checking_while_start_index is not None:
            if l[-1].name == ':':
                checking_while_start_index = None
            elif l[-1].name == '\n':
                while_condition_tokens = [Token(tokenize.NAME, 'if'), Token(tokenize.NAME, 'not'), Token(tokenize.OP, '(')] + l[checking_while_start_index + 1:-1] + [Token(tokenize.OP, ')'), Token(tokenize.OP, ':'), Token(tokenize.NEWLINE, '\n')]
                i = 0
                while True:
                    if l[i].name == 'continue' or i == checking_while_start_index:
                        for j, while_condition_token in enumerate(while_condition_tokens):
                            l.insert(i + j, while_condition_token)
                        """
                        if i > 0 and l[i - 1].type == tokenize.INDENT:
                            l.insert(i + j + 1, Token(tokenize.INDENT, l[i - 1] + '    '))
                            l.insert(i + j + 2, Token(tokenize.NAME, 'break'))
                            l.insert(i + j + 3, Token(tokenize.DEDENT, ''))
                            if l[i + j + 4].name != 'continue':
                                while len(l) > i + j + 4:
                                    del l[i + j + 4]
                                checking_while_start_index = None
                                break
                            else:
                                l.insert(i + j + 4, Token(tokenize.INDENT, l[i - 1]))
                                i += j + 5
                                checking_while_start_index += j + 4
                        else:
                        """
                        l.insert(i + j + 1, Token(tokenize.INDENT, '                '))
                        l.insert(i + j + 2, Token(tokenize.NAME, 'break'))
                        l.insert(i + j + 3, Token(tokenize.NEWLINE, '\n'))
                        l.insert(i + j + 4, Token(tokenize.DEDENT, ''))
                        if l[i + j + 5].name != 'continue':
                            while len(l) > i + j + 5:
                                del l[i + j + 5]
                            checking_while_start_index = None
                            break
                        else:
                            i += j + 5
                            checking_while_start_index += j + 4
                    i += 1
                if len(stack) > 1:
                    stack[-2].extend(l)
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
            l = []
            stack.append(l)
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
