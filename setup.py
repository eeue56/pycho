#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

try:
    license = open('LICENSE').read()
except:
    license = None

try:
    readme = open('README.md').read()
except:
    readme = None

setup(name='pycho',
      version='0.0.3',
      description='A game engine for Python 2 and 3 with built in AI',
      long_description=readme,
      license=license,
      url='http://github.com/eeue56/pycho/',
      author='Enalicho',
      author_email='enalicho@gmail.com',
      packages=find_packages(),
      install_requires=['PyOpenGL', 'numpy'],
)
