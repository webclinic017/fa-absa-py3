
import acm
import os
import FOrderFlowController
import FOrderFlowRecorderDlg
from datetime import datetime
import time

"""----------------------------------------------------------------------------

MODULE

    RecordOrderFlows: Task for recording order flow in a specific market segment
    
    (C) Copyright 2011 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module is used for recording order flows of the order books in a market segment.

NOTES:
    
------------------------------------------------------------------------------"""

# Helper class for saving order flows
class OrderFlowsSaveInfo():
    def __init__(self, handlers, path, filePostFix, fileType):
        self.handlers = handlers
        self.path = path
        self.filePostFix = filePostFix
        self.fileType = fileType
    
    def CreateFilePath(self, orderBook):
        fileName = self.path
        if not fileName.endswith('\\') and not fileName.endswith('/'):
            fileName = fileName + '\\'
        return fileName + orderBook.Name() + self.filePostFix + self.fileType
        
    def Save(self):
        for handler in self.handlers:
            orderBook = handler.Recorder().TradingInterface()
            try:
                fileName = self.CreateFilePath(orderBook)
                FOrderFlowController.exportOrderFlow(handler.OrderFlow(), fileName)
                print ('Saved order flow for ' + orderBook.StringKey() + ' at ' + fileName)
            except:
                print ('Failed to save order flow for', orderBook.Name())
            
# Record order flow for order books in market segment
def recordOrderFlows(marketSegment, startTime, stopTime):
    handlers = []
    segment = acm.FMarketSegment[marketSegment]
    if segment != None:
        orderBooks = segment.OrderBooks()
        if orderBooks != None:
            for ob in orderBooks:
                handlers.append(recordOrderFlow(ob, startTime, stopTime))
    return handlers
    
# Record order flow for order book
def recordOrderFlow(orderBook, startTime, stopTime):
    handler = FOrderFlowRecorderDlg.OrderFlowRecorderHandler(acm.FOrderFlowRecorder(orderBook))
    handler.Start(startTime)
    handler.Stop(stopTime)
    return handler

# Return path selection
def filePathSelection():
    selection = acm.FFileSelection()
    selection.PickDirectory(True)
    return selection   

# Save order flow files
def onSave(saveInfo):
    saveInfo.Save()

ael_variables = [
    ['segment', 'Market Segment', 'string', None, None,  1, 0, 'Market Segment for the order book order flows to be recorded', None, None], 
    ['orderFlowPath', 'Save Path', filePathSelection(), None, filePathSelection(),  1, 1,\
    'The save path of the order flow files for the order books in the selected market segment.', None, 1],
    ['fileDateFormat', 'Format of Date Added to File Name', 'string', ['%d%m%y', '%y%m%d'], '',\
    0, 0, 'Format of the date added to the file name. No date is added to the file name if this field is left blank', None, None],
    ['startTime', 'Start Time (H:M:S)', 'string', None, None,  1, 0, 'The start time of the recording.', None, None],
    ['stopTime', 'Stop Time (H:M:S)', 'string', None, None, 1, 0, 'The stop time of the recording', None, None]
    ]

def ael_main(dictionary):
    local = time.localtime()
    localStart = time.strptime(dictionary['startTime'], '%H:%M:%S')
    localStop = time.strptime(dictionary['stopTime'], '%H:%M:%S')    
    startTime = acm.Time.LocalTimeAsUTCDays(local.tm_year, local.tm_mon, local.tm_mday, localStart.tm_hour, localStart.tm_min, localStart.tm_sec, 0)
    stopTime = acm.Time.LocalTimeAsUTCDays(local.tm_year, local.tm_mon, local.tm_mday, localStop.tm_hour, localStop.tm_min, localStop.tm_sec, 0) 
    
    handlers = recordOrderFlows(dictionary['segment'], startTime, stopTime)
    fileSelection = dictionary['orderFlowPath']
    filePath = fileSelection.SelectedDirectory().StringKey()
    fileDateFormat = dictionary['fileDateFormat']
    filePostFix = ''
    if fileDateFormat and fileDateFormat != '':
        filePostFix = time.strftime(fileDateFormat)
    fileType = '.fof'
    
    saveInfo = OrderFlowsSaveInfo(handlers, filePath, filePostFix, fileType)
    timer = acm.GetFunction('timer', 0)()
    timer.CreateTimerEventAt(stopTime, onSave, saveInfo)
    timeFormatter = acm.Get('formats/TimeOnly')
    print ('Record order flows for market segment ' + dictionary['segment'] + ' ' + timeFormatter.Format(startTime) + ' - ' + timeFormatter.Format(stopTime))
