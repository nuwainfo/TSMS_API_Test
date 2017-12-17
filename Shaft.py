#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Shaft.py 417 2013-05-07 11:43:37Z Bear $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

shaftSrv = TSMS_API.Web.Shaft.Service

def f2_4_1():
    shaft = shaftSrv.FindShafts(tunnelId)[4] # 三號豎井進氣井
    shaftId = shaft.Key
    print '結構物: %s (%d)' % (shaft.Value, shaftId)
    
    # 98年度頭城段
    proj = shaftSrv.FindProjects(tunnelId, shaftId)[0]
    projId = proj.Key
    print '本期檢測專案: %s (%d)' % (proj.Value, projId)
    
    view = shaftSrv.QueryWebView1(tunnelId, shaftId, projId)
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
    