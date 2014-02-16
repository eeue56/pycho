#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(name='pycho',
      version='0.0.1',
      description='A game engine for Python 2 and 3 with built in AI',
      author='Enalicho',
      author_email='enalicho@gmail.com',
      packages=find_packages(),
      requires=['PyQt', 'OpenGL'],
     )