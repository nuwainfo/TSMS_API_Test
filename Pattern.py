#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Pattern.py 435 2013-05-09 11:37:05Z Bear $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

patternSrv = TSMS_API.Web.Pattern.Service

def f2_7_1():
    df = patternSrv.FindDamageForces()[0] # ALL
    dfId = df.Key
    print '肇因類別: %s (%d)' % (df.Value, dfId)
        
    view = patternSrv.QueryWebView1(tunnelId, dfId)
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
    