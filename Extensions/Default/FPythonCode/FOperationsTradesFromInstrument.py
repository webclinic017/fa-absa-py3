""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsTradesFromInstrument.py"
import acm
import FOperationsUtils as Utils
from FOperationsEnums import InsType, LegType

def GetTrades(obj):
    trades = list()
    if obj.IsKindOf(acm.FTrade):
        trades.append(obj)
    elif obj.IsKindOf(acm.FInstrument):
        for trade in GetTradesFromInstrument(obj):
            trades.append(trade)
    return trades

def GetTradesFromInstrument(instrument):
    combInsList = __GetCombinationsForInstrument(instrument)
    undInsList = __GetDerivatesForInstrument(instrument)
    trsList = __GetTRSForInstrument(instrument)

    insList = []
    for ins in (combInsList + undInsList + trsList):
        __AddToListNoDuplicates(ins, insList)

    return __GetTradesForInstrumentList(insList)

def __GetCombinationsForInstrument(ins):
    ''' Help function that get all the combination instruments where the
        given instrument is used as member somewhere in the hierarchy '''

    combInsList = list()
    combInsList.append(ins)
    __GetCombinationsForInstrumentCore(ins, combInsList)
    return combInsList

def __GetDerivatesForInstrument(ins):
    ''' Help function for getting all instrument where the instrument
        is used as underlying '''

    underlyingList = list()
    returnedList = list()
    for ins in acm.FInstrument.Select('underlying = %d' % ins.Oid()):
        underlyingList.append(ins)
        returnedList.append(ins)
    for ins in underlyingList:
        combList = __GetCombinationsForInstrument(ins)
        for i in combList:
            __AddToListNoDuplicates(i, returnedList)
    return returnedList

def __GetCombinationsForInstrumentCore(ins, combInsList):
    ''' The recursive function what can loop through the combination hierarchy '''

    combLinksList = acm.FCombInstrMap.Select('instrument = %d' % ins.Oid())
    for combLink in combLinksList:
        try:
            combIns = combLink.Combination()
            combInsList.append(combIns)
            __GetCombinationsForInstrumentCore(combIns, combInsList)
        except RuntimeError as re:
            Utils.LogAlways('Incorrect combination link. Cause: %s' % re)
    return combInsList

def __AddToListNoDuplicates(instrument, instrumentList):
    for ins in instrumentList:
        if ins.Oid() == instrument.Oid():
            break
    else:
        instrumentList.append(instrument)

def __GetTRSForInstrument(instrument):
    trsList = []
    returnedList = []
    if instrument.InsType() == InsType.STOCK:
        query = acm.CreateFASQLQuery(acm.FLeg, 'AND')
        query.AddAttrNode('Instrument.InsType', 'EQUAL', Utils.GetEnum('InsType', InsType.TOTAL_RETURN_SWAP))
        query.AddAttrNode('LegType', 'EQUAL', Utils.GetEnum('LegType', LegType.TOTAL_RETURN))
        query.AddAttrNode('IndexRef.Oid', 'EQUAL', instrument.Oid())
        resultSet = query.Select()
        for leg in resultSet:
            trsList.append(leg.Instrument())
            returnedList.append(leg.Instrument())
        for ins in trsList:
            combList = __GetCombinationsForInstrument(ins)
            for i in combList:
                __AddToListNoDuplicates(i, returnedList)
    return returnedList

def __GetTradesForInstrumentList(insList):
    ''' Help function for getting all trades from a list of instruments '''

    tradeList = list()
    for ins in insList:
        for trd in ins.Trades():
            tradeList.append(trd)
    return tradeList