# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#更新日期：2014.07.29
#修订版本：第32次修订

import urllib2
import hashlib
import socket
import time
import wx
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
#from wx.lib.pubsub import Publisher #用这条命令会导致py2exe生成的程序报错
#from wx.lib.pubsub import setuparg1  #换成这个后，需要把代码中的Publisher()换成Publisher


#==================== 定义全局变量 ====================

termEocCnuIndex = ''          #Eoc终端设备Cnu的索引
termEocCnuDevName = ''        #Cnu设备编号，例如“2/3”
termEocCnuDevMac = ''         #Cnu的mac地址
termEocCnuDevModel = ''       #Cnu的型号
termEocCnuEtherVlanPVID = ''  #Cnu某个端口的pvid
running_mode = 'console'      #运行模式，判断当前是在console中还是在gui中运行

#==================== 创建基本功能函数（函数默认为ip可以正常访问的情况，异常状态后续处理） ====================

#函数功能：保存配置信息
#函数输入：四个元素(str格式)
#函数返回：无
def saveconfig(start_ip, end_ip, start_pvid, end_pvid):
	configfile = open('config.txt','w+')
	configfile.write(start_ip + "," + end_ip + "," + start_pvid + "," + end_pvid)
	configfile.close()



#函数功能：读取配置信息
#函数输入：无
#函数返回：四个元素(str格式)
def getconfig():
	try:
		configfile = open('config.txt')
		configlist = configfile.readline()
		configfile.close()
		configlist = configlist.split(',')
		start_ip   = configlist[0]
		end_ip     = configlist[1]
		start_pvid = configlist[2]
		end_pvid   = configlist[3]
	except:
		saveconfig("50","151","2000","2499")
		start_ip   = "50"
		end_ip     = "151"
		start_pvid = "2000"
		end_pvid   = "2499"
	return start_ip, end_ip, start_pvid, end_pvid



#函数功能：登陆函数（默认ip可以正常访问）
#函数输入：ip、用户名、密码
#函数返回：cookies、错误代码（出错时，cookies是一个包含错误原因的字符串）
def logineoc(ip, user, password):
	#设置cookie保存登录状态
	cookies = urllib2.HTTPCookieProcessor()
	opener = urllib2.build_opener(cookies)
	urllib2.socket.setdefaulttimeout(3)  #设置超时为2秒
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
		termEocCnuIndex         = str(response['termEocCnuIndex'])
		termEocCnuDevName       = str(response['termEocCnuDevName'])
		termEocCnuDevMac        = str(response['termEocCnuDevMac'])
		termEocCnuDevModel      = str(response['termEocCnuDevModel'])
		termEocCnuEtherVlanPVID = str(response['termEocCnuEtherVlanPVID'])
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
		#首先把json的空值符号换成python的空值符号
		response = response.replace('\/','/')
		#然后替换转义符
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

	cookies,errorcode1 = logineoc(ip,'xxxxxxxxx','xxxxxxxxxxx')  #如果登陆出错，返回错误代码，并打印错误原因
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
	get_dev_unique_number(ip,cookies) #因为获取全部ip的cnu列表的时候，这些设备独立编码已经被覆盖了，所以设置pvid的时候要重新设置一次并保存回全局变量中
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


#函数功能：自动检索全部头端及下属终端的信息，并配置vlan
#函数输入：runtype是gui模式还是console模式
#函数输出：无
def eoc_auto_main(runtype = "console"):
	#由于本部分功能与gui窗口属于不同的线程，为了防止冲突，配置信息直接从配置文件中获取
	start_ip, end_ip, start_pvid, end_pvid = getconfig()
	start_ip   = int(start_ip)
	end_ip     = int(end_ip)
	start_pvid = int(start_pvid)
	end_pvid   = int(end_pvid)


	#global all_head_info_list
	#global unset_cnu_count
	all_head_info_list = [] #首先把全局列表清空
	unset_cnu_count = 0 #用来定义有多少个cnu设备尚未设置pvid

	output_csv_file_name = time.strftime('logs/%Y%m%d_%H%M%S.csv',time.localtime(time.time()))#文件名是导出文件的完整文件名，包含扩展名

	#wx.MessageBox(u"开始搜索，界面可能处于假死状态，请耐心等待。\n\n执行完成后，数据将保存在csv文件中",u"警告",wx.OK|wx.ICON_INFORMATION)

	if runtype == "gui":
		rate = 0#程序进度的百分比
		#wx.CallAfter(Publisher().sendMessage, "update", rate)
		wx.CallAfter(pub.sendMessage, "update", msg = rate)

	file_object = open(output_csv_file_name, 'w+')
	s = '"Eoc Head IP","Cnu Index","Cnu Name","Cnu MAC","Cnu Modal","Cnu PVID1","Cnu PVID2","Cnu PVID3","Cnu PVID4"\n'
	print s
	file_object.write(s)
                
	for ip_last in range(start_ip,end_ip + 1):
		ip = 'x.x.x.' + str(ip_last)
		temptemptemp = show_eochead_info(ip)
		all_head_info_list.extend(temptemptemp)
		if runtype == "gui":
			rate = 100.0 * ( ip_last - start_ip + 1 ) / ( end_ip - start_ip +1 )
			print ip_last,start_ip,end_ip,( ip_last - start_ip + 1 ),( end_ip - start_ip +1 ),rate,int(rate)
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

	if runtype == "gui":
		wx.MessageBox(u"搜索完成，共找到" + str(len(all_head_info_list)) + u"个设备\n\n其中，" + str(unset_cnu_count) + u"台设备尚未设置pvid",u"通知",wx.OK|wx.ICON_INFORMATION)


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
			cookies,errorcode1 = logineoc(ip,'xxxxxxxxx','xxxxxxxxxxx')
			if errorcode1 == 0: #重新登陆一次，并获取cookies
				cnuindex = temp_cnu['Cnu_index'] #cnu的索引
				port_index1 = 100000 + cnuindex + 1 #4个FE端口的索引。因为暂时没有开通其他服务，所以4个端口设置同样的pvid
				port_index2 = 100000 + cnuindex + 2
				port_index3 = 100000 + cnuindex + 3
				port_index4 = 100000 + cnuindex + 4
				temppvid = pvid_notused_list[0] #pvid设置为第一个尚未使用的值
				pvid_notused_list = pvid_notused_list[1:] #把第一个从未使用的列表中去掉
				set_port_pvid(ip,cookies,str(port_index1),str(temppvid))
				set_port_pvid(ip,cookies,str(port_index2),str(1000))  #1000为点播的vlan
				set_port_pvid(ip,cookies,str(port_index3),str(1))     #1为未配置时的默认值，此时端口暂不开启
				set_port_pvid(ip,cookies,str(port_index4),str(1))     #1为未配置时的默认值，此时端口暂不开启
				#print ip + ", " + temp_cnu['Cnu_name'] + "   pvid: " + str(temppvid)
	if runtype == "gui":
		wx.MessageBox(u"pvid设置成功",u"通知",wx.OK|wx.ICON_INFORMATION)
		#wx.CallAfter(Publisher().sendMessage, "update", u"完成")
		wx.CallAfter(pub.sendMessage, "update", msg = u"完成")
