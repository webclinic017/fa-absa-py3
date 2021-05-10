"""-----------------------------------------------------------------------------
PROJECT                 :  N/A
PURPOSE                 :  Sweeps bond positions into a specified portfolio
DEPATMENT AND DESK      :  FIXED INCOME
REQUESTER               :  Kelly Hattingh
DEVELOPER               :  Francois Truter
CR NUMBER               :  549170
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2010-06-28 355193    Francois Truter           Initial Implementation
2010-08-26 412608    Francois Truter           Added Valuation Group parameter
2011-01-18 549170    Francois Truter           Added bid and offer adjustments
2019-03-05 CHG1001472203	 Delsayo Lukhele		   Added function generate_cm_task
"""

import acm
import FRunScriptGUI
import cm_BuySellBackProcess

inputFileKey = 'InputFile'
tradeFilterKey = 'TradeFilter'
portfolioKey = 'Portfolio'
startDateKey = 'StartDate'
endDateKey = 'EndDate'
valGroupKey = 'ValuationGroup'
bidAdjustmentKey = 'BidAdjustment'
offerAdjustmentKey = 'OfferAdjustment'

fileSelection = FRunScriptGUI.InputFileSelection("CSV Files (*.csv)|*.csv|All Files (*.*)|*.*||")
defaultTradeFilter = acm.FTradeSelection['Bonds Spot']
defaultPortfolio = acm.FPhysicalPortfolio['JOB12']
t2 = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(acm.Time().DateNow(), 2)
t3 = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(acm.Time().DateNow(), 3)
valuationGroupList = acm.FChoiceList.Select("list = 'ValGroup'").SortByProperty('Name')
defaultValuationGroup = acm.FChoiceList.Select01("list = 'ValGroup' and name = 'AC_GLOBAL_Bonds'", 'More than one Valuation Group returned with name AC_GLOBAL_Bonds')

#Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [inputFileKey, 'Rates File', fileSelection, None, fileSelection, 1, 1, 'The CSV file from which the bid and offer rates will be read', None, 1],
    [tradeFilterKey, 'Counterparty Trade Filter', 'FTradeSelection', None, defaultTradeFilter, 1, 1, 'The Trade Filter that returns the positions to be swept', None, 1],
    [portfolioKey, 'Acquiring Portfolio', 'FPhysicalPortfolio', None, defaultPortfolio, 1, 1, 'The portfolio that will be acquiring the instruments', None, 1],
    [startDateKey, 'Start Date', 'date', None, t2, 1, 0, 'The start date of the Buy Sell-Backs that will be booked', None, 1],
    [endDateKey, 'End Date', 'date', None, t3, 1, 0, 'The end date of the Buy Sell-Backs that will be booked', None, 1],
    [valGroupKey, 'Valuation Group', 'string', valuationGroupList, defaultValuationGroup, 1, 0, 'The Valuation Group for the trades to be booked.', None, 1],
    [bidAdjustmentKey, 'Bid Adjustment', 'float', None, 0.15, 1, 0, 'The rate by which short positions will adjusted', None, 1],
    [offerAdjustmentKey, 'Offer Adjustment', 'float', None, 0.10, 1, 0, 'The rate by which long positions will adjusted', None, 1]
]

def ael_main(parameters):
    inputFile = parameters[inputFileKey]
    tradeFilter = parameters[tradeFilterKey][0]
    portfolio = parameters[portfolioKey][0]
    startDate = parameters[startDateKey]
    endDate = parameters[endDateKey]
    valGroupStr = parameters[valGroupKey]
    bidAdjustment = parameters[bidAdjustmentKey]
    offerAdjustment = parameters[offerAdjustmentKey]
    
    valGroup = acm.FChoiceList.Select01("list = 'ValGroup' and name = '%s'" % valGroupStr, 'More than one Valuation Group returned with name %s' % valGroupStr)
    
    processor = cm_BuySellBackProcess.CapMarketBuySellBack(inputFile.SelectedFile().Text(), tradeFilter, portfolio, startDate, endDate, valGroup, bidAdjustment, offerAdjustment)
    processor.run()
    
def generate_cm_task(self):
    acm.RunModuleWithParameters('cm_BuySellBackProcess_run', 'Standard' )
