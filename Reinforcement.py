#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Reinforcement.py 2220 2019-02-21 09:21:30Z Kevin $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

reinforcementSrv = TSMS_API.Web.Reinforcement.Service

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

            clrType = clr.GetClrType(reinforcementSrv)
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
            msg += ('\n出錯函式：TSMS_API.Web.Reinforcement.Service.{}({})'.format(
                theFunction.__name__,
                ', '.join(['{}={}'.format(k, v) for k, v in paramsDict.items()])
            ))
            msg += '\n詳細 API 呼叫的參數及過程請參照 "API.log"'

            # https://stackoverflow.com/questions/
            # 6062576/adding-information-to-an-exception
            e.args = (msg,)
            raise e
    return _wrapper


def f2_5_1():
    project = reinforcementSrv.FindProjects(tunnelId)[0] # 101年頭城段隧道維護工程
    projectId = project.Key
    print '維修專案名稱: %s (%d)' % (project.Value, projectId)
    
    tunnel2 = reinforcementSrv.FindTunnels(tunnelId)[0] # ALL
    tunnel2Id = tunnel2.Key
    print '隧道名稱: %s (%d)' % (tunnel2.Value, tunnel2Id)    
    
    #structureType = reinforcementSrv.FindStructureTypes(tunnel2Id)[0] # ALL
    #structureTypeId = structureType.Key
    #print '結構體類型: %s (%d)' % (structureType.Value, structureTypeId)     
    structureTypeId = 0
    
    #structure = reinforcementSrv.FindStructures(tunnel2Id, structureTypeId)[0] # ALL
    #structureId = structure.Key
    #print '結構體名稱: %s (%d)' % (structure.Value, structureId)     
    structureId = 0
    
    view = _log(reinforcementSrv.QueryWebView1)(tunnelId, projectId, tunnel2Id, structureTypeId, structureId)
    print
        
    print "維修補強紀錄列表:"                      
    showTable(view.RepairRecords, others=[
        ('修補前照片路徑', 'BeforePhoto'),
        ('修補後照片路徑', 'AfterPhoto'),
    ])
    print
        
    return view
    
def f2_5_2():
    project = reinforcementSrv.FindProjects(tunnelId)[0] # 101年頭城段隧道維護工程
    projectId = project.Key
    print '維修專案名稱: %s (%d)' % (project.Value, projectId)
    
    tunnel2 = reinforcementSrv.FindTunnels(tunnelId)[0] # ALL
    tunnel2Id = tunnel2.Key
    print '隧道名稱: %s (%d)' % (tunnel2.Value, tunnel2Id)    
        
    view = _log(reinforcementSrv.QueryWebView2)(tunnelId, projectId, tunnel2Id)
    print
        
    print "其他維修資料列表:"                      
    showTable(view.RepairOtherRecords)
    print
        
    return view    
            
if __name__ == '__main__':
    showMainMenu('2.5', 2, locals())
    