# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-log-file-viewer',
    version='0.10',
    include_package_data=True,
    description='Django admin expansion to read/parse file based Django Logging output.',
    author='',
    packages=['django_log_file_viewer'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: Log Analysis',
        'Topic :: System :: Logging',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Processing',
    ],
)
