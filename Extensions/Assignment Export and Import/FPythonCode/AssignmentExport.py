""" Compiled: 2012-02-16 11:04:24 """

import acm

from ExportImportStrategies import ExportImportStrategy

class AssignmentExporter(object):

    @staticmethod
    def exportRouting(filename):
        exporter = AssignmentExporter.createRoutingInstructionExporter()
        return exporter.export(filename)

    @staticmethod
    def createRoutingInstructionExporter():
        exporter = AssignmentExporter(acm.FRoutingInstructionMapping, 
                                      ExportImportStrategy.getRoutingStrategy())
        return exporter

    def __init__(self, assignmentMappingClass, instanceExportStrategy):
        self.m_mappingClass = assignmentMappingClass
        self.m_instanceExportStrategy = instanceExportStrategy

    def exporter(self):
        return self.m_instanceExportStrategy
    
    def strategy(self):
        return self.m_instanceExportStrategy
    
    def mappingClass(self):
        return self.m_mappingClass

    def __getAllMappingInstances(self):
        return self.m_mappingClass.Select("oid > 0")

    def __findRootMappingInstances(self, allInstances):
        parentInstances = []
        for instance in allInstances:
            if (not instance.Parent()):
                parentInstances.append(instance)
        return parentInstances
    
    def __findMappingChildren(self, parent, allInstances):
        children = [i for i in allInstances if i.Parent() == parent]
        return children

    """ Retrieve the instances of the related mapping class in the order which they should be imported
        later on. """
    def __getInstancesHierarchyOrdered(self):
        mappingsOrdered = []
        allInstances = self.__getAllMappingInstances()
        rootMappingInstances = self.__findRootMappingInstances(allInstances)
        for root in rootMappingInstances:
            self.__getMappingTree(root, allInstances, mappingsOrdered)
        return mappingsOrdered

    def getAllReferencedObjects(self):
        allInstances = self.__getAllMappingInstances()
        referencedObjects = []
        for i in allInstances:
            for o in self.__getMappingObjectMemberObjects(i):
                if not o in referencedObjects:
                    referencedObjects.append(o)
        return referencedObjects

    @staticmethod
    def compareSameLevelMappings(first, second):
        if not second.Previous():
            return 1
        tmp = second
        while tmp and tmp != first:
            tmp = tmp.Previous()
        return tmp == first and -1 or 1

    def __getMappingTree(self, parent, allInstances, mappingsOrdered):
        mappingsOrdered.append(parent)
        children = self.__findMappingChildren(parent, allInstances)
        children.sort(AssignmentExporter.compareSameLevelMappings)
        for child in children:
            self.__getMappingTree(child, allInstances, mappingsOrdered)

    def __getMappingObjectMemberObjects(self, mappingInstance):
        return self.strategy().getMappingObjectMemberObjects(mappingInstance)
    
    def __exportAllObjects(self, file):
        self.exportReferencedObjects(file)
        self.exportMappingObjects(file)
    
    def exportReferencedObjects(self, file):
        messageGenerator = acm.FAMBAMessageGenerator()
        messageGenerator.ShowSeqNbr(False)
        for o in self.getAllReferencedObjects():
            self.strategy().exportObject(o, file, messageGenerator)

    def exportMappingObjects(self, file):
        messageGenerator = acm.FAMBAMessageGenerator()
        for o in self.__getInstancesHierarchyOrdered():
            self.strategy().exportObject(o, file, messageGenerator)
    
    def export(self, fileName):
        result = True
        with open(fileName, 'w') as file:
            try:
                self.__exportAllObjects(file)
            except Exception as e:
                acm.Log("Export failed: %s"%str(e))
                result = False
        return result
