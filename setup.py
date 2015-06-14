#!/usr/bin/env python

from os.path import exists
from setuptools import setup, find_packages

from django_smalluuid import __version__

setup(
    name='django-smalluuid',
    version=__version__,
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    packages=find_packages(),
    scripts=[],
    url='https://github.com/adamcharnock/django-smalluuid',
    license='MIT',
    description='Short-form UUID field for Django 1.8 and above',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    install_requires=[
        'django>=1.8',
        'smalluuid>=0.1.4',
    ],
)
