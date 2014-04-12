# -*- coding: UTF-8 -*-
#EoC管理

import urllib2


#登陆函数，输入ip，返回cookie（默认ip可以正常访问）
def logineoc(ip):
    #设置cookie保存登录状态
    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)
    #首先登陆账号，并设置cookie
    request = urllib2.Request(
        url     = 'http://' + ip + '/index.html',
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : 'http://' + ip + '/login.html'
            },
        data    = 'username=xxxxxxxxxxxx&password=xxxxxxxxxxxxxxxxx&language=cn&x=37&y=6'
        )

    try:
        response = opener.open(request)
    except:
        print '\n=======地址为' + ip + '的Eoc无法访问=====\n'

    return cookies


#获取设备列表函数，输入ip、cookies，返回dict格式的列表（默认ip可以正常访问）
def get_cnu_devlist(ip,cookies):
    opener = urllib2.build_opener(cookies)
    request = urllib2.Request(
        url     = 'http://' + ip + '/g',
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : 'http://' + ip + '/cnu_devlist.html',
            },
        data    = 'entry=a:0:0;46849;46852;46850;46851;46854;46860;46868'
        )
    try:
        response = opener.open(request)
    except:
        print '\n=======地址为' + ip + '的Eoc无法访问=====\n'

    cnu_ajax_devlist = eval(response.read())
    cnu_devlist = cnu_ajax_devlist['entry']
    
    return cnu_devlist


#获取单个网口的pvid，输入ip、cookies、网口的id，返回网口信息的dict格式（默认ip可以正常访问）



#获取所有网口的信息函数
#def getlists():

#获取单个网口信息函数
#def getlist():




















#首先进入for循环，分别依次处理各个Eoc头端设备
#ip为x.x.x.xx，现有xx为50-108
for ip_last in range(101, 101 + 1):
    #下面开始进入单个Eoc头端进行操作

    #设置当前头端的ip地址
    ip = 'x.x.x.' + str(ip_last)

    cookies = logineoc(ip)
    cnu_devlist = get_cnu_devlist(ip,cookies)
    
    #处理列表
    print '在Eoc头端' + ip + '中，共发现如下设备：'
    for cnu_dev in cnu_devlist:
        print '编号：' + cnu_dev['index'] + '；mac地址：' + cnu_dev['46850'] + '\n'

    #各个CNU设备的pvid获取
    
    #根据设备列表，进行for循环

    #获取单个CNU的pvid
    #以索引号为16512的CNU为例
    #其共有5个pvid，分别分配给了1个Cable、4个FE。
    #这五个pvid的索引号分别为6016513、116513、116514、116515、116516
    #下面获取第一个网络接口116513的pvid（即其vlan）
    request = urllib2.Request(
        url     = 'http://' + ip + '/g',
        headers = {
            'Content-Type' : 'application/x-www-form-urlencoded',
            'Referer' : 'http://' + ip + '/cnu_port_config.html',
            },
        data    = 'entry=g:116513:0;49153;49154;48899;48900;48901;48902;48903;48904;48905;48897;48898'
        )
    try:
        response = opener.open(request)
    except :
        print '列表获取错误'

    cnu_ajax_portconfig = eval(response.read())
    #cnu_portconfig = cnu_ajax_portconfig['entry']
    #================待编写list处理程序=============
    #print '\n\n单个设备其中一个网口的信息\n' + cnu_ajax_portconfig



















