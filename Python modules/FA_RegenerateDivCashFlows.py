#-----------------------------------------------------------------------------------------------------------------------------------------
#  Developer           : [Tshepo Mabena],[Willie van der Bank],[Willie van der Bank],[Bhavnisha Sarawan],[Bhavnisha Sarawan],[Heinrich Cronje],[Andreas Bayer]
#  Purpose             : [An additional info on the TRS instrument, the add info will be a Boolean to indicate if Special Dividends Excluded. 
#                        If set to yes, then the regeneration must ignore all dividends with ""Spec"" or ""CR"" or ""CR(2)"" or ""Special"" in the free text field.
#                        The module is scheduled to exclude special dividends.],[Ammended with poll() function so that it only has be run once.],[Added
#                        removal of Call Float Rate cashflows],[Included expiry date today and moved the check above regen to prevent expired trades from regenerating],
#                        [Added a date parameter to regen function call to prevent regen of past div cashflows.],[Only Special dididends should be 
#                        removed from the cashflow table with all of its fixed amounts.]
#                        [Dividends should not be generated if Ex div date >= the end date of the last equity cf, i.e. regardless of the total return leg's end date]
#  Department and Desk : [PCG - Secondary Markets Equities],[PCG - Secondary Markets Equities],[PCG],[PCG - Secondary Markets Equities],[PCG],[PCG - Secondary Markets Equities],
#                        [TCU]
#  Requester           : [Marko Milutinovic],[Marko Milutinovic],[Marko Milutinovic],[Marko Milutinovic],[Marko Milutinovic],[Marko Milutinovic],[Irfaan Karim, Brad Stransky]
#  CR Number           : [325393],[C392890 (05/08/2010)],[C423846 (07/09/2010)],[C (19/10/2010)],[C474067 (25/10/2010)],[C513559 (07/12/2010)]
#------------------------------------------------------------------------------------------------------------------------------------------

import acm
import at_time
import FLogger

LOGGER = None
LOG_LEVEL = {'DEBUG': 2, 'INFO': 1, 'WARNING':3, 'ERROR':4}
                            
def regen(trs):
    tr_leg = get_total_return_leg(trs)
    #some old instruments, which have been set up in 2010.2 (without trades)
    #might miss a total return leg
    if tr_leg:
        start_date = at_time.ael_date(tr_leg.StartDate())
    else:
        start_date = None
        
    end_date = at_time.ael_date(get_last_equity_cf_end_date(trs))
    today = at_time.ael_date('TODAY')
    tomorrow = at_time.ael_date('TOMORROW')
    #the second, third, and fourth case are unnecessary in current FA since
    #RegenerateDividendCashFlows would not generate dividend cash flows
    #for dividends with ex date > date_today
    dividends_before_generation = get_dividends(trs)
    if end_date and today != start_date:
        trs.RegenerateDividendCashFlows(today, end_date)
    elif end_date and today == start_date:
        trs.RegenerateDividendCashFlows(tomorrow, end_date)
    elif not end_date and today == start_date:
        trs.RegenerateDividendCashFlows(tomorrow)
    else:
        trs.RegenerateDividendCashFlows(today)
    acm.PollDbEvents()
    dividends_after_generation = get_dividends(trs)

    if len(dividends_after_generation.difference(dividends_before_generation)) > 0:
        LOGGER.LOG('Generated/Updated dividend(s) on instrument %s' % trs.Name())
    
def get_dividends(trs):
    query = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    query.AddAttrNodeString('Leg.Instrument.Name', trs.Name(),  'EQUAL')
    query.AddAttrNodeString('CashFlowType', 'Dividend', 'EQUAL')
    divs = query.Select()
    return set([(div.Oid(), trs.VersionId()) for div in divs])
    
def remove_cashflow(ins, ex_div_day):
    query = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    query.AddAttrNodeString('Leg.Instrument.Name', ins.Name(), 'EQUAL')
    for c in query.Select():
        if c.StartDate() == ex_div_day or c.CashFlowType() in ('Call Fixed Rate', 'Redemption Amount', 'Call Float Rate'):
            try:
                leg = c.Leg()
                leg.CashFlows().Remove(c)
                leg.Commit()
            except:
                LOGGER.ELOG('Cashflow not deleted!')

def remove_special_cashflow(ins, div, comb_link):
    if comb_link:
        weight = comb_link.Weight()
        amount = div.Amount() * weight / comb_link.Owner().IndexFactor()
    else:
        amount = div.Amount()
        
    query = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
    query.AddAttrNodeString('Leg.Instrument.Name', ins.Name(), 'EQUAL')
    for c in query.Select():
        if (c.StartDate() == div.ExDivDay() and abs(round(c.FixedAmount(), 11)) == abs(round(amount, 11))) or c.CashFlowType() in ('Call Fixed Rate', 'Redemption Amount', 'Call Float Rate'):
            try:
                leg = c.Leg()
                leg.CashFlows().Remove(c)
                leg.Commit()
            except:
                LOGGER.ELOG('Cashflow not deleted!')
        
def cash_flow_comparator(cf1, cf2):
    if at_time.to_datetime(cf1.EndDate()) < at_time.to_datetime(cf2.EndDate()):
        return -1
    elif at_time.to_datetime(cf1.EndDate()) > at_time.to_datetime(cf2.EndDate()):
        return 1
    else:
        return 0
    return cash_flow_comparator

def get_total_return_cashflows(trs):
    '''due to incorrect instrument setup in older instruments total return cash flows
    might have been added not only to total return cash flows but also to fixed legs'''
    cash_flows = []
    for leg in trs.Legs():
        for cf in leg.CashFlows():
            if cf.CashFlowType() == 'Total Return':
                cash_flows.append(cf)
    return cash_flows
        
def get_last_equity_cf_end_date(trs):
    cash_flows = get_total_return_cashflows(trs)
    if cash_flows:
        sorted_cash_flows = sorted(cash_flows, cmp = cash_flow_comparator)
        return sorted_cash_flows[-1].EndDate()
    else:
        return None

def get_total_return_leg(trs):
    equity_leg = None
    for leg in trs.Legs():
        if leg.LegType() == 'Total Return':
            equity_leg = leg
            break
    return equity_leg

ael_variables = [
['exclude_instruments', 'Exclude Instruments', acm.FTotalReturnSwap, None, None, 0, 1, '', None, 1],
['log_level', 'Log Level', 'string', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], 'INFO', 1, 0]]

def _init_logging(params):
    global LOGGER
    LOGGER = FLogger.FLogger('TRS Checker')
    LOGGER.Reinitialize(
        level=LOG_LEVEL[params['log_level']], 
        keep=False, 
        logOnce=False, 
        logToConsole=False, 
        filters=None
    )
    return LOGGER

def ael_main(ael_vars):
    LOGGER = _init_logging(ael_vars)
    
    trs_collection = acm.FInstrument.Select("insType='TotalReturnSwap'")
    LOGGER.LOG('%s TRS instruments selected.' % len(trs_collection))
    
    for trs in trs_collection:
        LOGGER.DLOG(trs.Name())
        if trs in ael_vars['exclude_instruments']:
            continue
        if trs.IsExpired():
            continue
        if at_time.to_datetime(trs.ExpiryDate()) >= at_time.to_datetime('TODAY'):
            regen(trs)
            legs = trs.Legs()
            for l in legs:
                if l.LegType() == 'Total Return':
                    if l.PassingType() != 'None':
                        UndIns = l.IndexRef()
                        addinfo = trs.AdditionalInfo().Special_Div_Passing()
                        if addinfo == True:
                            ex_div_day = ''
                            remove_cashflow(trs, ex_div_day)  
                                        
                        elif addinfo == False:
                            query = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
                            query.AddAttrNodeString('Leg.Instrument.Name', trs.Name(), 'EQUAL')
                            #Create Array
                            cashflows = query.Select()
                            cashflows_list = []
                            for cf in cashflows:
                                if cf.CashFlowType() in ('Total Return'):
                                    cashflows_list.append(cf)
                            for cf in cashflows_list:
                                if l.IndexRef():
                                    if l.IndexRef().InsType() in ('Stock'):
                                        
                                        div = acm.FDividend.Select('instrument = "%s"' % UndIns.Name())
                                        for d in div:
                                            if d.ExDivDay() >= cf.StartDate():
                                                if d.Description() in ('SPEC', 'CR', 'CR (2)', 'Special'):
                                                    remove_special_cashflow(trs, d, '')
                                                    
                                    elif l.IndexRef().InsType() in ('EquityIndex'):
                                        query = acm.CreateFASQLQuery(acm.FCashFlow, 'AND')
                                        query.AddAttrNodeString('Leg.Instrument.Name', trs.Name(), 'EQUAL')
                                        
                                        links = l.IndexRef().InstrumentMaps()
                                        for mem in links:
                                            share = mem.Instrument()
                                            div = acm.FDividend.Select('instrument="%s"' % share.Name())
                                            for d in div:
                                                if d.ExDivDay() >= cf.StartDate():
                                                    if d.Description() in ('SPEC', 'CR', 'CR (2)', 'Special'):
                                                        remove_special_cashflow(trs, d, mem)
    LOGGER.LOG('COMPLETED SUCCESSFULLY')
