# opyum

[![version](https://img.shields.io/pypi/v/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![downloads](https://img.shields.io/pypi/dw/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![license](https://img.shields.io/pypi/l/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![status](https://img.shields.io/pypi/status/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![pyversions](https://img.shields.io/pypi/pyversions/opyum.svg)](http://pypi.python.org/pypi/opyum)


## Description

**Optimizing Python applications without mutilation code.** 

Use the automatic modification of AST for code optimization, which is transparent to the user and requires the addition of only a couple of lines.


## Usage

**Decorator**:

```python
from opyum import optimize

@optimize
def function_for_optimize():
	...
```

**Import-hook**:

```python
import opyum
opyum.activate()

# other imports
```

**"With" syntax:**

```python
import opyum

with opyum.activate:
	# other imports
```

**Command-line mode:**

Show optimized source:

    $ opyum show myfile.py

Diff between original source and optimized source:

    $ opyum diff myfile.py

Console diff (with "-c" or "--console" option):

![console diff example](https://raw.githubusercontent.com/Amper/opyum/master/example/screen1.png)

Custom app diff (with "--app" option):

![app diff example](https://raw.githubusercontent.com/Amper/opyum/master/example/screen2.png)

By default, html diff (without options):

![app diff example](https://raw.githubusercontent.com/Amper/opyum/master/example/screen3.png)


## List of optimizations

**Constant folding**

Before:

```python

```

After:

```python

```

**"'Power' to 'multiplication'" optimization**

Before:

```python
x1 = a ** (-2)
x2 = a ** (-1)
x3 = a ** ( 0)
x4 = a ** ( 1)
x5 = a ** ( 2)
```

After:

```python
x1 = 1 / (a * a)
x2 = 1 / a
x3 = 1
x4 = a
x5 = a * a
```

**"'Yield' to 'yield from'" optimization**

Before:

```python
for x in some_expression:
	yield x
```

After

```python
yield from some_expression
```

**Builtin constant propagation**

Before:

```python
from math import pi
def circumference(r):
	return 2 * pi * r
```

After:

```python
from math import pi
def circumference(r):
	return 2 * 3.141592653589793 * r
```

**Custom constant propagation**

Before:

```python
C_PI = 3.141592653589793

def circumference(r):
	return 2 * C_PI * r
```

After:

```python
C_PI = 3.141592653589793

def circumference(r):
	return 2 * 3.141592653589793 * r
```


## Installation

Installation is simple with pip:

    $ pip install opyum

or with setuptools:

    $ easy_install opyum


## Documentation

 [opyum.readthedocs.org](http://opyum.readthedocs.org/)

 [opyum.rtfd.org](http://opyum.rtfd.org/)

