#!/usr/bin/python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#修订信息参考__init__.py文件

import time
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from device import RcEocHead
from common import getiplist
import threading

class GetCnuInHeadThread(threading.Thread):
	"""将获取终端信息的代码打包，采用多线程调用，加快检索速度"""
	def __init__(self, ip, runtype):
		threading.Thread.__init__(self)
		self.ip = ip
		self.runtype = runtype
	def run(self):
		global mylock, file_object, all_cnu_info_list, all_ip_list
		this_dev = RcEocHead(self.ip, 'xxxxxxxxx','xxxxxxxxxxx')
		if this_dev.device_is_up == False:
			s = '"%s","Can NOT open"\n' % (self.ip)
			print s
			file_object.write(s)
		else:
			temptemptemp = this_dev.get_allcnu_info()
		if this_dev.device_is_up and mylock.acquire():
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
	output_csv_file_name = time.strftime('logs/%Y%m%d_%H%M%S.csv',time.localtime(time.time()))#文件名是导出文件的完整文件名，包含扩展名

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
		time.sleep(0.3) # 休息一下，避免同一时刻几百个线程同时启动，下载js文件会阻塞导致失败
	for t in threads: # 这是上面的线程全部启动了，等待所有线程都结束
		t.join()

	file_object.close()

#第二步，根据终端的数量，生成VLAN仓库
	cnu_numbers = len(all_cnu_info_list)
	cnu_numbers_thousands = int(cnu_numbers/1000)+1 # 有几千个cnu，方便生成几千个VLAN

	start_pvid = 2000 # 点播VLAN直接减1000计算
	end_pvid   = 2009
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
		if temp_cnu['Cnu_pvid1'] == 1:  #如果当前cnu第一个FE网口没有设置pvid，则开始设置
			unset_cnu_count = unset_cnu_count + 1
			ip = temp_cnu['Eoc_ip']
			this_dev = RcEocHead(ip, 'xxxxxxxxx','xxxxxxxxxxx')
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
