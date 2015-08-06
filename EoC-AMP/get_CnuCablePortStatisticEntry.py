#!/usr/bin/python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：钱卫(Leniy Tsan)
#创建日期：2014.04.25
#修订信息参考__init__.py文件

"""瑞斯康达最近批次的头端，下挂cnu的cable输出低频部分场强过高，导致用户cnu开电上网，就会导致电视马赛克
#有两种解决办法
# 1.添加高通滤波器
# 2.手动将每个头端下面每个cnu的cable增益值降低10dB。下面就是批量处理方法
"""

from eoclib.common import getiplist
from eoclib.device import RcEocHead

aa = getiplist()
for ii in aa:
	a = RcEocHead(ii, 'admin', 'admin')
	if a.device_is_up:
		termEocPMDCnuCablePortAveAtt   = str(a.mib_obj_enum['termEocPMDCnuCablePortAveAtt'])   # 平均衰减
		termEocPMDCnuCablePortAvePower = str(a.mib_obj_enum['termEocPMDCnuCablePortAvePower']) # 平均输出功率
		for thiscnu in a.get_CnuCablePortStatisticEntry():
			print a.ip,"   ",thiscnu["index"],"   ",thiscnu[termEocPMDCnuCablePortAveAtt],"   ",thiscnu[termEocPMDCnuCablePortAvePower]