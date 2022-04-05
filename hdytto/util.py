from typing import NamedTuple
import sys

class Token(NamedTuple):
    type: int
    name: str


def isrepl():
    return hasattr(sys, 'ps1')
