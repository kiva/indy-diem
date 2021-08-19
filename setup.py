import os
from setuptools import setup

with open(os.path.abspath("./README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name='indy-diem',
    version='0.0.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/kiva/indy-diem',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    description='indy transaction layer for Diem ledger ',
    license='Apache-2.0',
    author='Kiva',
    author_email='camilop@kiva.org',
    packages=['indy-diem'],
    install_requires=['pytest'],
    tests_require=['pytest']
)