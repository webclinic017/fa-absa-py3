
"""----------------------------------------------------------------------------
MODULE
    FRepoProcessing - Code for rerating and terminating open end repo 
    instruments.

    (c) Copyright 2005 by Front Capital Systems AB. All rights reserved.

DESCRIPTION

----------------------------------------------------------------------------"""
import acm
import ael
import datetime
  
def openEndReRate(invokationInfo):
    cells = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    func=acm.GetFunction('msgBox', 3)
    doReRate = func("Warning", "New rate will be applied for selected trades. Continue?", 1)
    if doReRate == 1:
        for cell in cells:
            tag = cell.Tag()
            column = cell.Column()
            columnId = column.ColumnId()
            context = column.Context().Name()
            if str(columnId) == "New Rate":
                row = cell.RowObject()
                instrument = row.Instrument()
                if isValidForOpenEndReRate(instrument):
                    newRate = acm.GetCalculatedValueFromString(instrument, context, 'openEndNewRate', tag).Value()
                    rerateDate = acm.GetCalculatedValueFromString(instrument, context, 'openEndRerateDate', tag).Value()  
                    today=acm.Time.DateToday()
                    func = acm.GetFunction('asDate', 1)
                    rerateDate = func(rerateDate)
                    if (newRate and rerateDate):
                        ins = ael.Instrument[instrument.Oid()]
                        if rerateDate>today:
                            func=acm.GetFunction('msgBox', 3)
                            func("Error", "Trade has already been extended.", 1)
                        else:
                            try:
                                ins.re_rate(ael.date(rerateDate), newRate)
                            except:
                                print ins.insid
                    else:
                        func=acm.GetFunction('msgBox', 3)
                        func("Error", "Please enter the New Rate for the Open End trade.", 1)

   
def openEndTerminate(invokationInfo):
    cells = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedCells()
    func=acm.GetFunction('msgBox', 3)
    doTerminate = func("Warning", "The selected trades will be terminated. Continue?", 1)
    if doTerminate == 1:
        for cell in cells:
            tag = cell.Tag()
            column = cell.Column()
            columnId = column.ColumnId()
            context = column.Context().Name()
            if str(columnId) == "Termination Date":
                row = cell.RowObject()
                instrument = row.Instrument()
                if isValidForOpenEndTerminate(instrument):
                    terminateDate = acm.GetCalculatedValueFromString(instrument, context, 'openEndTerminateDate', tag).Value()  
                    func=acm.GetFunction('asDate', 1)                    
                    terminateDate = func(terminateDate)
                    if terminateDate:
                        ins = ael.Instrument[instrument.Oid()]
                        ins.terminate_open_end(ael.date(terminateDate))
                    else:
                        func=acm.GetFunction('msgBox', 3)
                        func("Error", "Please enter the Termination Date for the Open End trade.", 1)


def isValidInsType(object):
    if object:
        if object.IsKindOf('FRepo') or object.IsKindOf('FSecurityLoan') or object.IsKindOf('FBasketRepo') or object.IsKindOf('FBasketSecurityLoan') or object.IsKindOf('FDeposit'):
            return True
    return False
    
def isValidForOpenEndReRate(object):
    if isValidInsType(object):
        if object.OpenEnd() == 'Open End':
            leg = object.Legs().At(0)
            if leg and leg.LegType() == 'Fixed Adjustable' or leg.LegType() == 'Call Fixed Adjustable':
                return True
    return False

def isValidForOpenEndTerminate(object):
    if isValidInsType(object):
        if object.OpenEnd() == 'Open End':
            return True
    return False
