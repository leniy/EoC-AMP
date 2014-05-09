# -*- coding: UTF-8 -*-
#作者：Leniy

import wx
import eoc_gui
import eoc_lib
import time

# 定义全局变量
all_head_info_list = []
pvid_dict = {}
unset_cnu_count = 0

#创建新的类MainGUI，继承自eoc_gui库。同时定义点击按钮时执行的代码
class MainGUI ( eoc_gui.MainFrame ):
	def search( self, event ):
		global all_head_info_list
		global unset_cnu_count
		all_head_info_list = [] #首先把全局列表清空
		unset_cnu_count = 0 #用来定义有多少个cnu设备尚未设置pvid

		output_csv_file_name = time.strftime('%Y%m%d_%H%M%S.csv',time.localtime(time.time()))#文件名是导出文件的完整文件名，包含扩展名
		start_ip      = int(self.StartIP.GetValue())#int格式的数字有效范围0-255，是ip格式A.B.C.D中的最后一位D
		end_ip        = int(self.EndIP.GetValue())

		wx.MessageBox(u"开始搜索，界面可能处于假死状态，请耐心等待。\n\n执行完成后，数据将保存在csv文件中",u"警告",wx.OK|wx.ICON_INFORMATION)

		file_object = open(output_csv_file_name, 'w+')
		s = '"Eoc Head IP","Cnu Index","Cnu Name","Cnu MAC","Cnu Modal","Cnu PVID1","Cnu PVID2","Cnu PVID3","Cnu PVID4"\n'
		print s
		file_object.write(s)


		for ip_last in range(start_ip,end_ip + 1):
			ip = 'x.x.x.' + str(ip_last)
			temptemptemp = eoc_lib.show_eochead_info(ip)
			all_head_info_list.extend(temptemptemp)

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
		print all_head_info_list

		wx.MessageBox(u"搜索完成，共找到" + str(len(all_head_info_list)) + u"个设备\n\n其中，" + str(unset_cnu_count) + u"台设备尚未设置pvid",u"通知",wx.OK|wx.ICON_INFORMATION)


	def setpvid( self, event ):
		global all_head_info_list
		global pvid_dict
		pvid_dict = {}

		start_pvid = int(self.StartPVID.GetValue()) #获取起始pvid值
		end_pvid   = int(self.EndPVID.GetValue())   #获取终止pvid值，后续自动设置pvid时，将从这个范围中选取未用过的pvid设置
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

		wx.MessageBox(u"危险功能，暂时只能在指定电脑上执行。\n\n需要在测试机器上经过大量试验后，才能开放",u"警告",wx.OK|wx.ICON_INFORMATION)

		#下面是自动设置代码，位于lib最后面的注释掉部分的代码。通过大量验证后，再复制过来

		for temp_cnu in all_head_info_list: #循环检测所有的cnu
			if temp_cnu['Cnu_pvid1'] == 1:  #如果当前cnu第一个FE网口没有设置pvid，则开始设置
				ip = temp_cnu['Eoc_ip']
				cookies,errorcode1 = eoc_lib.logineoc(ip,'xxxxxxxxxx','xxxxxxxxxxxxxxxx')
				if errorcode1 == 0: #重新登陆一次，并获取cookies
					cnuindex = temp_cnu['Cnu_index'] #cnu的索引
					port_index1 = 100000 + cnuindex + 1 #4个FE端口的索引。因为暂时没有开通其他服务，所以4个端口设置同样的pvid
					port_index2 = 100000 + cnuindex + 2
					port_index3 = 100000 + cnuindex + 3
					port_index4 = 100000 + cnuindex + 4
					temppvid = pvid_notused_list[0] #pvid设置为第一个尚未使用的值
					pvid_notused_list = pvid_notused_list[1:] #把第一个从未使用的列表中去掉
					eoc_lib.set_port_pvid(ip,cookies,str(port_index1),str(temppvid))
					eoc_lib.set_port_pvid(ip,cookies,str(port_index2),str(temppvid))
					eoc_lib.set_port_pvid(ip,cookies,str(port_index3),str(temppvid))
					eoc_lib.set_port_pvid(ip,cookies,str(port_index4),str(temppvid))
					print ip + ", " + temp_cnu['Cnu_name'] + "   pvid: " + str(temppvid)
		wx.MessageBox(u"pvid设置成功",u"通知",wx.OK|wx.ICON_INFORMATION)


app = wx.App()
gui = MainGUI(None)
gui.Show()
app.MainLoop()



