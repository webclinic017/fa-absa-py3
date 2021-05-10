""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/upgrade/FSwiftUpgradeScript.py"
import acm

import FOperationsUtils as Utils

import FSwiftUpgradeSteps as UpgradeSteps
import FSwiftUpgradeUtilities as UpgradeUtils
import FSwiftParameters as FSwiftParameters


ael_gui_parameters = {'windowCaption' : 'Upgrade script for the new SWIFT solution'}

ael_variables = [
    ['customMessageTypes', 'Custom Message Types', 'string', None, '', 0, 0, "Enter custom message types seperated by comma. Don't use single or double quotes"],
    ['customMessageTemplates', 'Template Names', 'string', None, '', 0, 0, "Enter template names for custom messages seperated by comma. Don't use single or double quotes"],
    ['fileNames', 'File Names', 'string', None, '', 0, 0, "Enter file names for custom messages seperated by comma. Don't use single or double quotes"]]

def ael_main(dictionary):
    try:
        customMessageTypes, customMessageTemplates, fileNames = UpgradeSteps.GetUserInput(dictionary)
        formator = UpgradeUtils.InputFormator(customMessageTypes, customMessageTemplates, fileNames)
        customMessageTypes, customMessageTemplates, fileNames = formator.GetFormattedInput()
        validator = UpgradeUtils.InputValidator(customMessageTypes, customMessageTemplates, fileNames)
        validator.ValidateInput()
        Utils.LogAlways('Valid User Input')
        confirmationOverrides, settlementOverrides = UpgradeSteps.GetOverridesFromHooksAndDropFields(FSwiftParameters.hooks, FSwiftParameters.DROP_FIELDS)
        settlementParamsUpdateAction = UpgradeUtils.SettlementParametersUpdateAction()
        confirmationParamsUpdateAction = UpgradeUtils.ConfirmationParametersUpdateAction()
        swiftParamsUpdateAction = UpgradeUtils.SwiftParametersUpdateAction()

        moduleActionList = [
            (UpgradeUtils.ModuleNames.SETTLE_PARAMS,    settlementParamsUpdateAction, None),
            (UpgradeUtils.ModuleNames.CONF_PARAMS,      confirmationParamsUpdateAction, None),
            (UpgradeUtils.ModuleNames.SWIFT_PARAMS,     swiftParamsUpdateAction, None),
            (UpgradeUtils.ModuleNames.CONF_XML_HOOKS,   UpgradeUtils.UpdateActions.UPDATE_CONFIRMATION_HOOKS, [confirmationOverrides, customMessageTypes, customMessageTemplates, fileNames]),
            (UpgradeUtils.ModuleNames.SETTLE_XML_HOOKS, UpgradeUtils.UpdateActions.UPDATE_SETTLEMENT_HOOKS, [settlementOverrides])
        ]

        Utils.LogAlways('\nUpgrade to the new SWIFT solution has started.')
        updatedModules = UpgradeUtils.UpdateModules(moduleActionList)

        try:
            acm.BeginTransaction()
            for updatedModule in updatedModules:
                updatedModule.Commit()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            Utils.LogAlways('\nUpgrade failed due to :')
            Utils.LogAlways(e)
            Utils.LogAlways('\nPlease re-run the upgrade script with details of all custom messages in the specified format (if any).')
        else:
            if any(customMessageTypes):
                Utils.LogAlways('Following custom messages have been upgraded to the new SWIFT solution:')
                for aCustomMessage in customMessageTypes:
                    Utils.LogAlways(aCustomMessage)
            Utils.LogAlways('Your environment has been successfully upgraded to the new SWIFT solution.')

    except Exception as e:
        Utils.LogAlways('\nUpgrade failed due to :')
        Utils.LogAlways(e)
        Utils.LogAlways('\nPlease re-run the upgrade script with details of all custom messages in the specified format (if any).')

