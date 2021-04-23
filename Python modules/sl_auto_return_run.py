"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Runs the Auto Return process
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Francois Truter
CR NUMBER               :  624338
-----------------------------------------------------------------------------

HISTORY
=============================================================================
Date       Change no Developer          Description
-----------------------------------------------------------------------------
2010-11-16 494829    Francois Truter    Initial Implementation
2010-11-23 502781    Francois Truter    Parameter name changed
2011-04-04 624338    Francois Truter    Added rate column parameter
2012-12-11 620455    Peter Fabian       Use rates stored in Front instead of SBL_Rates file, 
                                        added T+1 .. T+4 to date dropdown + custom date option, 
                                        added internal rate and spread as task parameters 
                                        (these are overwritten by upload script) 
2013-04-02 951379    Peter Fabian       Don't raise exception in case of errors
2015-06-04 2860253   Ondrej Bahounek    Internal rates replaced by external ones in sweeping,
                                        thus some changes here as well.
"""

from sl_process_log import ProcessLog
from sl_process_log import ProcessLogException
import acm
import sl_auto_return


returnDateKey = 'ReturnDateDropdown'
returnDateCustomKey = 'ReturnDate'
positionsKey = 'Positions'
sblPortfolioKey = 'SblPortfolio'
agencyPortfolioKey = 'AgencyPortfolio'
expiryBarrierKey = 'ExpiryBarrierKey'
costBarrierKey = 'CostBarrierKey'
internalRateKey = 'InternalRate'
internalSpreadKey = 'InternalSpread'


calendar = acm.FCalendar['ZAR Johannesburg']
today = acm.Time().DateNow()
Plus1BusinessDay = calendar.AdjustBankingDays(today, 1)
Plus2BusinessDays = calendar.AdjustBankingDays(today, 2)
Plus3BusinessDays = calendar.AdjustBankingDays(today, 3)
Plus4BusinessDays = calendar.AdjustBankingDays(today, 4)

nextBusinessDay = calendar.AdjustBankingDays(today, 1)

customDateKey = 'Custom Date'
returnDateList = {
                   'Next Business Day': nextBusinessDay,
                   customDateKey: today,
                   'Today': today,
                   '+1 Business Day': Plus1BusinessDay,
                   '+2 Business Days': Plus2BusinessDays,
                   '+3 Business Days': Plus3BusinessDays,
                   '+4 Business Days': Plus4BusinessDays,
                   }
returnDateKeys = returnDateList.keys()
returnDateKeys.sort()

def enableCustomDate(index, fieldValues):
    ael_variables[1][9] = (fieldValues[0] == customDateKey)
    return fieldValues


boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()
boolDictDisplay.sort()

# warning: internal rate and spread are updated automatically by script sl_upload_SBL_Rates

# Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
ael_variables = [
    [returnDateKey, 'Return Date', 'string', returnDateKeys, customDateKey, 1, 0, 'Date for which trades must be returned.', enableCustomDate, 1],
    [returnDateCustomKey, 'Return Custom Date', 'date', None, today, 1, 0, 'The date for which trades must be returned.', None, 1],
    [positionsKey, 'Positions', 'FStoredASQLQuery', None, None, 1, 1, 'The Query Folder that returns the positions that are covered.', None, 1],
    [sblPortfolioKey, 'SBL Portfolio', 'FPhysicalPortfolio', None, None, 1, 1, 'The SBL portfolio whose trades will be returned.', None, 1],
    [agencyPortfolioKey, 'Agency Portfolio', 'FPhysicalPortfolio', None, None, 1, 1, 'The agency portfolio whose trades will be returned.', None, 1],
    [expiryBarrierKey, 'Days to One Year Expiry Barrier', 'int', None, 90, 1, 0, 'Trades expiring after this number of days will not be prioritised by exipration date.', None, 1],
    [costBarrierKey, 'Cost Barrier (R)', 'float', None, 50, 1, 0, 'Partial returns with a cost less than this cost barrier will not be returned.', None, 1],
    [internalRateKey, 'Internal Rate', 'float', None, 0.35, 1, 0, 'Internal rate for securities lending.', None, 1],
    [internalSpreadKey, 'Internal Spread', 'float', None, 0.03, 1, 0, 'Spread for securities lending.', None, 1],
    ['exclude_lenders', 'Exclude Lenders', 'FParty', None, None, 0, 1, 'Turn off returns for selected lenders.', None, 1],
    ['exclude_borrowers', 'Exclude Borrowers', 'FParty', None, None, 0, 1, 'Turn off returns for selected borrowers.', None, 1],
]

def ael_main(parameters):
    if parameters[returnDateKey] == customDateKey:
        returnDate = parameters[returnDateCustomKey]
    else:
        returnDate = returnDateList[parameters[returnDateKey]]
    print "Return Date:", returnDate

    positions = parameters[positionsKey][0]
    sblPortfolio = parameters[sblPortfolioKey][0]
    agencyPortfolio = parameters[agencyPortfolioKey][0]
    expiryBarrier = parameters[expiryBarrierKey]
    costBarrier = parameters[costBarrierKey]
    internalRate = parameters[internalRateKey]
    internalSpread = parameters[internalSpreadKey]
    exclude_lenders = [party.Name() for party in parameters['exclude_lenders']]
    exclude_borrowers = [party.Name() for party in parameters['exclude_borrowers']]

    log = ProcessLog('SBL Auto Return')
    log.Information('Exclude lenders: %s' % ', '.join(exclude_lenders))
    log.Information('Exclude borrowers: %s' % ', '.join(exclude_borrowers))
    
    try:
        returner = sl_auto_return.AutoReturn(positions, sblPortfolio, agencyPortfolio, returnDate, 
                                             expiryBarrier, costBarrier, exclude_lenders, exclude_borrowers)
        returner.ReturnTrades(log, internalRate, internalSpread)
    except Exception, ex:
        if not isinstance(ex, ProcessLogException):
            log.Exception(str(ex))
        else:
            print str(ex)
        log.Error("Exception: " + str(ex))
    finally:
        # print log
        log.PrintWarnings()
        log.PrintErrors()
        # warnings are ok
        if not log.GetErrors() and not log.GetExceptions():
            print "Completed Successfully"

