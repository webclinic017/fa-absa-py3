""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/FSecLendColumns.py"

from __future__ import print_function
"""------------------------------------------------------------------------------------------------
MODULE
    FSecLendColumns

    (c) Copyright 2017 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Contains supporting functions for columns used by workbenches.

------------------------------------------------------------------------------------------------"""
import acm
import operator
from collections import Counter
from collections import defaultdict

import FSecLendHoldTrade
import FSecLendHooks
import FSecLendUtils

logger = FSecLendUtils.Logger()
SEC_LEND_RESPOND_STATE = 'Awaiting Reply'

# Used as OnPostInputHook for column Hold Time
def HoldTime(row, col, calcval, input, operation):
    trade = row.Originator().Trade()
    hasTimePast = FSecLendHoldTrade.IsTimePastHoldTime(trade)
    if IsOwnOrder(row, col, calcval, input, operation) and input and not hasTimePast:
        trade.Status(FSecLendHooks.OnHoldTradeStatus())
        return input
    FSecLendHoldTrade.UnholdTrade(trade)
    return 0


# Custom fuction used for coloring column Security Loan Trade Origin Id
def SetColor(originId):
    if not originId:
        return 0
    if originId % 100 > 50:
        return originId % 10 + 1
    elif originId % 100 < 50:
        return originId % 10 + 11
    else:
        return 0


def TargetSource(trade):
    bps = acm.BusinessProcess.FindBySubjectAndStateChart(trade, FSecLendHooks.WorkflowStateChart.NAME)
    if bps and bps.First().CurrentStateName() == SEC_LEND_RESPOND_STATE:
        diary = bps.First().CurrentStep().DiaryEntry()
        if diary and diary.Parameters() and diary.Parameters().HasKey("TargetSource"):
            return diary.Parameters().At('TargetSource', '')


def IsColumnModificationAllowed(row, col, calcval, input, operation):

    def TransformColumnInput(row, col, calcval, input, operation):
        if input == '-':
            if str(col.Method()) == 'Instrument.StartingFee':
                return str(-calcval.Value()*100)
            elif str(col.Method()) == 'FaceValue':
                return str(-calcval.Value())
        if input in ('*', 's') and str(col.Method()) == 'Instrument.StartingFee':
            # Set Fee to Suggested Fee
            try:
                suggestedFee = acm.GetCalculatedValueFromString(calcval.RowObject(), col.Context(),
                                                                "secLendSuggestedFee", calcval.Tag())
                return col.Formatter().Format(suggestedFee.Value())
            except Exception as e:
                logger.error('Failed to calculate suggested fee - %s' % e)
                return 0
        
        return input
    
    return TransformColumnInput(row, col, calcval, input, operation) \
            if IsOwnOrder(row, col, calcval, input, operation) else 0


def CountsByProperty(objects, propertyName):
    properties = propertyName.split('.')

    def PropertyValue(obj):
        try:
            value = obj
            for prop in properties:
                value = getattr(value, prop)()
            return value
        except AttributeError:
            return None

    values = (PropertyValue(o) for o in objects)
    return Counter([v for v in values if v is not None])


def HighestCounts(counts, maxCounts=1, collapseRemaining=False):
    # Convert from FVariantDictionary
    counts = Counter({k: abs(counts.IntAt(k)) for k in counts.Keys()})
    mostCommon = counts.most_common()
    highestCounts = dict(mostCommon[:maxCounts])
    if collapseRemaining:
        remainingCount = sum([v for k, v in mostCommon[maxCounts:]])
        if remainingCount:
            highestCounts['Other'] = remainingCount
    return highestCounts


def CountsString(counts):
    values = sorted(counts.Keys(), key=lambda k: counts.IntAt(k), reverse=True)
    return ', '.join(values)


def QueryResults(queryResult):
    if queryResult:
        if queryResult.IsDirty():
            queryResult.ApplyChanges()
        return queryResult.Result()
    return acm.FIndexedCollection()


def TradesPerCounterparty(trades):
    # Dictionary with counterparties as keys and trades as values
    d = dict()
    for t in trades:
        if t.CounterpartyId() in d.keys():
            d[t.CounterpartyId()].append(t)
        else:
            d[t.CounterpartyId()] = [t]
    return d


def SecLendPositionDictionary(keys, positions, borrow):
    i = 0
    d = dict()
    for k in keys:
        if not k.IsEmpty():
            if (borrow and positions.At(i).First() > 0) or (not borrow and positions.At(i).First() < 0):
                if k.First() in d.keys():
                    d[k.First()] += positions.At(i).First()
                else:
                    d[k.First()] = positions.At(i).First()
        i += 1
    return d


def SecLendDictionary(keys, positions):
    i = 0
    d = dict()
    for k in keys:
        d[k] = positions[i]
        i += 1
    return d


def SecLendCreateDictionaryCounterpartyPerSecurity(dictionary, max, borrow):
    d = defaultdict(lambda: 0)
    for k in dictionary.Keys():
        if (dictionary.At(k) > 0 and borrow) or (dictionary.At(k) < 0 and not borrow):
            d[k.Underlying().Name()] += abs(dictionary.At(k))
    if len(d) > max:
        newDict = dict(sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)[:max])
        newDict["Other"] = sum(d.values()) - sum(newDict.values())
        return newDict
    return d



def IsOwnOrder(row, column, cell, input, aspect):
    trades = row.Trades() if hasattr(row, 'Trades') else [row.Trade()]
    if not all([trade.Trader() == acm.User() for trade in trades]):
        for app in acm.UX.SessionManager().RunningApplications():
            if app.IsKindOf('FUiTrdMgrFrame') and \
                app.ActiveSheet() and \
                app.ActiveSheet().Selection() and \
                app.ActiveSheet().Selection().SelectedCell() and \
                app.ActiveSheet().Selection().SelectedCell().RowObject() and \
                app.ActiveSheet().Selection().SelectedCell().RowObject().Handle() == cell.RowObject().Handle():
                app.InvokeCommand('cmdUndoChanges')
                msg = 'Changes not accepted, Assign yourself as trader for the order'
                logger.error(msg)
                acm.UX.Dialogs().MessageBoxInformation(app.Shell(), msg)
                return False
        return False
    return True

def OnChangeOwnOrder(row, column, cell, input, aspect):
    return input if IsOwnOrder(row, column, cell, input, aspect) else 0


def OnCounterPartyChanged(tradeRow, column, cell, input, aspect):
    """ Called as post input hook by the column Security Loan Trade Counterparty """
    if input:
        tradeClone = tradeRow.Trade()
        trade = tradeClone.Originator()
        if tradeClone.Counterparty() != trade.Counterparty():
            FSecLendHooks.EnrichTradeData(tradeClone, trade)

def OnValueDayChange(tradeRow, column, cell, input, aspect):
    """ Called as post input hook by the column Security Loan Trade Value Day """
    if input:
        tradeClone = tradeRow.Trade()
        trade = tradeClone.Originator()
        if tradeClone.ValueDay() != trade.ValueDay():
            tradeClone.AcquireDay(tradeClone.ValueDay())
            if trade.ContractTrade().Oid() == trade.Oid() and tradeClone.Status() in ('Simulated', 'Reserved'):
                newStartDate = tradeClone.ValueDay()
                slDeal = acm.Deal.WrapAsDecorator(tradeClone)
                slDeal.SetAttribute('ins_startDate', newStartDate)            


def LogExtensionAttribute(object, extension, node=None):
    try:
        print('called', extension, 'with', type(object), object.StringKey(), type(node), node, node.Value())
    except:
        pass
    if node:
        acm.StartApplication("Valuation Viewer", node)
        return node.Value()


def AlertNotesInput(row, column, cell, input, aspect):
    if row.Originator().IsKindOf(acm.FAlert):
        alert = row.Originator()
        alert.AddInfoValue("Notes", input)
        alert.Commit()
    else:
        pass

