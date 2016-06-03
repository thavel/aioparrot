#!/usr/bin/env python

from pip.req import parse_requirements
from setuptools import setup, find_packages


try:
    with open('VERSION.txt', 'r') as v:
        version = v.read().strip()
except FileNotFoundError:
    version = '0.0.0-dev'

with open('DESCRIPTION', 'r') as d:
    long_description = d.read()

# Requirements
install_reqs = parse_requirements('requirements.txt', session='dummy')
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='aioparrot',
    description='Asyncio based project to control Parrot drones',
    long_description=long_description,
    author='Thibaut Havel',
    version=version,
    install_requires=reqs,
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
