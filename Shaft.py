#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Shaft.py 2220 2019-02-21 09:21:30Z Kevin $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

shaftSrv = TSMS_API.Web.Shaft.Service

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

            clrType = clr.GetClrType(shaftSrv)
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
            msg += ('\n出錯函式：TSMS_API.Web.Shaft.Service.{}({})'.format(
                theFunction.__name__,
                ', '.join(['{}={}'.format(k, v) for k, v in paramsDict.items()])
            ))
            msg += '\n詳細 API 呼叫的參數及過程請參照 "API.log"'

            # https://stackoverflow.com/questions/
            # 6062576/adding-information-to-an-exception
            e.args = (msg,)
            raise e
    return _wrapper

def f2_4_1():
    shaft = shaftSrv.FindShafts(tunnelId)[4] # 三號豎井進氣井
    shaftId = shaft.Key
    print '結構物: %s (%d)' % (shaft.Value, shaftId)
    
    # 98年度頭城段
    proj = _log(shaftSrv.FindProjects)(tunnelId, shaftId)[0]
    projId = proj.Key
    print '本期檢測專案: %s (%d)' % (proj.Value, projId)
    
    view = _log(shaftSrv.QueryWebView1)(tunnelId, shaftId, projId)
    print
    
    for h, v in zip(view.Labels, view.Values):
        print '%s: %s' % (h, v)
    print
    
    print "損傷列表:"                      
    showTable(view.ShaftRecords, others=[('檔案路徑', 'File'),])
    print

    print "參考圖檔:"
    print view.RefImage
    print    
    
    print "影像資料列表:"                      
    showTable(view.MediaRecords, others=[('檔案路徑', 'File'),])
    print    
        
    return view
            
if __name__ == '__main__':
    showMainMenu('2.4', 1, locals())
    