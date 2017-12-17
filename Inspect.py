#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Inspect.py 1028 2015-10-14 07:51:59Z Bear $

import sys

from API import TSMS_API
from API import tunnelId

from API import showTable, showChart, showMainMenu

inspectSrv = TSMS_API.Web.Inspect.Service

structure = TSMS_API.Web.QueryService.FindStructures(tunnelId)[2] # 導坑
structureId = structure.Key
print '結構物: %s (%d)' % (structure.Value, structureId)

def f2_3_1():
    # 100 年第1階段
    proj = TSMS_API.Web.QueryService.FindProjects(structureId)[0]
    projId = proj.Key
    print '本期檢測專案: %s (%d)' % (proj.Value, projId)
    
    # S001
    startSector = TSMS_API.Web.QueryService.FindSectors(structureId)[0]
    print '區段編號(自): %s (%d)' % (startSector.Value, startSector.Key)    
    
    # S005
    endSector = TSMS_API.Web.QueryService.FindSectors(structureId)[4]
    print '區段編號(至): %s (%d)' % (endSector.Value, endSector.Key)    
    
    view = inspectSrv.QueryWebView1(tunnelId, structureId, projId, 
                                    startSector.Key, endSector.Key)                      
    print

    print "損傷圖右半部:"
    print view.TunWallMap
    print
    
    print "損傷圖左半部:"
    print view.TunRoadMap
    print    
    
    print "控制點測量表:"
    showTable(view.TunInjureRecord, others=[('照片', 'Photo'),])
    print

    return view    
    
def f2_3_2():
    # 隧道類型
    structureType = inspectSrv.FindStructureTypes()[1]
    structureTypeId = structureType.Key
    print '結構物類型: %s (%d)' % (structureType.Value, structureTypeId)
    
    # 導坑
    structure = inspectSrv.FindStructures(tunnelId, structureTypeId)[3]
    structureId = structure.Key
    print '結構體名稱: %s (%d)' % (structure.Value, structureId)    
    
    # 100 年第1階段
    proj = inspectSrv.FindProjects(tunnelId, structureId, structureTypeId)[0]
    projId = proj.Key
    print '本期檢測專案: %s (%d)' % (proj.Value, projId)
    
    ndt = inspectSrv.FindNDTs()[0] # ALL
    ndtId = ndt.Key
    print '非破壞檢測工法: %s (%d)' % (ndt.Value, ndtId)   

    # 新資料庫無此資料
    # 100 年第2階段
    #proj2 = inspectSrv.FindProjects(tunnelId, structureId, structureTypeId)[1]
    #proj2Id = proj2.Key
    #print '對比檢測專案: %s (%d)' % (proj2.Value, proj2Id) 
    proj2Id = -1

    start = 15500
    end = 28500
    print '範圍: %d - %d' % (start, end)
    
    print ('DEBUG: inspectSrv.QueryWebView2%s' % 
           str((tunnelId, structureId, structureTypeId, projId, ndtId, 
               start, end, proj2Id)))
               
    view = inspectSrv.QueryWebView2(tunnelId, structureId, structureTypeId, 
                                    projId, ndtId, start, end, proj2Id)
    print

    def showView(view):
        print "非破壞檢測工作成果表:"
        showTable(view.NDTRecord, others=[
            ('摘要檔案路徑', 'File'),
            ('檢測照片1圖檔路徑', 'Photo1'),
            ('檢測照片2圖檔路徑', 'Photo2'),
        ])
        print
        
        if view.NDTRecord2:
            print "對比專案資料列表:"
            showTable(view.NDTRecord2, others=[
                ('摘要檔案路徑', 'File'),
                ('檢測照片1圖檔路徑', 'Photo1'),
                ('檢測照片2圖檔路徑', 'Photo2'),
            ])
            print    
        
        print "檢測位置展開圖:"
        print view.NDTMap
        print
        
        print "檢測位置展開圖圖例:"
        print view.NDTLegend
        print        
        
    showView(view)
    
    print ('DEBUG: inspectSrv.QueryWebView2%s' % 
           str((tunnelId, structureId, structureTypeId, projId, ndtId, 
               start, end, proj2Id)))    
               
    view2 = inspectSrv.QueryWebView2(tunnelId, structureId, structureTypeId, 
                                     projId, ndtId)
    
    showView(view2)
    
    print ('DEBUG: inspectSrv.QueryWebView2%s' % 
           str((tunnelId, structureId, structureTypeId, projId, ndtId, 
               start, end, proj2Id)))    
               
    view3 = inspectSrv.QueryWebView2(tunnelId, structureId, structureTypeId, 
                                     projId, ndtId, comparisonProjectId=proj2Id)
    
    showView(view3)    

    return view        
    
def f2_3_3():
    # 導坑
    structure = TSMS_API.Web.QueryService.FindStructures(tunnelId)[2]
    structureId = structure.Key
    print '結構體名稱: %s (%d)' % (structure.Value, structureId)    
    
    # 100 年第1階段
    proj = TSMS_API.Web.QueryService.FindProjects(structureId)[0]
    projId = proj.Key
    print '本期檢測專案: %s (%d)' % (proj.Value, projId)
    
    # S001
    startSector = TSMS_API.Web.QueryService.FindSectors(structureId)[0]
    print '區段編號(自): %s (%d)' % (startSector.Value, startSector.Key)    
    
    # S005
    endSector = TSMS_API.Web.QueryService.FindSectors(structureId)[4]
    print '區段編號(至): %s (%d)' % (endSector.Value, endSector.Key)    
        
    view = inspectSrv.QueryWebView3(tunnelId, structureId, projId, startSector.Key, endSector.Key)
    print
        
    print "區段健全度資料表:"
    showTable(view.TunSectorEvaluationRecord)
    print
    
    print "出露損傷數量百分比圖:"
    showChart(view.TunInjurePercentCalChart)
    print    
    
    print "區段損傷評定資料總表:"
    showTable(view.RecordData)
    print    
    
    if view.RecordDataChart:
        print "區段損傷評定統計圖:"
        showChart(view.RecordDataChart)
        print   

    print "異狀摘要表:"
    showTable(view.RecordData2)
    print
        
    print "區段出露損傷尺寸統計圖:"
    for i, r in enumerate(view.RecordData2.Rows):
        print i + 1, '=>'
        showChart(r.Chart)
    print 

    return view           
    
def f2_3_4():
    # 主線南洞口
    otherStructure = inspectSrv.FindOtherStructures(tunnelId)[0]
    otherStructureId = otherStructure.Key
    print '結構體名稱: %s (%d)' % (otherStructure.Value, otherStructureId)    
    
    # 100 年第1階段
    proj = inspectSrv.FindProjectsByOtherStructure(tunnelId, 
                                                   otherStructureId)[0]
    projId = proj.Key
    print '本期檢測專案: %s (%d)' % (proj.Value, projId)
        
    view = inspectSrv.QueryWebView4(tunnelId, otherStructureId, projId)       
    print

    print "南下線里程:"
    print view.Sta1
    print
    
    print "北上線里程:"
    print view.Sta2
    print    
    
    print "平面示意圖1:"
    print view.RefPhoto1
    print    
    
    print "平面示意圖2:"
    print view.RefPhoto2
    print        
    
    print "異狀記錄表:"
    showTable(view.OtherStructureRecord, others=[('照片', 'Photo'),], output='234.txt')
    print

    return view        
    
if __name__ == '__main__':
    showMainMenu('2.3', 4, locals())
    