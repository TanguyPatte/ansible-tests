#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

setup(
    name='ansible-tests',
    version='0.0.1',
    packages=find_packages(exclude=["*_tests"]),
    install_requires=[
        'click',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'ansible_tests = ansible_tests.__main__:run',
        ],
    },
)
