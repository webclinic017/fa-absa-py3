""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE
    FCATypes - Module which executes different corporate action types.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.
        
    Functions:
        
        rightsdistribution - Function which performs the Corporate Actions
                             New Issue, Stock Dividend and Buyback.

        convert - Function which converts the chosen convertible.
        
        merger - Function which performs a merger/acquisition.
    
        spin - Function which performs the corporate action Spin-off.

        split - Function which performs a Stock Split Corporate Action.

        bond_call - Function which performs calls bonds, partially or fully.

----------------------------------------------------------------------------"""
try:
    import string
except ImportError:
    print('The module string was not found.')
    print()
try:
    import FCARollback
except ImportError:
    print('The module FCARollback was not found.')
    print()
import ael
import FCAGeneral
import FCAVariables

Voluntary           = FCAVariables.Voluntary
rights_distribution = FCAVariables.rights_distribution
Price               = FCAVariables.Price
#Curr               = FCAVariables.Curr
#AccCurr            = FCAVariables.AccCurr
ComparisonDate      = FCAVariables.ComparisonDate
#Default_Portfolio  = FCAVariables.Default_Portfolio
commit              = FCAVariables.commit
verb                = FCAVariables.verb
debug               = FCAVariables.debug
pp                  = FCAVariables.pp
log                 = FCAVariables.log
#if log:
    #logfile = FCAVariables.logfile #'c:\\temp\\corpact.txt'
    #lf = open(logfile, 'a')
    #FCAGeneral.close_log(lf)
    #lf = open(logfile, 'a')
#else: lf = None
try: Default_Portfolio
except NameError: Default_Portfolio = None

"""----------------------------------------------------------------------------
FUNCTION
    RightsDistribution - Function which performs the Corporate Actions
    New Issue, Stock Dividend and Buyback.

DESCRIPTION
    New Stock Right trades are created. Positions are closed out and opened up,
    or adjusted, depending on which CA_Method has been specified.  Information
    about what is done is saved to the database via the module FCARollback.
----------------------------------------------------------------------------"""

def rightsdistribution(verb, commit, ca, rb, pf, pos, filtered_trades, ins, 
    n, o, mtmp, cash, quantity, price, call_or_put, CA_Method, cod = None):
    """Performs new issue, stock dividend and buyback corporate actions."""
    ### A New Instrument has to be defined to run this function:
    if not ins:
        s = 'Corporate Action demands a second instrument '\
            '(Stock Right) in the "New Instrument"-field.'
        FCAGeneral.logme(s)
        noins = 'No New Instrument'
        raise noins
    ### General calculations:
    else:
        f = None #newp / mtmp #Not used
        ins_strike = ins.strike_price
        ### Convert strike price if needed:
        try:
            from FCAVariables import Curr
        except ImportError, msg:
            if string.rfind(msg, 'Curr') != -1:
                Curr = None
            else:
                raise
        if Curr == 'PortfolioCurr': # and prf.prfnbr and prf.curr:
            pfcurr = 1
        else:
            pfcurr = 0
        if Curr == 'InstrumentCurr' and ca.insaddr.curr:
            Curr = ca.insaddr.curr # Instrument currency is preferred.
        else:
            Currid = ael.used_acc_curr()
            Curr = ael.Instrument[Currid]
        if ins.strike_curr != Curr:
            try:
                fx_rate = Curr.used_price(ca.ex_date, ins.strike_curr.insid)
                if verb:
                    s = 'Exchange rate used:%f\nStrike before:%f\nAfter:%f'\
                      % (fx_rate, ins.strike_price, ins.strike_price / fx_rate)
                    FCAGeneral.logme(s)
                ins_strike = ins.strike_price / fx_rate
            except ZeroDivisionError:
                s = 'ZeroDivisionError, not possible to convert Strike into'+\
                    ' correct currency. Will continue without converting. '+\
                    'Fx rate:%f' % fx_rate
                FCAGeneral.logme(s)
        
        if Price:
            if call_or_put == 'put':
                if n == o:
                    adjp = mtmp - ins_strike
                else:
                    newp = (o * mtmp - n * ins_strike)/(o - n)
                    adjp = (ins_strike - newp) * (n / o)
            else:
                newp = (o * mtmp + n * ins_strike)/(o + n)
                adjp = (newp - ins_strike) * (n / o)
            rightp = max(adjp, 0)
        else:
            rightp = 0
        if ca.insaddr.quote_type != ins.quote_type:
            if ca.insaddr.quote_type == 'Per Unit' \
                and ins.quote_type != 'Per Contract':
                adj_rightp = rightp * 100
            else:
                adj_rightp = rightp
            if ca.insaddr.quote_type == 'Per 100 Units':
                adj_rightp = rightp / 100
        else: 
            adj_rightp = rightp
        
        ### If one portfolio:
        if pf:
            q = pos[pf][2]
            ### Create Stock Right trades in one portfolio:
            e = FCAGeneral.create_trade(verb, commit, debug, pp,
                                        ca, ins, pf, ca.record_date,
                                        'Adjust', q, adj_rightp, 'Rights')
            if e != None: rb.add('Delete', e)

        for prf in pos.keys():
            ### Calculations in each portfolio:
            if quantity == None:
                q = pos[prf][0]
            else:
                q = quantity

            ### Note that cash has to be separately adjusted for quantity, 
            ### since quantity is never adjusted when there is a Rights 
            ### Distribution.
            adj_cash = cash * (q / o)

            ### Convert adj_rightp into portfolio currency if needed:
            adj_rightp_old = adj_rightp #Reset the price in the loop.
            adj_rightp = adj_rightp_old

            if pfcurr == 1: # Conversion of adj_rightp is needed
                try:
                    fx_rate = prf.curr.used_price(ca.ex_date, Curr.insid)
                    adj_rightp = adj_rightp / fx_rate
                except ZeroDivisionError:
                    s = 'ZeroDivisionError, not possible to convert ' + \
                        'RightPrice into correct currency. Will continue' + \
                        'without converting. Fx rate:%f' % fx_rate
                    FCAGeneral.logme(s)

            if price:
                openp = avgp = price
            elif Price and q != 0:
                avgp  = pos[prf][1]
                openp = avgp - adj_rightp #- adj_cash # * n / o - cash / q
            else:
                openp = avgp = 0
            
            if verb:
                s = '\n\n### CALCULATIONS FOR %s in %s ###\n'\
                    '\nPosition: %f'\
                    '\nAdjusted Stock Price: %f'\
                    '\n%s Strike: %f'\
                    '\nStock Right Price: max(%f;0)' \
                    % (ca.insaddr.insid, prf.prfid, q, openp,
                    ins.insid, ins.strike_price, adj_rightp)
                FCAGeneral.logme(s)
            if verb: 
                s = '\n\n### CREATING TRADES ###\n'
                FCAGeneral.logme(s)

            ### Create close & open trades:
            if CA_Method == 'Close':
                if rights_distribution != 1: # Want to adjust existing pos.
                    ### Create closing trade:
                    t = FCAGeneral.create_trade(verb, commit, debug,
                                                pp, ca, ca.insaddr, prf,
                                                ca.record_date, 'Closing', q,
                                                avgp, 'NewIssue')
                    if t != None: rb.add('Delete', t)

                    ### Create opening trade:
                    op = FCAGeneral.create_trade(verb, commit, debug,
                                                 pp, ca, ca.insaddr, prf,
                                                 ca.record_date, 'Adjust', q,
                                                 openp, adj_cash)
                    if op != None: rb.add('Delete', op)

            ### Create Stock Right trades:
            #rightq = q * n / o
            if not pf:
                e = FCAGeneral.create_trade(verb, commit, debug, pp,
                                            ca, ins, prf, ca.record_date,
                                            'Adjust', q, adj_rightp, 'Rights')
                if e != None:
                    rb.add('Delete', e)
            
            ### If rounding errors are found, add cash payment for the 
            ### difference:
            try:
                if CA_Method == 'Close' and rights_distribution != 1\
                    and ca.cash_curr not in (None, 'None'):
                    switch_cash = FCAGeneral.switch_curr(verb, ca, e.curr,
                        adj_cash, ca.ex_date, ca.cash_curr.insid)
                    FCAGeneral.prem_diff(commit, verb, ca, op, 
                        t.premium, op.premium, switch_cash, e.premium)
            except AttributeError, msg:
                pass
    
        ### Adjust trades:
        if CA_Method == 'Adjust':
            if verb:
                s = '\n### ADJUSTING TRADE HISTORY ###\n'
                FCAGeneral.logme(s)
            test = {}
            for trd in filtered_trades: #ca.insaddr.trades():
                if FCAGeneral.time_in_interval(ca.record_date, 
                    ComparisonDate, cod, trd, verb):
                    
                    ### Calculate factor for each trade:
                    adj_cash = cash * (trd.quantity / o)
                    switch_cash = adj_cash
                    try:
                        if ca.cash_curr not in (None, 'None'):
                            switch_cash = FCAGeneral.switch_curr(verb, ca, 
                                trd.curr, adj_cash, ca.ex_date, 
                                ca.cash_curr.insid)
                    except AttributeError, msg:
                        pass
                    
                    f = (trd.price - adj_rightp - 
                        switch_cash / trd.quantity) / trd.price

                    ### The test only works for one portfolio:
                    if trd.status not in ('Confirmed Void', 'Simulated',
                                          'Void', 'Reserved', 'Terminated'):
                        test[trd.trdnbr] = trd.premium, trd.premium * f,\
                            e.premium, adj_cash

                    FCAGeneral.update_trade(commit, verb, ca, trd,
                        rb, f, adj_trd_q = 0, var1 = switch_cash)

            ### Check: The check only works for one portfolio.
            check = 0 # 1           
            if check:
                if test.values():
                    old_prem = 0.0
                    prem = 0.0
                    #rights = 0.0
                    add_pay = 0.0
                    for i, j, k, l in test.values():
                        old_prem = old_prem + i
                        prem = prem + j
                        rights = k # rights + k
                        add_pay = add_pay + l
                    print(old_prem, prem, rights, add_pay, prem+rights-add_pay)

    return rb, f

"""----------------------------------------------------------------------------
FUNCTION
    convert - Function which converts the chosen convertible.

DESCRIPTION
    The convertible position per portfolio is closed out, at the price 100%
    (assuming Quote Type = Pct of nominal). Furthermore, new equity trade(s)
    are created. Information about the conversion is saved to the database so
    that Rollbacks can be performed to undo the Corporate Action.
----------------------------------------------------------------------------"""

def convert(verb, commit, ca, rb, pf, pos, n, o, cash, quantity, 
    amount_in_percent, CA_Method):
    """Convert the convertible, i.e.closing out convertible + buying stock."""

    ratio = ca.insaddr.conversion_ratio
    f = n/o ### n=1 o=1 => convert to all equity; n=0 o=1 => convert to 
            ### all cash.
    all_cash = 0
    if n == 2:
        ### Workaround: to convert all into cash. No equity trade.
        all_cash = 1
        f = 1.0
    
    if Price != 1:
        ### Not applicable if close out convertible price is not 100%.
        openp = ca.insaddr.contr_size / ratio 
    
    ### Create new equity trade:
    if pf: ### Create trade in specified portf if possible.
        if quantity == None:
            q = pos[pf][2] * amount_in_percent
        else:
            q = quantity
        close_premium = q * ca.insaddr.contr_size * (1 - f)
        openq = q * ratio * f
        
        e = FCAGeneral.create_trade(verb, commit, debug, pp,
                                    ca, ca.insaddr.und_insaddr, pf,
                                    ca.record_date, 'Adjust', openq,
                                    openp, 'Conversion')
        rb.add('Delete', e)
        
    for prf in pos.keys():
        if quantity == None:
            q = pos[prf][0] * amount_in_percent
        else:
            q = quantity
        closep = pos[prf][1]
        openq = q * ratio * f
        adj_cash = cash * openq

        if verb:
            s = '\n\n### CREATING TRADES ###\n'
            FCAGeneral.logme(s)
        ### Always create following trades in original portf. 
        ### Close out convertible position:
        if Price != 1: #Close at price 100%.
            t = FCAGeneral.create_trade(verb, commit, debug, pp, 
                ca, ca.insaddr, prf, ca.record_date, 'Closing', q, 
                closep, 'Conversion')
        if Price == 1: #Close at avg_price.
            if all_cash == 0:
                var1 = 'None'
            else:
                var1 = adj_cash
            t = FCAGeneral.create_trade(verb, commit, debug, pp, 
                ca, ca.insaddr, prf, ca.record_date, 'Closing', q, 
                closep, var1)
        rb.add('Delete', t)

        if not pf and all_cash == 0: 
            ### If no prf has been specified, create trade in 
            ### original prf. 

            ### This piece of code ensures that for stocks, and if in 
            ### FCAVariables Price = 1,
            ### the premiums will cancel each other out, regardless of the
            ### stock's quote type,
            ### provided that contract size for the stocks is always 1.
            ### Note that this code does not ensure that this will work if only
            ### one opening portfolio
            ### is used, as this would require further development.
            if Price == 1:
                if ca.insaddr.und_insaddr.quote_type == 'Per Unit':
                    openp = abs(t.premium / ca.insaddr.und_insaddr.contr_size\
                                 / openq)
                elif ca.insaddr.und_insaddr.quote_type == 'Per 100 Units':
                    openp = abs(t.premium * 100 / openq)
                else: openp = abs(t.premium / openq)

            e = FCAGeneral.create_trade(verb, commit, debug, pp, ca, 
                                        ca.insaddr.und_insaddr, prf,
                                        ca.record_date, 'Adjust', openq, 
                                        openp, adj_cash)
            rb.add('Delete', e)
    return rb

"""----------------------------------------------------------------------------
FUNCTION
    merger - Function which performs a merger/acquisition.

DESCRIPTION
    The original stock position per portfolio is closed out, at the market
    price.  Furthermore, new equity trade(s) are created in the new stock.
    Information about what is done is saved to the database via the module
    FCARollback so that Rollbacks can be performed to undo the Corporate
    Action.
----------------------------------------------------------------------------"""

def merger(verb, commit, ca, rb, pf, pos, ins, n, o, mtmp, mtmp2, cash, 
    quantity, amount_in_percent, price, newprice, cashins, CA_Method):
    """Perform switch of stocks, etc."""
    # Solution implemented (provided that Price == 1):
    # q = the position
    # f = o / n = for each o old we hold we get n new.
    # cash = we get cash per each lump o of the old stock we hold
    # If o = 10 we get cash per 10 shares = cash / o per old share
    # = (o / n) * (cash / o) = cash / n per new share.
    # Closing trade at the MtMPrice minus the cash payment. 
    # If we view the cash payment as a cash dividend the MtMPrice would 
    # decrease, and thus the value of the position would decrease by the 
    # cash amount received:
    # -q * (mtmp - cash) = +premium 
    # Opening trade: Since the stock price is assumed to have already 
    # decreased by the amount of the cash received, the opening price is
    # the adjusted closing price:
    # (+q/f) * (f * (mtmp - cash)) = q * (mtmp - cash) = -premium 

    f = o / n
    
    openp = None
    if Price == 1:
        if mtmp != None:
            closep = mtmp - cash #mtmp
            openp = (mtmp - cash) * f #(mtmp * f)
    elif Price == 'MtM':
        if mtmp != None:
            closep = mtmp
        if mtmp2 != None:
            openp = mtmp2
    elif Price == 0:
        closep = 0
        openp = 0
    
    ### If prices have been specified in addinfo fields they override other 
    ### prices:
    if price != None:
        closep = price
    if newprice != None:
        openp = newprice
    
    ### Create new equity trade:
    if pf:
        q = pos[pf][2] * amount_in_percent
        openq = q / f #* (n/o)
            
        e = FCAGeneral.create_trade(verb, commit, debug, pp,
                                    ca, ins, pf, ca.record_date,
                                    'Adjust', openq, openp, cash)
        rb.add('Delete', e)

    for prf in pos.keys():
        if quantity == None:
            q = pos[prf][0] * amount_in_percent
        else: #If quantity has been specified in an addinfo field:
            q = quantity
        openq = q / f #* (n/o)

        ### Cash adjusted for quantity to be received:
        adj_cash = cash * (q / o) # * openq
        
        if Price == 1:
            if mtmp != None:
                closep = mtmp #- adj_cash
                openp = (mtmp - adj_cash) * f #(mtmp * f)
        elif Price == 'MtM':
            if mtmp != None:
                closep = mtmp
        if mtmp2 != None:
            openp = mtmp2
        elif Price == 0:
            closep = 0
            openp = 0
            
        ### If prices have been specified in addinfo fields they override other
        ### prices:
        if price != None:
            closep = price
        if newprice != None:
            openp = newprice

        ### Convert prices into portfolio currency if needed:
        openp_old = openp #Reset the prices in the loop.
        closep_old = closep
        openp = closep_old
        closep = closep_old
        try:
            from FCAVariables import Curr
        except ImportError, msg:
            if string.rfind(msg, 'Curr') != -1:
                Curr = None
            else:
                raise
        if Curr == 'PortfolioCurr' and prf.prfnbr and prf.curr:
            pfcurr = 1
        else:
            pfcurr = 0
        if Curr == 'InstrumentCurr' and ca.insaddr.curr:
            Curr = ca.insaddr.curr # Instrument currency is preferred.
        else:
            Currid = ael.used_acc_curr()
            Curr = ael.Instrument[Currid]

        if pfcurr == 1: # Conversion of mtmp and mtmp2 are needed
            try:
                fx_rate = prf.curr.used_price(ca.ex_date, Curr.insid)
                if verb:
                    s = 'Exchange rate used:%f\nOpenPrice before:%f\nAfter:%f'\
                        % (fx_rate, openp, openp / fx_rate)
                    FCAGeneral.logme(s)
                    s = 'Exchange rate used:%f\nClosePrice before:%f\n'\
                        'After:%f' % (fx_rate, closep, closep / fx_rate)
                    FCAGeneral.logme(s)
                openp = openp / fx_rate
                closep = closep / fx_rate
            except ZeroDivisionError:
                s = 'ZeroDivisionError, not possible to convert Trade Prices '\
                    'into correct currency. Will continue without converting.'\
                    ' Fx rate:%f' % fx_rate
                FCAGeneral.logme(s)
        
        if verb:
            s = '\n### CREATING TRADES ###\n'
            FCAGeneral.logme(s)

        ### Create closing trade:
        if Voluntary != 1:
            t = FCAGeneral.create_trade(verb, commit, debug, pp, ca, 
                                    ca.insaddr, prf, ca.record_date,
                                    'Closing', q, closep, adj_cash)
            rb.add('Delete', t)
        else:
            t = FCAGeneral.create_trade(verb, commit, debug, pp, ca, 
                                    ca.insaddr, prf, ca.record_date,
                                    'Closing', q, closep, 'Merger')
            rb.add('Delete', t)

        ### This piece of code ensures that for stocks, and if in FCAVariables 
        ### Price = 1, the premiums will cancel each other out, 
        ### regardless of the stocks' quote types,
        ### provided that contract size for the stocks is always 1.
        ### Note that this code does not ensure that this will work if only one
        ### opening portfolio is used, as this would require further 
        ### development.
        if Price == 1:
            if mtmp != None and ins != None:
                if ins.quote_type == 'Per Unit':
                    openp = abs(t.premium / ins.contr_size / openq)
                elif ins.quote_type == 'Per 100 Units':
                    openp = abs(t.premium * 100 / openq)
                else: openp = abs(t.premium / openq)

        if Voluntary == 1:
            ### Create new equity trade, and new cash trade:
            if not pf:
                if ins != None:
                    e = FCAGeneral.create_trade(verb, commit, debug, 
                        pp, ca, ins, prf, ca.record_date, 'Adjust',
                        openq, openp, 'Merger')
                    rb.add('Delete', e)
            if cashins != None:
                cashins = ael.Instrument[cashins]
                #cash = float(cash)
                c = FCAGeneral.create_trade(verb, commit, debug, pp, 
                ca, cashins, prf, ca.record_date, 'Adjust',
                        q, adj_cash, 'Merger')
                rb.add('Delete', c)
    
        else:
            ### Create new equity trade:
            if not pf:
                if ins != None:
                    e = FCAGeneral.create_trade(verb, commit, debug, 
                        pp, ca, ins, prf, ca.record_date, 'Adjust',
                        openq, openp, 'Merger')
                    rb.add('Delete', e)
    
        ### If rounding errors are found, add cash payment for the difference:
        #switch_cash = adj_cash
        #if ca.cash_curr not in (None, 'None'):
            #switch_cash = FCAGeneral.switch_curr(verb, ca, e.curr,
                #adj_cash, ca.ex_date, ca.cash_curr.insid)
        try:
            FCAGeneral.prem_diff(commit, verb, ca, e, 
                    t.premium, e.premium, 0.0, 0.0) #switch_cash, 0.0)
        except UnboundLocalError, msg:
            print(msg) #local variable 'e' referenced before assignment
            pass #will happen if e is not defined and this is ok
    return rb, f

"""----------------------------------------------------------------------------
FUNCTION
    spin - Function which performs the corporate action Spin-off.

DESCRIPTION
    New Stock Right trades are created.  Information about what is done is
    saved to the database via the module FCARollback.

ARGUMENTS
    ca  Entity  Corporate Action record

RETURNS
    e   Entity  New trade entity
    Saves new equity trade to the database
    Prints information about the trades to the console
----------------------------------------------------------------------------"""

def spin(verb, commit, ca, rb, pf, pos, filtered_trades, ins, n, o, 
    mtmp, mtmp2, cash, CA_Method, cod = None):
    """Function which performs the corporate action spin-off."""
    f = o / n
    spintrades = {}
    ### Temporary explanations:
    # mtmp = factor to adjust original stock price with.
    # mtmp2 = factor at which to open spin-off stock trade

    if CA_Method == 'Close':
        ### Create new equity trade:
        if pf:
            q = pos[pf][2]
            avgp = pos[pf][1]
            openq = q / f
            if Voluntary == 1:
                ###openp = opening price of original equity trade.
                openp = avgp * mtmp
            else:
                openp = (mtmp2 / mtmp) * avgp
            if Voluntary == 1:
                ###newp = price of new equity trade
                newp = mtmp2
            else:
                newp = avgp - openp
            e = FCAGeneral.create_trade(verb, commit, debug, pp,
                                        ca, ins, pf, ca.record_date,
                                        'Adjust', openq, newp, cash)
            rb.add('Delete', e)
        
    for prf in pos.keys():
        t = None # Necessary to refresh trade calculations.
        q = pos[prf][0]
        avgp = pos[prf][1]
        openq = q / f
        
        ### Note that cash has to be separately adjusted for quantity, 
        ### since quantity is never adjusted when there is a Spin-off
        adj_cash = cash * (q / o)
        
        ### Convert MtMPrices into portfolio currency if needed:
        mtmp_old = mtmp #Reset the prices in the loop.
        mtmp2_old = mtmp2
        mtmp = mtmp_old
        mtmp2 = mtmp2_old
        try:
            from FCAVariables import Curr
        except ImportError, msg:
            if string.rfind(msg, 'Curr') != -1:
                Curr = None
            else:
                raise
        if Curr == 'PortfolioCurr' and prf and prf.prfnbr and prf.curr:
            pfcurr = 1
        else:
            pfcurr = 0
        if Curr == 'InstrumentCurr' and ca.insaddr.curr:
            Curr = ca.insaddr.curr # Instrument currency is preferred.
        else:
            Currid = ael.used_acc_curr()
            Curr = ael.Instrument[Currid]

        if pfcurr == 1: # Conversion of mtmp and mtmp2 are needed
            try:
                fx_rate = prf.curr.used_price(ca.ex_date, Curr.insid)
                if verb:
                    s = 'Exchange rate used:%f\nMtMPrice before:%f\nAfter:%f'\
                        % (fx_rate, mtmp, mtmp / fx_rate)
                    FCAGeneral.logme(s)
                    s = 'Exchange rate used:%f\nMtMPriceNew before:%f\n'\
                        'After:%f' % (fx_rate, mtmp2, mtmp2 / fx_rate)
                    FCAGeneral.logme(s)
                mtmp = mtmp / fx_rate
                mtmp2 = mtmp2 / fx_rate
            except ZeroDivisionError:
                s = 'ZeroDivisionError, not possible to convert MtMPrices '\
                    'into correct currency. Will continue without converting.'\
                    ' Fx rate:%f' % fx_rate
                FCAGeneral.logme(s)
        
        if Voluntary == 1:
            openp = avgp * mtmp #new eq trd
        else:
            #openp = (mtmp2 / mtmp) * avgp
            adj_mtmp2 = mtmp2 * (n/o)
            openp = (adj_mtmp2 / mtmp) * avgp
        if Voluntary == 1:
            newp = mtmp2
        else:
            newp = avgp - openp

        if verb and prf:
            s = '\n### CALCULATIONS FOR %s in %s ###'\
                '\nPosition: %f\nQty * New/Old: %f\n'\
                % (ca.insaddr.insid, prf.prfid, q, openq)
            FCAGeneral.logme(s)

        if debug and Voluntary != 1:
            s = '\n(MtMPriceNewInstr*(NewQty/OldQty)/MtMPrice)*AvgPrice:'\
                '(%f*(%f/%f)/%f)*%f=%f'\
                '\nAdjusted Stock Price = %f - %f = %f' %\
                (mtmp2, n, o, mtmp, avgp, openp, avgp, openp, newp)
            FCAGeneral.logme(s)

        if CA_Method == 'Close':
            if verb:
                s = '\n### CREATING TRADES ###'
                FCAGeneral.logme(s)
            
            ### Create closing trade:
            t = FCAGeneral.create_trade(verb, commit, debug, pp,
                                        ca, ca.insaddr, prf, ca.record_date,
                                        'Closing', q, avgp, 'Spin-off')
            rb.add('Delete', t)

            ### Create opening trade:
            ### Switched openp to newp
            op = FCAGeneral.create_trade(verb, commit, debug, pp,
                                         ca, ca.insaddr, prf,
                                         ca.record_date, 'Adjust', q, newp,
                                         'Spin-off')
            rb.add('Delete', op)

        ### This piece of code ensures that for stocks, and if in 
        ### FCAVariables Price = 1, the premiums will cancel each other 
        ### out, regardless of the stocks' quote types, provided that 
        ### contract size for the stocks is always 1.
        ### Note that this code does not ensure that this will work if 
        ### only one opening portfolio is used, as this would require 
        ### further development.
        if Price == 1 and mtmp != None:
            if t == None: ### The close out trade above.
            ### This dummy trade is necessary for the Adjust method.
                s = 'Dummy trade:'
                FCAGeneral.logme(s)
                t = FCAGeneral.create_trade(verb, 0, debug, pp,
                                        ca, ca.insaddr, prf, ca.record_date,
                                        'Closing', q, avgp, 'Spin-off')
            
            pr1 = t.premium_from_quote(ca.record_date, avgp)
            pr2 = t.premium_from_quote(ca.record_date, newp)
            pr3 = pr1 - pr2
            if ins.quote_type == 'Per Unit':
                adj_openp = abs(pr3 / ins.contr_size / openq)
            elif ins.quote_type == 'Per 100 Units':
                adj_openp = abs(pr3 * 100 / openq)
            else: adj_openp = abs(pr3 / openq)

        ### Create new equity trade:
        ### Switched newp to openp
        if not pf:
            e = FCAGeneral.create_trade(verb, commit, debug, pp, 
                ca, ins, prf, ca.record_date, 'Adjust', openq, adj_openp, 
                adj_cash)
            rb.add('Delete', e)
        
        if CA_Method == 'Adjust':
            spintrades[e.prfnbr] = openp, e.curr #e.price, e.curr
            
    if CA_Method == 'Adjust':
        if verb:
            s = '\n### ADJUSTING TRADE HISTORY ###'
            FCAGeneral.logme(s)
        for trd in filtered_trades: #ca.insaddr.trades():
            if FCAGeneral.time_in_interval(ca.record_date, 
                ComparisonDate, cod, trd, verb):
                
                ### Calculate factor for each trade:
                #adj_cash: Already incorporated in spin-off share trade.
                spin_price, spin_curr = spintrades[trd.prfnbr]
                if spin_curr != trd.curr:
                    fx_rate = trd.curr.used_price(ca.ex_date, spin_curr.insid)
                    if verb:
                        s = 'Exchange rate used:%f\nSpinPrice before:%f\n'\
                            'SpinPrice after:%f'\
                            % (fx_rate, spin_price, spin_price / fx_rate)
                        FCAGeneral.logme(s)
                    spin_price = spin_price / fx_rate
                f = (trd.price - spin_price) / trd.price
                    # - adj_cash / trd.quantity) / trd.price
                        
                FCAGeneral.update_trade(commit, verb, ca, trd, rb, f,
                                        adj_trd_q = 0)
    return rb, f
    
"""----------------------------------------------------------------------------
FUNCTION
    split - Function which performs a Stock Split Corporate Action.

DESCRIPTION
    New equity trade(s) are created in the new stock.  Information about what
    is done is saved to the database via the module FCARollback so that
    Rollbacks can be performed to undo the Corporate Action.
----------------------------------------------------------------------------"""

def split(verb, commit, ca, rb, pf, date, pos, filtered_trades, ins, n, o, 
    mtmp, CA_Method, cod = None):

    if ca.ca_type == 'Stock Split':
        try:
            f = o / n
        except ZeroDivisionError:
            raise 'New Quantity can not be 0.'
    elif ca.ca_type == 'Capital Adjustment':
        try:
            f = n / o
        except ZeroDivisionError:
            raise 'Old Quantity can not be 0.'
    elif ca.ca_type in ('Stock Dividend', 'New Issue'):
        try:
            f = o / (n + o)
        except ZeroDivisionError:
            raise 'Old Quantity + New Quantity can not be 0.'
    elif ca.ca_type == 'Buyback':
        if n == o: f = 1.0
        else: f = o / (o - n)

    if CA_Method == 'Close':
        for prf in pos.keys():
            q = pos[prf][0]
            avgp = pos[prf][1]
            if Price == 1:
                adjp = avgp * f
            elif Price == 'MtM':
                avgp = mtmp
                adjp = mtmp * f
            elif Price == 0:
                avgp = 0
                adjp = 0
            adjq = q / f

            if verb:
                s = '\n### CREATING TRADES ###\n'
                FCAGeneral.logme(s)
            ### Create closing trade:
            t = FCAGeneral.create_trade(verb, commit, debug, pp,
                                        ca, ca.insaddr, prf, ca.record_date,
                                        'Closing', q, avgp, 'StockSplit')
            rb.add('Delete', t)

            if not ins:
                ins = ca.insaddr
            ### Create opening trade:
            op = FCAGeneral.create_trade(verb, commit, debug, pp,
                                         ca, ins, prf,
                                         ca.record_date, 'Adjust', adjq,
                                         adjp, 'StockSplit')
            rb.add('Delete', op)

            ### If rounding errors are found, add cash payment for the
            ### difference:
            #if pf: # Not implemented. Workaround: Manually add 1 cash payment.
            FCAGeneral.prem_diff(commit, verb, ca, op,
                t.premium, op.premium, 0.0, 0.0)

    if CA_Method == 'Adjust':
        if verb:
            s = '\n\n### ADJUSTING TRADE HISTORY ###\n'
            FCAGeneral.logme(s)
        for trd in filtered_trades: #ca.insaddr.trades():
            if FCAGeneral.time_in_interval(ca.record_date, 
                ComparisonDate, cod, trd, verb):
                FCAGeneral.update_trade(commit, verb, ca, trd, rb, f,
                                            adj_trd_q = ca.adj_trade_quantity)
    return rb, f

"""----------------------------------------------------------------------------
FUNCTION
    bond_call - Function which performs calls bonds, partially or fully.

DESCRIPTION
    
----------------------------------------------------------------------------"""

def bond_call(verb, commit, ca, rb, pf, pos, ins, n, o, mtmp, cash, quantity, 
    amount_in_percent, price, method):
    """Call bond, fully or partially."""
    
    f = None
    for prf in pos.keys():
        if quantity == None:
            q = pos[prf][0]
        else:
            q = quantity
        if price:
            avgp = price
            openp = price
        elif Price == 1:
            avgp = pos[prf][1]
        elif Price == 0:
            avgp = 0
        elif Price == 'MtM':
            if mtmp != None:
                avgp = mtmp
        if verb:
            s = '\n### CREATING TRADES ###'
            FCAGeneral.logme(s)
    
        ### Create closing trade:
        t = FCAGeneral.create_trade(verb, commit, debug,
            pp, ca, ca.insaddr, prf, ca.record_date, 'Closing', q, avgp, cash)
        rb.add('Delete', t)
    
    return rb, f




