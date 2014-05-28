# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

ID_2 = 1000
ID_3 = 1001
ID_4 = 1002
ID_5 = 1003
ID_6 = 1004

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"广电网络EoC终端自动管理软件(作者:Leniy)", pos = wx.DefaultPosition, size = wx.Size( 471,247 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		fgSizer = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"全部信息检索" ), wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 1, 4, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		gSizer1 = wx.GridSizer( 2, 1, 0, 0 )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"头端起始ip地址的最后一位", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		gSizer1.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"头端终止ip地址的最后一位", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		gSizer1.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer2.Add( gSizer1, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		gSizer2 = wx.GridSizer( 2, 1, 0, 0 )
		
		self.StartIP = wx.TextCtrl( self, wx.ID_ANY, u"50", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.StartIP, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.EndIP = wx.TextCtrl( self, wx.ID_ANY, u"130", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.EndIP, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer2.Add( gSizer2, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		gSizer3 = wx.GridSizer( 1, 1, 0, 0 )
		
		self.SearchButton = wx.Button( self, wx.ID_ANY, u"开始搜索", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer3.Add( self.SearchButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer2.Add( gSizer3, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		gSizer4 = wx.GridSizer( 1, 1, 0, 0 )
		
		self.m_hyperlink1 = wx.HyperlinkCtrl( self, wx.ID_ANY, u"About", u"http://blog.leniy.org", wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
		gSizer4.Add( self.m_hyperlink1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		fgSizer2.Add( gSizer4, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		sbSizer1.Add( fgSizer2, 1, wx.EXPAND|wx.ALL, 5 )
		
		fgSizer.Add( sbSizer1, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"自动设置VLAN" ), wx.VERTICAL )
		
		fgSizer4 = wx.FlexGridSizer( 1, 4, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"请输入vlan起止范围", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer4.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.StartPVID = wx.TextCtrl( self, wx.ID_ANY, u"2001", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.StartPVID, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.EndPVID = wx.TextCtrl( self, wx.ID_ANY, u"2999", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.EndPVID, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.SetButton = wx.Button( self, wx.ID_ANY, u"自动设置", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.SetButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		sbSizer2.Add( fgSizer4, 1, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		fgSizer.Add( sbSizer2, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.SetSizer( fgSizer )
		self.Layout()
		self.m_menubar6 = wx.MenuBar( 0 )
		self.about1 = wx.Menu()
		self.about2 = wx.MenuItem( self.about1, ID_2, u"程序：Eoc头终端自动管理", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about2 )
		
		self.about3 = wx.MenuItem( self.about1, ID_3, u"用途：自动检索全部用户终端，并可以自动配置", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about3 )
		
		self.about4 = wx.MenuItem( self.about1, ID_4, u"作者：Leniy", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about4 )
		
		self.about5 = wx.MenuItem( self.about1, ID_5, u"授权：仅限公司技术部使用", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about5 )
		
		self.about6 = wx.MenuItem( self.about1, ID_6, u"版本：2014.04", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about6 )
		
		self.m_menubar6.Append( self.about1, u"关于本软件" ) 
		
		self.SetMenuBar( self.m_menubar6 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.SearchButton.Bind( wx.EVT_BUTTON, self.search )
		self.SetButton.Bind( wx.EVT_BUTTON, self.setpvid )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def search( self, event ):
		event.Skip()
	
	def setpvid( self, event ):
		event.Skip()
	

