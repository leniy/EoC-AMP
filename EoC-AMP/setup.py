# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#更新日期：2014.07.22
#修订版本：第31次修订

from distutils.core import setup
import py2exe, sys, os

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
	version = "0.0.31",
	description = u"山东广电网络集团-EoC管理软件",
	name = "EoC",#这儿的参数只能是ASCII字符
	options = options,     
	zipfile=None,
	author = u"Leniy(Leniy Tsan)",
	data_files = [('res', ['res/author.png'])],
	#console = [{'script': "eoc_main_console.py"}],
	#console = [{'script': "eoc_main.py"}],
	windows = [{'script': "eoc.pyw",'icon_resources': [(1, "res/author.ico")]}],
)
