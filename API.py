#!/usr/bin/env ipy
# -*- coding: utf-8 -*-
# $Id: API.py 1841 2018-03-20 22:46:23Z Kevin $

import clr
import sys, os

sys.path.append(os.path.abspath('.'))
clr.AddReference('TSMS_API')

# add a environment variable let log4let make log file in right path
os.environ.update({'PWD': os.getcwd()})

sys.path.append(os.path.abspath('.\\TSMS_API_Web\\bin\\Debug'))
clr.AddReference('TSMS_API_Web')

import TSMS_API

# ============================================================================
# Utility functions
# ============================================================================

import codecs
import cStringIO as StringIO

def utf8(s):
    """
    Convert a string (UNICODE or ANSI) to a utf8 string.

    @param s String.
    @return UTF8 string.
    """
    info = codecs.lookup('utf8')
    try:
        out = StringIO.StringIO()
        srw = codecs.StreamReaderWriter(out,
                info.streamreader, info.streamwriter, 'strict')
        srw.write(s)
        return out.getvalue()
    except UnicodeError:
        # Try again by forcing convert to unicode type first.
        srw.write(_unicode(s, strict=True))
        return out.getvalue()
    finally:
        srw.close()
        out.close()

def showTable(tableView, others=[], output=''):
    """
    Show TableView<> to console.
    
    @param tableView TableView object.
    @param others Any other columns to display, a list of tuples which 
                  represent (header, field name).
    @param output Output file name.
    """
    from prettytable import PrettyTable
    x = PrettyTable()
    x.field_names = list(tableView.Headers) + [v[0] for v in others]
    for r in tableView.Rows:        
        x.add_row([getattr(r, 'Data%d' % (i + 1)) 
                   for i in range(len(tableView.Headers))] + 
                   [getattr(r, v[1]) for v in others])
        
    print unicode(x)
    
    if output:
        with open(output, 'wb') as f:
            f.write(utf8(unicode(x)))
    return x
    
def showChart(chartView, attr='Values'):
    print '圖例數:', len(getattr(chartView, attr))
    for i, v in enumerate(getattr(chartView, attr)):
        print '圖例%d 共有 %d 個資料點' % (i + 1, len(v))

def showMainMenu(fid, subn, handlerDict):
    for i in range(subn):
        n = i + 1
        print n, ':', '%s.%d' % (fid, n)
    
    c = None
    while c is None:
        c = raw_input("Choose sub functions:")    
        print
        try:
            handlerDict['f%s_%s' % (fid.replace('.', '_'), c)]()
        except Exception, e:
            #print str(e)            
            
            import traceback
            for l in traceback.format_exception(*sys.exc_info()):
                print l
                
            raise
            c = None

# ============================================================================    
    
print 'ConnectionString:', TSMS_API.API.Settings.Instance.ConnectionString
print

# Hardcode for demo:
# 北工處
enginerringOffice = TSMS_API.Web.QueryService.FindALLEngineeringOffice()[0]
enginerringOfficeId = enginerringOffice.Key
#print '工程處: %s (%d)' % (enginerringOffice.Value, enginerringOfficeId)

# 雪山遂道
tunnel = TSMS_API.Web.QueryService.FindTunnelsByEnginerringOffice(enginerringOfficeId)[4]
tunnelId = tunnel.Key

sectionId = TSMS_API.API.Service.FindSectionidByTunid(tunnelId)

tunnelHierarcy = TSMS_API.Web.QueryService.GetTunnelHierarcy(tunnelId)
print '工程處: %s (%d)' % (tunnelHierarcy.engineeringOffice, enginerringOfficeId)
print '工務段: %s (%d)' % (tunnelHierarcy.section, sectionId)
print '國道: %s' % tunnelHierarcy.freeway

print '遂道: %s (%d)' % (tunnel.Value, tunnelId)
