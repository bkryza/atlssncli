import os
from setuptools import setup, find_packages

from atlssncli import __version__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requirements = []

setup(
    name = "atlssncli",
    version = ".".join(map(str, __version__)),
    description = "Simple command-line client unifying access to Atlassian® services.",
    long_description = read('README.rst'),
    url = 'https://github.com/bkryza/atlssncli',
    license = 'Apache License 2.0',
    author = 'Bartek Kryza',
    author_email = 'bkryza@gmail.com',
    packages = find_packages(exclude=['tests']),
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = [
        'configparser',
        'Click',
        'humanfriendly',
        'joblib',
        'six',
        'decorest',
        'pygit2',
        'python-dateutil'
    ],
    entry_points='''
        [console_scripts]
        atlssn=atlssncli.atlssn:cli
    ''',
    tests_require = [],
)
