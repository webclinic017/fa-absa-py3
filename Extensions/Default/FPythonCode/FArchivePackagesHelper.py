""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/archive/FArchivePackagesHelper.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import ael

import FPackagesProcessingHelper as helper
import importlib
importlib.reload(helper)
import FPackagesProcessingUtility as util
importlib.reload(util)

def _archive(performer, target_archive_status):
    """
    Expects the archive status of object to be different from target
    any logic filtering out this object should be done prior to this call
    """
    if not isinstance(performer, helper._AelObjectPerformer):
        raise Exception('Invalid archive performer type')

    archive_status = int(performer.getObject().archive_status)
    archive_status_to_change_from = int(not bool(target_archive_status))
    if archive_status == archive_status_to_change_from:
        util.archive(
            obj=performer.getObject(),
            target_archive_status=target_archive_status,
            testmode=performer.isInTestMode(),
            rollback=performer.getRollback()
        )
    elif archive_status != target_archive_status:
        raise Exception(
            'Unable to handle %s archive status = %s' % (
                performer._name, archive_status
            )
        )

    return

def get_archiver(owner, indentation, objs, archive, perform_func=None):
    """
    Returns the archive performer (object wrapper on which to call perform)
    """
    if not len(objs):
        return None

    def check_success(obj_type, oid):
        if obj_type == util.Type.pkg_wrapper:
            return

        success = False
        obj = util.makeAelObject(obj_type, oid)
        if obj and (obj.archive_status == int(archive)):
            success = util.getOid(obj) > 0

        if not success:
            ael.poll()
            obj = util.makeAelObject(obj_type, oid)
            if obj and (obj.archive_status == int(archive)):
                success = util.getOid(obj) > 0

        if not success:
            msg = None
            if obj:
                msg = '%s still has archive status = %i' % (
                    util.getAelName(obj), obj.archive_status
                )
            else:
                msg = 'ael.%s[%s] not found' % (obj_type, oid)

            raise Exception(msg)

        return

    helper.assertCompatibleWithPerformer(objs)
    obj_type = util.getType(objs[0])
    action = helper._WorldProxy.ARCHIVE_ACTION if archive \
        else helper._WorldProxy.DEARCHIVE_ACTION
    if obj_type == util.Type.trade:
        params = owner.other_params['gui_params']
        return helper.make_FNewExpirationPerform_performer(
            owner, params, objs, _AelTradesArchiver,
            check_success, action
        )
    elif obj_type == util.Type.ins:
        params = owner.other_params['gui_params']
        return helper.make_FNewExpirationPerform_performer(
            owner, params, objs, _AelInstrumentsArchiver,
            check_success, action
        )

    if not perform_func:
        perform_func = lambda performer: _archive(performer, int(archive))

    return helper.make_generic_performer(
        owner, objs, util.INDENTATION if indentation == None else indentation,
        _AelGenericArchiver, check_success, perform_func
    )

# Performer classes (used only to help with debugging)
class _AelGenericArchiver(helper._AelSameObjectsPerformer):
    pass

class _AelTradesArchiver(helper._AelTradesPerformer):
    pass

class _AelInstrumentsArchiver(helper._AelInstrumentsPerformer):
    pass
