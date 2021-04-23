""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE
    FCAGeneral - Module including all functions common to Corporate Actions.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module stores those functions which are common to several Corporate
    Action modules.
----------------------------------------------------------------------------"""

import ael
import FCARollback

try:
    import string
except ImportError:
    print 'Could not find the module string' 
try:
    import math
except ImportError:
    print 'Could not find the module math' 
from FCAMisc import *

import FCAVariables
Auto_Cancel         = FCAVariables.Auto_Cancel_Premiums

"""----------------------------------------------------------------------------
FUNCTION
    logme - Function which logs information to file or console.

DESCRIPTION
    The log and logfile variables have to be set if logging to file
    should be used. If these variables are not sett logging to console
    will take place. 

ARGUMENTS
    string     string     Text to be logged
----------------------------------------------------------------------------"""

def close_log(lf):
    """Function which closes the log after all has been written to it."""
    lf.close()
    return lf

try:
    from FCAVariables import log, logfile
except ImportError:
    print 'Define a logfile if you want to log to file. Logging will '\
        'be done to console.' 

def logme(string):
    """Log to file or console."""
    
    try:
        lf = open(logfile, 'a')
        console = 0
    except TypeError:
        console = 1
    except NameError:
        console = 1
    except IOError:
        console = 1
        print 'Logfile location not found. Logfile =', logfile
    if log == 1 and console != 1:
        lf.write(string)
        lf.close()
    else:
        print string

"""----------------------------------------------------------------------------
FUNCTION
    switch_curr - Function which returns amount in other currency.

DESCRIPTION

ARGUMENTS
    string     string     Text to be logged
----------------------------------------------------------------------------"""

def switch_curr(verb, ca, entity, amount, date, curr):
    """Function which returns amount in other currency."""

    if ca.cash_curr not in (None, 'None') and ca.cash_amount not in (0.0, 
                                                                    'None'):
        try:
            fx_rate = entity.used_price(date, curr)
            if verb:
                s = 'Exchange rate used:%f\nCash before:%f\nCash after:%f'\
                    % (fx_rate, amount, amount / fx_rate)
                logme(s)
            return amount / fx_rate
        except ZeroDivisionError:
            s = 'ZeroDivisionError, not possible to convert Amount into'\
                ' correct currency. Will continue without converting. '\
                'Fx rate:%f' % fx_rate
            logme(s)
            return amount
    else:
        return amount

"""----------------------------------------------------------------------------
FUNCTION
    user - Function which checks if the necessary user and party exist.

DESCRIPTION
    The User and the Party FMaintenance have to be defined. The Party 
    FMaintenance is automatically created by the function, but the user has to
    be manually created.

ARGUMENTS
    commit     Int     Number: enable commit to database = 1
    
RETURNS
    Values of the variables ca_user, ca_trader and ca_acquirer
----------------------------------------------------------------------------"""

def user(commit = 1):
    """Assign user and party names."""
    
    u = ael.User['FMAINTENANCE']
    
    if not u:
        u = ael.User['CORPACTION']
        if not u:
            s = '\nA user called FMaintenance has to be defined.'
            logme(s)
            raise s
    ca_user   = u
    ca_trader = u

    party = ael.Party['FMAINTENANCE']
    if party:
        if party.type == 'Intern Dept':
            return ca_user, ca_trader, party
        else:   
            p = party.clone()
    else:
        p = ael.Party.new()
        p.ptyid = 'FMAINTENANCE'
    p.type = 'Intern Dept'
    if commit:
        try:
            p.commit()
        except RuntimeError:
            raise 'RuntimeError. One reason could be that your ADS user do '\
                  'not have the rights to create or update the party.'\
                  'The easiest solution is probably to manually create a '\
                  'party with ptyid "FMaintenance" and type "Intern Dept".'
    ca_acquirer = p
    return ca_user, ca_trader, ca_acquirer
    
def prfid(p):
    if p:
        return p.prfid
    else:
        return 'none'

"""----------------------------------------------------------------------------
FUNCTION
    check_if_in_trd_filter - Filters out trades based on trade filter.

DESCRIPTION
    If a trade filter and a selection of trades based on an instrument is 
    passed, a list with trade entities will be returned including all trades
    in the instrument which are included in the trade filter.
    
ARGUMENTS
    verb    int     Logging switched on or off
    filter  entity  A trade filter
    trades_in_ins   selection   A selection based on an instrument
----------------------------------------------------------------------------"""

def check_if_in_trd_filter(verb, filter, trades_in_ins):
    """Filters out trades based on trade filter."""

    flt = {}
    ins = {}
    trd = []
    for f in filter.trades():
        flt[f] = f.trdnbr
    for i in trades_in_ins:
        ins[i] = i.trdnbr
        
    if verb:
        s = 'Match %s with %s.' % (flt.values(), ins.values())
        logme(s)

    for t in flt.keys():
        if t in ins.keys():
            trd.append(t)
    return trd

"""----------------------------------------------------------------------------
FUNCTION
    position - Calculates the total position and avg_price per
    instrument/portfolio.

DESCRIPTION
    This function creates a dictionary with each portfolio containing trades in
    the instrument for which a Corporate Action is to be performed. For each
    portfolio, the position and the average price is saved in the dictionary.

ARGUMENTS
    debug       Int     Number: debug = 1
    trades      Entity  Trade record
    rec_date    Date    Record Date
    pf          String  Portfolio specified when starting module FCAExecute
    acc_method  String  Accounting Method specified in FCAExecute

RETURNS
    pos     Dictionary  The keys are portfolios, the values are position and
                        price.
----------------------------------------------------------------------------"""

def position(debug, trades, rec_date, pf, acc_method, ComparisonDate = None):
    """Creates dictionary with portfolios and their positions."""
    ### Find correct currency for the avg_price calculation:
    try:
        from FCAVariables import Curr
    except ImportError, msg:
        if string.rfind(msg, 'Curr') != -1:
            Curr = None
        else:
            raise
    if Curr == 'PortfolioCurr' and trades[0].prfnbr and \
        trades[0].prfnbr.curr: # Portfolio currency is preferred.
        pfcurr = 1
    else:
        pfcurr = 0
    if Curr == 'InstrumentCurr' and trades[0].insaddr.curr:
        Curr = trades[0].insaddr.curr # Instrument currency is preferred.
        inscurr = 1
    else:
        inscurr = 0
    if Curr in (None, 'PortfolioCurr'):
        Currid = ael.used_acc_curr()
        Curr = ael.Instrument[Currid]
    
    pos = {}
    price = {}

    ### Calculate avg_price for the whole position, accross portfolios:
    try:
        ap = ael.avg_price(trades, rec_date, Curr, acc_method, 3)
    except TypeError:
        if acc_method:
            ap = ael.avg_price(trades, rec_date, Curr, acc_method)
        else:
            accError = 'Acc_Method has to be specified in FCAVariables.'
            raise accError
            
    if debug:
        s = '\nAverage Price of total position, all portfolios: %f'\
            '\nCurr used to calculate AvgPrice: %s' % (ap, Curr.insid)
        logme(s)

    for t in trades:
        quantity = t.quantity

        ### Check if the portfolio of this trade is already in the
        ### dictionary.
        if pos.has_key(t.prfnbr):
            oldq, oldp = pos[t.prfnbr]
        else:
            oldq, oldp = 0, 0
        pos[t.prfnbr] = oldq + quantity, 0

        if price.has_key(t.prfnbr):
            oldtrade = price[t.prfnbr]
        else:
            oldtrade = []
        oldtrade.append(t)
        price[t.prfnbr] = oldtrade
    
    ### "price" is a dictionary of portfolios as keys and Trades on which to
    ### calculate average price as a list within the dictionary:
    ### {<portf entity>: [<Trd entity1>, <Trd entity2>], <portf entity2>: []}
    for i in price.values(): ### Average Price calculation per instr & portf.
        if debug:
            for t in i:
                s = '\nTrdnbr: %i, Pf: %s, Price: %f, Qty: %f, Curr: %s' %\
                    (t.trdnbr, prfid(t.prfnbr), t.price, t.quantity, 
                    t.curr.insid)
                logme(s)
        ### Calculate avg_price per each portfolio position:
        try:
            if inscurr == 1:
                pass
            elif pfcurr == 1 and i[0].prfnbr and inscurr == 0:
                Curr = i[0].prfnbr.curr
            else:
                if debug:
                    s = 'Will use Accounting Currency for this position, '\
                  'since no other currency has been defined. '\
                    'Trade(s) may not belong to any portfolio, %s' % Curr.insid
                    logme(s)        
            p = ael.avg_price(i, rec_date, Curr, acc_method, 3) 
        except TypeError:
            if acc_method:
                p = ael.avg_price(i, rec_date, Curr, acc_method)
            else:
                accError = 'Acc_Method has to be specified in FCAVariables.'
                raise accError
        if debug:
            s = '\n=> Average Price of %s in portfolio %s: %f Used Curr: %s\n'\
                % (trades[0].insaddr.insid, prfid(i[0].prfnbr), p, Curr.insid)
            logme(s)
        
        for k in pos.keys():
            if k == i[0].prfnbr:
                oldq, oldp = pos[k]
                pos[k] = oldq, p
                
    if pf:
        ### "pos" is a dictionary of portfolios as keys and as values a tuple
        ### consisting of the position quantity and average price.
        if pos.values():
            q = 0
            for i, j in pos.values(): ### Sum up total quantity.
                q = q + i
            if q != 0:
                if pos.has_key(pf):     
                    pos[pf] = pos[pf][0], ap, q
                else:
                    pos[pf] = 0 , ap, q
                
    if debug:
        s = 'Finally in position-dictionary (zero positions will not be '\
            'adjusted):'
        logme(s)
    for k in pos.keys():
        if debug:
            s = '%s %s' % (prfid(k), pos[k])
            logme(s)
        if pos[k][0] == 0:
            del pos[k]
    return pos

"""----------------------------------------------------------------------------
FUNCTION
    create_trade - Function which creates new trades.

DESCRIPTION
    This function is used to create trades as decided in the module FCAExecute.
    Depending on if a portfolio has been elected on the command line, or in the
    macro variables window, the position is opened in the chosen
    portfolio. Otherwise trades are created in the portfolios where the
    original positions were found. The exception is for Close Out and Open Up
    trades, which are always created in the portfolios where the original
    position was found.  The price is calculated in FCAExecute and just passed
    on to this function, where it is adjusted depending on the instrument's
    Quote Type.
    
ARGUMENTS
    verb        Int     Number: enable verbose / information printouts = 1
    commit      Int     Number: commit = 1 to commit db changes
    debug       Int     Number: debug = 1
    pp          Int     Number: pp = 1 to see db records
    ca          Entity  A record in the Corporate Action table
    ins         Entity  A record in the Instrument table            
    pf          String  A portfolio name (prfid)
    rec_date    Date    Date which will become the trade's value day and
                        acquire day
    trdtype     String  Type of trade, e.g. 'Closing' or 'Normal'
    q           Float   The quantity of the trade
    p           Float   The price of the trade
    var1        String  The Corporate Action type, only used when necessary

RETURNS
    e           Entity  New equity trade entity
----------------------------------------------------------------------------"""

def create_trade(verb, commit, debug, pp, ca, ins, pf, rec_date,
                 trdtype, q, p, var1):
    """Create new trade."""
    ca_user, ca_trader, ca_acquirer = user(commit = commit)
    
    if q != 0.0:
        try:
            e = ael.Trade.new(ins)
        except:
            e = None
            s = '\nException due to ael.Trade.new(ins) not possible in '\
                'FCAGeneral.create_trade.'
            logme(s)
        e.prfnbr = pf

        try:
            from FCAVariables import Curr
        except ImportError, msg:
            if string.rfind(msg, 'Curr') != -1:
                Curr = None
            else:
                raise
        if Curr == 'PortfolioCurr' and e.prfnbr and e.prfnbr.curr:
            e.curr = e.prfnbr.curr
        elif Curr == 'InstrumentCurr' and ins.curr:
            e.curr = ins.curr
        else:
            Currid = ael.used_acc_curr()
            e.curr = ael.Instrument[Currid]

        e.value_day = rec_date
        e.acquire_day = rec_date
        if trdtype == 'Closing':
            e.time = rec_date.add_days(1).to_time() - 3
        else:
            e.time = rec_date.add_days(1).to_time() - 1
        
        if e.prfnbr and e.prfnbr.owner_ptynbr:
            e.acquirer_ptynbr = e.prfnbr.owner_ptynbr
        else:
            e.acquirer_ptynbr = ca_acquirer
        e.counterparty_ptynbr = ca_acquirer
        e.trader_usrnbr = ca_trader
        e.updat_usrnbr = ca_user
        e.status = 'FO Confirmed'
        e.type = trdtype
        
        ### Note! When creating trades, quantity must be updated.
        if e.type == 'Closing':
            e.quantity = -q
        elif ca == None:
            e.quantity = q
        elif ca.trade_quantity_dec == -1:
            e.quantity = q
        else:
            if ca.trade_quantity_dec == 0:
                e.quantity = int(q)
            else:
                e.quantity = round(q, ca.trade_quantity_dec)
        
        if (ca == None or ca.trade_price_dec == -1):
            e.price = p
        else:
            e.price = round(p, ca.trade_price_dec)
            
        ### Added for Cash trades:
        if ins.instype == 'FreeDefCF':
            e.quantity = -q * p
            e.price = 100

        if var1 == 'Conversion':
            e.price = 100
        try:
            if ca.cash_curr not in (None, 'None')\
                and ca.cash_amount not in (0.0, 'None'):
                fx_rate = e.curr.used_price(ca.ex_date, ca.cash_curr.insid)
                if verb:
                    s = 'Exchange rate used:%f\nCash before:%f\nCash after:%f'\
                        % (fx_rate, var1, var1 / fx_rate)
                    logme(s)
                var1 = var1 / fx_rate
            e.price = e.price - var1 / e.quantity
        except AttributeError, msg:
            pass
        except TypeError, msg:
            pass
        except ZeroDivisionError:
            s = 'ZeroDivisionError, not possible to convert Cash Amount into'\
                ' Cash Currency. Will continue without converting. Fx rate:%f'\
                % fx_rate
            logme(s)
        e.premium = e.premium_from_quote(rec_date, e.price)
        
        try:
            import FCACustomization
            FCACustomization.fill_in_trade_keys(e, ca)
        except ImportError:
            pass

        if pp: logme(e.pp())
        if e.quantity == 0.0:
            s = 'WARNING! Trade quantity cannot be zero. '\
                'Trade will not be created.'
            logme(s)
        else:
            if commit:
                e.commit()

        ### This is used to add Additional cash for the Close method:
        if var1 not in (None, 0.0, 0, 'None'):
            try:
                cash = float(var1)
                p = ael.Payment.new(e)
                p.payday = ca.record_date
                p.amount = cash
                p.curr = e.curr
                try:
                    if ca.cash_curr not in (None, 'None')\
                        and ca.cash_amount not in (0.0, 'None'):
                        p.curr = ca.cash_curr
                        p.amount = cash * fx_rate
                except AttributeError:
                    pass
                if pp: logme(p.pp())
                if commit: p.commit()
                if verb:
                    s = '\nAdditional Payment: %f\nCurr: %s' % (p.amount, 
                        p.curr.insid)
                    logme(s)
            except ValueError:
                pass

        if pf: prfid = pf.prfid
        else: prfid = 'None'
        if verb:
            s = '\nTrade: %i \nInsid: %s \nPortfolio: %s \nQuantity: %f'\
                '\nPrice: %f \nPremium: %f \nContrSize: %f\nCurr: %s' \
                % (e.trdnbr, ins.insid, prfid, e.quantity, e.price, e.premium,
                   e.insaddr.contr_size, e.curr.insid)
            logme(s)
        return e
        
def checkStatus(t):
    if t.status in ('Void', 'Confirmed Void', 'Simulated', 'Terminated'):
        s = '\nWill not update any of Void, Confirmed Void, Simulated, '\
            'or Terminated trades. Skip trdnbr %i' % t.trdnbr
        logme(s)
        return 0
    else:
        return 1

"""----------------------------------------------------------------------------
FUNCTION
    update_trade - Function which changes trade price and / or quantity.

DESCRIPTION
    The fields quantity and / or price are updated to the price * factor and
    quantity/factor. For Eurex derivatives updates, the Trade quantity is never
    adjusted.
        
ARGUMENTS
    commit      Int         Number: commit = 1 to commit db changes
    debug       Int         Number: debug = 1
    ca          Entity      A record in the Corporate Action table
    trd         Entity      A record in the Trade table     
    rb          Instance    Collector of information about rollbacks
    factor      Float       Price/Quantity changing factor
    adj_trd_q   Int         Number: To adjust trade quantity, ajd_trd_q = 1

RETURNS
    rb          Instance    Information about rollbacks
----------------------------------------------------------------------------"""

def update_trade(commit, verb, ca, trd, rb, factor, adj_trd_q, 
                  adj_trd_p = 2, var1 = None, cs = 0.0):
    """Update trades in the trade table."""
    
    if adj_trd_p == 2:
        adj_trd_p = ca.adj_trade_price
    
    diff = 0.0 #Not recognised as diff even if var1=diff in passage of argument
        
    ca_user, ca_trader, ca_acquirer = user(commit = commit)
    if checkStatus(trd): 
        t = trd.clone()
        if factor == 1:
            change_in_trade = 0 # There will only be a Payment
        else:
            change_in_trade = 1 # As opposed to Payment
            old_premium = t.premium
            t.updat_usrnbr = ca_user
            if trd.acquirer_ptynbr \
                and trd.acquirer_ptynbr.type == 'Intern Dept':
                rb.add('Update', t, ['price', 'quantity', 'premium'])
            else:
                t.acquirer_ptynbr = ael.Party['FMaintenance']
                rb.add('Update', t, ['price', 'quantity', 'premium', 
                'acquirer_ptynbr'])

            if adj_trd_p:
                if ca.trade_price_dec != -1:
                    t.price = round(t.price * factor, ca.trade_price_dec)
                else:
                    t.price = t.price * factor
            if adj_trd_q:
                if ca.trade_quantity_dec != -1:
                    if ca.trade_quantity_dec == 0:
                        t.quantity = math.floor(t.quantity / factor)
                    else:
                        t.quantity = round(t.quantity / factor, 
                            ca.trade_quantity_dec)
                else:
                    t.quantity = t.quantity / factor
            t.premium = t.premium_from_quote(ca.record_date, t.price)
            if ca.ca_type in ('New Issue', 'Stock Dividend', 'Buyback', 
                'Spin-off') and ca.new_insaddr not in (0, None):
                pass # No rounding effect, premiums should not add up.
            else:
                new_prem = t.premium
                if commit == 0:
                    if t.insaddr.quote_type in ('Per Unit', 'Per 100 Units'):
                        new_prem = -1 * t.price * t.quantity * cs
                diff = old_premium - new_prem
                if verb:
                    s = '\nDiff calculation: %f - %f = %f'\
                        % (old_premium, new_prem, diff)
                    logme(s)

        ### This is used to add Rounding cash for the Close method,
        ### or Additional cash for the Adjust method:
        if var1 not in (None, 0.0, 0, 'None'):
            try:
                cash = float(var1)
                p = ael.Payment.new(t)
                p.payday = ca.record_date
                p.amount = cash
                p.curr = t.curr
                try:
                    if ca.cash_curr not in (None, 'None')\
                        and ca.cash_amount not in (0.0, 'None'):
                        if change_in_trade: # Implying Additional cash,
                                            # not Rounding cash.
                            switch_cash = switch_curr(verb, ca, ca.cash_curr, 
                                cash, ca.ex_date, t.curr.insid)
                            p.amount = switch_cash
                            p.curr = ca.cash_curr
                except AttributeError, msg:
                    pass
                if commit: p.commit()
                if change_in_trade: # Otherwise trade will be deleted, 
                                    # and a payment update is unnecessary.
                    rb.add('Update', p, ['paynbr'])
                if verb:
                    s = '\nAdditional Cash Payment: %f\nCurr: %s' % (p.amount,
                        p.curr.insid)
                    logme(s)
            except ValueError:
                pass
                
        ### This is used to add Rounding cash for the Adjust method.
        ### Exceptions: Rounding cash is never added for Spin-offs, 
        ### Stock Dividend, New Issue or Buyback.
        if diff != 0.0 and Auto_Cancel:
            try:
                d = ael.Payment.new(t)
                d.payday = t.value_day
                # To keep trade premium and cash on same date.
                d.amount = diff
                d.curr = t.curr
                if commit: d.commit()
                rb.add('Update', d, ['paynbr']) # We know the trade is changed
                if verb:
                    s = '\nAdditional Diff Payment: %f\nCurr: %s' % (d.amount,
                        d.curr.insid)
                    logme(s)
            except ValueError:
                pass

        if commit:
            t.commit()

        if verb and adj_trd_p:
            s = '\nUpdated Trade: Trdnbr %s \nOld Price %f -> New Price %f'\
                '\nOld Qty %f -> New Qty %f \nOld Prem %f -> New Prem %f'\
                % (t.trdnbr, trd.price, t.price, trd.quantity, t.quantity,
            trd.premium, t.premium)
            logme(s)
    return rb

"""----------------------------------------------------------------------------
Rounding
NOTE: gui_cash should be the total amount of cash, that is cash * quantity.
----------------------------------------------------------------------------"""
def prem_diff(commit, verb, ca, trd, prem1, prem2, adj_cash, prem3):
    """Find out if premiums cancel, add cash payment if not."""

    if Auto_Cancel:
        diff = prem1 + (prem2 + adj_cash + prem3)
        if verb:
            s = 'Diff calculation: %f +(%f + %f + %f) =%f'\
                % (prem1, prem2, adj_cash, prem3, diff)
            logme(s)
        if round(diff, 8) != 0.0:
            try:
                update_trade(commit, verb, ca, trd, 
                    None, 1, 0, adj_trd_p = 0, var1 = -diff)
            except: raise

"""----------------------------------------------------------------------------
FUNCTION
    find_mtm_price - Function which finds MtM Price for CorpAct instrument(s).

DESCRIPTION
    This function tries to find a Settle price for the instrument on which a
    Corporate Action is to be performed. Note that the name of the MtM Market
    has to be specified in the module FCAVariables as 'MtM_Market'. The 
    function first looks for the price saved for the day before the Ex Date 
    specified in the Corporate Action application. If there is no such price it
    looks for prices before that date for as many days back as has been 
    specified in FCAVariables by 'Max_Days'. If all else fails, the function 
    used_price() is used to find a price. If there is no used price, the parts
    of the Corporate Action which demands a MtM Price will not be performed.
        
ARGUMENTS
    debug       Int             Number: debug = 1
    ca          Entity          A record in the Corporate Action table
    pr          Selection       An ael selection of prices
    MtM_Market  String          The name of the MtM Market specified in
                                FCAExecute
    Max_Days    Int             Number of days back to look for MtM Prices

RETURNS
    mtmp        Float           A price
----------------------------------------------------------------------------"""

def find_mtm_price(debug, ca, pr, MtM_Market, Max_Days):
    """Find an MtM Price."""
    ### Find correct price currency:
    try:
        from FCAVariables import Curr
    except ImportError, msg:
        if string.rfind(msg, 'Curr') != -1:
            Curr = None
        else:
            raise
    if Curr == 'InstrumentCurr' and pr[0].insaddr.curr:
        Curr = pr[0].insaddr.curr # Instrument currency is preferred.
    else:
        Currid = ael.used_acc_curr()
        Curr = ael.Instrument[Currid]
    if debug:
        s = 'Curr used to find MtMPrice:%s' % Curr.insid
        logme(s)

    mtmp = None
    mtmmkt = None
    p = None
    pty = ael.Party.select('type = "MtM Market"')
    for i in pty:
        if string.upper(MtM_Market) == string.upper(i.ptyid):
            mtmmkt = i
    if not mtmmkt:
        s = 'There is no market called %s.' % MtM_Market
        logme(s)

    if len(pr) > 0:
        ###changed from range(1,Max_Days)to make it work when Max_Days=1
        for r in range(1, Max_Days + 1):
            if p != None:
                break
            yday = str(ca.ex_date.add_banking_day(Curr, -r))
            for z in pr:
                if mtmmkt:
                    ### If no price is found, the following row helps:
                    #print z.insaddr.insid, yday, mtmmkt.ptyid, Curr.insid
                    p = ael.Price.read("insaddr=%d and day='%s'\
                        and ptynbr=%d and curr=%d" % (z.insaddr.insaddr, yday, 
                        mtmmkt.ptynbr, Curr.insaddr)) #z.insaddr.curr.insaddr))
                if p:
                    if debug:
                        s = '\nSettle price: %f; day: %s' % (p.settle, p.day)
                        logme(s)
                    mtmp = p.settle
                    break
                else: mtmp = None
                        
        if mtmp == None:
            mtmp = pr[0].insaddr.used_price()
    else:
        mtmp = ca.insaddr.used_price()
        s = '\nNo historical prices in instrument. Will use used_price().'
        logme(s)
    if not mtmp:
        raise """ There is no mark to market price. """
    return mtmp
    
"""----------------------------------------------------------------------------
FUNCTION
    update_price - Function which changes prices in the price_hst/price table.

DESCRIPTION
    Takes the methods prices() and historical_prices() as basis for adjusting
    and saving new prices/quantities to the price and price_hst tables
    respectively.
        
ARGUMENTS
    commit                  Int         Number: commit = 1 to commit db changes
    debug                   Int         Number: debug = 1
    pp                      Int         Number: pp = 1 to see db records
    ca                      Entity      A record in the Corporate Action table
    rb                      Instance    Collector of information about
                                        rollbacks
    pr                      Selection   An ael selection of prices
    factor                  Float       Price changing factor
    Price_Rollback_Method   String      Save info about the price change to db
                                        or not

RETURNS
    rb                      Instance    Information about rollbacks
----------------------------------------------------------------------------"""

def update_price(commit, debug, pp, ca, rb, pr, factor, 
    Save_Price_Changes, Protected_Markets, eurex):
    """Change prices in the price tables."""
    ca_user, ca_trader, ca_acquirer = user(commit = commit)

    if len(pr) > 0 and eurex != 2:
        for i in pr.members():
            if i.day < ca.ex_date and not i.ptynbr.ptyid in Protected_Markets:
                
                if debug: 
                    s = '\nPrice Date: %s\nParty Type: %s\nParty Id: %s\n'\
                        'Settle Price: %f' \
                        % (i.day, i.ptynbr.type, i.ptynbr.ptyid, i.settle)
                    logme(s)
                if pp:
                    s = '\nOriginal price record:%s\n' % i.pp()
                    logme(s)
                p = i.clone()
                p.updat_usrnbr = ca_user
                if Save_Price_Changes == 1:
                    rb.add('Update', p, ['bid', 'ask', 'last', 'high', 'low',
                        'open', 'settle', 'diff', 'n_bid', 'n_ask',
                        'volume_last', 'volume_nbr', 'available'])
                
                if ca.hist_price_dec != -1:
                    p.bid = round(p.bid * factor, ca.hist_price_dec)
                    p.ask = round(p.ask * factor, ca.hist_price_dec)
                    p.last = round(p.last * factor, ca.hist_price_dec)
                    p.high = round(p.high * factor, ca.hist_price_dec)
                    p.low = round(p.low * factor, ca.hist_price_dec)
                    p.open = round(p.open * factor, ca.hist_price_dec)
                    p.settle = round(p.settle * factor, ca.hist_price_dec)
                    p.diff = round(p.diff * factor, ca.hist_price_dec)
                    
                else:
                    p.bid = p.bid * factor
                    p.ask = p.ask * factor
                    p.last = p.last * factor
                    p.high = p.high * factor
                    p.low = p.low * factor
                    p.open = p.open * factor
                    p.settle = p.settle * factor
                    p.diff = p.diff * factor
                
                if ca.instype not in ('Option', 'Warrant', 'Future/Forward')\
                    or eurex in (None, 0):
                    p.n_bid = math.floor(p.n_bid / factor) ### Round down.
                    p.n_ask = math.floor(p.n_ask / factor)
                    p.volume_last = math.floor(p.volume_last / factor)
                    p.volume_nbr = math.floor(p.volume_nbr / factor)
                    p.available = math.floor(p.available / factor)
                if commit: p.commit()
                
                if debug:
                    s = '=> Settle Price after: %s' % p.settle
                    logme(s)
                if pp:
                    s = 'New price details:%s\n' % p.pp()
                    logme(s)
        return rb
    
"""----------------------------------------------------------------------------
FUNCTION
    time_in_interval - Function which tells if ComparisonDate is between 
    CutOff Date and record_date.

DESCRIPTION
    Returns 1 if ComparisonDate is between CutOff Date and record_date or if
    there is no CutOff Date and Comparison Date is before record_date. Cod
    is short for CutOff Date. Maybe td means trade date or something.
    
----------------------------------------------------------------------------"""

def time_in_interval(record_date, ComparisonDate, cod, trd, verb = 0):
    if ComparisonDate == 'Acquire Date':
        td = trd.acquire_day
    elif ComparisonDate == 'Trade Time':
        td = ael.date_from_time(trd.time)
    else:
        td = trd.acquire_day
        s = "\nComparisonDate can be set to one of:\n"\
        "ComparisonDate = 'Acquire Date' (default) or"\
        "\nComparisonDate = 'Trade Time'"
        logme(s)
    if verb:
        s = '\nTrade found:%i\n%s must be <= RecordDate.'\
        '\n%s %s, RecordDate %s' % (trd.trdnbr, ComparisonDate, ComparisonDate,
        td, record_date)
        logme(s)
    if td <= record_date and (not cod or cod < td):
        return 1                                    
    else:                                           
        return 0                                    

"""----------------------------------------------------------------------------
FUNCTION
    serie_round - Function which rounds the strike price according to the
    option serie.

DESCRIPTION
    The function rounds the strike price such that the difference between the
    orginal strike and the new strike is a multiple of the series difference.
    
----------------------------------------------------------------------------"""

def serie_round(new, f, series_difference):
    serie = list(range(int(new / f), 0, -series_difference)) + \
            list(range(int(new / f), new + series_difference,  series_difference))
    serie.append(new)
    serie.sort()
    i = serie.index(new)
    if i == 0:
        return serie[1]
    elif i == len(serie) - 1:
        return serie[len(serie) - 2]
    elif new - serie[i - 1] < serie[i + 1] - new:
        return serie[i - 1]
    else:
        return serie[i + 1]

"""----------------------------------------------------------------------------
FUNCTION
    aggregate_check - Function which checks if there are aggregate trades.

DESCRIPTION
    This function makes sure that there is no aggregate trade visible in the
    instrument for which the Corporate Action is to be performed. Aggregate
    trades are not visible from an ATLAS client logged on in archived mode.

ARGUMENTS
    ca      Entity      Corporate Action record
----------------------------------------------------------------------------"""

def aggregate_check(ca):
    """Check if client is run in archived mode."""

    AggError = '\nWARNING! Avoid running FCAExecute in non-archived mode!\n'\
        'If there is an aggregate trade in the instrument on which the '\
        'Corporate Action is to be performed, the script will stop running.'\
        '\nCalculations will be incorrect if trades are later '\
        'dearchived or reaggregated.'\
        '\nPlease run this script from the prompt, or open ATLAS in archived '\
        'mode to run FCAExecute from the AEL Module Editor.'\
        '\n\nWill skip Corporate Action %s in %s (%s), ExDate %s, since '\
        'there is an aggregate trade in this instrument.\n' \
        % (ca.ca_type, ca.insaddr.insid, ca.instype, ca.ex_date)

    for t in ca.insaddr.trades():
        if t.aggregate == 1:
            logme(AggError)
            return AggError

"""----------------------------------------------------------------------------
FUNCTION
    get_corp_actions - Function which retrieves relevant Corporate Actions.

DESCRIPTION
    The function selects those Corporate Actions, from the Corporate Action
    table which have their Ex Date set on or before the 'date' which has been
    filled into the macro values box, has Trade Status and/or Instrument Status
    set to 'Script Update'.

ARGUMENTS
    date    String  Corporate Actions with Ex Date on or before this date will 
                    be executed.
RETURNS
    actions Entity  Corporate Action record(s)
----------------------------------------------------------------------------"""

def get_corp_actions(date, corpacts):
    """Return Corporate Actions with ExDate on or before Date specified."""
    
    cl = []
    try:
        corpacts = int(corpacts)
        cl.append(corpacts)
    except:
        for s in corpacts:
            if s[:6] == 'Seqno.':
                aString = s[6:]
                firstSpace = string.find(aString, ' ')
                cl.append(int(aString[:firstSpace]))
    actions = []
    for ca in ael.CorpAction:
        if (ca.ca_trade_status == 'Script Update' 
            or ca.ca_ins_status == 'Script Update'):
            if ca.seqnbr in cl or corpacts == ['All listed'] and ca.ex_date <=\
            date:
                actions.append(ca)
    return actions

"""----------------------------------------------------------------------------
FUNCTION
    update_done - Updates the Corporate Action table to 'Script Update Done'.

DESCRIPTION
    For each Corporate Action which has been performed, the Corporate Action
    table is updated to 'Script Update Done'.

ARGUMENTS
    ca  Entity  Corporate Action record
----------------------------------------------------------------------------"""

def update_done(ca):
    """Update the Corporate Action table to 'Script Update Done'."""
    if ca.ca_trade_status == 'Script Update':
        ca.ca_trade_status = 'Script Update Done'
    if ca.ca_ins_status == 'Script Update':
        ca.ca_ins_status = 'Script Update Done'
    ca.commit()
  
"""----------------------------------------------------------------------------
FUNCTION
    update_ca - Function which updates the Corporate Action to desired default
    values.

DESCRIPTION
    This function is not used at the moment, but may be used to update existing
    Corporate Actions to desired values which should be default.

ARGUMENTS
    debug       Int     Number: debug = 1
    ca          Entity  Corporate Action record
    CA_Method   String  Either 'Close' or 'Adjust' depending on what has been
                        chosen in FCAExecute.
----------------------------------------------------------------------------"""

def update_ca(debug, ca, CA_Method):
    """Updates CorpAction table to desired default values."""

    c = ca.clone()
    if CA_Method == '6_decimals': #That is, rounding == '6_decimals'
        c.trade_price_dec = 6
        c.trade_quantity_dec = 6
        c.hist_price_dec = 6
        c.ins_strike_dec = 6
        c.ins_cs_dec = 6
        c.ins_name_dec = 6
        c.div_dec = 6
    if CA_Method == 'infinity': #That is, rounding == 'infinity'
        c.trade_price_dec = -1
        c.trade_quantity_dec = -1
        c.hist_price_dec = -1
        c.ins_strike_dec = -1
        c.ins_cs_dec = -1
        c.ins_name_dec = 6
        c.div_dec = -1
    if ca.ca_type == 'Stock Split':
        c.adj_trade_quantity = 1
        if CA_Method == 1: #That is, Voluntary == 1
            c.adj_hist_price = 0
    if ca.ca_type in ('Spin-off', 'Capital Adjustment', 'Conversion'):
        if CA_Method == 1: #That is, Voluntary == 1
            c.adj_trade_quantity = 1
            c.adj_trade_price = 1
            c.trade_quantity_dec = -1
            c.trade_price_dec = -1
    c.commit()

"""----------------------------------------------------------------------------
FUNCTION
    select_deriv - Function which finds those derivatives we want to adjust.

DESCRIPTION
    A list is created with derivatives on the underlying for which Corporate
    Actions is to be performed. Derivatives which have expired are not
    included. The list is also filtered for OTC or non-OTC instruments if this
    has been specified in the Corporate Action application.
        
ARGUMENTS
    debug       Int         Number: debug = 1
    ca          Entity      A record in the Corporate Action table

RETURNS
    der_ins     List        List of derivatives instruments, entities
----------------------------------------------------------------------------"""

def select_deriv(debug, ca):
    """Make list with only those derivatives we want to change."""
    
    der_ins = []
    
    if (ca.instype == 'Option' 
        or ca.instype == 'Future/Forward' 
        or ca.instype == 'Warrant'):
        der = ael.Instrument.select('und_insaddr = %i' % ca.insaddr.insaddr)
        
        for i in der.members():
            if debug:
                s = '\nDerivative on %s: %s\nExpiryDay %s must be > ExDate '\
                    '%s' % (ca.insaddr.insid, i.insid, i.exp_day, ca.ex_date)
                logme(s)
            if ca.instype == i.instype and i.exp_day > ca.ex_date:
                der_ins.append(i)

    elif (ca.instype == 'Combination'
        or ca.instype == 'EquityIndex'):
        for i in ael.CombinationLink:
            if ca.instype == i.owner_insaddr.instype\
                and i.member_insaddr == ca.insaddr:
                der = ael.Instrument[i.owner_insaddr.insaddr]
                der_ins.append(der)
     
    if debug:
        if ca.adj_otc == 'OTC':
            s = 'Adjust OTC derivatives only.'
        elif ca.adj_otc == 'Non OTC':
            s = 'Adjust Non OTC derivatives only.'
        elif ca.adj_otc == 'None': 
            s = 'Valid for is None.'
        elif ca.adj_otc =='ALL':
            s = 'Valid for is ALL.'
        logme(s)
        s = '\nDerivatives to adjust:'
        logme(s)
    for i in der_ins:
        if ca.adj_otc == 'OTC'     and i.otc == 0\
        or ca.adj_otc == 'Non OTC' and i.otc == 1 or ca.adj_otc == 'None':
            der_ins.remove(i)  
        if debug:
            s = i.insid
            logme(s)
    return der_ins

"""----------------------------------------------------------------------------
FUNCTION
    save_deriv - Function which creates a Derivative instrument.

DESCRIPTION
    A new Derivative instrument is created according to specifications.

ARGUMENTS
    ins         Entity  Underlying instrument; None = same as before
    name        String  Name of the new Derivative instrument
    strike      Float   The strike of the Derivative instrument
    xd          Date    Date of expiry of the Derivative instrument; None = as
                        before
    cs          Float   The contract size of the Derivative
    c           String  Call or Put option, 1 = Call; None = same as before
    template    Entity  Template derivative instrument, if specific instr
                        desired
    instype     String  Type of instrument to serve as template

RETURNS
    r       Entity      New instrument entity
----------------------------------------------------------------------------"""

def save_deriv(commit, ins, name, strike, xd, cs, c, template, instype,
               startday, sedol):
    """Create new right issue instrument."""

    if instype: ### If we want to create a NEW option based on an INSTYPE.
        r = ael.Instrument.new(instype)
    if template: ### If creating a NEW option based on an existing INSTRUMENT.
        r = template.new()
    if r.insid == name: ### If we want to UPDATE an existing INSTRUMENT.
        r = template.clone()
        r.instype = 'Option'
    if (instype or r.insid == name):
        r.quote_type = 'Per Contract'
        r.und_instype = 'Stock'
        r.settlement = 'Physical Delivery'
        r.paytype = 'Spot'
        r.pay_day_offset = ins.pay_day_offset
        r.exercise_type = 'European'
        #r.exercise_type = 'American'
        r.mtm_from_feed = 0
        r.curr = ins.curr
        r.strike_curr = ins.curr
        r.strike_type = 'Absolute'
        r.exp_day = xd
        r.call_option = c ### 1= Yes
        r.und_insaddr = ins
        if (sedol != None):
            r.otc = 0
            r.extern_id2 = sedol

    ### Fields common to all:
    r.start_day = startday
    r.insid = name
    r.contr_size = cs
    r.strike_price = float(strike)
    ###r.category_chlnbr = ### = Val Group in Trade window
    if commit: r.commit()
    return r
    
"""----------------------------------------------------------------------------
FUNCTION
    name_change - Function which only renames an instrument.
----------------------------------------------------------------------------"""

def name_change(commit, ca, new_name, rb):
    """Change name of instrument."""

    y = ca.insaddr.clone()
    z = ca.clone()
    rb.add('Update', y, ['insid'])
    rb.add('Update', z, ['text'])
    y.insid = new_name
    v = z.text + ' <= ' + str(ca.insaddr.insid)
    z.text = str(v)
    if commit: y.commit()
    if commit: z.commit()
    return rb

"""----------------------------------------------------------------------------
FUNCTION
    update_name - Function which changes derivative name / insid.

DESCRIPTION
    This function tries to figure out a new instrument id of a derivative. If
    there is no strike figure in the name, the new name will be 'old name + a
    modifier', where a modifier will be X, Y, Z or W. If there is a strike
    number in the name, the new name will be 'old name + new strike +
    modifier'. The strike is assumed to be at the end of the name, unless the
    series has been modified before.
        
ARGUMENTS
    ca  Entity      A record in the Corporate Action table
    x   Entity      A record in the Instrument table

RETURNS
    x   Entity      A record in the Instrument table
----------------------------------------------------------------------------"""

def update_name(ca, x, adjustStrike = 1):
    try:
        fieldName = FCAVariables.ShortCodeFieldName
    except:
        fieldName = ''
        print 'Warning, FCAVariables has no variable ShortCodeFieldName.'
    """Change derivative name according to specified rules."""
    if fieldName and ca.ca_type in ('Merger', 'Capital Adjustment', 'Stock Split'):
        if ca.new_insaddr:
            old_underlying = eval('ca.insaddr.' + fieldName)
            ca_new = ca.new_insaddr
            try:
                new_underlying = eval('ael.Instrument[ca_new].' + fieldName)
            except TypeError:
                new_underlying = eval('ca_new.' + fieldName)
            if old_underlying:
                exec 'x.insid = string.replace(x.insid\
                     , old_underlying, new_underlying)'
    if not (ca.ca_type in ('Merger',)):
        modifiers = ('X', 'Y', 'Z')
        old_mod = []
        if x.insid[-1] in modifiers:
            old_mod = x.insid[-1]
            x.insid = x.insid[:-1] ### Peel off the modifier.
        if old_mod == []:
            new_mod = 'X'
        elif old_mod == 'X':
            new_mod = 'Y'
        elif old_mod == 'Y':
            new_mod = 'Z'
        elif old_mod == 'Z':
            new_mod = 'A'
        if x.insid[-3:] in ('ABE', 'CBK', 'DSE', 'FSP', 'SHB', 'NDS', 'SEB',
                            'SGA', 'UBS'):
            emmitent = x.insid[-3:]
            x.insid = x.insid[:-3]
        else:
            emmitent = ''
        ### Find out how many figures there are at the end.
        j = -1
        while x.insid[j] in string.digits + '.':
            j = j - 1
        if adjustStrike and j <> -1:
            name_strike = real_round(x.strike_price, ca.ins_name_dec)
            s = x.insid[0:j+1] + name_strike + emmitent + new_mod
        else:
            s = x.insid + emmitent + new_mod
        x.insid = s[0:39] # Insid can be max 39 characters.
    return x

def real_round(number, dec):
    r = round(number, dec)
    if dec == 0:
        return str(int(r))
    else:
        str_dec = str(r - math.floor(r))
        zeros = dec + 2 - len(str_dec)
        return str(r) + zeros * '0' 

"""----------------------------------------------------------------------------
FUNCTION
    update_nominal - Function which changes the nominal amount.

DESCRIPTION
    The nominal_amount is the quantity times the contract_size.
    This function adjusts derivative contract size or quantity. In the Eurex
    case, the contract size is always changed, since the trade quantity is not
    changed. If the strike is adjusted, the contract size is adjusted to 
    'old contr_size * old strike_price / new strike_price'. If the strike has
    not been adjusted, the contract size is changed to 'old contr_size * new
    stock quantity / old stock quantity'.
    
    In the OM case, it is possible to choose to adjust the contract size or the
    trade quantity. Therefore, in order to make it impossible to change both 
    trade quantity and contract size, a rule has been specified (in FCAExecute)
    which forces the trade quantity to change and keeps the contract size as it
    was, if nothing else has been specified.
        
ARGUMENTS
    commit      Int         Number: commit = 1 to commit db changes
    debug       Int         Number: debug = 1
    pp          Int         Number: pp = 1 to see db records
    ca          Entity      A record in the Corporate Action table
    der_ins     List        List of derivatives instruments, entities
    f           Float       Adjustment factor
    rb          Instance    Collector of information about rollbacks

RETURNS
    rb          Instance    Information about rollbacks
----------------------------------------------------------------------------"""

def update_nominal(commit, debug, pp, ca, x, f, adj_ins_cs, 
                adj_ins_strike, adj_ins_name, eurex, old_strike):
    """Change Eurex and OM derivatives according to specified rules."""
    if adj_ins_strike:
        ### Change Contract Size; Alt. 1:
        if adj_ins_cs:
            if x.strike_price > 0:
                old_cs = x.contr_size
                if ca.ins_cs_dec == -1:
                    x.contr_size = x.contr_size / f
                else:
                    x.contr_size = round((x.contr_size * old_strike) / 
                                x.strike_price,  ca.ins_cs_dec)
    else:
        if eurex <> 0:
            ### Change Contract Size; Alt. 2:
            if adj_ins_cs:
                old_cs = x.contr_size
                if ca.ins_cs_dec == -1:
                    x.contr_size = x.contr_size / f ### * (n/o)
                else:
                    x.contr_size = round(x.contr_size / f, ca.ins_cs_dec)
                    x.phys_contr_size = math.floor(x.contr_size)
    if pp: logme(x.pp())
    return x

"""----------------------------------------------------------------------------
FUNCTION
    update_dividend - Function which changes stock dividends.

DESCRIPTION
    The dividend field is updated to dividend * factor.
            
ARGUMENTS
    commit      Int         Number: commit = 1 to commit db changes
    debug       Int         Number: debug = 1
    ca          Entity      A record in the Corporate Action table
    div         Entity      A record in the Dividend table
    rb          Instance    Collector of information about rollbacks
    factor      Float       Dividend changing factor

RETURNS
    rb          Instance    Information about rollbacks
----------------------------------------------------------------------------"""

def update_dividend(commit, debug, ca, div, rb, factor):
    """Update dividends in the dividend table."""
    
    ca_user, ca_trader, ca_acquirer = user()
    
    d = div.clone()
    d.pp()
    d.updat_usrnbr = ca_user
    rb.add('Update', d, ['dividend'])
    if ca.div_dec != -1:
        d.dividend = round(d.dividend * factor, ca.div_dec)
    else:
        d.dividend = d.dividend * factor
    if commit: d.commit()
    
    if debug:
        s = '\nOld Div %f -> New Div %f' % (div.dividend, d.dividend)
        logme(s)
    return rb

"""----------------------------------------------------------------------------
FUNCTION
    update_weight - Function which changes Equity Index or Combination weights.

DESCRIPTION
    The weight field is updated to weight / factor.
            
ARGUMENTS
    commit      Int         Number: commit = 1 to commit db changes
    debug       Int         Number: debug = 1
    ins         Entity      A record in the Instrument table
    rb          Instance    Collector of information about rollbacks
    factor      Float       Dividend changing factor

RETURNS
    rb          Instance    Information about rollbacks
----------------------------------------------------------------------------"""

def update_weight(commit, debug, ins, rb, factor):
    """Update weights in the CombinationLink table."""
    
    ca_user, ca_trader, ca_acquirer = user()

    for i in ael.CombinationLink:
        if i.member_insaddr == ins:
            rb.add('Update', i, ['weight'])
            w = i.clone()
            w.updat_usrnbr = ca_user
            w.weight = i.weight / factor
            if commit: w.commit()

            if debug:
                s = '\n%s in %s: Old Factor %f -> New Factor %f' %\
                (i.member_insaddr.insid, i.owner_insaddr.insid, i.weight,
                 w.weight)
                logme(s)
    return rb

"""----------------------------------------------------------------------------
FUNCTION
    save_addinfo - Function which enters new addinfo field in database.

DESCRIPTION
    The addinfo fields are created with values passed to the function.
            
ARGUMENTS
    ca          Entity      Corporate Action record
    specname    String      The name of the addinfo specification (field_name)
    rb          Instance    Collector of information about rollbacks
    value       String      Name of instrument or amount of stock

RETURNS
    rb          Instance    Information about rollbacks
----------------------------------------------------------------------------"""

def save_addinfo(ca, specname, value):
    """Save corporate action values to the AdditionalInfo table."""
    
    ai = ael.AdditionalInfo.new(ca)
    ai.addinf_specnbr = ael.AdditionalInfoSpec[specname]
    ai.value = value
    ai.commit()
    s = 'Committed %s to AdditionalInfo table.' % ai.value
    logme(s)

"""----------------------------------------------------------------------------
FUNCTION
    add_addinfo_spec - Function which enters new addinfo specification in the 
                       database.

DESCRIPTION
    The addinfo fields are created with values passed to the function.
            
ARGUMENTS
    table       Enum        Table to which addinfo spec refers
    field_name  String      Name of the addinfo specification (field_name)
    desc        String      Description of addinfo spec
    default     String      If a default field_name is desired
    typegroup   EnumName    Enum category in ds_enums
    type        Enum        Enum instance, e.g. Table name
    rb          Instance    Collector of information about rollbacks

RETURNS
    rb          Instance    Information about rollbacks
----------------------------------------------------------------------------"""

def add_addinfo_spec(table, field_name, desc, default, typegroup, type):
    """Save addinfo specifications."""

    for i in ael.AdditionalInfoSpec:
        if i.field_name == field_name:
            #s = 'AddInfoSpec %s already defined.' % i.field_name
            #logme(s)
            return # already defined
        #Released before, change name
        elif i.field_name == 'Portfolio' and field_name == 'Portfolio':
            b = i.clone()
            b.field_name = field_name
            b.commit()
            return
        elif i.field_name == 'Quantity' and field_name == 'Quantity': 
            return
        elif i.field_name == 'Price 1' and field_name == 'Old Price': 
            return
        elif i.field_name == 'Price 2' and field_name == 'New Price': 
            return
        #Released before, switch field & delete
        elif i.field_name == 'CashInstrument' and field_name == 'Cash Ins': 
            return
                
    a = ael.AdditionalInfoSpec.new()
    
    a.rec_type = table
    a.field_name = field_name
    setattr(a, 'data_type.grp', typegroup)
    a.default_value = default
    if typegroup == 'Standard':
        setattr(a, 'data_type.type', ael.enum_from_string('B92StandardType', 
                                                           type))
    elif typegroup == 'RecordRef':
        setattr(a, 'data_type.type', ael.enum_from_string('B92RecordType', 
                                                           type))
    elif typegroup == 'Enum':
        setattr(a, 'data_type.type', ael.enum_from_string('B92EnumType', 
                                                           type))
    a.description = desc
    a.commit()
    s = 'Added Additional Info Specification: %s' % a.field_name
    logme(s)
















