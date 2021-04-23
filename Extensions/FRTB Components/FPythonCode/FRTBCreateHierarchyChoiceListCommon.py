
import acm, time

def ValidHierarchies(columnName):
    validHierarchies = []
    for hierarchyType in acm.FHierarchyType.Select(''):
        for column in hierarchyType.HierarchyColumnSpecifications():
            if columnName == column.Name():
                validHierarchies.extend(hierarchyType.Hierarchies())
                break
    return validHierarchies

def TimeStamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def ChoiceListFromName(name):
    choiceList = acm.FChoiceList.Select01('name="' + name + '" list="MASTER"', '')
    if not choiceList:
        choiceList = acm.FChoiceList()
        choiceList.List = 'MASTER'
        choiceList.Name = name
        choiceList.Commit()
        print (TimeStamp() + '    "' + name + '"')
    return choiceList

def AddChoiceListItemIfNeeded(list, listValue):
    found = False
    for choice in list.Choices():
        if listValue == choice.Name():
            found = True
            break
    if not found:
        newChoiceList = acm.FChoiceList()
        newChoiceList.List = list
        newChoiceList.Name = listValue
        sortOrder = 0
        if listValue.isdigit():
            #Put integers in correct sort order
            sortOrder = int(listValue)
        elif acm.FCurrency[listValue]:
            #Put currencies last
            sortOrder = 100
        newChoiceList.SortOrder = sortOrder
        newChoiceList.Commit()
        print (TimeStamp() + '    "' + listValue + '"')

def AddChoiceListDataRecursive(hierarchyTree, node, levelColumn, choiceListPerTag):
    for dataValue in node.HierarchyDataValues():
        column = dataValue.HierarchyColumnSpecification()
        dataValue = dataValue.DataValue()
        if (column == levelColumn) and (dataValue in choiceListPerTag):
            AddChoiceListItemIfNeeded(choiceListPerTag[dataValue], node.DisplayName())
    else:                
        children = hierarchyTree.Children(node)
        if children:
            for child in children:
                AddChoiceListDataRecursive(hierarchyTree, child, levelColumn, choiceListPerTag)

def GetLevelColumn(hierarchy):
    levelColumn = None
    for column in hierarchy.HierarchyType().HierarchyColumnSpecifications():
        if 'Level Type' == column.Name():
            levelColumn = column
            break
    if not levelColumn:
        raise Exception('Hierarchy lacks Level Type column.')
    return levelColumn

def DeleteChoiceListData(choiceList, bannedList):
    for c in choiceList.Choices(): 
        if (c.Name() in bannedList) and c.CanBeDeleted():
            print (TimeStamp() + "    Removing " + '"'+c.Name() + '"')
            c.Delete()
