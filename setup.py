import os
from setuptools import setup, find_packages

from atlssncli import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = []

setup(
    name = "atlssncli",
    version = ".".join(map(str, __version__)),
    description = "",
    long_description = read('README.rst'),
    url = 'https://github.com/bkryza/atlssncli',
    license = 'MIT',
    author = 'Bartek Kryza',
    author_email = 'bkryza@gmail.com',
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = [
        'Click',
        'humanfriendly',
        'six',
        'decorest',
        'pygit2',
        'dateutil'
    ],
    entry_points='''
        [console_scripts]
        atlssn=atlssncli.atlssn:cli
    ''',
    tests_require = [],
)
