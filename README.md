# hdytto: How do you turn this on

A library adding new syntax into your Python.
i.e. It is NOT Pythonic :)

* [Compatibility](#compatibility)
* [Usage](#usage)
* [API](#api)
  * [Increment / Decrement](#increment--decrement)
  * [do...while](#dowhile)
  * [Comment](#comment)

## Compatibility

* Python >=3.8

## Usage

At first, make `sitecustomize.py`:

```python
from hdytto import register_hdytto
register_hdytto()
```

Set the environmental variable `PYTHONPATH` the path to the directory containing the `sitecustomize.py`.
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

## API
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
