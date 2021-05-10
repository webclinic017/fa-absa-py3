""" Compiled: 2020-01-21 09:44:09 """

#__src_file__ = "extensions/expiration/etc/FNewExpirationObjRefHandler.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2021 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import ael


import FBDPCommon
import string

supportedBusinessEvtType = ['Exercise/Assign', 'Allocation']

def validateType(type, expectedType, funcName, log):
    if type != expectedType:
        log.logError('Wrong type %s for handler %s, Expect type %s'
            % (type, funcName, expectedType))
        return False

    return True


def IgnoreTrdReference(aelObj, refObj, resultlist, log):
    if not validateType(refObj.record_type, 'Trade',
        'IgnoreTrdReference', log):
        return False

    return True

def ErrorOnTrdReference(aelObj, refObj, resultlist, log):

    if not validateType(refObj.record_type, 'Trade',
        'ErrorOnTrdReference', log):
        return False

    aelObjPrimaryKey = FBDPCommon.getPrimaryKey(aelObj)
    log.logError(
        'Unexpected Trade reference %s to object %s id = %s'
        % (refObj.trdnbr, aelObj.record_type, aelObjPrimaryKey)
    )
    return False


def HandleTrdReferenceOnArchive(aelObj, refObj, resultlist, log):

    if not validateType(refObj.record_type, 'Trade',
        'HandleTrdReferenceOnArchive', log):
        return False

    if refObj.archive_status == 1:
        return True

    elif refObj.mirror_trdnbr and \
         refObj.mirror_trdnbr.trdnbr == aelObj.trdnbr:
        return True
    elif refObj.correction_trdnbr and \
         refObj.correction_trdnbr.trdnbr == aelObj.trdnbr:
        return True
    elif refObj.connected_trdnbr and \
        refObj.connected_trdnbr.trdnbr == aelObj.trdnbr:
        return True
    else:
        aelObjPrimaryKey = FBDPCommon.getPrimaryKey(aelObj)
        log.logError(
            'Unexpected trade reference %s to object %s with id %s'
            % (refObj.trdnbr, aelObj.record_type, aelObjPrimaryKey)
        )
        return False


def ArcDeArcExAssignBusiEvt(aelObj, refObj, resultlist, log):

    if not validateType(refObj.record_type, 'BusinessEventTrdLink',
        'ArchiveExAssignBusiEvt', log):
        return False

    refId = FBDPCommon.getPrimaryKey(refObj)
    aelObjId = FBDPCommon.getPrimaryKey(aelObj)

    evt = refObj.parent()
    if not evt:
        log.logWarning(
            'Ignore the business evt trade link id = %s (with no '
            'business event) that reference to the %s with Id %s'
            % (refId, aelObj.record_type, aelObjId)
        )
        return True

    if evt.event_type not in supportedBusinessEvtType:
        log.logWarning(
            'Ignore the business evt trade link id = %s (with '
            'business event type = %s) that reference to the %s with Id %s'
            % (refId, evt.event_type, aelObj.record_type, aelObjId)
        )
        return True

    resultlist.append(refObj)
    if evt not in resultlist:
        resultlist.append(evt)

    return True

def DeleteExAssignBusiEvt(aelObj, refObj, resultlist, log):

    if not validateType(refObj.record_type, 'BusinessEventTrdLink',
        'DeleteExAssignBusiEvt', log):
        return False

    refId = FBDPCommon.getPrimaryKey(refObj)
    aelObjId = FBDPCommon.getPrimaryKey(aelObj)

    evt = refObj.parent()
    if not evt:
        log.logError(
            'Unexpected business evt trade link id = %s (with no '
            'business event) that reference to the %s with Id %s'
            % (refId, aelObj.record_type, aelObjId)
        )
        return False

    if evt.event_type not in supportedBusinessEvtType:
        log.logError(
            'Unexpect business trade link with '
            'business event that has type %s' % (evt.event_type)
        )
        return False

    evtReflist = evt.reference_in(1)
    if evtReflist:
        evtId = FBDPCommon.getPrimaryKey(evt)
        log.logError(
            'Exercise Assign business event %s that reference to '
            'object id = %s has some unhandled external references %s' % (
                evtId, aelObjId, evtReflist
            )
        )
        return False

    evtTrdLinkReflist = refObj.reference_in(1)
    if evtTrdLinkReflist:
        log.logError(
            'Exercise Assign business event trade link %s that reference to '
            'object id = %s has some unhandled external references %s' % (
                refId, aelObjId, evtReflist
            )
        )
        return False

    if evt not in resultlist:
        resultlist.append(evt)

    return True
