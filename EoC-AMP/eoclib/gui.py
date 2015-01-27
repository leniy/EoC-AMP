# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Main_Frame
###########################################################################

class Main_Frame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"广电网络EoC终端自动管理软件(作者:Leniy)", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		fgSizer = wx.FlexGridSizer( 4, 1, 0, 0 )
		fgSizer.SetFlexibleDirection( wx.BOTH )
		fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"头端ip地址范围" ), wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 1, 3, 0, 0 )
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
		
		self.StartIP = wx.TextCtrl( self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StartIP.SetMaxLength( 0 ) 
		self.StartIP.Enable( False )
		
		gSizer2.Add( self.StartIP, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.EndIP = wx.TextCtrl( self, wx.ID_ANY, u"150", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.EndIP.SetMaxLength( 0 ) 
		self.EndIP.Enable( False )
		
		gSizer2.Add( self.EndIP, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		fgSizer2.Add( gSizer2, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap( u"res/author.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer1.Add( fgSizer2, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizer1, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"自动设置VLAN范围" ), wx.VERTICAL )
		
		fgSizer4 = wx.FlexGridSizer( 1, 3, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"请输入vlan起止范围", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer4.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.StartPVID = wx.TextCtrl( self, wx.ID_ANY, u"2000", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StartPVID.SetMaxLength( 0 ) 
		self.StartPVID.Enable( False )
		
		fgSizer4.Add( self.StartPVID, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.EndPVID = wx.TextCtrl( self, wx.ID_ANY, u"2999", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.EndPVID.SetMaxLength( 0 ) 
		self.EndPVID.Enable( False )
		
		fgSizer4.Add( self.EndPVID, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer2.Add( fgSizer4, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizer2, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"自动检索并设置" ), wx.VERTICAL )
		
		fgSizer51 = wx.FlexGridSizer( 1, 3, 0, 0 )
		fgSizer51.SetFlexibleDirection( wx.BOTH )
		fgSizer51.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.EocStartButton = wx.Button( self, wx.ID_ANY, u"开始执行", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.EocStartButton.SetDefault() 
		fgSizer51.Add( self.EocStartButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		self.rate_gauge = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.rate_gauge.SetValue( 0 ) 
		fgSizer51.Add( self.rate_gauge, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND, 5 )
		
		self.rate_staticText = wx.StaticText( self, wx.ID_ANY, u"已完成0%", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rate_staticText.Wrap( -1 )
		fgSizer51.Add( self.rate_staticText, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		sbSizer3.Add( fgSizer51, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizer3, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Log记录区" ), wx.VERTICAL )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.LogRedirect = wx.TextCtrl( self, wx.ID_ANY, u"\n\n\n\n\n\n\n\n\n\n\n\n\n", wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer1.Add( self.LogRedirect, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		
		sbSizer4.Add( bSizer1, 1, wx.EXPAND, 5 )
		
		
		fgSizer.Add( sbSizer4, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer )
		self.Layout()
		fgSizer.Fit( self )
		self.m_menubar6 = wx.MenuBar( 0 )
		self.about1 = wx.Menu()
		self.about2 = wx.MenuItem( self.about1, wx.ID_ANY, u"程序：Eoc头终端自动管理", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about2 )
		
		self.about3 = wx.MenuItem( self.about1, wx.ID_ANY, u"用途：自动检索全部用户终端，并可以自动配置", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about3 )
		
		self.about4 = wx.MenuItem( self.about1, wx.ID_ANY, u"作者：Leniy", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about4 )
		
		self.about5 = wx.MenuItem( self.about1, wx.ID_ANY, u"授权：仅限公司技术部使用（2014.04-2024.03）", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about5 )
		
		self.about6 = wx.MenuItem( self.about1, wx.ID_ANY, u"更新：2014.07", wx.EmptyString, wx.ITEM_NORMAL )
		self.about1.AppendItem( self.about6 )
		
		self.m_menubar6.Append( self.about1, u"关于本软件" ) 
		
		self.SetMenuBar( self.m_menubar6 )
		
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.EocStartButton.Bind( wx.EVT_BUTTON, self.eocstart )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def eocstart( self, event ):
		event.Skip()
	

