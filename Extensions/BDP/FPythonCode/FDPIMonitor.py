""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FDPIMonitor.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FDividendPointIndexDividendMonitor

    (c) Copyright 2018 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    The module monitors for updates to the dividend table and
    regenerates Dividend Point Index Instruments' cashflows accordingly.

----------------------------------------------------------------------------"""
import acm, ael
import FDividendPointIndexProcessingPerform
import FBDPCommon

class DPIMonitor():
    def __init__(self):
        self._messageQueue = []
    
    def pushItem(self, item):
        self._messageQueue.append(item)
    
    def popItem(self):
        return self._messageQueue.pop(0)
        
    def work(self):
        while len(self._messageQueue) > 0:
            try:
                dpis = getDividendPointIndexes(self.popItem())
                task_dictionary = {
                    'Testmode' : 0,
                    'StartDate' : acm.Time.DateToday(),
                    'EndDate' : acm.Time.DateToday(),
                    'Logmode' : 2,
                    'Instruments' : dpis,
                    'LogToFile' : 0,
                    'ReportMessageType' : 'Full Log'
                }
                FBDPCommon.execute_script(FDividendPointIndexProcessingPerform.perform, task_dictionary)
            except Exception as e:
                import traceback
                s = 'Failed to process dividend\n' + traceback.format_exc()            
                acm.Log(s)

def getDividendPointIndexes(dividend):
    insts = set()
    if dividend is None:
        return
    instrument = dividend.Instrument()
    #may be a stock or an equityindex
    if instrument.IsKindOf(acm.FEquityIndex):
        legs = acm.FLeg.Select('indexRef=' + instrument.Name())
        for leg in legs:
            insts.add(leg.Instrument())
    else:
        pass
    return list(insts)

"""---------------------------------------------------------------
ATS interface methods.
---------------------------------------------------------------"""
def start():
    acm.Log('FDividendPointIndexDividendMonitor started')
    acm.Log('Starting dividend subscription')
    ael.Dividend.subscribe(dividend_update_cb)
    global dpiMonitor
    dpiMonitor = DPIMonitor()

def stop():
    acm.Log('Stopping dividend subscription')
    ael.Dividend.unsubscribe(dividend_update_cb)
    acm.Log('FDividendPointIndexDividendMonitor stopped')

def status():
    pass

def work():
    global dpiMonitor
    if dpiMonitor:
        dpiMonitor.work()

def dividend_update_cb(obj, dividend, arg, event):
    div_oid = dividend.seqnbr
    div = acm.FDividend[div_oid]
    global dpiMonitor
    if dpiMonitor:
        dpiMonitor.pushItem(div)
