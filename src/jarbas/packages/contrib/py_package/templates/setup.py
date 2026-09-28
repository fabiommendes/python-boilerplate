# -*- coding: utf-8 -*-
{%- if boilerplate_header|default(True) %}
#
# This file were created by Python Boilerplate. Use boilerplate to start simple
# usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#
{% endif %}
import os
import codecs
from setuptools import setup, find_packages

# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'src', {{ pyname|repr }}, '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = {{ author|unicode_escape|repr }}
''' % version
with open(path, 'w') as F:
    F.write(meta)

setup(
    # Basic info
    name={{ pyname|replace('_', '-')|repr }},
    version=version,
    author={{ author|repr }},
    author_email='{{ email }}',
    url='{{ url|default(github) }}',
    description='{{ short_description|default("A short description for your project.") }}',
    long_description=codecs.open('README.rst', 'rb', 'utf8').read(),

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        {%- for classifier in classifiers %}
        '{{ classifier }}',
        {%- endfor %}
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and dependencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[{{ requirements|indent(8) }}
    ],
    extras_require={
        'dev': [
            'python-boilerplate[dev]',
        ],
    },
    {%- if has_script|default(True) %}

    # Scripts
    entry_points={
        'console_scripts': ['{{ pip_name }} = {{ package_name }}.__main__:main'],
    },
    {%- endif %}

    # Other configurations
    zip_safe=False,
    platforms='any',
)