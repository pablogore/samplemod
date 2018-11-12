# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='livestories',
    version='0.1.0',
    description='livestories download files and process',
    long_description=readme,
    author='Kenneth Reitz',
    author_email='pablo.m.gore@gmail.com',
    url='https://github.com/pablogore/livestories',
    license=license,
    packages=find_packages(exclude='tests'),
    install_requires=[
        'SimpleConfigParser',
        'pandas',
    ],
    include_package_date=True,
    package_dir={'': '.'},
    package_data={
        '': ['*.ini'],
    },
    entry_points={
        'console_scripts': [
            'live=livestories.scripts.download_and_process:main',
        ],
    },
)

