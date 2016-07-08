# -*- coding: utf8 -*-
{%- if boilerplate_header|default(True) %}
#
# This file were created by Python Boilerplate. Use boilerplate to start simple
# usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/boilerplate/
#
{% endif %}
import os
from setuptools import setup, find_packages


# Meta information
name = '{{ project }}'
project = '{{ pyname }}'
author = '{{ author }}'
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)


# Save version and author to __meta__.py
with open(os.path.join(dirname, 'src', project, '__meta__.py'), 'w') as F:
    F.write('__version__ = %r\n__author__ = %r\n' % (version, author))


setup(
    # Basic info
    name=name,
    version=version,
    author=author,
    author_email='{{ email }}',
    url='{{ url|default(github) }}',
    description='{{ short_description|default("A short description for your project.") }}',
    long_description=open('README.rst').read(),

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        {%- for classifier in classifiers %}
        '{{ classifier }}'
        {%- endfor %}
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[{{ requirements }}],
    extras_require={
        'testing': ['pytest'],
    },
    {%- if has_script|default(True) %}

    # Scripts
    entry_points={
        'console_scripts': ['{{ dashed_pyname }} = {{ pyname }}.__main__:main'],
    },
    {%- endif %}

    # Other configurations
    zip_safe=False,
    platforms='any',
    test_suite='%s.test.test_%s' % (name, name),
)