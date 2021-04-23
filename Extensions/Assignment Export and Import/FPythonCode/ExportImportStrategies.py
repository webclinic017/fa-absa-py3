""" Compiled: 2012-02-16 11:04:24 """

import acm

from ObjectImportExportProcedures import ObjectImportExportProcedure

class ExportImportStrategy:

    @staticmethod
    def getRoutingStrategy():
        strategy = ExportImportStrategy(acm.FRoutingInstructionMapping, 
                ("Parent", "Previous", "Next"),
                ("RoutingInstruction", "Query"))
        return strategy

    @staticmethod
    def getBookStrategy():
        from ObjectImportExportProcedures import BookProcedure 
        strategy = ExportImportStrategy(acm.FBookMapping,
                                        ("Parent", "Previous", "Next"),
                                        ("Book", "Query"))
        strategy.registerExportImportProcedure(acm.FBook, BookProcedure())
        return strategy

    def __init__(self, mappingClass, mappingReferences, memberProperties):
        self.m_exportImportProcedures = {}
        self.m_defaultExportImportProcedure = ObjectImportExportProcedure()
        self.m_referenceMap = {}
        self.m_mappingObjectClass = mappingClass
        self.m_mappingReferenceNames = mappingReferences
        self.m_memberProperties = memberProperties

    def registerExportImportProcedure(self, domain, procedure):
        self.m_exportImportProcedures[domain] = procedure

    def __getMemberDomain(self, attrName):
        attr = self.m_mappingObjectClass.GetMethod(attrName, 0)
        return attr.Domain()

    def getMappingObjectMemberObjects(self, mappingObject):
        objects = []
        for attrName in self.m_memberProperties:
            memberObject = mappingObject.GetProperty(attrName)
            if None != memberObject:
                objects.append(memberObject)
        return objects

    def isMappingObject(self, object):
        return object.IsKindOf(self.m_mappingObjectClass)

    """ Store references to the mapping object in a map while setting the references to None in order to Commit """
    def manageMappingObject(self, mappingObject):
        objectReferenceValues = []
        for attrName in self.m_mappingReferenceNames:
            val = mappingObject.GetProperty(attrName)
            objectReferenceValues.append(None != val and val.Oid() or None)
            mappingObject.SetProperty(attrName, None)
        self.m_referenceMap[mappingObject.Oid()] = (mappingObject, objectReferenceValues)

    def getManagedMappingObjects(self):
        self.replaceMappingObjectReferences()
        mappingObjects = [pair[0] for pair in self.m_referenceMap.values()]
        return mappingObjects

    def replaceMappingObjectReferences(self):
        for mappingObject, referenceValues in self.m_referenceMap.values():
            referenceDict = dict(list(zip(self.m_mappingReferenceNames, referenceValues)))
            for attrName, oldReferenceId in referenceDict.items():
                mappingObject.SetProperty(attrName, self.mappingObjectFromOldOid(oldReferenceId))

    def mappingObjectFromOldOid(self, oldOid):
        if None != oldOid and not self.m_referenceMap.has_key(oldOid):
            raise Exception("Object id not found. Could not replace reference.")
        return None != oldOid and self.m_referenceMap[oldOid][0] or None

    def exportObject(self, o, file, messageGenerator):
        if self.m_exportImportProcedures.has_key(o.Class()):
            exportProcedure = self.m_exportImportProcedures[o.Class()]
            exportProcedure.exportObject(o, file, messageGenerator)
        else:
            message = messageGenerator.Generate(o)
            try:
                file.write(message.AsString())
            except Exception as e:
                acm.Log("Could not export object: " + str(e))
                raise e

    def __getImportedObjectDomain(self, o):
        """ Composite member objects are exported as an FArray """
        domain = None
        if o.IsKindOf(acm.FCollection):
            firstObject = o.First()
            domain = firstObject and firstObject.Domain() or None
        else:
            domain = o.Domain()
        return domain

    def __getImportProcedure(self, o):
        procedure = None
        memberDomain = self.__getImportedObjectDomain(o)
        if memberDomain and self.m_exportImportProcedures.has_key(o.Class()):
            procedure = self.m_exportImportProcedures[o.Class()]
        else:
            procedure = self.m_defaultExportImportProcedure
        return procedure 

    def importObject(self, o, overwriteExistingObject):
        self.__getImportProcedure(o).importObject(o, overwriteExistingObject)
        
    def preProcessMemberObject(self, o):
        # Do modifications needed to connect object references.
        if o.IsKindOf(acm.FStoredASQLQuery):
            o.AutoUser(False)

    def checkForMissingReferences(self, o):
        foundMissingReference = False
        importProcedure = self.__getImportProcedure(o)
        if importProcedure:
            foundMissingReference = importProcedure.checkForMissingReferences(o)
        return foundMissingReference
