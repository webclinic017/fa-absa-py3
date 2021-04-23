# This script updates security loans by creating leg and cash flows,
# and updating trades.
# SPR 13310
    
import sys, getopt
import string
import math
import ael

#####################################################################
### strip_quotes
#####################################################################
def strip_quotes(value):
    out = ''
    for i in value:
        if (i != "\"") and (i != "\012") :
            out = out + i
    return out

#####################################################################
### list_from_line
#####################################################################
def list_from_line(line):
    data=[]
    for i in string.split(line, ','):
        value = strip_quotes(i)
        data.append(value)

    return data

######################################################################
### sv     SqlValue returns string of arg if not 'None' or NULL
######################################################################
def sv(val):
    if val == None:
        return 'NULL'
    else:
        return `val`

######################################################################
### set ini values for needed variables
######################################################################
def init_val(M):

#####  Time right now  ##################    
    res = ael.dbsql('SELECT getdate()')
    if res:
        now = res[0][0][0]
    else:
        print 'Failed to do gettime()'
        sys.exit(2)
    M['now'] = sv(now)

#####  Enum values  ##################    
    M['SecurityLoan'] = sv(ael.enum_from_string('InsType', 'SecurityLoan'))
    M['Fixed'] = sv(ael.enum_from_string('LegType', 'Fixed'))
    M['Fixed_Rate'] = sv(ael.enum_from_string('CashFlowType', 'Fixed Rate'))
    M['Rounding_Normal'] = sv(ael.enum_from_string('RoundingRule', 'Normal'))
    M['DC_None'] = sv(ael.enum_from_string('DaycountMethod', 'None'))
    M['Spot'] = sv(ael.enum_from_string('PayType', 'Spot'))
    M['Following'] = sv(ael.enum_from_string('BusinessDayMethod', 'Following'))
    M['Days'] = sv(ael.enum_from_string('DatePeriodUnit', 'Days'))

    return

######################################################################
### get_ini_values
######################################################################
def get_ini_values(M, inifile):

    server = 0
    user = 0
    password = 0
    atlasuser = 0
    adsaddress = 0
    atlaspassword = ''
    check_ref_val = 0
    update_ref_val = 0
    create_legs = 0
    verbose   = 0

    in_data = open(inifile)
    while  1:
        line=in_data.readline()
        if not line:
            break
        list=list_from_line(line)
        try:
            o = list[0]
            a = list[1]
        except:
            continue
        if a and o:
            if o == '-U': user = a
            if o == '-P': password = a
            if o == '-S': server = a
            if o == '-atlasuser': atlasuser = a
            if o == '-atlaspassword': atlaspassword = a
            if o == '-adsaddress': adsaddress = a
            if o == '-check_sec_loans': check_sec_loans = int(a)
            if o == '-update_ref_val': update_ref_val = int(a)
            if o == '-create_legs':  create_legs = int(a) 
            if o == '-verbose': verbose = int(a)

    if (server == 0) or (user == 0) or (password == 0) or \
       (atlasuser == 0) or (adsaddress == 0):
        help_text()
        
    M['server']          = server
    M['user']            = user
    M['password']        = password
    M['atlasuser']       = atlasuser
    M['adsaddress']      = adsaddress
    M['atlaspassword']   = atlaspassword
    M['check_sec_loans'] = check_sec_loans
    M['update_ref_val']  = update_ref_val
    M['create_legs']     = create_legs
    M['verbose']         = verbose

    return

######################################################################
### help_text
######################################################################
def help_text():

    print 'Inifile must contain the following values:'
    print 'Tag               Default  Description'
    print '====================================================='
    print '-S,               -        name of sybase server'
    print '-U,               -        name of sybase user'
    print '-P,               -        sybase password'
    print '-atlasuser,       -        name of Atlas user'
    print '-adsaddress,      -        name of ads address'
    print ''
    print 'Optional values are:'
    print '--------------------'
    print '-atlaspassword,   \'\'        atlas password'
    print '-check_sec_loans, 0         1 if you want to check security loans'
    print '-update_ref_val,  0         1 if you want to update ref_values'
    print '-create_legs,     0         1 if you want to create legs and \
cash_flows'
    print '-verbose,         0         1 if you want printouts'

    sys.exit(2)


######################################################################
### Read instrument table to get SecurityLoan instruments 
######################################################################
def get_sec_loans_without_legs(M):

    if M['verbose'] == 1:
        print 'Reading security loans'

    q = ' \
    SELECT \
               i.insaddr,\
               i.insid, \
               i.ref_value, \
               i.contr_size \
    FROM \
                instrument i\
    WHERE \
                i.instype =  ' + M['SecurityLoan'] + '\
    ORDER BY i.insaddr'

    secls = ael.dbsql(q)

    if M['verbose'] == 1 and secls:
        print 'The database contains', len(secls[0]), 'security loans'
        print 'Checking security loans with legs'

    res = []
    if secls:
        for sec in secls[0]:
        
            q = ' \
            SELECT \
                    l.legnbr\
            FROM \
                    instrument i, \
                    leg l \
            WHERE \
                    i.insaddr =  l.insaddr \
            AND     i.insaddr = ' + sv(sec[0])

            s = ael.dbsql(q)

            if not s[0]:
                res.append(sec)
            else:
                if M['verbose'] == 1 and M['create_legs'] == 1:
                    print 'Security loan', sec[1], 'already has a leg'

    if M['verbose'] == 1 and res:
        print 'Found', len(res), 'security loans without legs'

    return res

######################################################################
### Read Leg table to get the created legs 
######################################################################
def get_leg(insaddr):

    q = ' \
    SELECT \
               l.legnbr \
    FROM \
               leg l\
    WHERE \
               l.insaddr = ' + insaddr +' \
    ORDER BY l.insaddr'

    leg = ael.dbsql(q)

    return leg

######################################################################
### Read trade table to get trades made in SecurityLoans
######################################################################
def get_trades(insaddr):

    q = ' \
    SELECT \
               t.trdnbr,\
               t.insaddr \
    FROM \
    		trade t \
    WHERE \
    		t.insaddr = ' + insaddr + ' \
    ORDER BY t.insaddr'
    
    trades = ael.dbsql(q)
    
    return trades

######################################################################
### create leg
######################################################################
def create_leg(M, insaddr):

    secloan = ael.Instrument[int(insaddr)]
    
    if M['verbose'] == 1:
            print 'Creating leg for instrument ', secloan.insid
            
    u = ' \
    INSERT leg \
        ( \
        insaddr \
        ) \
    VALUES \
        ( \
        ' + insaddr + '  \
        )'
    
    legs = ael.dbsql(u)
        
    return

######################################################################
### fill leg
######################################################################
def fill_leg(M, insaddr):

    secloan = ael.Instrument[int(insaddr)]
    curr_leg = ael.Leg.select('insaddr=' + str(secloan.curr.insaddr))[0]
    calendar = curr_leg.pay_calnbr
    
    if secloan.open_end:
        end_day = str(ael.date_today())
    else:
        end_day = str(secloan.exp_day)

    u = ' \
    UPDATE \
           leg \
    SET \
           creat_time            = ' + M['now'] + ', \
           updat_time            = ' + M['now'] + ' ,\
           type                  = ' + M['Fixed'] + ', \
           payleg                = 1, \
           daycount_method       = i.daycount_method ,\
           curr                  = i.curr ,\
           nominal_factor        = 1.0 ,\
           rounding              = ' + M['Rounding_Normal'] + ', \
           decimals              = 5, \
           start_day             = i.start_day,\
           start_period_unit     =  ' + M['Days'] + ', \
           end_day               = ' + sv(end_day) + ',\
           end_period_unit       = i.exp_period_unit, \
           end_period_count      = i.exp_period_count, \
           rolling_period_unit   =  ' + M['Days'] + ', \
           rolling_base_day      = ' + sv(end_day) + ',\
           pay_day_offset_unit   = ' + M['Days'] + ', \
           pay_day_method        =  ' + M['Following'] + ', \
           reset_period_unit     =  ' + M['Days'] + ', \
           reset_day_method      =  ' + M['Following'] + ', \
           fixed_rate            = i.rate ,\
           pay_calnbr            = ' + sv(calendar.calnbr) + ' ,\
           amort_period_unit     =  ' + M['Days'] + ', \
           amort_start_day       = i.start_day, \
           amort_start_period_unit =  ' + M['Days'] + ', \
           amort_end_day         = ' + sv(end_day) + ',\
           amort_end_period_unit =  ' + M['Days'] + ', \
           amort_daycount_method = i.daycount_method, \
	   archive_status	 = i.archive_status \
    FROM \
           instrument i \
    WHERE \
          leg.insaddr = i.insaddr \
    AND   i.insaddr = ' + insaddr
    
    res = ael.dbsql(u)

    return

######################################################################
### update trade and instrument table
######################################################################
def update_trade_and_ins(M, insaddr, trdnbr, old_ref_value, contr_size):

    trade = ael.Trade[int(trdnbr)]
    secloan = ael.Instrument[int(insaddr)]
    
    if contr_size != 0.0:
        new_qty = old_ref_value * trade.quantity / contr_size
    else:
        new_qty = 0.0
        
    if old_ref_value != 0.0 and trade.quantity != 0.0:
        new_ref_value = contr_size * contr_size / old_ref_value
    else:
        new_ref_value = 0.0

    if M['verbose'] == 1:
        print 'Updating trade table for ', trade.trdnbr

    u = ' \
    UPDATE \
        trade \
    SET \
        quantity   = ' + sv(new_qty) + ' ,\
        updat_time = ' + M['now'] + '\
    WHERE \
        trdnbr = ' + trdnbr
        
    res = ael.dbsql(u)

    if trade.type == 'Normal':
        if M['verbose'] == 1:
            print 'Updating instrument table for ', secloan.insid
        
        u = ' \
        UPDATE \
                instrument \
        SET \
                ref_value         = ' + sv(new_ref_value) + ' ,\
                updat_time        = ' + M['now'] + ',\
                daycount_method   = ' + M['DC_None'] + ', \
                paytype           = ' + M['Spot'] + ' \
        WHERE \
                insaddr = ' + insaddr

        res = ael.dbsql(u)
        
    return

######################################################################
### update instrument table when no trade for instrument
######################################################################
def update_ins_no_trade(M, insaddr):

    secloan = ael.Instrument[int(insaddr)]
    
    if M['verbose'] == 1:
        print 'Updating instrument table for ', secloan.insid

    u = ' \
    UPDATE \
        instrument \
    SET \
        updat_time        = ' + M['now'] + ',\
        daycount_method   = ' + M['DC_None'] + ', \
        paytype           = ' + M['Spot'] + ' \
    WHERE \
        insaddr = ' + insaddr

    res = ael.dbsql(u)

    return

######################################################################
### create cashflow
######################################################################
def create_cashflow(M, legnbr):
    
    if M['verbose'] == 1:
        print 'Creating CashFlow for Leg number ', legnbr

    u = ' \
    INSERT cash_flow \
	( \
	legnbr \
	) \
    VALUES \
	( \
	' + legnbr + ' \
	)'
    
    cashflows = ael.dbsql(u)
        
    return

######################################################################
### fill cashflow
######################################################################
def fill_cashflow(legnbr):

    u = ' \
    UPDATE \
        cash_flow \
    SET \
        creat_time     = ' + M['now'] + ', \
        updat_time     = ' + M['now'] + ' ,\
        nominal_factor = 1.0, \
        rate           = l.fixed_rate, \
        start_day      = l.start_day, \
        end_day        = l.end_day, \
        pay_day        = l.end_day, \
        type           = ' + M['Fixed_Rate'] + ', \
        archive_status = l.archive_status \
    FROM \
        leg l \
    WHERE \
        cash_flow.legnbr = l.legnbr \
    AND l.legnbr = ' + legnbr
    
    res = ael.dbsql(u)
      
    return

######################################################################
### check_instrument
######################################################################
def check_instrument(insaddr):

    secloan = ael.Instrument[int(insaddr)]

    if secloan == None:
        print 'Got instrument from sybase that is not accessible from ael'
        print 'Skipping insaddr = ', insaddr
        return 0
    else:
        return 1

######################################################################
### check_trade
######################################################################
def check_trade(trdnbr):

    trade = ael.Trade[int(trdnbr)]

    if trade == None:
        print 'Got trade from sybase that is not accessible from ael'
        print 'Skipping trdnbr = ', trdnbr
        return 0
    else:
        return 1

######################################################################
### is_jgb
######################################################################
def is_jgb(ins):

    chl = ins.category_chlnbr
        
    if chl and chl.entry == 'JGB':
        return 1
    else:
        return 0

######################################################################
### ref_val
######################################################################
def ref_val(secloan):
    
    und_ins = secloan.und_insaddr
    curr =  und_ins.curr
    
    if und_ins.quote_type == 'Pct of nominal':
        return (secloan.ref_price / 100.0) * secloan.contr_size
    else:
        return (secloan.ref_price / 100.0 + \
                und_ins.interest_accrued(None, secloan.start_day, curr.insid)/ \
                und_ins.contr_size) * secloan.contr_size

######################################################################
### check_ref_val
######################################################################
def check_ref_val(insaddr):
    
    secloan = ael.Instrument[int(insaddr)]
    und_ins = secloan.und_insaddr
    
    r = ref_val(secloan)
    
    if und_ins.instype != 'Stock':
        diff = abs(secloan.ref_value - r)
        if diff < 1e-10:
            diff = 0
        print secloan.insid
        print secloan.ref_value, ' ', r, ' ', diff
        print ''
            
    return

######################################################################
### check_sec_loans
######################################################################
def check_sec_loans(ins):

    if M['verbose'] == 1:
        print ''
        print 'Checking ref_values'
        print 'The following information is printed:'
        print '<Insid>'
        print '<Old ref_value>  <New (computed) ref_value>  <Diff>'
        print ''

        for row in ins:
            insaddr = sv(row[0])
            
            ins_ok = check_instrument(insaddr)
            
            if ins_ok:
                check_ref_val(insaddr)
                
    print 'There are', len(ins), \
          'security loans in the database that have not been upgraded'

    return

######################################################################
### update_ref_val
######################################################################
def update_ref_val(M, insaddr):

    secloan = ael.Instrument[int(insaddr)]
    und_ins = secloan.und_insaddr
    
    if und_ins.instype != 'Stock':
	    real_ref_value = ref_val(secloan)
	
            if M['verbose'] == 1:
                print 'Setting ref_value for', secloan.insid, 'to', \
                      real_ref_value
	
	    u = ' \
	    UPDATE \
                instrument \
	    SET \
                ref_value         = ' + sv(real_ref_value) + ' ,\
                updat_time        = ' + M['now'] + '\
	    WHERE \
                insaddr = ' + insaddr

	    res = ael.dbsql(u)

    return

######################################################################
### update_ref_values
######################################################################
def update_ref_values(ins):

    if M['verbose'] == 1:
        print 'Updating ref_value for', len(ins), 'security loans'

    for row in ins:
        insaddr = sv(row[0])

        ins_ok = check_instrument(insaddr)

        if ins_ok:
            update_ref_val(M, insaddr)
            
    return

######################################################################
### create_legs
######################################################################
def create_legs(ins):

    if M['verbose'] == 1:
        print 'Creating legs and cash_flows for', len(ins), 'security loans'

    error_ins = []
    error_trds = []
    for row in ins:
        insaddr            = sv(row[0])
        insid              = sv(row[1])
        old_ref_value      = row[2]
        contr_size         = row[3]
        
        ins_ok = check_instrument(insaddr)

        if ins_ok:
            # Create and fill leg for instrument
            res = ael.dbsql('begin transaction')
            create_leg(M, insaddr)
            fill_leg(M, insaddr)
            res = ael.dbsql('commit')           
            
            leg = get_leg(insaddr)
            if leg:
                # Create and fill cash flow for leg
                for row in leg[0]:
                    legnbr = sv(row[0])
                    
                    res = ael.dbsql('begin transaction')
                    create_cashflow(M, legnbr)
                    fill_cashflow(legnbr)
                    res = ael.dbsql('commit')           
                    
            trade = get_trades(insaddr)
            if trade:
                # Update trades and instrument
                for row in trade[0]:
                    trdnbr = sv(row[0])
                    trdinsaddr = sv(row[1])
                    
                    trd_ok = check_trade(trdnbr)
                    
                    if trd_ok:
                        res = ael.dbsql('begin transaction')
                        update_trade_and_ins(M, trdinsaddr, trdnbr, \
                                             old_ref_value, contr_size)
                        res = ael.dbsql('commit')
                    else:
                        # Could not read trade in ael
                        error_trds.append(trdnbr)
                        
            else:
                # Found no trade, update instrument
                res = ael.dbsql('begin transaction')
                update_ins_no_trade(M, insaddr)
                res = ael.dbsql('commit')
        else:
            # Could not read instrument in ael
            error_ins.append(insaddr)

        if M['verbose'] == 1:
            print ''

    if not error_ins:
        print 'Succesfully upgraded', len(ins), 'security loans'
    else:
        print 'Succesfully upgraded', len(ins) - len(error_ins), \
              'security loans'
        print 'Security loans with the following insaddrs could not be \
        upgraded'
        print error_ins[0]

    if not error_trds:
        print 'All trades succesfully upgraded'
    else:
        print 'Trades with the following trdnbrs could not be upgraded'
        print error_trds[0]

    return

######################################################################
### Main
######################################################################
try:
    opts, args = getopt.getopt(sys.argv[1:], 'f:h')
    if len(opts) != 1: raise getopt.error, ''
except getopt.error, msg:
    print msg
    print 'Usage: ael prod upgrade_security_loans.py -f inifilename | -h',
    sys.exit(2)

inifile = 0
for o, a in opts:
    if o == '-f': inifile = a
    if o == '-h': help_text()
    
if inifile == 0:
    print msg
    print 'Usage: ael prod upgrade_security_loans.py -f inifilename | -h',
    sys.exit(2)

M= {}
get_ini_values(M, inifile)

if M['check_sec_loans'] == 0 and M['update_ref_val'] == 0 and \
   M['create_legs'] == 0:
    sys.exit(2)

atlas = ael.connect(M['adsaddress'], M['atlasuser'], M['atlaspassword'], '', 1)
    
# The following is needed if the database is corrupt and loops when trying to
# create new legs (or cash_flows).  If this is used the ads needs to be
# restarted after the  script has been run.
#if 0 and M['create_legs'] == 1:
#    q = 'set textsize 313131'
#    ael.dbsql(q)

init_val(M)
    
ins = get_sec_loans_without_legs(M)

if ins:
    if M['check_sec_loans'] == 1:
        check_sec_loans(ins)
        
    if M['update_ref_val'] == 1:
        update_ref_values(ins)
        
    if M['create_legs'] == 1:
        create_legs(ins)
else:
    print 'All security loans have already been upgraded'

ael.disconnect()


