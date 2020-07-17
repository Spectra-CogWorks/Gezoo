"""
The setup file used to configure the command-line interface stored in __init__.py
"""

from setuptools import setup, find_packages

setup(
    name='Gezoo',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
		'pillow',
		'mygrad',
		'facenet-pytorch',
		'mynn',
		'numpy',
		'networkx',
    ],
    entry_points='''
        [console_scripts]
        gezoo=Gezoo.__init__:cli
    ''',
)