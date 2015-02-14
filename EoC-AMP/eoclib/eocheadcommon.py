# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#更新日期：2015.02.17
#修订版本：第40次修订

import urllib2
import hashlib
import socket
import json

class RcEocHeadCommon(object): # 处理Raisecom公司的EoC头端的通用类
	def __init__(self, ip, username, password): # 参数为头端的ip地址
		self.ip           = ip
		self.username     = username
		self.password     = password
		self.cookies      = None
		self.mib_obj_enum = None # 头端各个参数的mib值
		self.device_is_up = True # 标记设备是否正常（能登陆且可获取mib，才算正常）
		self.device_down_reason = 'device is OK' # 登记设备异常原因
		if self.device_is_up:
			self.login()
		#if self.device_is_up:
		self.get_mib_obj_enum()

	def login(self):
		if not self.cookies: # 只需要获取一次
			self.cookies = urllib2.HTTPCookieProcessor()
			opener = urllib2.build_opener(self.cookies)
			urllib2.socket.setdefaulttimeout(3)  #设置超时为3秒
			request = urllib2.Request(
				url = 'http://%s/index.html' % (self.ip),
				headers = {'Content-Type' : 'application/x-www-form-urlencoded', 'Referer' : 'http://%s/login.html' % (self.ip)},
				data = 'username=%s&password=%s&language=en&x=38&y=16' % (self.username, hashlib.md5(self.password).hexdigest()),
			)
		
			try:
				response = opener.open(request)
				self.device_is_up = True
			except:
				try: # 再试一次，刚刚有可能网络堵塞
					response = opener.open(request)
					self.device_is_up = True
				except:
					self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
					self.device_down_reason = 'Error: %s Login Failure' % (self.ip)
					print self.device_down_reason

	def get_mib_obj_enum(self):
		if not self.device_is_up:#如果设备是down的，本函数直接跳出
			return
		opener = urllib2.build_opener(self.cookies)
		request = urllib2.Request( url = 'http://%s/js/mib_obj_enum.js' % (self.ip) )
		try:
			response = opener.open(request)
			response = response.read()
			response = response.replace('window.top.__mib_oids = ','')
			response = response.replace(';','')
			self.mib_obj_enum = json.JSONDecoder().decode(response)
		except:
			self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
			self.device_down_reason = 'Error: %s mib_obj_enum.js can NOT be downloaded' % (self.ip)
			print self.device_down_reason

	@property
	def dev_time(self): # 获取设备的系统时间(十六进制)
		default_time = '07 b2 01 01 08 00 00 00 2b 08 00' # 无法获取时间时，返回这个1970-01-01 08:00:00.00 +08:00
		if not self.device_is_up:#如果设备是down的，直接返回默认时间，后面的代码不执行
			return default_time
		opener = urllib2.build_opener(self.cookies)
		request = urllib2.Request(
			url = 'http://%s/g' % (self.ip),
			headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Referer' : 'http://%s/sys_timemng.html' % (self.ip) },
			data = 'scalar=%s' % (self.mib_obj_enum['raisecomClockDateAndTime'])
		)
		try:
			response = opener.open(request)
			response = response.read()
			response = json.JSONDecoder().decode(response)
			if response['errcode'] == 0:
				temptime = response[str(self.mib_obj_enum['raisecomClockDateAndTime'])]
				return temptime
			elif response['errcode'] == -1:
				tempstr = 'GetDevTime Error: %s' % (response['errinfo'])
				print tempstr
				return default_time
		except:
			self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
			self.device_down_reason = 'Error: %s can NOT get dateandtime' % (self.ip)
			print self.device_down_reason
			return default_time

	@property
	def cable_freqinfo(self): # 获取Cable频段信息(固定衰减使能，固定衰减值)
		if not self.device_is_up:#如果设备是down的，后面的代码不执行
			return (-9999,-9999)
		opener = urllib2.build_opener(self.cookies)
		request = urllib2.Request(
			url = 'http://%s/g' % (self.ip),
			headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Referer' : 'http://%s//eoc_cable_freqinfo.html' % (self.ip) },
			data = 'entry=a:0:0;%s;%s' % (self.mib_obj_enum['termEocPMDCbatCablePortPowerFixAttenEnable'], self.mib_obj_enum['termEocPMDCbatCablePortPowerFixAtten'])
		)

		try:
			response = opener.open(request)
			response = response.read()
			response = json.JSONDecoder().decode(response)
			if response['errcode'] == 0:
				responsetemp = response['entry'][0]
				return responsetemp[str(self.mib_obj_enum['termEocPMDCbatCablePortPowerFixAttenEnable'])],responsetemp[str(self.mib_obj_enum['termEocPMDCbatCablePortPowerFixAtten'])]
			elif response['errcode'] == -1:
				tempstr = 'errinfo: ' + response['errinfo']
				print tempstr
				return tempstr
		except:
			self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
			self.device_down_reason = 'Error: %s can NOT get cable_freqinfo' % (self.ip)
			print self.device_down_reason
			return self.device_down_reason

	def set_cable_freqinfo_FixAtten(self, attenenable, fixatten): # 使能并设置头端Cable的固定衰减值为FixAtten(cable低频信号过强，会影响高频部分数字电视的误码率)
		#attenenable=1为使能，attenenable=2为禁止
		if not self.device_is_up:#如果设备是down的，后面的代码不执行
			print  'Device %s is down, set cable freqinfo FixAtten ERROR' % (self.ip)
			return 'Device %s is down, set cable freqinfo FixAtten ERROR' % (self.ip)
		opener = urllib2.build_opener(self.cookies)
		request = urllib2.Request(
			url = 'http://%s/s' % (self.ip),
			headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Referer' : 'http://%s//eoc_cable_freqinfo.html' % (self.ip) },
			data = '%s.6000001=%s&%s.6000001=%s' % (self.mib_obj_enum['termEocPMDCbatCablePortPowerFixAttenEnable'], attenenable, self.mib_obj_enum['termEocPMDCbatCablePortPowerFixAtten'], fixatten)
		)

		try:
			response = opener.open(request)
			response = response.read()
			response = json.JSONDecoder().decode(response)
			if response['errcode'] == 0:
				return True
			elif response['errcode'] == -1:
				tempstr = 'errinfo: ' + response['errinfo']
				return False
		except:
			self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
			self.device_down_reason = 'Error: %s can NOT set cable_freqinfo' % (self.ip)
			print self.device_down_reason
			return self.device_down_reason

	def get_cnu_devlist(self): # 获取EoC头端下挂CNU终端的列表
		#函数返回：列表，其中每项都是一个dict
		if not self.device_is_up:#如果设备是down的，后面的代码不执行，返回一个空列表
			return []
		opener = urllib2.build_opener(self.cookies)
		request = urllib2.Request(
			url = 'http://%s/g' % (self.ip),
			headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Referer' : 'http://%s/cnu_devlist.html' % (self.ip) },
			data = 'entry=a:0:0;%s;%s;%s;%s' % (self.mib_obj_enum['termEocCnuIndex'], self.mib_obj_enum['termEocCnuDevName'], self.mib_obj_enum['termEocCnuDevMac'], self.mib_obj_enum['termEocCnuDevModel'])
		)
		try:
			response = opener.open(request)
			response = response.read()
			response = json.JSONDecoder().decode(response)
			if response['errcode'] == 0:
				cnu_devlist = response['entry']
				return cnu_devlist
			elif response['errcode'] == -1:
				tempstr = response['errinfo']
				print 'errinfo: ' + tempstr
				return [] # 返回一个空表
		except:
			self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
			self.device_down_reason = 'Error: %s can NOT get cnu_list' % (self.ip)
			print self.device_down_reason
			return [] # 返回一个空表

	def get_port_pvid(self, port_index): # 获取某终端单个端口的pvid
		#函数返回：int格式的pvid（pvid > 1 为正常设置，pvid = 1 为尚未设置，pvid = -9999 为系统返回错误）

		if not self.device_is_up:#如果设备是down的，后面的代码不执行，返回一个-9999
			return -9999

		#port_index设置原理：
		#终端设备共有5个端口，分别为1个Cable、4个FE
		#end_index定义为：某头端中，各个终端设备的索引
		#port_index定义为：某终端设备中，各个端口的索引
		#如果end_index为16512
		#则这五个端口的port_index分别为16512+6000001、16512+100001、16512+100002、16512+100003、16512+100004
		#FE的pvid，就是给设备设置的vlan。

		opener = urllib2.build_opener(self.cookies)
		request = urllib2.Request(
			url = 'http://%s/g' % (self.ip),
			headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Referer' : 'http://%s/cnu_port_config.html' % (self.ip) },
			data = 'entry=g:%s:0;%s' % (port_index, self.mib_obj_enum['termEocCnuEtherVlanPVID'])
		)
		try:
			response = opener.open(request)
			response = response.read()
			response = json.JSONDecoder().decode(response)
			if response['errcode'] == 0:
				cnu_portconfig = response['entry'][0]
				pvid = cnu_portconfig[str(self.mib_obj_enum['termEocCnuEtherVlanPVID'])]
				return pvid
			elif response['errcode'] == -1:
				#tempstr = response['errinfo']
				return -9999
		except:
			self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
			self.device_down_reason = 'Error: %s get port pvid error' % (self.ip)
			print self.device_down_reason
			return -9999

	def set_port_pvid(self, port_index, pvid): # 设置某终端某个端口的pvid
		if not self.device_is_up:#如果设备是down的，后面的代码不执行
			print  'Device %s is down, set port %s pvid %s ERROR' % (self.ip, port_index, pvid)
			return 'Device %s is down, set port %s pvid %s ERROR' % (self.ip, port_index, pvid)

		opener = urllib2.build_opener(self.cookies)
		request = urllib2.Request(
			url = 'http://%s/s' % (self.ip),
			headers = { 'Content-Type' : 'application/x-www-form-urlencoded', 'Referer' : 'http://%s/cnu_port_config.html' % (self.ip) },
			data = '%s.%s=%s' % (self.mib_obj_enum['termEocCnuEtherVlanPVID'], port_index, pvid)
		)
		try:
			response = opener.open(request)
			response = response.read()
			response = json.JSONDecoder().decode(response)
			return response['errcode']
		except:
			self.device_is_up = False # request失败，说明此时设备挂掉或者帐号别处登录了，则认为设备的DOWN的
			self.device_down_reason = 'Error: %s set port pvid error' % (self.ip)
			print self.device_down_reason
			return -1

	def get_allcnu_info(self): # 显示当前头端下面所有终端的信息（含终端各个FE口的pvid信息）
		if not self.device_is_up:#如果设备是down的，后面的代码不执行，直接返回空列表
			return []

		allcnu_info_list = []
		#函数返回：allcnu_info_list列表，每个元素是一个cnu，每个cnu用dict存储各个信息

		cnu_devlist = self.get_cnu_devlist()
		for cnu_dev in cnu_devlist:
			Eoc_ip    = self.ip

			Cnu_index = cnu_dev[str(self.mib_obj_enum['termEocCnuIndex'])]  #注意，这个是int格式的数字
			Cnu_name  = 'Cnu ' + cnu_dev[str(self.mib_obj_enum['termEocCnuDevName'])]
			Cnu_mac   = cnu_dev[str(self.mib_obj_enum['termEocCnuDevMac'])]
			Cnu_model = cnu_dev[str(self.mib_obj_enum['termEocCnuDevModel'])]

			port_index1 = 100000 + Cnu_index + 1  #获取第一个FE端口的索引号
			port_index2 = 100000 + Cnu_index + 2  #获取第二个FE端口的索引号
			port_index3 = 100000 + Cnu_index + 3  #获取第三个FE端口的索引号
			port_index4 = 100000 + Cnu_index + 4  #获取第四个FE端口的索引号

			Cnu_pvid1 = self.get_port_pvid(port_index1)  #注意，这个是int格式的数字
			Cnu_pvid2 = self.get_port_pvid(port_index2)  #注意，这个是int格式的数字
			Cnu_pvid3 = self.get_port_pvid(port_index3)  #注意，这个是int格式的数字
			Cnu_pvid4 = self.get_port_pvid(port_index4)  #注意，这个是int格式的数字

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
			allcnu_info_list.extend(templist)
		if type(allcnu_info_list) == list:
			return allcnu_info_list
		else:
			return []
