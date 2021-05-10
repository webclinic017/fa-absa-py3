""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/upgrade/FSwiftUpgradeSteps.py"

import FSwiftUpgradeMTMessageToXmlMapUtilities as XmlUtils
import FSwiftUpgradeHooksAndDropFieldsUtilities as HookUtils


def GetUserInput(dictionary):
    customMessageTypes = dictionary.get('customMessageTypes').split(',')
    customMessageTemplates = dictionary.get('customMessageTemplates').split(',')
    fileNames = dictionary.get('fileNames').split(',')
    return customMessageTypes, customMessageTemplates, fileNames

def UpdateFSwiftParameters(moduleText, *args):
    optionsText = XmlUtils.GetOptionsTextToBeAddedInSwiftParam(moduleText)
    updatedText = XmlUtils.AddOptionsTextToSwiftParam(moduleText, optionsText)
    return updatedText

def UpdateFConfirmationParameters(moduleText, *args):
    mtMessagetoXmlMapText = XmlUtils.GenerateMtMessageToXMLMapText()
    importStatementForTemplates = XmlUtils.GetImportStatementForConfirmationTemplates()
    updatedText = XmlUtils.AddVariableTextToModuleText(moduleText, mtMessagetoXmlMapText)
    updatedText = XmlUtils.AddImportStatement(updatedText, importStatementForTemplates)
    return updatedText

def UpdateFSettlementParameters(moduleText, *args):
    importStatement = XmlUtils.GetImportStatementForSettlementTemplates()
    updatedText = XmlUtils.AddImportStatement(moduleText, importStatement)
    defaultTuple = XmlUtils.GetMTMessageToXMLMapDefaultTupleForSettlement()
    updatedText = XmlUtils.AddMTMessageToXMLMapDefaultTupleForSettlement(updatedText, defaultTuple)
    return updatedText

def UpdateSettlementSwiftHooks(moduleText, *args):
    argsList = args[0]
    textList = argsList[0]
    updatedText = ""
    for textRow in textList:
        updatedText += textRow
    return str(updatedText)

def UpdateConfirmationSwiftHooks(moduleText, *args):
    updatedText = ""
    argsList = args[0]
    confirmationOverrides = argsList[0]
    customMessageTypes = argsList[1]
    customMessageTemplates = argsList[2]
    fileNames = argsList[3]
    textList = UpgradeCustomMessages(customMessageTypes, customMessageTemplates, fileNames, confirmationOverrides)
    for textRow in textList:
        updatedText += textRow

    return str(updatedText)

def GetOverridesFromHooksAndDropFields(hooks, dropfieldsDict):
    confirmationOverrides = []
    settlementOverrides = []
    hooksDict = HookUtils.GetDictFromHooks(hooks)
    allMessageTypes = HookUtils.GetAllMessageTypesToProcess(hooksDict, dropfieldsDict)
    for aMessageType in allMessageTypes:
        templateXml = HookUtils.GetOverrideTemplateForMessageType(aMessageType, hooksDict, dropfieldsDict)
        HookUtils.AddTemplateToOverrideVariable(templateXml, aMessageType, confirmationOverrides, settlementOverrides)
    return (confirmationOverrides, settlementOverrides)

def UpgradeCustomMessages(customMessageTypes, customMessageTemplates, fileNames, confirmationOverrides):
    updatedText = confirmationOverrides
    if customMessageTypes:
        updatedText = XmlUtils.ModifyFConfirmationSwiftXmlHooks(updatedText, customMessageTypes, customMessageTemplates, fileNames)
    return updatedText
