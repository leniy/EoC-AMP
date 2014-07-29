#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#更新日期：2014.07.27
#修订版本：第32次修订

import wx
import eoclib
import eoclib.gui as lib_eoc_gui
import eoclib.func as lib_eoc_func
import time
import os
import sys
from threading import Thread
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
#from wx.lib.pubsub import Publisher #用这条命令会导致py2exe生成的程序报错
#from wx.lib.pubsub import setuparg1  #换成这个后，需要把代码中的Publisher()换成Publisher

#sys.argv.append("-gui")#测试GUI模式
#sys.argv.append("-console")#测试命令行模式

#定义全局变量
#all_head_info_list = []
#pvid_dict = {}
#unset_cnu_count = 0

#创建logs文件夹，放置每次运行的记录文件
if not os.path.exists('logs'):
	os.makedirs('logs')

#创建RedirectText类，用于将程序中print打印的信息，重定向到文本框
class RedirectText(object):
	def __init__(self,aWxTextCtrl):
		self.out=aWxTextCtrl

	def write(self,string):
		self.out.WriteText(string)
		#self.out.WriteText('\n\r')

#创建新的MainGUI类，继承自lib_eoc_gui库。同时定义点击按钮时执行的代码
class MainGUI ( lib_eoc_gui.MainFrame ):
	def __init__( self, parent ):
		#创建界面
		lib_eoc_gui.MainFrame.__init__ ( self, parent )
		#读取配置信息
		start_ip, end_ip, start_pvid, end_pvid = lib_eoc_func.getconfig()
		self.StartIP.SetValue(start_ip)
		self.EndIP.SetValue(end_ip)
		self.StartPVID.SetValue(start_pvid)
		self.EndPVID.SetValue(end_pvid)
		#监听来自update的消息，利用updateDisplay函数更新窗口
		#Publisher().subscribe(self.updateDisplay, "update")
		pub.subscribe(self.updateDisplay, "update")
		#将系统标准输出重定向
		redir=RedirectText(self.LogRedirect)#gui布局代码尚未更新，暂时定向到这个文本框
		sys.stdout=redir
	def eocstart( self, event ):
		event.GetEventObject().Disable()#把执行本函数的按钮禁用掉
		#因为用户可能修改了配置，故需要重新获取一次配置信息，并在线程执行前保存至配置文件
		start_ip   = str(self.StartIP.GetValue())
		end_ip     = str(self.EndIP.GetValue())
		start_pvid = str(self.StartPVID.GetValue())
		end_pvid   = str(self.EndPVID.GetValue())
		lib_eoc_func.saveconfig(start_ip, end_ip, start_pvid, end_pvid)
		EocStartThread()
		self.rate_staticText.SetLabel(u"开始自动配置")
	def updateDisplay(self, msg):#msg是监听自update的消息
		#t = msg.data#t是EocStartThread线程执行进度的百分比
		t = msg
		if isinstance(t, int):#如果是数字，说明线程正在执行，更新进度条
			self.rate_staticText.SetLabel(u"已完成%s%%" % t)
			self.rate_gauge.SetValue( t )
		elif t == u"完成":
			self.rate_staticText.SetLabel("%s" % t)
			self.rate_gauge.SetValue( 100 )
			self.EocStartButton.Enable()
		else:
			self.rate_staticText.SetLabel("%s" % t)

#创建新的EocStartThread类，将自动配置的代码封装在一个线程中
class EocStartThread(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.setDaemon(True)#设置本线程随主线程一起结束。
		self.start()
	def run(self):
		lib_eoc_func.eoc_auto_main("gui")

#下面是主程序
if len(sys.argv) == 1:#如果程序不带参数运行，默认为GUI模式
	sys.argv.append("-gui")
if len(sys.argv) == 2:#如果程序带一个参数运行，则判断模式
	if sys.argv[1] == "-h":
		print u"    -h         显示本帮助信息"
		print u"    -gui       窗口模式"
		print u"    -console   命令行模式"
	if sys.argv[1] == "-gui":
		app = wx.App()
		gui = MainGUI(None)
		gui.Show()
		app.MainLoop()
	if sys.argv[1] == "-console":
		lib_eoc_func.eoc_auto_main("console")
