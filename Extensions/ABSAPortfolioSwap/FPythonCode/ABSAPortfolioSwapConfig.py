"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapConfig
    
    Created from FSEQPortfolioSwapConfig

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Functions that handle leg-, cash flow- and reset-generation for Portfolio Swaps.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""

# Customized valuation code should be placed in a module with the name given 
# below.
#----------------------------------------------------------------------------
customValuationModuleName = 'ABSAPortfolioSwapCustom'
#----------------------------------------------------------------------------
# Two different ways to fix the return resets. Either the total invested value
# is fixed or else the average price.
#----------------------------------------------------------------------------
fixTotalInvested = True
#----------------------------------------------------------------------------
# Additional Payment types that need to be defined in order for the script to 
# generate payments. See choice list "Additional Payments".
#----------------------------------------------------------------------------
executionFeePaymentType = 'Execution Fee'
divUPLPaymentType = 'UPL Adjustment'
RPLPaymentType = 'RPL'
#----------------------------------------------------------------------------
# Defines wether the funding cost on the night of the expiry day should be
# included in the Portfolio Swap.
#----------------------------------------------------------------------------
includeExpiryDayFunding = True
#----------------------------------------------------------------------------
# When consecutive fixed period portfolio swaps (not open ended) are intended
# the funding in the switch between two swaps may be separated according to 
# calendar months by setting "monthEndAdjustFunding" to True.
#----------------------------------------------------------------------------
monthEndAdjustFunding = False
#----------------------------------------------------------------------------
# Total return
#----------------------------------------------------------------------------
colIdPosition = "Portfolio Profit Loss Period Position"
colIdAveragePrice = "Portfolio Average Price"
colIdTotalInvested = "Portfolio Invested"
#----------------------------------------------------------------------------
# Execution Fee
#----------------------------------------------------------------------------
usePerPortfolioExecutionFee = False
colIdDailyExecutionFee = "Portfolio Fees"
#----------------------------------------------------------------------------
# Funding
#----------------------------------------------------------------------------
usePerPortfolioFunding = False
colIdFinancingAmount = "Portfolio Unfunded Cash"
#----------------------------------------------------------------------------
# Dividend legs
#----------------------------------------------------------------------------
generateDividendLegs = True
colIdInventoryPosition = "Portfolio Inventory"
#----------------------------------------------------------------------------
# Call deposit leg
#----------------------------------------------------------------------------
useCallDepositLeg = False
colIdCallDepositAmount = "Portfolio Accumulated Cash"
colIdDailyCash = "Portfolio Accumulated Cash Daily"
#----------------------------------------------------------------------------
# Repo leg ("None", "Single", "Per Security")
#----------------------------------------------------------------------------
repoLegConfig = "Per Security"
#----------------------------------------------------------------------------
# RPL
#----------------------------------------------------------------------------
usePerPortfolioRPL = False
colIdDailyRPL = None
colIdPaymentsComparisonRule = "PFS paymentsComparisonRuleOverride"
#----------------------------------------------------------------------------
# Margin leg
#----------------------------------------------------------------------------
useMarginLeg = False
#----------------------------------------------------------------------------
# Dividend UPL handled as daily payments
#----------------------------------------------------------------------------
calculateDivUPL = False
colIdPortfolioSwapDivUPL = "PFS UPL Div Amount"
colIdPortfolioDivUPL = "Portfolio PL Period Payments"
#----------------------------------------------------------------------------
# The minimum amount to be stored as a cash flow
#----------------------------------------------------------------------------
cashFlowEpsilon = 1e-6
#----------------------------------------------------------------------------
# Configures the size of data base transaction batches in different stages of 
# swap generation/re-generation. Larger transactions leads to less instrument
# updates. The maximum possible size depends on RAM, data base configuration 
# et.c.
#----------------------------------------------------------------------------
resetBatchSize = 400
cashFlowBatchSize = 400
legBatchSize = 400
resetClearingBatchSize = 200
legClearingBatchSize = 200


