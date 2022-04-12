from typing import List, Optional
from dataclasses import dataclass
import tokenize
from token import tok_name
from keyword import iskeyword
import traceback
import sys
import inspect

from .util import Token, syntax_error_util, isrepl


@dataclass
class StackItem:
    const_vars: List[str]
    indent: int
    class_name: Optional[str] = None,


def _in_stack(name, stack):
    for item in stack:
        if name in item.const_vars:
            return True

const_vars_for_repl = None
const_vars_stack_for_repl = None

def const(a):
    global const_vars_for_repl
    global const_vars_stack_for_repl

    if isrepl() and const_vars_for_repl is not None:
        const_vars_stack = const_vars_stack_for_repl
        const_vars = const_vars_stack[-1].const_vars
    else:
        const_vars = []
        const_vars_stack = [StackItem(const_vars, 0)]

    lineno = 1
    l = []
    for type, name in a:
        if isrepl():
            const_vars_for_repl = const_vars
            const_vars_stack_for_repl = const_vars_stack

        #print(tok_name[type], name)
        l.append(Token(type, name))
        #print(l)
        #print(const_vars_stack)
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
            if _in_stack(l[1].name, const_vars_stack):
                syntax_error_util.raise_error(f'redeclaration of const {l[1].name}', lineno=lineno, offset=sum([len(each_l.name) for each_l in l[:-1]]) + len(l) - 2, line=' '.join([each_l.name for each_l in l[:-1]]))
            lineno += 1
            const_vars.append(l[1].name)
            #print(const_vars)
            l.pop(0) # remove const
            while len(l) > 0:
                yield l.pop(0)
            continue
        #if l[0].name == 'class': # TODO: class variables
        #    if l[-1].type != tokenize.INDENT:
        #        continue
        #    const_vars = []
        #    const_vars_stack.append(StackItem(const_vars, 1, l[1].name))
        #    while len(l) > 0:
        #        yield l.pop(0)
        #    continue
        if l[0].name == 'def':
            if l[-1].name != ':':
                continue
            const_vars = []
            const_vars_stack.append(StackItem(const_vars, 0))
            for i in range(len(l)):
                if l[i].name == 'const':
                    const_vars.append(l[i + 1].name)
            while len(l) > 0:
                if l[0].name == 'const':
                    l.pop(0)
                    continue
                yield l.pop(0)
            continue
        if l[0].type == tokenize.INDENT:
            const_vars_stack[-1].indent += 1
            yield l.pop(0)
            continue
        if l[0].type == tokenize.DEDENT:
            const_vars_stack[-1].indent -= 1
            yield l.pop(0)
            if len(const_vars_stack) > 1 and const_vars_stack[-1].indent <= 0:
                const_vars_stack.pop(-1)
                const_vars = const_vars_stack[-1].const_vars
            continue
        if l[0].type == tokenize.NAME:
            if not _in_stack(l[0].name, const_vars_stack):
                yield l.pop(0)
                continue
            if len(l) == 1:
                continue
            if l[1].name not in ['=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '**=', '//=', '@=', ':=']:
                yield l.pop(0)
                continue
            if l[-1].name != '\n' and l[-1].type != tokenize.ENDMARKER:
                continue
            if isrepl() and len(const_vars_stack) > 1:
                while len(const_vars_stack) > 1:
                    const_vars_stack.pop(-1)
                    const_vars = const_vars_stack[-1].const_vars
            syntax_error_util.raise_error(f'invalid assignment to const {l[0].name}', lineno=lineno, offset=sum([len(each_l.name) for each_l in l[:-1]]) + len(l) - 2, line=' '.join([each_l.name for each_l in l[:-1]]))

        if l[0].name == '\n':
            lineno += 1
        yield l.pop(0)

    #print('end')
    for t, n in l:
        yield t, n
    l = []
