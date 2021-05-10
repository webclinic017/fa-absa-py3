""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/structured_eq/admin/FSEQBarrierMonitorPrice.py"
"""----------------------------------------------------------------------------
MODULE
    FSEQBarrierMonitorPrice

    (c) Copyright 2006 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    The module monitors barrier options for underlying price and
    updates their "crossed status" accordingly.

----------------------------------------------------------------------------"""
import acm

from FSEQOptionMonitorBase import OptionCollectionUpdateHandler
import FSEQBarrierMonitoring

"""---------------------------------------------------------------
ATS interface methods.
---------------------------------------------------------------"""
def start():
    acm.Log('FSEQBarrierMonitorPrice started')
    updateHandler = OptionCollectionUpdateHandler.get_instance(FSEQBarrierMonitoring.BarrierStrategy(False))

def stop():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    if updateHandler:
        updateHandler.unsubscribe()
        updateHandler.clearInstance()
    acm.Log('FSEQBarrierMonitorPrice stopped')

def status():
    pass

def work():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    updateHandler.processUpdates()
