""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE
    FCAAction - Module which executes the Corp Actions listed in the
    CorpAction table.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module executes the Corporate Actions listed in the Corporate Action
    table which have not already been executed, and which have an Ex Date set
    which is on or before the corpact date.
    
NOTE
    The Acquire Day of any trade has to be the same or less than the Record
    Date entered in the Corporate Action table, or they will not be included.
    Furthermore, the Ex Date has to be on or before the 'CorpAct Date' provided
    in the macro variables window in order for the script to include the
    Corporate Action.  Portfolios with a total position of zero, are not
    included.  Trades which are Void, Confirmed Void, Simulated, Reserved or
    Terminated are not included. Only Corporate Actions with one or both of
    the Statuses Instrument or Trade set to 'Script Update' are included.
----------------------------------------------------------------------------"""
import ael
try:
    import string
except ImportError:
    print 'The module string was not found.'
    print
try:
    import FCARollback
except ImportError:
    print 'The module FCARollback was not found.'
    print
try:
    from FCADeleteReferences import *
except ImportError:
    print 'The module FCADeleteReferences was not found.'
    print
try:
    import FCAMisc
except ImportError:
    print 'The module FCAMisc was not found.'
    print
import FCAGeneral
from FCAVariables import *
import FCATypes
reload(FCATypes)
from FCATypes import *
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
    deriv - Function which performs Corporate Actions relevant for derivatives.

DESCRIPTION
    The underlying of the derivatives on a specific instrument is changed if a
    New instrument has been specified. Trades are closed out and opened up or
    adjusted if this has been specified. The name, contract size and strike of
    a derivative are changed if specified in the corporate action.
----------------------------------------------------------------------------"""

def deriv(verb, commit, ca, rb, pf, ins, f, der_ins, CA_Method,
    series_difference = None, cod = None, filter = None):
    """Perform corporate action on derivatives."""
    case  = None
    x     = None
    eurex = None
    renamed = []
    if string.find(string.upper(ca.text), 'EUREX') != -1\
        or (string.upper(Default_Deriv_Exch) == 'EUREX'\
        and string.find(string.upper(ca.text), 'OM') == -1):
        eurex = 1
    elif (string.find(string.upper(ca.text), 'OM') != -1
        or string.upper(Default_Deriv_Exch) == 'OM'):
        eurex = 0
    try:
        if ca.market_ptynbr:
            if ael.Party[ca.market_ptynbr.ptyid]:
            # The above syntax is necessary since if the field is not set, it 
            # equals None, and if it has been set, it is a string, not an
            # entity or ptynbr.
                if ca.market_ptynbr.ptyid == 'EUREX':
                    eurex = 1
                elif ca.market_ptynbr.ptyid in ('OM', ' TOB'):
                    eurex = 0
                else:
                    s = 'Market / Derivative Exchange not supported:%s' %\
                        ca.market_ptynbr.ptyid
                    FCAGeneral.logme(s)
        else:
            eurex = None
    except AttributeError:
        pass
    if eurex == 1:
        adj_trd_q      = 0
        adj_trd_p      = 1
        adj_ins_strike = 1
        adj_ins_cs     = 1
        adj_ins_name   = 1
    elif eurex == 0:
        adj_trd_q      = 1
        adj_trd_p      = 1
        adj_ins_strike = 1
        adj_ins_cs     = 0
        adj_ins_name   = 1
    else:
        adj_trd_q      = ca.adj_trade_quantity
        adj_trd_p      = ca.adj_trade_price
        adj_ins_strike = ca.adj_ins_strike
        adj_ins_cs     = ca.adj_ins_cs
        adj_ins_name   = ca.adj_ins_name

    if ca.ca_type == 'Spin-off':
        adj_trd_q  = 0
    ftemp = f
    for i in der_ins:
        f = ftemp
        too_new = 0
        if ca.ca_ins_status == 'Script Update':
            x = i.clone()
            ael.poll()
            ### Change Strike:
            old_strike = x.strike_price
            if ca.instype == 'Option' and not x.otc:
                ut = ael.date_from_time(x.updat_time)
                ct = ael.date_from_time(x.creat_time)
                if ut < ct:
                    ut = ct
                if verb:
                    s = 'Update time of option %s must be < Ex Date: %s < %s'\
                        % (x.insid, ut, ca.ex_date)
                    FCAGeneral.logme(s)
                if ut >= ca.ex_date:
                    too_new = 1 #Try and find a new name
            if adj_ins_strike:
                new = x.strike_price * f
                if series_difference:
                    x.strike_price = FCAGeneral.serie_round(new, f, 
                        series_difference)
                elif ca.ins_strike_dec == -1:
                    x.strike_price = new
                else:
                    x.strike_price = round(new, ca.ins_strike_dec)
                if debug:
                    s = '\n%s Strike: %s => %s' \
                    % (x.insid, x.strike_price / f, x.strike_price)
                    FCAGeneral.logme(s)

            ### Change Instrument Name of Derivative:
            if adj_ins_name:            
                if ca.ca_type == 'Merger' or too_new == 0:
                    x = FCAGeneral.update_name(ca, x, adj_ins_strike)
                    if debug:
                        s = 'Insid: %s => %s' % (i.insid, x.insid)
                        FCAGeneral.logme(s)

                ### Check if x already exists.
                y = ael.Instrument[x.insid]
                if CA_Method == 'Adjust':
                    if y:
                        case = 3
                        if x.insid == y.insid:
                            s = '\nERROR! Instrument name is not adjusted by '\
                                'the script.  %s' % (i.insid)
                        
                        else:
                            s = '\nERROR! Adjusted instrument already exists,'\
                            ' please use the Close Out method, or delete the '\
                            'instruments if you want to use the Adjust method'\
                            '. %s, %s' % (i.insid, x.insid)
                        raise s
                    else:
                        case = 6
                else:
                    if not too_new:
                        rb = FCAMisc.renameOldInstrument(i, rb, ca.ex_date, commit,
                                                                         debug)
                        renamed.append(i)
                    if y:
                        case = 4
                        old_cs = x.contr_size
                        x = y.clone()
                        x.contr_size = old_cs #Otherwise cs will be adjusted 
                                              #twice
                    else:
                        case = 5
                        n = i.new()
                        n.insid = x.insid
                        n.strike_price = x.strike_price
                        x = n
                        if commit:
                            rb.add('Delete', x)

            else:
                case = 1
                if CA_Method == 'Close':
                    case = 2
                    s = '\nWARNING! If the instrument name is not to be '\
                    'changed, the instrument will be adjusted '\
                    '(i.e. not created new). '\
                    'Therefore the adjust trade method is more natural '\
                    'than the close out method.'
                    FCAGeneral.logme(s)
            ### Update the cloned instrument with strike, cs and insid:
            x = FCAGeneral.update_nominal(commit, debug, pp, ca, x, f,
                            adj_ins_cs, adj_ins_strike, adj_ins_name, eurex,
                            old_strike)
            if eurex:
                f = i.contr_size / x.contr_size # To get the trade price right.

            ### Change underlying of derivatives:
            if ins != None and ca.ca_type in ('Merger', 'Capital Adjustment',
                                           'Stock Split'):
                if verb:
                    s= '\n### CHANGING UNDERLYING ###\n'\
                        'Change underlying of %s: %s => %s' % (x.insid, 
                        ca.insaddr.insid, ins.insid)
                    FCAGeneral.logme(s)
                x.und_insaddr = ins
                case = 7
                if pp: FCAGeneral.logme(x.pp())

            if commit:
                if case in (1, 2, 6, 7):
                    rb.add('Update', i, ['strike_price', 'contr_size', 
                                'phys_contr_size', 'insid', 'und_insaddr',
                                 'extern_id1', 'extern_id2', 'isin'])
                    if x.extern_id1:
                        x.extern_id1 = ''
                    if x.extern_id2:
                        x.extern_id2 = ''
                    if x.isin:
                        x.isin = ''
                    alias_list = []
                    for a in x.aliases():
                        alias_list.append(a)
                    for a in alias_list:
                        new_alias = a
                        new_alias.delete()
                try:
                    if too_new == 0:
                        x.commit()
                except RuntimeError, msg:
                    raise str(msg) + x.insid
        else:
            x = i

        if adj_ins_cs == 1 and adj_trd_q == 1:
            f = 1.0 / f

        if ca.ca_trade_status == 'Script Update' and \
            (adj_trd_p or adj_trd_q):
            filtered_trades = i.trades()
            if filter != None:
                trades_in_ins = i.trades()
                filtered_trades = FCAGeneral.check_if_in_trd_filter(verb,
                    filter, trades_in_ins)

            if CA_Method == 'Close' and too_new == 0:
                ### Calculate the positions in the instrument, per portfolio:
                try:
                    cod = ael.date('1970-01-01') # Do not want CutOffDate
                    trades = []
                    for t in filtered_trades:
                        if FCAGeneral.checkStatus(t):
                            if FCAGeneral.time_in_interval(ca.record_date, 
                                ComparisonDate, cod, t, verb):
                                trades.append(t)
                    pos = FCAGeneral.position(debug, trades, 
                        ca.record_date, pf, Acc_Method, ComparisonDate)
                except IndexError, msg:
                    s = 'No trades in instrument %s, %s.' % (i.insid, msg)
                    FCAGeneral.logme(s)
                else:
                    for prf in pos.keys():
                        q = pos[prf][0]
                        if Price: avgp = pos[prf][1]
                        else: avgp = 0
                        if adj_trd_q:
                            openq = q / f
                        else:
                            openq = q
                
                        
                        if verb:
                            s = '\n### CREATING TRADES ###'
                            FCAGeneral.logme(s)
                        ### Create closing trade:
                        t = FCAGeneral.create_trade(verb, commit, 
                            debug, pp, ca, i, prf, ca.record_date,
                                                'Closing', q, avgp,
                                                'Derivative')
                        rb.add('Delete', t)

                        ### Added to make prices take quote type into
                        ### account:
                        if t:
                            if i.quote_type == 'Per Unit':
                                openp = abs(t.premium / x.contr_size /
                                    openq)
                            elif i.quote_type == 'Per 100 Units':
                                openp = abs(t.premium / x.contr_size /
                                    openq*100)
                            else: openp = abs(t.premium / openq)

                        if adj_trd_p:
                            if Price == 0:
                                openp = 0
                            else:
                                openp = avgp * f
                        else:
                            openp = avgp

                        op = FCAGeneral.create_trade(verb, commit, 
                            debug, pp, ca, x, prf, ca.record_date,
                            'Adjust', openq, openp, 'Derivative')
                        rb.add('Delete', op)

                    ### If rounding errors are found, add cash payment for
                    ### the difference: # See SPR 223686. Corrected 011022.
                        if eurex != 1 and ca.ca_type != 'Stock Split':
                            FCAGeneral.prem_diff(commit, verb, ca, op,
                                t.premium, op.premium, 0.0, 0.0)
            if CA_Method == 'Adjust':
                ael.poll() ### Necessary to assure that premium is updated.

                if adj_trd_p or adj_trd_q:
                    for trd in filtered_trades: #i.trades():
                        if FCAGeneral.time_in_interval(ca.record_date, 
                            ComparisonDate, cod, trd, verb):
                            FCAGeneral.update_trade(commit, verb, ca, 
                                trd, rb, f, adj_trd_q, 
                                adj_trd_p = adj_trd_p, cs = x.contr_size)
                else:
                    if verb:
                        s = '\nTrades will not be adjusted.'
                        FCAGeneral.logme(s)
    if renamed:
        deleteReferences(renamed, commit)
    return rb
     
"""----------------------------------------------------------------------------
FUNCTION
    perform_actions - Function which finds prices and performs the Corporate
    Actions.

DESCRIPTION
    This function decides what functions should be run and in what order. It
    finds MtM prices, positions, derivative instruments and then selects what
    Corporate Action to run, or if to adjust derivatives. Finally, historical
    prices are adjusted if this has been selected in the Corporate Action
    application.
----------------------------------------------------------------------------"""

def perform_actions(ca, verb              = 1, 
                        commit            = 1, 
                        pf                = None, 
                        date              = None,
                        method            = 'Adjust', 
                        series_difference = None, 
                        cod               = None, 
                        filter            = None):
    """Find what CorpActions to perform, and what to do with them."""
    
    if date:
        date = ael.date(date)
    else:
        date = ael.date_today().add_years(20)

    ### Define rollback instance for this Corporate Action:
    FCARollback.test() 
    rb = FCARollback.RollbackInfo(ca)
    
    
    ### Add Additional Info Specifications if they do not already exist:
    if Voluntary == 1:
        FCAGeneral.add_addinfo_spec('CorpAction', 'Portfolio', 
            'CorpAct Portfolio', '', 'RecordRef', 'Portfolio')
        FCAGeneral.add_addinfo_spec('CorpAction', 'Quantity', 
            'CorpAct Quantity', '', 'Standard', 'CorpAction')
        FCAGeneral.add_addinfo_spec('CorpAction', 'Price 1', 
            'CorpAct Price old security', '', 'Standard', 'CorpAction')
        FCAGeneral.add_addinfo_spec('CorpAction', 'Price 2', 
            'CorpAct Price new security', '', 'Standard', 'CorpAction')
        FCAGeneral.add_addinfo_spec('CorpAction', 'CashInstrument',
            'CorpAct Cash instrument', '', 'RecordRef', 'Instrument')

    try:
        if verb:
            if ca.instype == 'Option': der = ' Options on'
            elif ca.instype == 'Future/Forward': der = ' Future/Forwards on'
            elif ca.instype == 'Warrant': der = ' Warrants on'
            elif ca.instype == 'Combination': der = ' Combinations including'
            elif ca.instype == 'EquityIndex': der = ' Equity Indices including'
            else: der = ''
            s = '\n---------------- CORP ACTION ----------------\n\n%s to be '\
                'performed on%s: %s\nEx Date: %s'\
                % (ca.ca_type, der, ca.insaddr.insid, ca.ex_date)
            FCAGeneral.logme(s)

        ### Define common variables:
        f = None
        if ca.new_insaddr:
            try:
                ins = ael.Instrument[ca.new_insaddr]
            except TypeError:
                ins = ael.Instrument[ca.new_insaddr.insaddr]
        else:
            ins = None
        n = ca.new_quantity
        o = ca.old_quantity
        ### Define cash payment amount:
        cash = FCAGeneral.string_parse(ca.text, None)
        try:
            if ca.cash_amount not in ('None', 0.0):
                cash = ca.cash_amount
        except AttributeError, msg:
            pass
        if cash == 'None':
            cash = 0.0
        else:
            try:
                cash = float(cash) #Doesn't work: string.atof(cash)
            except ValueError:
                cash = 0.0   # Wrong cash syntax in the description field.
        if ca.ca_type == 'Spin-off':
            cash1 = FCAGeneral.string_parse(ca.text, ['PF1:'])
            cash2 = FCAGeneral.string_parse(ca.text, ['PF2:'])
            
        ### For Voluntary CorpActs: Find AddInfos
        portf = None
        quantity = None
        price = None
        newprice = None
        cashins = None
        amount_in_percent = 1   # Not used. Maybe we remove it or use it later.
        #for i, j in (('Prf', portf), ('Qty', quantity), 
        #             ('Pr1', price), ('Pr2', newprice),
        #             ('Ins', cashins)):
        for i, j in (('Portfolio', portf), ('Quantity', quantity), 
                     ('Price 1', price), ('Price 2', newprice),
                     ('CashInstrument', cashins)):
            readString = """
ael.AdditionalInfo.read('addinf_specnbr = %s \
and recaddr = %s' % (ael.AdditionalInfoSpec.read('field_name = "CA_""" \
+ i + "\"\').specnbr, ca.seqnbr))"
            try:
                if Voluntary == 1 and eval(readString):
                    try:
                        string = eval(readString).value
                        j = float(eval(readString).value)
                    except ValueError, msg:
                        print msg
                        j = string
            except AttributeError, msg:
                if msg == "'NoneType' object has no attribute 'specnbr'":
                    pass
            if i == 'Portfolio': portf = j
            if i == 'Quantity': quantity = j
            if i == 'Price 1': price = j
            if i == 'Price 2': newprice = j
            if i == 'CashInstrument': cashins = j

        ### Hardcode which database fields should be updated:
        #FCAGeneral.update_ca(debug, ca, CA_Method)
        if rounding in ('infinity',
                        '6_decimals') and ca.trade_price_dec not in (-1, 6):
            FCAGeneral.update_ca(debug, ca, rounding)
        if Voluntary == 1:
            if ca.ca_type in ('Spin-off', 'Stock Split', 'Capital Adjustment',
             'Conversion'):
                FCAGeneral.update_ca(debug, ca, Voluntary)
                ael.poll()
        
        if debug:
            s = '\n\nAdjust Trade Quantity = %i\nAdjust Trade Price = %i\
                \nAdjust Historical Prices = %i\nAdjust Instrument Strike = %i\
                \nAdjust Instrument Contract Size = %i\nAdjust Instrument '\
                'Name = %i\
                \nAdjust Dividends = %i' % (ca.adj_trade_quantity, 
                ca.adj_trade_price, ca.adj_hist_price, ca.adj_ins_strike, 
                ca.adj_ins_cs, ca.adj_ins_name, ca.adj_div)
            FCAGeneral.logme(s)

        filtered_trades = ca.insaddr.trades()
        try:
            if ca.fltnbr != None:
                s = 'Filter %s has been specified.' % ca.fltnbr.fltid
                FCAGeneral.logme(s)
                filt = ca.fltnbr
                if ca.instype not in ('Option', 'Warrant', 'Future/Forward'):
                    trades_in_ins = ca.insaddr.trades()
                #else: Not implemented like this (yet)
                    filtered_trades = FCAGeneral.check_if_in_trd_filter(verb,
                        filt, trades_in_ins)
            else: filt = None
        except AttributeError, msg:
            filt = None

        ### Adjust trades, different procedure depending on corpact-type:
        class_bond = None
        if ca.insaddr.instype in ('Bond', 'Bill', 'Zero', 'FRN', 'PromisLoan'):
            class_bond = 1
        if ca.instype in ('Stock', 'Convertible', 'Bond', 'Bill', 'Zero',
            'FRN', 'PromisLoan') or class_bond == 1:
            if ca.ca_trade_status == 'Script Update' and \
                (ca.adj_trade_price == 1 or ca.adj_trade_quantity == 1):
                ### Calculate the positions in the instrument, per portfolio:
                try:
                    if method == 'Close' \
                        or (ca.ca_type in ('New Issue', 'Stock Dividend', 
                            'Buyback') and ins not in (None, 0))\
                        or ca.ca_type in ('Conversion', 'Merger', 'Spin-off'):
                        cod = ael.date('1970-01-01') # Do not want CutOffDate
                        trades = []
                        if portf == None: #I.e. if not voluntary.
                            for t in filtered_trades:
                                if t.status not in ('Void', 'Confirmed Void',
                                    'Simulated', 'Terminated'):
                                    if FCAGeneral.time_in_interval(
                                        ca.record_date, ComparisonDate, 
                                        cod, t, verb):
                                        trades.append(t)
                            pos = FCAGeneral.position(debug,
                                trades, ca.record_date,
                                pf, Acc_Method, ComparisonDate)
                        else: # For voluntary corporate actions:
                            for t in ael.Portfolio[portf].trades():
                                if t.insaddr == ca.insaddr:
                                    trades.append(t)
                            pos = FCAGeneral.position(debug,
                                trades, ca.record_date,
                                pf, Acc_Method)
                    else:
                        pos = {}
                except IndexError, msg:
                    s = 'No trades in instrument %s, %s.' % (ca.insaddr.insid,
                        msg)
                    FCAGeneral.logme(s)
                    
                else:
                    ### Find MtM Market Price:
                    mtmp = None
                    mtmp2 = None
                    try:
                        if ca.ca_type in ('New Issue', 'Buyback',
                            'Stock Dividend', 'Merger', 'Spin-off')\
                            or Price == 'MtM':
                            if price == None:
                                pr = ca.insaddr.historical_prices().members()
                                mtmp = FCAGeneral.find_mtm_price(debug,
                                    ca, pr, MtM_Market, Max_Days)
                                if verb:
                                    s = '\nChosen MtM/Settle Price: %f' % mtmp
                                    FCAGeneral.logme(s)
                            ### Find MtM Market Price for New instrument:
                            if newprice == None:
                                if (ca.ca_type == 'Spin-off'\
                                    and ins not in (None, 0))\
                                    or (Price == 'MtM'
                                    and ca.ca_type in ('Spin-off', 'Merger')):
                                    pr = ins.historical_prices().members()
                                    mtmp2 = FCAGeneral.find_mtm_price(debug, 
                                        ca, pr, MtM_Market, Max_Days)
                                    if verb:
                                        s = '\nChosen MtM/Settle Price, '\
                                            'second instrument: %f' % mtmp2
                                        FCAGeneral.logme(s)
                    except IndexError, msg:
                        s = 'No MtMPrice/used_price found, %s.' % (msg)
                        raise s
                    
                    ### Select which Corporate Action function to run:
                    try:

                        ### For Voluntary Mergers, Tenders/Buybacks and 
                        ### USA specific Exchanges: #ca.factor == 0.0001
                        if Voluntary == 1 and (ca.ca_type == 'Merger'
                            or ca.ca_type == 'Buyback'):
                            merger(verb, commit, ca, rb, pf, pos, ins, n, o, 
                                mtmp, mtmp2, cash, quantity, amount_in_percent,
                                price, newprice, cashins, method)

                        ### For Callable Bonds: #Voluntary #ca.factor == 0.0001
                        elif ca.instype in ('Bond', 'Bill', 'Zero', 'FRN',
                            'PromisLoan') or ca.insaddr.instype in ('Bond',
                            'Bill', 'Zero', 'FRN', 'PromisLoan'):
                            bond_call(verb, commit, ca, rb, pf, pos, ins, n, o,
                                mtmp, cash, quantity, amount_in_percent, 
                                price, method)
            
                        elif ca.ca_type == 'New Issue': #Mandatory
                            if ca.new_insaddr in (None, 0):
                                FCAGeneral.logme('There is no new Instrument.')
                                split(verb, commit, ca, rb, pf, date, 
                                    pos, filtered_trades, ins,
                                    n, o, mtmp, method, cod = cod)
                            else:
                                rightsdistribution(verb, commit, ca, rb, pf,
                                    pos, filtered_trades, ins, 
                                    n, o, mtmp, cash, quantity, price, 'call', 
                                    method, cod = cod)

                        elif ca.ca_type == 'Buyback': #Mandatory
                            if ca.new_insaddr in (None, 0):
                                FCAGeneral.logme('There is no new Instrument.')
                                split(verb, commit, ca, rb, pf, date, 
                                    pos, filtered_trades, ins,
                                    n, o, mtmp, method, cod = cod)
                            else:
                                rightsdistribution(verb, commit, ca, rb, pf, 
                                    pos, filtered_trades, ins, 
                                    n, o, mtmp, cash, quantity, price, 'put',  
                                    method, cod = cod)

                        elif ca.ca_type == 'Stock Dividend':
                            if ca.new_insaddr in (None, 0):
                                FCAGeneral.logme('There is no new Instrument.')
                                split(verb, commit, ca, rb, pf, date, 
                                    pos, filtered_trades, ins,
                                    n, o, mtmp, method, cod = cod)
                            else:
                                rightsdistribution(verb, commit, ca, rb, pf, 
                                   pos, filtered_trades, ins, n, o, mtmp, cash,
                                   quantity, price, 'call', method, cod = cod)
                                    
                        elif ca.ca_type == 'Merger': # Mandatory
                            merger(verb, commit, ca, rb, pf, pos, ins, n, o,
                                mtmp, mtmp2, cash, quantity, 
                                amount_in_percent, price, newprice, None, 
                                method)
                                   
                        elif ca.ca_type == 'Spin-off': #Mandatory
                            if Voluntary == 1:
                                mtmp = float(cash1)
                                mtmp2 = float(cash2)
                            spin(verb, commit, ca, rb, pf, 
                                pos, filtered_trades, ins, n, o, 
                                mtmp, mtmp2, cash, method, cod = cod)
                                 
                        elif ca.ca_type in ('Stock Split', 
                            'Capital Adjustment'): #Mandatory
                            split(verb, commit, ca, rb, pf, date, 
                                pos, filtered_trades, ins, n,
                                o, mtmp, method, cod = cod)
                                  
                        elif ca.ca_type == 'Conversion': #Mandatory
                            convert(verb, commit, ca, rb, pf, pos, n, o, cash,
                                quantity, amount_in_percent, method)
                            
                    except: 
                        s = '\nWill quit performing this Corporate Action.\n'
                        FCAGeneral.logme(s)
                        raise

        if f == None:
            if n == 0: n = 1
            if o == 0: o = 1
            if ca.ca_type in ('Stock Split', 'Merger'):
                f = o / n ### Example: f = 0.5 if Split 2:1
            elif ca.ca_type in ('New Issue', 'Stock Dividend'):
                f = o / (o + n)
            elif ca.ca_type == 'Buyback':
                if n == o: f = 1.0
                else: f = o / (o - n)
            else:
                f = n / o ### Example: f = 0.8 if Capital Adjustment 0.8:1
                
        ### Adjust derivatives (same procedure for all corpact-types):
        if (ca.instype == 'Option'
            or ca.instype == 'Future/Forward'
            or ca.instype == 'Warrant'):
            der_ins = FCAGeneral.select_deriv(debug, ca)
            ### Added following constraint so that if ONLY HistPr is set to
            ### 'Yes' then no trades (= ONLY HistPr) will be adjusted:
            if ca.adj_hist_price and ca.adj_hist_price not in\
               (ca.adj_trade_price, 
                ca.adj_trade_quantity,
                ca.adj_ins_name, 
                ca.adj_ins_cs, 
                ca.adj_ins_strike):
                pass
            else:
                deriv(verb, commit, ca, rb, pf, ins, f, der_ins, method,
                    series_difference = series_difference, cod = cod, 
                    filter = filt)
        elif ca.instype == 'Convertible':
            der_ins = []

        ### Adjust Equity Index or Combination weights:
        elif (ca.instype == 'EquityIndex' or ca.instype == 'Combination')\
            and (ca.ca_type == 'Stock Split' 
            or ca.ca_type == 'Stock Dividend'):
            der_ins = FCAGeneral.select_deriv(debug, ca)
            rb = FCAGeneral.update_weight(commit, debug, ca.insaddr,
                                          rb, f)
            
        elif (ca.instype == 'EquityIndex' or ca.instype == 'Combination')\
            and ca.ca_type != 'Stock Split' and ca.ca_type != 'Stock Dividend':
            der_ins = []
            s = '\nInvalid Corporate Action. E.g. Combinations are not '\
                'possible to adjust for other Corporate Actions than Stock '\
                'Splits or Stock Dividends.'
            FCAGeneral.logme(s)

        ### Adjust Historical Prices:
        if ca.adj_hist_price:
            eurex = None
            if verb:
                s = '\n### ADJUSTING HISTORICAL PRICES ###'
                FCAGeneral.logme(s)
                s = '\nAdjust Historical %s Prices, %s in %s.'\
                    '\nFactor to adjust hist prices with: %f'\
                    % (ca.instype, ca.ca_type, ca.insaddr.insid, f)
                FCAGeneral.logme(s)

            if (ca.instype == 'Stock'
                or ca.instype == 'EquityIndex'):
                try:
                    der_ins = [ca.insaddr]
                except NameError:
                    s = '\nNameError: There is no derivative instrument\
                     to adjust.\n'
                    FCAGeneral.logme(s)
                    
            for i in der_ins:

                if ca.instype in ('Option', 'Warrant', 'Future/Forward'):
                    import string
                    if string.find(string.upper(ca.text), 'EUREX') != -1\
                        or (string.upper(Default_Deriv_Exch) == 'EUREX'\
                        and string.find(string.upper(ca.text), 'OM') == -1):
                        eurex = 1 ### No quantities will be adjusted.
                    elif (string.find(string.upper(ca.text), 'OM') != -1
                        or string.upper(Default_Deriv_Exch) == 'OM'):
                        eurex = 0 ### Quantities will be adjusted.
                    try:
                        if ca.market_ptynbr != None\
                            and ael.Party[ca.market_ptynbr.ptyid]:
                            if ca.market_ptynbr.ptyid == 'EUREX':
                                eurex = 1
                            elif ca.market_ptynbr.ptyid in ('OM', ' TOB'):
                                eurex = 0
                            else:
                                s = 'Market / Derivative Exchange not '\
                                    'supported:%s' % ca.market_ptynbr.ptyid
                                FCAGeneral.logme(s)
                                eurex = 0
                    except AttributeError:
                        pass
                    if (ca.ca_type == 'Spin-off'):
                        eurex = 1 ### No quantities will be adjusted.
                    if (i.quote_type == 'Per Contract' and eurex == 1):
                        eurex = 2 ### These types of instruments should not 
                                  ### be adjusted.
                    
                pf = i.historical_prices()
                if len(pf) > 0:
                    if verb:
                        s = '\nAdjust price(s) in instrument: %s' %\
                            i.insid
                        FCAGeneral.logme(s)
                    FCAGeneral.update_price(commit, debug, pp, ca, rb,
                                   pf, f, Save_Price_Changes, 
                                   Protected_Markets, eurex)

                else:
                    s = '\nNo prices in instrument %s.\n' % i.insid
                    FCAGeneral.logme(s)
                    
        ### Adjust Dividends:
        #if CA_Method == 'Adjust': # Switched off not to force this on users.
        if ca.adj_div and ca.instype == 'Stock':
            if verb:
                s = '\n### ADJUSTING DIVIDENDS ###'
                FCAGeneral.logme(s)

            div = ael.Dividend.select('insaddr = "%i"' % ca.insaddr.insaddr)
            if debug:
                s = '\nHistorical Dividends to adjust:%s' % div
                FCAGeneral.logme(s)

            for d in div.members():
                if debug:
                    s = '\nHistorical Dividend Record Day (%s) must be <= '\
                        'CorpAct Record Date (%s).' % (d.day, ca.record_date)
                    FCAGeneral.logme(s)
                if d.day <= ca.record_date:
                    FCAGeneral.update_dividend(commit, debug,
                                               ca, d, rb, f)
                    
            stream = ael.DividendStream.select('insaddr = "%i"'
                                                % ca.insaddr.insaddr)
            if debug:
                s = '\nDividend Streams to adjust:%s' % stream
                FCAGeneral.logme(s)
            for d in stream:
                div_est = ael.DividendEstimate.select('stream_seqnbr = "%i"'
                                                        % d.seqnbr)
                if debug:
                    s = '\nDividend Estimates to adjust:%s' % div_est
                    FCAGeneral.logme(s)
                for e in div_est:
                    print e.day
                    print commit
                    FCAGeneral.update_dividend(commit, debug,
                                                    ca, e, rb, f)
    finally:
        if commit:
            rb_list = rb.commit()
            if rb_list != None:
                FCAGeneral.update_done(ca)










