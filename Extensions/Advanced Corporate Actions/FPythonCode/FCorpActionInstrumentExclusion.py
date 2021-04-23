""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FCorpActionInstrumentExclusion.py"
"""----------------------------------------------------------------------------
MODULE
    FCorpActionInstrumentExclusion - Module to update the instrument exclusion
    list to freeze the corporate action instruments during the period of
    corporate action processing.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm
import FBDPCommon

from FBDPCurrentContext import Summary, Logme
from FTransactionHandler import ACMHandler

__all__ = ['ExclusionListUpdater', 'AddInstrumentToPageGroups', 'RemoveInstrumentFromPageGroups', 'FrozenAndUnFrozenInstrumentsCount']

def _SubGroupsRecursive(exclusionList):
    returnGroups = set()
    if exclusionList.Terminal():
        returnGroups.add(exclusionList)
    for subList in exclusionList.SubGroups():
        returnGroups = returnGroups.union(
                _SubGroupsRecursive(subList))
    return returnGroups


def _FreezeInsAndDerivatives():
    FreezeInsAndDerivatives = FBDPCommon.valueFromFParameter(
                'FCAVariables', 'FreezeInsAndDerivatives')
    if FreezeInsAndDerivatives and FreezeInsAndDerivatives != '0':
        return 1
    return 0


def _ExclusionListPageGroups():
    exclusionListNamesStr = FBDPCommon.valueFromFParameter(
                'FCAVariables', 'ExclusionPages')
    leafPages = set()
    if exclusionListNamesStr:
        pagesList = [acm.FPageGroup[i.strip()]
                    for i in exclusionListNamesStr.split(',')
                    if acm.FPageGroup[i.strip()]]
        for page in pagesList:
            leafPages = leafPages.union(_SubGroupsRecursive(page))
    return leafPages


def _InstrumentInExclusionList(instrument, pageGroup):
    instrGroupMap = acm.FInstrGroupMap.Select01('instrument=%s and group=%s' % 
                        (instrument.Oid(), pageGroup.Oid()), None)
    if instrGroupMap:
        return True
    else:
        return False


def _ActionToFreezeInstrument(currentDate, corpAction):

    FreezeInsFrom = FBDPCommon.valueFromFParameter(
                'FCAVariables', 'FreezeInsFrom')
    if not FreezeInsFrom:
        FreezeInsFrom = '-2d'
    FreezeInsTo = FBDPCommon.valueFromFParameter(
                'FCAVariables', 'FreezeInsTo')
    if not FreezeInsTo:
        FreezeInsTo = '2d'
    startDate = acm.Time().DateAdjustPeriod(corpAction.ExDate(), FreezeInsFrom)
    endDate = acm.Time().DateAdjustPeriod(corpAction.ExDate(), FreezeInsTo)
    if currentDate > startDate and currentDate < endDate:
        return 'ADD'
    else:
        return 'REMOVE'


def _GetInstruments(ca):
    ins = ca.Instrument()
    if _FreezeInsAndDerivatives():
        return [ins]
    else:
        return [ins for ins in ins.Derivatives().AsList() if ins.InsType() == 'SecurityLoan']


def _CreateInstrGroupMap(ins, pageGroup):
    instrGroupMap = acm.FInstrGroupMap()
    instrGroupMap.Instrument(ins)
    instrGroupMap.Group(pageGroup)
    instrGroupMap.Commit()


def AddInstrumentToPageGroups(ca):
    freezeInstruments = _GetInstruments(ca)
    exclusionPageGroups = _ExclusionListPageGroups()
    for pageGroup in exclusionPageGroups:
        for ins in freezeInstruments:
            if _InstrumentInExclusionList(ins, pageGroup):
                continue
            else:
                _CreateInstrGroupMap(ins, pageGroup)


def RemoveInstrumentFromPageGroups(ca):
    freezeInstruments = _GetInstruments(ca)
    exclusionPageGroups = _ExclusionListPageGroups()
    for pageGroup in exclusionPageGroups:
        for ins in freezeInstruments:
            instrGroup = acm.FInstrGroupMap.Select01('instrument=%s and group=%s' %
                                    (ins.Oid(), pageGroup.Oid()), None)
            if instrGroup:
                instrGroup.Delete()


def FrozenAndUnFrozenInstrumentsCount(cas):
    
    exclusionPageGroups = _ExclusionListPageGroups()
    countFrozen = 0
    countUnFrozen = 0
    for ca in cas:
        for pageGroup in exclusionPageGroups:
            freezeInstruments = _GetInstruments(ca)
            for ins in freezeInstruments:
                if not _InstrumentInExclusionList(ins, pageGroup):
                    countUnFrozen += 1
                else:
                    countFrozen += 1
    
    return countFrozen, countUnFrozen


class ExclusionListUpdater(object):

    def __init__(self, corpAction, transHandler=ACMHandler()):
        self._action = corpAction
        self._transHandler = transHandler
        self._caInstrument = corpAction.Instrument()
        self._instruments = {e.Instrument()
                                for caChoice in corpAction.CaChoices()
                                for e in caChoice.CaElections()}
        self._exclusionPageGroups = _ExclusionListPageGroups()

    def _CommitPageGroup(self, pageGroup):
        imgage = pageGroup.StorageImage()
        imgage.UpdateTime = acm.Time.TimeNow()
        imgage.Commit()
        if pageGroup.SuperGroup():
            self._CommitPageGroup(pageGroup.SuperGroup())

    def _CreateInstrGroupMap(self, ins, pageGroup):
        instrGroupMap = acm.FInstrGroupMap()
        instrGroupMap.Instrument(ins)
        instrGroupMap.Group(pageGroup)
        with self._transHandler.Transaction():
            self._transHandler.Add(instrGroupMap)
        Logme()('Added instrument "%s" to Exclusion List %s' % (
                            ins.Name(), pageGroup.Name()), 'DEBUG')
        Summary().ok(instrGroupMap, Summary().CREATE, instrGroupMap.Oid())

    def _FreezeInstruments(self):
        freezeInstruments = self._instruments
        if _FreezeInsAndDerivatives():
            freezeInstruments = [self._caInstrument]
        return freezeInstruments

    def _AddInstrumentToPageGroups(self):
        freezeInstruments = self._FreezeInstruments()
        for pageGroup in self._exclusionPageGroups:
            for ins in freezeInstruments:
                if _InstrumentInExclusionList(ins, pageGroup):
                    Logme()('The InstrGroupMap with ISIN "%s" already exists. None is created.' % ins.Isin())
                    continue
                else:
                    self._CreateInstrGroupMap(ins, pageGroup)

    def _RemoveInstrument(self):
        freezeInstruments = self._FreezeInstruments()
        for pageGroup in self._exclusionPageGroups:
            for ins in freezeInstruments:        
                instrGroup = acm.FInstrGroupMap.Select01('instrument=%s and group=%s' %
                                        (ins.Oid(), pageGroup.Oid()), None)
                if instrGroup:
                    with self._transHandler.Transaction():
                        self._transHandler.Add(instrGroup, op='Delete')
                    Logme()('Deleted instrument "%s" from Exclusion List %s' %
                            (ins.Name(), pageGroup.Name()), 'DEBUG')
                    Summary().ok(instrGroup, Summary().DELETE, instrGroup.Oid())


    def update(self):
        if _ActionToFreezeInstrument(
                acm.Time.DateToday(), self._action) == 'ADD':
            self._AddInstrumentToPageGroups()
        else:
            self._RemoveInstrument()