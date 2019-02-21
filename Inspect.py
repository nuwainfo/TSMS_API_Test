#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Inspect.py 2220 2019-02-21 09:21:30Z Kevin $

import clr
import datetime

from API import TSMS_API
from API import tunnelId

from API import showTable, showChart, showMainMenu

inspectSrv = TSMS_API.Web.Inspect.Service
structure = TSMS_API.Web.QueryService.FindStructures(tunnelId)[2] # 導坑
structureId = structure.Key
print '結構物: %s (%d)' % (structure.Value, structureId)


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

            clrType = clr.GetClrType(inspectSrv)
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
            msg += ('\n出錯函式：TSMS_API.Web.Inspect.Service.{}({})'.format(
                theFunction.__name__,
                ', '.join(['{}={}'.format(k, v) for k, v in paramsDict.items()])
            ))
            msg += '\n詳細 API 呼叫的參數及過程請參照 "API.log"'

            # https://stackoverflow.com/questions/
            # 6062576/adding-information-to-an-exception
            e.args = (msg,)
            raise e
    return _wrapper


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
    
    view = _log(inspectSrv.QueryWebView1)(tunnelId, structureId, projId,
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
               
    view = _log(inspectSrv.QueryWebView2)(
        tunnelId, structureId, structureTypeId,
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
               
    view2 = _log(inspectSrv.QueryWebView2)(
        tunnelId, structureId, structureTypeId, projId, ndtId)
    
    showView(view2)
    
    print ('DEBUG: inspectSrv.QueryWebView2%s' % 
           str((tunnelId, structureId, structureTypeId, projId, ndtId, 
               start, end, proj2Id)))    
               
    view3 = _log(inspectSrv.QueryWebView2)(
        tunnelId, structureId, structureTypeId,
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

    view = _log(inspectSrv.QueryWebView3)(
        tunnelId, structureId, projId, startSector.Key, endSector.Key)
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
        
    view = _log(inspectSrv.QueryWebView4)(tunnelId, otherStructureId, projId)
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


def f2_3_5():
    # 北工處
    enginerringOffice = TSMS_API.Web.QueryService.FindALLEngineeringOffice()[0]
    enginerringOfficeId = enginerringOffice.Key

    # 彭山隧道
    tunnel = TSMS_API.Web.QueryService.FindTunnelsByEnginerringOffice(enginerringOfficeId)[3]
    tunnelId = tunnel.Key
    sectionId = TSMS_API.API.Service.FindSectionidByTunid(tunnelId)
    tunnelHierarcy = TSMS_API.Web.QueryService.GetTunnelHierarcy(tunnelId)
    print '工程處: %s (%d)' % (tunnelHierarcy.engineeringOffice, enginerringOfficeId)
    print '工務段: %s (%d)' % (tunnelHierarcy.section, sectionId)
    print '國道: %s' % tunnelHierarcy.freeway
    print '遂道: %s (%d)' % (tunnel.Value, tunnelId)

    # 北上線管線廊道
    structure = TSMS_API.Web.QueryService.FindGalleryStructures(tunnelId)[1]
    structureId = structure.Key
    print '結構物: %s (%d)' % (structure.Value, structureId)

    # 2050年TEST_2050測試專案
    proj = TSMS_API.Web.QueryService.FindProjectsByGallery(tunnelId, structureId)[0]
    projId = proj.Key
    print '本期檢測專案: %s (%d)' % (proj.Value, projId)

    startSector = TSMS_API.Web.QueryService.FindSectors(structureId)[0]
    print '區段編號(自): %s (%d)' % (startSector.Value, startSector.Key)

    endSector = TSMS_API.Web.QueryService.FindSectors(structureId)[7]
    print '區段編號(至): %s (%d)' % (endSector.Value, endSector.Key)

    view = _log(inspectSrv.QueryWebView5)(
        tunnelId, structureId, projId,
        startSector.Key, endSector.Key, 0, False, True)
    print

    print "損傷圖右半部:"
    print view.TunWallMap
    print

    print "損傷圖左半部:"
    print view.TunRoadMap
    print

    print "控制點測量表:"
    showTable(view.TunInjureRecord, others=[('照片', 'Photo'), ])
    print

    return view


def f2_3_6():
    # 北工處
    enginerringOffice = TSMS_API.Web.QueryService.FindALLEngineeringOffice()[0]
    enginerringOfficeId = enginerringOffice.Key

    # 石碇隧道
    tunnel = TSMS_API.Web.QueryService.FindTunnelsByEnginerringOffice(enginerringOfficeId)[1]
    tunId = tunnel.Key

    # 北上線
    structures = TSMS_API.API.Service.FindStructuresName(tunId, 0)
    structureId = structures[1].Key

    # 2050年TEST_2050測試專案
    project = TSMS_API.API.Service.FindProjectsByStructure(tunId, structureId)[4]
    projectId = project.Key

    #
    startStation = 795
    endStation = 3515

    print '遂道: %s (%d)' % (tunnel.Value, tunnelId)
    print '安檢專案: %s (%d)' % (project.Value, projectId)
    print "區段里程： %d 至 %d" % (startStation, endStation)

    # search
    view = _log(inspectSrv.QueryWebView6)(
        structureId, projectId, startStation, endStation)

    for r in view.ImageInfoRecord.Rows:
        print r.Key, r.Value

    return view

def f2_3_7():
    from System.Collections.Generic import List
    tunnelId = 5  # 雪山隧道
    structureIds = List[int]([24, 24, 24])  # 南下線
    projectIds = List[int]([3, 4, 8])
    startSectorIds = List[int]([70, 70, 70])
    endSectorIds = List[int]([100, 100, 100])
    view = _log(inspectSrv.QueryWebView7)(
        tunnelId, structureIds, projectIds, startSectorIds, endSectorIds)

    def showProject(project):
        print '隧道異狀展開圖'
        print project.Option0RightPic
        print project.Option0LeftPic
        print

        print '隧道區段分級展開圖'
        print project.Option1RightPic
        print project.Option1LeftPic
        print

        print '隧道異狀數量百分比圖'
        showChart(project.Option3Chart)
        print

        print '隧道區段異狀分級統計圖'
        showTable(project.Option2Records)
        print

        print '隧道單一區段異狀數量圖'
        showTable(project.Option4Records)
        print

    print '查詢一'
    showProject(view.project1)
    print

    print '查詢二'
    showProject(view.project2)
    print

    print '查詢三'
    showProject(view.project3)
    print

    return view

def f2_3_8():
    tunnelId = 5  # 雪山隧道
    structureId = 24  # 南下線
    projectId = 2000  # 2050年TEST_2050測試專案

    from System import DateTime
    startDate = DateTime(2018, 1, 1)
    endDate = DateTime(2018, 12, 31)

    view = _log(inspectSrv.QueryWebView8)(
        structureId, projectId, startDate, endDate)

    print '排水設施資料表'
    showTable(view.Records)
    print

    return view

if __name__ == '__main__':
    showMainMenu('2.3', 8, locals())
