""" Compiled: 2012-02-16 11:04:24 """

import acm

from ExportImportStrategies import ExportImportStrategy

class AssignmentImporter:
    
    messageBeginTag = "[MESSAGE]"
    messageEndTag = "[/MESSAGE]"
    
    @staticmethod
    def importRouting(filename, overwriteMembers):
        result = True
        importer = AssignmentImporter.createRoutingInstructionImporter(overwriteMembers)
        if importer.checkForMissingReferences(filename):
            acm.Log("Import was not performed due to missing referenced objects.")
            result = False
        else:
            importer.importAll(filename)
        return result
    
    @staticmethod
    def createRoutingInstructionImporter(overwriteExistingMembers):
        importer = AssignmentImporter(acm.FRoutingInstructionMapping, 
                                      ExportImportStrategy.getRoutingStrategy(),
                                      overwriteExistingMembers)
        return importer
    
    def __init__(self, assignmentMappingClass, instanceExportStrategy, overwriteExistingMembers):
        self.m_instanceExportStrategy = assignmentMappingClass
        self.m_instanceExportStrategy = instanceExportStrategy
        self.m_overwriteMembers = overwriteExistingMembers
    
    def strategy(self):
        return self.m_instanceExportStrategy
    
    def __getObjectsFromMessages(self, file):
        messageString = self.__readMessageString(file)
        while messageString:
            object = self.__getObjectFromMessage(messageString)
            if None != object:
                yield object
            messageString = self.__readMessageString(file)             

    def __getObjectFromMessage(self, messageString):
        try:
            object = acm.AMBAMessage.CreateObjectFromMessage(messageString)
            if not object:
                raise Exception("Could not create object from message")
            return object
        except Exception as e:
            acm.Log("############### Erroneous Message #################")
            acm.Log(messageString)
            acm.Log("############### End Erroneous Message #################")
            raise e

    def getMappingObjectsFromMessages(self, file):
        # Import all mapping objects at once in order to be able to resolve references later
        allMappingObjects = []
        for object in self.__getObjectsFromMessages(file):
            if self.strategy().isMappingObject(object):
                allMappingObjects.append(object)
        return allMappingObjects
    
    def getMemberObjectsFromMessages(self, file):
        for object in self.__getObjectsFromMessages(file):
            if not self.strategy().isMappingObject(object):
                self.strategy().preProcessMemberObject(object)
                yield object
            else:
                # Member objects comes first in file
                break
    
    def __readMessageString(self, file):
        messageComplete = False
        messageLines = []
        line = file.readline().rstrip()
        if line == AssignmentImporter.messageBeginTag:
            messageLines.append(line)
            while line and line != AssignmentImporter.messageEndTag:
                line = file.readline().rstrip()
                messageLines.append(line)

        if len(messageLines) and line == AssignmentImporter.messageEndTag:
            messageComplete = True
        return messageComplete and "\n".join(messageLines) or None

    def importMemberObjects(self, fileName):
        with open(fileName, 'r') as file:
            try:
                acm.BeginTransaction()
                for o in self.getMemberObjectsFromMessages(file):
                    self.strategy().importObject(o, self.m_overwriteMembers)
                acm.CommitTransaction()
            except Exception as e:
                acm.AbortTransaction()
                acm.Log("Import of referenced objects failed: %s"%str(e))
                raise e
    
    def importMappingObjects(self, fileName):
        """ Write down the mapping objects without references to each other """
        with open(fileName, 'r') as file:
            try:
                acm.BeginTransaction()
                for o in self.getMappingObjectsFromMessages(file):
                    objectClone = o.Clone()
                    self.strategy().manageMappingObject(objectClone)
                    objectClone.Commit()
                acm.CommitTransaction()
            except Exception as e:
                acm.AbortTransaction()
                acm.Log("Import of mapping objects failed #1: %s"%str(e))
                raise e
            
        """ Write down the mapping objects with the references updated with new Oid's """
        try:
            acm.BeginTransaction()
            for o in self.strategy().getManagedMappingObjects():
                o.Commit()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            acm.Log("Import of mapping objects failed #2: %s"%str(e))
            raise e

    def importAll(self, filename):
        acm.Log("Importing member objects...")
        self.importMemberObjects(filename)
        acm.Log("...import of member objects done.")
        acm.PollDbEvents()
        acm.Log("Importing mapping objects...")
        self.importMappingObjects(filename)
        acm.Log("...import of mapping objects done.")

    def checkForMissingReferences(self, filename):
        foundMissingReferences = False
        with open(filename, 'r') as file:
            for o in self.getMemberObjectsFromMessages(file):
                if self.strategy().checkForMissingReferences(o):
                    foundMissingReferences = True
        return foundMissingReferences
