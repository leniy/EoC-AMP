# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#更新日期：2015.02.14
#修订版本：第39次修订

import urllib2
import hashlib
import socket
import struct
import time
import wx
import re
import json
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from eocheadcommon import RcEocHeadCommon

#==================== 定义全局变量 ====================

mib_obj_enum = {}             #下面几个termEoC什么的,就是从这里面提取到的
running_mode = 'console'      #运行模式，判断当前是在console中还是在gui中运行
#termEocCnuIndex = ''          #Eoc终端设备Cnu的索引
#termEocCnuDevName = ''        #Cnu设备编号，例如“2/3”
#termEocCnuDevMac = ''         #Cnu的mac地址
#termEocCnuDevModel = ''       #Cnu的型号
#termEocCnuEtherVlanPVID = ''  #Cnu某个端口的pvid
#termEocCnuEtherPortOperStatus = '' #这个端口的状态：开启或关闭

#==================== 创建基本功能函数（函数默认为ip可以正常访问的情况，异常状态后续处理） ====================

def ip2int(ip): # str格式的ip，转换为int或long格式的数字
	return socket.htonl(struct.unpack('I', socket.inet_aton(ip))[0])

def int2ip(i): # int或long格式的数字，转换为str格式的ip
	return socket.inet_ntoa(struct.pack('I', socket.htonl(i)))

#函数功能：从list.csv中获取全部待配置头端的IP范围
#函数输入：无
#函数返回：包含全部ip的list
def getiplist():
	reip = re.compile(r"((?:\d+\.){3}\d+),((?:\d+\.){3}\d+)", re.DOTALL)
	listfile = open('list.csv')
	all_ip_region = []
	all_ip_list = []
	for line in listfile:
		all_ip_region.extend(reip.findall(line))
	listfile.close()
	for startip,endip in all_ip_region:
		for ip_num in range(ip2int(startip),ip2int(endip)+1):
			all_ip_list.append(int2ip(ip_num))
	return all_ip_list

#函数功能：保存配置信息
#函数输入：四个元素(str格式)
#函数返回：无
#def saveconfig(start_ip, end_ip, start_pvid, end_pvid):
#	configfile = open('config.txt','w+')
#	configfile.write(start_ip + "," + end_ip + "," + start_pvid + "," + end_pvid)
#	configfile.close()
#
#函数功能：读取配置信息
#函数输入：配置文件名称
#函数返回：四个元素(str格式)
#def getconfig(config_file = 'config.txt'):
#	try:
#		configfile = open(config_file)
#		configlist = configfile.readline()
#		configfile.close()
#		configlist = configlist.split(',')
#		start_ip   = configlist[0]
#		end_ip     = configlist[1]
#		start_pvid = configlist[2]
#		end_pvid   = configlist[3]
#	except:
#		saveconfig("2","120","2000","2999")
#		start_ip   = "2"
#		end_ip     = "120"
#		start_pvid = "2000"
#		end_pvid   = "2999"
#	return start_ip, end_ip, start_pvid, end_pvid
#

















#函数功能：自动检索全部头端及下属终端的信息，并配置vlan
#函数输入：runtype是gui模式还是console模式
#函数输出：无
def eoc_auto_main(runtype = "console"):
	#由于本部分功能与gui窗口属于不同的线程，为了防止冲突，配置信息直接从配置文件中获取
	#把所有的头端ip放到一个列表中
	all_ip_list = []
	all_ip_list.extend(getiplist())
	#把所有宽带VLAN放到一个列表中（点播VLAN直接减1000计算）
	start_pvid = 2000
	end_pvid   = 2999
	all_vlan_list = range(start_pvid,end_pvid + 1)

	all_head_info_list = [] #首先把全局列表清空
	unset_cnu_count = 0 #用来定义有多少个cnu设备尚未设置pvid

	output_csv_file_name = time.strftime('logs/%Y%m%d_%H%M%S.csv',time.localtime(time.time()))#文件名是导出文件的完整文件名，包含扩展名

	if runtype == "gui":
		rate = 0#程序进度的百分比
		#wx.CallAfter(Publisher().sendMessage, "update", rate)
		wx.CallAfter(pub.sendMessage, "update", msg = rate)

	file_object = open(output_csv_file_name, 'w+')
	s = '"Eoc Head IP","Cnu Index","Cnu Name","Cnu MAC","Cnu Modal","Cnu PVID1","Cnu PVID2","Cnu PVID3","Cnu PVID4"\n'
	print s
	file_object.write(s)

	for ip in all_ip_list:
		this_dev = RcEocHeadCommon(ip, 'x', 'x')
		if this_dev.device_is_up == False:
			continue
		temptemptemp = this_dev.get_allcnu_info()
		all_head_info_list.extend(temptemptemp)
		if runtype == "gui":
			#rate = 100.0 * ( ip_last - start_ip + 1 ) / ( end_ip - start_ip +1 )
			rate = 100.0 * ( all_ip_list.index(ip) ) / ( len(all_ip_list) )
			#print ip_last,start_ip,end_ip,( ip_last - start_ip + 1 ),( end_ip - start_ip +1 ),rate,int(rate)
			#wx.CallAfter(Publisher().sendMessage, "update", int(rate))
			wx.CallAfter(pub.sendMessage, "update", msg = int(rate))

		if len(temptemptemp) > 0:#当前ip至少有一个Cnu记录的时候
			for temp_list in temptemptemp:
				if temp_list['Cnu_pvid1'] == 1:
					unset_cnu_count += 1
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
			file_object.write('"' + ip + '","Can NOT open or has no device"\n')


	file_object.close()
	#print all_head_info_list

#	if runtype == "gui":
#		wx.MessageBox(u"搜索完成，共找到" + str(len(all_head_info_list)) + u"个设备\n\n其中，" + str(unset_cnu_count) + u"台设备尚未设置pvid",u"通知",wx.OK|wx.ICON_INFORMATION)


	#global all_head_info_list
	#global pvid_dict
	pvid_dict = {}

	for temp_vid in range(start_pvid, end_pvid + 1): #首先把全部pvid设置到字典，0表示尚未使用
		pvid_dict[temp_vid] = 0

	for temp_cnu in all_head_info_list: #把已经被使用的pvid，在字典中设置为-1，表示已经被使用过排除
		temp_pvid = temp_cnu['Cnu_pvid1']
		#print temp_pvid
		pvid_dict[temp_pvid] = -1
	#print pvid_dict

	pvid_notused_list = []
	for tempkey,tempvalue in pvid_dict.items(): #提取出来还没有被使用的pvid，并保存在list中
		if tempvalue == 0:
			pvid_notused_list.append(tempkey)
	pvid_notused_list.sort()

	#print pvid_notused_list

	#wx.MessageBox(u"危险功能，暂时只能在指定电脑上执行。\n\n需要在测试机器上经过大量试验后，才能开放",u"警告",wx.OK|wx.ICON_INFORMATION)

	#下面是自动设置代码，位于lib最后面的注释掉部分的代码。通过大量验证后，再复制过来

	for temp_cnu in all_head_info_list: #循环检测所有的cnu
		if temp_cnu['Cnu_pvid1'] == 1:  #如果当前cnu第一个FE网口没有设置pvid，则开始设置
			ip = temp_cnu['Eoc_ip']
			this_dev = RcEocHeadCommon(ip, 'xxxxxxxxx','xxxxxxxxxxx')
			if this_dev.device_is_up == False:
				continue
			cnuindex = temp_cnu['Cnu_index'] #cnu的索引
			port_index1 = 100000 + cnuindex + 1 #4个FE端口的索引。因为暂时没有开通其他服务，所以4个端口设置同样的pvid
			port_index2 = 100000 + cnuindex + 2
			port_index3 = 100000 + cnuindex + 3
			port_index4 = 100000 + cnuindex + 4
			temppvid = pvid_notused_list[0] #pvid设置为第一个尚未使用的值
			pvid_notused_list = pvid_notused_list[1:] #把第一个从未使用的列表中去掉
			this_dev.set_port_pvid(str(port_index1),str(temppvid))
			print "set a pvid " + str(temppvid) + " in " + str(ip)
			this_dev.set_port_pvid(str(port_index2),str(temppvid - 1000))  #1000为点播的vlan
			this_dev.set_port_pvid(str(port_index3),str(1))     #1为未配置时的默认值，此时端口暂不开启
			this_dev.set_port_pvid(str(port_index4),str(1))     #1为未配置时的默认值，此时端口暂不开启
			#print ip + ", " + temp_cnu['Cnu_name'] + "   pvid: " + str(temppvid)
	if runtype == "gui":
		wx.MessageBox(u"搜索完成，共找到" + str(len(all_head_info_list)) + u"个设备\n\n其中，" + str(unset_cnu_count) + u"台未配置，现已配置完成",u"通知",wx.OK|wx.ICON_INFORMATION)
#		wx.MessageBox(u"pvid设置成功",u"通知",wx.OK|wx.ICON_INFORMATION)
		#wx.CallAfter(Publisher().sendMessage, "update", u"完成")
		wx.CallAfter(pub.sendMessage, "update", msg = u"完成")
