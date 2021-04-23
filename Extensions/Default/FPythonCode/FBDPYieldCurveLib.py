""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/common/FBDPYieldCurveLib.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FBDPYieldCurveLib - Library assisting yield curve manipulation

DESCRIPTION
----------------------------------------------------------------------------"""

import collections
import copy


import acm
import ael


INS_SPRD_CURVE_TYPES = ('Instrument Spread', 'Instrument Spread Bid/Ask')
ATTR_SPRD_CURVE_TYPES = ('Attribute Spread',)
SEASONALITY_CURVE_TYPES = ('Seasonality',)
COMPOSITE_CURVE_TYPES = ('Composite',)
MULTI_CURVE_TYPES = ('Benchmark',)
SPRD_CURVE_TYPES = ('Spread',)
INFLATION_CURVE_TYPES = ('Inflation',)
CURVE_TYPES_SUPPORT_CALCULATE = ('Benchmark', 'Price', 'Spread', 'Inflation')
CURVE_TYPES_SUPPORT_CALIBRATE_SPREADS = INS_SPRD_CURVE_TYPES


# #############################################################################
# Definition
#
# Original Yield Curve - An original yield curve does not refer any other curve
#         as its original curve.  An original yield curve must have
#         (bool(yc.OriginalCurve()) == False).
#
# Historical Yield Curve - A historical yield curve that has its historical
#         day set to some date.  A historical yield curve curve must have
#         (i.e. bool(yc.HistoricalDay()) == True).
#
# Archived Yield Curve - A archived yield curve has its archive status set to
#         some value other than 0.  An archived yield curve must have
#         (bool(yc.ArchiveStatus()) == True).
#
# Basis - Curve A is basing on curve B (equivalently curve B is based upon by
#         curve A) if curve A references curve B as its underlying curve or
#         dependency curve.
# #############################################################################


# #############################################################################
#  Yield Curve Characteristics
#
# **** MUST-HAVE characteristics ****
# M1. All original yield curves must not be historical.
# M2. All non-original yield cure must be historical.
# M3. All historical yield curves must be archived.
# M4. All non-historical yield curve must not be archived.
# (Note, if M1 to M4 holds, you will have DM1 and DM2 holds)
# M5. All original yield curves' underlying curves and dependency curves must
#         also be original.
# M6. All non-original yield curves' underlying curves and dependency curves
#         must also be non-original.
# M7. All historical yield curves underlying curves and dependency curves
#         must also be historical, and they must all dated to the same date.
# (Note, if M1 to M7 holds, you will have DM3 holds)
# M8. For all non-original yield curve, its original yield curve must be
#         original.  (i.e. originality-non-transitivity)
# **** Derived MUST-HAVE characteristics ****
# DM1. All original yield curves must not be archived.
# DM2. All non-original yield curve must be archived.
# DM3. All non-original yield curve are archived and historical, its underlying
#         curve and dependency curve are also archived and historical of the
#         same date.
# **** SHOULD-HAVE characteristics ****
# S1. For all non-original yield curve, its underlying curve's original curve
#         should be its original curve's underlying curve.
# S2. For all non-original yield curve, its dependency curve's original curve
#         should be its original curve's dependency curve.
# #############################################################################


# #############################################################################
# Programming Guide
#
# * Discovery of all original yield curve via DbSql in case some original
#         yield curves are archived, but find their name via ACM.
# * All hierarchy discovery are manipulated through original yield curve names
#         and via ACM.
# * All historical yield curve are manipulated through either their oid
#         directly or the pair (original yield curve name, iso date string).
# #############################################################################


def getLiveAcmYieldCurve(ycOid):

    acmYc = acm.FYieldCurve[ycOid]
    if acmYc and acmYc.ArchiveStatus():  # In case acm cache already polluted.
        return None
    return acmYc


def getMayBeArchivedAcmYieldCurve(ycOid):

    aelYc = ael.YieldCurve[ycOid]
    if not aelYc:
        return None
    if aelYc.archive_status == 0:
        acmYc = acm.FYieldCurve[ycOid]  # direct look up since live
    else:
        acmYc = acm.Ael.AelToFObject(aelYc)  # will force acm cache pollution
    return acmYc


def getYieldCurveName(ycOid):
    """
    Note that the yield curve name is not directly found from the database
    yield curve table.  The yield curve name column on the table is only 31
    character wide, but the actual name can be longer.
    """
    acmYc = getMayBeArchivedAcmYieldCurve(ycOid)
    if acmYc:
        return acmYc.Name()
    return None


def _oidUniqueSorted(acmObjList):

    oidToObjMap = dict((acmObj.Oid(), acmObj) for acmObj in acmObjList)
    return [acmObj for (_oid, acmObj) in sorted(oidToObjMap.iteritems())]


def isAcmYieldCurveOriginal(acmYc):

    return not bool(acmYc.OriginalCurve())


def isAcmYieldCurveHistorical(acmYc):

    return bool(acmYc.HistoricalDay())


def isAcmYieldCurveArchived(acmYc):

    return bool(acmYc.ArchiveStatus())


def findAllOriginalYieldCurveNameList():
    """
    Return all the original yield curves' names.
    Note that this function purposely find those names via DbSql.  In this way
    it is faster than iterating through AEL.  It is also slower than iterating
    through ACM, however, ACM does not cope well when an original curve is
    wrongly archived.
    """
    qryStmt = (
            'SELECT seqnbr '
            'FROM yield_curve '
            'WHERE original_yc_seqnbr IS NULL')
    allOrigYcOids = [row[0] for row in ael.dbsql(qryStmt)[0]]
    allOrigYcNames = [getYieldCurveName(ycOid) for ycOid in allOrigYcOids]
    return allOrigYcNames


def findAllLiveYieldCurveNameList():
    """
    Return all the live (i.e. original, non-historical & non-archived) yield
    curves' names.
    Note that this function purposely find those names via DbSql.  In this way
    it is faster than iterating through AEL.  It is also slower than iterating
    through ACM, however, ACM does not cope well when an original curve is
    wrongly archived.
    """
    qryStmt = (
            'SELECT seqnbr '
            'FROM yield_curve '
            'WHERE original_yc_seqnbr IS NULL '
                    'AND historical_day IS NULL '
                    'AND archive_status = 0')
    allLiveYcOids = [row[0] for row in ael.dbsql(qryStmt)[0]]
    allLiveYcNames = [getYieldCurveName(ycOid) for ycOid in allLiveYcOids]
    return allLiveYcNames


def findAllOnDateHistoricalYieldCurveOidList(strIsoDate):
    """
    Return all the historical yield curves' oid of the given date.
    Note that this function purposely find those names via DbSql.  In this way
    it is faster than iterating through AEL.  It is also slower than iterating
    through ACM, however, ACM does not cope well when an original curve is
    wrongly archived.
    """
    qryStmt = (
            'SELECT seqnbr '
            'FROM yield_curve '
            'WHERE historical_day = \'{0}\''.format(strIsoDate))
    allOnDateHistYcOids = [row[0] for row in ael.dbsql(qryStmt)[0]]
    return allOnDateHistYcOids


def _assertAcmYieldCurveOriginalNonHistorical(acmYc, strYcDesc='yield curve'):

    assert isAcmYieldCurveOriginal(acmYc), ('Expecting {0} \'{1}\' to be '
            'original.'.format(strYcDesc, acmYc.Name()))
    assert not isAcmYieldCurveHistorical(acmYc), ('Expecting original {0} '
            '\'{1}\' to be non-historical.'.format(strYcDesc, acmYc.Name()))


def _findOriginalAcmYieldCurve(origYcName):

    acmYc = acm.FYieldCurve[origYcName]
    assert acmYc, 'The live yield curve \'{0}\' does not exist.'.format(
            origYcName)
    _assertAcmYieldCurveOriginalNonHistorical(acmYc, 'yield curve')
    return acmYc


def _findUnderlyingOriginalAcmYieldCurve(origAcmYc):

    acmUndYc = origAcmYc.UnderlyingCurve()
    if not acmUndYc:
        return None
    _assertAcmYieldCurveOriginalNonHistorical(acmUndYc, 'underlying curve')
    return acmUndYc


def _findDependencyOriginalAcmYieldCurve(origAcmYc):

    acmDepYc = origAcmYc.DependencyCurve()
    if not acmDepYc:
        return None
    _assertAcmYieldCurveOriginalNonHistorical(acmDepYc, 'dependency curve')
    return acmDepYc


def _findInstrumentSpreadUnderlyingOriginalAcmYieldCurveList(origInsSprdAcmYc):

    strYcDesc = ('instrument spread curve \'{0}\' spread underlying '
            'curve'.format(origInsSprdAcmYc.Name()))
    insSprdUndYcList = [insSprd.UnderlyingYieldCurve() for insSprd
            in origInsSprdAcmYc.InstrumentSpreads()
            if insSprd.UnderlyingYieldCurve()]
    oidUniqueSortedInsSprdUndYcList = _oidUniqueSorted(insSprdUndYcList)
    for insSprdUndYc in oidUniqueSortedInsSprdUndYcList:
        _assertAcmYieldCurveOriginalNonHistorical(insSprdUndYc, strYcDesc)
    return oidUniqueSortedInsSprdUndYcList


def _findAttributeSpreadUnderlyingOriginalAcmYieldCurveList(origAttrSprdAcmYc):

    strYcDesc = ('attribute spread curve \'{0}\' spread underlying '
            'curve'.format(origAttrSprdAcmYc.Name()))
    attrUndYcList = [ycAttr.UnderlyingCurve() for ycAttr
            in origAttrSprdAcmYc.Attributes()
            if ycAttr.UnderlyingCurve()]
    oidUniqueSortedAttrUndYcList = _oidUniqueSorted(attrUndYcList)
    for attrUndYc in oidUniqueSortedAttrUndYcList:
        _assertAcmYieldCurveOriginalNonHistorical(attrUndYc, strYcDesc)
    return oidUniqueSortedAttrUndYcList


def _findCompositeConstituentsOriginalAcmYieldCurveList(origCompositeAcmYc):

    strYcDesc = ('composite curve \'{0}\' constituent curve'.
                format(origCompositeAcmYc.Name()))
    constituentYcList = [link.ConstituentCurve() for link
                in origCompositeAcmYc.YieldCurveLinks()]
    oidUniqueSortedConstituentYcList = _oidUniqueSorted(constituentYcList)
    for constituentYc in oidUniqueSortedConstituentYcList:
        _assertAcmYieldCurveOriginalNonHistorical(constituentYc, strYcDesc)
    return oidUniqueSortedConstituentYcList

def _findMultiCurveMembersOriginalAcmYieldCurveList(origMultiCurveOwnerAcmYc):

    strYcDesc = ('multi curve \'{0}\' member curve'.
                format(origMultiCurveOwnerAcmYc.Name()))
    memberYcList = [link.ConstituentCurve() for link
                in origMultiCurveOwnerAcmYc.YieldCurveLinks()]
    oidUniqueSortedMemberYcList = _oidUniqueSorted(memberYcList)
    for memberYc in oidUniqueSortedMemberYcList:
        _assertAcmYieldCurveOriginalNonHistorical(memberYc, strYcDesc)
    return oidUniqueSortedMemberYcList

def _findOidUniqueSortedReferencingOutOriginalAcmYieldCurveList(origAcmYc):

    refOutYcList = []  # May contain None
    refOutYcList.append(_findUnderlyingOriginalAcmYieldCurve(origAcmYc))
    origAcmYcType = origAcmYc.Type()
    if origAcmYcType in INS_SPRD_CURVE_TYPES:
        refOutYcList.append(_findDependencyOriginalAcmYieldCurve(origAcmYc))
        refOutYcList.extend(
                _findInstrumentSpreadUnderlyingOriginalAcmYieldCurveList(
                origAcmYc))
    elif origAcmYcType in ATTR_SPRD_CURVE_TYPES:
        refOutYcList.append(_findDependencyOriginalAcmYieldCurve(origAcmYc))
        refOutYcList.extend(
                _findAttributeSpreadUnderlyingOriginalAcmYieldCurveList(
                origAcmYc))
    elif origAcmYcType in COMPOSITE_CURVE_TYPES:
        refOutYcList.append(_findDependencyOriginalAcmYieldCurve(origAcmYc))
        refOutYcList.extend(
                _findCompositeConstituentsOriginalAcmYieldCurveList(
                origAcmYc))
    elif origAcmYcType in SPRD_CURVE_TYPES + INFLATION_CURVE_TYPES:
        refOutYcList.append(_findDependencyOriginalAcmYieldCurve(origAcmYc))
    elif origAcmYcType in MULTI_CURVE_TYPES:
        refOutYcList.append(_findDependencyOriginalAcmYieldCurve(origAcmYc))
    # Filter out None and then uniquify to remove duplicate
    return _oidUniqueSorted(acmYc for acmYc in refOutYcList if acmYc)

def findMemberCurves(origAcmYcList):

    memberYcList = []
    for origAcmYc in origAcmYcList:
        if origAcmYc.Type() in MULTI_CURVE_TYPES:
            memberYcList.extend(
                _findMultiCurveMembersOriginalAcmYieldCurveList(
                origAcmYc))
    return _oidUniqueSorted(acmYc for acmYc in memberYcList if acmYc)

def findBaseCurves(initOrigYcNameList,
        toExclOrigYcNameList):
    """
    Given a list of yield curve names, find the names of
    yield curves that are based upon by the given curves.
    """
    toExclOrigYcNameSet = set(toExclOrigYcNameList)
    origYcOidSet = set()
    origTransBasedAcmYcList = []
    for ycName in initOrigYcNameList:
        origAcmYc = _findOriginalAcmYieldCurve(ycName)
        if ycName in toExclOrigYcNameSet:
            continue
        origYcOid = origAcmYc.Oid()
        if origYcOid in origYcOidSet:
            continue
        origYcOidSet.add(origYcOid)
        origTransBasedAcmYcList.append(origAcmYc)
    # Breadth-First-Search
    idx = 0
    while idx < len(origTransBasedAcmYcList):
        origAcmYc = origTransBasedAcmYcList[idx]
        refOutYcList = (
                _findOidUniqueSortedReferencingOutOriginalAcmYieldCurveList(
                origAcmYc))
        for refOutYc in refOutYcList:
            refOutYcOid = refOutYc.Oid()
            if (refOutYc.Oid() not in origYcOidSet and
                    refOutYc.Name() not in toExclOrigYcNameSet):
                origYcOidSet.add(refOutYcOid)
                origTransBasedAcmYcList.append(refOutYc)
        # Increment index
        idx += 1
    return [origAcmYc.Name() for origAcmYc in origTransBasedAcmYcList]


class YCNode(object):

    # This graph contains all yield curve nodes (graph is a graph)
    graph = {}

    def __init__(self, yc):
        self.deps = \
            _findOidUniqueSortedReferencingOutOriginalAcmYieldCurveList(yc)
        self.yc = yc
        self.status = 'unchecked'
        YCNode.graph[str(yc.Oid())] = self

    def search(self):
        if self.status == 'unchecked':
            self.status = 'search'
            for node in self.deps:
                try:
                    next_status = YCNode.graph[str(node.Oid())].search()
                    if next_status == 'dep':
                        self.status = 'dep'
                        return 'dep'
                except:
                    print("""Dependency graph isn't initiate corectly
dependencies curve oid {0} isn't in dependency graph.""".format(node))
            self.status = 'non_dep'
            return 'non_dep'
        else:
            return self.status

def findDerivedCurves(initOrigYcOidList):
    """
    Given a list of yield curve Oids,
    find the Oids of yield curves that
    reference the given yield
    curves as underlying curves or dependency curves.
    """

    # Cleans graph
    YCNode.graph = {}
    #creates dependency graph
    for yc_name in findAllLiveYieldCurveNameList():
        YCNode(acm.FYieldCurve[yc_name])
    #initiates nodes in original list as 'dep'
    for yc_oid in initOrigYcOidList:
        try:
            init_node = YCNode.graph[str(yc_oid)]
            init_node.status = 'dep'
        except:
            print('Given yield curve is not alive')

    #search
    for key, value in YCNode.graph.iteritems():
        value.search()

    return [int(key) for key, value in
            YCNode.graph.iteritems() if value.status == 'dep']

def findLiveBasingYieldCurveOidList(ycOid):
    """
    Finds the oids of the live yield curves that reference the given yield
    curve as the underlying curve or dependency curve. UNION is chosen
    instead of JOIN because we join more then one table and if some tables
    are empty it can cause unexpected behaviour.
    """
    qryStmt = (
            '(SELECT seqnbr '
            'FROM yield_curve '
            'WHERE (underlying_yield_curve_seqnbr = {0} '
            'OR dependency_yield_curve_seqnbr = {0}) '
            'AND original_yc_seqnbr IS NULL '
            'AND historical_day IS NULL '
            'AND archive_status = 0) '
            'UNION '
            '(SELECT yield_curve.seqnbr '
            'FROM yield_curve, instrument_spread '
            'WHERE instrument_spread.underlying_yield_curve_seqnbr = {0} '
            'AND yield_curve.seqnbr = instrument_spread.yield_curve_seqnbr '
            'AND yield_curve.original_yc_seqnbr IS NULL '
            'AND yield_curve.historical_day IS NULL '
            'AND yield_curve.archive_status = 0) '
            'UNION '
            '(SELECT yield_curve.seqnbr '
            'FROM yield_curve, yc_attribute '
            'WHERE yc_attribute.underlying_yield_curve_seqnbr = {0} '
            'AND yield_curve.seqnbr = yc_attribute.yield_curve_seqnbr '
            'AND yield_curve.original_yc_seqnbr IS NULL '
            'AND yield_curve.historical_day IS NULL '
            'AND yield_curve.archive_status = 0) '
            'UNION '
            '(SELECT yield_curve.seqnbr '
            'FROM yield_curve, yield_curve_link '
            'WHERE yield_curve_link.member_yc_seqnbr={0} '
            'AND yield_curve.seqnbr = yield_curve_link.owner_yc_seqnbr '
            'AND yield_curve.original_yc_seqnbr IS NULL '
            'AND yield_curve.historical_day IS NULL '
            'AND yield_curve.archive_status = 0) '
            .format(ycOid))
    basingYcOids = sorted(set(row[0] for row in ael.dbsql(qryStmt)[0]))
    return basingYcOids

def findBasingYieldCurveOidList(ycOid):
    """
    Find the oids of the yield curves that references the given yield curve as
    the underlying curve or dependency curve.
    """
    qryStmt = (
            '(SELECT seqnbr '
                    'FROM yield_curve '
                    'WHERE underlying_yield_curve_seqnbr = {0} '
                            'OR dependency_yield_curve_seqnbr = {0}) '
            'UNION ALL '
            '(SELECT DISTINCT yield_curve_seqnbr '
                    'FROM instrument_spread '
                    'WHERE underlying_yield_curve_seqnbr = {0}) '
            'UNION ALL '
            '(SELECT DISTINCT yield_curve_seqnbr '
                    'FROM yc_attribute '
                    'WHERE underlying_yield_curve_seqnbr = {0})'
            'UNION ALL '
            '(SELECT owner_yc_seqnbr '
                    'FROM yield_curve_link '
                    'WHERE member_yc_seqnbr={0})'
                .format(ycOid))
    basingYcOids = sorted(set(row[0] for row in ael.dbsql(qryStmt)[0]))
    return basingYcOids


class YieldCurveHierarchicalSorter(object):
    """
    Sort by original curves' depth (ascending), then by their oid (ascending).
    """

    __SORT_DATA = collections.namedtuple('__SORT_DATA', 'depth oid name')

    __OID_AND_DEPTH = collections.namedtuple('__OID_AND_DEPTH', 'oid depth')

    class _CyclicDependencySearchPreventer(object):

        def __init__(self):

            self.__pathYcOidList = []

        def check(self, origAcmYc):

            ycOid = origAcmYc.Oid()
            assert ycOid not in self.__pathYcOidList, ('The yield curve {0} '
                    '(oid={1}) had already appeared in the search path.  This '
                    'indicates the cyclic dependency path exists.  The search '
                    'path yield curve oids so far are: {2}'.format(
                    origAcmYc.Name(), ycOid, self.__pathYcOidList))
            self.__pathYcOidList.append(ycOid)

        def _getPath(self):

            return self.__pathYcOidList

        def clone(self):

            return copy.deepcopy(self)

    def __init__(self, origYcNameList):

        self.__nameToOidAndDepthMap = {}
        self.__origYcNameSet = set(origYcNameList)
        # Start building nameToOidAndDepthMap
        origAcmYcList = [_findOriginalAcmYieldCurve(ycName) for ycName
                in origYcNameList]
        for origAcmYc in _oidUniqueSorted(origAcmYcList):
            cdsp = self._CyclicDependencySearchPreventer()
            self.__getCachedYieldCurveDepth(origAcmYc, cdsp)

    def __searchYieldCurveDepth(self, origAcmYc,
            cyclicDependencySearchPreventer):
        cyclicDependencySearchPreventer.check(origAcmYc)  # check before search
        refOutYcList = (
                _findOidUniqueSortedReferencingOutOriginalAcmYieldCurveList(
                origAcmYc))
        origAcmYcOid = origAcmYc.Oid()  # Filter away to prevent infinite loop
        refOutYcDepthList = [self.__getCachedYieldCurveDepth(acmYc,
                cyclicDependencySearchPreventer.clone())
                for acmYc in refOutYcList if acmYc.Oid() != origAcmYcOid]
        if not refOutYcDepthList:
            return 0
        return max(refOutYcDepthList) + 1

    def __getCachedYieldCurveDepth(self, origAcmYc,
            cyclicDependencySearchPreventer):

        # Now acmYc is original
        origYcName = origAcmYc.Name()
        if origYcName in self.__nameToOidAndDepthMap:
            depth = self.__nameToOidAndDepthMap[origYcName].depth
        else:
            depth = self.__searchYieldCurveDepth(origAcmYc,
                    cyclicDependencySearchPreventer)
            self.__nameToOidAndDepthMap[origYcName] = self.__OID_AND_DEPTH(
                    origAcmYc.Oid(), depth)
        return depth

    def __getSortedSortDataList(self):
        """
        Return sorted sort data extracted from cached nameToOidAndDepthMap.
        """
        sortDataList = []
        for ycName in self.__nameToOidAndDepthMap:
            oidAndDepth = self.__nameToOidAndDepthMap[ycName]
            sortDataList.append(self.__SORT_DATA(depth=oidAndDepth.depth,
                    oid=oidAndDepth.oid, name=ycName))
        return sorted(sortDataList)

    def getSortedOriginalYieldCurveNames(self):
        """
        Return the hierarchically sorted yield curve names.
        """
        sortedYcNameList = [sd.name for sd in self.__getSortedSortDataList()
                if sd.name in self.__origYcNameSet]
        return sortedYcNameList

    def getAllCachedOriginalYieldCurveNames(self):
        """
        Return the name of all the yield curves visited during the sort.  Note
        that the returned names may be more than what was given to the sorter.
        """
        return self.__nameToOidAndDepthMap.keys()

    def getStatisticsAsStringList(self):

        depthToHieSortedYcNameListMap = {}
        for sortData in self.__getSortedSortDataList():
            if sortData.depth not in depthToHieSortedYcNameListMap:
                depthToHieSortedYcNameListMap[sortData.depth] = []
            depthToHieSortedYcNameListMap[sortData.depth].append(sortData.name)
        strList = []
        strList.append('{0} Statistics'.format(self.__class__.__name__))
        numDepthLevels = len(depthToHieSortedYcNameListMap)
        strList.append('Total depth levels: {0}'.format(numDepthLevels))
        for level in range(numDepthLevels):
            sortedYcNameList = depthToHieSortedYcNameListMap[level]
            strList.append('Level {0:-2} : {1}'.format(level,
                    ','.join(sortedYcNameList)))
        return strList


def _findOnDateHistoricalYieldCurveOidsViaDbSql(origYcOid, strIsoDate):

    qryStmt = (
            'SELECT seqnbr '
            'FROM yield_curve '
            'WHERE original_yc_seqnbr = {0} '
                     'AND historical_day = \'{1}\''.format(
            origYcOid, strIsoDate))
    onDateHistYcOids = [row[0] for row in ael.dbsql(qryStmt)[0]]
    return onDateHistYcOids


def findOnDateHistoricalYieldCurveOid(origYcName, strIsoDate):
    """
    Return None or the historical yield curve oid of the date for the original
    yield curve.
    """
    origAcmYc = _findOriginalAcmYieldCurve(origYcName)
    onDateHistYcOids = _findOnDateHistoricalYieldCurveOidsViaDbSql(
            origAcmYc.Oid(), strIsoDate)
    if not onDateHistYcOids:
        return None
    assert len(onDateHistYcOids) <= 1, ('The yield curve \'{0}\' has more '
            'than one historical curve on date \'{1}\': {2}.'.format(
            origYcName, strIsoDate, repr(onDateHistYcOids)))
    return onDateHistYcOids[0]


def findOnDateHistoricalYieldCurveOidList(origYcNameList, strIsoDate):
    """
    Return a list of historical yield curve oids of the date for the original
    yield curve name specified in the given list.  If there isn't a historical
    curve on the date, the original yield curve name is skipped.
    """
    onDateHistYcOidList = []
    for ycName in origYcNameList:
        onDateHistYcOid = findOnDateHistoricalYieldCurveOid(ycName, strIsoDate)
        if not onDateHistYcOid:
            continue
        onDateHistYcOidList.append(onDateHistYcOid)
    return onDateHistYcOidList
