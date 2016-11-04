#!/usr/bin/env python

from setuptools import setup

__version__ = '0.0.0.1'
__author__ = 'r-p1e'


def project_description():
    return """
           gripari-ftp-lestate load data from lestate ftp server.
           """


setup(name="gripari-ftp-lestate",
      version=__version__,
      description=project_description(),
      author=__author__,
      author_email="r-p1e@protonmail.com",
      url="https://www.github.com/r-p1e/gripari-ftp-lestate",
      packages=["gripari_ftp_lestate"],
      setup_requires=["pytest-runner", "xmltodict", "transliterate"],
      tests_require=["pytest", "pyftpdlib", "pytest-xdist", "pytest-sugar",
                     "pytest-cov"],
      package_dir={"gripari_ftp_lestate": "src"},
      scripts=["app/gripari_ftp_lestate.py"])
