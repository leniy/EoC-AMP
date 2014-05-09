# -*- coding: utf-8 -*-
#作者：Leniy
from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
	options = {'py2exe': {'bundle_files': 1}},
	#console = [{'script': "eoc_main.py"}],
	windows = [{'script': "eoc_main.py", 'icon_resources': [(1, "author.ico")]}],
	zipfile = None,
)
