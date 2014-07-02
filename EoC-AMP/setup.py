# -*- coding: utf-8 -*-
#作者：Leniy
from distutils.core import setup
import py2exe, sys, os

if len(sys.argv) == 1:
	sys.argv.append("py2exe")

options = {'py2exe':{
		"compressed": 1,
		"optimize": 0, #1和2运行不起来
		'bundle_files': 1,
		"dll_excludes": ["w9xpopen.exe"]
	}}

setup(
	version = "0.0.1",
	description = u"广电网络EoC终端自动管理软件",
	name = "EoC",
	options = options,     
	zipfile=None,
	author = u"Leniy(Leniy Tsan)",
	data_files = [('', ['author.png'])],
	console = [{'script': "eoc_main_console.py"}],
	windows = [{'script': "eoc_main_gui.py",'icon_resources': [(1, "author.ico")]}],
)
