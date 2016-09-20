#!/usr/bin/env python3

from setuptools import setup

setup (name = 'linkbot_hub_manager',
       author = 'David Ko',
       author_email = 'david@barobo.com',
       version = '0.0.1',
       description = "This is a web application that can be used to manage settings on a Linkbot Hub",
       long_description = README,
       scripts = ['bin/linkbot-hub-manager.py'],
       url = 'http://github.com/BaroboRobotics/linkbot-hub-manager',
       install_requires=[
           'websockets>=3.0', 'passlib', 'bottle'],
       classifiers=[
           'Development Status :: 3 - Alpha',
           'Intended Audience :: Education',
           'Operating System :: OS Independent',
           'Programming Language :: Python :: 3.5',
       ],
)
