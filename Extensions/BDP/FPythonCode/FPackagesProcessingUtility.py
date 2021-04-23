""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/etc/FPackagesProcessingUtility.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import collections

import ael

import FBDPCommon
import FNewExpirationUtility
import importlib
importlib.reload(FNewExpirationUtility)
from FBDPCurrentContext import Logme, Summary

INDENTATION = '  '

PackageWrapper = collections.namedtuple(
    'PackageWrapper',
    'root ins_pkgs deal_pkgs trades instrs ' \
    + 'ins_pkg_links deal_pkg_links trade_links ins_links'
)
Packages = collections.namedtuple('Packages', 'ins_pkgs deal_pkgs')
ExaminedObject = collections.namedtuple(
    'ExaminedObject', 'expired added can_add in_progress'
)

# Deal/instrument package related attributes names should match PackageWrapper
class Type:
    ins_pkg = 'InstrumentPackage'
    deal_pkg = 'DealPackage'
    trade = 'Trade'
    ins = 'Instrument'
    ins_pkg_link = 'InstrumentPackageLink'
    deal_pkg_link = 'DealPackageLink'
    trade_link = 'DealPackageTrdLink'
    ins_link = 'DealPackageInsLink'
    pkg_wrapper = 'PackageWrapper'

__ALLOWED_TYPES = [
    v for k, v in Type.__dict__.items() if not k.startswith('_')
]

class Log:
    @staticmethod
    def log(msg, log_target, indent=False):
        if msg:
            indentation = INDENTATION if indent else ''
            Logme()('%s%s' % (indentation, msg), log_target)
        else:
            Logme()(None, log_target)

    @staticmethod
    def logProcessing(obj, source_obj, indent):
        ael_obj = source_obj or obj
        name = getAelName(ael_obj)
        msg = None
        if source_obj:
            msg = 'Processing %s from %s' % (obj, name)
        else:
            msg = 'Processing %s' % name

        Log.log(msg, 'INFO', indent)
        if ael_obj.seqnbr <= 0:
            raise Exception('Attempted to process invalid object: %s' % name)

    @staticmethod
    def logFinishedProcessing(obj, source_obj, indent):
        ael_obj = source_obj or obj
        name = getAelName(ael_obj)
        msg = None
        if source_obj:
            msg = 'Finished processing %s from %s' % (obj, name)
        else:
            msg = 'Finished processing %s' % name

        Log.log(msg, 'INFO', indent)

    @staticmethod
    def logProcessed(obj):
        if not isinstance(obj, list):
            Summary().ok(obj, Summary().PROCESS)
        elif len(obj):
            Summary().ok(obj[0], Summary().PROCESS, None, len(obj))

    @staticmethod
    def logUnexpired(obj):
        Log.logIgnore(obj, 'underlying instrument(s) yet to expire', True)

    @staticmethod
    def logIgnore(obj, reason, indent):
        if reason:
            reason = 'As ' + reason

        if obj:
            Summary().ignore(obj, Summary().PROCESS, reason, getOid(obj))

        if reason:
            Log.log(reason + ', skipping', 'DEBUG', indent)

    @staticmethod
    def logWarning(obj, msg, indent):
        if obj:
            oid = getOid(obj)
            msg = '%s%s' % (msg[0].lower(), msg[1:])
            Summary().warning(obj, Summary().PROCESS, oid, msg)

        Log.log('%s, skipping' % msg, 'WARNING', indent)

    @staticmethod
    def logError(obj, reason, indent, action):
        assert xnor(obj, action), 'Specify both object and action or neither'
        if obj:
            oid = getOid(obj)
            if reason:
                reason = '%s%s' % (reason[0].lower(), reason[1:])

            if not action.endswith('d'):
                action = action + 'd'

            Summary().fail(obj, action, oid, reason)

        if reason:
            Log.log(reason, 'ERROR', indent)

    @staticmethod
    def logActionStarted(task, name, indentation):
        msg = '%s %s' % (task.capitalize(), name)
        Log.log('%s%s' % (indentation, msg), 'DEBUG', False)

    @staticmethod
    def logActionFinished(task, name, indentation):
        msg = 'Finished %s %s' % (task.lower(), name)
        Log.log('%s%s' % (indentation, msg), 'DEBUG', False)

    @staticmethod
    def logOk(obj, action, name, count=1):
        assert count in (-1, 1), 'count must be -1 or 1'
        assert obj, 'Non-none object required to log action success'
        if not action.endswith('d'):
            action = action + 'd'

        Summary().ok(obj, action, name, count)


def archive(obj, target_archive_status, testmode, rollback):
    obj = obj.clone()
    obj.archive_status = target_archive_status
    if not testmode:
        if rollback:
            rollback.add(obj, ['archive_status'])
        else:
            obj.commit()

    return

def delete(obj, testmode):
    if not testmode:
        if 'Link' in obj.record_type:
            if obj.archive_status == 1:
                archive(obj, 0, testmode, None)

            obj = FBDPCommon.ael_to_acm(obj)
            obj.Delete()
        else:
            obj.delete()

    return

def getMakeAelObjectParams(obj):
    obj = getAelObject(obj)
    return getType(obj, False), getOid(obj)

def getMakeAelObjectParamsFromList(objs):
    return [getMakeAelObjectParams(obj) for obj in objs]

def makeAelObject(obj_type, oid):
    if obj_type not in __ALLOWED_TYPES:
        msg = 'Can only recreate objects corresponding to types: %s' % (
            __ALLOWED_TYPES
        )
        raise Exception(msg)

    obj = None
    try:
        obj = getattr(ael, obj_type)[oid]
    except Exception as e:
        if 'entity is deleted' not in str(e):
            raise

    return obj

def makeAelObjectFromListOfParams(list_of_params):
    return [makeAelObject(obj_type, oid) for obj_type, oid in list_of_params]

def getAelObject(obj):
    if not hasattr(obj, 'record_type'):
        if isinstance(obj, PackageWrapper):
            obj = obj.root
        else:
            obj = FBDPCommon.acm_to_ael(obj)

    assert obj != None, 'Object is None'
    return obj

def getType(obj, allow_wrapper_type=True):
    # useful where the object could be an ael entity or a package wrapper
    ref_type = getattr(obj, 'record_type', None)
    if ref_type:
        allowed = __ALLOWED_TYPES
        if (ref_type in allowed) and not isinstance(obj, PackageWrapper):
            return ref_type
    else:
        if allow_wrapper_type and isinstance(obj, PackageWrapper):
            return Type.pkg_wrapper

        return getType(getAelObject(obj), allow_wrapper_type)

    raise Exception('Unhandled object specified: %s' % type(obj))

def isKnownType(obj, allow_wrapper_type):
    try:
        getType(obj, allow_wrapper_type)
    except:
        return False

    return True

def areAllKnownTypes(objs, allow_wrapper_type):
    return all(isKnownType(obj, allow_wrapper_type) for obj in objs)

def isType(obj, ref_type):
    return getType(obj) == ref_type

def getOid(obj):
    obj = getAelObject(obj)
    return int(FBDPCommon.getPrimaryKey(obj))

def getAelName(obj):
    obj = getAelObject(obj)
    oid = getOid(obj)
    name = '%s[%i]' % (obj.record_type, oid)
    display_id = str(obj.display_id())
    if (len(display_id) == 0) or (display_id == str(oid)):
        return name

    return name + ' ' + repr(display_id)

def getPackageWrapperAttribute(obj, pkg_wrapper):
    if not isinstance(pkg_wrapper, PackageWrapper):
        msg = 'Invalid package wrapper specified: %s (%s)' % (
            type(pkg_wrapper), getAelName(pkg_wrapper)
        )
        raise Exception(msg)

    if not isKnownType(obj=obj, allow_wrapper_type=False):
        msg = 'Unknown object specified: %s (%s)' % (
            type(obj), obj.display_id()
        )
        raise Exception(msg)

    obj_type = getType(obj, False)
    attr_name = None
    if obj_type == Type.ins_pkg:
        attr_name = 'ins_pkgs'
    elif obj_type == Type.deal_pkg:
        attr_name = 'deal_pkgs'
    elif obj_type == Type.trade:
        attr_name = 'trades'
    elif obj_type == Type.ins:
        attr_name = 'instrs'
    elif obj_type == Type.ins_pkg_link:
        attr_name = 'ins_pkg_links'
    elif obj_type == Type.deal_pkg_link:
        attr_name = 'deal_pkg_links'
    elif obj_type == Type.trade_link:
        attr_name = 'trade_links'
    elif obj_type == Type.ins_link:
        attr_name = 'ins_links'

    return getattr(pkg_wrapper, attr_name)

def returnOrNone(func):
    try:
        return func()
    except:
        pass

    return None

def applyToPackageWrapper(pkg_wrapper, func, apply_to_root):
    if apply_to_root:
        func(pkg_wrapper.root)

    func(pkg_wrapper.trade_links)
    func(pkg_wrapper.trades)
    func(pkg_wrapper.ins_links)
    func(pkg_wrapper.instrs)
    func(pkg_wrapper.deal_pkg_links)
    func(pkg_wrapper.deal_pkgs)
    func(pkg_wrapper.ins_pkg_links)
    func(pkg_wrapper.ins_pkgs)

def xnor(a, b):
    # returns true when a and b are both true or both false
    return (a and b) or not (a or b)

def prepareFNewExpiration(pkgs):
    # update a global FNewExpiration dictionary to prevent
    # unnessary logging and exception throwing for cases
    # handled by local code but not FNewExpiration code
    dct = {}

    def update(objs):
        for obj in makeAelObjectFromListOfParams(objs):
            dct.setdefault(obj.record_type, []).append(getOid(obj))

    for pkg in pkgs:
        applyToPackageWrapper(pkg, update, False)

    FNewExpirationUtility.OBJECTS_ALLOWING_REF_CHECK_SUPPRESSION.update(dct)

def undoPrepareFNewExpiration():
    FNewExpirationUtility.OBJECTS_ALLOWING_REF_CHECK_SUPPRESSION.clear()
