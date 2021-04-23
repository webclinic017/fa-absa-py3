""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/DealPackage/delete/FDeletePackagesHelper.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import ael

import FPackagesProcessingHelper as helper
import importlib
importlib.reload(helper)
import FPackagesProcessingUtility as util
importlib.reload(util)
import FArchivePackagesHelper as archive_helper
importlib.reload(archive_helper)

def _delete(performer):
    """
    Attempts to delete entity, but some entities are currently required
    first be de-archived before deletion
    """
    if not isinstance(performer, helper._AelObjectPerformer):
        raise Exception('Invalid delete performer type')

    try:
        util.delete(
            obj=performer.getObject(), testmode=performer.isInTestMode()
        )
    except Exception as e:
        raise Exception('Failed to delete %s: %s' % (performer._name, str(e)))

    return

def get_deleter(
    owner, indentation, objs, objs_are_archived, perform_func=None
):
    """
    Returns the deleter performer (object wrapper on which to call perform)
    """
    if not len(objs):
        return None

    def check_success(obj_type, oid):
        if obj_type != util.Type.pkg_wrapper:
            try:
                obj = util.makeAelObject(obj_type, oid)
                if obj:
                    ael.poll()
                    obj = util.makeAelObject(obj_type, oid)

                if obj:
                    name = util.getAelName(obj)
                    raise Exception('%s still exits' % name)
            except Exception as e:
                if 'entity is deleted' not in str(e):
                    raise e

        return

    helper.assertCompatibleWithPerformer(objs)
    action = helper._WorldProxy.ARCHIVE_DELETE_ACTION if objs_are_archived \
        else helper._WorldProxy.LIVE_DELETE_ACTION
    obj_type = util.getType(objs[0])
    if obj_type == util.Type.trade:
        params = owner.other_params['gui_params']
        return helper.make_FNewExpirationPerform_performer(
            owner, params, objs, _AelTradesDeleter,
            check_success, action
        )
    elif obj_type == util.Type.ins:
        params = owner.other_params['gui_params']
        return helper.make_FNewExpirationPerform_performer(
            owner, params, objs, _AelInstrumentsDeleter,
            check_success, action
        )

    perform_func = perform_func or _delete
    return helper.make_generic_performer(
        owner, objs, util.INDENTATION if indentation == None else indentation,
        _AelGenericDeleter, check_success, perform_func
    )

# Performer classes (used only to help with debugging)
class _AelGenericDeleter(helper._AelSameObjectsPerformer):
    pass

class _AelTradesDeleter(helper._AelTradesPerformer):
    pass

class _AelInstrumentsDeleter(helper._AelInstrumentsPerformer):
    pass
