#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Geology.py 585 2013-06-26 02:51:42Z Bear $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

geologySrv = TSMS_API.Web.Geology.Service

def f2_8_1():
    structure = TSMS_API.Web.QueryService.FindStructures(tunnelId)[0] # 南下線
    structureId = structure.Key
    print '結構物: %s (%d)' % (structure.Value, structureId)
    
    stationRange = geologySrv.GetStationRange(structureId)
    print '里程: %f - %f' % (stationRange.Key, stationRange.Value)    
    
    view = geologySrv.QueryWebView1(tunnelId, structureId, stationRange.Key, stationRange.Value)  
    print
    
    print "營運里程開始:"                     
    print view.OpStationStart
    print
    
    print "營運里程結束:"                     
    print view.OpStationEnd
    print
    
    print "岩體評分資料列表:"                     
    showTable(view.RMRRecord, others=[('檔案路徑', 'File'),])
    print
    
    print "RMR 趨勢圖:"
    showChart(view.RMRChart)
    print 

    print "岩體等級趨勢圖:"
    showChart(view.RockStyleChart)
    print     
    
    print "支撐等級趨勢圖:"
    showChart(view.SupportVChart)
    print     
        
    return view
    
def f2_8_2():
    # 南港遂道
    tunnel = TSMS_API.Web.QueryService.FindTunnelsByEnginerringOffice(enginerringOfficeId)[0]
    tunnelId = tunnel.Key
    print '遂道: %s (%d)' % (tunnel.Value, tunnelId) 
    
    structure = TSMS_API.Web.QueryService.FindStructures(tunnelId)[0] # 南下線
    structureId = structure.Key
    print '結構物: %s (%d)' % (structure.Value, structureId)    
    
    view = geologySrv.QueryWebView2(tunnelId)  
    print
    
    print "地層資料圖:"
    print view.RefGeoMap
    print
    
    print "圖例:"
    print view.RefGeoLegend
    print
    
    select = view.GeologyInfoList[1] # 木山層
    print '%s - %s:' % (select.GeoType, select.GeoName)
    print '  施工里程 自 %d - 至 %d' % (select.ExcStartSta, select.ExcEndSta)
    print '  營運里程 自 %d - 至 %d' % (select.NowStartSta, select.NowEndSta)
    print
    print '  地質資料:' 
    print '  %s' % select.GeoContent
    print
    print '  特殊記事:' 
    print '  %s' % select.SpecialNotes
    print

    view2 = geologySrv.QueryWebView2_2(structureId)  
    print "岩體分類資料圖:"
    showChart(view2.Chart1)
    print
        
    return view
        
if __name__ == '__main__':
    showMainMenu('2.8', 2, locals())
    