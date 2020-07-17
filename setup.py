"""

"""

from setuptools import setup

setup(
    name='__init__',
    version='0.1',
	py_modules=[''],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        yourscript=yourscript:cli
    ''',
)