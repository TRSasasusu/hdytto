# hdytto: How do you turn this on

A library adding new syntax into your Python.
i.e. It is NOT Pythonic :)

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
