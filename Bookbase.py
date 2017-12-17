#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Bookbase.py 1090 2015-12-16 08:35:54Z Bear $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId, sectionId

from API import showTable, showChart, showMainMenu

bookbaseSrv = TSMS_API.Web.Bookbase.Service

def f2_9_1():
    structureType = bookbaseSrv.FindStructureTypes()[0] # 主遂道
    structureTypeId = structureType.Key
    print '結構物類別: %s (%d)' % (structureType.Value, structureTypeId)
    
    view = bookbaseSrv.QueryWebView1(tunnelId, structureTypeId)
    print
    
    print "起點城市:"                      
    print view.StartCity  
    print "終點城市:"                      
    print view.EndCity
    print "起點里程:"                      
    print view.StartStation
    print "終點里程:"                      
    print view.EndStation
    print "隧道等級:"                      
    print view.Grade
    print "設計單位:"                      
    print view.Designer
    print "監造單位:"                      
    print view.Supervisor
    print "施工廠商:"                      
    print view.Contractor
    print "完工年份:"                      
    print view.CompletionYear    
    print "啟用年份:"                      
    print view.ToperatingYear    
    print "最大覆蓋厚度:"                      
    print view.ToverBurden        
    print    
    
    print "隧道結構體資訊列表:"                      
    showTable(view.StructureInfoRecords)
    print
        
    return view
    
def f2_9_2():
    # FIXME: It seems like there is a bug in FindReportBelongs, the result 
    #        and id is not matched. This causes Web's bug.
    reportBelong = bookbaseSrv.FindReportBelongs(sectionId)[0] # 當前工務段
    reportBelongId = reportBelong.Key
    print '報告書歸屬: %s (%d)' % (reportBelong.Value, reportBelongId)
    
    reportType = bookbaseSrv.FindReportTypes()[0] # ALL
    reportTypeId = reportType.Key
    print '報告書類別: %s (%d)' % (reportType.Value, reportTypeId)
    
    view = bookbaseSrv.QueryWebView2(sectionId, reportBelongId, reportTypeId, 
                                     tunnelId)
    print
    
    print "報告書列表 (%d 筆):" % len(view.ReportDocRecords.Rows)
    showTable(view.ReportDocRecords, others=[('檔案路徑', 'File'),])
    print
    
    # By keyword
    keyword = '98年'
    print '關鍵字:', keyword
    view = bookbaseSrv.QueryWebView2(sectionId, reportBelongId, reportTypeId,  
                                     tunnelId, keyword)
    print
    
    print "報告書列表 (%d 筆):" % len(view.ReportDocRecords.Rows)
    showTable(view.ReportDocRecords, others=[('檔案路徑', 'File'),])
    print    
        
    return view
    
def f2_9_3():
    drawingType = bookbaseSrv.FindDrawingTypes()[0] # ALL
    drawingTypeId = drawingType.Key
    print '圖說類別: %s (%d)' % (drawingType.Value, drawingTypeId)
    
    drawingStructureType = bookbaseSrv.FindDrawingStructureTypes()[0] # ALL
    drawingStructureTypeId = drawingStructureType.Key
    print '結構體類別: %s (%d)' % (drawingStructureType.Value, drawingStructureTypeId)
    
    drawingFigureType = bookbaseSrv.FindDrawingFigureTypes()[0] # ALL
    drawingFigureTypeId = drawingFigureType.Key
    print '圖說特性: %s (%d)' % (drawingFigureType.Value, drawingFigureTypeId)    
    
    view = bookbaseSrv.QueryWebView3(tunnelId, drawingTypeId, drawingStructureTypeId, drawingFigureTypeId)
    print
    
    print "峻工圖列表 (%d 筆):" % len(view.BuiltDrawingRecords.Rows)
    showTable(view.BuiltDrawingRecords, others=[('檔案路徑', 'File'),])
    print
    
    # By keyword
    keyword = '鋼筋圖'
    print '關鍵字:', keyword
    view = bookbaseSrv.QueryWebView3(tunnelId, drawingTypeId, drawingStructureTypeId, drawingFigureTypeId, 
                                     0, 0, keyword)
    print
    
    print "峻工圖列表 (%d 筆):" % len(view.BuiltDrawingRecords.Rows)
    showTable(view.BuiltDrawingRecords, others=[('檔案路徑', 'File'),])
    print    
        
    return view    
    
def f2_9_4():
    view = bookbaseSrv.QueryWebView4(sectionId, tunnelId)
    print
       
    def show(select):
        print '%s - %s - %s - %s:' % (select.Level1, select.Level2, select.Level3, select.Method)
        print '  維修工法編號: %s' % select.MethodId
        print '  維修工法: %s' % select.Method    
        print '  單位: %s' % select.Unit
        print '  單價: %s' % select.UnitPrice
        print '  維修施工圖: %s' % select.FigureName
        print '  備註: %s' % select.Remarks    
        print
        
        print "單價分析列表:"
        if select.PriceAnalysisRecords:
            showTable(select.PriceAnalysisRecords)
        print        
        
    show(view.MaintainTypeRecords[0]) # 混凝土裂縫灌注修補(≧0.5mm)        

    # By keyword
    keyword = 'A類'
    print '關鍵字:', keyword
    
    view = bookbaseSrv.QueryWebView4(sectionId, tunnelId, keyword)
    print
    
    show(view.MaintainTypeRecords[0]) # 人行橫坑門修繕(A類)    
        
    return view    
    
def f2_9_5():
    photoType = bookbaseSrv.FindPhotoTypes()[0] # ALL
    photoTypeId = photoType.Key
    print '照片類別: %s (%d)' % (photoType.Value, photoTypeId)
    
    view = bookbaseSrv.QueryWebView5(tunnelId, photoTypeId)
    print
    
    print "照片列表 (%d 筆):" % len(view.PhotoRecords.Rows)
    showTable(view.PhotoRecords, others=[('檔案路徑', 'File'),])
    print
    
    # By keyword
    keyword = '地質圖'
    print '關鍵字:', keyword
    view = bookbaseSrv.QueryWebView5(tunnelId, photoTypeId, keyword)
    print
    
    print "照片列表 (%d 筆):" % len(view.PhotoRecords.Rows)
    showTable(view.PhotoRecords, others=[('檔案路徑', 'File'),])
    print  
        
    return view    
        
if __name__ == '__main__':
    showMainMenu('2.9', 5, locals())
    