""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fixing/FPortfolioSwapPerform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from FPortfolioSwapProcessing import Param
from FPortfolioSwapProcessingPerform import Action, perform

def Fix(dictionary):
    dictionary['actions'] = [Action.FIX]
    perform(dictionary)

def Extend(dictionary):
    dictionary['actions'] = [Action.EXTEND]
    if dictionary.get('SweepCash'):
        dictionary['actions'].append(Action.SWEEP)

    perform(dictionary)

def Regenerate(dictionary):
    dictionary['actions'] = [Action.REGENERATE]
    dictionary[Param.REGENERATE_STARTDATE] = dictionary['StartDate']
    dictionary[Param.REGENERATE_ENDDATE] = dictionary['EndDate']
    dictionary['Date'] = dictionary['EndDate']
    dictionary['to_remove'] = [
        Param.REGENERATE_STARTDATE, Param.REGENERATE_ENDDATE, 'Date'
    ]
    perform(dictionary)
