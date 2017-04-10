#! /usr/bin/env python

# Standard library
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="groupten",
    version='v0.1',
    author="Semyeong Oh",
    author_email="semyeong.oh@gmail.com",
    packages=["groupten"],
    url="https://github.com/smoh/groupten",
    # license="MIT",
    description="",
    package_data={},
    install_requires=[],
    # include_package_data=True,
)
