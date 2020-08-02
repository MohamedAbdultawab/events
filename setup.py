# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in events/__init__.py
from events import __version__ as version

setup(
	name='events',
	version=version,
	description='Event Management Module',
	author='Mohamed Abdultawab',
	author_email='mohamedtoba96@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
