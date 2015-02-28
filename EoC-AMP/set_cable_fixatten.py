#!/usr/bin/python
# -*- coding: UTF-8 -*-
#山东广电网络集团-EoC管理软件
#作者：Leniy(Leniy Tsan)
#创建日期：2014.03.24
#修订信息参考__init__.py文件

"""瑞斯康达最近批次的头端，低频部分场强过高，用户上网会导致电视马赛克
#有两种解决办法
# 1.添加高通滤波器
# 2.手动将每个头端cable增益值降低10dB。下面就是批量处理方法
"""

from eoclib.common import getiplist
from eoclib.device import RcEocHead

aa = getiplist()
for ii in aa:
	a = RcEocHead(ii, 'xxxxxxxxx','xxxxxxxxxxx')
	if a.device_is_up:
		#if a.cable_freqinfo[1] == -5:
		#	a.set_cable_freqinfo_FixAtten(2,0)
		print ii ,a.cable_freqinfo
