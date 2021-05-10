""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/SalesTrading/./etc/FTrade2SalesActivityScript.py"
"""--------------------------------------------------------------------------
MODULE
    FTrade2SalesActivityScript

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    
-----------------------------------------------------------------------------"""

from FTrade2SalesActivity import Trade2SalesActivity

logLevelsDict = {'1. Normal': 1,
             '2. Warnings/Errors': 3,
             '3. Debug': 2}

logLevels = sorted(logLevelsDict)

ael_variables = [
    ['pageRoot', 'Page Group Root_General', 'FPageGroup', Trade2SalesActivity.GetPageGroups(), Trade2SalesActivity.GetPageGroupRoot(), 2, 0],
    ['forceUpdate', 'Force Update_General', 'bool', [True, False], False, 2, 0],
    ['date', 'Date_General', 'string', None, None, 0, 0], # acm.Time.DateValueDay()
    ['logLevel', 'Logging level_Logging', 'string', logLevels, logLevels[0], 2, 0]
]

def ael_main(params):
    pageGroup = params['pageRoot']
    lvl = logLevelsDict[params['logLevel']]
    trade2SalesActivity = Trade2SalesActivity(pageGroup, params['forceUpdate'], lvl, params['date'])
    trade2SalesActivity.UpdateTrade2SalesActities()