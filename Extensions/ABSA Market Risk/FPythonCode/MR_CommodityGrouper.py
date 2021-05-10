#grouping: sheet columns/portfoliosheet


"""----------------------------------------------------------------------------
MODULE
    MR_CommodityGrouper - Module that creates groupings

    (c) Copyright 2015 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    This module allows customised groupings on the additional infos. 
    Commodity_Deli and Commodity_SubAsset

----------------------------------------------------------------------------"""

import acm

def Group_Commodity_Deli(self): 

    addInfoForObject = Get_Commodity_AddInfo(self.Instrument())
     
    try:
        commodityDeliValue = addInfoForObject.Commodity_Deli()
        
        if commodityDeliValue == None:
            return "No Commodity Deli"
            
        else:
            return commodityDeliValue
 
    except AttributeError:
        return "No Commodity Deli"

def Group_Commodity_SubAsset(self): 
    
    addInfoForObject = Get_Commodity_AddInfo(self.Instrument())
        
    try:
        commoditySubAssetValue = addInfoForObject.Commodity_SubAsset()
        
        if commoditySubAssetValue == None:
            return "No Commodity SubAsset"
            
        else:
            return commoditySubAssetValue
 
    except AttributeError:
        return "No Commodity SubAsset"
    
def Get_Commodity_AddInfo(ins):
        
        addInfoForObject = None
        
        if ins.InsType() == "Curr" or ins.InsType() == "Deposit":
            addInfoForObject = ins.Currency().AdditionalInfo()
        else:
            addInfoForObject = ins.AdditionalInfo()
        
        return addInfoForObject
    
