from __future__ import print_function
import acm
import FLogger

logger = FLogger.FLogger.GetLogger("FAlgoMonitor -")

#--------------------------------------------
#                EVENTS        
#--------------------------------------------
def showAlgoMonitorButtons(invokationInfo):

    grouperRow = getGrouperRow(invokationInfo)
    if grouperRow:
        grouperOnRootLevel = grouperRow.GrouperOnRootLevel()
        if grouperOnRootLevel:
            rootGrouperName = str(grouperOnRootLevel.DisplayName())
            if rootGrouperName:
                if  "Marketplace / Algo Id" == rootGrouperName or "Algo Id" == rootGrouperName:
                    return True
    return False
    

#--------------------------------------------
def onEnableAlgoButton(invokationInfo):
    updateAlgoStatus(invokationInfo, "enable")

#--------------------------------------------
def onBlockAlgoButton(invokationInfo):
    updateAlgoStatus(invokationInfo, "block")

#--------------------------------------------
def onKillAlgoButton(invokationInfo):
    updateAlgoStatus(invokationInfo, "kill")
        

#--------------------------------------------
#                 ACTIONS        
#--------------------------------------------

def updateAlgoStatus(invokationInfo, status):

    shell = invokationInfo.Parameter('shell')
    
    warningText = "Are you sure you want to "+status+" "
    reason = "User wants to "+status+" the algo"
    
    algoIdList = getAlgoIdList(invokationInfo, shell, warningText)
    marketInfo = getMarketInfo(invokationInfo)

    for algoId in algoIdList:
        UpdateAlgosStatusRequest(shell, marketInfo, algoId, status, reason)

#--------------------------------------------
def UpdateAlgosStatusRequest(shell, marketInfo, algoId, requested_status, reason):
    
    logStr = reason +" "+str(algoId)+" on "+marketInfo
    logger.LOG( 'UpdateAlgosStatusRequest: %s' % logStr)
    
    completion = acm.Trading.CreateCommandCompletion(shell, 'Algo Status')
    target_strategies = getTargetStrategies(algoId, marketInfo)
    
    if requested_status   == "enable":
        acm.AlgorithmicTrading.EnableAlgos( target_strategies, reason, completion)           
        
    elif requested_status == "block":
        acm.AlgorithmicTrading.BlockAlgos( target_strategies, reason, completion)       
    
    elif requested_status == "kill":
        acm.AlgorithmicTrading.KillAlgos( target_strategies, reason, completion)       

#--------------------------------------------
#                 UTILS        
#--------------------------------------------
def getGrouperRow(invokationInfo):

    rowObject = None
    cell = invokationInfo.Parameter("Cell")
    button = invokationInfo.Parameter('ClickedButton')
    if cell:
        try:
            rowObject = cell.RowObject()
        except:
            pass
    elif button:
        try:
            rowObject = button.RowObject()
        except:
            pass
            
    if rowObject and rowObject.IsKindOf(acm.FGroupingOrder):
        return rowObject
        
    return None
    
    
#--------------------------------------------
def getTargetStrategies(algoId, marketInfo):

    target_strategies = acm.FArray()
    all_strategies = acm.FAlgoTradingStrategies.Instances() 
    
    for s in all_strategies:
        strategy = s.StrategyFromRegulatoryId(algoId)
        if strategy:
            if marketInfo == "ALL_MARKETS" or marketInfo == strategy.StrategySource():
                print ("Strategy name for AlgoId", algoId, " is ", strategy, " on ", strategy.StrategySource())
                target_strategies.Add(strategy)
            
    return target_strategies
            
            
#--------------------------------------------
def addAlgoIdToList(grouperRow, algoIdList):

    algoID = grouperRow.GroupingValue()
    if algoID:
        print ("Adding "+str(algoID)+" to algo list")
        algoIdList.Add(algoID)
        
        
#--------------------------------------------
def populateAlgoIdList(grouperRow, grouperName, algoIdList):
    
    if "Algo Id" == grouperName and grouperRow.GroupingValue() is not None:
        return addAlgoIdToList(grouperRow, algoIdList)
        
    else:
        memberRows = grouperRow.OwnOrders()
        if memberRows:
            for membRow in memberRows:
                if membRow.IsKindOf(acm.FGroupingOrder):
                    membRowGrouperName = str(membRow.GrouperOnLevel().DisplayName())
                    populateAlgoIdList(membRow, membRowGrouperName, algoIdList)               
    
    
#--------------------------------------------
def getAlgoIdList(invokationInfo, shell, warningText):

    algoIdList = acm.FArray()    
    grouperRow = getGrouperRow(invokationInfo)
    
    if grouperRow:

        grouperName = str(grouperRow.GrouperOnLevel().DisplayName())
        msgBoxText = warningText+"algo(s) listed on and under this level"

        if acm.UX().Dialogs().MessageBoxOKCancel(shell, 3, msgBoxText) == 'Button1':
            populateAlgoIdList(grouperRow, grouperName, algoIdList)

    return algoIdList
    
#--------------------------------------------
def getMarketInfo(invokationInfo):

    marketPlace="ALL_MARKETS"    
    grouperRow = getGrouperRow(invokationInfo)
    
    if grouperRow:
        grouperName = ""
        parentGrouperName = ""
        
        grouper = grouperRow.GrouperOnLevel()
        parentGrouper = grouperRow.GrouperOnParentLevel()
        
        if grouper:
            grouperName = str(grouper.DisplayName())
            #print ("grouper:", grouperName)
            
            if grouperName == "Marketplace":
                marketPlace = grouperRow.GroupingValue()
                return marketPlace.Id()
            
        if parentGrouper:
            parentGrouperName = str(parentGrouper.DisplayName())
            #print ("parentGrouper:", parentGrouperName)
        
            if parentGrouperName == "Marketplace":
                marketPlace = grouperRow.GroupingValueAtParent()
                return marketPlace.Id()
        
    return marketPlace
