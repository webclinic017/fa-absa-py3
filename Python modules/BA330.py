"""---------------------------------------------------------------------------------------------------------------
Project                 : Client Valuation Project
Purpose                 : Ammended the code to include LegNbr;DayCount;InitialRate fields. Dividend cashflows have 
                          been excluded on TotalReturnSwap. This will feed Exposure Management. 
Department and Desk     : IT - CTB Primary Markets 
Requester               : Phil Ledwaba
Developer               : Tshepo Mabena
CR Number               : 829680 
------------------------------------------------------------------------------------------------------------------"""

import ael, acm, csv, time
from SAGEN_Cashflows import CurrentCF
import SAGEN_Resets, FXRATE
import FSQL_functions

from BA330_trsAmounts import trs_Proj_Amt_Pay, trs_Proj_Amt_Rec, pv_Amount_Pay, pv_Amount_Rec

tradeFilters = [
    'LA_CF_Stocks_1',
    'LA_CF_Stocks_2',
    'LA_CF_Stocks_3',
    'LA_CF_Stocks_4',
    'LA_CF_Stocks_5',
    'LA_CF_Stocks_6',
    'LA_CF_Stocks_7',
    'LA_CF_Stocks_8',
    'LA_CF_Stocks_9',
    'LA_CF_Stocks_10',
    'LA_CF_Stocks_11',
    'LA_CF_Stocks_12',
    'LA_CF_Stocks_13',
    'LA_CF_Stocks_14',
    'LA_CF_Stocks_15',
    'LA_CF_Stocks_16',
    'LA_CF_Stocks_17',
    'LA_CF_Stocks_18',
    'LA_CF_Stocks_19',
    'LA_CF_Stocks_20',
    'LA_CF_Stocks_21',
    'LA_CF_Stocks_22',
    'LA_CF_Stocks_23',
    'LA_CF_Stocks_24',
    'LA_CF_Stocks_25',
    'LA_CF_Stocks_26',
    'LA_CF_Stocks_27',
    'LA_CF_Stocks_28',
    'LA_CF_Stocks_29',
    'LA_CF_Stocks_30',
    'LA_CF_Stocks_31',
    'LA_CF_Stocks_32',
    'LA_CF_Stocks_Delta',
    'LA_CF_BSB_Repos',
    'LA_CF_Bill',
    'LA_CF_CAPFLOOR',
    'LA_CF_CD',
    'LA_CF_CFD_1',
    'LA_CF_CFD_2',
    'LA_CF_CFD_3',
    'LA_CF_Commodity',
    'LA_CF_CredDefSwap',
    'LA_CF_Curr',
    'LA_CF_FRA',
    'LA_CF_FRN',
    'LA_CF_FXCurrSwap',
    'LA_CF_FreeDefCFs',
    'LA_CF_Fut_Fwds',
    'LA_CF_Options',
    'LA_CF_SWAP',
    'LA_CF_Stocks_nonZAR',
    'LA_CF_Warrants',
    'LA_CF_Zero_Index_Bonds',
    'LA_CF_Bonds_1',
    'LA_CF_Bonds_2',
    'LA_CF_Bonds_3',
    'LA_CF_Bonds_4',
    'LA_CF_Bonds_5',
    'LA_CF_Deposit',
    'LA_CF_CurrSwap',
    'LA_CF_Combination',
    'TM',
    'LA_CF_SWAP_test'
]

USDRateDict = acm.FDictionary()
cs = acm.Calculations().CreateStandardCalculationsSpaceCollection()
psIndicator = acm.FDictionary()

def present_val(t, leg, date, ccy, *rest):
        
    pv = 0
    
    insType = t.Instrument().InsType()
    try:
        if insType in ('BuySellback', 'Warrant', 'CFD', 'Stock', 'Future/Forward', 'VarianceSwap', 'Bill', 'Deposit', 'FRN', 'CD',
                                 'Combination', 'FreeDefCF', 'Commodity', 'Cap', 'Floor', 'EquityIndex'):
            pv = ael.Trade[t.Oid()].present_value()
        elif insType in ('Swap', 'IndexLinkedSwap', 'CurrSwap', 'CreditDefaultSwap', 'EquitySwap',
                                    'Repo/Reverse', 'Bond', 'IndexLinkedBond', 'Zero', 'FRA', 'CLN'):
            
            calc = leg.Calculation()
            pv = calc.PresentValue(cs, t).Number()
            
        elif insType in ('TotalReturnSwap'):    
        
            for cf in leg.CashFlows():
            
                cals = cf.Calculation()
                pv   =cals.PresentValue(cs, t).Number()
        
        else:
            pv = ael.Trade[t.Oid()].present_value()
    except Exception, e:
        print 'Present_Val - Error', str(e), ' on trade ', t.Oid()
        #raise
    
    return pv
       
       
def proj_cf(t, leg, date, ccy, *rest):
    pj = 0

    insType = t.Instrument().InsType()
    try:
        if insType in ('BuySellback', 'Warrant', 'CFD', 'Stock', 'Future/Forward', 'VarianceSwap', 'Bill', 'Deposit', 'FRN', 'CD', 
                                 'Combination', 'FreeDefCF', 'Commodity', 'Cap', 'Floor', 'EquityIndex'):
            pj = ael.Trade[t.Oid()].projected_cf(date)
        elif insType in ('Swap', 'IndexLinkedSwap', 'TotalReturnSwap', 'CurrSwap', 'CreditDefaultSwap', 'EquitySwap',
                                    'Repo/Reverse', 'Bond', 'IndexLinkedBond', 'Zero', 'FRA', 'CLN'):
            pj = ael.Leg[leg.Oid()].projected_cf(ael.date_today()) * t.Quantity()
        else:
            pj = ael.Trade[t.Oid()].projected_cf(date)
    except Exception, e:
        print 'Proj_Cf - Error', str(e), ' on trade ', t.Oid()
        #raise
    
    return pj


def delta_fields(t, leg, date, ccy, *rest):
    if leg:
        Curr = leg.Currency().Name()
        InitialRate = 0.0
        if leg.LegType() == 'Fixed':
            RateType = 'Fixed'
            CurrentInt = leg.FixedRate()
            if leg.FixedRate():
                InitialRate = leg.FixedRate()
            else:    
                InitialRate = 0.0
                
        elif leg.LegType() == 'Float':
            if leg.FloatRateReference().Name():
	    	fl_rate = leg.FloatRateReference().Name()
            	if fl_rate in ('ZAR-SAFEX-ON-DEP', 'ZAR-PRIME', 'ZAR-PRIME-1M', 'ZAR-PRIME-3M', 'ZAR-PRIME-77_5', 'ZAR-PRIME-ABSA', 'ZAR-PRIME-AVERAGE', 'ZAR-PRIME-AVERAGE-OPT', 'ZAR-CPI-3M', 'ZAR-CPI-6M'):
                    RateType = 'Variable'
            	else:
	    	    RateType = 'Adjustable'
	    else:
	    	RateType = 'Adjustable'
            CurrentInt = SAGEN_Resets.CurrentReset(1, leg.Oid(), date, 0)
            
            if SAGEN_Resets.CurrentReset(1, leg.Oid(), leg.StartDate(), 0):
                InitialRate = SAGEN_Resets.CurrentReset(1, leg.Oid(), leg.StartDate(), 0)
            else:    
                InitialRate = 0.0
                
        elif leg.LegType() in ('Call Fixed', 'Call Float', 'Call Fixed Adjustable'):
            RateType = 'Variable'
            if leg.FixedRate():
                CurrentInt = leg.FixedRate()
            else:
                CurrentInt = 0.0
        else:
            RateType = 'Non Rate'
            CurrentInt = 0.0
            InitialRate = SAGEN_Resets.CurrentReset(1, leg.Oid(), leg.StartDate(), 0)
                    
        if leg.FloatRateReference():
            fl_rate = leg.FloatRateReference().Name().split('-')
            try:
                DrivingRate = fl_rate[2] + ' ' + fl_rate[1]
            except:
                DrivingRate = leg.FloatRateReference().Name()
        else:
            DrivingRate = ''
        
        #CurrentInt = int(CurrentCF(1, leg.legnbr, date, 5))
        Spread = leg.Spread()
        RepricingFreq = leg.RollingPeriod()    
        NextResetDate = SAGEN_Resets.FirstResetAfter(1, leg.Oid(), date, t.Oid(), 3)
        
        DayCount = leg.DayCountMethod()
        LegNbr = leg.Oid()
    
    Delta_list = {}
    Delta_list['CurrencyNbr'] = Curr
    Delta_list['RateType'] = RateType
    Delta_list['DrivingRate'] = DrivingRate
    Delta_list['CurrentInterest'] = CurrentInt
    Delta_list['Spread'] = Spread
    Delta_list['RepricingFreq'] = RepricingFreq
    Delta_list['NextResetDate'] = NextResetDate
    Delta_list['DayCount'] = DayCount
    Delta_list['LegNbr'] = LegNbr
    Delta_list['InitialRate'] = InitialRate
    
    return Delta_list

def daily_fields(t, leg, date, ccy, *rest):
    
    Date = acm.Time().AsDate(date)
    calc = t.Calculation()
    
    if leg:
        if not USDRateDict.HasKey(leg.Currency()):
            try:
                USDRateDict[leg.Currency()] = FXRATE.FXRate(ael.Instrument[leg.Currency().Name()], date, 'USD')
            except:
                USDRateDict[leg.Currency()] = 1
            
        USDrate = USDRateDict[leg.Currency()]
                
        if t.Instrument().InsType() == ('TotalReturnSwap'):
            if leg.PayLeg():
                Amount = trs_Proj_Amt_Pay(t, Date)
                PV     = pv_Amount_Pay(t, Date)
            else:
                Amount = trs_Proj_Amt_Rec(t, Date)
                PV     =pv_Amount_Rec(t, Date)
        else:
            Amount = proj_cf(t, leg, date, ccy)    
            PV = present_val(t, leg, date, ccy)    
        
    
        AmountUSDEq = Amount * USDrate
        PV_USDEq    = PV * USDrate
    
        if leg.LegType() == 'Fixed':
            CurrentInt = leg.FixedRate()
        elif leg.LegType() == 'Float':
            CurrentInt = SAGEN_Resets.CurrentReset(1, leg.Oid(), date, 0)
        else:
            CurrentInt = 1
            
        lastReset = ael.date(SAGEN_Resets.CurrentReset(1, leg.Oid(), date, 3))        
        if not leg.Resets():            
            acmDate = acm.Time().AsDate(date)
            cashFlow = [cf for cf in leg.CashFlows() if ((cf.StartDate() < acmDate) and (cf.EndDate() >= acmDate) and (cf.CashFlowType() <> 'Fixed Amount'))]
            if cashFlow:            
                lastReset = ael.date(cashFlow[0].StartDate())
        
        days = abs(FSQL_functions.LastDayOfMonth(1, date).days_between(lastReset) / 365.0)
        nominal = 0
        try:
            nominal = calc.Nominal(cs, date).Number()
        except Exception, e:
            print e
        
        AccruedInterest = nominal * (float(CurrentInt)/100.0) * days
        
        LegNbr = leg.Oid()
        '''
        print 'days=', days
        print 'nominal=', nominal
        print 'accrued=', AccruedInterest
        print 'rate=', CurrentInt
        '''
        
        #AccruedInterest = cominal x Fixed/100 x (last day of reporting month   previous reset date)/365 = Accrued Interest receivable;
    
    Daily_list = {}
    Daily_list['AccruedInterest'] = AccruedInterest
    Daily_list['Amount'] = Amount
    Daily_list['Amount_USDEq'] = AmountUSDEq
    Daily_list['PV'] = PV
    Daily_list['PV_USDEq'] = PV_USDEq
    Daily_list['LegNbr'] = LegNbr
    
    return Daily_list


def write_file(name, data, access):
    f = file(name, access)
    c = csv.writer(f, dialect = 'excel-tab')
    c.writerows(data)
    f.close()
  
ael_variables = [['tradeFilter', 'TradeFilter', 'string', tradeFilters, '', 0, 1],
                 ['filePath_day', 'File and Path Daily', 'string', None, 'F:/LA_Cashflow_Daily.tab'],
                 ['filePath_del', 'File and Path Delta', 'string', None, 'F:/LA_Cashflow_Delta.tab'],
                 ['currency', 'Valuation Currency', 'string', 'ZAR', 'ZAR'],
                ['RepDay', 'Date', 'string', None, 'Today', 1],
                 ['takeOn', 'Takeon Delta', 'int', [0, 1], 1]]


def ael_main(ael_dict):
    #filter, path, filename
    #FA_FX .... secondary output code
    filename_day   = ael_dict['filePath_day']
    filename_del   = ael_dict['filePath_del']
    takeOn = ael_dict['takeOn']
        
    output_day = []
    output_del = []
    
    inputDate = ael_dict['RepDay']
    if inputDate == 'Today':
        d = ael.date_today()
    else:
        try:
            d = ael.date_from_string(inputDate, '%Y-%m-%d')
        except:
            d = ael.date_today()

    c = ael_dict['currency']
    #c = 'ZAR'
    
    #file headings
    output_day.append(['Trdnbr', 'LegType', 'LegNbr', 'AccruedInterest', 'Amount', 'Amount_USDEq', 'PV', 'PV_USDEq', 'RepDay'])
    output_del.append(['Trdnbr', 'LegType', 'LegNbr', 'CurrencyNbr', 'RateType', 'DrivingRate', 'CurrentInterest', 'InitialRate', 'Spread', 'RepricingFreq', 'NextResetDate', 'RepDay', 'DayCount'])
    #look at trade 216307
    count = 0
    repDate = d.to_string('%Y-%m-%d')
    ael.log('Running extract for ' + repDate)
    TradeFilters = ael_dict['tradeFilter']
    for tfName in TradeFilters: 
        filter = acm.FTradeSelection[tfName]
        if filter:
            tf = filter.Trades()
            for t in tf:
                delta = 'no'
                if t.Instrument().Legs():
                    for l in t.Instrument().Legs():
                    
                        if l.PayLeg():
                            legtype = 'P'
                        else:
                            legtype = 'S'
                        
                        if not psIndicator.HasKey(t.Oid()):
                            psIndicator.Clear()
                            psIndicator[t.Oid()] = legtype
                        else:
                            if legtype == psIndicator[t.Oid()]:
                                if legtype == 'P':
                                    legtype = 'S'
                                else:
                                    legtype = 'P'    
     
                        if t.Instrument().InsType() == ('TotalReturnSwap'):
                            
                            if not l.FixedCoupon(): 
                                if l.NominalScaling() != 'Dividend':
                                    
                                    if l.PayLeg():
                                        legtype = 'P'
                                    else:
                                        legtype = 'S'
                                    
                                    Day_list = daily_fields(t, l, d, c)
                                    
                                    #if ('%.5f' %float(Day_list['AccruedInterest']) != '0.00000') or ('%.5f' %float(Day_list['Amount']) != '0.00000') or ('%.5f' %float(Day_list['Amount_USDEq']) != '0.00000') or \
                                    #  ('%.5f' %float(Day_list['PV']) != '0.00000') or ('%.5f' %float(Day_list['PV_USDEq']) != '0.00000'):
                                    output_day.append([t.Oid(), legtype, Day_list['LegNbr'], '%.5f' %float(Day_list['AccruedInterest']), '%.5f' %float(Day_list['Amount']), '%.5f' %float(Day_list['Amount_USDEq']), \
                                                '%.5f' %float(Day_list['PV']), '%.5f' %float(Day_list['PV_USDEq']), repDate])
                        else:
                            Day_list = daily_fields(t, l, d, c)
                                                                           
                            if ('%.5f' %float(Day_list['AccruedInterest']) != '0.00000') or ('%.5f' %float(Day_list['Amount']) != '0.00000') or ('%.5f' %float(Day_list['Amount_USDEq']) != '0.00000') or \
                              ('%.5f' %float(Day_list['PV']) != '0.00000') or ('%.5f' %float(Day_list['PV_USDEq']) != '0.00000'):
                                output_day.append([t.Oid(), legtype, Day_list['LegNbr'], '%.5f' %float(Day_list['AccruedInterest']), '%.5f' %float(Day_list['Amount']), '%.5f' %float(Day_list['Amount_USDEq']), \
                                            '%.5f' %float(Day_list['PV']), '%.5f' %float(Day_list['PV_USDEq']), repDate])
                                                
                        if (takeOn) or (ael.date_from_time(t.UpdateTime()) >= d or ael.date_from_time(t.Instrument().UpdateTime()) >= d):
                            #delta = 'yes'
                            if t.Instrument().InsType() == ('TotalReturnSwap'):
                                
                                if not l.FixedCoupon(): 
                                    if l.NominalScaling() != 'Dividend':
                                                                                
                                        Del_list = delta_fields(t, l, d, c) 
                                        
                                        legtype = ''
                                        
                                        if l.PayLeg():
                                            legtype = 'P'
                                        else:
                                            legtype = 'S'
                                        
                                        output_del.append([t.Oid(), legtype, Del_list['LegNbr'], Del_list['CurrencyNbr'], Del_list['RateType'], \
                                            Del_list['DrivingRate'], '%.2f' %float(Del_list['CurrentInterest']), '%.3f' %float(Del_list['InitialRate']), '%.3f' %float(Del_list['Spread']), \
                                            Del_list['RepricingFreq'], ael.date_from_string(Del_list['NextResetDate']).to_string('%Y-%m-%d'), repDate, Del_list['DayCount']])
                            else:
                                
                                Del_list = delta_fields(t, l, d, c) 
                                
                                output_del.append([t.Oid(), legtype, Del_list['LegNbr'], Del_list['CurrencyNbr'], Del_list['RateType'], \
                                        Del_list['DrivingRate'], '%.2f' %float(Del_list['CurrentInterest']), '%.3f' %float(Del_list['InitialRate']), '%.3f' %float(Del_list['Spread']), \
                                        Del_list['RepricingFreq'], ael.date_from_string(Del_list['NextResetDate']).to_string('%Y-%m-%d'), repDate, Del_list['DayCount']])
                                
                count += 1
                        
            
    write_file(filename_day, output_day, 'wb')
    write_file(filename_del, output_del, 'wb')
    ael.log('Wrote secondary output to:::' + filename_day)
    ael.log('Wrote secondary output to:::' + filename_del)
    print 'Complete'

