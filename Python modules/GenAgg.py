""" AggregationArchiving:1.3.2.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
    genagg - general aggregation functionality

    (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
        This module contains the main functions needed for performing
        aggregation.  It is not run directly on its
        own but is rather called from the modules agg_equity.py and
        agg_bond.py.

NOTE        
        The aggregation scripts can be run from either a command prompt or from
        the AEL Module Editor within the ATLAS client.  When the scripts are
        run from a command prompt this module must be named genagg.py, and in
        the AEL Module Editor it should be called GenAgg.

ENDDESCRIPTION
----------------------------------------------------------------------------"""
import sys
import time
import string
import math
import ael


""" --- Custom Varibles --- """

""" - max_transaction - 
    Defines the amount of actions to be performed in one data transaction 
    to the SQL server. Decrease this figure if the SQL server's procedure cashe 
    can not handle this amount of actions. A higher figure gives better performance. """

max_transaction = 400


""" - non_agg_trade_statuses -
    This list consists of the trade statuses that should NOT be aggregated. """
    
non_agg_trade_statuses = ['Reserved', 'Void', 'Confirmed Void', 'Simulated', 'FO Confirmed']


""" - used_curr -
    This string states which currency to use when aggregating. These are the possible
    values used_curr can have:
    - 'Accounting'      Use the accounting currency (default)
    - 'Portfolio'       Use the portfolio currency
    - 'Instrument'      Use the instrument currency
    Warning! If other than the above values are set the default currency will be used. """

used_curr = 'Accounting'

""" - realize_daily_settlement - 
    If daily realisation is used, i.e. 'Realize daily settlement' in 
    Accounting Parameters is marked, set realize_daily_settlement to 1, 
    otherwise set it to 0."""
    
realize_daily_settlement = 1

""" Set these payment lists according to the settings in the accounting parameters. """

payments_included_as_fee = ['Assignment Fee', 'Broker Fee', 'Internal Fee',\
                            'Extension Fee', 'Termination Fee', 'Cash']
payments_included_as_cost = []
payments_not_included = []


""" --- End of Variables --- """


def trade_status_clause():
    q = ' '
    for i in non_agg_trade_statuses:
        q= q + 'AND t.status != ' + sv(ael.enum_from_string('TradeStatus', i)) + ' '     
    return q
    
def get_used_curr(insid, prfid):
    if used_curr == 'Instrument':
        curraddr       = sv(ael.Instrument[insid].curr.insaddr)
        currid         = ael.Instrument[insid].curr.insid
    elif used_curr == 'Portfolio':
        curraddr       = sv(ael.Portfolio[prfid].curr.insaddr)
        currid         = ael.Portfolio[prfid].curr.insid            
    else: # 'Accounting' (default)
        curraddr       = sv(ael.Instrument[ael.used_acc_curr()].insaddr)
        currid         = ael.used_acc_curr()
    return (curraddr, currid)        

def not_included(ptype):
    if (ptype == 'Aggregated Settled' or
       ptype == 'Aggregated Accrued' or       
       ptype == 'Aggregated Funding' or
       ptype == 'Aggregated Dividends' or
       ptype == 'Exercise Cash' or
       ptype == 'None'):
        return 1
    for pt in payments_not_included:
        if pt == ptype:
            return 1
    return 0
    
def included_as_fee(ptype):
    if ptype == 'Aggregated Fees':
        return 1
    for pt in payments_included_as_fee:        
        if pt == ptype:
            return 1
    return 0
                   
def included_as_cost(ptype):
    if ptype == 'Premium':
        return 1
    for pt in payments_included_as_cost:
        if pt == ptype:
            return 1       
    return 0

def strip_quotes(value):
    out = ''
    for i in value:
        if i != "\"" and i != "\012":
            out = out + i
    return out


def list_from_string(line, a):
    data = []

    if a: str_list = string.split(line, ',', a)
    else: str_list = string.split(line, ',')

    for i in str_list:
        data.append(string.lstrip(strip_quotes(i)))

    return data


def sv(val):
    if val == None:
        return 'NULL'
    else:
        return `val`
    

def get_compound(p, p_list):
    if p.compound:
        for l in p.links():
            get_compound(l.member_prfnbr, p_list)
    else:
        p_list.append(p.prfid)
    return


def init_values(M):

    agg_user = ael.User['FMAINTENANCE']
    if agg_user == None:
        agg_user = ael.User['AGGREGATE']
        
    if agg_user == None:
        print 'A user called FMAINTENANCE must be defined'
        return -1
    M['agg_user'] = sv(agg_user.usrnbr)

    agg_party = ael.Party['FMAINTENANCE']
    if agg_party == None:
        agg_party = ael.Party['AGGREGATE']
        
    if agg_party == None:
        print 'A party called FMAINTENANCE must be defined'
        return -1
    M['agg_party'] = sv(agg_party.ptynbr)    

    res = ael.dbsql('SELECT getdate()')
    if res[0]:
        now = res[0][0][0]
    else:
        print 'Failed to do gettime()'
        return -1
    M['now'] = sv(now)

    if M['use_daysalive']:
        M['date'] = str(ael.date_today().add_days(M['daysalive']))
    
    M['tstatus_bo']    = sv(ael.enum_from_string('TradeStatus', 'BO Confirmed'))
    M['tstatus_fo']    = sv(ael.enum_from_string('TradeStatus', 'FO Confirmed'))
    M['tstatus_res']   = sv(ael.enum_from_string('TradeStatus', 'Reserved'))
    M['tstatus_sim']   = sv(ael.enum_from_string('TradeStatus', 'Simulated'))
    M['tstatus_void']  = sv(ael.enum_from_string('TradeStatus', 'Void'))

    M['ttype_normal']  = sv(ael.enum_from_string('TradeType', 'Normal'))

    M['ptype_fund']    = sv(ael.enum_from_string('PaymentType', \
                                                 'Aggregated Funding'))
    M['ptype_fee']     = sv(ael.enum_from_string('PaymentType', \
                                                 'Aggregated Fees'))
    M['ptype_cash']    = sv(ael.enum_from_string('PaymentType', 'Cash'))
    M['ptype_premium'] = sv(ael.enum_from_string('PaymentType', 'Premium'))

    M['rectype_trade'] = sv(ael.enum_from_string('B92RecordType', 'Trade'))

    if M['prf_list'] == []:
        M['prf_list'] = ['']
    else:
        prf_list = []
        for p in M['prf_list']:
            prf = ael.Portfolio[p]
            if prf:
                get_compound(prf, prf_list)
            else:
                print '\nPortfolio %s does not exist in the database' % p

        M['prf_list'] = prf_list

    if M['ins_list'] == [] and M['und_list'] == []:
        M['ins_list'] = ['']
    else:
        ins_list = []
        for i in M['ins_list']:
            ins = ael.Instrument[i]
            if ins:
                ins_list.append(ins.insid)
            else:
                print '\nInstrument %s does not exist in the database' % i

        for u in M['und_list']:
            und_ins = ael.Instrument[u]
            if und_ins:
                ins_list.append(und_ins.insid)
                s = ael.Instrument.select('und_insaddr=%d' % und_ins.insaddr)
                for i in s:
                    ins_list.append(i.insid)
            else:
                print '\nInstrument %s does not exist in the database' % u

        M['ins_list'] = ins_list

    return 1


def get_valid_instypes(type, und):

    bond    = ael.enum_from_string('InsType', 'Bond')
    stock   = ael.enum_from_string('InsType', 'Stock')
    option  = ael.enum_from_string('InsType', 'Option')
    warrant = ael.enum_from_string('InsType', 'Warrant')
    future  = ael.enum_from_string('InsType', 'Future/Forward')
    eqindex = ael.enum_from_string('InsType', 'EquityIndex')

    instypes = '(0)'
    if type == 'eq':
        if und:
            instypes = `(0, stock, eqindex)`
        else:
            instypes = `(stock, option, future, warrant)`
    elif type == 'bond':
        if und:
            instypes = `(0, bond, future)`
        else:
            instypes = `(bond, option, future)`        

    return instypes


def init_eq_values(M):

    if M['given_instype'] == '':
        M['instype_list'] = get_valid_instypes('eq', 0)
    else:
        instype_list = []
        for instype in M['given_instype']:
            if instype != 'Stock' and instype != 'Option' and \
               instype != 'Future/Forward' and instype != 'Warrant':
                print 'Supplied Instype must be either of Stock,'
                print 'Option, Future/Forward and Warrant'
                return -1
            else:
                instype_list.append(ael.enum_from_string('InsType', instype))
        M['instype_list'] = string.replace(string.replace(str(instype_list), \
                                                          '[', '('), ']', ')')

    M['valid_und_instype_list'] = get_valid_instypes('eq', 1)
    
    M['ptype_div'] = sv(ael.enum_from_string('PaymentType', \
                                             'Aggregated Dividends'))
    return 1


def init_bond_values(M):

    if M['given_instype'] == '':
        M['instype_list'] = get_valid_instypes('bond', 0)
    else:
        instype_list = []
        for instype in M['given_instype']: 
            if instype != 'Bond' and instype != 'Option' and \
               instype != 'Future/Forward':
                print 'Supplied Instype must be either of Bond,'
                print 'Option and Future/Forward '
                return -1
            else:
                instype_list.append(ael.enum_from_string('InsType', instype))
        M['instype_list'] = string.replace(string.replace(str(instype_list), \
                                                          '[', '('), ']', ')')

    M['valid_und_instype_list'] = get_valid_instypes('bond', 1)

    M['ptype_settled'] = sv(ael.enum_from_string('PaymentType', \
                                               'Aggregated Settled'))
    M['ptype_accrued'] = sv(ael.enum_from_string('PaymentType', \
                                               'Aggregated Accrued'))
    return


def init_repo_values(M):

    repo    = ael.enum_from_string('InsType', 'Repo/Reverse')
    buse    = ael.enum_from_string('InsType', 'BuySellback')
    secloan = ael.enum_from_string('InsType', 'SecurityLoan')
    deposit = ael.enum_from_string('InsType', 'Deposit')
    collateral = ael.enum_from_string('InsType', 'Collateral')

    a = M.get('given_instype', '')

    if a != '':
        instype_in = ael.enum_from_string('InsType', a)
        if instype_in != collateral and instype_in != buse and \
           instype_in != deposit and instype_in != repo and \
           instype_in != secloan:
            print 'Supplied Instype must be either of Repo/Reverse,'
            print 'Collateral, Deposit, SecurityLoan and BuySellback'
            sys.exit(2)
        else:
            instype_string = '(' + `instype_in` + ')'
            M['instype_list']=instype_string
            instype_tuple = [repo, collateral, deposit, buse, secloan]
            i = 0
            while i < 5:
                if instype_tuple[i] != instype_in:
                    instype_tuple[i] = -1
                i = i + 1
                    
    else:
        instype_tuple = (repo, collateral, deposit, buse, secloan)
        M['instype_list']=sv(instype_tuple)

    M['instype_repo']       = sv(instype_tuple[0])
    M['instype_collateral'] = sv(instype_tuple[1])
    M['instype_deposit']    = sv(instype_tuple[2])
    M['instype_buse']       = sv(instype_tuple[3])
    M['instype_secloan']    = sv(instype_tuple[4])

    M['rectype_trade']=sv(ael.enum_from_string('B92RecordType', 'Trade'))
    M['rectype_ins']=sv(ael.enum_from_string('B92RecordType', 'Instrument'))

    M['ptype_settled'] = sv(ael.enum_from_string('PaymentType', \
                                               'Aggregated Settled'))
    M['ptype_accrued'] = sv(ael.enum_from_string('PaymentType', \
                                               'Aggregated Accrued'))

    return


def init_deagg_values(M):

    M['rectype_trade']=sv(ael.enum_from_string('B92RecordType', 'Trade'))
    M['rectype_ins']=sv(ael.enum_from_string('B92RecordType', 'Instrument'))

    return


def get_ini_values(M, type, inifile):

    date = 0
    daysalive = 0
    use_daysalive = 0
    atlas_user = 0
    ads_address = 0
    atlas_password = ''
    prf_from = ''
    prf_to   = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    prf_list = []
    given_prf = ''
    ins_from = ''
    ins_to   = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz'
    ins_list = []
    given_ins = ''
    und_list = []
    given_und = ''
    given_instype = ''
    arch_from = 0
    arch_to   = 0
    cl_pl_time = '1970-01-01 00:00:00'
    no_of_trades = 3
    correct_agg = 'Aggregate'
    verbose   = 0

    in_data = open(inifile)
    while  1:
        line=in_data.readline()
        if not line:
            break
        data_list = list_from_string(line, 1)
        try:
            o = data_list[0]
            a = data_list[1]
        except:
            continue
        if a and o:
            if o == '-date':
                date = a
            if o == '-daysalive':
                daysalive = int('-' + a)
                use_daysalive = 1
            if o == '-atlasuser': atlas_user = a
            if o == '-atlaspassword': atlas_password = a
            if o == '-adsaddress': ads_address = a
            if o == '-portfolio':
                prf_from = a
                prf_to = a
                given_prf = a
                prf_list = list_from_string(a, 0)
            if o == '-instrument':
                ins_from = a
                ins_to = a
                given_ins = a
                ins_list = list_from_string(a, 0)
            if o == '-underlying':
                given_und = a
                und_list = list_from_string(a, 0)
            if o == '-archive':
                arch_to = int(a)
            if o == '-verbose':
                verbose = int(a)
            if o == '-instype':
                given_instype = list_from_string(a, 0)
            if o == '-ClearPLTime':
                cl_pl_time = a
            if o == '-positionsize':
                no_of_trades = int(a)
            if o == '-action':
                correct_agg = a

    if ((correct_agg == 'Aggregate' or correct_agg == 'CorrectAndAggregate') and \
        date == 0 and use_daysalive == 0) or \
       atlas_user == 0 or ads_address == 0:
        help_text(type)
        
    elif (correct_agg == 'Aggregate' or correct_agg == 'CorrectAndAggregate') and \
         date != 0 and use_daysalive != 0:
        print 'Cannot use both -date and -daysalive at the same time.'
        sys.exit(2)

    M['date']           = date
    M['daysalive']      = daysalive
    M['use_daysalive']  = use_daysalive
    M['atlas_user']     = atlas_user
    M['ads_address']    = ads_address
    M['atlas_passwd']   = atlas_password
    M['prf_from']       = sv(prf_from)
    M['prf_to']         = sv(prf_to)
    M['prf_list']       = prf_list
    M['given_prf']      = given_prf
    M['ins_from']       = sv(ins_from)
    M['ins_to']         = sv(ins_to)
    M['ins_list']       = ins_list
    M['given_ins']      = given_ins
    M['und_list']       = und_list
    M['given_und']      = given_und
    M['given_instype']  = given_instype
    M['arch_from']      = sv(arch_from)
    M['arch_to']        = sv(arch_to)
    M['cl_pl_time']     = sv(cl_pl_time)
    M['no_of_trades']   = sv(no_of_trades)
    M['correct_agg']    = correct_agg
    M['verbose']        = verbose

    return


def store_variables(M, dictionary):

    date = '1970-01-01'
    use_date = 0
    daysalive = 0
    use_daysalive = 1
    prf_list = []
    given_prf = ''
    ins_list = []
    given_ins = ''
    und_list = []
    given_und = ''
    given_instype = ''
    arch_from = 0
    arch_to   = ael.archived_mode()
    cl_pl_time = '1970-01-01 00:00:00'
    no_of_trades = 3
    correct_agg = 'Aggregate'
    verbose   = 0

    if dictionary['date']:
        date = dictionary['date'].to_string()
        use_daysalive = 0
    if dictionary['daysalive']:
        daysalive = int('-' + str(dictionary['daysalive']))
    if dictionary['portfolio']:
        given_prf = dictionary['portfolio']
        prf_list = dictionary['portfolio'] 
    if dictionary['instrument']:
        given_ins = dictionary['instrument']
        ins_list = dictionary['instrument'] 
    if dictionary['underlying']:
        given_und = dictionary['underlying']
        und_list = dictionary['underlying'] 
    if dictionary['verbose']:
        verbose = dictionary['verbose']
    if dictionary['instype']:
        given_instype = dictionary['instype']
    if dictionary['positionsize']:
        no_of_trades = dictionary['positionsize']
    if dictionary['correctagg']:
        correct_agg = dictionary['correctagg']
    if dictionary['ClearPLTime']:
        cl_pl_time = dictionary['ClearPLTime']

    if (correct_agg == 'Aggregate' or correct_agg == 'CorrectAndAggregate') and \
       use_daysalive == 0 and daysalive:
        print 'Cannot use both Date and Days Alive at the same time'
        return -1

    if given_prf == '' and given_ins == '' and given_und == '' \
       and given_instype == '' and \
       (correct_agg == 'Aggregate' or correct_agg == 'CorrectAndAggregate'):
        print 'At least one of Instrument, underlying, Instype and ' + \
              'Portfolio must be specified'
        return -1

    if verbose:
        if arch_to:
            not_str = ''
        else:
            not_str = 'not '
        print '\nApplication is ' + not_str + 'using archived data'
        print 'Dearchivation is ' + not_str + 'possible'

    M['date']           = date
    M['daysalive']      = daysalive
    M['use_daysalive']  = use_daysalive
    M['prf_list']       = prf_list
    M['given_prf']      = given_prf
    M['ins_list']       = ins_list
    M['given_ins']      = given_ins
    M['und_list']       = und_list
    M['given_und']      = given_und
    M['given_instype']  = given_instype
    M['arch_from']      = sv(arch_from)
    M['arch_to']        = sv(arch_to)
    M['cl_pl_time']     = sv(cl_pl_time)
    M['no_of_trades']   = sv(no_of_trades)
    M['correct_agg']    = correct_agg
    M['verbose']        = verbose

    return 1


def get_ini_values_no_agg(M, inifile):

    date = 0
    atlas_user = 0
    ads_address = 0
    atlas_password = ''
    verbose   = 0

    in_data = open(inifile)
    while  1:
        line=in_data.readline()
        if not line:
            break
        data_list = list_from_string(line, 1)
        try:
            o = data_list[0]
            a = data_list[1]
        except:
            continue
        if a and o:
            if o == '-atlasuser': atlas_user = a
            if o == '-atlaspassword': atlas_password = a
            if o == '-adsaddress': ads_address = a
            if o == '-date':
                date = a
            if o == '-verbose':
                verbose = 1
            if o == '-instype':
                instype = a
                M['given_instype'] = a

    if date == 0 or atlas_user == 0 or ads_address == 0:
        help_text_no_agg()
        
    M['date']        = date
    M['atlas_user']  = atlas_user
    M['ads_address']  = ads_address
    M['atlas_passwd']= atlas_password
    M['verbose']     = verbose

    return


def get_ini_values_deagg(M, inifile):

    atlas_user = 0
    ads_address = 0
    atlas_password = ''
    trdnbr = 0
    verbose   = 0

    in_data = open(inifile)
    while  1:
        line=in_data.readline()
        if not line:
            break
        data_list = list_from_string(line, 1)
        try:
            o = data_list[0]
            a = data_list[1]
        except:
            continue
        if a and o:
            if o == '-atlasuser': atlas_user = a
            if o == '-atlaspassword': atlas_password = a
            if o == '-adsaddress': ads_address = a
            if o == '-trdnbr':
                sv_trdnbr = sv(a)
                trdnbr = a
            if o == '-verbose':
                verbose = 1

    if trdnbr == 0 or atlas_user == 0 or ads_address == 0:
        help_text_deagg()
        
    M['deagg_trdnbr']    = trdnbr
    M['sv_deagg_trdnbr'] = sv_trdnbr
    M['atlas_user']  = atlas_user
    M['ads_address']  = ads_address
    M['atlas_passwd']= atlas_password
    M['verbose']     = verbose

    return


def help_text_mandatory():

    print 'The inifile could not be properly read.'
    print ''
    print 'Tag            Default              Description'
    print '-----------------------------------------------'
    print 'The following values are required:'
    print ''
    print '-atlasuser,    -                    name of atlas user'
    print '-adsaddress,   -                    name of ads address'
    print ''
    print ''
    print 'If -action is set to Aggregate or CorrectAndAggregate'
    print 'exactly one of the following values must be specified:'
    print ''
    print '-date,         -                    latest val day for incl trades'
    print '-daysalive,    -                    number of days to keep trades'
    print ''
    print ''
    print 'Optional values are:'
    print ''

    return


def help_text_bond():

    print '-instype,      Bond,                list of instrument types to aggregate'
    print '               Option,'
    print '               Future '

    return


def help_text_eq():

    print '-instype,      Stock,               list of instrument types to aggregate'
    print '               Option,'
    print '               Future, '
    print '               Warrant '

    return


def help_text_repo():

    print '-instype,      Repo/Reverse,        list of instrument types to aggregate'
    print '               Collateral,'
    print '               SecurityLoan, '
    print '               BuySellback, '
    print '               Deposit '

    return


def help_text(inst_type):

    help_text_mandatory()

    print '-atlaspassword,-                    atlas password'
    print '-action,       Aggregate        One of Check, Correct, Aggregate and'
    print '                                    CorrectAndAggregate'
    print '-portfolio,    all                  list of names of portfolios'
    print '-instrument,   all                  list of names of instruments'
    print '-underlying,   all                  list of names of underlyings'

    if inst_type == 'bond':
        help_text_bond()
    elif inst_type == 'eq':
        help_text_eq()
    elif inst_type == 'repo':
        help_text_repo()

    print '-ClearPLTime,  1970-01-01 00:00:00  when P&L was last cleared'
    print '-positionsize, 3                    required minimum position size'
    print '-archive,      0                    1 if dearchive or reaggregating, or if'  
    print '                                    -action is set to Correct or CorrectAndAggregate' 
    print '-verbose,      0                    1 if you want printouts'

    sys.exit(2)


def help_text_no_agg():

    help_text_mandatory()

    print '-instype,      Repo/Reverse,       Instrument type to archive'
    print '               BuySellBack,'
    print '               Deposit,'
    print '               SecurityLoan,'
    print '               Collateral'
    print '-verbose,      0                   1 if you want printouts'

    sys.exit(2)


def help_text_deagg():

    print 'Inifile must contain the following values:'
    print 'Tag            Default             Description'
    print '====================================================='
    print '-atlasuser,    -                   name of atlas user'
    print '-adsaddress,   -                   name of ads address'
    print '-trdnbr,       -                   aggregate trade to deaggregate'
    print ''
    print 'Optional values are:'
    print '--------------------'
    print '-atlaspassword,-                   atlas password'
    print '-verbose,      0                   1 if you want printouts'

    sys.exit(2)

def get_positions(M, prf, ins_list, date):
        
    pos = []

    if prf <> '':
        prf_clause = "AND p.prfid = '%s'" % (prf)
    else:
        prf_clause = ''

    for ins in ins_list:
        if ins:
            ins_clause = "AND i.insid = '%s'" % (ins)
        else:
            ins_clause = ''

        q = ' \
        SELECT \
                count(t.trdnbr),\
                t.insaddr, \
                i.insid, \
                t.prfnbr, \
                p.prfid, \
                i.curr, \
                c.insid \
        FROM \
                instrument i, \
                instrument c, \
                portfolio p, \
                trade t \
        WHERE \
                i.instype in ' + M['instype_list'] + '\
        AND     i.und_instype in ' + M['valid_und_instype_list'] + '\
        AND     i.curr = c.insaddr \
        AND t.insaddr = i.insaddr '\
        + ins_clause + '\
        AND     t.prfnbr != NULL \
        AND     t.prfnbr = p.prfnbr '\
        + prf_clause + '\
        AND     t.value_day < ' + `date` \
         + trade_status_clause() + '\
        AND     t.archive_status >= ' + M['arch_from'] + ' \
        AND     t.archive_status <= ' + M['arch_to'] + ' \
        AND     t.time > ' + M['cl_pl_time'] + ' \
        GROUP BY t.prfnbr,p.prfid, t.insaddr, i.insid, i.curr, c.insid \
        HAVING count(t.trdnbr) > ' + M['no_of_trades']
        
        positions = ael.dbsql(q)

        if positions[0]:
            pos = pos + positions[0]

        if M['arch_to'] == '1':
            # Try to find positions that were opened after this date, but
            # which now should be deaggregated, i.e. that did not fit our
            # first select.
            q2 = ' \
            SELECT      count(t.trdnbr),\
                        t.insaddr, \
                        i.insid, \
                        t.prfnbr, \
                        p.prfid, \
                        i.curr, \
                        c.insid \
            FROM \
                        instrument i, \
                        instrument c, \
                        portfolio p, \
                        trade t \
            WHERE \
                        i.instype in ' + M['instype_list'] + '\
            AND         i.und_instype in ' + M['valid_und_instype_list'] + '\
            AND         i.curr = c.insaddr \
            AND         i.insaddr = t.insaddr '\
            + ins_clause + '\
            AND         t.prfnbr != NULL \
            AND         p.prfnbr = t.prfnbr '\
            + prf_clause  \
            + trade_status_clause() + '\
            AND         t.aggregate = 0 \
            AND         t.archive_status = 1 \
            AND         t.time > ' + M['cl_pl_time'] + ' \
            GROUP BY t.prfnbr,p.prfid,t.insaddr,i.insid,i.curr,c.insid \
            HAVING (count(t.trdnbr) > 0 \
            AND         min(t.value_day) >= ' + `date` + ')'
    
            positions2 = ael.dbsql(q2)
        
            if positions2[0]:
                pos = pos + positions2[0]
        
    return pos


def get_trades(M, insaddr, prfnbr, trades, date):

    agg_from = '0'
    if M['arch_to'] == '1':
        agg_to = '0'
    else:
        agg_to = '1'

    time = `date + ' 00:00:00'`

    q = ' \
    SELECT      t.trdnbr \
    FROM \
            trade t \
    WHERE \
            t.insaddr = ' + insaddr + ' \
    AND         t.prfnbr = ' + prfnbr + ' \
    AND         t.value_day < ' + `date` + ' \
    AND         t.time < ' + time + ' \
    AND         t.time > ' + M['cl_pl_time'] \
    + trade_status_clause() + '\
    AND         t.aggregate >= ' + agg_from + ' \
    AND         t.aggregate <= ' + agg_to   + ' \
    AND         t.archive_status >= ' + M['arch_from'] + ' \
    AND         t.archive_status <= ' + M['arch_to'] + ' \
    ORDER BY t.time'
    
    trdnbrs = ael.dbsql(q)
    
    if trdnbrs[0]:
        for row in trdnbrs[0]:
            trdnbr = row[0]
            tmp = ael.Trade[trdnbr]
            if tmp == None:
                print 'Got trade from sybase that is not accessible from ael'
                print 'Trdnbr = ', trdnbr
                print 'Can not go on aggregating.'
                return -1
            trades.append(tmp)

    return 1


def insert_payment(M, pay_day, pay_type, amount, text, agg_trd, curraddr):

    if agg_trd:
        p = ael.Payment.new(agg_trd)
        p.type           = ael.enum_to_string('PaymentType', int(pay_type))
        p.payday         = pay_day
        p.amount         = amount
        p.curr           = int(curraddr)
        p.ptynbr         = int(M['agg_party'])
        p.text           = text
        p.archive_status = 0
        p.creat_usrnbr   = int(M['agg_user'])
        p.creat_time     = ael.date_today().to_time()
        p.updat_usrnbr   = int(M['agg_user'])
        p.updat_time     = ael.date_today().to_time()
        
    return
 
def calc_aggregate(trades, M, insaddr, prfnbr, curraddr, currid, date, inst_type):
    
    d0 = ael.date('1970-01-01')
    d1 = ael.date(date)
    if len(trades) > 0:
        agg_time = trades[-1].time
    else:
        agg_time = d1.to_time()
    agg_time = max(agg_time, 43200)     # 43200 = 1970-01-01 12:00:00 PM 
                                        # To avoid problems with stepping before "beginning of time" when 
                                        # adjusting the trade time between UTC and different local time zones 

    c  = ael.Instrument[currid]
    i  = ael.Instrument[int(insaddr)]

    if inst_type == 'bond' and i.exp_day <= d1:
        if i.instype == 'Bond':
            d1 = i.exp_day.add_period('-' + i.ex_coup_period)
            d1 = d1.add_days(-1)
        else:
            d1 = i.exp_day

    elif inst_type == 'eq' and i.exp_day != None and i.exp_day <= d1:
        if (i.instype == 'Future/Forward'
         or i.instype == 'Option'
         or i.instype == 'Warrant'):
            d1 = max(i.exp_day, trades[-1].value_day)

    rpl = ael.rpl(trades, d0, d1, c, 'Open Average', 3)    

    pos  = 0
    fees = 0
    fund = 0
    divid = 0
    divid_fund = 0
    fut_div= {}
    fut_div['amount'] = 0
    rpl_div = 0
    fees_in_rpl = 0
    fut_fees_in_rpl = 0
    fut_premium = 0
    fut_pays = []
    int_settled = 0
    int_accrued = 0
    
    for trd in trades:
        pos  = pos + trd.quantity
        fees = fees + trd.fee
        fees_in_rpl = fees_in_rpl + trd.fees(d0, d1, currid, 3)
        fund = fund + trd.accumulated_funding(d1, currid, 3, 0, '', 0, 'Continuous')
        
        for p in trd.payments(): 
            if p.payday > d1 and not_included(p.type) == 0 and inst_type == 'eq':
                
                amount = p.amount * p.curr.market_value(ael.date_today(), currid) 
                fp = {}
                include_fp = 0
                
                if included_as_fee(p.type):
                    fut_fees_in_rpl = fut_fees_in_rpl + amount
                    fp['type'] = M['ptype_fee']
                    include_fp = 1
                    
                elif included_as_cost(p.type):                    
                    fp['type'] = M['ptype_premium']
                    fut_premium = fut_premium + amount
                    include_fp = 1
                
                fp['date'] = p.payday
                fp['amount'] = amount

                if include_fp == 1:
                    if len(fut_pays) == 0:
                        fut_pays.append(fp)
                    else:
                        found = 0
                        counter = 0
                
                        while found == 0 and counter < len(fut_pays):                
                            if fut_pays[counter]['date'] == fp['date'] and \
                               fut_pays[counter]['type'] == fp['type']:
                           
                                fut_pays[counter]['amount'] = fut_pays[counter]['amount'] + fp['amount']
                                found = 1
                            else:
                                counter = counter + 1
                    
                        if found == 0:
                            fut_pays.append(fp)
                     
        if inst_type == 'eq':
            divid = divid + trd.accumulated_dividend(d1, currid, 3, 0, '', 0, 'None') 
            divid_fund = divid_fund + trd.accumulated_dividend(d1, currid, 3, 0, '', 0, 'Continuous')

            for d in i.dividends(ael.date('2525-01-01')):

                if ( ael.date(date) <= d.pay_day and trd.value_day <= d.day ):

                    if ( ael.date(date) < d.pay_day and ael.date(date) > d.day ):
                        div_amount= trd.accumulated_dividend(d.pay_day, currid, 3, 0, '', 0, 'None') -\
                                    trd.accumulated_dividend(d.pay_day.add_delta(-1, 0, 0), currid, 3, 0, '', 0, 'None')                                  
                        fut_div['amount'] = fut_div['amount'] + div_amount
                        fut_div['date'] = d.pay_day

                    elif ( ael.date(date) <=  d.day ):
                        adjusted_date = ael.date(date)
                        adjusted_date = adjusted_date.add_banking_day(c, i.spot_banking_days_offset)
                        adjusted_date = adjusted_date.add_days(-1)

                        if ( d.day <= adjusted_date ):
                            div_amount = trd.accumulated_dividend(d.pay_day, currid, 3, 0, '', 0, 'None') -\
                                         trd.accumulated_dividend(d.pay_day.add_delta(-1, 0, 0), currid, 3, 0, '', 0, 'None')
                            rpl_div = rpl_div + div_amount

                            """ Special for removing dividends from agg_pl that are included in rpl() 
                                but not in accumulated_dividends() - see 'get_dividends()' in accounting.c:
                                Dividends are included in rpl() where record day is at most date + spot - 1"""
                

                if  ( d1 == d.day and d1 == d.pay_day ):
                    divid = divid - trd.accumulated_dividend(d1, currid, 3, 0, '', 0, 'None') -\
                                    trd.accumulated_dividend(d1.add_delta(-1, 0, 0), currid, 3, 0, '', 0, 'None')
                    divid_fund = divid_fund - trd.accumulated_dividend(d1, currid, 3, 0, '', 0, 'Continuous') -\
                                    trd.accumulated_dividend(d1.add_delta(-1, 0, 0), currid, 3, 0, '', 0, 'Continuous')

        else:
            int_settled = int_settled + trd.interest_settled(d0, d1, currid)
            int_accrued = int_accrued + trd.interest_accrued(d0, d1, currid)

    divid_fund = divid_fund - divid
    
    if abs(pos) < 1e-12:
        pos = 0

    if (inst_type == 'eq'):
        pos = i.ca_adjust_trade_quantity(d1, pos, 0)
        fees = 0
        agg_pl = rpl - fees_in_rpl - divid - fut_div['amount'] - rpl_div
        
        if (i.paytype == 'Spot'):
            avg_price = ael.avg_price(trades, d1, c, 'Open Average', 3)
            avg_price = i.ca_adjust_trade_price(d1, avg_price, 0)
            premium = i.premium_from_quote(d1, avg_price) * pos - fut_premium
        
    else:   #inst_type == 'bond'
        agg_pl = rpl - int_accrued - int_settled - fees_in_rpl
        
        if (i.paytype == 'Spot'):
            avg_price = ael.avg_price(trades, d1, c, 'Open Average', 3)

            if i.round_clean < 10:
                # Have to fix the fact that the premium might not correspond
                # to the sum_of_cost, which is the base for average price,
                # the premium might be rounded, as in Sweden.
                i_copy = i.clone()
                i_copy.round_clean = 11
                premium = i_copy.premium_from_quote(d1, avg_price) * pos
            else:
                premium = i.premium_from_quote(d1, avg_price) * pos

    # Futures, Forwards on both Equities and Bonds:
    # If Realize daily: set the avg_price to the mark to market price.
    # If NOT Realize daily: set the avg_price to avg_price(), 
    # except when aggregation date >= expiry day - then use the mark to market price,
    # because rpl() settles the position on the expire day to the mark to market price.
    # When the aggregation date (or the date for getting the price) is today - 
    # use the avg_price(), as there is no mark to market price available yet.
    if (i.paytype != 'Spot'):
        premium = 0
        divid = 0
        if pos == 0:
            avg_price = 0
        else:
            mtm_day = min(d1, i.exp_day)
            if ((realize_daily_settlement or d1 >= i.exp_day) and
                 mtm_day < ael.date_today()):                    
                avg_price = i.mtm_price(mtm_day, currid, 1)
                if (avg_price == 0):
                    print '\nWarning!: Could not find mark to market price for %s on %s.' % \
                        (i.insid, mtm_day)
            else:
                avg_price = ael.avg_price(trades, d1, c, 'Open Average', 3)
                if (inst_type == 'eq'):
                    avg_price = i.ca_adjust_trade_price(d1, avg_price, 0)   


    
    if M['verbose'] == 1:
        print 'date    = ', d1
        print 'rpl     = ', rpl
        print 'avg     = ', avg_price
        print 'pos     = ', pos
        print 'fees    = ', fees + fees_in_rpl
        print 'fund    = ', fund   

        if inst_type == 'eq':
            print 'divid   = ', divid
        else:
            print 'settled = ', int_settled
            print 'accrued = ', int_accrued

        print 'premium = ', premium
        print 'agg_pl  = ', agg_pl
        print


    """Get the aggregate trade if there exists one"""
    q = ' \
    SELECT      t.trdnbr, \
                t.value_day \
    FROM \
                trade t \
    WHERE \
                t.insaddr = ' + insaddr + ' \
    AND         t.prfnbr = ' + prfnbr + ' \
    AND         t.aggregate != 0'

    agg_trade = ael.dbsql(q)

    agg_trd = None
    agg_trdnbr = 0

    if agg_trade[0]:
        agg_trdnbr = sv(agg_trade[0][0][0])
        try:
            val_day = ael.date(string.split(agg_trade[0][0][1], ' ')[0])
        except:
            val_day = agg_trade[0][0][1]
                
        agg_trd = ael.Trade[int(agg_trdnbr)]

        if agg_trd.value_day > d1 and M['arch_to'] == '0':
            print 'Date is %s but there is an aggregate trade with value ' \
            'day %s.\nTo reaggregate this position use the -archive ' \
            'option for the script or run the script from a client in ' \
            'archive  mode.' % (d1, val_day)
            return -1

        t = agg_trd.clone()

        p_sel = t.payments()
        while 1:
            try:
                p = p_sel[0]
            except:
                break
            p.delete()

        t.protection   = 'W:RW,O:RW,G:RW,U:RW' # 3510
        t.acquire_day  = d1
        t.value_day    = d1
        t.time         = agg_time
        t.quantity     = pos
        t.price        = avg_price
        t.curr         = c
        t.trade_curr   = c
        t.premium      = premium
        t.fee          = fees
        t.updat_usrnbr = int(M['agg_user'])
        t.updat_time   = ael.date_today().to_time()
        t.aggregate_pl = agg_pl

        if M['arch_to'] == '1':
            t.aggregate = 1

        agg_trd = t
 
    else:
        """Create an aggregate trade"""
        agg_trd = ael.Trade.new(i)
        agg_trd.prfnbr = int(prfnbr)
        agg_trd.insaddr = int(insaddr)
        agg_trd.acquire_day = d1
        agg_trd.curr = c
        agg_trd.trade_curr = c
        agg_trd.value_day = d1
        agg_trd.time = agg_time
        agg_trd.quantity = pos
        agg_trd.price = avg_price
        agg_trd.premium = premium
        agg_trd.fee = fees
        agg_trd.aggregate_pl = agg_pl
        agg_trd.counterparty_ptynbr = int(M['agg_party'])
        agg_trd.acquirer_ptynbr =  int(M['agg_party'])
        agg_trd.status = 'BO Confirmed'
        agg_trd.type = 'Normal'
        agg_trd.aggregate = 1
        agg_trd.archive_status = 0
        agg_trd.trader_usrnbr = int(M['agg_user'])
        agg_trd.creat_usrnbr = int(M['agg_user'])
        agg_trd.creat_time = ael.date_today().to_time()
        agg_trd.updat_usrnbr = int(M['agg_user'])
        agg_trd.updat_time = ael.date_today().to_time()
        agg_trd.protection = 'W:RW,O:RW,G:RW,U:RW' # 3510
        agg_trd.owner_usrnbr = int(M['agg_user'])


    if inst_type == 'eq':
        if divid != 0:
            insert_payment(M, d1, M['ptype_div'], divid, '', agg_trd, curraddr)
                          
        if (fees_in_rpl - fut_fees_in_rpl) != 0:
            insert_payment(M, d1, M['ptype_fee'], fees_in_rpl - fut_fees_in_rpl, '',
                           agg_trd, curraddr)  
                           
        if fut_div['amount'] != 0:
            insert_payment(M, fut_div['date'], M['ptype_div'], fut_div['amount'], '',
                           agg_trd, curraddr)       
               
    else:
        if int_settled != 0:
            insert_payment(M, d1, M['ptype_settled'], int_settled,
                           'Aggr Settled', agg_trd, curraddr)

        if int_accrued != 0:
            insert_payment(M, d1, M['ptype_accrued'], int_accrued, '',
                           agg_trd, curraddr)

    if fund != 0:
        insert_payment(M, d1, M['ptype_fund'], fund, '', agg_trd, curraddr)
        
    if divid_fund != 0:
        insert_payment(M, d1, M['ptype_fund'], divid_fund, "Dividend funding", agg_trd, curraddr)
        
    for fp in fut_pays:
        if fp['amount'] != 0:
            insert_payment(M, fp['date'], fp['type'], fp['amount'], 'Aggr future payment',
                           agg_trd, curraddr)        
    
    if agg_trd:
        agg_trd.commit()

    return agg_trd


def get_aggregate(M, insaddr, prfnbr, currid):
    
    d0 = ael.date('1970-01-02')
    c  = ael.Instrument[currid]
    i  = ael.Instrument[int(insaddr)]


    """Get the aggregate trade if there exists one"""
    q = ' \
    SELECT      t.trdnbr, \
                t.value_day \
    FROM \
                trade t \
    WHERE \
                t.insaddr = ' + insaddr + ' \
    AND         t.prfnbr = ' + prfnbr + ' \
    AND         t.aggregate != 0'

    agg_trade = ael.dbsql(q)

    agg_trd = None
    agg_trdnbr = 0

    if agg_trade[0]:
        agg_trdnbr = sv(agg_trade[0][0][0])

        agg_trd = ael.Trade[int(agg_trdnbr)]

    else:
        """Create an aggregate trade"""

        agg_trd = ael.Trade.new(i)
        agg_trd.prfnbr = int(prfnbr)
        agg_trd.insaddr = int(insaddr)
        agg_trd.acquire_day = d0
        agg_trd.curr = c
        agg_trd.trade_curr = c
        agg_trd.value_day = d0
        agg_trd.time = d0.to_time()
        agg_trd.quantity = 0
        agg_trd.price = 0
        agg_trd.premium = 0
        agg_trd.fee = 0
        agg_trd.aggregate_pl = 0
        agg_trd.counterparty_ptynbr = int(M['agg_party'])
        agg_trd.acquirer_ptynbr =  int(M['agg_party'])
        agg_trd.status = 'BO Confirmed'
        agg_trd.type = 'Normal'
        agg_trd.aggregate = 1
        agg_trd.archive_status = 0
        agg_trd.trader_usrnbr = int(M['agg_user'])
        agg_trd.creat_usrnbr = int(M['agg_user'])
        agg_trd.creat_time = ael.date_today().to_time()
        agg_trd.updat_usrnbr = int(M['agg_user'])
        agg_trd.updat_time = ael.date_today().to_time()
        agg_trd.protection = 'W:RW,O:RW,G:RW,U:RW' # 3510
        agg_trd.owner_usrnbr = int(M['agg_user'])

        try:
            agg_trd.commit()
        except RuntimeError, msg:
            print msg
            return None
                
    return agg_trd
    

def archive_trade(trade, agg_trade):
    
    archived = 0

    if trade.aggregate == 0:
        clone = 0

        if (trade.aggregate_trdnbr == None or
            trade.aggregate_trdnbr.trdnbr != agg_trade.trdnbr or
            trade.archive_status == 0):                
            t_clone = trade.clone()
            clone = 1
            t_clone.aggregate_trdnbr = agg_trade
            t_clone.archive_status = 1

        update = 0
        for add in trade.additional_infos():
            if add.archive_status == 0:          
                update = 1
                break
        if update:
            if clone == 0:
                t_clone = trade.clone()
                clone = 1
            for add in t_clone.additional_infos():
                if add.archive_status == 0:
                    add.archive_status = 1

        update = 0
        for pay in trade.payments():
            if pay.archive_status == 0:
                update = 1
                break
        if update:
            if clone == 0:
                t_clone = trade.clone()
                clone = 1
            for pay in t_clone.payments():
                if pay.archive_status == 0:                    
                    pay.archive_status = 1   

        if clone:  
            t_clone.commit()
            archived = 1
            
    return archived
    
    
def archive_trades(trades, agg_trade, arch_trades):
    
    nr_upd_trades = 0    
    
    while (len(trades) > 0 and
           nr_upd_trades < max_transaction):
           
        trade = trades[0]
        arch_trades.append(trade)
        del trades[0]       
        
        if archive_trade(trade, agg_trade):
            nr_upd_trades = nr_upd_trades + 1

    return trade.value_day


def archive_trades_correct(M, trades, agg_trade):

    nr_upd_trades = 0
    
    for trade in trades:
    
        try:
            if archive_trade(trade, agg_trade):
                nr_upd_trades = nr_upd_trades + 1
        except RuntimeError, msg:
            print msg
            return -1
                
        if (nr_upd_trades == max_transaction):
            try:
                commit_transaction(M)
            except RuntimeError, msg:
                print msg
                return -1
            nr_upd_trades = 0
            begin_transaction(M)
            
    return nr_upd_trades


def dearchive_trade(trade):
    
    t_clone = trade.clone()

    t_clone.archive_status = 0
    t_clone.aggregate_trdnbr = 0

    for add in t_clone.additional_infos():
        add.archive_status = 0

    for pay in t_clone.payments():
        pay.archive_status = 0

    t_clone.commit()
    

def dearchive_trades_correct(M, insaddr, prfnbr, date, nr_transact):

    nr_upd_trades = 0
    
    if M['arch_to'] == '1':

        time = `date + ' 00:00:00'`
        instr = ael.Instrument[int(insaddr)]                    
        trades = ael.Trade.select('prfnbr = %s' % prfnbr)

        for trade in trades:
            if (trade.insaddr == instr and
                trade.archive_status == 1 and 
                trade.aggregate == 0 and
                (trade.value_day >= ael.date(date) or 
                 trade.time >= time)):
                 
                try:
                    dearchive_trade(trade)
                except RuntimeError, msg:
                    print msg
                    return -1
        
                nr_upd_trades = nr_upd_trades + 1        
                nr_transact = nr_transact + 1
                
            if nr_transact == max_transaction:
                try:
                    commit_transaction(M)
                except RuntimeError, msg:
                    print msg
                    return -1
                nr_transact = 0
                begin_transaction(M)

    return nr_upd_trades


def dearchive_trades(trades):

    nr_upd_trades = 0
    
    for trade in trades:
        if (trade.archive_status == 1 and 
            trade.aggregate == 0):

            dearchive_trade(trade)  
            nr_upd_trades = nr_upd_trades + 1        

    return nr_upd_trades
       

def abort_transaction(M):
    try:
        ael.abort_transaction()
    except:
        pass
    
def begin_transaction(M):
    try:
        ael.abort_transaction()
    except:
        pass
    ael.begin_transaction()


def commit_transaction(M):
    ael.commit_transaction()


def correct_position(M, prf, instr, break_date, inst_type):
    
    correct_date = ael.date(break_date)
    i = ael.Instrument[instr]
    if ( i.exp_day != None and correct_date >= i.exp_day ):
        correct_date = correct_date.add_days(1)
    correct_date = sv(correct_date)

    positions = get_positions(M, prf, [instr], correct_date)
    result = (0, 1)
    fail_agg = 0
    if len(positions) != 1:
        return result
        
    pos = positions[0]
                
    nbr_of_trades      = sv(pos[0])
    insaddr            = sv(pos[1])
    insid              = pos[2]
    prfnbr             = sv(pos[3])
    prfid              = pos[4]
    
    (curraddr, currid) = get_used_curr(insid, prfid)

    failMsg = '\nFailed to aggregate trades in %s in portfolio %s.' % \
            (insid, prfid)

    trades = []        
    if get_trades(M, insaddr, prfnbr, trades, correct_date) == -1:
        print failMsg
        return result

    if M['verbose'] == 1:
        print '\nAggregating %d trades in %s in portfolio %s at %s' % \
              (len(trades), insid, prfid, time.ctime(time.time()))

    agg_trd = get_aggregate(M, insaddr, prfnbr, currid)
    if agg_trd == None:
        print failMsg
        return result
    
    begin_transaction(M)

    nr_trans = archive_trades_correct(M, trades, agg_trd)
    if nr_trans == -1:
        abort_transaction(M)
        print failMsg
        return result

    deaggsize = dearchive_trades_correct(M, insaddr, prfnbr, correct_date, nr_trans)
    if deaggsize == -1:
        abort_transaction(M)            
        print failMsg
        return result

    try:
        agg_trd = calc_aggregate(trades, M, insaddr, prfnbr, curraddr,
                                currid, break_date, inst_type)           
    except RuntimeError, msg:
        print msg, failMsg
        abort_transaction(M)
        return result

    try:
        commit_transaction(M)
    except RuntimeError, msg:
        print msg, failMsg
        abort_transaction(M)
        return result

    if M['arch_to'] == '1' and M['verbose'] == 1:
        print '\nDeaggregated %d trades in %s in portfolio %s' % \
              (deaggsize, insid, prfid)

    return (1, 0)


def agg_ins_in_portfolio(M, prf, ins_list, break_date, inst_type):
    
    positions = get_positions(M, prf, ins_list, break_date)
    succ_agg = 0
    fail_agg = 0
    if positions:
        nr_pos = len(positions)
        for row in positions:
                
            nbr_of_trades      = sv(row[0])
            insaddr            = sv(row[1])
            insid              = row[2]
            prfnbr             = sv(row[3])
            prfid              = row[4]
                        
            (curraddr, currid) = get_used_curr(insid, prfid)
            
            failMsg = '\nFailed to aggregate trades in %s in portfolio %s.' % \
                    (insid, prfid)

            instr = ael.Instrument[int(insaddr)]
            if ( instr.exp_day != None and ael.date(break_date) >= instr.exp_day ):
                end_date = sv(ael.date(break_date).add_days(1))
            else:
                end_date = break_date

            trades = []
            if get_trades(M, insaddr, prfnbr, trades, end_date) == -1:
                print failMsg
                continue
                       
            agg_trade = get_aggregate(M, insaddr, prfnbr, currid)
            if agg_trade == None:
                print failMsg
                break
            
            if ( agg_trade.aggregate == -1 ):
                if ael.archived_mode() == 0:
                    print '\nThe aggregate trade %s in instrument %s \
                            in portfolio %s needs to be corrected. \
                            Please correct the aggregate trade from archive mode.' % \
                           (agg_trade.trdnbr, insid, prfid)
                            
                else:                    
                    (s, f) = correct_position(M, prfid, insid, break_date, inst_type)
                    succ_agg = succ_agg + s
                                
            elif ( ael.date(break_date) >= agg_trade.value_day ):
            
                if M['verbose'] == 1:
                    print '\nAggregating %d trades in %s in portfolio %s at %s' % \
                        (len(trades), insid, prfid, time.ctime(time.time()))
                
                success = 1    
                while len(trades) > 0:
                                   
                    begin_transaction(M)
                    
                    arch_trades = [] 
                    try:
                        arch_date = archive_trades(trades, agg_trade, arch_trades)
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
                        break
                                                           
                    if len(trades) > 0:
                        agg_date = str(arch_date)
                    else:
                        agg_date = break_date
                        
                    try:
                        agg_trade = calc_aggregate(arch_trades, M, insaddr, prfnbr, curraddr,
                                                currid, agg_date, inst_type)                        
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
                        break
                     
                    try:
                        commit_transaction(M)
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
                        break

                    ael.poll()
                    if len(trades) > 0:
                        trades.insert(0, agg_trade)

                if success:
                    succ_agg = succ_agg + 1
        
            else:
                if M['verbose'] == 1:
                    print '\nAggregating %d trades in %s in portfolio %s at %s' % \
                        (len(trades), insid, prfid, time.ctime(time.time()))
                               
                if (M['arch_to'] == '0'):
                    print 'Date is %s but there is an aggregate trade with value ' \
                          'day %s.\nTo reaggregate this position use the -archive ' \
                          'option for the script or run the script from a client in ' \
                          'archive  mode.' % (break_date, agg_trade.value_day)
                    print failMsg
                    continue
                
                success = 1
                old_trades = []
                dearch_date = agg_trade.value_day
                instr = ael.Instrument[int(insaddr)]
                if ( instr.exp_day != None and dearch_date >= instr.exp_day ):
                    dearch_date = dearch_date.add_days(1)
                if get_trades(M, insaddr, prfnbr, old_trades, sv(dearch_date)) == -1:
                    print failMsg
                    continue
                
                deaggsize = 0
                nr_archived = len(old_trades) - len(trades)
                
                if (nr_archived == 0):
                    begin_transaction(M)
                    try:
                        agg_trade = calc_aggregate(trades, M, insaddr, prfnbr, curraddr,
                                                currid, break_date, inst_type)
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
            
                    try:
                        commit_transaction(M)
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
                
                while (nr_archived > 0):
                
                    begin_transaction(M)
                
                    if (nr_archived > max_transaction):
                        trades_to_dearch = old_trades[-max_transaction:]
                        old_trades = old_trades[:-max_transaction]
                        agg_trades = old_trades
                        agg_date = str(old_trades[-1].value_day)
                    else:
                        trades_to_dearch = old_trades[-nr_archived:]
                        old_trades = old_trades[:-nr_archived]
                        agg_trades = trades
                        agg_date = break_date

                    try:
                        deaggs = dearchive_trades(trades_to_dearch)
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
                        break
                    
                    try:
                        agg_trade = calc_aggregate(agg_trades, M, insaddr, prfnbr, curraddr,
                                                currid, agg_date, inst_type)
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
                        break
            
                    try:
                        commit_transaction(M)
                    except RuntimeError, msg:
                        print msg, failMsg
                        success = 0
                        abort_transaction(M)
                        break
                    
                    ael.poll()
                    nr_archived = len(old_trades) - len(trades)

                    deaggsize = deaggsize + deaggs
                    
                if success:
                    succ_agg = succ_agg + 1
                    
                if M['verbose'] == 1:
                    print '\nDeaggregated %d trades in %s in portfolio %s' % \
                          (deaggsize, insid, prfid)
            
        fail_agg = nr_pos - succ_agg

    return (succ_agg, fail_agg)


def get_instype(trade):
    
    instype = trade.insaddr.instype
    und_instype = trade.insaddr.und_instype
    
    if (instype == 'Stock' or
        (instype in ('Option', 'Future/Forward', 'Warrant') and
         und_instype in ('Stock', 'EquityIndex'))):
         return 'eq'

    if (instype == 'Bond' or
        (instype in ('Option', 'Future/Forward') and
         und_instype in ('Bond', 'Future/Forward'))):
         return 'bond'
         
    return -1


def correct_invalid_aggregate_trades(M, aggtrds):

    succ_agg = 0
    fail_agg = 0
    
    for t in aggtrds:
        inst_type = get_instype(t)
        
        if inst_type == 'eq':
            if init_eq_values(M) == -1:
                return -1
        elif inst_type == 'bond':
            if init_bond_values(M) == -1:
                return -1

        if M['verbose'] == 1:
            print '\nUpdating aggregate trade %s' % t.trdnbr
        (succ, fail) = correct_position(M, t.prfnbr.prfid, 
                            t.insaddr.insid, t.value_day.to_string(), inst_type)
        if succ == 0:
            print '\nFailed to correct aggregate trade %s' % t.trdnbr
        succ_agg = succ_agg + succ
        fail_agg = fail_agg + fail
        
    total = succ_agg + fail_agg
    if fail_agg > 0:        
        print '\nFailed to correct %d of totally %d aggregate trade(s).' % \
            (fail_agg, total)
    if succ_agg > 0:
        print '\nSucceded to correct %d of totally %d position(s).' % \
            (succ_agg, total)
    return 1
            

def get_invalid_aggregate_trades(M):

    q = '''select trdnbr from trade where aggregate = -1'''

    res = ael.dbsql(q)

    trades = []
    for r in res[0]:
        trd = ael.Trade[r[0]]
        if trd:
            trades.append(trd)
        else:
            print 'Got trade from sybase that is not accessible from ael'
            print 'Trdnbr = ', trd
            print 'Cannot correct this trade.'

    if M['verbose'] == 1:
        if len(trades) > 0:
            print '\nThe following aggregate trades need to be updated:'
            for trd in trades:
                print '\nTrade %s in instrument %s, portfolio %s ' \
                      'with value day %s' % \
                      (trd.trdnbr, trd.insaddr.insid, trd.prfnbr.prfid,
                       trd.value_day)
        else:
            print '\nNo aggregate trades need to be updated'

    return trades


def perform_correction(M):

    if init_values(M) == -1:
        return -1

    aggtrds = get_invalid_aggregate_trades(M)

    if ael.archived_mode() == 0:
        print 'Correction of aggregate trades can only be done in '
        print 'archive mode'
        return -1

    return correct_invalid_aggregate_trades(M, aggtrds)


def perform_agg_and_arch(M, inst_type):

    if init_values(M) == -1:
        return -1

    if inst_type == 'eq':
        if init_eq_values(M) == -1:
            return -1
    elif inst_type == 'bond':
        if init_bond_values(M) == -1:
            return -1

    if (M['correct_agg'] != 'Aggregate'): 
        aggtrds = get_invalid_aggregate_trades(M)

        if M['correct_agg'] == 'Check':
            return 1

        elif M['correct_agg'] == 'Correct' or \
             M['correct_agg'] == 'CorrectAndAggregate':
            if ael.archived_mode() == 0:
                print 'Correction of aggregate trades can only be done in '
                print 'archive mode'
                return -1
            elif correct_invalid_aggregate_trades(M, aggtrds) == -1:
                return -1
            elif M['correct_agg'] == 'Correct':
                return 1

    found = 0
    succ_agg = 0
    fail_agg = 0
    if M['prf_list'] == ['']:
    
        (succ_agg, fail_agg) = agg_ins_in_portfolio(M, '', 
                                    M['ins_list'], M['date'], inst_type)
                                    
    else:
        for prf in M['prf_list']:
        
            (succ, fail) = agg_ins_in_portfolio(M, prf, 
                                M['ins_list'], M['date'], inst_type)
            succ_agg = succ_agg + succ
            fail_agg = fail_agg + fail
        
    total = succ_agg + fail_agg
    if total > 0:
        found = 1
                
    if fail_agg > 0:
        print '\nFailed to aggregate %d of totally %d position(s).' % \
            (fail_agg, total)
    if succ_agg > 0:
        print '\nSucceded to aggregate %d of totally %d position(s).' % \
            (succ_agg, total)
    
    if not found and M['verbose'] == 1:
        print '\nNo position with at least %d trades matched the input ' \
              'criteria:' % (1 + int(M['no_of_trades']))
        print 'Date:\t\t%s' % M['date']
        if M['given_instype'] != '':
            print 'Instype:\t%s' % M['given_instype']
        if M['given_ins'] != '':
            print 'Instrument:\t%s' % M['given_ins']
        if M['given_und'] != '':
            print 'Underlying:\t%s' % M['given_und']
        if M['given_prf'] != '':
            print 'Portfolio:\t%s' % M['given_prf']

    return 1
    


