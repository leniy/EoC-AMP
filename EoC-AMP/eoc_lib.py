# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
'''1111

'''

import urllib2
import hashlib
import socket
import time


#==================== 定义全局变量 ====================

termEocCnuIndex = ''          #Eoc终端设备Cnu的索引
termEocCnuDevName = ''        #Cnu设备编号，例如“2/3”
termEocCnuDevMac = ''         #Cnu的mac地址
termEocCnuDevModel = ''       #Cnu的型号
termEocCnuEtherVlanPVID = ''  #Cnu某个端口的pvid


#==================== 创建基本功能函数（函数默认为ip可以正常访问的情况，异常状态后续处理） ====================

#函数功能：登陆函数（默认ip可以正常访问）
#函数输入：ip、用户名、密码
#函数返回：cookies、错误代码（出错时，cookies是一个包含错误原因的字符串）
def logineoc(ip, user, password):
	#设置cookie保存登录状态
	cookies = urllib2.HTTPCookieProcessor()
	opener = urllib2.build_opener(cookies)
	urllib2.socket.setdefaulttimeout(5)  #设置超时为5秒
	#首先登陆账号，并设置cookie
	request = urllib2.Request(
		url	 = 'http://' + ip + '/index.html',
		headers = {
			'Content-Type' : 'application/x-www-form-urlencoded',
			'Referer' : 'http://' + ip + '/login.html'
		},
		data	= 'username=' + user + '&password=' + hashlib.md5(password).hexdigest() + '&language=en&x=38&y=16',
	)

	try:
		response = opener.open(request)
		return cookies,0
	except:
		print 'Error: ' + ip + ' Login Failure'
		return 'cookies_error',-1



#函数功能：获取设备中各个参数的唯一编号
#函数输入：ip、cookies
#函数返回：错误代码（编号值直接赋值给全局变量，不用返回）
def get_dev_unique_number(ip, cookies):
	#Eoc头端中，各个项目采用数字表示，这儿对其意义进行定义
	global termEocCnuIndex
	global termEocCnuDevName
	global termEocCnuDevMac
	global termEocCnuDevModel
	global termEocCnuEtherVlanPVID

	opener = urllib2.build_opener(cookies)
	request = urllib2.Request(
		url	 = 'http://' + ip + '/js/mib_obj_enum.js',
	)
	try:
		response = opener.open(request)
		response = response.read()
		response = response.replace('window.top.__mib_oids = ','')
		response = response.replace(';','')
		response = eval(response)
		termEocCnuIndex                     = str(response['termEocCnuIndex'])
		termEocCnuDevName                   = str(response['termEocCnuDevName'])
		termEocCnuDevMac                    = str(response['termEocCnuDevMac'])
		termEocCnuDevModel                  = str(response['termEocCnuDevModel'])
		termEocCnuEtherVlanPVID             = str(response['termEocCnuEtherVlanPVID'])
		return 0
	except:
		print 'Error: ' + ip + ' mib_obj_enum.js can NOT be downloaded'
		return -1


#函数功能：获取设备列表函数（默认ip可以正常访问）
#函数输入：ip、cookies
#函数返回：dict格式的cnu_devlist列表、错误代码（出错时，第一个返回值是一个包含错误原因的字符串）
def get_cnu_devlist(ip, cookies):
	global termEocCnuIndex
	global termEocCnuDevName
	global termEocCnuDevMac
	global termEocCnuDevModel
	get_cnu_devlist_poststr = termEocCnuIndex + ';' + termEocCnuDevName + ';' + termEocCnuDevMac + ';' + termEocCnuDevModel

	opener = urllib2.build_opener(cookies)
	request = urllib2.Request(
		url	 = 'http://' + ip + '/g',
		headers = {
			'Content-Type' : 'application/x-www-form-urlencoded',
			'Referer' : 'http://' + ip + '/cnu_devlist.html',
		},
		data	= 'entry=a:0:0;' + get_cnu_devlist_poststr
	)
	try:
		response = opener.open(request)
		response = response.read()
		#print response
		response = response.replace('null','None')
		response = response.replace('\/','/')
		cnu_ajax_devlist = eval(response)
		if cnu_ajax_devlist['errcode'] == 0:
			cnu_devlist = cnu_ajax_devlist['entry']
			return cnu_devlist,0
		elif cnu_ajax_devlist['errcode'] == -1:
			tempstr = cnu_ajax_devlist['errinfo']
			print 'errinfo: ' + tempstr
			return tempstr,-1
	except:
		print 'Error: ' + ip + ' can NOT get list'
		return 'get_cnu_devlist_error',-1


#函数功能：获取某终端单个端口的pvid（默认ip可以正常访问）
#函数输入：ip、cookies、port_index
#函数返回：int格式的pvid（不必返回错误代码。pvid > 1 为正常设置，pvid = 1 为尚未设置，pvid = -9999 为系统返回错误）
def get_port_pvid(ip, cookies, port_index):
	global termEocCnuEtherVlanPVID
	get_port_pvid_poststr = termEocCnuEtherVlanPVID

	opener = urllib2.build_opener(cookies)
	request = urllib2.Request(
		url	 = 'http://' + ip + '/g',
		headers = {
			'Content-Type' : 'application/x-www-form-urlencoded',
			'Referer' : 'http://' + ip + '/cnu_port_config.html',
		},
		data	= 'entry=g:' + port_index + ':0;' + get_port_pvid_poststr
	)
	#port_index设置原理：
	#终端设备共有5个端口，分别为1个Cable、4个FE
	#end_index定义为：某头端中，各个终端设备的索引
	#port_index定义为：某终端设备中，各个端口的索引
	#如果end_index为16512
	#则这五个端口的port_index分别为16512+6000001、16512+100001、16512+100002、16512+100003、16512+100004
	#FE的pvid，就是给设备设置的vlan。
	try:
		response = opener.open(request)
		response = response.read()
		#print response
		response = response.replace('null','None')
		cnu_ajax_portconfig = eval(response)
		#print cnu_ajax_portconfig
		if cnu_ajax_portconfig['errcode'] == 0:
			cnu_portconfig = cnu_ajax_portconfig['entry']
			pvid = cnu_portconfig[0][termEocCnuEtherVlanPVID]
			return pvid
		elif cnu_ajax_portconfig['errcode'] == -1:
			#tempstr = cnu_ajax_portconfig['errinfo']
			return -9999
	except:
		print 'Error: ' + ip + ' get port pvid error'
		return -9999


#函数功能：列出某头端的全部信息（默认ip可以正常访问）
#函数输入：字符串格式的ip
#函数返回：单个头端Eoc中，所有Cnu的信息的列表head_info_list（单个Cnu的信息，以dict格式存储于list中）
def show_eochead_info(ip):
	global termEocCnuIndex
	global termEocCnuDevName
	global termEocCnuDevMac
	global termEocCnuDevModel
	#global termEocCnuEtherVlanPVID

	cookies,errorcode1 = logineoc(ip,'admin','admin')  #如果登陆出错，返回错误代码，并打印错误原因
	if errorcode1 == 0:  #如果成功登陆，再继续执行下面的代码
		get_dev_unique_number(ip,cookies)
		cnu_devlist,errorcode2 = get_cnu_devlist(ip,cookies)  #如果获取列表失败，返回错误代码，并打印错误原因
		if errorcode2 == 0:  #如果列表成功获取，再继续执行下面的代码
			#head_info_str  = ''
			head_info_list = []
			#head_info_str += '在Eoc头端' + ip + '中，共发现' + str(len(cnu_devlist)) + '台设备：\n'
			#head_info_str += '"头端ip","唯一编号","终端设备号","终端MAC","终端型号","终端PVID1","终端PVID2","终端PVID3","终端PVID4"\n'
			#根据设备列表，进行for循环
			for cnu_dev in cnu_devlist:

				Eoc_ip    = ip
				Cnu_index = cnu_dev[termEocCnuIndex]  #注意，这个是int格式的数字
				Cnu_name  = 'Cnu ' + cnu_dev[termEocCnuDevName]
				Cnu_mac   = cnu_dev[termEocCnuDevMac]
				Cnu_model = cnu_dev[termEocCnuDevModel]

				port_index1 = str(100000 + Cnu_index + 1)  #获取第一个FE端口的索引号
				port_index2 = str(100000 + Cnu_index + 2)  #获取第一个FE端口的索引号
				port_index3 = str(100000 + Cnu_index + 3)  #获取第一个FE端口的索引号
				port_index4 = str(100000 + Cnu_index + 4)  #获取第一个FE端口的索引号

				Cnu_pvid1 = get_port_pvid(ip,cookies,port_index1)  #注意，这个是int格式的数字
				Cnu_pvid2 = get_port_pvid(ip,cookies,port_index2)  #注意，这个是int格式的数字
				Cnu_pvid3 = get_port_pvid(ip,cookies,port_index3)  #注意，这个是int格式的数字
				Cnu_pvid4 = get_port_pvid(ip,cookies,port_index4)  #注意，这个是int格式的数字

				#head_info_str += '"' + Eoc_ip         + '",'
				#head_info_str += '"' + str(Cnu_index) + '",'
				#head_info_str += '"' + Cnu_name       + '",'
				#head_info_str += '"' + Cnu_mac        + '",'
				#head_info_str += '"' + Cnu_model      + '",'
				#head_info_str += '"' + str(Cnu_pvid1) + '",'
				#head_info_str += '"' + str(Cnu_pvid2) + '",'
				#head_info_str += '"' + str(Cnu_pvid3) + '",'
				#head_info_str += '"' + str(Cnu_pvid4) + '"\n'

				templist = [{
					"Eoc_ip"    : Eoc_ip,
					"Cnu_index" : Cnu_index,
					"Cnu_name"  : Cnu_name,
					"Cnu_mac"   : Cnu_mac,
					"Cnu_model" : Cnu_model,
					"Cnu_pvid1" : Cnu_pvid1,
					"Cnu_pvid2" : Cnu_pvid2,
					"Cnu_pvid3" : Cnu_pvid3,
					"Cnu_pvid4" : Cnu_pvid4
					}]
				head_info_list.extend(templist)
			if type(head_info_list) == list:
				return head_info_list
			else:
				return []
		else:
			return []
	else:
		return []


#函数功能：设置某终端单个端口的pvid（默认ip可以正常访问）
#函数输入：ip、cookies、port_index（str格式）、pvid（str格式）
#函数返回：int格式的错误代码
def set_port_pvid(ip, cookies, port_index, pvid):
	global termEocCnuEtherVlanPVID
	set_port_pvid_poststr = termEocCnuEtherVlanPVID + '.' + port_index + '=' + pvid
	#print set_port_pvid_poststr

	opener = urllib2.build_opener(cookies)
	request = urllib2.Request(
		url	 = 'http://' + ip + '/s',
		headers = {
			'Content-Type' : 'application/x-www-form-urlencoded',
			'Referer' : 'http://' + ip + '/cnu_port_config.html',
		},
		data	= set_port_pvid_poststr
	)
	try:
		response = opener.open(request)
		response = response.read()
		#print response
		response = eval(response)
		return response['errcode']
	except:
		print 'Error: ' + ip + ' set port pvid error'
		return -1


###################################
# 下面是测试设置vlan的代码

#cookies,errorcode1 = logineoc('x.x.x.70','admin','admin')
#get_dev_unique_number('x.x.x.70',cookies)
#cnu_devlist,errorcode2 = get_cnu_devlist('x.x.x.70',cookies)
#test_cnu = cnu_devlist[2]
#print test_cnu
#test_index = test_cnu[termEocCnuIndex]
#test_port_index1 = test_index + 100000 + 1
#test_port_index2 = test_index + 100000 + 2
#test_port_index3 = test_index + 100000 + 3
#test_port_index4 = test_index + 100000 + 4
#print set_port_pvid('x.x.x.70',cookies,str(test_port_index1),str(2155))
#print set_port_pvid('x.x.x.70',cookies,str(test_port_index2),str(2155))
#print set_port_pvid('x.x.x.70',cookies,str(test_port_index3),str(2155))
#print set_port_pvid('x.x.x.70',cookies,str(test_port_index4),str(2155))
#cnu_devlist,errorcode2 = get_cnu_devlist('x.x.x.70',cookies)
#test_cnu = cnu_devlist[2]
#print test_cnu
