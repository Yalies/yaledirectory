# Upload package to PyPi.

from setuptools import setup

setup(name='yaledirectory',
      version='1.0.0',
      description='Library for fetching data from the Yale Directory API.',
      url='https://github.com/ErikBoesen/yaledirectory',
      author='Erik Boesen',
      author_email='me@erikboesen.com',
      license='GPL',
      packages=['yaledirectory'],
      install_requires=['requests'])
