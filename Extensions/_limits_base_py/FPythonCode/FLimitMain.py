""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/limits/./etc/FLimitMain.py"
"""--------------------------------------------------------------------------
MODULE
    FLimitMain

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A module for the server-side monitoring of all limits on an Arena Task
    Server. 

    To set up ATS limit monitoring:

    - Add the "Limits Base" module to the context of the ATS user.
    - Ensure the ATS user has sufficient permissions for accessing 
      all limits that may be created in the system.
    - Set the module_name parameter in the ATS to "FLimitMain".

-----------------------------------------------------------------------------"""
import acm
import ael
import FAssetManagementUtils 
import FLimitServer
import FLimitSettings


logger = FAssetManagementUtils.GetLogger()
server = FLimitServer.FLimitServer()
new_limits = set()


def start():
    FAssetManagementUtils.ReinitializeLogger(FLimitSettings.ServerLoggingLevel())
    logger.info('Starting limits monitoring task...')
    FLimitSettings.LogLimitSettings()

    ael.BusinessProcess.subscribe(_business_process_table_cb)
    ael.Limit.subscribe(_limit_table_cb)
    for limit in acm.FLimit.Select(''):
        server.AddLimit(limit)
    logger.info('Limit monitoring initialisation complete')
    
def work():
    server.ProcessLimits()

def stop():
    ael.Limit.unsubscribe(_limit_table_cb)
    ael.BusinessProcess.unsubscribe(_business_process_table_cb)
    logger.info('Limits monitoring task terminated.')

def status():
    return 'Hi mum!'


def _limit_table_cb(_object, ael_entity, _arg, event):
    # The limit must have a business process in the active state for it
    # to be ready for monitoring. Mark the new limit here and process it
    # further in the business process table callback.
    if event == 'insert':
        new_limits.add(ael_entity.seqnbr)
        try:
            limit = acm.Ael().AelToFObject(ael_entity)
            limit.BusinessProcess()
        except:
            pass

def _business_process_table_cb(_object, ael_entity, _arg, event):
    if event == 'insert':
        bp = acm.FBusinessProcess[ael_entity.seqnbr]
        if bp and bp.Subject() and bp.Subject().IsKindOf(acm.FLimit):
            limit = bp.Subject()
            if limit.Oid() in new_limits and bp.CurrentStep().IsInReadyState():
                new_limits.remove(limit.Oid())
                server.AddLimit(limit)

