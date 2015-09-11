# -*- coding: utf-8 -*-
#!/usr/bin/env python

from setuptools import setup

setup(name='django-log-file-viewer',
    version='0.10',
    description='Django admin expansion to read/parse file based Django Logging output.',
    author='Intelie',
    packages=['django_log_file_viewer'],
    package_data={'django_log_file_viewer': [
        'templatetags/',
        'templates/*.html',
        'testdata/log/test/.gitignore', # To keep this directory (required for farther tests)
        'testdata/log/testlog.log',
        'README.rst',
        'README',
        ]},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: Log Analysis',
        'Topic :: System :: Logging',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Processing',
        ],
)
