from __future__ import print_function
import acm, FRTBCreateHierarchyChoiceListCommon
import importlib
importlib.reload(FRTBCreateHierarchyChoiceListCommon)

ael_variables = [['Hierarchy', 'Hierarchy', acm.FHierarchy, FRTBCreateHierarchyChoiceListCommon.ValidHierarchies('Liquidity Horizon'), None, 1, 0, 'The Hierarchy where the choice list data is retreived.']]

def ael_main(parameters):
    hierarchy = parameters['Hierarchy']
    hierarchyName = hierarchy.Name()
    print ('---------------- Setup of FRTB hierarchy choice lists for "' + hierarchyName + '" ----------------')

    print (FRTBCreateHierarchyChoiceListCommon.TimeStamp())
    print (FRTBCreateHierarchyChoiceListCommon.TimeStamp() + ' Creating choice lists')
    choiceListPerTag = {
        'Risk Class':FRTBCreateHierarchyChoiceListCommon.ChoiceListFromName('FRTB IMA Risk Class'),
        'Risk Factor Category':FRTBCreateHierarchyChoiceListCommon.ChoiceListFromName('FRTB IMA Category')
    }

    hierarchyTree = acm.FHierarchyTree()
    hierarchyTree.Hierarchy = hierarchy

    levelColumn = FRTBCreateHierarchyChoiceListCommon.GetLevelColumn(hierarchy)

    print (FRTBCreateHierarchyChoiceListCommon.TimeStamp())
    print (FRTBCreateHierarchyChoiceListCommon.TimeStamp() + ' Creating choice list values')
    FRTBCreateHierarchyChoiceListCommon.AddChoiceListDataRecursive(hierarchyTree, hierarchyTree.RootNode(), levelColumn, choiceListPerTag)

    print ('---------------- Setup of FRTB hierarchy choice lists for "' + hierarchyName + '" finished    ----------------')
    print ('---------------- Choice lists created for "' + hierarchyName + '", restart of client required ----------------')
    print ('')
