#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#��˹����������ε�ͷ�ˣ���Ƶ���ֳ�ǿ���ߣ��û������ᵼ�µ���������
#�����ֽ���취
# 1.��Ӹ�ͨ�˲���
# 2.�ֶ���ÿ��ͷ��cable����ֵ����10dB�������������������
from eoclibnew.func import *

aa = getiplist()			
for ii in aa:
	a = RcEocHeadCommon(ii, 'xxxxxxx', 'xxxxxxxxxx')
	if a.device_is_up:
		#if a.cable_freqinfo[1] == -5:
		#	a.set_cable_freqinfo_FixAtten(2,0)
		#print ii ,a.cable_freqinfo
