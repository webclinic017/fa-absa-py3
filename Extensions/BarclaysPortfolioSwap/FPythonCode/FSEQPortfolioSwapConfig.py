""" Compiled: 2013-11-07 14:33:49 """

"""----------------------------------------------------------------------------
MODULE
    
    FSEQPortfolioSwapConfig

    (c) Copyright 2010 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    Functions that handle leg-, cash flow- and reset-generation for portfolio
    swaps.

----------------------------------------------------------------------------"""
# Customized valuation code should be placed in a module with the name given 
# below.
#----------------------------------------------------------------------------
customValuationModuleName = None
#----------------------------------------------------------------------------
# Two different ways to fix the return resets. Either the total invested value
# is fixed or else the average price.
#----------------------------------------------------------------------------
fixTotalInvested = True
#----------------------------------------------------------------------------
# Additional Payment types that should be transferred from the portfolio to 
# the portfolio swap trade. Custom payment types need to be added to choice 
# list "Additional Payments".
#----------------------------------------------------------------------------
paymentTypes = []
colIdPaymentsPerType = "Portfolio PL Payments Daily"
#----------------------------------------------------------------------------
# Defines wether the funding cost on the night of the expiry day should be
# included in the Portfolio Swap.
#----------------------------------------------------------------------------
includeExpiryDayFunding = False
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
colIdTotalInvested = "Invested Premium"
#----------------------------------------------------------------------------
# Execution Fee
#----------------------------------------------------------------------------
usePerPortfolioExecutionFee = False
colIdDailyExecutionFee = "Portfolio Swap Execution Fees Daily"
#----------------------------------------------------------------------------
# Funding
#----------------------------------------------------------------------------
usePerPortfolioFunding = True
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
# RPL - RPL can be handled as a daily payment added to the portfolio swap
# trade.
#----------------------------------------------------------------------------
usePerPortfolioRPL = False
RPLPaymentType = "Extension Fee"
#----------------------------------------------------------------------------
# Margin leg
#----------------------------------------------------------------------------
useMarginLeg = False
#----------------------------------------------------------------------------
# Dividend UPL stored as daily payments
#----------------------------------------------------------------------------
calculateDivUPL = False
divUPLPaymentType = "UPL Adjustment"
colIdPortfolioSwapDivUPL = "PFS UPL Div Amount"
#----------------------------------------------------------------------------
# In order for not creating unnecessary legs corresponding to securities that
# are no longer traded, this configuration can be used to define which
# column values must be zero on a particular day for the leg to be left out.
# That is, if all the columns below are evaluated to zero for the stock
# portfolio on a given day, there is no need to create legs corresponding to
# the security.
#
# The return fixing column is automatically included.
#----------------------------------------------------------------------------
nonZeroColumnsIds = [colIdPosition, colIdFinancingAmount]
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
