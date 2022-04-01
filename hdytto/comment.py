import re
import tokenize

from .util import Token

# `comment` uses regex because indent cannot be restored from dedent generated by tokenize.
def comment(stream):
    return re.sub(r'\/\*[^\/*]*\*\/', '', stream)
