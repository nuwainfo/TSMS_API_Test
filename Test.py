#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: Test.py 2209 2019-02-14 06:19:50Z Kevin $

import unittest
import datetime

from API import TSMS_API

def getMessage(objectName, attrName):
    msg = ('\n{}.{} 物件為空，請參考 "API.log"'
           '\n尋找缺少的物件屬性是從哪個 API 及參數獲得').format(objectName, attrName)
    msg += '\n時間： ' + str(datetime.datetime.now()) + ')'
    return msg

class TestAPI(unittest.TestCase):
    """
    第二期功能為
    func228, func229, func2210, func2211
    func235, func236, func237, func238
    func213, func214
    func224, func225 雨量查詢擴充功能
    ，其餘為第一期功能
    """
    def testCommon(self):
        from API import enginerringOffice
        from API import tunnel
        from API import tunnelHierarcy
        
        self.assertEqual(enginerringOffice.Value, u"北區養護工程分局")
        self.assertEqual(tunnelHierarcy.section, u"頭城工務段")
        self.assertEqual(tunnelHierarcy.freeway, u"國道5號")        
        self.assertEqual(tunnel.Value, u"雪山隧道")
        
        # Other API test.
        self.assertTrue(TSMS_API.Web.QueryService.FindALLTunnel())
        
class TestPatrol(unittest.TestCase):

    def test2_1_1(self):
        from Patrol import f2_1_1
        
        v = f2_1_1()
        
        self.assertTrue(v.EventLogs)
        
    def test2_1_2(self):
        from Patrol import f2_1_2
        
        v = f2_1_2()
        
        self.assertTrue(v.FrequentInspectRecords)
        
class TestMonitor(unittest.TestCase):

    def test2_2_1(self):
        from Monitor import f2_2_1
        
        v = f2_2_1()
        
        self.assertTrue(v.ControlPts)
        self.assertTrue(v.Coordinate)
        
    def test2_2_2(self):
        from Monitor import f2_2_2
        
        v = f2_2_2()
        
        self.assertTrue(v.Monitor3DData)
        self.assertTrue(v.TimeChart1)
        self.assertTrue(v.TimeChart2)
        
        self.assertTrue(v.WarningChart)
        self.assertTrue(v.WarningData)
        
    def test2_2_3(self):
        from Monitor import f2_2_3
        
        v = f2_2_3()
        
        self.assertTrue(v.MonitorCrackData)
        self.assertTrue(v.TimeChart1)  
        
    def test2_2_4(self):
        from Monitor import f2_2_4
        
        v = f2_2_4()
        
        self.assertTrue(v.TimeChart1)
        self.assertTrue(v.TimeChart2)
        self.assertTrue(v.MonitorWaterData)
        self.assertTrue(v.MonitorSingleWaterData)
        
        self.assertTrue(v.WarningChart)
        
    def test2_2_5(self):
        from Monitor import f2_2_5
        
        v = f2_2_5()
        
        self.assertTrue(v.TimeChart1)
        self.assertTrue(v.TimeChart2)
        self.assertTrue(v.MonitorStackWaterData)   
        
    def test2_2_6(self):
        from Monitor import f2_2_6
        
        v = f2_2_6()
        
        self.assertTrue(v.InstallSectionInfoRecords)

    def test2_2_7(self):
        from Monitor import f2_2_7
        
        v = f2_2_7()
        
        self.assertTrue(v.MonitorRepairInfoRecords)

    def test2_2_8(self):
        from Monitor import f2_2_8

        v = f2_2_8()

        self.assertTrue(v.InstallInfo)
        self.assertTrue(v.microDispRecords)
        self.assertTrue(v.DispChart.XYChart1)
        self.assertTrue(v.DefChart.XYChart1)

    def test2_2_9(self):
        from Monitor import f2_2_9

        v = f2_2_9()

        self.assertTrue(v.InstallInfo)
        self.assertTrue(v.CeilingInstallDiagram)
        self.assertTrue(v.TimeChart1)
        self.assertTrue(v.TimeChart2)
        self.assertTrue(v.CeilingDefRecords)
        self.assertTrue(v.CeilingDefMaxValuesRecords)

    def test2_2_10(self):
        from Monitor import f2_2_10
        v = f2_2_10()

        self.assertTrue(v.InstallInfo)
        self.assertTrue(v.LevelingRecords)
        self.assertTrue(v.WarningRecords)
        self.assertTrue(v.LevelingChart)
        self.assertTrue(v.DateLevelingChart1)
        self.assertTrue(v.DateLevelingChart2)

    def test2_2_11(self):
        from Monitor import f2_2_11
        v = f2_2_11()

        self.assertTrue(v.InstallInfo)
        self.assertTrue(v.GeoDefRecords)
        self.assertTrue(v.GeoDefMarksRecords)
        self.assertTrue(v.TimeChartEast)
        self.assertTrue(v.TimeChartNorth)
        self.assertTrue(v.TimeChartUp)

class TestInspect(unittest.TestCase):

    def test2_3_1(self):
        from Inspect import f2_3_1
        
        v = f2_3_1()
        
        self.assertTrue(v.TunWallMap)
        self.assertTrue(v.TunRoadMap)
        self.assertTrue(v.TunInjureRecord)
        
    def test2_3_2(self):
        from Inspect import f2_3_2
        
        v = f2_3_2()
        
        self.assertTrue(v.NDTRecord)        
        #self.assertTrue(v.NDTMap)
        #self.assertTrue(v.NDTLegend)
        
    def test2_3_3(self):
        from Inspect import f2_3_3
        
        v = f2_3_3()

        objectName = 'Inspect.WebView3'
        
        self.assertTrue(v.TunSectorEvaluationRecord,
                        msg=getMessage(objectName, 'TunSectorEvaluationRecord'))
        self.assertTrue(v.TunInjurePercentCalChart,
                        msg=getMessage(objectName, 'TunInjurePercentCalChart'))
        self.assertTrue(v.RecordData,
                        msg=getMessage(objectName, 'RecordData'))
        self.assertTrue(v.RecordData2,
                        msg=getMessage(objectName, 'RecordData2'))
        
    def test2_3_4(self):
        from Inspect import f2_3_4
        
        v = f2_3_4()
        
        self.assertTrue(v.Sta1)
        self.assertTrue(v.Sta2)
        self.assertTrue(v.RefPhoto1)
        self.assertTrue(v.RefPhoto2)     
        self.assertTrue(v.OtherStructureRecord)

    def test2_3_5(self):
        from Inspect import f2_3_5

        v = f2_3_5()

        self.assertTrue(v.TunWallMap)
        self.assertTrue(v.TunRoadMap)
        self.assertTrue(v.TunInjureRecord)

    def test2_3_6(self):
        from Inspect import f2_3_6

        v = f2_3_6()

        self.assertTrue(v.ImageInfoRecord)

    def test2_3_7(self):
        from Inspect import f2_3_7

        v = f2_3_7()

        def assertProject(self, project):
            self.assertTrue(project.Option0RightPic)
            self.assertTrue(project.Option0LeftPic)
            self.assertTrue(project.Option1RightPic)
            self.assertTrue(project.Option1LeftPic)
            self.assertTrue(project.Option3Chart)
            self.assertTrue(project.Option2Records)
            self.assertTrue(project.Option4Records)

        assertProject(self, v.project1)
        assertProject(self, v.project2)
        assertProject(self, v.project3)

    def test2_3_8(self):
        from Inspect import f2_3_8

        v = f2_3_8()

        self.assertTrue(v.Records)

class TestShaft(unittest.TestCase):

    def test2_4_1(self):
        from Shaft import f2_4_1
        
        v = f2_4_1()
        
        self.assertTrue(v.Labels)
        self.assertTrue(v.Values)
        self.assertTrue(v.ShaftRecords)
        self.assertTrue(v.RefImage)
        self.assertTrue(v.MediaRecords)
        
class TestPattern(unittest.TestCase):

    def test2_7_1(self):
        from Pattern import f2_7_1
        
        v = f2_7_1()
        
        self.assertTrue(v.DamagePatterns)
        
class TestGeology(unittest.TestCase):

    def test2_8_1(self):
        from Geology import f2_8_1
        
        v = f2_8_1()
        
        self.assertTrue(v.OpStationStart)
        self.assertTrue(v.OpStationEnd)
        self.assertTrue(v.RMRRecord)
        self.assertTrue(v.RMRChart)
        self.assertTrue(v.RockStyleChart)
        self.assertTrue(v.SupportVChart)
        
    def test2_8_2(self):
        from Geology import f2_8_2
        
        v = f2_8_2()
        
        self.assertTrue(v.RefGeoMap)
        self.assertTrue(v.RefGeoLegend)
        self.assertTrue(v.GeologyInfoList)
        
class TestBookbase(unittest.TestCase):

    def test2_9_1(self):
        from Bookbase import f2_9_1
        
        v = f2_9_1()
        
        self.assertTrue(v.StartCity)        
        self.assertTrue(v.EndCity)   
        self.assertTrue(v.StructureInfoRecords)
        
    def test2_9_2(self):
        from Bookbase import f2_9_2
        
        v = f2_9_2()
        
        self.assertTrue(v.ReportDocRecords)
        
    def test2_9_3(self):
        from Bookbase import f2_9_3
        
        v = f2_9_3()
        
        self.assertTrue(v.BuiltDrawingRecords)        
        
    def test2_9_4(self):
        from Bookbase import f2_9_4
        
        v = f2_9_4()
        
        self.assertTrue(v.MaintainTypeRecords)           
        
        m = v.MaintainTypeRecords[0]
        
        self.assertTrue(m.Level1)
        self.assertTrue(m.Level2)
        self.assertTrue(m.Method)
        self.assertTrue(m.PriceAnalysisRecords, getMessage(
            'Bookbase.WebView4', 'PriceAnalysisRecords'))
        
    def test2_9_5(self):
        from Bookbase import f2_9_5
        
        v = f2_9_5()
        
        self.assertTrue(v.PhotoRecords)         
        
if __name__ == '__main__':
    unittest.main()
