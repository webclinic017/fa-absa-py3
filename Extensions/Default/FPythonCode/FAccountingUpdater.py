""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingUpdater.py"

import acm




class PostSimulationHandler(object):
    def __init__(self, acmObject, message, importExportStrategy):
        self.__acmObject = acmObject
        self.__message = message
        self.__importExportStrategy = importExportStrategy
        self.__importExportStrategy.AddSeqnbrObjects(acmObject, message)

    def GetImportExportStrategy(self):
        return self.__importExportStrategy

    def GetMessage(self):
        return self.__message

    def GetObject(self):
        return self.__acmObject

    def SetObject(self, acmObject):
        self.__acmObject = acmObject

    def PreCommit(self):
        pass

    def Commit(self):
        self.PreCommit()
        self.__acmObject.Commit()


class MappingPostSimulationHandler(PostSimulationHandler):
    def PreCommit(self):
        self.GetImportExportStrategy().ManageMappingObject(self.GetObject(), self.GetMessage())

class QueryPostSimulationHandler(PostSimulationHandler):
    def PreCommit(self):
        self.GetObject().AutoUser(False)
        self.GetObject().User(None)

def GetMappingClass(typeFunction, message):
    for key, val in __mappingClassesDict.items():
        if typeFunction(key, message):
            return val
    return None


def GetAcmObjectFromMessage(typeFunction, message):
    mappingClass = GetMappingClass(typeFunction, message)
    acmObject = None
    if mappingClass:
        clone = acm.AMBAMessage.CreateCloneFromMessage(message)
        acmObject = mappingClass()
        acmObject.Apply(clone)
    else:
        acmObject = acm.AMBAMessage.CreateObjectFromMessage(message)
    return acmObject



__acmClassToPostSimulationHandlerMap = {acm.FStoredASQLQuery              : QueryPostSimulationHandler,
                                        acm.FBookMapping                  : MappingPostSimulationHandler,
                                        acm.FTreatmentMapping             : MappingPostSimulationHandler,
                                        acm.FAccountingInstructionMapping : MappingPostSimulationHandler,
                                        acm.FTAccountMapping              : MappingPostSimulationHandler}

__mappingClassesDict = {"BOOKMAPPING"             : acm.FBookMapping,
                        "TREATMENTMAPPING"        : acm.FTreatmentMapping,
                        "ACCINSTRUCTIONMAPPING"   : acm.FAccountingInstructionMapping,
                        "TACCOUNTMAPPING"         : acm.FTAccountMapping}

def GetPostSimulationHandlerForObject(acmObject, message, importExportStrategy):
    if acmObject.Class() in __acmClassToPostSimulationHandlerMap:
        return __acmClassToPostSimulationHandlerMap[acmObject.Class()](acmObject, message, importExportStrategy)
    return PostSimulationHandler(acmObject, message, importExportStrategy)
