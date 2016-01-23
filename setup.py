import os
from setuptools import setup
from opyum import \
    ( __version__
    , __author__
    , __url__
    , __email__
    )

PATH_BASE = os.path.dirname(__file__)
PATH_BIN  = os.path.join(PATH_BASE, 'bin')

SCRIPTS = None
if os.path.exists(PATH_BIN):
    SCRIPTS = [os.path.join('bin', f) for f in os.listdir(PATH_BIN) if os.path.join(PATH_BIN, f)]

with open(os.path.join(PATH_BASE, 'README.rst')) as file_readme:
    README = file_readme.read()

with open(os.path.join(PATH_BASE, 'REQUIREMENTS.txt')) as file_req:
    REQUIREMENTS = file_req.readlines()

setup\
    ( name = 'opyum'
    , version = '.'.join(map(str, __version__))
    , url = __url__

    , description = 'Optimizing Python applications without mutilation code'
    , long_description = README
    , license = 'BSD 3-Clause License'

    , author = __author__
    , author_email = __email__

    , packages = ['opyum', 'opyum.optimizations']
    , include_package_data = True
    , zip_safe = False

    , install_requires = REQUIREMENTS
    , scripts = SCRIPTS

    , classifiers = \
        [ 'Development Status :: 2 - Pre-Alpha'
        , 'Operating System :: OS Independent'
        , 'Intended Audience :: Developers'
        , 'Intended Audience :: Information Technology'
        , 'Programming Language :: Python'
        , 'Programming Language :: Python :: 2'
        , 'Programming Language :: Python :: 2.7'
        , 'Programming Language :: Python :: 3'
        , 'Programming Language :: Python :: 3.3'
        , 'Programming Language :: Python :: 3.4'
        , 'Programming Language :: Python :: 3.5'
        , 'Programming Language :: Python :: Implementation :: CPython'
        , 'License :: OSI Approved :: BSD License'
        ]
    )

