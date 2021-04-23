""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/vps/etc/FVPSYieldCurve.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FVPSYieldCurve - Stores historical yield curves

DESCRIPTION
    Functionality for storing and deleting historical entities of
        type YieldCurve

----------------------------------------------------------------------------"""


import collections


import acm
import ael


import FBDPCommon
import FBDPYieldCurveLib
import FBDPWorld


big_attr_spread_count = 500


def _areSameYc(acmYc1, acmYc2):

    acmYc1Oid = 0
    if acmYc1:
        acmYc1Oid = acmYc1.Oid()
    acmYc2Oid = 0
    if acmYc2:
        acmYc2Oid = acmYc2.Oid()
    return acmYc1Oid == acmYc2Oid

def _isValidToDelete(world, name, inclAllYcByDefault,
                         ycNameInclList, ycNameExclList):
    yc = acm.FYieldCurve[name]
    if not yc:
        world.logDebug('        No Yield curve named \'{0}\''
                    .format(name))
        return False

    if not (yc.DualCalibrationMainCurve() and yc.RealTimeUpdated()):
        return True

    dependencyCurve = yc.DependencyCurve()
    if not dependencyCurve:
        return True

    if not dependencyCurve.RealTimeUpdated():
        return True

    depCurveName = dependencyCurve.Name()
    if depCurveName in ycNameInclList and depCurveName not in ycNameExclList:
        return True

    if inclAllYcByDefault and depCurveName not in ycNameExclList:
        return True

    world.logDebug('        Yield curve \'{0}\' cannot be deleted '
                    'because it is real time dual calibrated with '
                    'yield curve \'{1}\''.format(name, depCurveName))

    return False

def _findSelectedOrigYcNamesToDelete(world, inclAllYcByDefault, ycNameInclList,
        ycNameExclList):

    allLiveYcNameList = FBDPYieldCurveLib.findAllLiveYieldCurveNameList()
    world.logInfo('    Filtering {0} live yield curves'.format(
            len(allLiveYcNameList)))
    world.logDebug('        inclAllYcByDefault = {0}'.format(
            inclAllYcByDefault))
    world.logDebug('        ycNameInclList = {0}'.format(ycNameInclList))
    world.logDebug('        ycNameExclList = {0}'.format(ycNameExclList))
    origYcNamesToDelete = []
    for ycName in allLiveYcNameList:
        if inclAllYcByDefault and ycName in ycNameExclList:
            world.logDebug('        Yield curve name \'{0}\' in '
                    'the exclusion list - will not delete'.format(ycName))
            continue
        if not inclAllYcByDefault and ycName not in ycNameInclList:
            world.logDebug('        Yield curve name \'{0}\' is not in '
                    'the inclusion list - will not delete'.format(ycName))
            continue
        if not _isValidToDelete(world, ycName, inclAllYcByDefault,
                                ycNameInclList, ycNameExclList):
            continue
        origYcNamesToDelete.append(ycName)
    world.logInfo('    Found {0} yield curves which historical curves are '
            'candidates for deletion.'.format(len(origYcNamesToDelete)))
    return origYcNamesToDelete


def _filterOutExtBasedYcOid(world, hieRevSortedHistYcOidsToDelete):
    """
    Filter out oids of yield curves that are based curves of some external
    curves outside the given yield curve oid list.
    """
    targetYcOidToDelete = []
    for ycOid in hieRevSortedHistYcOidsToDelete:
        # In reverse hierarchical order.  No yield curve at the back of the
        # list can base on those in the front of the list.
        basingYcOidList = FBDPYieldCurveLib.findBasingYieldCurveOidList(ycOid)
        hasExternalReference = False
        for basingYcOid in basingYcOidList:
            if basingYcOid not in targetYcOidToDelete:
                hasExternalReference = True
                break
        if hasExternalReference:
            acmYc = acm.FYieldCurve[ycOid]
            if not acmYc:
                continue
            failMsg = ('Yield curve \'{0}\'(oid={1}) cannot be deleted '
                    'because it is referenced by other yield curves:  '.format(
                    acmYc.Name(), ycOid))
            failMsg += ', '.join([('\'{0}\'(oid={1})'.format(FBDPYieldCurveLib.
                    getYieldCurveName(basingYcOid), basingYcOid))
                    for basingYcOid in basingYcOidList])
            world.summaryAddFail('YieldCurve[Hist]', ycOid, 'SELECT',
                reasons=[failMsg])
            world.logError(failMsg)
        else:
            world.summaryAddOk('YieldCurve[Hist]', ycOid, 'SELECT')
            targetYcOidToDelete.append(ycOid)
    # return the result
    return targetYcOidToDelete


def _deleteYc(world, ycToDeleteOidList):

    numYcDeleted = 0
    for oid in ycToDeleteOidList:
        aelYc = ael.YieldCurve[oid]
        ycName = aelYc.yield_curve_name
        try:
            if world.isInTestMode():
                continue
            aelYc.delete()
            world.logInfo('    Deleted historical yield curve '
                    '\'{0}\' (oid={1})'.format(ycName, oid))
            world.summaryAddOk('YieldCurve[Hist]', oid, 'DELETE')
            numYcDeleted += 1
        except Exception as e:
            failMsg = ('Unable to delete historical yield curve {0}.  '
                    '{1}'.format(aelYc.yield_curve_name, e))
            world.logError(failMsg)
            world.summaryAddFail('YieldCurve[Hist]', oid, 'DELETE',
                    reasons=[failMsg])
    world.logInfo('    Total {0} historical yield curves deleted.'.format(
            numYcDeleted))


def delete_all_yc_of_a_day(world, aelDelDate, params):
    """
    Delete all historical yield curves on a specified date. The yield curves
    lowest in the hierarchy will be deleted first
    """
    assert isinstance(aelDelDate, ael.ael_date), ('The aelDelDate must be an '
            'ael_date.')
    world.logInfo('Deleting historical yield curves as of {0}'.format(
            aelDelDate.to_string()))
    world.logInfo('    Finding yield curves on historical date '
            '{0}'.format(aelDelDate.to_string()))
    # INSPECT Stage: Find all yield curve names
    strIsoDelDate = aelDelDate.to_string(ael.DATE_ISO)
    origYcNamesToDelete = _findSelectedOrigYcNamesToDelete(world,
            inclAllYcByDefault=params.yield_curve_base,
            ycNameInclList=params.yield_curves_incl,
            ycNameExclList=params.yield_curves_excl)
    # INSPECT Stage: Reverse hierarchical sort.
    ycHieSorter = FBDPYieldCurveLib.YieldCurveHierarchicalSorter(
            origYcNamesToDelete)
    hieRevSortedOrigYcNamesToDelete = (ycHieSorter.
            getSortedOriginalYieldCurveNames()[::-1])
    # INSPECT stage: find historical yield curve oids
    hieRevSortedHistYcOidsToDelete = (FBDPYieldCurveLib.
            findOnDateHistoricalYieldCurveOidList(
            hieRevSortedOrigYcNamesToDelete, strIsoDelDate))
    targetYcOidsToDelete = _filterOutExtBasedYcOid(world,
            hieRevSortedHistYcOidsToDelete)
    # PROCESS DELETE Stage
    _deleteYc(world, targetYcOidsToDelete)
    world.logInfo('Finished deleting historical yield curves')


def _testIfNameInDb(ycname):
    """
    Is the new yield curve name already in the database ?
    """
    name = ycname.replace("'", "''")
    sql_query = ('select count(1) from yield_curve where yield_curve_name = '
            '\'{0}\' '.format(name))

    for dset in ael.dbsql(sql_query):
        for column in dset:
            if int(column[0]) > 0:
                return ycname
    return None


def _getNewYcName(ycname, today):
    """
    Create a new name for the historical yield curve
    """
    return FBDPCommon.createNewNameByAddingDate(ycname, today, _testIfNameInDb)


def _findLastHistYcOid(origYcOid, strDateToday):

    sqlQuery = ('select seqnbr from yield_curve where original_yc_seqnbr = '
            '{0} and historical_day = \'{1}\''.format(origYcOid,
            ael.date(strDateToday).to_string(ael.DATE_ISO)))

    ycOidList = FBDPCommon.get_result_in_list(ael.dbsql(sqlQuery))
    if ycOidList:
        return ycOidList[0]
    return 0


def _stripOffAttrsAndAttrSprdsForCloneYc(world, cloneYc):
    """
    Attribute spread curve's attribute and attribute spread are difficult
    to clone and commit in one transaction.  So the first step is to
    commit the attribute spread curve without the attributes and attribute
    spreads, and then in the second step to clone the attributes and attribute
    spreads only.  This is for the first step, which is to strip of all
    attributes.
    """
    if cloneYc.Type() not in FBDPYieldCurveLib.ATTR_SPRD_CURVE_TYPES:
        return cloneYc
    # From this point, only attribute spread curve is considered.
    # Here we clear out all the yield curve attribute on the cloneYc.
    if cloneYc.IsClone():
        # Since the cloneYc is still a clone and not yet made into the
        # database.  We only need to clear the attribute container.  The
        # cloned curve will be committed later, and those attribute will then
        # not committed into the database.
        cloneYc.Attributes().Clear()
    else:
        # Since the cloneYc is no longer a fresh clone, it must be the one
        # recently de-archived.  In this case, we need to delete those yield
        # curve attributes that made into the database.  Now we need to go
        # through ael because acm cache may not have been updated yet.  But
        # we need to delete them via acm, because ael would insist their
        # ael yield curve to be deleted at the same time.
        aelAttrList = [aelAttr for aelAttr in ael.YCAttribute.select(
                'yield_curve_seqnbr = {0}'.format(cloneYc.Oid()))]
        if aelAttrList:
            for aelAttr in aelAttrList:
                attrOid = aelAttr.seqnbr
                acmAttr = FBDPCommon.ael_to_acm(aelAttr)
                try:
                    world.logDebug('            Stripping off attribute '
                            '{0}'.format(attrOid))
                    acmAttr.Delete()
                    world.summaryAddOk('YCAttribute', attrOid, 'DELETE')
                except Exception as e:
                    failMsg = ('Unable to delete attribute {0}.  '
                            '{1}'.format(attrOid, e))
                    world.summaryAddFail('YCAttribute', attrOid, 'DELETE',
                            reasons=[failMsg])
                    world.logError(failMsg)
                    cloneYc = None
                    break
        # If something went wrong, cloneYc would have been None.
        if cloneYc:
            cloneYc.Attributes().Clear()
    # cloneYc's attribute cleared.  Returnt the cloneYc
    return cloneYc


def _cloneAttrsAndAttrSprdsForCloneYc(world, origYc, cloneYc, ycCloneMngr):
    """
    Attribute spread curve's attribute and attribute spread are difficult
    to clone and commit in one transaction.  So the first step is to
    commit the attribute spread curve without the attributes and attribute
    spreads, and then in the second step to clone the attributes and attribute
    spreads only.  This is for the second step.
    """
    if cloneYc.Type() not in FBDPYieldCurveLib.ATTR_SPRD_CURVE_TYPES:
        return cloneYc
    # Clone attributes
    cloneAttrList = []
    for origAttr in origYc.Attributes():
        cloneAttr = origAttr.Clone()
        cloneAttr.Curve(cloneYc)
        _cloneYcAttr_setUnderlyingCurveToClone(cloneAttr, origAttr,
                ycCloneMngr)
        # Newly cloned attribute spread point to a newly created yield
        # curve point.  However, we should move the reference from that
        # newly created yield curve point to the only already exists.
        for cloneAttrSprd in cloneAttr.Spreads():
            clonePtDatePeriod = cloneAttrSprd.Point().DatePeriod()
            clonePtDate = cloneAttrSprd.Point().Date()
            clonePtInstrument = cloneAttrSprd.Point().Instrument()
            clonePt = None
            for pt in cloneYc.Points():
                if (pt.DatePeriod() == clonePtDatePeriod and
                        pt.Date() == clonePtDate and
                        pt.Instrument() == clonePtInstrument):
                    clonePt = pt
                    break
            if clonePt:
                cloneAttrSprd.Point(clonePt)
        # Cache up this attribute for commit.
        cloneAttrList.append(cloneAttr)
    # split cloneAttrList into batches
    batchedCloneAttrsList = []
    batchSize = int(big_attr_spread_count)
    numBatch = len(cloneAttrList) // batchSize + 1
    world.logDebug('            Splitting attributes into {0} '
            'batches.'.format(numBatch))
    for batchNum in range(0, numBatch):
        batchBeginNum = batchNum * batchSize
        batchEndNum = (batchNum + 1) * batchSize
        batchedCloneAttrsList.append(cloneAttrList[batchBeginNum:batchEndNum])
    # Process batch by batch
    for cloneAttrBatch in batchedCloneAttrsList:
        try:
            acm.BeginTransaction()
            for cloneAttr in cloneAttrBatch:
                world.logDebug('            Cloning attribute {0} for '
                        'historical yield curve \'{1}\''.format(
                        cloneAttr.Oid(), cloneYc.Name()))
                cloneAttr.Commit()
            acm.CommitTransaction()
            for cloneAttr in cloneAttrBatch:
                world.summaryAddOk('YCAttribute[Hist]', cloneAttr.Oid(),
                        'CREATE')
        except Exception as e:
            acm.AbortTransaction()
            failMsg = ('Unable to create historical attributes for '
                    'historical yield curve \'{0}\' because some attributes '
                    'in the batch failed to be commited.  {1}'.format(
                    cloneYc.Name(), e))
            for cloneAttr in cloneAttrBatch:
                world.summaryAddFail('YCAttribute[Hist]', cloneAttr.Oid(),
                        'CREATE', reasons=[failMsg])
            world.logError(failMsg)
            cloneYc = None
            break
    return cloneYc


def _cloneYc_setUnderlyingCurveToClone(cloneYc, origYc, ycCloneMngr):

    origYcUndYc = origYc.UnderlyingCurve()
    if not origYcUndYc:
        cloneYc.UnderlyingCurve(None)
        return
    origYcUndYcOid = origYcUndYc.Oid()
    cloneUndYc = ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
            origYcOid=origYcUndYcOid,
            strYcRelationship='underlying curve',
            strHostEntityType='yield curve')
    cloneYc.UnderlyingCurve(cloneUndYc)


def _cloneYc_setDependencyCurveToClone(cloneYc, origYc, ycCloneMngr):

    origYcDepYc = origYc.DependencyCurve()
    if not origYcDepYc:
        cloneYc.DependencyCurve(None)
        return
    origYcDepYcOid = origYcDepYc.Oid()
    cloneDepYc = ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
            origYcOid=origYcDepYcOid,
            strYcRelationship='dependency curve',
            strHostEntityType='yield curve')
    cloneYc.DependencyCurve(cloneDepYc)

def _updateDepCurves(yieldCurve, ycCloneMngr):
    dependencyCurve = yieldCurve.DependencyCurve()
    if dependencyCurve is None:
        return

    oid = dependencyCurve.Oid()
    histDepCurve = ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
            origYcOid=oid,
            strYcRelationship='dependency curve',
            strHostEntityType='yield curve')
    yieldCurve.DependencyCurve(histDepCurve)

def _cloneYc_setInstrumentSpreadUnderlyingCurveToClone(cloneYc, ycCloneMngr):

    if cloneYc.Type() not in FBDPYieldCurveLib.INS_SPRD_CURVE_TYPES:
        return
    for cloneInsSprd in cloneYc.InstrumentSpreads():
        _cloneYcInsSprd_setUnderlyingCurveToClone(cloneInsSprd, ycCloneMngr)


def _cloneYc_setConstituentsCurvesToClones(compositeClone, origYc,
        ycCloneMngr):

    if compositeClone.Type() not in FBDPYieldCurveLib.COMPOSITE_CURVE_TYPES:
        return
    compositeClone.YieldCurveLinks().Clear()
    for originalLink in origYc.YieldCurveLinks():
        cloneConstituentYc = (
                ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
                        origYcOid=originalLink.ConstituentCurve().Oid(),
                        strYcRelationship='constituent curve',
                        strHostEntityType='yield curve'))
        link = compositeClone.AddConstituentCurve(cloneConstituentYc)
        link.LinkType(originalLink.LinkType())

def _cloneYc_setMemberCurvesToClones(multiCurveClone, origYc,
        ycCloneMngr):

    if multiCurveClone.Type() not in FBDPYieldCurveLib.MULTI_CURVE_TYPES:
        return
    multiCurveClone.YieldCurveLinks().Clear()
    for originalLink in origYc.YieldCurveLinks():
        cloneMemberYc = (
                ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
                        origYcOid=originalLink.ConstituentCurve().Oid(),
                        strYcRelationship='member curve',
                        strHostEntityType='yield curve'))
        link = multiCurveClone.AddConstituentCurve(cloneMemberYc)

def _cloneYc_moveUnderlyingCurveToClone(cloneYc, origYc, ycCloneMngr):

    if _areSameYc(cloneYc.UnderlyingCurve(), origYc.UnderlyingCurve()):
        return
    _cloneYc_setUnderlyingCurveToClone(cloneYc, origYc, ycCloneMngr)


def _cloneYc_moveDependencyCurveToClone(cloneYc, origYc, ycCloneMngr):

    if _areSameYc(cloneYc.DependencyCurve(), origYc.DependencyCurve()):
        return
    _cloneYc_setDependencyCurveToClone(cloneYc, origYc, ycCloneMngr)


def _cloneYcInsSprd_setUnderlyingCurveToClone(cloneInsSprd, ycCloneMngr):

    cloneYcInsSprdUndYc = cloneInsSprd.UnderlyingYieldCurve()
    if not cloneYcInsSprdUndYc:
        cloneInsSprd.UnderlyingYieldCurve(None)
        return
    cloneYcInsSprdUndYcOid = cloneYcInsSprdUndYc.Oid()
    cloneInsSprdUndYc = ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
            origYcOid=cloneYcInsSprdUndYcOid,
            strYcRelationship='underlying curve',
            strHostEntityType=('instrument spread of the instrument spread '
                    'yield curve'))
    cloneInsSprd.UnderlyingYieldCurve(cloneInsSprdUndYc)


def _cloneYcAttr_setUnderlyingCurveToClone(cloneAttr, origAttr, ycCloneMngr):

    origAttrUndYc = origAttr.UnderlyingCurve()
    if not origAttrUndYc:
        cloneAttr.UnderlyingCurve(None)
        return
    origAttrUndYcOid = origAttrUndYc.Oid()
    cloneAttrUndYc = ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
            origYcOid=origAttrUndYcOid,
            strYcRelationship='underlying curve',
            strHostEntityType=('yield curve attribute of the attribute spread '
                    'yield curve'))
    cloneAttr.UnderlyingCurve(cloneAttrUndYc)


def _cloneYc_moveConstituentCurvesToClone(compositeClone, origYc, ycCloneMngr):

    if compositeClone.Type() not in FBDPYieldCurveLib.COMPOSITE_CURVE_TYPES:
        return

    compositeClone.YieldCurveLinks().Delete()
    for originalLink in origYc.YieldCurveLinks():
        cloneConstituentYc = (
                ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
                        origYcOid=originalLink.ConstituentCurve().Oid(),
                        strYcRelationship='constituent curve',
                        strHostEntityType='yield curve'))
        link = compositeClone.AddConstituentCurve(cloneConstituentYc)
        link.LinkType(originalLink.LinkType())

def _cloneYc_moveMemberCurvesToClone(multiCurveClone, origYc, ycCloneMngr):

    if multiCurveClone.Type() not in FBDPYieldCurveLib.MULTI_CURVE_TYPES:
        return
    multiCurveClone.YieldCurveLinks().Delete()
    for originalLink in origYc.YieldCurveLinks():
        # should already have been created
        cloneMemberYc = (
                ycCloneMngr.getOrLookUpExistingHistoricalOrUseOrigYc(
                        origYcOid=originalLink.ConstituentCurve().Oid(),
                        strYcRelationship='member curve',
                        strHostEntityType='yield curve'))
        link = multiCurveClone.AddConstituentCurve(cloneMemberYc)

def _dearchiveAndPrepCloneYc(world, ycCloneMngr, origYc, lastHistYcOid):
    # Dearchive if it is archived.
    aelLastHistYc = ael.YieldCurve[lastHistYcOid]
    try:
        # De-archive the curve first, so that the ael functions
        # yc.attributes(), yc.instrument_spreads(), yc.points()
        # and yc.benchmarks() could work properly.  Here the
        # yield curve attributes are not de-archived, because they
        # are about to be stripped off from the curve anyway.
        if aelLastHistYc.archive_status:
            aelLastHistYcClone = aelLastHistYc.clone()
            aelLastHistYcClone.archive_status = 0
            aelLastHistYcClone.commit()
            aelLastHistYc = ael.YieldCurve[lastHistYcOid]
        for aelInsSprd in aelLastHistYc.instrument_spreads():
            if aelInsSprd.archive_status:
                aelInsSprdClone = aelInsSprd.clone()
                aelInsSprdClone.archive_status = 0
                aelInsSprdClone.commit()
        for aelPt in aelLastHistYc.points():
            if aelPt.archive_status:
                aelPtClone = aelPt.clone()
                aelPtClone.archive_status = 0
                aelPtClone.commit()
        for aelBm in aelLastHistYc.benchmarks():
            if aelBm.archive_status:
                aelBmClone = aelBm.clone()
                aelBmClone.archive_status = 0
                aelBmClone.commit()
        aelLastHistYcClone = aelLastHistYc.clone()
        aelLastHistYcClone.commit()
        world.summaryAddOk('YieldCurve[Hist]', lastHistYcOid, 'DEARCHIVE')
    except Exception as e:
        failMsg = ('Unable to de-archive historical yield curve \'{0}\'.  '
                '{1}'.format(aelLastHistYc.yield_curve_name, e))
        world.summaryAddFail('YieldCurve[Hist]', lastHistYcOid, 'DEARCHIVE',
                reasons=[failMsg])
        world.logError(failMsg)
        return None
    # Now work with acm.  Use the ael yield curve to guide acm to find the
    # recently de-archived yield curve.  At this point the acm cache may not
    # have been updated about the recent de-archival in ael.
    cloneYc = acm.Ael.AelToFObject(ael.YieldCurve[lastHistYcOid])
    # Move the underlying curve reference
    _cloneYc_moveUnderlyingCurveToClone(cloneYc, origYc, ycCloneMngr)
    # Move the dependency curve reference
    _cloneYc_moveDependencyCurveToClone(cloneYc, origYc, ycCloneMngr)
    # Move the instrument spread underlying reference
    _cloneYc_setInstrumentSpreadUnderlyingCurveToClone(cloneYc, ycCloneMngr)
    # Move the constituent curve references
    _cloneYc_moveConstituentCurvesToClone(cloneYc, origYc, ycCloneMngr)
    # Move the member curve references
    _cloneYc_moveMemberCurvesToClone(cloneYc, origYc, ycCloneMngr)
    # Attribute spread are copied in different transaction
    cloneYc = _stripOffAttrsAndAttrSprdsForCloneYc(world, cloneYc)
    # Commit the cloneYc (without attributes and attribute spreads)
    if cloneYc:
        try:
            cloneYc.Commit()
            world.summaryAddOk('YieldCurve[Hist]', cloneYc.Oid(), 'REDEFINE')
        except Exception as e:
            failMsg = ('Unable to redefine the de-archive historical yield '
                    'curve \'{0}\' as a clone of the original.  {1}'.format(
                    cloneYc.Name(), e))
            world.summaryAddFail('YieldCurve[Hist]', lastHistYcOid, 'REDEFINE',
                    reasons=[failMsg])
            world.logError(failMsg)
            cloneYc = None
    # Clone attributes and attribute spreads
    if cloneYc:
        cloneYc = _cloneAttrsAndAttrSprdsForCloneYc(world, origYc, cloneYc,
                ycCloneMngr)
    return cloneYc

def _cloneYc(world, today, origYc,
         realtimeUpdatedUnchanged):
    cloneYc = origYc.Clone()
    cloneYc.Name(_getNewYcName(origYc.Name(), today))
    cloneYc.OriginalCurve(origYc)
    cloneYc.HistoricalDay(today)
    cloneYc.User(origYc.User())
    cloneYc.UpdateInterval(0)
    if not realtimeUpdatedUnchanged:
    # Turn off real time updates for clone yield curves
        cloneYc.RealTimeUpdated(0)
    else:
        cloneYc.RealTimeUpdated(origYc.RealTimeUpdated())
    return cloneYc

def _createAndPrepCloneYc(world, ycCloneMngr, origYc, today,
         realtimeUpdatedUnchanged):
    acm.BeginTransaction()
    cloneYc = _cloneYc(world, today, origYc,
         realtimeUpdatedUnchanged)
    # Map underlying yield_curve to a clone
    _cloneYc_setUnderlyingCurveToClone(cloneYc, origYc, ycCloneMngr)
    # Map dependency yield_curve to a historical
    _cloneYc_setDependencyCurveToClone(cloneYc, origYc, ycCloneMngr)
    # InsSpread handling
    _cloneYc_setInstrumentSpreadUnderlyingCurveToClone(cloneYc, ycCloneMngr)
    # Attribute spread are copied in different transaction
    cloneYc = _stripOffAttrsAndAttrSprdsForCloneYc(world, cloneYc)
    # Map constituent curves to clones
    _cloneYc_setConstituentsCurvesToClones(cloneYc, origYc, ycCloneMngr)
    # Map member curves to clones
    _cloneYc_setMemberCurvesToClones(cloneYc, origYc, ycCloneMngr)
    # Commit the cloneYc (without attributes and attribute spreads)
    if cloneYc:
        try:
            world.logDebug('        Cloning historical yield curve '
                    '\'{0}\''.format(cloneYc.Name()))
            cloneYc.Commit()
            world.summaryAddOk('YieldCurve[Hist]', cloneYc.Oid(), 'CREATE')
        except Exception as e:
            failMsg = ('Unable to create historical yield curve \'{0}\'.  '
                    '{1}'.format(cloneYc.Name(), e))
            world.summaryAddFail('YieldCurve[Hist]', cloneYc.Oid(), 'CREATE',
                    reasons=[failMsg])
            world.logError(failMsg)
            cloneYc = None
            acm.AbortTransaction()

    acm.CommitTransaction()

    # Clone attributes and attribute spreads
    if cloneYc:
        cloneYc = _cloneAttrsAndAttrSprdsForCloneYc(world, origYc, cloneYc,
            ycCloneMngr)

    return cloneYc


class _YcCloneMngr(FBDPWorld.WorldInterface):
    """
    Manages the yield curves being duplicated.  This class behave like an
    ordered dict to map original yield curve's oid to the clone yield curve,
    with additional functionality to look up existing historical yield curve if
    the curve is not being duplicated.
    """
    def __init__(self, world, strIsoDateToday):

        FBDPWorld.WorldInterface.__init__(self, world)
        self.__strIsoDateToday = strIsoDateToday
        self.__origYcOidOrderList = []
        self.__origYcOidToYcCloneMap = {}

    def getItems(self):
        return self.__origYcOidToYcCloneMap

    def _get(self, origYcOid):

        return self.__origYcOidToYcCloneMap.get(origYcOid)

    def _lookUpExistingHistorical(self, origYcOid):

        lastHistYcOid = _findLastHistYcOid(origYcOid, self.__strIsoDateToday)
        cloneYc = None
        if lastHistYcOid:
            cloneYc = FBDPYieldCurveLib.getMayBeArchivedAcmYieldCurve(
                    lastHistYcOid)
        return cloneYc

    def getOrLookUpExistingHistoricalOrUseOrigYc(self, origYcOid,
            strYcRelationship, strHostEntityType):

        retYc = self._get(origYcOid)
        if retYc:
            return retYc
        origYc = FBDPYieldCurveLib.getLiveAcmYieldCurve(origYcOid)
        retYc = self._lookUpExistingHistorical(origYcOid)
        origYcName = acm.FYieldCurve[origYcOid].Name()
        if origYc:
            origYcName = origYc.Name()
        if retYc:
            msg = ('NOTICE: New historical copy of the {strYcRelationship} '
                    '"{origYcName}" is not selected to be created.  The '
                    'historical {strHostEntityType} has instead used an '
                    'existing historical copy as its '
                    '{strYcRelationship}.'.format(
                    strYcRelationship=strYcRelationship, origYcName=origYcName,
                    strHostEntityType=strHostEntityType))
        else:
            retYc = origYc
            msg = ('NOTICE: New historical copy of the {strYcRelationship} '
                    '"{origYcName}" is not selected to be created, and no '
                    'existing historical version is found.  The historical '
                    '{strHostEntityType} has instead used the original as '
                    'its {strYcRelationship}.'.format(
                    strYcRelationship=strYcRelationship, origYcName=origYcName,
                    strHostEntityType=strHostEntityType))
        self._logInfo(msg)
        return retYc

    def set(self, origYcOid, cloneYc):

        assert origYcOid not in self.__origYcOidToYcCloneMap, ('There has '
                'been a cloneYc previously set for origYcOid={0}'.format(
                origYcOid))
        self.__origYcOidOrderList.append(origYcOid)
        self.__origYcOidToYcCloneMap[origYcOid] = cloneYc


def _duplicateOrigYc(world, today, ycToStoreList, memberCurves,
                    realtimeUpdatedUnchanged):

    ycCloneMngr = _YcCloneMngr(world, ael.date(today).to_string(ael.DATE_ISO))
    for origYc in ycToStoreList:
        origYcOid = origYc.Oid()
        world.logDebug('        Duplicating from original yield curve '
                '\'{0}\'(oid={1})'.format(origYc.Name(), origYcOid))
        lastHistYcOid = _findLastHistYcOid(origYcOid, today)
        if lastHistYcOid:
            cloneYc = _dearchiveAndPrepCloneYc(world, ycCloneMngr, origYc,
                    lastHistYcOid)
        else:
            cloneYc = _createAndPrepCloneYc(world, ycCloneMngr,
                    origYc, today, realtimeUpdatedUnchanged)
        if not cloneYc:
            world.logError('Unable to proceed.')
            continue
        ycCloneMngr.set(origYcOid, cloneYc)
        world.logInfo('        Duplicated into historical yield curve '
                '\'{0}\'(oid={1})'.format(cloneYc.Name(), cloneYc.Oid()))
    origYcOidAndYcClonePairs = ycCloneMngr.getItems()

    # Update dependency for member yield curves
    world.logInfo('    Updating dependency for member yield curves')
    memberCurvesOids = [memberCurve.Oid()
                for memberCurve in memberCurves]
    for origYcOid, cloneMember in origYcOidAndYcClonePairs.items():
        if origYcOid in memberCurvesOids:
            _updateDepCurves(cloneMember, ycCloneMngr)
            cloneMember.Commit()
    return origYcOidAndYcClonePairs


_RecalcYcInfo = collections.namedtuple('_RecalcYcInfo',
        'origYcOid cloneYc isRecalculated cloneYcName')

def __recalcYcFailed(world, recalcYcInfoList, origYcOid, cloneYc, cloneYcName,
                     origYcName, resultErrorMsgs):
    recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                                          isRecalculated=False,
                                          cloneYcName=cloneYcName))
    errMsg = 'Skipping historical yield curve '\
    '\'{0}\'. Calculation Failed. Reasons: {1}. '.format(origYcName,
                                                         resultErrorMsgs)
    world.summaryAddFail('YieldCurve[Hist]', cloneYc.Oid(), 'RECALCULATE',
                         reasons=[errMsg])
    world.logError(errMsg)

def _recalculateYcClones(world, origYcOidAndYcClonePairs, recalculationOrder):
    """
    Note, yield curves internally may recognise each other by name.  So in
    order to ensure the calculation is performed correctly, the name may be
    temporarily replaced with the original yield curve's name before commit.
    Please pay attention to the names of the yield curve.
    """

    #Proxy object for cloned yield curve
    unknownClonedYc = acm.FBenchmarkCurve()
    unknownClonedYc.Name('UnknownClonedYc')
    failedYieldCurveOids = []
    # First, recalculate (and don't commit) loop
    recalcYcInfoList = []
    for origYcOid in recalculationOrder:
        try:
            cloneYc = origYcOidAndYcClonePairs[origYcOid]
            cloneYcName = cloneYc.Name()

            if origYcOid in failedYieldCurveOids:
                ignMsg = ('Skipping recalculation of historical yield curve '
                        '\'{0}\'.  Calculation of base curve '
                        'has failed.'.format(cloneYcName))
                world.summaryAddIgnore('YieldCurve[Hist]', cloneYc.Oid(),
                        'RECALCULATE', reasons=[ignMsg])
                world.logWarning(ignMsg)
                recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                        isRecalculated=False, cloneYcName=cloneYcName))
                continue

            if cloneYc.Type() in FBDPYieldCurveLib.ATTR_SPRD_CURVE_TYPES:
                ignMsg = ('Skipping recalculation of historical yield curve '
                   '\'{0}\'.  Curve type \'{1}\' ignored in '
                   'recalculation.'.format(cloneYcName, cloneYc.Type()))
                world.summaryAddIgnore('YieldCurve[Hist]', cloneYc.Oid(),
                        'RECALCULATE', reasons=[ignMsg])
                world.logWarning(ignMsg)
                recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                        isRecalculated=False, cloneYcName=cloneYcName))
                continue

            if cloneYc.Type() in FBDPYieldCurveLib.COMPOSITE_CURVE_TYPES:
                ignMsg = ('Skipping recalculation of historical yield curve '
                   '\'{0}\'. Calculate method not supported for curve type '
                   '\'{1}\'(both live and historical composite curves are '
                   'only calculated from its constituent curves).'.format(
                        cloneYcName, cloneYc.Type()))
                world.summaryAddIgnore('YieldCurve[Hist]', cloneYc.Oid(),
                        'RECALCULATE', reasons=[ignMsg])
                world.logInfo(ignMsg)
                recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                        isRecalculated=False, cloneYcName=cloneYcName))
                continue

            if cloneYc.Type() not in (
                FBDPYieldCurveLib.CURVE_TYPES_SUPPORT_CALCULATE +
                FBDPYieldCurveLib.CURVE_TYPES_SUPPORT_CALIBRATE_SPREADS):
                ignMsg = ('Skipping recalculation of historical yield curve '
                  '\'{0}\'.  Calculate method not supported for curve type '
                  '\'{1}\'.'.format(cloneYcName, cloneYc.Type()))
                world.summaryAddIgnore('YieldCurve[Hist]', cloneYc.Oid(),
                        'RECALCULATE', reasons=[ignMsg])
                world.logWarning(ignMsg)
                recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                        isRecalculated=False, cloneYcName=cloneYcName))
                continue
            if not cloneYc.Benchmarks():
                ignMsg = ('Skipping recalculation of historical yield curve '
                        '\'{0}\'.  This yield curve has no benchmarks.'.format(
                        cloneYcName))
                world.summaryAddIgnore('YieldCurve[Hist]', cloneYc.Oid(),
                        'RECALCULATE', reasons=[ignMsg])
                world.logInfo(ignMsg)
                recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                        isRecalculated=False, cloneYcName=cloneYcName))
                continue
            if (cloneYc.Type() in FBDPYieldCurveLib.INFLATION_CURVE_TYPES and
                    len(cloneYc.Benchmarks()) == 1 and
                    cloneYc.Benchmarks()[0].Instrument().
                    InsType() == 'PriceIndex'):
                ignMsg = ('Skipping recalculation of historical yield curve '
                        '\'{0}\'.  This inflation yield curve only has one '
                        'benchmark being a Price Index.'.format(
                        cloneYcName))
                world.summaryAddIgnore('YieldCurve[Hist]', cloneYc.Oid(),
                        'RECALCULATE', reasons=[ignMsg])
                world.logInfo(ignMsg)
                recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                        isRecalculated=False, cloneYcName=cloneYcName))
                continue

            origYc = FBDPYieldCurveLib.getLiveAcmYieldCurve(origYcOid)
            origYcName = origYc.Name()
            world.logDebug('        Recalculating historical yield curve '
                    '\'{0}\'.'.format(cloneYcName))
            recalcYc = cloneYc.Clone()
            recalcYc.Name(origYcName)
            calibrationResults = acm.FCalibrationResults()
            rtn = recalcYc.Calculate(calibrationResults)
        except:
            if 'origYcName' not in locals():
                proxyOrigYc = acm.FYieldCurve[origYcOid]
                if proxyOrigYc and origYcOid not in failedYieldCurveOids:
                    failedYieldCurveOids.append(proxyOrigYc.Oid())
                    failedYieldCurveOids = \
                    FBDPYieldCurveLib.findDerivedCurves(failedYieldCurveOids)
                origYcName = proxyOrigYc.Name() if proxyOrigYc else \
                                                'UnknownYieldCurve'

            if 'cloneYc' not in locals():
                cloneYc = unknownClonedYc
                cloneYcName = cloneYc.Name()

            if 'cloneYcName' not in locals():
                cloneYcName = cloneYc.Name()

            __recalcYcFailed(world, recalcYcInfoList,
                origYcOid, cloneYc, cloneYcName, origYcName,
                'Recalculate failed for unknown reason')
            continue

        resultErrorMsgs = ''
        for result in calibrationResults.Results().Values():
            if result.SolverResult().ErrorMessage():
                resultErrorMsgs = resultErrorMsgs + ' ' + \
                    result.SolverResult().ErrorMessage()
        if rtn or not resultErrorMsgs:
            cloneYc.Apply(recalcYc)
            # cloneYc's name is temporarily the original
            recalcYcInfoList.append(_RecalcYcInfo(origYcOid, cloneYc,
                isRecalculated=True, cloneYcName=cloneYcName))
            world.logInfo('        Recalculated historical yield curve '
                '\'{0}\' (oid={1})'.format(cloneYcName, cloneYc.Oid()))
        else:
            __recalcYcFailed(world, recalcYcInfoList,
                origYcOid, cloneYc, cloneYcName, origYcName, resultErrorMsgs)

    # Second, get-the-name-back and then commit-the-recalculated loop
    recalcOrigYcOidAndYcClonePairs = {}
    recalcOrigYcOidOrder = []
    for recalcYcInfo in recalcYcInfoList:
        origYcOid = recalcYcInfo.origYcOid
        cloneYc = recalcYcInfo.cloneYc
        cloneYcName = recalcYcInfo.cloneYcName
        # Whether or not recalculated, put into the return list
        recalcOrigYcOidAndYcClonePairs[origYcOid] = cloneYc
        recalcOrigYcOidOrder.append(origYcOid)
        # If not recalculated, don't need to commit.
        if not recalcYcInfo.isRecalculated:
            continue
        try:
            # Recalculate
            world.logDebug('        Committing recalculated historical yield '
                    'curve \'{0}\'.'.format(cloneYcName))
            cloneYc.Name(cloneYcName)
            cloneYc.Commit()
            world.summaryAddOk('YieldCurve[Hist]', cloneYc.Oid(),
                    'RECALCULATE')
        except Exception as e:
            failMsg = ('Unable to commit recalculated historical yield curve '
                    '\'{0}\'.  {1}'.format(cloneYcName, e))
            world.summaryAddFail('YieldCurve[Hist]', cloneYc.Oid(),
                    'RECALCULATE', reasons=[failMsg])
            world.logError(failMsg)
            continue
        world.logInfo('        Committed recalculated historical yield curve '
                '\'{0}\' (oid={1})'.format(cloneYcName, cloneYc.Oid()))
    # Finally return
    return recalcOrigYcOidAndYcClonePairs, recalcOrigYcOidOrder


def _archiveAttrsAndAttrsSprdsForCloneYc(world, cloneYc):

    if cloneYc.Type() not in FBDPYieldCurveLib.ATTR_SPRD_CURVE_TYPES:
        return cloneYc
    # archive attribute and attribute spreads
    cloneAttrList = [attr for attr in cloneYc.Attributes()]
    # split cloneAttrList into batches
    batchedCloneAttrsList = []
    batchSize = int(big_attr_spread_count)
    numBatch = len(cloneAttrList) // batchSize + 1
    world.logDebug('            Splitting attributes into {0} '
            'batches.'.format(numBatch))
    for batchNum in range(0, numBatch):
        batchBeginNum = batchNum * batchSize
        batchEndNum = (batchNum + 1) * batchSize
        batchedCloneAttrsList.append(cloneAttrList[batchBeginNum:batchEndNum])
    # Process batch by batch
    for cloneAttrBatch in batchedCloneAttrsList:
        try:
            acm.BeginTransaction()
            for cloneAttr in cloneAttrBatch:
                cloneAttr.ArchiveStatus(1)
                for cloneAttrSprd in cloneAttr.Spreads():
                    cloneAttrSprd.ArchiveStatus(1)
                world.logDebug('            Archiving attribute {0} for '
                        'historical yield curve \'{1}\''.format(
                        cloneAttr.Oid(), cloneYc.Name()))
                cloneAttr.Commit()
            acm.CommitTransaction()
            for cloneAttr in cloneAttrBatch:
                world.summaryAddOk('YCAttribute[Hist]', cloneAttr.Oid(),
                        'ARCHIVE')
        except Exception as e:
            acm.AbortTransaction()
            failMsg = ('Unable to archive historical attributes for '
                    'historical yield curve \'{0}\' because some attributes '
                    'in the batch failed to be commited.  {1}'.format(
                    cloneYc.Name(), e))
            for cloneAttr in cloneAttrBatch:
                world.summaryAddFail('YCAttribute[Hist]', cloneAttr.Oid(),
                        'ARCHIVE', reasons=[failMsg])
            world.logError(failMsg)
            cloneYc = None
            break
    return cloneYc


def _archiveYcClones(world, origYcOidAndYcClonePairs,
                    recalculationOrder):

    arcOrigYcOidAndYcClonePairs = []
    for origYcOid in recalculationOrder:
        cloneYc = origYcOidAndYcClonePairs[origYcOid]
        # Yield curve attributes and yield curve attribute spreads are
        # archive-and-committed separately.  The number may be large, and may
        # not be able to fit into one transaction.
        cloneYc = _archiveAttrsAndAttrsSprdsForCloneYc(world, cloneYc)
        acm.BeginTransaction()
        if not cloneYc or cloneYc.IsDeleted():
            continue
        # Now archive the curve itself.
        cloneYc.ArchiveStatus(1)
        for pt in cloneYc.Points():
            pt.ArchiveStatus(1)
        for bm in cloneYc.Benchmarks():
            bm.ArchiveStatus(1)
        if cloneYc.Type() in FBDPYieldCurveLib.INS_SPRD_CURVE_TYPES:
            for insSprd in cloneYc.InstrumentSpreads():
                insSprd.ArchiveStatus(1)
        try:
            world.logDebug('        Archiving historical yield curve '
                    '\'{0}\'.'.format(cloneYc.Name()))
            cloneYc.Commit()
            world.summaryAddOk('YieldCurve[Hist]', cloneYc.Oid(), 'ARCHIVE')
            arcOrigYcOidAndYcClonePairs.append((origYcOid, cloneYc))
        except Exception as e:
            failMsg = ('Unable to archive historical yield curve \'{0}\'.  '
                    '{1}'.format(cloneYc.Name(), e))
            world.summaryAddFail('YieldCurve[Hist]', cloneYc.Oid(), 'ARCHIVE',
                    reasons=[failMsg])
            world.logError(failMsg)
            acm.AbortTransaction()
            continue

        acm.CommitTransaction()
        world.logInfo('        Archived historical yield curve \'{0}\' '
                '(oid={1})'.format(cloneYc.Name(), cloneYc.Oid()))
    return arcOrigYcOidAndYcClonePairs


def _findSelectedOrigYcNamesToStore(world, inclAllYcByDefault, ycNameInclList,
        ycNameExclList):

    allLiveYcNameList = FBDPYieldCurveLib.findAllLiveYieldCurveNameList()
    world.logInfo('    Filtering {0} live yield curves'.format(
            len(allLiveYcNameList)))
    world.logDebug('        inclAllYcByDefault = {0}'.format(
            inclAllYcByDefault))
    world.logDebug('        ycNameInclList = {0}'.format(ycNameInclList))
    world.logDebug('        ycNameExclList = {0}'.format(ycNameExclList))
    origYcNamesToStore = []
    for ycName in allLiveYcNameList:
        if inclAllYcByDefault and ycName in ycNameExclList:
            world.logDebug('        Yield curve name \'{0}\' in '
                    'the exclusion list - will not store'.format(ycName))
            continue
        if not inclAllYcByDefault and ycName not in ycNameInclList:
            world.logDebug('        Yield curve name \'{0}\' is not in '
                    'the inclusion list - will not store'.format(ycName))
            continue
        origYcNamesToStore.append(ycName)
    world.logInfo('    Found {0} yield curves to store.'.format(
            len(origYcNamesToStore)))
    return origYcNamesToStore


def update_all_yield_curves(world, params, today):
    """
    Store historical yield curves according to the settings in FVPSVariables.
    Main function.
    """
    delete_all_yc_of_a_day(world, ael.date(today), params)
    world.logInfo('Storing yield curves')
    selOrigYcNameList = _findSelectedOrigYcNamesToStore(world,
            inclAllYcByDefault=params.yield_curve_base,
            ycNameInclList=params.yield_curves_incl,
            ycNameExclList=params.yield_curves_excl)
    world.logInfo('    Searching and include based curves.')
    selAndBasedOrigYcNameList = (FBDPYieldCurveLib.findBaseCurves(
            initOrigYcNameList=selOrigYcNameList,
            toExclOrigYcNameList=params.yield_curves_excl))

    ycHieSorter = FBDPYieldCurveLib.YieldCurveHierarchicalSorter(
            selAndBasedOrigYcNameList)
    hieSortedOrigYcNameList = ycHieSorter.getSortedOriginalYieldCurveNames()
    for origYcName in hieSortedOrigYcNameList:
        origAcmYc = acm.FYieldCurve[origYcName]
        origYcOid = origAcmYc.Oid()
        world.logInfo('    Selected \'{0}\' (oid={1})'.format(origYcName,
                origYcOid))
        world.summaryAddOk('YieldCurve', origYcOid, 'SELECT')
    world.logInfo('    Total {0} yield curves selected'.format(
            len(hieSortedOrigYcNameList)))
    ycToStoreList = [acm.FYieldCurve[ycName]
            for ycName in hieSortedOrigYcNameList]
    memberCurves = FBDPYieldCurveLib.findMemberCurves(ycToStoreList)

    # Build archive order
    archiveOrder = [yc.Oid() for yc in ycToStoreList
                        if yc not in memberCurves]
    memberOids = []
    if memberCurves:
        memberOids = [yc.Oid() for yc in memberCurves]

    # Build recalculation order
    recalculationOrder = [yc.Oid() for yc in ycToStoreList]
    if memberCurves:
        memberOidsToAdd = [yc.Oid() for yc in memberCurves
                        if yc not in ycToStoreList]
        recalculationOrder.extend(memberOidsToAdd)

    # Duplication Order, member curves first
    ycToStoreList = [yc for yc in ycToStoreList
                    if yc not in memberCurves]
    ycToStoreList = memberCurves + ycToStoreList

    # Duplicate original curves
    world.logInfo('    Duplicating original yield curves')
    origYcOidAndYcClonePairs = _duplicateOrigYc(world, today,
              ycToStoreList, memberCurves,
            params.yc_realtimeupdatedunchanged)

    world.logInfo('    Total {0} original yield curves duplicated.'.format(
            len(origYcOidAndYcClonePairs)))

    # Recalibrate cloned curves
    if params.calculate:
        world.logInfo('    Recalculating cloned yield curves')
        origYcOidAndYcClonePairs, recalculationOrder = \
                _recalculateYcClones(world,
                origYcOidAndYcClonePairs, recalculationOrder)
        world.logInfo('    Total {0} cloned yield curves recalculated.'.format(
                len(origYcOidAndYcClonePairs)))
    # Archive cloned curves
    world.logInfo('    Archiving cloned yield curves')

    nonMemberArchiveOrder = [ycOid for ycOid in recalculationOrder
                                if ycOid in archiveOrder]
    nonMemberArchiveOrder.reverse()
    memberArchiveOrder = [ycOid for ycOid in recalculationOrder
                                if ycOid in memberOids]
    recalculationOrder = nonMemberArchiveOrder + memberArchiveOrder

    origYcOidAndYcClonePairs = _archiveYcClones(world,
            origYcOidAndYcClonePairs, recalculationOrder)
    world.logInfo('    Total {0} cloned yield curves archived.'.format(
            len(origYcOidAndYcClonePairs)))
    # Finished
    world.logInfo('Finished storing yield curves.')
