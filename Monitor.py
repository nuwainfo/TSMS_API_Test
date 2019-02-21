#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Monitor.py 2220 2019-02-21 09:21:30Z Kevin $

import sys
from API import TSMS_API
from API import tunnelId

from API import showTable, showChart, showMainMenu

monitorSrv = TSMS_API.Web.Monitor.Service

structure = TSMS_API.Web.QueryService.FindStructures(tunnelId)[1] # 北上線
structureId = structure.Key
print '結構物: %s (%d)' % (structure.Value, structureId)

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

            clrType = clr.GetClrType(monitorSrv)
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
            msg += ('\n出錯函式：TSMS_API.Web.Monitor.Service.{}({})'.format(
                theFunction.__name__,
                ', '.join(['{}={}'.format(k, v) for k, v in paramsDict.items()])
            ))
            msg += '\n詳細 API 呼叫的參數及過程請參照 "API.log"'

            # https://stackoverflow.com/questions/
            # 6062576/adding-information-to-an-exception
            e.args = (msg,)
            raise e
    return _wrapper


def select(tunnelId, monitorId, instInfoN=0):
    instInfo = monitorSrv.FindInstallInfos(tunnelId, monitorId)[instInfoN]
    instId = instInfo.Key
    print '監測斷面: %s (%d)' % (instInfo.Value, instId)
    
    dateRange = monitorSrv.GetDateRange(tunnelId, monitorId, instId)
    print '日期: %s - %s' % (dateRange.Key, dateRange.Value)    
    
    return {
        'tunnelId': tunnelId, 
        'monitorId': monitorId, 
        'installId': instId, 
        'start': dateRange.Key, 
        'end': dateRange.Value,
    }

def f2_2_1():
    monitorId = 1
    # 9016
    kws = select(tunnelId, monitorId)    
    view = _log(monitorSrv.QueryWebView1)(**kws)
    print    
    
    print "控制點測量表:"                      
    showTable(view.ControlPts)
    print
    
    print "列座標:"
    for c in view.Coordinate:
        print c.Key, c.Value
        
    return view
        
def printBaseInfo(view):
    print "儀器安裝位置圖:"
    print view.RefImg
    print
    
    print "地質資訊:"
    print view.InstallInfo
    print        
    
def f2_2_2():
    monitorId = 2
    # NRL0001
    kws = select(tunnelId, monitorId)    
    view = _log(monitorSrv.QueryWebView2)(**kws)
    print
    
    printBaseInfo(view)
    
    print "控制點測量表:"
    showTable(view.Monitor3DData)
    print
    
    print "歷時曲線圖:"
    showChart(view.TimeChart1)
    print
    
    print "累積變化量圖:"
    showChart(view.TimeChart2)
    print
    
    if view.WarningChart:
        print "警戒值圖形資料:"    
        showChart(view.WarningChart)
        print    
        
    print "測值大於警戒值資料表:"
    showTable(view.WarningData)
    print    
        
    return view
    
def f2_2_3():
    monitorId = 3
    # C1
    kws = select(tunnelId, monitorId)
    view = _log(monitorSrv.QueryWebView3)(**kws)
    print
    
    printBaseInfo(view)
    
    print "裂縫擴展測量表:"
    showTable(view.MonitorCrackData)
    print
    
    print "歷時變位圖:"
    showChart(view.TimeChart1)
    print
    
    return view
    
def f2_2_4():
    monitorId = 4
    rainInstallId = 1
    rainUnitIndex = 1
    # NWPS1
    kws = select(tunnelId, monitorId)
    kws['chartNum'] = 3
    kws['rainInstallId'] = rainInstallId
    kws['rainUnitIndex'] = rainUnitIndex
    view = _log(monitorSrv.QueryWebView4)(**kws)
    print
    
    printBaseInfo(view)
    
    if view.TimeChart1:
        print "孔隙水壓歷時曲線圖:"
        showChart(view.TimeChart1)
        print
        
    if view.TimeChart2:
        print "單點流量歷時曲線圖:"
        showChart(view.TimeChart2)
        print        
    
    if view.MonitorWaterData:
        print "孔隙水壓測量表:"
        showTable(view.MonitorWaterData)
        print
        
    if view.MonitorSingleWaterData:
        print "單點流量測量表:"
        showTable(view.MonitorSingleWaterData)
        print    
        
    if view.WarningChart:
        print "警戒值圖形資料:"    
        showChart(view.WarningChart)
        print    

    if view.WarningData:
        print "測值大於警戒值資料表:"
        showTable(view.WarningData)
        print
        
    # 20130827
    print "每6小時間隔顯示"
    kws['dataStep'] = 12
    view2 = _log(monitorSrv.QueryWebView4)(**kws)
    print        
    
    printBaseInfo(view2)
    
    if view2.TimeChart1:
        print "孔隙水壓歷時曲線圖:"
        showChart(view2.TimeChart1)
        print
        
    if view2.TimeChart2:
        print "單點流量歷時曲線圖:"
        showChart(view2.TimeChart2)
        print        
    
    if view2.MonitorWaterData:
        print "孔隙水壓測量表:"
        showTable(view2.MonitorWaterData)
        print
        
    if view2.MonitorSingleWaterData:
        print "單點流量測量表:"
        showTable(view2.MonitorSingleWaterData)
        print    
        
    if view2.WarningChart:
        print "警戒值圖形資料:"    
        showChart(view2.WarningChart)
        print    
        
    print "測值大於警戒值資料表:"
    showTable(view2.WarningData)
    print            
    
    # NWPS2
    try:
        kws = select(tunnelId, monitorId, instInfoN=1)    
    except TSMS_API.Web.QueryService.DataNotExistException, e:
        print 'NWPS2', 'DataNotExistException', 'passed' # OK.
    print

    print '降雨量資料'
    showTable(view.RainFallRecords)
    print

    print '雨量歷時圖'
    showChart(view.RainFallChart)
    print

    return view        

def f2_2_5():
    monitorId = 6
    rainInstallId = 1
    rainUnitIndex = 1

    # OCM3
    kws = select(tunnelId, monitorId, 2)
    kws['rainInstallId'] = rainInstallId
    kws['rainUnitIndex'] = rainUnitIndex
    view = _log(monitorSrv.QueryWebView5)(**kws)
    print
    
    print "儀器安裝位置圖1:"
    print view.RefImg1
    print
    
    if view.RefImg2:
        print "儀器安裝位置圖2:"
        print view.RefImg2
        print
    
    print "地質資訊:"
    print view.InstallInfo
    print   
    
    print "流量計歷時曲線圖(平均流量):"
    showChart(view.TimeChart1)
    print
    
    print "流量計歷時曲線圖(平均水深):"
    showChart(view.TimeChart2)
    print    

    print "累積流量測量表:"
    showTable(view.MonitorStackWaterData)
    print    
    
    # 20130827
    print "每12小時間隔顯示"
    kws['dataStep'] = 120
    view2 = _log(monitorSrv.QueryWebView5)(**kws)
    print
    
    print "儀器安裝位置圖1:"
    print view2.RefImg1
    print
    
    if view2.RefImg2:
        print "儀器安裝位置圖2:"
        print view2.RefImg2
        print
    
    print "地質資訊:"
    print view2.InstallInfo
    print   
    
    print "流量計歷時曲線圖(平均流量):"
    showChart(view2.TimeChart1)
    print
    
    print "流量計歷時曲線圖(平均水深):"
    showChart(view2.TimeChart2)
    print    

    print "累積流量測量表:"
    showTable(view2.MonitorStackWaterData)
    print

    print '降雨量資料'
    showTable(view.RainFallRecords)
    print

    print '雨量歷時圖'
    showChart(view.RainFallChart)
    print

    return view
    
def f2_2_6():
    def query(monitorTypeIdx, installSectionIdx=0):
        monitorType = monitorSrv.FindMonitorTypes()[monitorTypeIdx]
        monitorTypeId = monitorType.Key
        print '監測儀器類別: %s (%d)' % (monitorType.Value, monitorTypeId)
                
        view = _log(monitorSrv.QueryWebView6)(tunnelId, monitorTypeId)
        print
        
        print "示意圖"
        print view.HintPic
        print
            
        print "監測斷面資料表:"                      
        showTable(view.InstallSectionInfoRecords, others=[
            ('照片路徑', 'Photo'),
            ('監測斷面Id', 'InstallId'),
        ])
        print
        
        
        installSection = view.InstallSectionInfoRecords.Rows[installSectionIdx]
        
        view2 = _log(monitorSrv.QueryWebView6_2)(tunnelId, monitorTypeId, installSection.InstallId)
        print
            
        print "%s 測點資料表:" % installSection.Data1
        if view2.InstallPointInfoRecords:
            showTable(view2.InstallPointInfoRecords, others=[('照片路徑', 'Photo')])
        print    
            
        return view       
        
    view = query(1) # 內空變位/NRL0001
    
    view2 = query(0) # 控制點測量/9016
    
    return view
    
def f2_2_7():
    monitorType = monitorSrv.FindMonitorTypes()[1] # 內空變位
    monitorTypeId = monitorType.Key
    print '監測儀器類別: %s (%d)' % (monitorType.Value, monitorTypeId)
            
    view = _log(monitorSrv.QueryWebView7)(tunnelId, monitorTypeId)
    print
        
    print "監測儀器維修資料表:"                      
    showTable(view.MonitorRepairInfoRecords)
    print
            
    return view

def f2_2_8():
    monitorType = 9

    from System import Array
    from System import DateTime

    installInfos = TSMS_API.Web.Monitor.Service.FindInstallInfos(
        tunnelId, monitorType, False)
    installInfoId = installInfos[0].Key  # 1

    arrayDates = Array[DateTime]([
        TSMS_API.Monitor.Service.GetMicroDispSurveyDate(tunnelId, installInfoId)[0].Value])

    view = _log(monitorSrv.QueryWebView8)(tunnelId, monitorType, installInfoId, arrayDates, 1)

    print '地質資訊'
    print view.InstallInfo

    print '微變位資料'
    showTable(view.microDispRecords)

    print '微變位圖'
    showChart(view.DispChart.XYChart1, attr='XYValues')
    showChart(view.DefChart.XYChart1, attr='XYValues')

    return view


def f2_2_9():
    monitorType = 10

    installInfos = monitorSrv.FindInstallInfos(tunnelId, monitorType, 0)
    installInfoId = installInfos[0].Key  # 1

    dates = monitorSrv.QueryMonitorDateRangeCommon(tunnelId, installInfoId, monitorType)
    endDate = dates[1]  # MaxDate
    startDate = endDate.AddMonths(-1)
    dataStep = 24

    view = _log(monitorSrv.QueryWebView9)(
        tunnelId, installInfoId, monitorType, startDate, endDate, dataStep)

    print '\n地質資訊'
    print view.InstallInfo

    print '\n天花板變位安裝示意圖'
    print view.CeilingInstallDiagram

    print '\n傾斜移角度變化量歷時曲線圖'
    showChart(view.TimeChart1)

    print '\n位移變化量歷時曲線圖'
    showChart(view.TimeChart2)

    print '\n監測資料'
    showTable(view.CeilingDefRecords)

    print '\n各儀器最大變位測值資料'
    showTable(view.CeilingDefMaxValuesRecords)

    return view


def f2_2_10():
    monitorType = 8
    tunnelId = 2

    installInfos = monitorSrv.FindMonitorInstallInfo(tunnelId, monitorType)
    installInfoId = installInfos[0].Key
    print(installInfos[0].Value)

    monitorPoint = monitorSrv.FindMonitorPoint(
        tunnelId, monitorType, installInfoId)
    monitorPointId = monitorPoint[0].Key

    surveyDates = monitorSrv.GetLevelingSurveyDate(
        tunnelId, installInfoId, monitorPointId)

    from System.Collections.Generic import List
    from System import DateTime
    from System import Array

    datesList = List[DateTime]()
    for date in surveyDates:
        datesList.Add(date.Value)

    levelingStations = monitorSrv.GetLevelingStation(
        tunnelId, installInfoId, monitorPointId)
    startStation = levelingStations[0].Value
    endStation = levelingStations[len(levelingStations) - 1].Value

    print(datesList.ToArray())
    view = _log(monitorSrv.QueryWebView10)(
        tunnelId, monitorType, installInfoId, monitorPointId,
        datesList.ToArray(), startStation, endStation)

    print '\n地質資訊'
    print view.InstallInfo

    print '\n路面沉陷觀測資料'
    showTable(view.LevelingRecords)

    print '\n測值大於警戒值總表'
    showTable(view.WarningRecords)

    print '\n路面變位速率圖'
    showChart(view.LevelingChart, attr='XYValues')

    print '\n歷時變位速率圖'
    showChart(view.DateLevelingChart1)

    print '\n歷時變位量圖'
    showChart(view.DateLevelingChart2)

    return view


def f2_2_11():
    # monitorType = 11
    tunnelId = 24
    installId = 3

    from System import DateTime
    startDate = DateTime(2017, 2, 6)
    endDate = DateTime(2018, 2, 6)

    view = _log(monitorSrv.QueryWebView11)(
        tunnelId, installId, startDate, endDate)

    print '\n地質資訊'
    print view.InstallInfo

    print '\n監測資料'
    showTable(view.GeoDefRecords)

    print '\nGoogle Map 測站資料'
    showTable(view.GeoDefMarksRecords)

    print '\n歷時曲線圖(East)'
    showChart(view.TimeChartEast)

    print '\n歷時曲線圖(North)'
    showChart(view.TimeChartNorth)

    print '\n歷時曲線圖(Up)'
    showChart(view.TimeChartUp)

    return view


if __name__ == '__main__':
    showMainMenu('2.2', 11, locals())
