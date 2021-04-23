'''
MODULE
    IM_OdysseyRecon
    
HISTORY
    2013-05-08        Ntuthuko Matthews         Added additional columns (ZAR Cash in ZAR, Other Non ZAR Cash in ZAR) to the report    output
    2013-07-19        Conicov Andrei            Code refactorization and optimisation.
    2013-10-15        Aaeda Salejee             Removing columns ZAR Cash in ZAR, Other Non ZAR Cash in ZAR
    2014-04-04        Godfrey Dire              Added additional columns ('MirrorRef','CounterPortfolioID','CounterPortfolioName','TradeCurrency','BuySellFlag',
                                                                          'ValueDay','ExpiryDate','HValEnd','FXRate') to the report output for FV
    2014-06-18	      Godfrey Dire		Added the GetMirrorTrade function to get the correct mirror trade and Removed the check for Zero values when writting
                                                out the two files, this will make sure that both files have the same number of trades.
    2014-07-10	      Godfrey Dire		Added the following additional columns ('Status','ExecutionTime','Issuer','SMS_CP_SDSID',
                                                'Eagle_SDSID','SMS_LE_SDSID') to the FairValue report. And added the 'Portfolio Accrued Interest' to the NomAcc file.
    2015-05-21        Bhavik Mistry     Seperated Nominal and FairValue runs to optimize run, amended _get_MM_addinfo function for slight performance increase
    2015-06-22        Bhavik Mistry     Added additional logic to Nominal column
    2016-11-14        Bushy Ngwako      Added additional column (Traded_Interest from 'Portfolio Traded Interest' column) to the Nominal Accrued report - ABITFA-4446
'''

import acm, ael, string
from at_time import acm_date, to_datetime

specFund = acm.FAdditionalInfoSpec['Funding Instype']
specMM = acm.FAdditionalInfoSpec['MM_Instype']
specIns = acm.FAdditionalInfoSpec['Instype']
    
def trdfilterList():
    """
    Returns the list of available trade filters
    """
    TradeFilterList = []
    for tf in acm.FTradeSelection.Select(''):
        TradeFilterList.append(str(tf.Name()))
    return TradeFilterList.sort()

def currList():
    """
    Returns the list of available currencies
    """
    CurrencyList = []
    for curr in acm.FCurrency.Select(''):
        CurrencyList.append(str(curr.Name()))
    return CurrencyList.sort()

INCEPTION = ael.date('1970-01-01')
today = ael.date_today()
TODAY = ael.date_today()
FIRSTOFYEAR = TODAY.first_day_of_year()
FIRSTOFMONTH = TODAY.first_day_of_month()
PREVBUSDAY = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1)
TWOBUSDAYSAGO = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2)  
TWODAYSAGO = TODAY.add_days(-2)
YESTERDAY = TODAY.add_days(-1)

StartDateList = {'Inception': INCEPTION.to_string(ael.DATE_ISO), 'First Of Year': FIRSTOFYEAR.to_string(ael.DATE_ISO), 'First Of Month': FIRSTOFMONTH.to_string(ael.DATE_ISO), 'PrevBusDay': PREVBUSDAY.to_string(ael.DATE_ISO), 'TwoBusinessDaysAgo': TWOBUSDAYSAGO.to_string(ael.DATE_ISO), 'TwoDaysAgo': TWODAYSAGO.to_string(ael.DATE_ISO), 'Yesterday': YESTERDAY.to_string(ael.DATE_ISO), 'Custom Date': TODAY, 'Now': TODAY.to_string(ael.DATE_ISO), } 
EndDateList = {'Now':TODAY.to_string(ael.DATE_ISO), 'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO), 'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO), 'Yesterday':YESTERDAY.to_string(ael.DATE_ISO), 'Custom Date':TODAY.to_string(ael.DATE_ISO)}

def _get_calc_space_val(calcSpace, child_tree, column, default=None):
    """
    Calculates the required value using the provide calculation
    space.
    In case of a exception return the provided default value. In case
    of an exception and no default value provided, rethrows the exception.
    """
    try:
        return calcSpace.CalculateValue(child_tree, column, None, False)
    except:
        if default == None:
            raise
        else: 
            return default
 
def _get_MM_addinfo(Trade):
    """
    Returns the trade additional info if one of the following
    exists, in the precise order (only one):
    Funding_Instype, MM_Instype, Instype
    """
  
    if specFund.AddInfo(Trade):
        MM_addinfo = specFund.AddInfo(Trade).FieldValue()
    elif specMM.AddInfo(Trade):
        MM_addinfo = specMM.AddInfo(Trade).FieldValue()
    elif specIns.AddInfo(Trade):
        MM_addinfo = specIns.AddInfo(Trade).FieldValue()
    else:
        MM_addinfo = ''
    
    return MM_addinfo.upper()

    
def _get_formated_value(value, default='', title=None):
    result = default
    if hasattr(value, "Number"):
        result = str("%.5f" % value.Number())
    else:
        print "{0}: {1}".format(title, value)
    return result 
    
def _fx_rate(from_currency, to_currency, date):
    """Obtains FX rate for a certain date.
    
    Parameters:
    from_currency -- str, eg. USD
    to_currency -- str, egk. ZAR
    date -- str, eg. 2012-10-10    
    """

    if (from_currency, to_currency, date) not in _fx_rate._ccy_cache.keys():
        calc_space = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        from_curr = acm.FCurrency[from_currency]
        to_curr = acm.FCurrency[to_currency]
        _fx_rate._ccy_cache[(from_currency, to_currency, date)] = from_curr.Calculation().FXRate(
            calc_space, to_curr, date).Number()
    
    return _fx_rate._ccy_cache[(from_currency, to_currency, date)]


class _FairValueContainer(object):
    """
    Container for the row information for a fair value report
    """
    def __init__(self, trade, calcSpace, childIter, mm_addinfo, mirror_trd, mirror_portid, mirror_portname, exp_dat, zar_amount, f_rate, tply_amt, exec_time, issuer):
        child_tree = childIter.Tree()
        
        self.trdnbr = child_tree.Item().StringKey()
        
        self.ValEnd = _get_calc_space_val(calcSpace, child_tree, 'Total Val End')
        
        self.ValEnd = _get_formated_value(self.ValEnd.Value(), '', 'ValEnd')
        
        self.trade_info = '\t'.join([
            trade.Instrument().StringKey(),
            trade.Instrument().InsType(),
            trade.Instrument().PayType(),
            mm_addinfo,
            trade.Portfolio().StringKey(),
            str(trade.Portfolio().Oid()),
            trade.Counterparty().StringKey(),
            str(trade.Counterparty().Oid()),
            trade.Counterparty().Type(),
            mirror_trd,
            mirror_portid,
            mirror_portname,
            trade.Currency().StringKey(),
            trade.BoughtAsString(),
            str(trade.ValueDay()),
            str(exp_dat),
            str(zar_amount),
            str(f_rate),
            tply_amt,
            trade.Status(),
            exec_time,
            issuer,
            str(trade.Counterparty().AdditionalInfo().BarCap_SMS_CP_SDSID()),
            str(trade.Counterparty().AdditionalInfo().BarCap_Eagle_SDSID()),
            str(trade.Counterparty().AdditionalInfo().BarCap_SMS_LE_SDSID())
        ])
    
    def __str__(self):
        return "{trdnbr}\t{ValEnd}\t{trade_info}".format(trdnbr=self.trdnbr, 
            ValEnd=self.ValEnd, 
            trade_info=self.trade_info
        )
    
    def __repr__(self):
        return self.__str__()

class _NomAccContainer(object):
    """
    Container for the row information for a not fair value report
    """
    def __init__(self, trade, calcSpace, childIter, mm_addinfo):
        child_tree = childIter.Tree()
        self.trdnbr = child_tree.Item().StringKey()
        self.AccruedInt = _get_calc_space_val(calcSpace, child_tree
                                , 'Portfolio Accrued Call Interest', 0.0)
        
        if ((trade.Instrument().InsType() == 'SecurityLoan') or 
            (('Call').upper() in mm_addinfo) or 
            (('Non Zar CFC').upper() in mm_addinfo)): 
            
            self.Nominal = _get_calc_space_val(calcSpace, child_tree, 'Deposit balance')
            self.Accrued = _get_calc_space_val(calcSpace, child_tree
                                               , 'Portfolio Accrued Call Interest', 0.0)
            self.TradedInt = _get_calc_space_val(calcSpace, child_tree
                                               , 'Portfolio Traded Interest')                        
                        
        elif (('IRD Funding').upper() in mm_addinfo):
            self.Nominal = 0.0
            self.Accrued = _get_calc_space_val(calcSpace, child_tree
                                               , 'Accrued Discount Balance')
            self.TradedInt = _get_calc_space_val(calcSpace, child_tree
                                               , 'Portfolio Traded Interest')
            
        else:
            self.Nominal = _get_calc_space_val(calcSpace, child_tree
                                               , 'Current Nominal')
            self.Accrued = _get_calc_space_val(calcSpace, child_tree
                                               , 'Accrued Discount Balance')
            self.AccruedInt = _get_calc_space_val(calcSpace, child_tree
                                               , 'Portfolio Accrued Interest')
            self.TradedInt = _get_calc_space_val(calcSpace, child_tree
                                               , 'Portfolio Traded Interest')
        
        if hasattr(self.Nominal, "Number"):
            self.Nominal = self.Nominal.Number()
        
        if hasattr(self.Accrued, "Number"):
            self.Accrued = self.Accrued.Number()
            
        if hasattr(self.AccruedInt, "Number"):
            self.AccruedInt = self.AccruedInt.Number()
            
        if hasattr(self.TradedInt, "Number"):
            self.TradedInt = self.TradedInt.Number()
            
        try:
            self.Nominal = str(round(self.Nominal, 2))
        except:
            self.Nominal = str(0.0)
    
        try:
            self.Accrued = str(round(self.Accrued, 2))
        except:
            self.Accrued = str(0.0)
            
        try:
            self.AccruedInt = str(round(self.AccruedInt, 2))
        except:
            self.AccruedInt = str(0.0)
            
        try:
            self.TradedInt = str(round(self.TradedInt, 2))
        except:
            self.TradedInt = str(0.0)
        
    def __str__(self):
        return "{trdnbr}\t{Nominal}\t{Accrued}\t{AccruedInt}\t{TradedInt}".format(trdnbr=self.trdnbr
                                           , Nominal=self.Nominal
                                           , Accrued=self.Accrued
                                           , AccruedInt=self.AccruedInt
                                           , TradedInt=self.TradedInt
                                           )
    
    def __repr__(self):
        return self.__str__()
   


'''-----------------------------------------------------------------------------------------------------------'''
ael_variables = \
[
['tradeFilter', 'TradeFilter', 'string', acm.FTradeSelection.Select(''), None],
['path', 'Path', 'string', None, '/services/frontnt/Task/', 0],
['fileName', 'File Name', 'string', None, 'Output.txt', 0],
['type', 'File Type', 'string', ('FairValue', 'Nominal_Accrued'), 'FairValue'],
['currency', 'Valuation Currency', 'string', currList(), 'ZAR'],
['startDate', 'Start Date', 'string', StartDateList.keys(), 'Inception', 0, 0, '', None, 1],
['startDateCustom', 'Start Date Custom', 'string', None, INCEPTION.to_string(ael.DATE_ISO), 0, 0, '', None, 1],
['endDate', 'End Date', 'string', EndDateList.keys(), 'Now', 0, 0, '', None, 1],
['enddateCustom', 'End Date Custom', 'string', None, TODAY.to_string(ael.DATE_ISO), 0, 0, '', None, 1],
]
'''-----------------------------------------------------------------------------------------------------------'''

def ael_main(ael_dict):
    columnId = 'Portfolio Currency'
    tf = acm.FTradeSelection[ael_dict['tradeFilter']]
    # sheetType  = 'FPortfolioSheet'     
    sheetType = 'FTradeSheet'     
    filePath = ael_dict['path'] + ael_dict['fileName']

    f = open(filePath, 'w')
    calcSpace = acm.Calculations().CreateCalculationSpace('Standard', sheetType)
    _fx_rate._ccy_cache = {}

    
    # each type of task must run on diff param overrides.  ACMB Global and CD_MM
    fileType = ael_dict['type']
    if fileType == 'FairValue':
        heading = ['TrdNbr', 'ValEnd', 'InsId', 'Instype', 'PayType', 'Funding_MMInstype', 
            'PortfolioName', 'PortfolioNbr', 'PartyName', 'PartyNbr', 'PartyType', 'MirrorRef',
            'CounterPortfolioID', 'CounterPortfolioName', 'TradeCurrency', 'BuySellFlag',
            'ValueDay', 'ExpiryDate', 'HValEnd', 'FXRate', 'TPLY', 'Status', 'ExecutionTime', 'Issuer',
            'SMS_CP_SDSID', 'Eagle_SDSID', 'SMS_LE_SDSID']
    else:
        heading = ['TrdNbr', 'Nominal', 'Accrued', 'Accrued_Interest', 'Traded_Interest']
    
    heading = '\t'.join(heading)
        
    f.writelines(heading + "\n")

    if ael_dict['startDate'] == 'Custom Date':
        startDate = ael_dict['startDateCustom']
    else:
        startDate = str(StartDateList[ael_dict['startDate']])

    if ael_dict['endDate'] == 'Custom Date':
        endDate = ael_dict['enddateCustom']
    else:
        endDate = str(EndDateList[ael_dict['endDate']])
    
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', startDate)
    calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', endDate)
    calcSpace.SimulateValue(tf, columnId, ael_dict['currency'])
    calcSpace.InsertItem(tf)
    calcSpace.Refresh()
    portfolioIter = calcSpace.RowTreeIterator().FirstChild()  
    childIter = portfolioIter.FirstChild()
    
    print "Iterating WB rows ..."
    while childIter:
        # Front Upgrade 2013: added call to Item() because FTreeProxy.StringKey() returns
        # only 'FTreeProxy' (in prev version it returned the actual trade no)
        trade = childIter.Tree().Item().OriginalTrade()

        mm_addinfo = _get_MM_addinfo(trade)
        
        if fileType == 'FairValue':
            if trade.GetMirrorTrade():
                mirror_trd = str(trade.GetMirrorTrade().Oid())
                mirror_portid = str(trade.GetMirrorTrade().Portfolio().Oid())
                mirror_portname = trade.GetMirrorTrade().Portfolio().StringKey()
            else:
                mirror_trd = ''
                mirror_portid = ''
                mirror_portname = ''
                
            fcurr = trade.Currency().StringKey()
            dt = str(ael.date_today()) 
            f_rate = _fx_rate(fcurr, 'ZAR', dt)

            #Set context, sheet type, column id, and instrument

            column_id = 'Total Val End'

            #Get raw value
            value = calcSpace.CalculateValue( trade, column_id )
            zar_amount_temp = value.Number() * f_rate
            zar_amount = str("%.2f" % zar_amount_temp)
            
            exp_dat_temp  = trade.Instrument().ExpiryDate()
            
            if exp_dat_temp == '':
                exp_dat = ''
            else:
                exp_dat = acm_date(to_datetime(exp_dat_temp))
            
            exec_time = acm_date(to_datetime(trade.ExecutionTime()))
            
            if trade.Instrument().Issuer():
                issuer = trade.Instrument().Issuer().StringKey()
            else:
                issuer =''
                
            #GD Added Total PL Yearly
            column_id = 'Portfolio Total Profit and Loss Yearly'
            
            tply= calcSpace.CalculateValue( trade, column_id )
            tply_amt = str("%.2f" % tply)
        
        try:
            # better let it fail than ignore the error
            if fileType == 'FairValue':
                fValueContainer = _FairValueContainer(trade, calcSpace, childIter, mm_addinfo, mirror_trd, mirror_portid, mirror_portname, exp_dat, zar_amount, f_rate, tply_amt, exec_time, issuer)
                line = fValueContainer
            else:
                nomAccContainer = _NomAccContainer(trade, calcSpace, childIter, mm_addinfo)
                line = nomAccContainer
            
            f.write("{0}\n".format(line))

        except Exception as e:
            print "Exception: {0}".format(e)

        childIter = childIter.NextSibling()

    calcSpace.RemoveSimulation(tf, columnId)
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss Start Date Custom')
    calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
    calcSpace.Clear()
    
    f.close()
    print 'Wrote secondary output to: ', filePath
    print 'completed successfully'
