""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/SecuritiesLending/etc/HierarchySetup.py"
from __future__ import print_function
"""-------------------------------------------------------------------------------------------
MODULE
    HierarchySetup

    (c) Copyright 2017 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    Generate an example tree of Additional Cost for SecLend pricing with dummy data
-------------------------------------------------------------------------------------------"""

import acm, ael
from random import uniform


class HierarchyCreator:

    HIERARCHY_NAME = 'Additional Cost'
    HIERARCHY_TYPE_NAME = 'Additional Cost'
    RESULT_COLUMN = 'Additional Cost'
    standardDomains = acm.FEnumeration['enum(B92StandardType)'].EnumeratorStringsSkipFirst().Sort()
    enumDomains = acm.FEnumeration['enum(B92EnumType)'].EnumeratorStringsSkipFirst().Sort()
    refsDomains = acm.FEnumeration['enum(B92RecordType)'].EnumeratorStringsSkipFirst().Sort()

    #                     ColumnName, Domain Type, Domain, DataTypeInfo, Description, Leafs only, Unique Values
    columnsDict =       {'Tier': ['RecordRef', 'ChoiceList', 'User Rating', 'User Rating', False, False],
                         'Source': ['RecordRef', 'Party', '', 'Source of trade', False, False],
                         'Additional Cost': ['Standard', 'Double', '', 'Resulting additional cost', False, False]
                        }

    columnDictOrderList = [ 'Tier', 'Source', 'Additional Cost' ]

    hierarchyDict = {HIERARCHY_TYPE_NAME: columnsDict}

    def GetDataTypeInteger(self, domainType, dataTypeString):
        enumeration = 0
        if domainType == 'Standard':
            enumeration = acm.FEnumeration['enum(B92StandardType)']
        elif domainType == 'Enum':
            enumeration = acm.FEnumeration['enum(B92EnumType)']
        elif domainType == 'RecordRef':
            enumeration = acm.FEnumeration['enum(B92RecordType)']
        return enumeration.Enumeration(dataTypeString) if enumeration else 0

    def CreateHierarchyType(self, name, columnDict):
        print('Creating hierarchy type for %s...' % name)
        ht = acm.FHierarchyType()
        ht.Name(name)
        ht.Commit()
        for column in self.columnDictOrderList:
            hierarchyColumnSpec = acm.FHierarchyColumnSpecification()
            hierarchyColumnSpec.Name(column)
            hierarchyColumnSpec.LeafsOnly(columnDict[column][4])
            hierarchyColumnSpec.UniqueValues(columnDict[column][5])
            hierarchyColumnSpec.Description(columnDict[column][3])
            hierarchyColumnSpec.DataTypeGroup(columnDict[column][0])
            hierarchyColumnSpec.DataTypeInfo(columnDict[column][2])
            hierarchyColumnSpec.DataTypeType(self.GetDataTypeInteger(
                hierarchyColumnSpec.DataTypeGroup(), columnDict[column][1]))
            
            hierarchyColumnSpec.HierarchyType(ht)
            hierarchyColumnSpec.Commit()
            print('Created column for %s' % column)
        print('HierarchyType %s created.' % name)

    def GetHierarchyColumnSpec(self, columnName):
        return acm.FHierarchyColumnSpecification.Select('name = "%s"\
            and hierarchyType = "%s"' % (columnName, self.HIERARCHY_TYPE_NAME))

    def SetDataValue(self, node, value, columnName):
        # Using try/except since dataValue doesn't accept empty strings.
        try:
            columnSpec = self.GetHierarchyColumnSpec(columnName)
            dataValue = acm.FHierarchyDataValue()
            dataValue.HierarchyNode(node)
            dataValue.HierarchyColumnSpecification(columnSpec)
            print('Setting value: ', value, ' on node ')
            dataValue.DataValueVA(value)
            node.HierarchyDataValues().Add(dataValue)
        except Exception as e:
            print(e)
            
    def RandomNumber(self, low, high, rounding):
        return round(uniform(low, high), rounding)

    def Setup(self):
        for key in self.hierarchyDict:
            if not acm.FHierarchyType[key]:
                self.CreateHierarchyType(key, self.hierarchyDict[key])
        
        hierarchy = acm.FHierarchy()
        hierarchy.Name(self.HIERARCHY_NAME)
        hierarchy.HierarchyType(self.HIERARCHY_TYPE_NAME)
        hierarchyTree = acm.FHierarchyTree()
        hierarchyTree.Hierarchy(hierarchy)
        rootNode = hierarchyTree.Add(hierarchy.Name(), None)
        self.SetDataValue(rootNode, hierarchy.Name(), self.RESULT_COLUMN)
        self.SetDataValue(rootNode, self.RandomNumber(0.9, 1.1, 0), self.RESULT_COLUMN)
        rootNode.IsLeaf(False)
        hierarchy.HierarchyNodes().Add(rootNode)
        
        ratings = acm.FChoiceList['User Rating']
        if ratings:
            for rating in ratings.Choices():
            
                hierarchyNode = hierarchyTree.Add(rating.Name(), rootNode)
                hierarchyNode.IsLeaf(False)
                hierarchy.HierarchyNodes().Add(hierarchyNode)
                for market in acm.FMarketPlace.Select(''):
                    hierarchyChildNode = hierarchyTree.Add(market.Name(), hierarchyNode)
                    self.SetDataValue(hierarchyChildNode, rating.Name(), 'Tier')
                    self.SetDataValue(hierarchyChildNode, market, 'Source')
                    self.SetDataValue(hierarchyChildNode, self.RandomNumber(0.1, 2, 2), self.RESULT_COLUMN)
                    hierarchyChildNode.IsLeaf(False)
                    hierarchy.HierarchyNodes().Add(hierarchyChildNode)
            hierarchy.Commit()
        else:
            print('FChoiceList User Rating is not defined')

    def Cleanup(self):
        for key in self.hierarchyDict:
            type = acm.FHierarchyType[key]
            hs = None
            if type:
                hs = acm.FHierarchy.Select('hierarchyType=%s'%type.Oid())            
            if hs:
                for h in hs:
                    h.Delete()
            if type:
                type.Delete() 

                
def RunCleanupAndSetup():
    h = HierarchyCreator()
    h.Cleanup()
    h.Setup()
        

