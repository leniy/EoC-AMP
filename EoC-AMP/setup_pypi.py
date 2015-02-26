#!/usr/bin/python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#修订信息参考__init__.py文件

from setuptools import setup, find_packages
import sys

if len(sys.argv) == 1:
	print "============= use 'register' to register\n============= use 'sdist' to package pip files\n============= use 'sdist upload' to upload\n"


setup(
	name = 'eoclib',
	version = '1.33.01.23',
	keywords = ('eoc', 'amp'),
	description = 'EoC automatic manager platform',
	license = 'BSD License',
	install_requires = ['wx>=0.1'],

	author = 'Leniy Tsan',
	author_email = 'm@leniy.org',

	packages = find_packages(),
	platforms = 'any',
)