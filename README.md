# hdytto: How do you turn this on

A library adding new syntax into your Python.
i.e. It is NOT Pythonic :)

* [Compatibility](#compatibility)
* [Getting Started](#getting-started)
  * [REPL](#repl)
* [hdytto Reference](#hdytto-reference)
  * [Increment / Decrement](#increment--decrement)
  * [do...while](#dowhile)
  * [Comment](#comment)

## Compatibility

* Python >=3.8

## Getting Started

Install from [PyPI](https://pypi.org/project/hdytto/):

```bash
$ pip install hdytto
```

This library cannot be used by `import hdytto` as in other libraries, but the usage is simple. At first, make `sitecustomize.py`:

```python
from hdytto import register_hdytto
register_hdytto()
```

Set the environmental variable `PYTHONPATH` the path to the directory containing the `sitecustomize.py` (e.g. `export PYTHONPATH=.`).
Then, run `main.py`:

```
# coding: hdytto

a = 5
print(a++)
print(a)
```

The output will be

```
5
6
```

### REPL

Additionally, make `.pythonrc.py`:

```python
import sys
import sitecustomize
sys.stdin.reconfigure(encoding='hdytto')
```

Set the environmental variable `PYTHONSTARTUP` the path to this `.pythonrc.py` (e.g. `export PYTHONSTARTUP=.pythonrc.py`).
Then, type `python`:

```
$ python
>>> a = 5
>>> a++
5
>>> do:
...     b = ++a
...     while b < 10
...
>>> b
10
```

## hdytto Reference
### Increment / Decrement
#### Syntax

```
x++
++x
x--
--x
```

#### Example

```
# coding: hdytto
a = 5
print(a++)
print(++a)
b = 10 - --a
print(b--)
```

Output:
```
5
7
4
```

### do...while
#### Syntax

```
do:
    statement
    while condition
```

#### Example

```
# coding: hdytto
do:
    a = 5
    while a < 3
do:
    b = a * 2
    while a++ < 10:
        pass
    while b <= 20
print(b)
```

Output:
```
22
```

### Comment
#### Syntax

```
/* */
```

#### Example

```
# coding: hdytto
a = /* foo */ 10
print(a)
if a == 10:
    b = 5
    /*b = 10
print(a - 20)*/
print(b)
```

Output:
```
10
5
```
