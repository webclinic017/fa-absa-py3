"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Runs sweeping process with a query folder as input 
                           for the positions
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  524194
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-03-11 243997    Francois Truter    Initial Implementation
2010-03-15 254192    Francois Truter    Added partial sweeping option
2010-11-16 494829    Francois Truter    Added CFD option
2010-12-14 524194    Francois Truter    Allocate held positions
2011-04-04 619099    Francois Truter    Added rate column parameter
2012-10-23 620455    Peter Fabian       Use rates stored in Front instead of SBL_Rates file, 
                                        added T+1 business day to date dropdown + custom date option, 
                                        added internal rate and spread as task parameters 
                                        (these are overwritten by upload script)
2015-06-04 2860253   Ondrej Bahounek    Internal rates replaced by external ones.
                                        Add external rates' spreads.
"""

import acm
import sl_sweeping
from sl_rates import SblTimeSeriesRates
from sl_process_log import ProcessLog
from sl_process_log import ProcessLogException
from sl_auto_return_run import internalRateKey, internalSpreadKey

instrumentsKey = 'instruments'
cfdSweepKey = 'CfdSweep'
sweepDateKey = 'SweepDateDropdown'
sweepDateCustomKey = 'SweepDate'
positionsKey = 'Positions'
sblPortfolioKey = 'SblPortfolio'
validationKey = 'ValidationKey'
allowPartialSweepingKey = 'AllowPartialSweeping'
allocateHeldPositionsKey = 'AllocateHeldPositions'
customDateKey = 'Custom Date'
buySpreadKey = 'BuySpread'
sellSpreadKey = 'SellSpread'

validation = 'Validation Mode'
sweeping = 'Sweeping Mode'

calendar = acm.FCalendar['ZAR Johannesburg']
today = acm.Time().DateNow()
nextBusinessDay = calendar.AdjustBankingDays(today, 1)

sweepDateList = {
                   'Next Business Day': nextBusinessDay,
                   customDateKey: today,
                   'Today': today,
                   }
sweepDateKeys = sweepDateList.keys()
sweepDateKeys.sort()

def enableCustomDate(index, fieldValues):
    ael_variables[2][9] = (fieldValues[1] == customDateKey)
    return fieldValues

boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

# warning: internal rate and spread are updated automatically by script sl_upload_SBL_Rates

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [cfdSweepKey, 'CFD Sweep', 'string', boolDictDisplay, 'No', 1, 0, 'Are these CFD positions being swept', None, 1],
    [sweepDateKey, 'Sweep Date', 'string', sweepDateKeys, customDateKey, 1, 0, 'The date for which positions must be swept.', enableCustomDate, 1],
    [sweepDateCustomKey, 'Sweep Custom Date', 'date', None, today, 1, 0, 'The date for which positions must be swept.', None, 1],
    [positionsKey, 'Positions Filter', 'FStoredASQLQuery', None, None, 1, 1, 'The Query Folder that returns the positions to be swept', None, 1],
    [instrumentsKey, 'Instrument', 'FInstrument', None, None, 0, 1, 'The instrument to run the script for. Leave blank for all instruments from Positions Filter.', None, 1],
    [sblPortfolioKey, 'SBL Portfolio', 'FPhysicalPortfolio', None, None, 1, 1, 'The SBL portfolio to where there will be borrowed, and from where there will be lent', None, 1],
    [validationKey, 'Run', 'string', [validation, sweeping], validation, 1, 0, 'Run a validation (no trades booked) or start sweeping (trades booked)', None, 1],
    [allowPartialSweepingKey, 'Allow Partial Sweeping', 'string', boolDictDisplay, 'No', 1, 0, 'Should partial sweeping of short positions be allowed or skipped', None, 1],
    [allocateHeldPositionsKey, 'Allocate Held Positions', 'string', boolDictDisplay, 'No', 1, 0, 'Should postions marked as held be completely allocated', None, 1],
    [internalRateKey, 'Internal Rate', 'float', None, 0.35, 1, 0, 'Internal rate for securities lending.', None, 1],
    [internalSpreadKey, 'Internal Spread', 'float', None, 0.03, 1, 0, 'Spread for securities lending.', None, 1],
    [buySpreadKey, 'Buy Spread', 'float', None, 0.05, 1, 0, 'Spread for buy SL trades.', None, 1],
    [sellSpreadKey, 'Sell Spread', 'float', None, 0.02, 1, 0, 'Spread for sellSL trades.', None, 1],
]

def ael_main(parameters):
    cfdSweep = boolDict[parameters[cfdSweepKey]]

    if parameters[sweepDateKey] == customDateKey:
        sweepDate = parameters[sweepDateCustomKey]
    else:
        sweepDate = sweepDateList[parameters[sweepDateKey]]
    print "Sweep Date:", sweepDate

    positionsQueryFolder = parameters[positionsKey][0]
    sblPortfolio = parameters[sblPortfolioKey][0]
    validationMode = True
    if parameters[validationKey] == sweeping:
        validationMode = False
    allowPartialSweeping = boolDict[parameters[allowPartialSweepingKey]]
    allocateHeldPositions = boolDict[parameters[allocateHeldPositionsKey]]

    internalRate = parameters[internalRateKey]
    internalSpread = parameters[internalSpreadKey]
    buySpread = parameters[buySpreadKey]
    sellSpread = parameters[sellSpreadKey]
        
    instruments = [i.Name() for i in parameters[instrumentsKey]]
    
    log = ProcessLog('SBL Sweeping')

    try:
        sl_rates = SblTimeSeriesRates(log, internalRate, internalSpread, buySpread, sellSpread)
        sweeper = sl_sweeping.SblSweeper(sweepDate, positionsQueryFolder,
                    sblPortfolio, cfdSweep, log, validationMode, allowPartialSweeping, 
                    sl_rates, allocateHeldPositions, instruments)
        sweeper.Sweep()
    except Exception, ex:
        if not isinstance(ex, ProcessLogException):
            log.Exception(str(ex))
        else:
            print str(ex)
    finally:
        print log
     
