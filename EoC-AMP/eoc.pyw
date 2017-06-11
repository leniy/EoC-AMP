#!/usr/bin/python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#修订信息参考__init__.py文件

import wx
import eoclib
import eoclib.gui
from eoclib.device import RcEocHead
from eoclib.common import getiplist
import time
import os
import sys
import threading
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub

#sys.argv.append("-gui")#测试GUI模式
#sys.argv.append("-console")#测试命令行模式

class RedirectText(object):
	"""创建RedirectText类，用于将程序中print打印的信息，重定向到文本框"""
	def __init__(self, aWxTextCtrl):
		self.out = aWxTextCtrl
	def write(self, string):
		self.out.WriteText(string)

class Main_Frame ( eoclib.gui.Main_Frame ):
	"""创建新的Main_Frame类，继承自eoclib.gui库。同时定义点击按钮时执行的代码"""
	def __init__( self, parent ):
		"""创建界面，创建监听，更改标准输出"""
		eoclib.gui.Main_Frame.__init__ ( self, parent )
		self.SetIcon(wx.Icon('res/author.ico', wx.BITMAP_TYPE_ICO))
		self.about6 = wx.MenuItem( self.about1, wx.ID_ANY, u"更新：" + eoclib.eoc_inf['update_date'], wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about6 )
		pub.subscribe(self.updateDisplay, "update") # 监听来自update的消息，利用updateDisplay函数更新窗口
		sys.stdout = RedirectText(self.LogRedirect) # 将系统标准输出重定向到文本框

	def updateDisplay(self, msg):#msg是监听自update的消息
		#msg是EocStartThread线程执行进度的百分比
		if isinstance(msg, int):#如果是数字，说明线程正在执行，更新进度条
			self.rate_staticText.SetLabel(u"已完成%s%%" % msg)
			self.rate_gauge.SetValue( msg )
		elif msg == u"完成":
			self.rate_staticText.SetLabel("%s" % msg)
			self.rate_gauge.SetValue( 100 )
			self.EocStartButton.Enable()
		else:
			self.rate_staticText.SetLabel("%s" % msg)

	def eocstart( self, event ):
		event.GetEventObject().Disable()#把执行本函数的按钮禁用掉
		#因为用户可能修改了配置，故需要重新获取一次配置信息，并在线程执行前保存至配置文件
		#start_ip   = str(self.StartIP.GetValue())
		#end_ip     = str(self.EndIP.GetValue())
		#start_pvid = str(self.StartPVID.GetValue())
		#end_pvid   = str(self.EndPVID.GetValue())
		#saveconfig(start_ip, end_ip, start_pvid, end_pvid)
		EocStartThread()
		self.rate_staticText.SetLabel(u"开始自动配置")

class EocStartThread(threading.Thread):
	"""创建新的EocStartThread类，将自动配置的代码封装在一个线程中"""
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)#设置本线程随主线程一起结束。
		self.start()

	def run(self):
		eoc_auto_main("gui")

class GetCnuInHeadThread(threading.Thread):
	"""将获取终端信息的代码打包，采用多线程调用，加快检索速度"""
	def __init__(self, ip, runtype):
		threading.Thread.__init__(self)
		self.ip = ip
		self.runtype = runtype

	def run(self):
		global mylock, file_object, all_cnu_info_list, all_ip_list
		mylock.acquire()
		this_dev = RcEocHead(self.ip, 'admin', 'admin')
		#mylock.acquire()
		if this_dev.device_is_up == False:
			s = '"%s","Can NOT open"\n' % (self.ip)
			print s
			file_object.write(s)
		else:
			temptemptemp = this_dev.get_allcnu_info()
		if this_dev.device_is_up:
			all_cnu_info_list.extend(temptemptemp)

			if self.runtype == "gui":
				rate = 100.0 * ( all_ip_list.index(self.ip) ) / ( len(all_ip_list) )
				wx.CallAfter(pub.sendMessage, "update", msg = int(rate))
			if len(temptemptemp) > 0:#当前ip至少有一个Cnu记录的时候
				for temp_list in temptemptemp:
					tempstrtempstr = ''
					tempstrtempstr += '"' + temp_list['Eoc_ip']         + '",'
					tempstrtempstr += '"' + str(temp_list['Cnu_index']) + '",'
					tempstrtempstr += '"' + temp_list['Cnu_name']       + '",'
					tempstrtempstr += '"' + temp_list['Cnu_mac']        + '",'
					tempstrtempstr += '"' + temp_list['Cnu_model']      + '",'
					tempstrtempstr += '"' + str(temp_list['Cnu_pvid1']) + '",'
					tempstrtempstr += '"' + str(temp_list['Cnu_pvid2']) + '",'
					tempstrtempstr += '"' + str(temp_list['Cnu_pvid3']) + '",'
					tempstrtempstr += '"' + str(temp_list['Cnu_pvid4']) + '"\n'
	
					print tempstrtempstr
					file_object.write(tempstrtempstr)
			else:
				file_object.write('"' + self.ip + '","has no device"\n')
		mylock.release()

def eoc_auto_main(runtype = "console"):
	"""函数功能：自动检索全部头端及下属终端的信息，并配置vlan
	函数输入：runtype是gui模式还是console模式
	函数输出：无
	"""
#第一步，获取全部头端下面全部终端的信息
	global mylock, file_object, all_cnu_info_list, all_ip_list

	all_ip_list = [] # 把所有的头端ip放到一个列表中
	all_ip_list.extend(getiplist()) # 由于本部分功能与gui窗口属于不同的线程，为了防止冲突，配置信息直接从配置文件中获取
	all_cnu_info_list = [] #全部终端的列表

	if not os.path.exists('logs'): # 创建logs文件夹，放置每次运行的记录文件
		os.makedirs('logs')
	if not os.path.exists(time.strftime('logs/%Y%m',time.localtime(time.time()))):
		os.makedirs(time.strftime('logs/%Y%m',time.localtime(time.time())))
	output_csv_file_name = time.strftime('logs/%Y%m/%Y%m%d_%H%M%S.csv',time.localtime(time.time()))#文件名是导出文件的完整文件名，包含扩展名

	if runtype == "gui":
		rate = 0#程序进度的百分比
		wx.CallAfter(pub.sendMessage, "update", msg = rate)

	file_object = open(output_csv_file_name, 'w+')
	s = '"Eoc Head IP","Cnu Index","Cnu Name","Cnu MAC","Cnu Modal","Cnu PVID1","Cnu PVID2","Cnu PVID3","Cnu PVID4"\n'
	print s
	file_object.write(s)

	mylock = threading.Lock() # 创建锁
	threads = [] # 保存线程列表
	for ip in all_ip_list: # 创建线程对象
		threads.append(GetCnuInHeadThread(ip, runtype))
	for t in threads: # 启动线程
		t.start()
		#time.sleep(0.2) # 休息一下，避免同一时刻几百个线程同时启动，下载js文件会阻塞导致失败
	for t in threads: # 这是上面的线程全部启动了，等待所有线程都结束
		t.join()
#	for ip in all_ip_list: # 创建线程对象
#		t = GetCnuInHeadThread(ip, runtype)
#		t.start()
#		t.join()
	file_object.close()

#第二步，根据终端的数量，生成VLAN仓库
	cnu_numbers = len(all_cnu_info_list)
	cnu_numbers_thousands = int(cnu_numbers/999)+1 # 有几千个cnu，方便生成几千个VLAN

	start_pvid = 2001 # 点播VLAN直接减1000计算
	end_pvid   = 2999
	all_vlan_list = []
	for i in range(cnu_numbers_thousands):
		all_vlan_list.extend(range(start_pvid,end_pvid + 1))

#第三步，将已经使用的VLAN从VLAN仓库中依次去掉
	for temp_cnu in all_cnu_info_list:
		temp_pvid = int(temp_cnu['Cnu_pvid1']) # 1口是2xxx的vlan，2口1xxx，直接减一，3口4口屏蔽，设vlan为1。故而只需要分析1口
		try: # 可能仓库中VLAN2000只出现2次，却要删除10次，因此多余的删除操作要忽略
			all_vlan_list.remove(temp_pvid) # 删除vlan仓库中第一次出现的temp_pvid
		except:
			pass

#第四步，将未配置的cnu配置上VLAN
	unset_cnu_count = 0 # 记录有几个未配置的设备
	for temp_cnu in all_cnu_info_list: #循环检测所有的cnu
		if (temp_cnu['Cnu_pvid1'] == 1) or (temp_cnu['Cnu_pvid1'] == 2000):  #如果当前cnu第一个FE网口没有设置pvid（1），或者是默认pvid（2000），则开始设置
			unset_cnu_count = unset_cnu_count + 1
			ip = temp_cnu['Eoc_ip']
			this_dev = RcEocHead(ip, 'admin', 'admin')
			if this_dev.device_is_up == False:
				continue
			cnuindex = temp_cnu['Cnu_index'] #cnu的索引
			port_index1 = 100000 + cnuindex + 1 #4个FE端口的索引。因为暂时没有开通其他服务，所以4个端口设置同样的pvid
			port_index2 = 100000 + cnuindex + 2
			port_index3 = 100000 + cnuindex + 3
			port_index4 = 100000 + cnuindex + 4
			temppvid = all_vlan_list[0] #pvid设置为第一个尚未使用的值
			all_vlan_list = all_vlan_list[1:] #把第一个从VLAN仓库中去掉
			this_dev.set_port_pvid(port_index1,temppvid)
			this_dev.set_port_pvid(port_index2,temppvid - 1000)  #1000为点播的vlan
			this_dev.set_port_pvid(port_index3,1)     #1为未配置时的默认值，此时端口暂不开启
			this_dev.set_port_pvid(port_index4,1)     #1为未配置时的默认值，此时端口暂不开启
			print "set a pvid " + str(temppvid) + " in " + str(ip)
	if runtype == "gui":
		wx.MessageBox(u"搜索完成，共找到" + str(len(all_cnu_info_list)) + u"个设备\n\n其中，" + str(unset_cnu_count) + u"台未配置，现已配置完成",u"通知",wx.OK|wx.ICON_INFORMATION)
		wx.CallAfter(pub.sendMessage, "update", msg = u"完成")

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
		gui = Main_Frame(None)
		gui.Show()
		app.MainLoop()
	if sys.argv[1] == "-console":
		eoc_auto_main("console")
