""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/aggr_arch/etc/FAggGeneral.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import time


import acm

import FBDPCommon


class Query:

    def __init__(self, aelVariables, q=acm.FMatrix()):
        self.matrix = q
        self.aelVariables = aelVariables

    def addBracketAtFirstRow(self):
        self.matrix.AtPut(0, 0, acm.FSymbol(''))
        self.matrix.AtPut(0, 1, acm.FSymbol('('))

    def setExpired(self):
        oe = self.removeValues('Instrument.Expiry day', 'OnlyExpired')
        if oe and int(oe):
            self.appendRow(['And', '', 'Instrument.Expiry day', 'less than',
                    '0d', ''])

    def setOTC(self):
        oo = self.removeValues('Instrument.Otc', 'OTC')
        if (oo == 'Only OTC'):
            self.appendRow(['And', '', 'Instrument.Otc', 'equal to', 'Yes',
                    ''])
        elif (oo == 'Only Non OTC'):
            self.appendRow(['And', '', 'Instrument.Otc', 'equal to', 'No', ''])

    def removeFirstAnd(self):
        if self.matrix:
            self.matrix.AtPut(0, 0, '')
        else:
            raise Exception('The Aggregation Rule has to have at least one '
                    'selection criterion.')

    def appendRow(self, array):
        array = [acm.FSymbol(x) for x in array]
        self.matrix.AddRow(array)

    def removeValues(self, queryField, aelVariablesField):
        clone_matrix = self.matrix.Clone()
        self.matrix.Size(0, 0)
        for row in clone_matrix:  # Remove needs a copy of the list.
            val = row[2].Text()
            if not val.upper() == queryField.upper():
                self.appendRow(row)
        res = self.aelVariables[aelVariablesField]
        return res

    def setValues(self, fieldName, oneWord=None):
        niceName = oneWord or fieldName
        selectedValues = self.removeValues(fieldName, niceName)
        if selectedValues:
            self.appendRow(['And', '(', fieldName, 'equal to',
                    selectedValues[0], ''])
            for v in selectedValues[1:]:
                self.appendRow(['Or', '', fieldName, 'equal to', v, ''])
            self.matrix.AtPut(self.matrix.Rows() - 1, 5, acm.FSymbol(')'))


def setTradeGroupingCriteria(ar, tgc):

    ar.GroupingCriteria = tgc and '"' + '","'.join(list(tgc)) + '"' or ''


def changeOrderNumber(ordernbr, oid):

    acm.PollDbEvents()
    l = acm.FAggregationRule.Select('')
    aggList = [(a.Ordernbr(), a.Oid(), a) for a in l]
    aggList.sort()  # First on ordernbr, then on oid.
    changes = {}
    for i in aggList:
        changes[i[1]] = (aggList.index(i) + 1, i[2])
    if ordernbr != changes[oid][0]:
        aggList = [(a[0], -a[1], a[2]) for a in aggList]
        aggList.sort()  # First on ordernbr, then on -oid.
        changes = {}
        for i in aggList:
            changes[i[1]] = (aggList.index(i) + 1, i[2])
    for new, ar in changes.values():
        if ar.Ordernbr() != new:
            c = ar.Clone()
            c.Ordernbr = new
            ar.Apply(c)
            ar.Commit()
            acm.PollDbEvents()
            ar.Touch()


def setFields(aggregationRule, flt, q, aelVariables):
    flt_orig = acm.FTradeSelection[flt.Oid()]
    flt.Name = '~AggRule_' + str(time.time())
    aelVariables['Instrument'] = [i.Name() for i in aelVariables['Instrument']]
    aelVariables['Underlying'] = [i.Name() for i in aelVariables['Underlying']]
    aelVariables['Portfolio'] = [i.Name() for i in aelVariables['Portfolio']]
    aelVariables['Counterparty'] = [i.Name() for i in
            aelVariables['Counterparty']]
    aelVariables['Acquirer'] = [i.Name() for i in aelVariables['Acquirer']]
    aelVariables['split_per_long_short_pos'] = ('Buy/Sell' in
            aelVariables['trade_grouping_criteria'])

    q.setValues('Instrument')
    q.setValues('Instrument.Type', 'Instype')
    q.setValues('Instrument.Underlying', 'Underlying')
    q.setValues('Instrument.Underlying type', 'UnderlyingInstype')
    q.setExpired()
    q.setOTC()
    q.setValues('Portfolio')
    q.setValues('Counterparty')
    q.setValues('Acquirer')
    q.removeFirstAnd()
    #print 'Query:', q.query
    flt.FilterCondition(q.matrix)
    FBDPCommon.commit(flt, flt_orig)

    #acm.PollDbEvents()
    aggregationRule.TradeFilter = flt
    aggregationRule.ExcludeHook = aelVariables.get('exclude_hook', '')
    aggregationRule.Ordernbr = int(aelVariables['ordernbr'])
    aggregationRule.Locked = aelVariables.get('aggregate', 0)
    aggregationRule.Yearly = aelVariables.get('aggregate_periodic_yearly', 0)
    aggregationRule.Monthly = aelVariables.get('aggregate_periodic_monthly', 0)
    aggregationRule.Daily = aelVariables.get('aggregate_periodic_daily', 0)
    aggregationRule.AggregateOpenDays = aelVariables.get('open_trade_days', 0)
    aggregationRule.SplitPerLongShortPos = aelVariables.get(
            'split_per_long_short_pos', 0)
    setTradeGroupingCriteria(aggregationRule,
            aelVariables['trade_grouping_criteria'])
    return aggregationRule
