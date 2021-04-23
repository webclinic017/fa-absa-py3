
from __future__ import print_function
import acm
TODAY = acm.Time().DateToday()
DEFAULT_LEG_START = TODAY
DEFAULT_LEG_END = acm.Time().DateAddDelta(TODAY, 0, 1, 0)

def AssignLegCategoryChoiceListEntry(list, entry):
    choice = None
    try:
        choices = acm.FChoiceList[list].Choices()
        idx = choices.FindString(entry)
        if idx > -1:
            choice = choices[idx]
        else:
            raise
    except:
        acm.Log("Not able to assign %s choice list entry %s in PortfolioSwapMetaLegs."%(list, entry))
    return choice

LEG_CATEGORY_FINANCING          = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Financing')
LEG_CATEGORY_PERFORMANCE        = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Performance')
LEG_CATEGORY_PERFORMANCE_UPL    = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Performance UPL')
LEG_CATEGORY_PERFORMANCE_RPL    = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Performance RPL')
LEG_CATEGORY_STOCK_BORROW       = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Stock Borrow')
LEG_CATEGORY_SYNTHETIC_CASH     = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Synthetic Cash')
LEG_CATEGORY_FEE                = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Fee')
LEG_CATEGORY_DIVIDEND           = AssignLegCategoryChoiceListEntry( 'Leg Category', 'Dividend')

def IsFinancingChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_FINANCING

def IsPerformanceChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_PERFORMANCE
    
def IsPerformanceUPLChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_PERFORMANCE_UPL

def IsPerformanceRPLChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_PERFORMANCE_RPL

def IsStockBorrowChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_STOCK_BORROW

def IsSyntheticCashChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_SYNTHETIC_CASH
    
def IsFeeChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_FEE
    
def IsDividendChoiceListItem(choiceListItem):
    return choiceListItem and choiceListItem == LEG_CATEGORY_DIVIDEND
    
#----------------------------------------------------------------------------
def StockSelectQuery(freeDefCFInstr):
    return "insType = 'Stock' and currency = '" + freeDefCFInstr.Currency().Name() + "'"

def RateIndexSelectQuery(freeDefCFInstr):
    return "insType = 'RateIndex' and currency = '" + freeDefCFInstr.Currency().Name() + "'"

def CreateDefaultLegs():
    freeDefCFInstr = acm.DealCapturing().CreateNewInstrument("FreeDefCF")
    freeDefCFInstr.OpenEnd = 'Open End'
    
    stockSelectQ = StockSelectQuery(freeDefCFInstr)
    rateIndexSelectQ = RateIndexSelectQuery(freeDefCFInstr)
    
    try:
        defaultStock = acm.FInstrument.Select(stockSelectQ).First()
    except:
        print ('Cannot create Meta Legs - No valid default Stock available in ADS')
        
    try:
        defaultFloatRateRef = acm.FInstrument.Select(rateIndexSelectQ).First()
    except:
        print ('Cannot create Meta Legs - No valid Rate Index available in ADS')
    

    CreateNewPerformanceMetaLeg(freeDefCFInstr, defaultStock)
    CreateNewPerformanceRPLMetaLeg(freeDefCFInstr, defaultStock)
    CreateNewPerformanceUPLMetaLeg(freeDefCFInstr, defaultStock)
    CreateNewStockBorrowMetaLeg(freeDefCFInstr)
    CreateNewSyntheticCashMetaLeg(freeDefCFInstr, defaultFloatRateRef)
    CreateNewFinancingMetaLeg(freeDefCFInstr, defaultFloatRateRef)
    CreateNewFeeMetaLeg(freeDefCFInstr)
    
    return freeDefCFInstr

def FindMetaLegByType(freeDefCFInstr, category):
    for leg in freeDefCFInstr.Legs():
        if leg.CategoryChlItem() == category:
            return leg
    return None
        
def AddMissingMetaLegs(freeDefCFInstr):
    missingLegs = False
    if not FindMetaLegByType(freeDefCFInstr, LEG_CATEGORY_STOCK_BORROW):
        missingLegs = True
        CreateNewStockBorrowMetaLeg(freeDefCFInstr)
    if not FindMetaLegByType(freeDefCFInstr, LEG_CATEGORY_SYNTHETIC_CASH):
        missingLegs = True
        CreateNewSyntheticCashMetaLeg(freeDefCFInstr)
    if not FindMetaLegByType(freeDefCFInstr, LEG_CATEGORY_FINANCING):
        missingLegs = True
        defaultFloatRateRef = acm.FInstrument.Select(RateIndexSelectQuery(freeDefCFInstr)).First()
        CreateNewFinancingMetaLeg(freeDefCFInstr, defaultFloatRateRef)
    if not FindMetaLegByType(freeDefCFInstr, LEG_CATEGORY_PERFORMANCE):
        missingLegs = True
        selectQ = StockSelectQuery(freeDefCFInstr)
        defaultStock = acm.FInstrument.Select(selectQ).First()
        CreateNewPerformanceMetaLeg(freeDefCFInstr, defaultStock)
    if not FindMetaLegByType(freeDefCFInstr, LEG_CATEGORY_PERFORMANCE_RPL):
        missingLegs = True
        selectQ = StockSelectQuery(freeDefCFInstr)
        defaultStock = acm.FInstrument.Select(selectQ).First()
        CreateNewPerformanceRPLMetaLeg(freeDefCFInstr, defaultStock)
    if not FindMetaLegByType(freeDefCFInstr, LEG_CATEGORY_PERFORMANCE_UPL):
        missingLegs = True
        selectQ = StockSelectQuery(freeDefCFInstr)
        defaultStock = acm.FInstrument.Select(selectQ).First()
        CreateNewPerformanceUPLMetaLeg(freeDefCFInstr, defaultStock)
    if not FindMetaLegByType(freeDefCFInstr, LEG_CATEGORY_FEE):
        missingLegs = True
        CreateNewFeeMetaLeg(freeDefCFInstr)
    return missingLegs
    
def CreateNewStockBorrowMetaLeg(freeDefCFInstr):
    legType  = "Fixed"
    resetType = 'None'
    isPayLeg = False
    security = None
    nominalScalingType = "Position Total"
    nominalScalingPeriod = "1d"
    passingType = "None"
    floatRateReference = None
    floatRateFactor = 0.0
    category = LEG_CATEGORY_STOCK_BORROW
    resetPeriod = "0d"
    resetDayOffset = 0
    generateSpreadFixings = True
    
    AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings)
  
def CreateNewPerformanceMetaLeg(freeDefCFInstr, defaultStock):
    legType  = 'Position Total Return'
    resetType = 'Return'
    isPayLeg = False
    security = defaultStock
    nominalScalingType = "None"
    nominalScalingPeriod = "0d"
    passingType = "Dividend Payday"
    floatRateReference = defaultStock
    floatRateFactor = 0.0
    category = LEG_CATEGORY_PERFORMANCE
    resetPeriod = "0d"
    resetDayOffset = -1
    addPassingData = True
    generateSpreadFixings = False
    
    AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings, addPassingData)
   
def CreateNewPerformanceRPLMetaLeg(freeDefCFInstr, defaultStock):
    legType  = 'Position Total Return'
    resetType = 'Return'
    isPayLeg = False
    security = defaultStock
    nominalScalingType = "None"
    nominalScalingPeriod = "0d"
    passingType = "Dividend Payday"
    floatRateReference = defaultStock
    floatRateFactor = 0.0
    category = LEG_CATEGORY_PERFORMANCE_RPL
    resetPeriod = "0d"
    resetDayOffset = -1
    addPassingData = True
    generateSpreadFixings = False
    
    AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings, addPassingData)
   
def CreateNewPerformanceUPLMetaLeg(freeDefCFInstr, defaultStock):
    legType  = 'Position Total Return'
    resetType = 'Return'
    isPayLeg = False
    security = defaultStock
    nominalScalingType = "None"
    nominalScalingPeriod = "0d"
    passingType = "None"
    floatRateReference = defaultStock
    floatRateFactor = 0.0
    category = LEG_CATEGORY_PERFORMANCE_UPL
    resetPeriod = "0d"
    resetDayOffset = -1
    addPassingData = False
    generateSpreadFixings = False
    
    AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings, addPassingData)
   
def CreateNewSyntheticCashMetaLeg(freeDefCFInstr, defaultFloatRateRef=None):
    if defaultFloatRateRef == None:
        defaultFloatRateRef = acm.FInstrument.Select(RateIndexSelectQuery(freeDefCFInstr)).First()
    legType  = 'Call Float'
    resetType = 'Weighted'
    isPayLeg = False
    security = None
    nominalScalingType = "None"
    nominalScalingPeriod = "0d"
    passingType = "None"
    floatRateReference = defaultFloatRateRef
    floatRateFactor = 1.0
    category = LEG_CATEGORY_SYNTHETIC_CASH
    resetPeriod = "1d" #Should this be possible to set
    resetDayOffset = 0
    generateSpreadFixings = False
    addPassingData = False
    reinvest = True

    AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings, addPassingData, reinvest)
  
  
def CreateNewFinancingMetaLeg(freeDefCFInstr, defaultFloatRateRef):
    legType  = "Float"
    resetType = 'Simple Overnight'
    isPayLeg = True
    security = None
    nominalScalingType = "Position Total"
    nominalScalingPeriod = "1d"
    passingType = "None"
    floatRateReference = defaultFloatRateRef
    floatRateFactor = 1.0
    category = LEG_CATEGORY_FINANCING
    resetPeriod = "1d" #Simple Overnight implies 1d
    resetDayOffset = 0
    generateSpreadFixings = True

    AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings)

def CreateNewFeeMetaLeg(freeDefCFInstr):
    legType  = 'Payment'
    resetType = 'None'
    isPayLeg = True
    security = None
    nominalScalingType = 'None'
    nominalScalingPeriod = "0d"
    passingType = 'None'
    floatRateReference = None
    floatRateFactor = 0.0
    category = LEG_CATEGORY_FEE
    resetPeriod = '0d'
    resetDayOffset = 0
    generateSpreadFixings = False

    AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings)


def AddNewLeg(freeDefCFInstr, legType, resetType, isPayLeg, security, nominalScalingType, nominalScalingPeriod, passingType, floatRateReference, floatRateFactor, category, resetPeriod, resetDayOffset, generateSpreadFixings, addPassingData = False, reinvest = False):
    newLeg = freeDefCFInstr.CreateLeg(isPayLeg)
    newLeg.RegisterInStorage()
    newLegDeco = acm.FBusinessLogicDecorator.WrapObject(newLeg)

    newLegDeco.Leg().LegType = legType
    newLegDeco.Leg().PayLeg = isPayLeg
    newLegDeco.Leg().IndexRef = security
    newLegDeco.Leg().FloatRateReference = floatRateReference
    newLegDeco.Leg().FloatRateFactor = floatRateFactor
    newLegDeco.Leg().NominalFactor = 1.0
    newLegDeco.Leg().StartDate = DEFAULT_LEG_START
    newLegDeco.Leg().EndDate = DEFAULT_LEG_END
    newLegDeco.Leg().Currency = freeDefCFInstr.Currency()
    newLegDeco.Leg().PayCalendar = freeDefCFInstr.Currency().Calendar()
    newLegDeco.Leg().ResetCalendar = freeDefCFInstr.Currency().Calendar()
    newLegDeco.Leg().NominalScaling = nominalScalingType
    newLegDeco.Leg().NominalScalingPeriod = nominalScalingPeriod
    newLegDeco.Leg().Spread = 0.0
    newLegDeco.Leg().Spread2 = 0.0
    newLegDeco.Leg().DayCountMethod = 'ACT/360'
    newLegDeco.Leg().ResetDayMethod = 'Following'
    newLegDeco.Leg().PayOffset = '0d'
    newLegDeco.Leg().PayDayMethod = 'Following'
    newLegDeco.Leg().PassingType = passingType
    newLegDeco.Leg().CategoryChlItem = category
    newLegDeco.Leg().ResetType = resetType
    newLegDeco.Leg().RollingPeriod = '0d'
    newLegDeco.Leg().ResetPeriod = resetPeriod
    newLegDeco.Leg().ResetDayOffset = resetDayOffset
    newLegDeco.GenerateSpreadFixings(generateSpreadFixings)
    if addPassingData and not newLegDeco.PassingData():
        passingData = newLegDeco.CreatePassingData()
        passingData.PassInReturnCurrency(True)
        passingData.IncludeTaxFactor('None')
    newLegDeco.Leg().Reinvest = reinvest

        
def RemoveStockBorrowMetaLeg(freeDefCFInstr):
    _RemoveMetaLegOfType(freeDefCFInstr, LEG_CATEGORY_STOCK_BORROW)
        
def RemovePerformanceMetaLeg(freeDefCFInstr):
    _RemoveMetaLegOfType(freeDefCFInstr, LEG_CATEGORY_PERFORMANCE)
        
def RemovePerformanceUPLMetaLeg(freeDefCFInstr):
    _RemoveMetaLegOfType(freeDefCFInstr, LEG_CATEGORY_PERFORMANCE_UPL)
        
def RemovePerformanceRPLMetaLeg(freeDefCFInstr):
    _RemoveMetaLegOfType(freeDefCFInstr, LEG_CATEGORY_PERFORMANCE_RPL)

def RemoveSyntheticCashMetaLeg(freeDefCFInstr):
    _RemoveMetaLegOfType(freeDefCFInstr, LEG_CATEGORY_SYNTHETIC_CASH)
            
def _RemoveMetaLegOfType(freeDefCFInstr, type):
    leg = FindMetaLegByType(freeDefCFInstr, type)
    if leg:
        freeDefCFInstr.Legs().Remove(leg)
        leg.Unsimulate()
