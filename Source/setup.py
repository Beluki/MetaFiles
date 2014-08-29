# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name = 'MetaFiles',
    version = '2014.08.29',
    url = 'https://github.com/Beluki/MetaFiles',
    license = 'BSD',
    author = 'Beluki',
    author_email = 'beluki@gmx.com',
    description = 'Like Flask-FlatPages or Flask-JSONPages, but reusable and library/markup agnostic.',
    py_modules = ['MetaFiles'],
    zip_safe = False,
    platforms = 'any',
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3'
    ]
)

