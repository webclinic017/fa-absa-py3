""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/settlement/etc/upgrade/FSettlementUpgradeVariables.py"
import acm
import FSettlementUpgradeModuleAdmin as ModuleAdministrator
import FSettlementUpgradeVarHandler as VariableHandler

from FSettlementUpgradeModuleAdmin import ModuleIndex

def ConvertIntToBoolean(boolVar):
    if boolVar == 0:
        return False
    return True

def SettlementUpgradeAllVariables():
    moduleAdmin = ModuleAdministrator.GetModuleAdministrator()
    moduleAdmin.AddFreeTextString(ModuleIndex.PARAMETER, 'from FOperationsHook import CustomHook')

    variableHandler = VariableHandler.VariableHandler()
    ambAddress = '\'' + variableHandler.GetVariables()['amb_login'] + '\''
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'ambAddress', ambAddress)


    receiverMBName = '\'' + variableHandler.GetVariables()['RECEIVER_MB_NAME'] + '\''
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'receiverMBName', receiverMBName)


    receiverSource = '\'' + variableHandler.GetVariables()['RECEIVER_SOURCE']  + '\''
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'receiverSource', receiverSource)

    alternativeCouponHandling = ConvertIntToBoolean(variableHandler.GetVariables()['alternative_coupon_handling'])
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'alternativeCouponHandling', alternativeCouponHandling)


    considerResetsForTRSDividends = ConvertIntToBoolean(variableHandler.GetVariables()['consider_resets_for_eq_swap_dividends'])
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'considerResetsForTRSDividends', considerResetsForTRSDividends)

    detailedLogging = True
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'detailedLogging', detailedLogging)


    forwardEarlyTermination = ConvertIntToBoolean(variableHandler.GetVariables()['forward_early_termination'])
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'forwardEarlyTermination', forwardEarlyTermination)

    updateVoidedSettlement = ConvertIntToBoolean(variableHandler.GetVariables()['update_void'])
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'updateVoidedSettlement', updateVoidedSettlement)

    maxDaysForwad = 10
    for key in sorted(variableHandler.GetVariable('days_curr')):
        if maxDaysForwad < (variableHandler.GetVariable('days_curr'))[key]:
            maxDaysForwad = (variableHandler.GetVariable('days_curr'))[key]
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'maximumDaysForward', maxDaysForwad)

    maxDaysBack = variableHandler.GetVariable('days_back')
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'maximumDaysBack', maxDaysBack)


    moduleName = moduleAdmin.ModuleNameFromIndex(ModuleAdministrator.ModuleIndex.HOOKS)
    hooks = str ('[Hook(\'%s\', \'GetDaysForward\')' %(moduleName ))
    hooks = hooks + str (',Hook(\'%s\', \'GetDaysBack\')]' %(moduleName ))
    moduleAdmin.AddVariableAndValue(ModuleIndex.PARAMETER, 'hooks', hooks)
