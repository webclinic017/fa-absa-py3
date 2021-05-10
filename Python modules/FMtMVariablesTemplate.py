""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
    FMtMVariables - Module with variables needed by the FMtMExecute script.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    In this module are some MtM variables that can be chosen by
    the customer.

NOTE
    Please rename the file to FMtMVariables.

----------------------------------------------------------------------------"""
import ael

# Switch on/off the saving of MtM Prices (mainly for test purposes).
Save_MtM_Prices = 1
#Save_MtM_Prices = 0

# Switch on/off the saving of Theoretical Prices.
Save_Theor_Prices = 1
#Save_Theor_Prices = 0

# IgnoreZeroMtMPrice : Ignore storing zero mtm prices
IgnoreZeroMtMPrice=0 # Default off

# For test purpose a list of underlying names can be listed but note: all derivitives
# on these underlyings will be listed
#Test_Underlyings=['ERIC B']
Test_Underlyings=[]


# For best performance turn of check if instruments has trades while
# testing. Or generate mtm prices for all instruments except instype Curr.
#CheckIfTrades=0
CheckIfTrades=1

# Exclude generating MtM prices for the following instypes.
# Some values may be overriden.
ExcludeMtMInstypes=[]

# Generating MtM prices for the following instypes.
# Some values may be overriden.
# NOTE: A listed instype in ExcludeMtMInstypes will be overriden
# by definitions from IncludeMtMInstypes.
# IncludeMtMInstypes=[]
IncludeMtMInstypes=[]

# Switch on/off the saving of prices relevant for historical valuation.
# In addition to traded instruments and their underlyings, prices for
# the following will be stored:
# - Non-traded volatility and yield curve benchmark instruments
# - The full underlying hierarchy of a traded instrument. This includes
#   underlyings of underlyings, members of a combination and delivarable
#   instruments.
# SaveHistoricalValuationPrices = 1
SaveHistoricalValuationPrices = 0

# SaveSEQPrices: If 1, then necessary structured equity valuation parameters
# will be stored. With SEQ 2.3 MtM-prices will be stored otherwise used_price
# will be stored.
# For further information see FCA 1390 - Structured Equity Products
#SaveSEQPrices = 1
SaveSEQPrices = 0

# Choose a settlement market, where MtM Prices should be saved.
Market = 'internal'

# Choose a date on which the MtM prices should be stored. Default is today.
Date = 'Today' # Default
#Date = 'Yesterday'
#Date = '2003-09-01'

# Choose a base currency. This will be the currency against which the MtM
# prices are stored for instruments of type Currency. Default is accounting
# currency.
#BaseCurr = 'USD'

# A price Spread which is substracted from the MtM-price for index warrants.
Spread = 0.00

# SaveBidAndAsk: If 0, no bid or ask prices will be stored, otherwise
# bid and ask prices will be stored.
SaveBidAndAsk = 1

# Rounding, number of decimals. Default is infinite.
#Rounding = 4

# Allow saving 0.01 as MtM price if price is 0.0
#ForcePositiveMtMPrice = 1
ForcePositiveMtMPrice = 0 # Recommended

# Sendmail or not. Receiver will be the recipient of the mail.
#Sendmail = 1 # Send mail
Sendmail = 0 # Do not send mail
#Receiver = 'fred.front@front.com'

# Verbosity: Integer that indicate the level of information that
# will be generated in the AEL console. 0-3
Verb = 1

# Choose if certain instruments mtm-prices should be calculated according
# to own method found in AEL-module MyOwnModule:
CalcMtMPriceForExceptions = 0
#CalcMtMPriceForExceptions = 1  # If CalcMtMPriceForExceptions = 1 you have
    # to set the variable:
    # ExceptionList

# A list of instruments for which the calculation of mtm-prices are taken
# care by the customer.
#ExceptionList = ["CHF/stockindex", "SMI"]

# Choose if Yield Curves should be updated:
UpdateYC = 0
#UpdateYC = 1   # If UpdateYC = 1 you have to set the variable:
    # YieldCurves

# A list of Yield curves has to be specified. These yieldcurves will
# automatically be recalculated with the help of the update_yc()-function
# found in the FMtMGeneral-module.
# Note: It is not possible to recalculate yield curves of type
# Attribute Spread, Instrument Spread or Spread.
#YieldCurves = ["EUR-SWAP", "GBP-SWAP"]
YieldCurves = ["EUR-SWAP", "USD-SWAP", "GBP-SWAP", "CHF-SWAP", "SEK-SWAP",\
    "NOK-SWAP", "JPY-SWAP", "ZAR-SWAP", "DKK-SWAP"]

# If Volatilities should only be recalculated, set RecalcVola to 1:
RecalcVol = 0
#RecalcVol = 1

# A list of Volatility surfaces has to be specified if RecalcVol has been set
# to 1. These Volatilities will automatically be recalculated.
VolSurfaces = []
#VolSurfaces = ["ALSI40_VOLS", "NIKKEI 225 Vols"]
#VolSurfaces = ["EQ/BMW", "EQ/BAY"]

# Choose if Volatilities should be updated:
UpdateVol = 0
#UpdateVol = 1  # If UpdateVol = 1 you have to set the variables:
    # VolMarket
    # AliasTypes OR Distributors
    # Context
    # VolSuffix

# UpdateVolInsTypes: Defines which instypes to include in vol surface 
#UpdateVolInsTypes = ['Option','Warrant']
UpdateVolInsTypes = ['Option']

# Choose if used volatilities for OTC's and Warrants should be updated:
UpdateOTCVol = 0
#UpdateOTCVol = 1       # If UpdateOTCVol = 1 you have to set the variables:
    # VolMarket

# Choose a market where to save volatilities if required.
VolMarket = 'VOLATILITY'

# A list of Alias types OR Price Distributors has to be specified.
# All instruments that have these alias types / distributors set
# will be selected and used in the functions that determine which volatilities
# to be saved.
# Specify:
#AliasTypes = ["EUREX","SAX"]
#AliasTypes = None #Set None if change to Distributors without restarting client
# OR:
#Distributors = ["AMPH_EUREX", "Open Trade", "AMPH_XETRA"]
#Distributors = ["AMPH_XETRA"]
#Distributors = None #Set None if change to AliasType without restarting client

# Volatility suffix.
Base = 'insid'
#Base = 'extern_id2'
VolSuffix = ["_Impvol"]

# SaveVolPrices: Should the calculated volatility points be stored as 
# prices also. If 0 only the volatility surface is updated.
# SaveVolPrices=0
SaveVolPrices=1

# ImpliedVolCutOff: Disgard calculated implied volatilities above this value.
ImpliedVolCutOff=100.0 # => 10000%

# Context.
Context = 'Global'

# If implied Dividend Yield should be calculated from the nearest
# at-the-money cal and put options, and thereafter saved as a Yield Curve.
# NOTE! See MtM documentation how to data prep for this functionality.
CalcImpDivYield = 0
#CalcImpDivYield = 1    # If CalcImpDivYield = 1 you have to set the variables:
    # Underlyings
    # and:
    # AliasTypes
    # OR
    # Distributors
    # unless all options should be searched.

# Specify for which Underlying(s) you want to calculate implied dividend yields.
# All underlying stocks and equity indexes listed will be included.
#Underlyings = ['SUA']
Underlyings = []

# Preferred Markets: A dictionary {ptyid1 : n,ptyid2:n-1,...} of markets
# to prefer a price from. If used instruments with mtm_from_feed set will
# calculate an mtm prices by prefering from prices in order where prices
# with a higher entry is checked first.
# NOTE:
# - Only applied on instrument with flag mtm_from_feed set.
# - If no price thero_price() is NOT calculated.
#
PreferredMarkets={}
#PreferredMarkets={'LIFFE':2,'R_LIFFE' : 1}

# ExcludePreferredInsTypes : A list of instrument types to exclude
# use the above described calculation i.e. use the standard mtm_price_suggest()
ExcludePreferredInsTypes=[]
#ExcludePreferredIntypes=['CurrSwap','FxSwap','Curr','RateIndex','FRN','PromisLoan','Zero','Deposit']

#CASuffixExp: A regulare expression identifying capital adjusted instruments. Normally
# the suffix _caYYYY-MM-DD is added to an adjusted instrument
# CASuffixExp = ''
CASuffixExp = '_ca\d\d\d\d-\d\d-\d\d$'

# SaveDailyCrossRate: A description describing if a fixed daily cross rate should be 
# stored.  The scription is a list of descriptions as shown below.
# Example: [(('GBP','GBX',100.0),['USD'])]
# This exmample means: Store the rate/price in instrument GBP in currency GBX and set prices
# to 100.0. Delete any found price in instrument USD in currency GBX on the corresponding day.
# The date is the mark-to-market date (today/yesterday).
#
#SaveDailyCrossRate =   [(('GBP','GBX',100.0),['USD'])]
SaveDailyCrossRate=[]

# SplitPricePerCurrency: Split theor prices for multicurrency instrument in components out of the 
# currencies. Instrument types are FX Swap and Curr Swap.
SplitPricePerCurrency = 1 # Stores two prices for each currency component
#SplitPricePerCurrency = 0 # Stores on price for the entire instrument. 

# Use Treasury Trader for FX MtM
use_tt_mtm = 0            # If use_tt_mtm = 0 MtM prices from FRONT ARENA are used for FX rates.
#use_tt_mtm = 1           # If use_tt_mtm = 1 MtM prices from Treasury Trader are used for FX rates.
# If FXSwapHasTwoLegs is on in a FRONT ARENA/Treasury Trader integration set this flag to 1.
# Only used when extracting MtM values from Treasurey Trader, i.e. use_tt_mtm = 1.
tt_fx_swap_has_2_legs = 0
#tt_fx_swap_has_2_legs = 1

# Reporting currency for P&L for FX deals comming from Treasury Trader.
# Only used when extracting MtM values from Treasurey Trader, i.e. use_tt_mtm = 1.
tt_reporting_currency = 'USD'