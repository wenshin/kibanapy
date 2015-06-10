#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kibanapy

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

with open('requirements.txt') as requires_file:
    requirements = requires_file.read().split('\n')
    if not requirements[-1]:
        requirements[:-1]

with open('requirements_dev.txt') as requires_dev_file:
    requirements_dev = requires_dev_file.read().split('\n')
    if not requirements[-1]:
        requirements[:-1]

setup(
    name='kibanapy',
    version=kibanapy.__version__,
    description="A python util to create kibana dashboard",
    long_description=readme + '\n\n' + history,
    author="kibanapy",
    author_email='yanwx@knownsec.com',
    url='https://github.com/wenshin/kibanapy',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='kibanapy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=requirements_dev
)
