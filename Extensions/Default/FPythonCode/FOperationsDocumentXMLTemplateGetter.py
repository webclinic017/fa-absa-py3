""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations_document/etc/FOperationsDocumentXMLTemplateGetter.py"

def IsCustomSwiftTemplate(mt, messageToXMLMap):
    messageToXMLMap = dict(messageToXMLMap)
    if str(mt) in messageToXMLMap:
        return True
    else:
        return False

def GetTemplate(confirmation, mt, MTMessageToXMLMap, templateToXMLMap, defaultXMLTemplate):
    if confirmation.IsApplicableForSWIFT():
        return GetSwiftTemplate(mt, MTMessageToXMLMap)

    if confirmation.ConfTemplateChlItem():
        return GetLongformTemplate(confirmation.ConfTemplateChlItem().Name(), templateToXMLMap, defaultXMLTemplate)

    return defaultXMLTemplate

def GetSwiftTemplate(mt, messageToXMLMap):
    messageToXMLMap = dict(messageToXMLMap)
    if str(mt) in messageToXMLMap:
        return messageToXMLMap[str(mt)]

    return messageToXMLMap['ALL']

def GetLongformTemplate(name, templateToXMLMap, defaultTemplate):
    templateToXMLMap = dict(templateToXMLMap)
    return templateToXMLMap.get(name, defaultTemplate)
