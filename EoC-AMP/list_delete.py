# -*- coding: utf-8 -*-
start_pvid = 2150
end_pvid   = 2160
pvid_list = {}
for temp_vid in range(start_pvid, end_pvid + 1):
	pvid_list[temp_vid] = 1


try:
	del(pvid_list[2155])
except:
	print "vlan重复"
print pvid_list

try:
	del(pvid_list[2155])
except:
	print "vlan重复"
print pvid_list
