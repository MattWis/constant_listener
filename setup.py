#!/usr/bin/env python
from setuptools import setup

setup(name='constant_listener',
      version='0.0.4',
      author='Matt Wismer',
      author_email='mattwis86@gmail.com',
      description='STT engine that listens in the background',
      license='MIT',
      packages=['constant_listener'],
      package_dir={'constant_listener': 'constant_listener'},
      url='https://github.com/MattWis/constant_listener.git',
      install_requires=['scikits.audiolab', 'scikits.samplerate', 'pyaudio'])
