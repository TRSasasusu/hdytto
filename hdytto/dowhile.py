import tokenize
from token import tok_name
import sys

from .util import Token, isrepl


stack_for_repl = None
repl_counter = None


def dowhile(a):
    global stack_for_repl
    global repl_counter

    if stack_for_repl is not None and len(stack_for_repl) > 0:
        stack = stack_for_repl
        l = stack[-1]
        #l.pop(-1) # remove previous ENDMARKER
        if repl_counter == 1:
            l.insert(0, Token(tokenize.INDENT, '    '))
        repl_counter += 1
    else:
        stack = []
        l = []
        stack_for_repl = None
        repl_counter = None

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
                dowhile_condition_tokens = [Token(tokenize.NAME, 'if'), Token(tokenize.NAME, f'_HDYTTO_DOWHILE_COUNTER_{len(stack)}'), Token(tokenize.NAME, 'and'), Token(tokenize.NAME, 'not'), Token(tokenize.OP, '(')] + l[checking_while_start_index + 1:-1] + [Token(tokenize.OP, ')'), Token(tokenize.OP, ':'), Token(tokenize.NEWLINE, '\n'), Token(tokenize.INDENT, l[8 + (2 if repl_counter is not None else 0)].name + '    '), Token(tokenize.NAME, 'break'), Token(tokenize.NEWLINE, '\n'), Token(tokenize.DEDENT, ''), Token(tokenize.NAME, f'_HDYTTO_DOWHILE_COUNTER_{len(stack)}'), Token(tokenize.VBAREQUAL, '|='), Token(tokenize.NAME, 'True'), Token(tokenize.NEWLINE, '\n')]
                for i, token in enumerate(dowhile_condition_tokens):
                    l.insert(9 + i + (2 if repl_counter is not None else 0), token)
                while len(l) > checking_while_start_index + len(dowhile_condition_tokens):
                    del l[checking_while_start_index + len(dowhile_condition_tokens)]
                checking_while_start_index = None
                if isrepl():
                    base_indent = l[10].name
                    for i in range(len(l)):
                        if i > 0 and l[i].type == tokenize.INDENT:
                            if i == 10 or l[i].name != base_indent:
                                l[i] = Token(l[i].type, '    ' + l[i].name)
                if len(stack) > 1:
                    stack[-2].extend(stack.pop(-1))
                    l = stack[-1]
                else:
                    #print('######')
                    #print(l)
                    #print('######')
                    for i, (t, n) in enumerate(l):
                        if isrepl() and i > 10 and l[i].type == tokenize.INDENT and l[i].name == base_indent:
                            continue
                        if t != tokenize.ENDMARKER:
                            yield t, n
                    l = []
                    stack = []
                    if stack_for_repl is not None:
                        yield tokenize.DEDENT, ''
                        stack_for_repl = None
                        repl_counter = None

        if len(l) <= 1:
            continue
        if l[-2].name == 'do' and l[-1].name == ':':
            l.pop(-1)
            l.pop(-1)
            l = []
            stack.append(l)
            #l.append(Token(tokenize.NAME, 'if'))
            #l.append(Token(tokenize.NAME, 'True'))
            #l.append(Token(tokenize.OP, ':'))
            #l.append(Token(tokenize.NEWLINE, '\n'))
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
    if isrepl():
        if len(stack) == 0:
            pass
        elif repl_counter is None:
            stack_for_repl = stack
            repl_counter = 1
            yield tokenize.NAME, 'if'
            yield tokenize.NAME, 'True'
            yield tokenize.OP, ':'
            yield tokenize.NEWLINE, '\n'
        else:
            if l[0].type != tokenize.INDENT: # there maybe error when inputing do: multi lines, so removing the stacks
                stack_for_repl = None
                repl_counter = None
                for t, n in l:
                    yield t, n
            else:
                yield tokenize.INDENT, '    '
                yield tokenize.NAME, 'pass'
                yield tokenize.NEWLINE, '\n'
    #if len(l) > 7 and l[-1].type == tokenize.ENDMARKER and len(stack) > 0:
        # Called in REPL:
        # >>> do:
    #    stack_for_repl = stack
    #    repl_counter = 1
    #    print('hoge')
    #elif stack_for_repl is not None:
    else:
        for t, n in l:
            yield t, n
    l = []
