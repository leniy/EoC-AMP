#!/usr/bin/python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#修订信息参考__init__.py文件

import socket
import struct
import re

#==================== 定义全局变量 ====================

#mib_obj_enum = {}             #下面几个termEoC什么的,就是从这里面提取到的
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


