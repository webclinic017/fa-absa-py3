""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FTradeProgram.py"
"""--------------------------------------------------------------------------
MODULE
    FTradeProgram

    (c) Copyright 2013 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    A Trade Program represents a group of trades together embodying
    one investment decision or strategy. The trade orders linked to the
    trades of the trade program either exist prior to or are created as a
    consequence of the trade program.

    This module defines Trade Program as a Deal Package with a definition
    that is part of the extension group 'trade program'.
-----------------------------------------------------------------------------"""
import acm
from FTradeToOrder import Logger
from ACMPyUtils import Transaction
from FParameterSettings import ParameterSettingsCreator

def IsTradeProgram(obj):
    try:
        return obj.IsKindOf(acm.FDealPackage) and obj.Definition() in _ValidDealPackageDefinitions()
    except AttributeError:
        return False

def Create(definition, trades):
    dealPackage = acm.DealPackage.New(definition)
    _SuggestName(dealPackage)
    for trade in trades:
        trade.OpeningDealPackage = dealPackage
    return dealPackage

def Save(dealPackage, trades=None):
    with Transaction():
        dealPackage.Save()
        for trade in trades or []:
            trade.Commit()

def Delete(dealPackage):
    try:
        oid = dealPackage.Oid()
        with Transaction():
            for t in LinkedTrades(dealPackage):
                t.Delete()
            dealPackage.Delete(deleteChildDealPackages=True,
                                   deleteAllTrades=True)
        Logger().debug('Deleted deal package {0}.'.format(oid))
    except Exception as e:
        Logger().error('Failed to delete deal package {0}.'.format(oid))
        Logger().debug(e, exc_info=True)
        raise e
        
def LinkedTrades(dealPackage):
    return acm.FTrade.Select('openingDealPackage = {0}'.format(dealPackage.Oid())).AsArray()

def TradeProgramWorkflowClass():
    settings = ParameterSettingsCreator.FromRootParameter('TABSettings')
    moduleName, className = settings.WorkflowClass().split('.')
    module = __import__(moduleName)
    return getattr(module, className)

"""
    Helper functions
"""

def _ValidDealPackageDefinitions():
    context = acm.GetDefaultContext()
    return context.GetAllExtensions(
            'FDealPackageDefinition',
            'FObject',
            False,
            True,
            'trade program')

def _SuggestName(dealPackage):
    if not dealPackage.OptionalId():
        dealPackage.SuggestName()
        dealPackage.OptionalId(dealPackage.InstrumentPackage().Name())