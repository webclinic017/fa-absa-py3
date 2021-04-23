""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/mark_to_market/etc/FMtMSelInsCurr.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FMtMUtil - Module which provides instrument selection and manipulation
            functionalities to Mark-to-Market script.

DESCRIPTION
    This module contains the utility function and classes for the script
    FMarkToMarket.
----------------------------------------------------------------------------"""


import acm
import ael


import FBDPInstrument
import FMtMUtil
import FSEQDataMaint
from FBDPWorld import OrderedDict
from FBDPWorld import OrderedSet

HIST_FUNDING_INS_NAME = 'HISTORICAL_FINANCING'
_DEFAULT_INSTRUMENTS = (
    'StockDefault', 'BillDefault', 'BondDefault', 'DualCurrencyBondDefault',
    'ZeroDefault', 'RepoDefault', 'ConvertibleDefault', 'OptionDefault',
    'DepositDefault', 'FRNDefault', 'SwapDefault',
)

# #############################################################################
# Instrument Selection
# #############################################################################


def _initialSelectInstrumentsByInsOid(world, insOidList):

    insOidToAcmInsMap = OrderedDict()
    for insOid in insOidList:
        acmIns = acm.FInstrument[insOid]
        if not acmIns:
            continue
        insOidToAcmInsMap[insOid] = acmIns
    world.logDebug('        {0} instruments initially selected.'.format(
            len(insOidToAcmInsMap)))
    return insOidToAcmInsMap


def _initialSelectZeroInstruments(world):

    insOidToAcmInsMap = OrderedDict()
    for acmIns in acm.FInstrument.Select('insType=\'Zero\''):
        insOidToAcmInsMap[acmIns.Oid()] = acmIns
    world.logDebug('        {0} instruments initially selected.'.format(
            len(insOidToAcmInsMap)))
    return insOidToAcmInsMap


def _filterOutNonOptionWarrntInstruments(world, insOidToAcmInsMap):

    numRemoved = 0
    for insOid in list(insOidToAcmInsMap.keys()):
        acmIns = insOidToAcmInsMap[insOid]
        if acmIns.InsType() not in ('Option', 'Warrant'):
            del insOidToAcmInsMap[insOid]
            numRemoved += 1
    world.logDebug('        {0} instruments removed because they are not '
            'option or warrant types of instruments.'.format(numRemoved))


def _filterOutInstrumentsHavingNonStockEquityIndexUnderlying(world,
        insOidToAcmInsMap):

    numRemoved = 0
    for insOid in list(insOidToAcmInsMap.keys()):
        acmIns = insOidToAcmInsMap[insOid]
        if (acmIns.Underlying() and
                acmIns.Underlying().InsType() not in ('Stock', 'EquityIndex')):
            del insOidToAcmInsMap[insOid]
            numRemoved += 1
    world.logDebug('        {0} instruments removed because they have '
            'underlying instruments that are neither stock nor equity '
            'index.'.format(numRemoved))


def _filterOutGenericInstruments(world, insOidToAcmInsMap):

    numRemoved = 0
    for insOid in list(insOidToAcmInsMap.keys()):
        acmIns = insOidToAcmInsMap[insOid]
        if acmIns.Generic():
            del insOidToAcmInsMap[insOid]
            numRemoved += 1
    world.logDebug('        {0} instruments removed by \'generic\' '
            'filtering'.format(numRemoved))


def _filterOutDefaultInstruments(world, insOidToAcmInsMap):

    numRemoved = 0
    for insOid in list(insOidToAcmInsMap.keys()):
        acmIns = insOidToAcmInsMap[insOid]
        if acmIns.Name() in _DEFAULT_INSTRUMENTS:
            del insOidToAcmInsMap[insOid]
            numRemoved += 1
    world.logDebug('        {0} instruments removed by \'default instrument\' '
            'filtering'.format(numRemoved))


def _filterOutExpiredInstruments(world, insOidToAcmInsMap, strIsoExpDate):

    numRemoved = 0
    for insOid in list(insOidToAcmInsMap.keys()):
        acmIns = insOidToAcmInsMap[insOid]
        if FBDPInstrument.isExpired(acmIns, strIsoExpDate):
            del insOidToAcmInsMap[insOid]
            numRemoved += 1
    world.logDebug('        {0} instruments removed by \'exp_day\' '
            'filtering'.format(numRemoved))


def _filterOutNonListNodePagesRelatedInstruments(world, insOidToAcmInsMap,
        listNodePagesInsOidSet):

    numRemoved = 0
    for insOid in list(insOidToAcmInsMap.keys()):
        if insOid not in listNodePagesInsOidSet:
            del insOidToAcmInsMap[insOid]
            numRemoved += 1
    world.logDebug('        {0} instruments removed by \'Listnodes/Pages\' '
            'filtering'.format(numRemoved))


def _getAcmInsList(insOidToAcmInsMap):

    nameInsPairList = [(insOidToAcmInsMap[k].Name(), insOidToAcmInsMap[k]) for k
            in list(insOidToAcmInsMap.keys())]
    return [nameInsPair[1] for nameInsPair in nameInsPairList]

def selectVolBmInstruments(world, insOids):

    elements = _initialSelectInstrumentsByInsOid(world, insOids)
    _filterOutNonOptionWarrntInstruments(world, elements)
    _filterOutInstrumentsHavingNonStockEquityIndexUnderlying(world, elements)
    _filterOutGenericInstruments(world, elements)
    _filterOutDefaultInstruments(world, elements)
    world.logDebug('        {0} instruments selected.'.format(len(elements)))
    return _getAcmInsList(elements)


def selectYcBmInstruments(world, insOids=()):

    elements = _initialSelectInstrumentsByInsOid(world, insOids)
    _filterOutDefaultInstruments(world, elements)
    world.logDebug('        {0} instruments selected.'.format(len(elements)))
    return _getAcmInsList(elements)


def _findMtMYcListNodeOidSet():

    listNodeOidSet = OrderedSet()  # Note: listnodes has no unique id
    #Note: can't use market_ptynbr constraint on ListNode
    for aelLn in ael.ListNode.select():
        if not (aelLn.id in ("MTM_YIELD_CURVES...",) and
                aelLn.nodnbr in ("MTM_YIELD_CURVES...",)):
            continue
        for child in aelLn.reference_in():
            if child.record_type == 'ListNode':
                listNodeOidSet.add(child.nodnbr)
            elif child.record_type == 'ListLeaf':
                listNodeOidSet.add(aelLn.nodnbr)
    return listNodeOidSet


def _findListNodeRelatedInsOidSet(world, listNodeOidSet):

    insOidSet = OrderedSet()  # of insaddr numbers
    for lnOid in listNodeOidSet:
        aelLn = ael.ListNode[lnOid]
        world.logDebug('+ process \'Listnodes/Pages\': {0}'.format(aelLn.id))
        for e in aelLn.reference_in():
            if e.record_type in ('ListLeaf', 'OrderBook'):
                insOid = e.insaddr.insaddr
                insOidSet[insOid] = None
    return insOidSet


def selectMtMYcInstruments(world):

    elements = _initialSelectZeroInstruments(world)
    mtmYcListNodeOidSet = _findMtMYcListNodeOidSet()
    listNodePagesRelatedInsOidSet = _findListNodeRelatedInsOidSet(world,
            mtmYcListNodeOidSet)
    _filterOutNonListNodePagesRelatedInstruments(world, elements,
            listNodePagesRelatedInsOidSet)
    _filterOutDefaultInstruments(world, elements)
    world.logDebug('        {0} instruments selected.'.format(len(elements)))
    return _getAcmInsList(elements)


def selectMtMInstruments(world, insOids, aelExpDay):

    strIsoExpDate = acm.Time.AsDate(aelExpDay)
    elements = _initialSelectInstrumentsByInsOid(world, insOids)
    _filterOutDefaultInstruments(world, elements)
    _filterOutExpiredInstruments(world, elements, strIsoExpDate)
    world.logDebug('        {0} instruments selected.'.format(len(elements)))
    return _getAcmInsList(elements)


def findInsAndAllUndInsList(insList):

    InsAndAllUndInsList = insList[:]
    insOidSet = OrderedSet([ins.Oid() for ins in InsAndAllUndInsList])
    i = 0
    while i < len(InsAndAllUndInsList):
        undIns = InsAndAllUndInsList[i].Underlying()
        if undIns:
            undInsOid = undIns.Oid()
            if undInsOid not in insOidSet:
                InsAndAllUndInsList.append(undIns)
                insOidSet.add(undInsOid)
        i += 1
    return FMtMUtil.uniquifyListByOid(InsAndAllUndInsList)


def findUndAndDersList(insList):

    # Find underlying instrument for each ins.  If a ins has undIns, then an
    # entry is added into undInsToInsListMap.
    undInsOidSet = OrderedSet()
    undInsToInsListMap = {}
    for ins in insList:
        undIns = ins.Underlying()
        if not undIns:
            continue
        undInsOid = undIns.Oid()
        if undInsOid not in undInsOidSet:
            undInsToInsListMap[undIns] = [ins]
            undInsOidSet.add(undInsOid)
        else:
            undInsToInsListMap[undIns].append(ins)
    # Uniquify values of dictionary undInsToInsListMap, which is a list of
    # derivative instruments
    for undIns in undInsToInsListMap:
        undInsToInsListMap[undIns] = FMtMUtil.uniquifyListByOid(
            undInsToInsListMap[undIns])
    undAndDersList = []
    # Make list undAndDers to return
    for k in undInsToInsListMap:
        v = undInsToInsListMap[k]
        undAndDersList.append(FMtMUtil.UndAndDers(undIns=k, derInsList=v))
    return undAndDersList


def _addUnderlyingInsToList(acmIns, acmInsList):

    undIns = acmIns.Underlying()
    if undIns:
        acmInsList.append(undIns)


def _addDeliverableRelatedInsToList(acmIns, acmInsList):

    if not acmIns.IsKindOf(acm.FCashFlowInstrument):
        return
    for dl in acmIns.Deliverables():
        dlIns = dl.Deliverable()
        if dlIns:
            acmInsList.append(dlIns)


def _addCombinationLinkRelatedInsToList(acmIns, acmInsList):

    if not acmIns.InstrumentMaps():
        return
    for cl in acmIns.InstrumentMaps():
        clIns = cl.Instrument()
        if clIns:
            acmInsList.append(clIns)


def _addLegRelatedInsToList(acmIns, acmInsList):

    for acmLeg in acmIns.Legs():
        legFloatRateRefIns = acmLeg.FloatRateReference()
        if legFloatRateRefIns and \
                legFloatRateRefIns.InsType() != 'PriceIndex':
            acmInsList.append(legFloatRateRefIns)
        legFloatRateRefIns2 = acmLeg.FloatRateReference2()
        if legFloatRateRefIns2 and \
                legFloatRateRefIns2.InsType() != 'PriceIndex':
            acmInsList.append(legFloatRateRefIns2)
        legIndexRefIns = acmLeg.IndexRef()
        if legIndexRefIns and \
                legIndexRefIns.InsType() != 'PriceIndex':
            acmInsList.append(legIndexRefIns)
        legCreditRefIns = acmLeg.CreditRef()
        if legCreditRefIns and \
                legCreditRefIns.InsType() != 'PriceIndex':
            acmInsList.append(legCreditRefIns)


def _addRelatedInsToList(ins, insList):
    """
    Note, will not include currency.
    """
    if ins.Oid() < 0:
        return
    # Will not add currency
    if ins.IsKindOf(acm.FCurrency):
        return
    # If already in the list.
    if ins.Oid() in [i.Oid() for i in insList]:
        return
    # Add this instrument, and figure out what else to add.
    insList.append(ins)
    insToAdd = []
    _addUnderlyingInsToList(ins, insToAdd)
    _addDeliverableRelatedInsToList(ins, insToAdd)
    _addCombinationLinkRelatedInsToList(ins, insToAdd)
    _addLegRelatedInsToList(ins, insToAdd)
    # Recursive add the non-repeated instrument-to-add
    for ins in FMtMUtil.uniquifyListByOid(insToAdd):
        _addRelatedInsToList(ins, insList)


def findRelatedInstruments(ins):

    insList = []
    _addRelatedInsToList(ins, insList)
    return FMtMUtil.uniquifyListByOid(insList)


def findBenchmarkInstruments():

    insList = []
    ycList = [yc for yc in acm.FYieldCurve.Select('')]
    for yc in ycList:
        for insSprd in yc.InstrumentSpreads():
            insSprdBm = insSprd.Benchmark()
            if insSprdBm:
                insList.append(insSprdBm)
            insSprdBm2 = insSprd.Benchmark()
            if insSprdBm2:
                insList.append(insSprdBm2)
        for bm in yc.Benchmarks():
            bmIns = bm.Instrument()
            if bmIns:
                insList.append(bmIns)
            spreadInst = bm.SpreadInstrument()
            if spreadInst:
                insList.append(spreadInst)
    return FMtMUtil.uniquifyListByOid(insList)


def _insToInsCurrPairs(ins):

    assert (hasattr(ins, 'IsKindOf') and ins.IsKindOf(acm.FInstrument) and
            not ins.IsKindOf(acm.FCurrency)), ('The ins must be an acm '
            'instrument, but not a currency.  However, {0} is given'.format(
            ins))
    insCurrPairs = []
    if ins.Name() == HIST_FUNDING_INS_NAME:
        currOidSet = OrderedSet()
        for price in ins.Prices():
            curr = price.Currency()
            currOid = curr.Oid()
            if currOid not in currOidSet:
                currOidSet.add(currOid)
                insCurrPairs.append(InsCurrPair(ins=ins, curr=curr))
    elif ins.InsType() in ('CurrSwap', 'FxSwap'):
        currOidSet = OrderedSet()
        for leg in ins.Legs():
            curr = leg.Currency()
            currOid = curr.Oid()
            if currOid not in currOidSet:
                currOidSet.add(currOid)
                insCurrPairs.append(InsCurrPair(ins=ins, curr=curr))
    else:
        insCurrPairs.append(InsCurrPair(ins=ins, curr=ins.Currency()))
    return insCurrPairs


# #############################################################################
# Instrument Currency Pair Manipulation
# #############################################################################


class InsCurrPair(object):

    def __init__(self, ins, curr):

        assert hasattr(ins, 'IsKindOf') and ins.IsKindOf(acm.FInstrument), (
                'InsCurrPair: ins must be an FInstrument.')
        assert hasattr(curr, 'IsKindOf') and curr.IsKindOf(acm.FCurrency), (
                'InsCurrPair, curr must be an Fcurrency.')
        self.ins = ins
        self.curr = curr
        self.__oidPair = (ins.Oid(), curr.Oid())  # Cache for cmp/eq/hash

    def __hash__(self):

        return hash(self.__oidPair)

    def __eq__(self, other):

        return self.__oidPair == other.getOidPair()

    def __cmp__(self, other):

        return cmp(self.__oidPair, other.getOidPair())

    def __str__(self):

        return '(ins={0},curr={1})'.format(self.ins.Name(), self.curr.Name())

    def __repr__(self):

        return '<InsCurrPair{0}>'.format(str(self))

    def getOidPair(self):

        return self.__oidPair


def splitInsCurrPairsByInsTypeCreditBalance(insCurrPairs):

    creditBalanceInsCurrPairs = []
    nonCreditBalanceInsCurrPairs = []
    for insCurrPair in insCurrPairs:
        if not isinstance(insCurrPair, InsCurrPair):
            raise ValueError('The given insCurrPairs contains an element '
                    '"{0}", which is not an instance of InsCurrPair.'.format(
                    insCurrPair))
        if insCurrPair.ins.IsKindOf(acm.FCreditBalance):
            creditBalanceInsCurrPairs.append(insCurrPair)
        else:
            nonCreditBalanceInsCurrPairs.append(insCurrPair)
    return creditBalanceInsCurrPairs, nonCreditBalanceInsCurrPairs


def converInsListToInsCurrPairList(insList):

    for ins in insList:
        assert (hasattr(ins, 'IsKindOf') and ins.IsKindOf(acm.FInstrument) and
                not ins.IsKindOf(acm.FCurrency)), ('The ins in the '
                'insList must be an acm instrument, but not a currency.  '
                'However, {0} is given'.format(ins))
    insCurrPairList = [insCurrPair for ins in insList
            for insCurrPair in _insToInsCurrPairs(ins)]
    return insCurrPairList


def convertCurrDupletNameListToInsCurrPairList(currDupletNameList):

    fxInsCurrPairList = []
    for currDupletName in currDupletNameList:
        curr1Name, curr2Name = currDupletName.split('/')[0:2]
        curr1 = acm.FCurrency[curr1Name]
        curr2 = acm.FCurrency[curr2Name]
        fxInsCurrPairList.append(InsCurrPair(ins=curr1, curr=curr2))
    return fxInsCurrPairList


def _IsExotic(ins):
    return ins in FSEQDataMaint.exotic_options or\
           ins in FSEQDataMaint.exotic_warrants or\
           ins in FSEQDataMaint.variance_swaps or\
           ins in FSEQDataMaint.volatility_swaps or\
           ins in FSEQDataMaint.certificates


def SplitInstrumentByInsTypeExotic(insCurrPairList):
    exoticInstrumentList = []
    nonExoticInstrumentList = []
    for insCurrPair in insCurrPairList:
        if _IsExotic(insCurrPair.ins):
            exoticInstrumentList.append(insCurrPair)
        else:
            nonExoticInstrumentList.append(insCurrPair)

    return exoticInstrumentList, nonExoticInstrumentList