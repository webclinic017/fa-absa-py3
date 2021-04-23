# This script combined with amort_instrument.ini updates the old daily mtm
# prices for amortising contracts with the correct value.
# SPR 3940
    
import sys, getopt
import string
import math
import sybdb
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
def init_values(sdb, M):

#####  Time right now  ##################    
    res = sdb.execute('SELECT getdate()')
    if res:
        now = res[0][0][0]
    else:
        print 'Failed to do gettime()'
        sys.exit(2)
    M['now'] = sv(now)


### AmortType None ##############################################
    res = sdb.execute("SELECT value from ds_enums where name = \
                  'AmortType' and tag = 'None'")
    if res:
       AmortTypeNone = res[0][0][0]
    else:
        print 'Failed to read enum AmortType'
        sys.exit(2)

    M['AmortTypeNone']=sv(AmortTypeNone)

### InsType FreeDefCF ##############################################
    res = sdb.execute("SELECT value from ds_enums where name = \
                  'InsType' and tag = 'FreeDefCF'")
    if res:
       FreeDefCF = res[0][0][0]
    else:
        print 'Failed to read enum InsType'
        sys.exit(2)

    M['FreeDefCF']=sv(FreeDefCF)

### Price MtMMarket ##############################################
    res = sdb.execute("SELECT value from ds_enums where name = \
                  'PartyType' and tag = 'MtM Market'")
    if res:
       MtMMarket = res[0][0][0]
    else:
        print 'Failed to read enum Price'
        sys.exit(2)

    M['MtMMarket']=sv(MtMMarket)

######################################################################
### get_ini_values
######################################################################
def get_ini_values(M, inifile):

    server = 0
    user = 0
    password = 0
    altas_user = 0
    ads_address = 0
    atlas_password = ''
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
            if o == '-atlasuser': atlas_user = a
            if o == '-atlaspassword': atlas_password = a
            if o == '-adsaddress': ads_address = a
            if o == '-verbose': verbose = int(a)

    if (server == 0) or (user == 0) or (password == 0) or \
       (atlas_user == 0) or (ads_address == 0):
        help_text()
        
    M['server']          = server
    M['user']            = user
    M['password']        = password
    M['atlas_user']      = atlas_user
    M['ads_address']     = ads_address
    M['atlas_passwd']    = atlas_password
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
    print '-verbose,         0         1 if you want printouts'

    sys.exit(2)


######################################################################
### Read instrument table to get amortising instruments 
######################################################################
def get_amort_instruments(sdb, M):

    if M['verbose'] == 1:
        print 'Reading amortising instruments'

    q = ' \
    SELECT DISTINCT\
                i.insaddr,\
                i.contr_size \
    FROM \
                instrument i,\
                leg l\
    WHERE \
                l.amort_type !=  ' + M['AmortTypeNone'] + '\
                and l.insaddr = i.insaddr \
                and i.instype != ' + M['FreeDefCF'] + '\
    ORDER BY i.insaddr'

    ins = sdb.execute(q)

    return ins

######################################################################
### Read price table to get mtm prices
######################################################################
def get_mtm_prices(sdb, M, insaddr):

    today = sv(ael.date_today())
    
    q = ' \
    SELECT \
                p.day,\
                p.settle,\
                p.last_,\
                p.bid,\
                p.ask,\
                p.prinbr,\
                c.insid\
    FROM \
                price_hst p,\
                party pty,\
                instrument i,\
                instrument c\
    WHERE \
                pty.ptynbr = p.ptynbr\
                and i.insaddr = ' + insaddr + '\
                and p.insaddr = i.insaddr\
                and pty.type = ' + M['MtMMarket'] + '\
                and i.curr = c.insaddr '
#                and i.exp_day > ' + sv(today)
                
    prices = sdb.execute(q)

    return prices


######################################################################
### update mtm price for an amortising instrument
######################################################################
def update_mtm_price(sdb, M, insaddr, curr, prinbr, settle, last, bid, ask, contr_size, p):

    i = ael.Instrument[int(insaddr)]
    print i.insid

    print settle
    p_date = p.day
    print date
    nominal = i.nominal_amount(p_date, curr)

    print nominal, contr_size, curr
    
    if nominal == 0.0:
        nominal = contr_size
        print 'Nominal is zero, use contr_size instead'

    new_settle_price = settle * contr_size/nominal
    new_last_price   = last * contr_size/nominal
    new_bid_price    = bid * contr_size/nominal
    new_ask_price    = ask * contr_size/nominal
            
    if M['verbose'] == 1:
        print 'Updating price table for ', i.insid
        
        u = ' \
        UPDATE \
                price_hst \
        SET \
                settle         = ' + sv(new_settle_price) + ' ,\
                last_          = ' + sv(new_last_price) + ' ,\
                bid            = ' + sv(new_bid_price) + ' ,\
                ask            = ' + sv(new_ask_price) + ' ,\
                updat_time     = ' + M['now'] + '\
        WHERE \
                prinbr = ' + sv(prinbr)

        print u
        res = sdb.execute(u)
        
    return


######################################################################
### check_instrument
######################################################################
def check_instrument(insaddr):

    ins = ael.Instrument[int(insaddr)]

    if ins == None:
        print 'Got instrument from sybase that is not accessible from ael'
        print 'Skipping insaddr = ', insaddr
        return 0
    else:
        return 1

######################################################################
### check_amort_instruments
######################################################################
def check_amort_instruments(ins):

    if M['verbose'] == 1:
        print 'Checking theor for', len(ins), 'amortising instruments'

        for row in ins:
            insaddr = sv(row[0])
            
            ins_ok = check_instrument(insaddr)
            
            if ins_ok:
                check_mtm_price(insaddr)
                
    if ins:
        print 'There are', len(ins), \
              'amortising instruments in the database that have not been upgraded'

    return


######################################################################
### update_mtm_prices
######################################################################
def update_mtm_prices(ins):

    if M['verbose'] == 1:
        print 'Updating mtm prices for', len(ins), 'amortising instruments'

    for row in ins:
        insaddr = sv(row[0])
        contr_size = row[1]
        ins_ok = check_instrument(insaddr)

        if ins_ok:
            prices = get_mtm_prices(sdb, M, insaddr)
            print prices
            if prices:
                for p in prices[0]:
                    prinbr = p[5]
#                    day    = ael.date_from_string(p[0][:10])
                    settle = p[1]
                    last   = p[2]
                    bid    = p[3]
                    ask    = p[4]
                    curr   = sv(p[6])
                    update_mtm_price(sdb, M, insaddr, curr, prinbr, settle, last, bid, ask, contr_size, p)
                    
    return



######################################################################
### Main
######################################################################
try:
    opts, args = getopt.getopt(sys.argv[1:], 'f:h')
    if len(opts) != 1: raise getopt.error, ''
except getopt.error, msg:
    print msg
    print 'Usage: upgrade_amort_instruments.py -f inifilename [-h]',
    sys.exit(2)

inifile = 0
for o, a in opts:
    if o == '-f': inifile = a
    if o == '-h': help_text()
    
if inifile == 0:
    print msg
    print 'Usage: upgrade_amort_instruments.py -f inifilename [-h]',
    sys.exit(2)

M= {}
get_ini_values(M, inifile)

sdb = sybdb.connect(M['user'], M['password'], M['server'])
ael.connect(M['ads_address'], M['atlas_user'], M['atlas_passwd'], '', 0)
    
init_values(sdb, M)
    
ins = get_amort_instruments(sdb, M)

print ins

if ins:
        update_mtm_prices(ins[0])
        
else:
    print 'All amortising instruments have already been upgraded'





