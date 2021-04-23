
import exceptions
import acm

from SACCRSetup import ColumnNames

#-------------------------------------------------------------------------
# Functions used for accessing static SA-CCR data    
#-------------------------------------------------------------------------
def GetAlpha():
    return __ColumnValue(ColumnNames.ALPHA)
    
#-------------------------------------------------------------------------
def GetMultiplierFloor():
    return __ColumnValue(ColumnNames.MULTIPLIER_FLOOR)
    
#-------------------------------------------------------------------------
def GetSupervisoryFactor(*levels):
    levels = [_f for _f in levels if _f]
    return __ColumnValue(ColumnNames.FACTOR, *levels)

#-------------------------------------------------------------------------
def GetCorrelation(*levels):
    levels = [_f for _f in levels if _f]
    return __ColumnValue(ColumnNames.CORRELATION, *levels)

#-------------------------------------------------------------------------
def GetOptionVolatility(*levels):
    levels = [_f for _f in levels if _f]
    return __ColumnValue(ColumnNames.VOLATILITY, *levels)

#-------------------------------------------------------------------------
# Private
#-------------------------------------------------------------------------
__hierarchy = acm.FHierarchy['SA-CCR Parameters']
__hierarchyTree = acm.FHierarchyTree()
__hierarchyTree.Hierarchy(__hierarchy)

#-------------------------------------------------------------------------
def __ColumnValue(columnName, *levels):
    try:
        dataNode = __FindNode(__hierarchyTree.RootNode(), levels)
        dataValue = __hierarchyTree.DataValueFromColumnName(dataNode, columnName)

        return dataValue.DataValueVA()
        
    except SACCRHierarchyNodeException as e:
        acm.Log("Could not find {} in SA-CCR hierarchy: {}".format(columnName, str(e)))
        raise e
        
#-------------------------------------------------------------------------
def __FindNode(parentNode, levels):
    if len(levels) == 0:
        return parentNode
    else:
        nextNode = __hierarchyTree.FindChildByName01(levels[0], parentNode)
    
        if not nextNode:
            raise SACCRHierarchyNodeException('Hierarchy node "{}" cannot be found'.format(levels[0]))
            
        return __FindNode(nextNode, levels[1:])
    
    return nextNode

#-------------------------------------------------------------------------
class SACCRHierarchyNodeException(exceptions.Exception):
    pass
