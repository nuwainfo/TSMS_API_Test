#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Bookbase.py 2220 2019-02-21 09:21:30Z Kevin $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId, sectionId

from API import showTable, showChart, showMainMenu

bookbaseSrv = TSMS_API.Web.Bookbase.Service

import clr
import datetime

def _log(theFunction):
    def _wrapper(*args, **kwds):
        try:
            returnval = theFunction(*args, **kwds)
            return returnval
        except Exception as e:
            paramsDict = {}
            params = None

            # https://stackoverflow.com/questions/10920499/
            # get-built-in-method-signature-python

            clrType = clr.GetClrType(bookbaseSrv)
            for m in clrType.GetMethods():
                if m.Name == theFunction.__name__:
                    params = m.GetParameters()

            for i in range(params.Count):
                if i == len(args):
                    # 沒有預設值會回傳物件 DBNull
                    if params[i].DefaultValue.GetTypeCode() \
                            != 'System.TypeCode.DBNull':
                        break

                paramsDict.update({
                    params[i].Name: args[i]})

            msg = '例外類別：' + str(e)
            msg += '\n時間：' + str(datetime.datetime.now())
            msg += ('\n出錯函式：TSMS_API.Web.Bookbase.Service.{}({})'.format(
                theFunction.__name__,
                ', '.join(['{}={}'.format(k, v) for k, v in paramsDict.items()])
            ))
            msg += '\n詳細 API 呼叫的參數及過程請參照 "API.log"'

            # https://stackoverflow.com/questions/
            # 6062576/adding-information-to-an-exception
            e.args = (msg,)
            raise e
    return _wrapper


def f2_9_1():
    structureType = bookbaseSrv.FindStructureTypes()[0] # 主遂道
    structureTypeId = structureType.Key
    print '結構物類別: %s (%d)' % (structureType.Value, structureTypeId)
    
    view = _log(bookbaseSrv.QueryWebView1)(tunnelId, structureTypeId)
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
    
    view = _log(bookbaseSrv.QueryWebView2)(sectionId, reportBelongId, reportTypeId,
                                     tunnelId)
    print
    
    print "報告書列表 (%d 筆):" % len(view.ReportDocRecords.Rows)
    showTable(view.ReportDocRecords, others=[('檔案路徑', 'File'),])
    print
    
    # By keyword
    keyword = '98年'
    print '關鍵字:', keyword
    view = _log(bookbaseSrv.QueryWebView2)(sectionId, reportBelongId, reportTypeId,
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
    
    view = _log(bookbaseSrv.QueryWebView3)(tunnelId, drawingTypeId, drawingStructureTypeId, drawingFigureTypeId)
    print
    
    print "峻工圖列表 (%d 筆):" % len(view.BuiltDrawingRecords.Rows)
    showTable(view.BuiltDrawingRecords, others=[('檔案路徑', 'File'),])
    print
    
    # By keyword
    keyword = '鋼筋圖'
    print '關鍵字:', keyword
    view = _log(bookbaseSrv.QueryWebView3)(tunnelId, drawingTypeId, drawingStructureTypeId, drawingFigureTypeId,
                                     0, 0, keyword)
    print
    
    print "峻工圖列表 (%d 筆):" % len(view.BuiltDrawingRecords.Rows)
    showTable(view.BuiltDrawingRecords, others=[('檔案路徑', 'File'),])
    print    
        
    return view    
    
def f2_9_4():
    view = _log(bookbaseSrv.QueryWebView4)(sectionId, tunnelId)
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
    
    view = _log(bookbaseSrv.QueryWebView4)(sectionId, tunnelId, keyword)
    print
    
    show(view.MaintainTypeRecords[0]) # 人行橫坑門修繕(A類)    
        
    return view    
    
def f2_9_5():
    photoType = bookbaseSrv.FindPhotoTypes()[0] # ALL
    photoTypeId = photoType.Key
    print '照片類別: %s (%d)' % (photoType.Value, photoTypeId)
    
    view = _log(bookbaseSrv.QueryWebView5)(tunnelId, photoTypeId)
    print
    
    print "照片列表 (%d 筆):" % len(view.PhotoRecords.Rows)
    showTable(view.PhotoRecords, others=[('檔案路徑', 'File'),])
    print
    
    # By keyword
    keyword = '地質圖'
    print '關鍵字:', keyword
    view = _log(bookbaseSrv.QueryWebView5)(tunnelId, photoTypeId, keyword)
    print
    
    print "照片列表 (%d 筆):" % len(view.PhotoRecords.Rows)
    showTable(view.PhotoRecords, others=[('檔案路徑', 'File'),])
    print  
        
    return view

def f2_9_7():
    tunnelId = 5  # 雪山隧道

    from System.Collections.Generic import List

    structureIds = List[int]([24, 24, 24])  # 南下線
    projectIds = List[int]([8, 8, 8])  # 103~104頭城段隧道檢監測工作_104第一階段巡查工作
    startSectorIds = List[int]([1, 11, 21])
    endSectorIds = List[int]([10, 20, 30])

    view = _log(bookbaseSrv.QueryWebView7)(
        tunnelId, structureIds, projectIds, startSectorIds, endSectorIds)

    def showProject(_WebView7):
        print _WebView7.Option0RightPic
        print _WebView7.Option0LeftPic
        print _WebView7.Option1RightPic
        print _WebView7.Option1LeftPic

        if _WebView7.Option2Records:
            showTable(_WebView7.Option2Records)

        if _WebView7.Option3Records:
            showTable(_WebView7.Option3Records)

        if _WebView7.Option3Chart:
            showChart(_WebView7.Option3Chart)

        if _WebView7.Option4Records:
            showTable(_WebView7.Option4Records)

    showProject(view.project1)
    showProject(view.project2)
    showProject(view.project3)

        
if __name__ == '__main__':
    showMainMenu('2.9', 7, locals())
    