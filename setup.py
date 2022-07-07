#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

from setuptools import find_packages
from setuptools import setup
import os

# One strategy for storing the overall version is to put it in the top-level
# package's __init__ but Nb. __init__.py files are not needed to declare
# packages in Python 3

# Populate long description setting with content of README
#
# Use markdown format read me file as GitHub will render it automatically
# on package page
here = os.path.abspath(os.path.dirname(__file__))
_long_description = open(os.path.join(here, "README.md")).read()

requirements = [line.strip() for line in open("requirements.txt")]

setup(
    # See:
    # https://www.python.org/dev/peps/pep-0301/#distutils-trove-classification
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Topic :: Security",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="BADC-csv package",
    python_requires=">=3.7.0",
    entry_points={},
    install_requires=requirements,
    long_description=_long_description,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    test_suite="tests",
    version='0.1.0',
    zip_safe=False,
)