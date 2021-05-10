""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/structured_eq/admin/FSEQBarrierMonitorPriceHiLo.py"
"""----------------------------------------------------------------------------
MODULE
    FSEQBarrierMonitorPriceHiLo

    (c) Copyright 2006 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    The module monitors barrier options for underlying price and
    updates their "crossed status" accordingly.

----------------------------------------------------------------------------"""
import acm
import datetime

from FSEQOptionMonitorBase import OptionCollectionUpdateHandler
import FSEQBarrierMonitoring

updateInterval = 3

"""---------------------------------------------------------------
ATS interface methods.
---------------------------------------------------------------"""
def start():
    acm.Log('FSEQBarrierMonitorPriceHiLo started')
    updateHandler = OptionCollectionUpdateHandler.get_instance(FSEQBarrierMonitoring.BarrierStrategy(True))

def stop():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    if updateHandler:
        updateHandler.unsubscribe()
        updateHandler.clearInstance()
    acm.Log('FSEQBarrierMonitorPriceHiLo stopped')

def status():
    pass

def work():
    updateHandler = OptionCollectionUpdateHandler.get_instance()
    optionStrategy = updateHandler.optionStrategy

    datetimeNow = datetime.datetime.now()
    timeDiff = datetimeNow - optionStrategy.lastUpdateDateTime

    if timeDiff.seconds > updateInterval:
        optionStrategy.lastUpdateTime = datetime.datetime.now()
        updateHandler.processUpdates()
        updateHandler.optionUpdateHandler.checkAllOptions()
