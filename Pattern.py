#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Pattern.py 2220 2019-02-21 09:21:30Z Kevin $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

patternSrv = TSMS_API.Web.Pattern.Service

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

            clrType = clr.GetClrType(patternSrv)
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
            msg += ('\n出錯函式：TSMS_API.Web.Pattern.Service.{}({})'.format(
                theFunction.__name__,
                ', '.join(['{}={}'.format(k, v) for k, v in paramsDict.items()])
            ))
            msg += '\n詳細 API 呼叫的參數及過程請參照 "API.log"'

            # https://stackoverflow.com/questions/
            # 6062576/adding-information-to-an-exception
            e.args = (msg,)
            raise e
    return _wrapper

def f2_7_1():
    df = patternSrv.FindDamageForces()[0] # ALL
    dfId = df.Key
    print '肇因類別: %s (%d)' % (df.Value, dfId)
        
    view = _log(patternSrv.QueryWebView1)(tunnelId, dfId)
    print
        
    print "隧道損傷型態資訊:"                      
    for p in view.DamagePatterns:
        print '  損傷型態照片路徑:', p.ExpandMap
        print '  異狀成因:', p.Causes
        print '  荷載位置:', p.LoadingDir
        print '  特徵說明:', p.Feature
        print '  發表人/單位:', p.Source
        print '  提供者:', p.Provider
        print '  立視圖路徑:', p.PerspectiveView
    print
        
    return view
            
if __name__ == '__main__':
    showMainMenu('2.7', 1, locals())
    