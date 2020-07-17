"""
The setup file used to configure the command-line interface stored in __init__.py
"""

from setuptools import setup

setup(
    name='Gezoo',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        yourscript=yourpackage.scripts.yourscript:cli
    ''',
)