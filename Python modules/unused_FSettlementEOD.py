""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementEOD - Module which executes the End of Day script for settlements

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module executes the night update of the Settlement table. It
    populates and updates the Settlement table with data from the trade,
    cashflow, payment, account, dividend, reset, party, settle instruction,
    instrument and netting rule tables.

DATA-PREP

REFERENCES
    See modules FSettlementParams and FSettlementGeneral.

----------------------------------------------------------------------------"""
def create_settle_trade(trade, settle_type):
    ''
    FSettlementGeneralRT.create_premium_t(trade, settle_type, 'New', 0)
    return

def create_settlement(trade):
    
    if not FSettlementGeneral.is_valid_instrument(trade.insaddr):
        return
        
    pr = 'Create Settlement(s) for trade %d' % (trade.trdnbr)
    log(1, pr)
    create_settle_trade(trade, 'Premium')
    create_settle_dividend(trade)
    create_addpayment(trade)
    create_settle_cf(trade)
    create_settle_trade(trade, 'Fee')
    FSettlementGeneral2.update_combination_trade(trade, None, 1, trade) #None will cause less cf updates
    FSettlementGeneral2.validate(trade, 'INSERT')
    FSettlementGeneral3.create_settle_future_forward(trade)
    
    
    if trade.insaddr and (trade.insaddr.instype in \
       FSettlementGeneral.ins_security or trade.insaddr.instype in \
       FSettlementGeneral.und_ins_security):
        create_coupon(trade)
    return

def create_coupon(trade):
    sel = ael.Settlement.select('trdnbr=%d' % trade.trdnbr)
    for s in sel:
        if FSettlementGeneral2.check_security([s]):        
            FSettlementGeneral2.update_position_cover(s)
            break
    return

def create_settle_dividend(tr):
    ''

    ins = tr.insaddr
    if ins != None and FSettlementGeneralRT.is_div_related(tr):
        if ins.instype == 'EquitySwap':
            create_equity_swap_dividends_EOD(tr, ins)
        elif ins.instype == 'Combination' and \
        is_combination_with_equityswap(ins):
            FSettlementGeneralRT.create_eq_swap_dividend(tr)
        else:
            sec = FSettlementGeneral2.get_sec_trade(tr.trdnbr)
            if sec:
                if FSettlementGeneral2.check_security([sec]):
                    FSettlementGeneral2.update_position_cover(sec)
    return

def create_addpayment(trade):
    ''

    pay = trade.payments()
    for p in pay:
        FSettlementGeneralRT.create_payment(p, 'New')

    return

def create_settle_cf(trade):
    ''
    cfs = FSettlementGeneralRT.cfs_from_tr(trade)
    for cf in cfs:
        FSettlementGeneralRT.create_cf(cf, trade, 'New')
    return

def create_equity_swap_dividends_EOD(t, i):
    """t is a trade. i is an equity swap instrument. This function retrieves all dividends
    from i, checks whether a settlement record already exists for the dividend,
    and creates a new dividend settlement record if applicable."""
    
    dividend_list = i.historical_dividends()
    
    for d in dividend_list:
    
        found = None
        s_list = ael.Settlement.select('trdnbr = %d' % t.trdnbr)
        
        for s in s_list:
            if s.dividend_seqnbr and s.dividend_seqnbr.seqnbr == d.seqnbr:
                found = s
                break
                
        if not found: #There's no settlement record for this dividend, for trade t.
            if FSettlementGeneral.enter_dividend(t, d) and \
            FSettlementGeneral.paydayOK(d.pay_day, d, 1, ''):
                FSettlementGeneral.dividend_creation(ael.Settlement.new(), d, 'New', 0, t, 1, 0)


def is_combination_with_equityswap(instrument):
    ret = False
    if instrument.instype == 'Combination':
        links = instrument.combination_links()
        for link in links:
            ins = FSettlementGeneral.get_combination_member(link)
            if ins and ins.instype == 'EquitySwap':
                ret = True
                break
    return ret

def check_authorised(param):    
    '''Puts authorised settlements with historic value date to Exception.'''
    global ZoneInfoImported
    if param.authorise_historic_value_day:
        ael.log('End of Day procedure is configured NOT to put Authorised')
        ael.log('settlements with historic value date to Exception.')
        ael.log('authorise_historic_value_day=1')
        return
    iday = ael.enum_from_string('StatusExplanation', 'Historic Value Date')
    sel = ael.Settlement.select()
    for s in sel:
        if s.status=='Authorised':
            ok = s.check_day()
            if not ok:
                clone = s.clone()
                clone.status='Exception'
                clone.status_explanation &=~pow(2, iday)
                clone.commit()
    log(1, 'check_authorised() completed')
    return

def acknowledged_to_pending_closure():
    log(1, 'Changing acknowledged to pending_closure')
    sel = ael.Settlement.select()
    for s in sel:
        if s.status == 'Acknowledged':
            clone = s.clone()
            clone.status = 'Pending Closure'
            clone.commit()
        elif s.status == 'Not Acknowledged':
            clone = s.clone()
            clone.status = 'Exception'
            clone.commit()
    log(1, 'acknowledged_to_pending_closure() completed')
    return

def status_new_to_stp(param):
    'Find possible settlements in status New.\
    Run stp on such in order to do recovery job.'
    
    for setl in ael.Settlement.select():
        if setl.status == 'New':
            pr = "Settlement %d in status New, recovery will be done" % (setl.seqnbr)
            log(1, pr)
            FSettlementSTP.STP(setl, param)
    log(1, 'status_new_to_stp() completed')
    return

def log(level, s):
    return FSettlementGeneral.log(level, s)
    
def eod_start(dict, param):
    
    eod_run = dict['eod_run']
    new_to_stp_run = dict['new_to_stp_run']
    
    if eod_run:    
        pr = "Run End Of Day procedure: %d" % (eod_run)
        log(1, pr)
        pre = len(ael.Settlement.select())
    if new_to_stp_run:
        pr = "Run STP on settlements in status New: %d" % (new_to_stp_run)
        log(1, pr)    
    pr = 'Start time: %s' %  (time.asctime(time.localtime()))
    log(1, pr)

    if param.ZoneInfoImported == 0:
        log(1, 0, FSettlementGeneral2.noZoneinfoMsg())
    
    if eod_run:    
        status_new_to_stp(param) # ok to run during EOD, find todays erroneus settlements
        for status in param.status:
            pr =  'Trade status %s traversed' % (status)
            log(1, pr)
            try:
                selection = ael.Trade.select('status="%s"' % (status))
            except:
                selection = []

            for tr in selection:
                create_settlement(tr)
                try:
                    FSettlementGeneral.commit_transaction()
                except:
                    str = 'Could not commit settlements for trade %d' % tr.trdnbr
                    log(1, str)
                ael.poll()               
                        
        ael.poll()
        acknowledged_to_pending_closure()
        check_authorised(param)

    if new_to_stp_run:
        status_new_to_stp(param)

    pr = 'End time: %s' % (time.asctime(time.localtime()))
    log(1, pr)
    if eod_run:    
        post = len(ael.Settlement.select())
        diff = post - pre
        pr = '%d new Settlements generated' % (diff)
        log(1, pr)
    log(1, ':-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:-:')

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""
try:
    if __name__ == "__main__":
        import sys, getopt

    import ael, time, FSettlementParams, FSettlementGeneral, FSettlementGeneral3
    import FSettlementGeneralRT, FSettlementGeneral2, FSettlementSTP
    param = FSettlementParams.get_default_params()
    ZoneInfoImported = param.ZoneInfoImported
    
    ael_variables = [('eod_run', 'Run End Of Day procedure', 'bool', [False, True], True)]

    def ael_main(dict):
        pr = '<< End of Day - %s >>' % (__file__)
        log(1, pr)
        dict['new_to_stp_run']=False
        eod_start(dict, FSettlementParams.get_default_params())

except Exception, e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    log(1, 'Could not run FSettlementEOD due to ')
    log(1, str(e))



