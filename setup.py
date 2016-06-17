# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='marvin-transfer',
    version='0.4.0',
    author='Fredrik Johansson',
    author_email='f95johansson@gmail.com',
    packages=['marvin'],
    entry_points = {
        'console_scripts': [
            'marvin=marvin.main:main',
        ],
    },
    url='https://github.com/f95johansson/marvin-transfer',
    license='LICENSE',
    description='Command line utility for easy transfer between local computer and android device.',
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7'
    ],
)