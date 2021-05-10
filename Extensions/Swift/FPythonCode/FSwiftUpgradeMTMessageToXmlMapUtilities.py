""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/upgrade/FSwiftUpgradeMTMessageToXmlMapUtilities.py"
import re
import sys

def ModifyFConfirmationSwiftXmlHooks(moduleText, customMessageTypes, customMessageTemplates, fileNames):
    updatedText = moduleText
    for aMessageType, aTemplateName, aFileName in zip(customMessageTypes, customMessageTemplates, fileNames):
        customTemplateVariableTextToBeAdded = GenerateTemplateForCustomMessage(aMessageType, aTemplateName, aFileName)
        updatedText = AddVariableTextToModuleText(updatedText, customTemplateVariableTextToBeAdded)
    return updatedText

def GetMTMessageToXMLMapDefaultTupleForSettlement():
    return '''('ALL', SwiftDefaultXML.documentSettlementSWIFT)'''

def GetImportStatementForSettlementTemplates():
    return '''import FSettlementSwiftDefaultXML as SwiftDefaultXML'''

def AddMTMessageToXMLMapDefaultTupleForSettlement(moduleText, defaultTuple):
    updatedText = moduleText
    reForMatchingMTMessageToXMLMap = GetRegularExpressionForMatchingMTMessageToXMLMap()
    matchObject = reForMatchingMTMessageToXMLMap.search(updatedText)
    if matchObject:
        mtMessageToXMLMap = matchObject.group().strip()
        reForCheckingEmptyMTMessageToXMLMapValue = GetRegularExpressionForCheckingIfMTMessageXMLMapValueIsEmpty()
        if reForCheckingEmptyMTMessageToXMLMapValue.search(mtMessageToXMLMap): #MTMessageToXMLMap is empty
            substituteValue = mtMessageToXMLMap[:-1] + defaultTuple + ']'
        else:
            substituteValue = mtMessageToXMLMap[:-1] + ',' + defaultTuple + ']'
        updatedText = reForMatchingMTMessageToXMLMap.sub(substituteValue, updatedText)
    return updatedText

def GetRegularExpressionForMatchingMTMessageToXMLMap():
    return re.compile('''MTMessageToXMLMap\s*=\s*\[\s*(\s*,*\s*\(\s*'\s*\w*\s*'\s*,\s*\w*.\w*\s*\)\s*)*\s*\]''', re.DOTALL)

def GetRegularExpressionForCheckingIfMTMessageXMLMapValueIsEmpty():
    return re.compile('''\[\s*\]''', re.DOTALL)

def GenerateMtMessageToXMLMapText():
    mtMessageToXMLMapTupleEntries = []
    defaultTuple = GetMTMessageToXMLMapDefaultTupleForConfirmation()
    mtMessageToXMLMapTupleEntries.append(defaultTuple)
    mtMessageToXMLMapValue = '[' + ', '.join(mtMessageToXMLMapTupleEntries) + ']'
    mtMessageToXMLMapText = '''MTMessageToXMLMap                               = '''
    return mtMessageToXMLMapText + mtMessageToXMLMapValue

def GetImportStatementForConfirmationTemplates():
    return '''import FConfirmationSwiftDefaultXML as SwiftDefaultXML'''

def GetMTMessageToXMLMapDefaultTupleForConfirmation():
    return '''('ALL', SwiftDefaultXML.documentConfirmationSWIFT)'''

def AddImportStatement(moduleText, importStatement):
    updatedText = moduleText
    index = moduleText.find('\nMTMessageToXMLMap')
    if index > 0:
        updatedText = moduleText[:index] + "\n" + importStatement + moduleText[index:]
    return updatedText

def AddVariableTextToModuleText(moduleText, variableTextToBeAdded):
    updatedText = moduleText
    if len(moduleText) and moduleText[-1] == "\n":
        updatedText += "\n"
    else:
        updatedText += "\n\n"
    updatedText += variableTextToBeAdded
    return updatedText

def GenerateTemplateForCustomMessage(mtType, templateName, fileName):
    mtVariable = 'MT%s_template' % mtType
    module = sys.modules[fileName]
    template = getattr(module, templateName)
    return ''.join([mtVariable, " = \'''", template, "\'''"])

def GetOptionsTextToBeAddedInSwiftParam(moduleText):
    option199 = "OPTIONS[199] = {}"
    option299 = "OPTIONS[299] = {}"
    option395 = "OPTIONS[395] = {}"

    concatList = [""]
    if option199 not in moduleText:
        concatList.append(option199)
    if option299 not in moduleText:
        concatList.append(option299)
    if option395 not in moduleText:
        concatList.append(option395)
    return "\n\n".join(concatList)

def AddOptionsTextToSwiftParam(moduleText, optionsText):
    updatedText = moduleText
    reForMatchingStartOfOptionsConfiguration = GetREForMatchingStartOfOptionsConfiguration()
    matchObject = reForMatchingStartOfOptionsConfiguration.search(updatedText)
    if matchObject:
        optionsEntry = matchObject.group().strip()
        substituteValue = optionsEntry + optionsText
        updatedText = reForMatchingStartOfOptionsConfiguration.sub(substituteValue, updatedText)
    return updatedText

def GetREForMatchingStartOfOptionsConfiguration():
    return re.compile("OPTIONS\s*=\s*\{\s*\}", re.DOTALL)

