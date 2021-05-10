
import acm

import SACCRParameters

#------------------------------------------------------------------------------
# SA-CCR Commodity Classification
#------------------------------------------------------------------------------
def IsCommodity( instrument ):
    if instrument.IsKindOf( acm.FFuture ) and (instrument.PayType() == "Forward"):
        if instrument.Underlying().Class() in [acm.FCommodity, acm.FCommodityVariant]:
            return True
    
    if instrument.IsKindOf( acm.FAverageForward ):
        underlying = instrument.Legs().First().FloatRateReference()
        
        if underlying:  
            if underlying.Class() in [acm.FCommodity, acm.FRollingSchedule]:
                return True
            else:
                return IsCommodity( underlying )
    
    return False

#------------------------------------------------------------------------------
def HedgingSet( instrument ):
    underlyingCommodity = UnderlyingCommodity( instrument )

    node = FindHierarchyNodeByLevelType( underlyingCommodity, "Hedging Set" )
    return node.DisplayName()

#------------------------------------------------------------------------------
def HedgingSubset( instrument ):
    underlyingCommodity = UnderlyingCommodity( instrument )

    node = FindHierarchyNodeByLevelType( underlyingCommodity, "Hedging Subset" )
    return node.DisplayName()
    
#------------------------------------------------------------------------------
def SACCRSubclass( object ):
    if isinstance( object, str ):
        node = __commodityHierarchyTree.FindChildByName01( object, __commodityHierarchyTree.RootNode() )
    else :
        underlyingCommodity = UnderlyingCommodity( object )
        node = FindHierarchyNodeByLevelType( underlyingCommodity, "Hedging Subset" )
    
    dataValue = __commodityHierarchyTree.DataValueFromColumnName( node, "Subclass" )
    return dataValue.DataValueVA()
    
#------------------------------------------------------------------------------
def UnderlyingCommodity( instrument ):
    underlying = instrument.Underlying()
    
    if instrument.IsKindOf( acm.FAverageForward ):
        underlying =  instrument.Legs().First().FloatRateReference()
    
    if underlying:
        return UnderlyingCommodity( underlying )
    
    return instrument
    
#------------------------------------------------------------------------------
# Supervisory Delta
#------------------------------------------------------------------------------
def SupervisoryDeltaAdjustment( instrument, positionQuantity ):
    return 1 if positionQuantity > 0 else -1

#------------------------------------------------------------------------------
# SA-CCR Commodity Hierarchy
#------------------------------------------------------------------------------
__commodityHierarchy = acm.FHierarchy['SA-CCR Commodity']
__commodityHierarchyTree = acm.FHierarchyTree()
__commodityHierarchyTree.Hierarchy( __commodityHierarchy )

#------------------------------------------------------------------------------
def FindHierarchyLevelType( underlyingCommodity, level ):
    node = __commodityHierarchyTree.FindChildByName01( underlyingCommodity.Name(), __commodityHierarchyTree.RootNode() )
    
    while node:
        dataValue = __commodityHierarchyTree.DataValueFromColumnName( node, "Level Type" )
        
        if dataValue:
            levelType = dataValue.DataValueVA()
            
            if level == levelType:
                return node.DisplayName()
            
        node = __commodityHierarchyTree.Parent( node )

#------------------------------------------------------------------------------
def FindHierarchyNodeByLevelType( underlyingCommodity, level ):
    node = __commodityHierarchyTree.FindChildByName01( underlyingCommodity.Name(), __commodityHierarchyTree.RootNode() )
    
    while node:
        dataValue = __commodityHierarchyTree.DataValueFromColumnName( node, "Level Type" )
        
        if dataValue:
            levelType = dataValue.DataValueVA()
            
            if level == levelType:
                return node
            
        node = __commodityHierarchyTree.Parent( node )
