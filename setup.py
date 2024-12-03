# Copyright (c) 2017 Kyle Howen
# All Rights Reserved.

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='cmdtools',
    version='0.1.0',
    description='Commandline Tools and Helpers',
    packages=["sipy"],
    # scripts=['bin/ssipy'],
    entry_points = {
        'console_scripts': [
            'sd=cmdtools.bin.sd:main',
            'gitp=cmdtools.bin.gitp:main',
        ]},
    # namespace_packages=['subinitial'],
    license='UNLICENSED',
    url='subinitial.com',
    author='Kyle Howen',
    author_email='kyle.howen@subinitial.com',
    long_description=read("./readme.md"),
    keywords="subinitial",
    classifiers = [
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ]
)
