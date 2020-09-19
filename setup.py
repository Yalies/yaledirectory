# Upload package to PyPi.

from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='yaledirectory',
      version='1.1.1',
      description='Library for fetching data from the Yale Directory API.',
      url='https://github.com/ErikBoesen/yaledirectory',
      author='Erik Boesen',
      author_email='me@erikboesen.com',
      license='GPL',
      packages=['yaledirectory'],
      install_requires=requirements)
