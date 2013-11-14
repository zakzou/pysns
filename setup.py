#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
        name = 'pysns',
        version = '0.0.2',
        keywords = ('OAuth2 Client', 'OAuth2', 'Login'),
        description = 'Third-party login',
        long_description = 'See http://github.com/zakzou/pysns',
        license = 'MIT',

        url = 'http://github.com/zakzou/pysns',
        author = 'zakzou',
        author_email = 'zakzou@live.com',

        packages = find_packages(),
        include_package_data = True,
        platforms = 'any',
        install_requires = ['simplejson>=2.3.2', 'liboauth2>=0.0.1'],
        classifiers=[
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            ],
        )
