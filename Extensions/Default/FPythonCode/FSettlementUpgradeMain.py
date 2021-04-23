""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeMain.py"
from FOperationsExceptions import WrapperException

class FSettlementUpgradeParametersException(WrapperException):
    def __init__(self, message, innerException = None):
        WrapperException.__init__(self, message, innerException)


def upgrade_start (archive):
    UpgradeVariables.SettlementUpgradeAllVariables()
    TradeQueries.CreateTradeFilterQueriesParameter()
    CreateQueries.CreatePreventSettlementCreationQueriesParameter()
    DelQueries.CreatePreventSettlementDeletionQueriesParameter()
    Hooks.CreateHooks()
    Utils.Log(True,  "Upgrade of Parameters, Hooks and Queries completed.")
    if archive:
        oldModuleNames = ['FSettlementAdHocNetManual',
                          'FSettlementAggregation',
                          'FSettlementAMB',
                          'FSettlementAMBAHook',
                          'FSettlementAMBAHookTemp',
                          'FSettlementEntityClasses',
                          'FSettlementEOD',
                          'FSettlementCheckBic',
                          'FSettlementClientNetting',
                          'FSettlementClientNettingTemp',
                          'FSettlementClientSTP',
                          'FSettlementClientSTPTemplate',
                          'FSettlementCutOff',
                          'FSettlementGeneral',
                          'FSettlementGeneral2',
                          'FSettlementGeneral3',
                          'FSettlementGeneralRT',
                          'FSettlementNetting',
                          'FSettlementParams',
                          'FSettlementSOD',
                          'FSettlementSTP',
                          'FSettlementSwiftXMLFieldsTemplate',
                          'FSettlementSwiftXMLSpecifier',
                          'FSettlementVariables',
                          'FSettlementVariablesTemplate',
                          'FUpdateTradeAccountLinks',
                          'FUpdateFutureForward',
                          'FUpdateEffectiveFromDate',
                          'FSettlement72'
                          ]
        mr = ModuleRenamer(oldModuleNames)
        mr.RenameOldModules()

        er = ExtensionRelocator(oldModuleNames, 'UpgradeContext')
        er.MoveOldExtensions()
    try:
        DuplicatesFinder.CreateMenuInSettlementSheet()
        Utils.Log(True, 'Menu Manage Duplicate Folders added to Settlement Sheet.')
    except DuplicatesFinder.MenuException as exception:
        Utils.Log(True, 'Failed to add Manage Duplicate Folders menu to Settlement Sheet.')
        Utils.Log(True, str(exception))

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    import acm
    import time
    import FOperationsUtils as Utils

    import FSettlementUpgradeHooks as Hooks
    import FSettlementUpgradeDelQueries as DelQueries
    import FSettlementUpgradeCreateQueries as CreateQueries
    import FSettlementUpgradeTradeQueries as TradeQueries
    import FSettlementUpgradeVariables as UpgradeVariables
    from FSettlementUpgradeRenameModule import ModuleRenamer, ExtensionRelocator
    import FSettlementUpgradeDuplicatesFinder as DuplicatesFinder

    try:
        import FSettlementUpgradeParameters as UpgradeParams
        if UpgradeParams.upgradeDate == 'YYYY-MM-DD':
            raise FSettlementUpgradeParametersException("Variable upgradeDate in FSettlementUpgradeParameters has not been set.")
    except ImportError:
        raise FSettlementUpgradeParametersException("The FSettlementUpgradeParameters Python module does not exist. \nCreate it based it on FSettlementUpgradeParametersTemplate.")

    ael_variables = [('archive', 'Archive old scripts', 'bool', [False, True], True)]

    def ael_main(dict):
        pr = '<< Settlement Upgrade - %s >>' % (__file__)
        Utils.Log(True, pr)
        upgrade_start(dict["archive"])

except Exception as e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    Utils.Log(True, 'Could not run FSettlementUpgradeMain due to ')
    Utils.Log(True, str(e))
