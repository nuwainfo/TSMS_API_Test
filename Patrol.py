#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Patrol.py 2220 2019-02-21 09:21:30Z Kevin $

import sys
import os

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

patrolSrv = TSMS_API.Web.Patrol.Service

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

            clrType = clr.GetClrType(patrolSrv)
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
            msg += ('\n出錯函式：TSMS_API.Web.Patrol.Service.{}({})'.format(
                theFunction.__name__,
                ', '.join(['{}={}'.format(k, v) for k, v in paramsDict.items()])
            ))
            msg += '\n詳細 API 呼叫的參數及過程請參照 "API.log"'

            # https://stackoverflow.com/questions/
            # 6062576/adding-information-to-an-exception
            e.args = (msg,)
            raise e
    return _wrapper

def f2_1_1():
    stage = patrolSrv.FindStages()[0] # 施工階段
    stageId = stage.Key
    print '階段類別: %s (%d)' % (stage.Value, stageId)
        
    view = _log(patrolSrv.QueryWebView1)(tunnelId, stageId)
    print

    for log in view.EventLogs:
        print '%s - %s:' % (log.Year, log.Event)
        for h, v in zip(log.Labels, log.Values):
            print '  %s: %s' % (h, v)
        print

    print '新增大事紀資料'
    print '=' * 50
    structure = TSMS_API.Web.QueryService.FindStructures(tunnelId)[0] # 南下線
    structureId = structure.Key
    print '結構物: %s (%d)' % (structure.Value, structureId)

    from System.Collections.Generic import *

    values = List[str]([
        '100k',
        '2013/04/26',
        '2013/04/26',
        '沒事',
        '就說沒事',
        ''
    ])
    print values
    ok = patrolSrv.CreateEventLog(tunnelId, 1, structureId, values)
    print '成功?', ok
    print

    id = _log(patrolSrv.QueryWebView1)(tunnelId, stageId).EventLogs[len(view.EventLogs)].EventId

    print '更新大事紀資料'
    print '=' * 50
    values = List[str]([
        '150k',
        '2013/04/26',
        '2013/04/26',
        '沒事',
        '就說沒事',
        ''
    ])
    print id, values
    ok = patrolSrv.UpdateEventLog(id, tunnelId, 1, structureId, values)
    print '成功?', ok

    print '刪除大事紀資料'
    print '=' * 50
    print id
    ok = patrolSrv.DeleteEventLog(id)
    print '成功?', ok

    return view

from System.Collections.Generic import *

def f2_1_2():
    xml = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Data',
                          '經常巡查2013_05_01.xml'))

    print "匯入經常巡查列表:", xml
    ok = patrolSrv.ImportFrequentInspectRecord(xml)
    print ok
    print

    view = _log(patrolSrv.QueryWebView2)(tunnelId)
    print

    print "經常巡查列表:"
    showTable(view.FrequentInspectRecords, others=[('Id', 'InspectId'),])
    print

    def update(idx, fixed):
        record = view.FrequentInspectRecords.Rows[idx]
        id = record.InspectId

        print '更新經常巡查資料'
        print '=' * 50
        values = List[str]([
            '%s' % getattr(record, 'Data%d' % (i + 1))
            for i in range(len(view.FrequentInspectRecords.Headers))])

        from System import DateTime, String
        import time
        values[2] = '%sk' % str(time.time()) # 里程
        values[11] = fixed
        values[5] = String.Format("{0:yyyy/M/d}", DateTime.Now.Date)

        print id, values
        ok = _log(patrolSrv.UpdateFrequentInspectRecord)(id, tunnelId, values)
        print '成功?', ok
        print

    update(0, '否')
    update(1, '是')

    # Query by 是否維修
    view2 = _log(patrolSrv.QueryWebView2)(tunnelId, '否')
    print
    
    print "經常巡查列表 (用是否維修:否 來查詢):"
    showTable(view2.FrequentInspectRecords, others=[('Id', 'InspectId'),])
    print
    
    # We MUST delete all imported records because of TSMS's suck API.
    for record in view.FrequentInspectRecords.Rows:
        ok = patrolSrv.DeleteFrequentInspectRecord(record.InspectId)
        print '刪除經常巡查', record.InspectId, '成功?', ok
        
    # WARN! THERE WILL BE STILL ONE RECORD REMAINED IN DB, BECAUSE OF ITS
    # TUNNEL ID IS NOT tunnelId.
                
    return view
        
if __name__ == '__main__':
    showMainMenu('2.1', 2, locals())
