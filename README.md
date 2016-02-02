# opyum

[![version](https://img.shields.io/pypi/v/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![downloads](https://img.shields.io/pypi/dw/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![license](https://img.shields.io/pypi/l/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![status](https://img.shields.io/pypi/status/opyum.svg)](http://pypi.python.org/pypi/opyum)
[![pyversions](https://img.shields.io/pypi/pyversions/opyum.svg)](http://pypi.python.org/pypi/opyum)

## Description

Optimizing Python applications without mutilation code


## Usage

### Decorator:

```python
from opyum import optimize

@optimize
def function_for_optimize():
	...
```

### Import-hook:

```python
import opyum
opyum.activate()

# other imports
```

### Command-line mode:

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

## Installation

Installation is simple with pip:

    $ pip install opyum

or with setuptools:

    $ easy_install opyum

## Documentation

 [opyum.readthedocs.org](http://opyum.readthedocs.org/)

 [opyum.rtfd.org](http://opyum.rtfd.org/)

