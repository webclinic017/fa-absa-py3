""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/upgrade/FSwiftUpgradeHooksAndDropFieldsUtilities.py"

import xml.dom.minidom as dom
import FSwiftParameters as FSwiftParameters

def GetAllMessageTypesToProcess(hooksDict, mtDropFieldsDict):
    return set(hooksDict.keys()).union({str(eachKey)   for eachKey in mtDropFieldsDict if mtDropFieldsDict[eachKey] })

def GenerateTagsFromHooks(mtTags, templateXml):
    for module, tagName in mtTags:
        newLineNode = templateXml.createTextNode('\n')
        spaceNode = templateXml.createTextNode('    ')
        acmCodeElement = templateXml.createElement('acmCode')
        acmCodeElement.setAttribute('function', tagName)
        acmCodeElement.setAttribute('file', module)
        tagElement = templateXml.createElement(tagName)
        tagElement.appendChild(acmCodeElement)
        templateXml.lastChild.appendChild(spaceNode)
        templateXml.lastChild.appendChild(tagElement)
        templateXml.lastChild.appendChild(newLineNode)

def GenerateTagsFromDropFields(dropFields, templateXml):
    for aDropField in dropFields:
        newLineNode = templateXml.createTextNode('\n')
        spaceNode = templateXml.createTextNode('    ')
        tagElement = templateXml.createElement('acmDelete')
        tagElement.setAttribute('tagName', aDropField)
        templateXml.lastChild.appendChild(spaceNode)
        templateXml.lastChild.appendChild(tagElement)
        templateXml.lastChild.appendChild(newLineNode)

def GetDictFromHooks(swiftHooks):
    hooksDict = {'CONFIRMATION': [], 'SETTLEMENT' : [] }
    for aHook in swiftHooks:
        mtType = aHook.GetMtType()
        if mtType.isdigit():
            if mtType not in hooksDict:
                hooksDict.setdefault(mtType, [])
            hooksDict[mtType].append( (aHook.GetModuleName(), aHook.GetXmlTagName()))
        elif mtType.find('C') != -1:
            hooksDict['CONFIRMATION'].append( (aHook.GetModuleName(), aHook.GetXmlTagName()))
        elif mtType.find('S') != -1:
            hooksDict['SETTLEMENT'].append( (aHook.GetModuleName(), aHook.GetXmlTagName()))
        elif len(mtType) == 3:
            hooksDict['CONFIRMATION'].append( (aHook.GetModuleName(), aHook.GetXmlTagName()))
            hooksDict['SETTLEMENT'].append( (aHook.GetModuleName(), aHook.GetXmlTagName()))
    return hooksDict

def GetOverrideTemplateForMessageType(aMessageType, hooksDict, dropfieldsDict):
    template = '''<SWIFT>
</SWIFT>'''
    templateXml = dom.parseString(template)
    if aMessageType.isdigit():
        if aMessageType in hooksDict:
            GenerateTagsFromHooks(hooksDict[aMessageType], templateXml)
        if int(aMessageType) in dropfieldsDict and dropfieldsDict[int(aMessageType)]:
            GenerateTagsFromDropFields(dropfieldsDict[int(aMessageType)], templateXml)
    else:
        GenerateTagsFromHooks(hooksDict[aMessageType], templateXml)
    return templateXml

def GenerateTemplateTextForSpecificMT(aMessageType, templateXml):
    templateVariable = 'MT%s_template' % aMessageType
    templateText = ''.join([templateVariable, " = \'''", templateXml.lastChild.toxml(), "\'''"])
    return templateText

def GenerateTemplateTextForCommonBlock(templateXml):
    templateVariable = 'commonBlock_template'
    templateText = ''.join([templateVariable, " = \'''", templateXml.lastChild.toxml(), "\'''"])
    return templateText

def AddTemplateTextForSpecificMT(templateXml, aMessageType, confirmationOverrides, settlementOverrides):
    templateText = GenerateTemplateTextForSpecificMT(aMessageType, templateXml)
    if int(aMessageType) in dict(FSwiftParameters.USED_MT_MESSAGES_CONFIRMATION):
        confirmationOverrides.append(templateText)
        confirmationOverrides.append('\n\n')
    elif int(aMessageType) in dict(FSwiftParameters.USED_MT_MESSAGES_SETTLEMENT):
        settlementOverrides.append(templateText)
        settlementOverrides.append('\n\n')

def AddTemplateTextForCommonBlock(templateXml, aMessageType, confirmationOverrides, settlementOverrides):
    template = '''<SWIFT>
</SWIFT>'''
    if template != templateXml.lastChild.toxml():
        templateText = GenerateTemplateTextForCommonBlock(templateXml)
        if aMessageType == 'CONFIRMATION' :
            confirmationOverrides.append(templateText)
            confirmationOverrides.append('\n\n')
        elif aMessageType == 'SETTLEMENT':
            settlementOverrides.append(templateText)
            settlementOverrides.append('\n\n')

def AddTemplateToOverrideVariable(templateXml, aMessageType, confirmationOverrides, settlementOverrides):
    if aMessageType.isdigit():
        AddTemplateTextForSpecificMT(templateXml, aMessageType, confirmationOverrides, settlementOverrides)
    else:
        AddTemplateTextForCommonBlock(templateXml, aMessageType, confirmationOverrides, settlementOverrides)
