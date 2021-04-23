
import acm, time

def __PopulateColumn(columnData, hierarchyType, colSpec, restriction, mandatory, uniqueValues):
    name, dataTypeGroup, dataTypeType, dataTypeInfo, description = columnData
    colSpec.Name = name
    colSpec.DataTypeGroup = dataTypeGroup
    colSpec.DataTypeType = dataTypeType
    colSpec.DataTypeInfo = dataTypeInfo
    colSpec.Description = description
    colSpec.HierarchyType = hierarchyType
    colSpec.Restriction = restriction
    colSpec.Mandatory = mandatory
    colSpec.UniqueValues = uniqueValues
    colSpec.Commit()
    
def CreateColumn(columnData, hierarchyType, restriction, mandatory, uniqueValues):
    newColSpec = acm.FHierarchyColumnSpecification()
    __PopulateColumn( columnData, hierarchyType, newColSpec, restriction, mandatory, uniqueValues )
    return newColSpec

def CreateDataValue(node, colDef, dataValue):
    newDataValue = acm.FHierarchyDataValue()
    newDataValue.HierarchyNode = node
    newDataValue.HierarchyColumnSpecification = colDef
    newDataValue.DataValue(dataValue)
    newDataValue.Commit()
    return newDataValue

def __TimeStamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def __VerifyAndModifyHierarchyType( hierarchyType, hierarchyColumns ):
    currentColumns = hierarchyType.HierarchyColumnSpecifications()
    columnsToAdd = [] #list of columnData
    columnsToModify = [] #list of columnData
    columnSpecsToRemove = set(currentColumns) #set of columnSpecs
    hierarchiesExist = hierarchyType.Hierarchies() and len( hierarchyType.Hierarchies() ) > 0
    
    for columnData in hierarchyColumns:
        name, dataTypeGroup, dataTypeType, dataTypeInfo, _ = columnData
        currentColumn = None
        for cc in currentColumns:
            if cc.Name() == name:
                currentColumn = cc
                columnSpecsToRemove.remove( currentColumn )
                break
        if currentColumn:
            if  hierarchiesExist and (currentColumn.DataTypeGroup() != dataTypeGroup or \
                currentColumn.DataTypeType() != dataTypeType or \
                currentColumn.DataTypeInfo() != dataTypeInfo):
                return False
            else:
                columnsToModify.append( (columnData, currentColumn) )
        else:
            columnsToAdd.append( columnData )

    if len(columnSpecsToRemove) > 0 and hierarchiesExist:
        return False

    for toRemove in columnSpecsToRemove:
        currentColumns.Remove( toRemove )
    for toAdd in columnsToAdd:
        currentColumns.Add( CreateColumn( toAdd, hierarchyType, 'None', False, False ) )
    for toModifyData, toModify in columnsToModify:
        __PopulateColumn( toModifyData, hierarchyType, toModify, 'None', False, False )
    return True

def __CreateNodesRecursive(level, hierarchy, parent, previousSibling, columnSpecificationsPerTag, depth):
    newNode = acm.FHierarchyNode()
    newNode.IsLeaf = False
    newNode.DisplayName = level[0]
    if parent:
        newNode.ParentId = parent.UniqueId()
    if previousSibling:
        newNode.PreviousSiblingId = previousSibling.UniqueId()
    newNode.Hierarchy = hierarchy
    newNode.Commit()
    
    tags = level[1]
    for tag in tags:
        colDef = columnSpecificationsPerTag[tag]
        if colDef:
            CreateDataValue(newNode, colDef, tags[tag])
        else:
            print ('Column Def for ', tag, ' not found')
    levelType = tags.get('Level Type') if tags.get('Level Type') else 'Top level'
    
    print (__TimeStamp() + '   ' + '  ' * depth + levelType + ' "' + level[0] + '"')

    children = level[2]
    if children:
        previousSibling = None
        for child in children:
            previousSibling = __CreateNodesRecursive(child, hierarchy, newNode, previousSibling, columnSpecificationsPerTag, depth + 1)
    return newNode

def CreateHierarchyType( typeName, hierarchyColumns ):
    hierarchyType = None
    if acm.FHierarchyType[typeName]:
        hierarchyType = acm.FHierarchyType[typeName]
        if not __VerifyAndModifyHierarchyType( hierarchyType, hierarchyColumns ):
            errorMessage = 'Hierarchy type ' + typeName + ' cannot be modified to align with column definitions'
            print (errorMessage)
            raise Exception(errorMessage)
    else:
        hierarchyType = acm.FHierarchyType()
        hierarchyType.Name = typeName
        hierarchyType.Commit()

        for columnData in hierarchyColumns:
            CreateColumn(columnData, hierarchyType, 'None', False, False)

    return hierarchyType

def CreateHierarchy(hierarchyType, hierarchyName, hierarchyData, createChoiceList, choiceListName):
    print ('---------------- Setup of hierarchy "' + hierarchyName + '" ----------------')

    if createChoiceList:
        print (__TimeStamp())
        print (__TimeStamp() + ' Creating choice list "' + choiceListName + '"')


    if acm.FHierarchy[hierarchyName]:
        errorMessage = 'Hierarchy  ' + hierarchyName + ' already exists'
        print (errorMessage)
        raise Exception(errorMessage)

    hierarchy = acm.FHierarchy()
    hierarchy.Name = hierarchyName
    hierarchy.HierarchyType = hierarchyType
    hierarchy.Commit()

    columnSpecificationsPerTag = {}
    print (__TimeStamp())
    print (__TimeStamp() + ' Creating hierarchy columns')
    for columnSpecification in hierarchyType.HierarchyColumnSpecifications():
        print (__TimeStamp() + '   "' + columnSpecification.Name() + '"')
        columnSpecificationsPerTag[columnSpecification.Name()] = columnSpecification

    print (__TimeStamp())
    print (__TimeStamp() + ' Creating hierarchy nodes')
    __CreateNodesRecursive(hierarchyData[0], hierarchy, None, None, columnSpecificationsPerTag, 0)

    print ('---------------- Setup of hierarchy "' + hierarchyName + '" finished ----------------')

    if createChoiceList:
        print ('---------------- Restart of client required ----------------')

def CreateNewChoiceList(name, list):
    choiceList = acm.FChoiceList()
    choiceList.List = list
    choiceList.Name = name
    choiceList.Commit()
    return choiceList
