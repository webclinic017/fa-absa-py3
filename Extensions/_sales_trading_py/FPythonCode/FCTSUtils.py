""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FCTSUtils.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    FCTSUtils

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm

from FIntegratedWorkbenchUtils import IsKindOf
from FSalesTradingLogging import logger


def _GetClientFromGrouping(obj):
    grp = obj.Grouping().GroupingValue()
    logger.debug("_GetClientFromGrouping() %s class: %s Is Client: %s" % (grp.StringKey(), grp.ClassName(), IsKindOf(grp, acm.FCounterParty)))
    if IsKindOf(grp, acm.FCounterParty):
        return grp
    else:
        return None

def GetClientFromFObject(obj):
    """ Given a FObject, determine client. """
    logger.debug("GetClientFromFObject() %s of %s" % (obj.StringKey(), obj.ClassName()))
    client = None
    if IsKindOf(obj, acm.FMultiInstrumentAndTrades):
        client = _GetClientFromGrouping(obj)
    elif IsKindOf(obj, acm.FPortfolioInstrumentAndTrades):
        client = acm.FCounterParty[obj.Name()]
    elif IsKindOf(obj, acm.FSingleInstrumentAndTrades):
        parent = obj.Parent()
        if parent:
            if IsKindOf(parent, acm.FMultiInstrumentAndTrades):
                client = _GetClientFromGrouping(parent)
            elif IsKindOf(parent.Parent(), acm.FMultiInstrumentAndTrades):
                client = _GetClientFromGrouping(parent.Parent())
    elif IsKindOf(obj, acm.FTradeRow):
        client = obj.Trade().Counterparty()

    return client

def GetInstrumentFromFObject(obj):
    if IsKindOf(obj, acm.FInstrument):
        return obj
    elif hasattr(obj, 'Instrument'):
        return obj.Instrument()
    else:
        return None

def GetInstrumentsFromExtObject(extensionObject):
    if extensionObject.IsKindOf(acm.CInsDefAppFrame):
        return [extensionObject.OriginalInstrument()]
    elif extensionObject.IsKindOf(acm.FUiTrdMgrFrame):
        if extensionObject.ActiveSheet().Selection().SelectedInstruments():
            return extensionObject.ActiveSheet().Selection().SelectedInstruments()
        elif extensionObject.ActiveSheet().Selection().SelectedOrderBooks():
            return [ob.Instrument() for ob in extensionObject.ActiveSheet().Selection().SelectedOrderBooks()]
        else: #No asset selected
            return []
    elif extensionObject.IsKindOf(acm.FTrade):
        return [extensionObject.Instrument()]
    elif extensionObject.IsKindOf(acm.FArray):
        if extensionObject.Size() > 0:
            if extensionObject[0].IsKindOf(acm.CInsDefAppFrame):
                return [obj.OriginalInstrument() for obj in extensionObject]
            elif extensionObject[0].IsKindOf(acm.FTrade):
                return [obj.Instrument() for obj in extensionObject]
        else:
            raise ValueError
    return extensionObject

def GetDivStreamFromInstrument(instrument):
    if instrument.IsKindOf(acm.FInstrument):
        dividendStream = instrument.MappedDividendStream().Parameter()
        if dividendStream:
            return dividendStream
        elif instrument.Underlying():
            return GetDivStreamFromInstrument(instrument.Underlying())
        else:
            return None

def GetUserPreferences():
    preferences = acm.FPreferences.Select01('user = %s' % acm.UserName(), None)
    if preferences is None:
        preferences = acm.FPreferences()
        preferences.Name(acm.UserName())
        preferences.Commit()
    return preferences

