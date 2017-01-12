from distutils.core import setup
from setuptools import find_packages

setup(
    name='StageIndicateursMultiDispositifs',
    version='1.1',
    license='',
    author='valentin',
    author_email='valentin@lachand.net',
    description='',

    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers, Searchers',
    'Programming Language :: Python :: 2.7',
    ],

    packages=find_packages(),
    install_requires=['kivy'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.kv', '*.json','*.png','*.jpeg'],
    },
    entry_points={
    'console_scripts':['Table=Dev.src.Table:main'],
    }
)
