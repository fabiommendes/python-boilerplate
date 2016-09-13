# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use Python Boilerplate to start
# simple, usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os
from setuptools import setup, find_packages


# Meta information
name = 'python-boilerplate'
pyname = 'python_boilerplate'
author = 'Fábio Macêdo Mendes'
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)


# Save version and author to __meta__.py
with open(os.path.join(dirname, 'src', 'python_boilerplate', '__meta__.py'), 'wb') as F:
    F.write(b'''# Automatically created. Please do not edit.
__version__ = u'%s'
__author__ = u'F\\xe1bio Mac\\xeado Mendes'
''' % version.encode())


setup(
    # Basic info
    name='python-boilerplate',
    version=version,
    author=author,
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/fabiommendes/python-boilerplate',
    description='Creates the skeleton of your Python project.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'jinja2',
        'invoke>=0.13',
        'unidecode',
        'six',
    ],
    extras_require={
        'dev': [
            'pytest',
            'mock',
        ],
    },

    # Data files
    package_data={
        'python_boilerplate': [
            'templates/*.*',
            'templates/license/*.*',
            'templates/docs/*.*',
            'templates/package/*.*'
        ],
    },

    # Scripts
    entry_points={
        'console_scripts': ['python-boilerplate = python_boilerplate.__main__:main'],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)
