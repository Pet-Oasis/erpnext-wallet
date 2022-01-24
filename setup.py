# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in erpnext_wallet/__init__.py
from erpnext_wallet import __version__ as version

setup(
	name='erpnext_wallet',
	version=version,
	description='Wallet',
	author='PET Oasis',
	author_email='alaa@petoasis.com.sa ',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
