from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'tpdf',
    version          = '0.0.2',
    description      = 'An app to generate PDS for subdirectories',
    long_description = readme,
    author           = 'mario',
    author_email     = 'hanmario@bu.edu',
    url              = 'http://wiki',
    packages         = ['tpdf'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    package_data     = {
        'tpdf': ['template/*', 'template/assets/*']
    },
    entry_points     = {
        'console_scripts': [
            'tpdf = tpdf.__main__:main'
            ]
        }
)
