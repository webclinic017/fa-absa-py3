""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/upgrade/FSwiftUpgradeUtilities.py"

import acm, sys, re

import FOperationsUtils as Utils
import FSwiftUpgradeSteps as UpgradeSteps


class ModuleNames:
    CONF_PARAMS                 = "FConfirmationParameters"
    SETTLE_PARAMS               = "FSettlementParameters"
    SWIFT_PARAMS                = "FSwiftParameters"
    SETTLE_XML_HOOKS            = "FSettlementSwiftXMLHooks"
    CONF_XML_HOOKS              = "FConfirmationSwiftXMLHooks"

class UpdateActions:
    MISSING_MODULE              = 1
    ALREADY_UPDATED             = 2
    UPDATE_AEL                  = 3
    UPDATE_EXTENSION            = 4
    UPDATE_SETTLEMENT_HOOKS     = 5
    UPDATE_CONFIRMATION_HOOKS   = 6

class ModuleTypes:
    MISSING_MODULE              = 0
    AEL_MODULE                  = 1
    EXTENSION_MODULE            = 2


class InputValidator(object):
    def __init__(self, customMessages, customMessageTemplates, fileNames):
        self.customMessages = customMessages
        self.customMessageTemplates = customMessageTemplates
        self.fileNames = fileNames
        self.isValidInput = False

    def IsValidInput(self):
        return self.isValidInput

    def ValidateInput(self):
        if len(self.customMessages) == len(self.customMessageTemplates) == len(self.fileNames):
            if (self.customMessages, self.customMessageTemplates, self.fileNames) == ([''], [''], ['']):
                self.isValidInput = True
            else:
                for templateName, fileName in zip(self.customMessageTemplates, self.fileNames):
                    self.CheckIfTemplateAndFileExist(templateName, fileName)
                else:
                    self.isValidInput = True
        else:
            raise SyntaxError('Message type, template name and file name should be entered for each custom message')

    def CheckIfTemplateAndFileExist(self, templateName, fileName):
        __import__(fileName)
        if fileName not in sys.modules:
            raise LookupError('\nFile  %s is missing' % fileName)
        if not hasattr(sys.modules[fileName], templateName):
            raise LookupError('\nTemplate  %s is missing in %s' % (templateName, fileName))

class InputFormator(object):

    def __init__(self, customMessageTypes, customMessageTemplates, fileNames):
        self.customMessageTypes = customMessageTypes
        self.customMessageTemplates = customMessageTemplates
        self.fileNames = fileNames

    def FormatInput(self):
        self.customMessageTypes = self.RemoveTrailingSpaces(self.customMessageTypes)
        self.customMessageTemplates = self.RemoveTrailingSpaces(self.customMessageTemplates)
        self.fileNames = self.RemoveTrailingSpaces(self.fileNames)
        self.customMessageTypes = self.FilterInvalidInputs(self.customMessageTypes)
        self.customMessageTemplates = self.FilterInvalidInputs(self.customMessageTemplates)
        self.fileNames = self.FilterInvalidInputs(self.fileNames)

    def GetFormattedInput(self):
        self.FormatInput()
        return self.customMessageTypes, self.customMessageTemplates, self.fileNames

    def RemoveTrailingSpaces(self, inputSequence):
        return [x.strip() for x in inputSequence]

    def FilterInvalidInputs(self, inputSequence):
        return filter(lambda x: bool(x), inputSequence)


def ModuleUpdateAction(moduleName, moduleIsUpdatedFunc):
    moduleType = GetModuleType(moduleName)
    moduleText = GetModuleText(moduleName, moduleType)
    updateAction = GetModuleUpdateActionFromModuleText(moduleText, moduleType, moduleIsUpdatedFunc)
    return updateAction

def GetModuleUpdateActionFromModuleText(moduleText, moduleType, moduleIsUpdatedFunc):
    updateAction = UpdateActions.MISSING_MODULE
    if moduleType == ModuleTypes.AEL_MODULE:
        if moduleIsUpdatedFunc(moduleText):
            updateAction = UpdateActions.ALREADY_UPDATED
        else:
            updateAction = UpdateActions.UPDATE_AEL
    elif moduleType == ModuleTypes.EXTENSION_MODULE:
        if moduleIsUpdatedFunc(moduleText):
            updateAction = UpdateActions.ALREADY_UPDATED
        else:
            updateAction = UpdateActions.UPDATE_EXTENSION
    return updateAction

def ConfirmationParametersUpdateAction():
    return ModuleUpdateAction("FConfirmationParameters", ConfirmationParamsIsUpdated)

def SettlementParametersUpdateAction():
    return ModuleUpdateAction("FSettlementParameters", SettlementParamsIsUpdated)

def SwiftParametersUpdateAction():
    return ModuleUpdateAction("FSwiftParameters", SwiftParamsIsUpdated)

def ConfirmationParamsIsUpdated(moduleText):
    isUpdated = "MTMessageToXMLMap" in moduleText
    return isUpdated

def SettlementParamsIsUpdated(moduleText):
    isUpdated = "('ALL', SwiftDefaultXML.documentSettlementSWIFT)" in moduleText
    return isUpdated

def SwiftParamsIsUpdated(moduleText):
    isUpdated = False
    if "OPTIONS[199] = {}" in moduleText and \
    "OPTIONS[299] = {}" in moduleText and \
    "OPTIONS[395] = {}" in moduleText:
        isUpdated = True
    return isUpdated

def GetModuleText(moduleName, moduleType):
    moduleText = ""
    if moduleType == ModuleTypes.AEL_MODULE:
        moduleText = GetAelPythonModuleText(moduleName)
    elif moduleType == ModuleTypes.EXTENSION_MODULE:
        moduleText = GetExtensionPythonModuleText(moduleName)
    else:
        raise Exception("Invalid module type")
    return moduleText

def GetModuleType(moduleName):
    moduleType = ModuleTypes.MISSING_MODULE
    context = acm.GetDefaultContext()
    extension = context.GetExtension(acm.FPythonCode, acm.FObject, moduleName)
    if extension:
        moduleType = ModuleTypes.EXTENSION_MODULE
    elif acm.FAel[moduleName]:
        moduleType = ModuleTypes.AEL_MODULE

    return moduleType

def CreateModuleFunctionList(moduleActionList):
    moduleFunctionList = []
    for moduleName, action, params in moduleActionList:
        actionTuple = None
        if action == UpdateActions.MISSING_MODULE:
            Utils.LogAlways("WARNING: Missing module '%s'." % moduleName)
            continue
        if action == UpdateActions.ALREADY_UPDATED:
            Utils.LogAlways("Module '%s' is already up-to-date." % moduleName)
            continue
        elif action == UpdateActions.UPDATE_AEL:
            if moduleName == ModuleNames.CONF_PARAMS:
                actionTuple = (moduleName, BackupAndUpdateAelPythonModuleModule, UpgradeSteps.UpdateFConfirmationParameters, params)
                moduleFunctionList.append(actionTuple)
            elif moduleName == ModuleNames.SETTLE_PARAMS:
                actionTuple = (moduleName, BackupAndUpdateAelPythonModuleModule, UpgradeSteps.UpdateFSettlementParameters, params)
                moduleFunctionList.append(actionTuple)
            elif moduleName == ModuleNames.SWIFT_PARAMS:
                actionTuple = (moduleName, BackupAndUpdateAelPythonModuleModule, UpgradeSteps.UpdateFSwiftParameters, params)
                moduleFunctionList.append(actionTuple)
        elif action == UpdateActions.UPDATE_EXTENSION:
            if moduleName == ModuleNames.CONF_PARAMS:
                actionTuple = (moduleName, BackupAndUpdateExtensionPythonModuleModule, UpgradeSteps.UpdateFConfirmationParameters, params)
                moduleFunctionList.append(actionTuple)
            elif moduleName == ModuleNames.SETTLE_PARAMS:
                actionTuple = (moduleName, BackupAndUpdateExtensionPythonModuleModule, UpgradeSteps.UpdateFSettlementParameters, params)
                moduleFunctionList.append(actionTuple)
            elif moduleName == ModuleNames.SWIFT_PARAMS:
                actionTuple = (moduleName, BackupAndUpdateExtensionPythonModuleModule, UpgradeSteps.UpdateFSwiftParameters, params)
                moduleFunctionList.append(actionTuple)
        elif action == UpdateActions.UPDATE_CONFIRMATION_HOOKS:
            actionTuple = (moduleName, UpdateAelPythonModule, UpgradeSteps.UpdateConfirmationSwiftHooks, params)
            moduleFunctionList.append(actionTuple)
        elif action == UpdateActions.UPDATE_SETTLEMENT_HOOKS:
            actionTuple = (moduleName, UpdateAelPythonModule, UpgradeSteps.UpdateSettlementSwiftHooks, params)
            moduleFunctionList.append(actionTuple)
    return moduleFunctionList

def UpdateModules(moduleActionList):
    updatedModules = [] #will contain both FAel and ExtensionModule objects
    moduleFunctionList = CreateModuleFunctionList(moduleActionList)
    for moduleName, moduleUpdateFunc, textUpdateFunc, params in moduleFunctionList:
        moduleUpdateFunc(updatedModules, moduleName, textUpdateFunc, params)
    return updatedModules

def BackupAndUpdateAelPythonModuleModule(updatedModules, moduleName, updateFunc, params):
    __BackupAelPython(updatedModules, moduleName)
    UpdateAelPythonModule(updatedModules, moduleName, updateFunc, params)

def UpdateAelPythonModule(updatedModules, moduleName, updateFunc, params, moduleText=None):
    Utils.LogAlways("Updating %s" % moduleName)
    if not moduleText:
        moduleText = GetAelPythonModuleText(moduleName)
    updatedText = updateFunc(moduleText, params)
    updatedModule = UpdateAelPythonModuleModuleText(updatedText, moduleName)
    updatedModules.append(updatedModule)

def __BackupAelPython(updatedModules, moduleName):
    backupName = "%s_BACKUP" % moduleName
    Utils.LogAlways("Creating backup %s" % backupName)
    moduleText = GetAelPythonModuleText(moduleName)
    backupModule = UpdateAelPythonModuleModuleText(moduleText, backupName)
    updatedModules.append(backupModule)

def GetAelPythonModuleText(moduleName):
    moduleText = ""
    module = acm.FAel[moduleName]
    if module:
        moduleText = module.Text()
    return moduleText

def UpdateAelPythonModuleModuleText(moduleText, moduleName):
    module = acm.FAel[moduleName]
    if not module:
        module = acm.FAel()
        module.Name(moduleName)
    module.Text(moduleText)
    return module

def BackupAndUpdateExtensionPythonModuleModule(updatedModules, moduleName, updateFunc, params):
    __BackupExtensionPython(updatedModules, moduleName)
    UpdateExtensionPythonModule(updatedModules, moduleName, updateFunc, params)

def UpdateExtensionPythonModule(updatedModules, moduleName, updateFunc, params, moduleText = None):
    Utils.LogAlways("Updating %s" % moduleName)
    if not moduleText:
        moduleText = GetExtensionPythonModuleText(moduleName)
    extensionModuleName = ExtractExtensionModuleName(moduleText)
    formattedText = FormatExtensionText(moduleText)
    updatedText = updateFunc(formattedText, params)
    updatedText = AddExtensionInformation(updatedText, moduleName, extensionModuleName)
    updatedExtensionModule = UpdateExtensionModule(updatedText, moduleName, extensionModuleName)
    if updatedExtensionModule not in updatedModules:
        updatedModules.append(updatedExtensionModule)

def __BackupExtensionPython(updatedModules, moduleName):
    backupName = "%s_BACKUP" % moduleName
    Utils.LogAlways("Creating backup %s" % backupName)
    moduleText = GetExtensionPythonModuleText(moduleName)   #should use some regex to replace info instead
    extensionModuleName = ExtractExtensionModuleName(moduleText)
    formattedText = FormatExtensionText(moduleText)
    updatedText = AddExtensionInformation(formattedText, backupName, extensionModuleName)
    updatedExtensionModule = UpdateExtensionModule(updatedText, backupName, extensionModuleName)
    if updatedExtensionModule not in updatedModules:
        updatedModules.append(updatedExtensionModule)

def GetExtensionPythonModuleText(moduleName):
    extensionText = ""
    context = acm.GetDefaultContext()
    extension = context.GetExtension(acm.FPythonCode, acm.FObject, moduleName)
    if extension:
        extensionText = extension.AsString()
    return extensionText

def FormatExtensionText(moduleText):
    #removes '[module]FObject:Name' and '...' from text
    formattedText = moduleText
    re = GetREForMatchingStartOfExtensionPythonModule()
    m = re.search(formattedText)
    endIndex = m.end()
    dotIndex = formattedText.rfind("\n...")
    if endIndex > 0 and dotIndex > 0 and endIndex < dotIndex:
        formattedText = formattedText[endIndex:dotIndex]
    return formattedText

def GetREForMatchingStartOfExtensionPythonModule():
    pattern = "^\[(?P<extensionModule>.+)]FObject:.+\n"
    return re.compile(pattern)

def ExtractExtensionModuleName(moduleText):
    extensionModule = ""
    re = GetREForMatchingStartOfExtensionPythonModule()
    m = re.search(moduleText)
    if m:
        extensionModule = m.group("extensionModule")
    return extensionModule

def AddExtensionInformation(moduleText, pythonModuleName, extensionModuleName):
    updatedText = "[%s]FObject:%s\n%s" % (extensionModuleName, pythonModuleName, moduleText)
    return updatedText

def UpdateExtensionModule(moduleText, pythonModuleName, extensionModule):
    context = acm.GetDefaultContext()
    extensionModule = context.GetModule(extensionModule)
    context.EditImport(acm.FPythonCode, moduleText, True, extensionModule)
    return extensionModule

