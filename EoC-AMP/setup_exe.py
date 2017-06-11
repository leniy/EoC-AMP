#!/usr/bin/python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#修订信息参考__init__.py文件

from distutils.core import setup
import py2exe, sys, os
from eoclib import eoc_inf

if len(sys.argv) == 1:
	sys.argv.append("py2exe")

options = {'py2exe':{
		"compressed": 1,
		"optimize": 0, #1和2运行不起来
		'bundle_files': 1,
		"dll_excludes": ["w9xpopen.exe"],
		"packages":["wx.lib.pubsub"]
	}}

setup(
	version = eoc_inf['version'],
	description = eoc_inf['description'],
	name = eoc_inf['name'],#这儿的参数只能是ASCII字符
	author = eoc_inf['author'],
	options = options,
	zipfile=None,
	data_files = [('res', ['res/author.png',"res/author.ico"]),('', ['list.csv'])],
	windows = [{'script': "eoc.pyw",'icon_resources': [(1, "res/author.ico")]}]
)

os.rename('dist/eoc.exe','dist/eoc.'+eoc_inf['version']+'.exe')
