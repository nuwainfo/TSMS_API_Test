#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Reinforcement.py 464 2013-05-17 02:59:48Z Bear $

import sys

from API import TSMS_API
from API import tunnelId, enginerringOfficeId

from API import showTable, showChart, showMainMenu

reinforcementSrv = TSMS_API.Web.Reinforcement.Service

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
    
    view = reinforcementSrv.QueryWebView1(tunnelId, projectId, tunnel2Id, structureTypeId, structureId)
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
        
    view = reinforcementSrv.QueryWebView2(tunnelId, projectId, tunnel2Id)
    print
        
    print "其他維修資料列表:"                      
    showTable(view.RepairOtherRecords)
    print
        
    return view    
            
if __name__ == '__main__':
    showMainMenu('2.5', 2, locals())
    