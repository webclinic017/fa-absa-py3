"""------------------------------------------------------------------------
MODULE
    FClearingBusinessProcessAdaptation -
DESCRIPTION:
    The additionalInfos that need to be set/ trade attributes that need to be set while the business process is associated to a trade can be achieved here.
    Please refer to documentation for further details  
VERSION: 1.0.30
 
--------------------------------------------------------------------------"""
def getResultingClearingStatus(acmTrade):
    """the key of this dictionary is trade status and value is  
    corresponding clearing status that needs to be set for that Trade Status
    The user can use the trade object sent into this function for conditional check 
    and deciding on the instrument type associated to the trade can return dictionary
    for setting trade status
    """   
    tradeNClearingStatus = {'BO Confirmed': 'Agreed'}
    return tradeNClearingStatus

def getClearingProcessDictionary():
    """This values in this dictionary for each workflow mentioned if match found, will be used to set the values on trade"""
    #The attributes that are supported are: cHouse, acquirer, repository, cBroker, middleware
    #The significance of each attribute is as follows:
    #cHouse:      The Clearing House to which trade would be reported for clearing purposes
    #acquirer:    The acquirer of this trade (could be specific on the basis of the Business Process being associated on the trade)
    #repository:  The repository for the trade
    #cBroker:     The clearing broker for the trade
    #middleware:  The middleware for the deal
    clDict = { 
              'LCH.Clearnet': {'cHouse':'LCH.Clearnet','acquirer':'Credit Desk', 'middleware':'MarkitWire', 'repository':'DTCC Copper'},              
              'Bilateral': {'acquirer':'Swap Desk', 'cHouse':'Clearstream', 'cBroker': 'BrokerD'}
              }
    return clDict
