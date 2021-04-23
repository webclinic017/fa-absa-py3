""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/CreateOrderMappingHierarchy.py"

"""------------------------------------------------------------------------------------------------
MODULE
    CreateOrderMappingHierarchy

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

DESCRIPTION
    Create Order Mapping Hierarchy

------------------------------------------------------------------------------------------------"""


import acm
from OrderMappingHierarchyDefinitions import Names, ChoiceListNames, ChoiceListDefs, DefaultReportingSheet, ColumnDefs, Hierarchy

RECREATE_HIERARCHY = False


class CreateSecLendHierarchy(object):
    def GetDataTypeInteger( self, dataTypeString, dataTypeGroup ):
        enumeration = 0

        if dataTypeGroup == 'Standard' :
            enumeration = acm.FEnumeration['enum(B92StandardType)']
        elif dataTypeGroup == 'Enums' :
            enumeration = acm.FEnumeration['enum(B92EnumType)']
        elif dataTypeGroup == 'RecordRef' :
            enumeration = acm.FEnumeration['enum(B92RecordType)']

        return enumeration.Enumeration(dataTypeString) if enumeration else 0

    def CreateChoiceList(self, choiceListName, choices, list = 'MASTER') :
        choiceList = acm.FChoiceList.Select('name = \'' + choiceListName + '\' and list = \'' + list + '\'')
    
        if not choiceList :
            choiceList = acm.FChoiceList()
            choiceList.List(list)
            choiceList.Name(choiceListName)
            choiceList.Commit()

        for choice in choices :
            self.CreateChoiceList(choice, [], choiceListName)

    def CreateChoiceLists(self) :
        try :
            acm.BeginTransaction() 

            for cd in ChoiceListDefs.Def :
                self.CreateChoiceList(cd['Name'], cd['Values'])


            acm.CommitTransaction()
        except Exception as ex :
            print(ex.message)
            acm.AbortTransaction()

    def CreateReportingSheetTemplate(self):
        if not acm.FTradingSheetTemplate.Select("name = '%s'" % DefaultReportingSheet.Name):
            sheetDefinition = acm.Sheet.GetSheetDefinition(DefaultReportingSheet.SheetType)
            gridBuilder = sheetDefinition.CreateGridBuilder(False)
            sheetTemplate = gridBuilder.MakeSheetTemplate(DefaultReportingSheet.Name, ".".join(DefaultReportingSheet.Columns))
            sheetTemplate.AutoUser(False)
            sheetTemplate.User = None
            sheetTemplate.Commit()
            
    def CreateColumnDefinition(self, columnSpecificationName, hierarchyType, dataTypeGroup, dataTypeString, dataTypeInfo, leavesOnly, description, previousColumnDefinitionName):

        columnDefinition = acm.FHierarchyColumnSpecification()
        columnDefinition.Name(columnSpecificationName)
        columnDefinition.HierarchyType(hierarchyType)
        columnDefinition.DataTypeGroup(dataTypeGroup)
        columnDefinition.DataTypeType(self.GetDataTypeInteger(dataTypeString, dataTypeGroup))
        columnDefinition.DataTypeInfo(dataTypeInfo)
        columnDefinition.LeafsOnly(leavesOnly)
        columnDefinition.Description(description)
        columnDefinition.PreviousColumnSpecificationName(previousColumnDefinitionName)

        columnDefinition.RegisterInStorage()
        
        return columnDefinition
        
    def GetValidHierachyDataValue(self, value, columnSpecification) :
        hierarchyDataValue = acm.FHierarchyDataValue()
        hierarchyDataValue.HierarchyColumnSpecification = columnSpecification
        
        if value :
            hierarchyDataValue.DataValueVA(value)

        dataValue = hierarchyDataValue.DataValue()

        return hierarchyDataValue, dataValue
        
    def CreateHierarchyDataValue(self, node, columnSpecification, value):
        hierarchyDataValue, dataValue = self.GetValidHierachyDataValue(value, columnSpecification)
        
        if hierarchyDataValue.DataValue() not in [None, '']:
            hierarchyDataValue.HierarchyNode = node
            hierarchyDataValue.RegisterInStorage()
            
    def CreateHierarcyFromDef(self, parentNode, nodeDefinitions, hierarchyTree, columnSpecByName) :
        for nodeDef in nodeDefinitions :
            nodeName = nodeDef.get('DisplayName', '')
            node = hierarchyTree.Add(nodeName, parentNode)
            node.RegisterInStorage()

            isLeaf = not nodeDef.get('Children') 
            leavesOnly = False

            for columnSpecName, value in nodeDef.iteritems() :
                if columnSpecName == 'Children' :
                    self.CreateHierarcyFromDef(node, value, hierarchyTree, columnSpecByName)
                elif columnSpecName != 'DisplayName' :
                    columnSpec = columnSpecByName.get(columnSpecName, None)
                    if columnSpec:
                        if  columnSpec.LeafsOnly() :
                            leavesOnly = True
                        if not isLeaf and leavesOnly:
                            print('Incorrect hierarchy, leaves only column specification value added to node that has children')
                        else:
                            self.CreateHierarchyDataValue(node, columnSpec, value)
                    else:
                        print('No column specification name: ' + columnSpecName)
            
            
            node.IsLeaf(isLeaf and leavesOnly)
            
    def CreateHierarchy(self, hierarchyTree) :
        hierarchy = hierarchyTree.Hierarchy()        
        hierarchyType = hierarchy.HierarchyType()

        columnSpecByName = {}

        for columnSpec in hierarchyType.HierarchyColumnSpecifications() :
            columnSpecByName[str(columnSpec.Name())] = columnSpec

        self.CreateHierarcyFromDef(None, Hierarchy.Def, hierarchyTree, columnSpecByName)

    def CreateHierarchyType(self, hierarchyTypeName) :
        hierarchyType = acm.FHierarchyType[hierarchyTypeName]

        if hierarchyType :
            hierarchyType.Delete()

        hierarchyType = acm.FHierarchyType()
        hierarchyType.Name(hierarchyTypeName)
        hierarchyType.RegisterInStorage()

        previous = ''
        for cd in ColumnDefs.Def :
            self.CreateColumnDefinition(cd['Name'], hierarchyType, cd['TypeGroup'], cd['TypeString'], cd.get('TypeInfo', ''), cd.get('LeavesOnly', False), cd.get('Description', ''), previous)
            previous = cd['Name']
        
        return hierarchyType

    def Create(self, hierarchyName, hierarchyTypeName) :
        try :
            self.CreateChoiceLists()
            self.CreateReportingSheetTemplate()

            hierarchy = acm.FHierarchy[hierarchyName]

            if hierarchy :
                if not RECREATE_HIERARCHY:
                    return
                hierarchy.Delete()
    
            hierarchy = acm.FHierarchy()
            hierarchy.Name(hierarchyName)
            hierarchy.RegisterInStorage()
            hierarchyType = self.CreateHierarchyType(hierarchyTypeName)

            hierarchy.HierarchyType(hierarchyType)
    
            hierarchyTree = acm.FHierarchyTree()
            hierarchyTree.Hierarchy(hierarchy)

            self.CreateHierarchy(hierarchyTree)
            
            hierarchyType.Commit()
            hierarchy.Commit()
        except Exception as ex:
            print(ex.message)


def Run() :
    c = CreateSecLendHierarchy()
    c.Create(Names.HierarchyInstance, Names.HierarchyType)
