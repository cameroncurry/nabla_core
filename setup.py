#
# Copyright Cameron Curry (c) 2017
#

from setuptools import setup, find_packages

install_requires = [
    'Django>=1.11.0'
]

setup(
    name='nabla_core',
    version='0.1.0',
    author='Cameron Curry',
    description='Core module for the Nabla project',
    install_requires=install_requires,
    packages=find_packages(),
    test_suite='runtests.runtests'
)
