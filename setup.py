# -*- coding: utf-8 -*-
#
#   pyramid_walrus : a walrus integration for pyramid
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import with_statement
from contextlib import contextmanager
import os.path


def setup_dir(f):
    ''' Decorate f to run inside the directory where setup.py resides.
    '''
    setup_dir = os.path.dirname(os.path.abspath(__file__))

    def wrapped(*args, **kwargs):
        with chdir(setup_dir):
            return f(*args, **kwargs)

    return wrapped


@contextmanager
def chdir(new_dir):
    old_dir = os.path.abspath(os.curdir)
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(old_dir)


@setup_dir
def import_setuptools():
    import setuptools
    return setuptools


@setup_dir
def readfile(path):
    with open(path) as f:
        return f.read()


@setup_dir
def get_version():
    import pyramid_walrus
    return pyramid_walrus.__version__


def alltests():
    import sys
    import unittest
    import zope.testrunner.options
    import zope.testrunner.find
    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    args = sys.argv[:]
    defaults = ['--test-path', here]
    options = zope.testrunner.options.get_options(args, defaults)
    suites = list(zope.testrunner.find.find_suites(options))
    return unittest.TestSuite(suites)


tests_require = [
    'pyramid',
    'hirlite',
    'vedis',
    'ledis',
    'zope.testrunner',
]

setup_info = {
    'name': 'pyramid_walrus',
    'version': get_version(),
    'description': 'a walrus integration for pyramid',
    'long_description': readfile('README.rst') + readfile('CHANGES.rst'),

    'author': 'mete0r',
    'author_email': 'mete0r@sarangbang.or.kr',
    'license': 'GNU Lesser General Public License v3 or later (LGPLv3+)',
    'url': 'https://github.com/mete0r/pyramid_walrus',

    'packages': [
        'pyramid_walrus',
        'pyramid_walrus.tests',
    ],
    'package_dir': {'': '.'},
    'install_requires': [
        'walrus',
    ],
    'tests_require': tests_require,
    'test_suite': '__main__.alltests',
    'extras_require': {
        'test': tests_require,
    },
    'entry_points': {
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: Pyramid',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',  # noqa
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    'keywords': ['pyramid', 'walrus'],
    'zip_safe': True,
}


@setup_dir
def main():
    setuptools = import_setuptools()
    setuptools.setup(**setup_info)


if __name__ == '__main__':
    main()
