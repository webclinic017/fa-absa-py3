""" AbandonClose:1.0.7 """

"""----------------------------------------------------------------------------
MODULE
	position_maintenance.py - Script for position maintenance 

DESCRIPTION
	This module performs positions maintenance such as delete position,
	abandon, clear P&L and cash posting.
	
	The module uses functionality in the FDMPosition module.
        Functions for deciding which date and price that should used are defined
        in FDMPositon. For example: when an option should be abandoned the suggested date is
        the expiry date and the suggested price is 0.0.
        
SUPPORTED INSTRUMENT TYPES
	Abandon:
	Option, Warrant, Future/Forward
	Clear PL:
	Bond, Future/Forward, Option, Stock, Warrant, Zero Bond 

	Note that PRIME does not currently support P&L for bonds. To view the P&L for bonds, 
	the ASQL Query App/BondPortfolio should be used.

REQUIREMENTS	
	- The script FDMPosition must be visble for this module.
	- For performing Delete and CashPositing of positions the FDMCascadeHandler
	module must be visble.(delete and cashposting are not supported in this version)
	
COMMANDLINE PARAMETER
	%ael <config> position_maintenance.py -f inifile [-l <logfilename>]
	config is the name of the ADS configuration. This only has to be specified when the script is run from UNIX.
	
DATA-PREP
	If the script is run from the command prompt an ini-file needs to be supplied
	
	inifile:
		-username       aggregate username                
		-password       password for the user
		-server         host:port
		-instypes        <comma separated list of instypes
		-portfolios 	<comma separated list of portfolios>
		-instruments	<comma separated list of instruments>
		-markets        <comma separated list of markets>
		-underlyings    <comma separated list of underlyings>
		-action         Abandon,Close,ClearRPL,ClearUPL,ClearTPL,ClearXPL
		-date           Date to abandon or clear P&L. 
		-pricefile      File with insid;price[;date].       (*)
		(*) Not implemented
	
	NOTE: A carriage return is needed after the last argument row.
	
    The username, password, server, action, instype and portfolios are mandatory. 
    If '*ALL*' is given as the portfolios argument the action will be performed on all
    portfolios.
    The arguments work as a filter, i.e only positions in those instruments that match
    all criteria will be considered. If a non-mandatory argument is not specified no 
    filtering will be made with respect to that argument.
    
		
	Example:
		(example of a inifile for deleting all Option and Future/Forward
		positions under the compound COMP1)
		-server         <host:port>
		-username       <username>
		-password       <secret>
		-instype        Option,Future/Forward
		-portfolios     *ALL*
		-action         Delete
		
	Note: 
	- The instruments traded on a market are determind by using the
	alias type with name 'Eurex' in the database in the example above.
	- If a compound portfolio is specified it is assumed that all physical
	children should be taken into account.
	- If no date is specified it will default to today's date. If a historic
	date is specified, the market prices that are used when clearing UPL or TPL
	will be the settlement prices of that date, i.e. there has to be settlement
	prices for the selected instruments on that date.

PRICEFILE
        A price file should have the following entries:
        INSID;price[;date] and one line per instrument.
        Spcifying a date is optional and then will the date speicfied by the -date parameter
        be used or if not specified (at all) be suggested by the FDMPosition module.
        If only the date should be specified this can be done as:
        ABB A;;2000-01-01 and the two formats can be mixed in the same file.
        Comments is written by "#" in the first position.

REFERENCES	
 	FDMPosion, [FDMCascadeHandler]
 	 	
ENDDESCRIPTION
----------------------------------------------------------------------------"""
import sys, getopt, string
import re
import time
from string import *
import ael
import types
from types import *

#
# Check that main modules are visible
#
module_error="""
======= ERROR ==========
The modules FDMPosition and (depending on action),FDMCascadeHandler must be visible
to this module.
Copy the corresponding .py files to the same direcftory or 
change/define environment variable PYTHONPATH to include path 
to directory(s) where those files could be found."""
try:
    for m in ['FDMPosition']:
    	c=('import %s' % m)
        exec(c)
except:
    print "Failed to import module:", m
    
    print module_error
    raise module_error

    
#==================================================================
# GLOBALS
#==================================================================
USAGE="""%ael <config> position_maintenance.py -f inifile [-t] [-l <logfilename>]
	 If -t is given means testmode i.e. don't perform the aggregate"""


ini_args=['username', 'password', 'server', 'instypes', 'instruments', 'underlyings', 'portfolios', 'markets', 'action', 'date', 'pricefile']
action_arguments=['instypes', 'instruments', 'underlyings', 'portfolios', 'markets', 'action', 'date', 'next_day_prices']
mandatory=['username', 'password', 'server', 'action', 'instypes', 'portfolios']
valid_actions=[FDMPosition.ABA, FDMPosition.CLO,
               FDMPosition.RPL, FDMPosition.UPL,
               FDMPosition.TPL, FDMPosition.XPL]
use_archive_mode=[FDMPosition.CSP, FDMPosition.DEL]

log_filename=None


#==================================================================
# HELPER CLASSES
#==================================================================

"""----------------------------------------------------------------------------
MODULE
	WPortfolio - Wrapper class for ael.Portfolio

DESCRIPTION
        The WPortfolio class adds a few methods missing in the ael.Portfolio
        class
	 

REFERENCES	
 	ael

ENDDESCRIPTION
----------------------------------------------------------------------------"""


class WPortfolio:
    """Wrapper class for ael.Portfolio"""
    def __init__(self, port):
        self.port=ael.Portfolio[port]
        


    def cmp(x, y):
        if x.prfid > y.prfid:
            return 1
        elif x.prfid < y.prfid:
            return -1
        return 0

    
    def childrenAux(self, port, only_phys, level, portfolios, processed, n):
        if processed.has_key(port.prfid) or (level and level==n):
            return
        processed[port.prfid]=None
        if not only_phys:
            portfolios[port]=n
        for l in port.links():
            if l.member_prfnbr.compound:
                self.childrenAux(l.member_prfnbr, only_phys, level, portfolios, processed, n+1)
            else:
                portfolios[l.member_prfnbr]=n+1
            

    def children(self,only_phys=None,level=None):
        """Returns a dictionary of <ael.Portfolio>:level"""
        if not self.port.compound:
            return []
        portfolios={}
        processed={}
        self.childrenAux(self.port, only_phys, level, portfolios, processed, 0)
        return portfolios
        
    
#==================================================================
# Local Operations
#==================================================================

#==================================================================
# Logging
#==================================================================
def log(text,tag='[i]'):
    global log_filename
    o=open(log_filename, 'a')
    now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    line=('%s %s %s' % (now, tag, str(text)))
    # Fix cutting of length
    o.write(line+'\n')
    o.close()

def logE(text):
    log(text, '[e]')

def logW(text):
    log(text, '[?]')

def logI(text):
    log(text, '[i]')
    
    
#==================================================================

def parse_price_file(filename):
    prices={}
    dates={}
    try:
        fp=open(filename, 'r')
    except:
        print "Unable to open file:", filename
        sys.exit(2)
    for line in fp.readlines():
        if line[0] == '#':
            continue
        values=string.split(line, ';')
        if len(values) == 2 and values[1]:
            (id, price)=map(string.strip, values)
            prices[id]=float(price)
        elif len(values) == 3:
            (id, price, d)=map(string.strip, values)
            if price:
                prices[id]=float(price)
            if d:
                dates[id]=ael.date(d)
    return (prices, dates)
        

def parse_inifile(filename):
    """ Parses a inifile and returns the arguments """
    global ini_args
    args={}
    try:
        fp=open(filename, 'r')
    except:
        print "Unable to open file:", filename
        sys.exit(2)
    for line in fp.readlines():
        matched=0
        for exp in ini_args:
           match=('-%s\s+(.*)\s+' % (exp))
           m=re.search(match, line, re.I)
           if m:
               v=string.strip(m. group(1))
               args[exp]=v
               matched=1
        if not matched and len(line) > 1 and line[0] != '#':
               msg='Invalid parameter [%s] in %s' % (line, filename)
               print msg
               raise msg
               
    return args

    
    
def validate_parameters(dic):
    cont=1
    global action_arguments
    for arg_type in action_arguments:
        values=dic.get(arg_type)
        if values:
            if not type(values) == types.ListType:     #If run from command prompt
                values=string.split(values, ',')
                values=map(string.strip, values)
            if not validate_single_parameter(values, arg_type):
                cont=0
                break
    return cont
    
    
    
def validate_single_parameter(values, type):
    cont=1
    n_errors=0
    if type == 'action':
        if len(values) > 1:
            print "ERROR in parameter %s: Only one action can be performed at a time!" % type
            cont = 0
        elif values[0] not in valid_actions:
            print "ERROR in parameter %s: Invalid action %s!" % (type, values[0])
            print "Valid actions are:"
            for i in valid_actions:
                print i
            cont = 0  
    elif type == 'date':
        if len(values) > 1:
            print "ERROR in parameter %s: Only one date can be specified!" % type
            cont = 0
        else:
            date=ael.date(values[0])
            if date.days_between(ael.date_today()) < 0:
                print "ERROR in parameter %s: %s is a future date!" % (type, date)
                cont = 0
    elif type == 'instruments':
        for insid in values:
            if not ael.Instrument[insid]:
                print "ERROR in parameter %s: Instrument %s does not exists!" % (type, insid)
                n_errors=n_errors+1
    elif type == 'instypes':
        for instype in values:
            if ael.enum_from_string('InsType', instype) == 0:
                print "ERROR in parameter %s: Invalid instype=%s!" % (type, instype)
                n_errors=n_errors+1
    elif type == 'portfolios':
        for prfid in values:
            if not ael.Portfolio[prfid]:
                print "Error in parameter %s: Portfolio %s does not exists!" % (type, prfid)
                n_errors=n_errors+1
    elif type == 'next_day_prices':
        if values[0] not in ['Yes', 'No']:
            print "ERROR in parameter %s: Select either 'Yes' or 'No'!" % type
            n_errors=n_errors+1
    elif type == 'underlyings':
        for insid in values:
            if not ael.Instrument[insid]:
                print "ERROR in parameter %s: Underlying instrument %s does not exists!" % (type, insid)
                n_errors=n_errors+1
    if n_errors > 0:
        if n_errors/len(values) < 0.1:
            print "The found errors are less then 10%! Continues anyway."
        else:
            cont = 0
    return cont   
        
            
                
def get_par(key, dic):
    value=dic.get(key)
    if value:
        if not type(value) == types.ListType:     #If run from command prompt
            value=string.split(value, ',')
            value=map(string.strip, value)
    return value
    


def cmp_pos(a, b):
    """ Sorts first on prfid, then insid """
    ret=cmp(a[0], b[0])
    if ret == 0:
        return cmp(a[1], b[1])
    return ret
    
    
def determent_instruments(instypes,markets,insids=[]):
    """ Returns a list of insid's of the set of instruments, filters on markets if defined """
    ins={}
    if insids:
        for insid in insids:
            i=ael.Instrument[insid]
    	    if i and (not instypes or i.instype in instypes):
     	        ins[i.insid]=i
    elif not instypes:
        for i in ael.Instrument.select():
            ins[i.insid]=i
    else:
    	for type in instypes:
            c=("instype='%s'" % type)
            for i in ael.Instrument.select(c):
                ins[i.insid]=i
    if markets:
        insids=[]
        alias_types=[]
        for m in markets:
            try:
            	alias_types.append(ael.InstrAliasType[m])
            except:
                msg=("AliasType %s doesn't exists in database" % m)
                print msg
                raise msg
        print "Filter instruments by market...."
        for (insid, instrument) in ins.items():
            for a in instrument.aliases():
                if a.type in alias_types:
                    insids.append(insid)
        return insids
    else:
        return ins.keys()
        
                    
def determent_physical_portfolios(portfolios):
    """ Returns a list of prfid's of physical_portfolios """
    ports={}
    if not portfolios:
        for p in ael.Portfolio.select():
            if not p.compound:
                ports[p.prfid]=None
    else:
        for p in portfolios:
            portfolio=WPortfolio(p)
            if not portfolio.port:
                print "No such portfolio %s! Aborts." % p
                sys.exit(2)
            if portfolio.port.compound:
                children=portfolio.children(1) # Only physical children
                for (child, level) in children.items():
                    ports[child.prfid]=None
            else:
                ports[p]=None
    return ports.keys()
    
#====================================================================
# Perhaps usefull stuff from Maintenace.py
#====================================================================

def getPositionsFor(port, ids):
    """ Returns a l(sorted) list of [port,instrument] refered by 
    trades in the portfolio for instrument ids"""
    # port could be prfid or prfnbr
    if not ael.Portfolio[port]:
        return []
    prfnbr=ael.Portfolio[port].prfnbr
    prfid=ael.Portfolio[port].prfid
    c_ids=[]
    if isinstance(ids[0], StringType):
        id='i.insid'
        string_cons=1
    else:
        id='i.insaddr'
        string_cons=0
    j=0
    c=''
    for i in ids:
        if j > 150:
            c_ids.append(c)
            j=0
            c=''
        if c == '':
            if string_cons:
                c="'"+i+"'"
            else:
                c=i
        else:
            if string_cons:
                c=c+",'"+i+"'"
            else:
                c=c+","+i
        j=j+1
    if c != '':
        c_ids.append(c)
    ret=[]
    for c in c_ids:
        stmt=("""select i.insid from instrument i where
                    %s in (%s) and exists (
                    	select * from trade t where 
                    		i.insaddr = t.insaddr and t.prfnbr = %d)""" % (id, c, prfnbr))
        #print stmt
    	rows=ael.dbsql(stmt)
    	for r in rows[0]:
     	   ret.append([prfid, r[0]]) # Rad can't handle lists
    return ret

               
def loadPositions(insids,portfolios=None):
    """returns of list of [prfid,insid] of positions for selected portfolio/instrument
    	Undefined list of portfolios means all physical portfolios"""
    if not portfolios or portfolios == 0 or portfolios == '':
        portfolios=[]
        for p in ael.Portfolio.select():
            if not p.compound:
                portfolios.append(p.prfid)
    else:
    	if isinstance(portfolios, StringType):
        	portfolios=string.split(portfolios, ',')
    positions=[]
    for p in portfolios:
        #print p
        if p:
            positions=positions+getPositionsFor(p, insids)
    positions.sort(cmp_pos)
    return positions
    
def determent_positions(instruments, portfolios):
    """ Returns a list of the positions that should be processed """
    positions=[]
    n=ael.Trade.count()
    max=len(instruments)*len(portfolios)
    if float(n) > float(max/2):
        print "Build positions by loadPositions()..."
        positions=loadPositions(instruments, portfolios)
    else:
        print "Builds positions by scanning the trades..."
        if len(portfolios) < len(instruments):
            seq=portfolios
            check=instruments
            table=ael.Portfolio
            type=0
        else:
            seq=instruments
            check=portfolios
            table=ael.Instrument
            type=1
        filter={}
        for c in check:
            filter[c]=None
        pos={}
        for s in seq:
            for t in table[s].trades():
                if type == 0: f=t.insaddr.insid
                elif type == 1: f=t.prfnbr.prfid
                if filter.has_key(f):
                    pos[(t.prfnbr.prfid, t.insaddr.insid)]=None
        positions=pos.keys()
    return positions


def find_archive_changed_positions(positions):
    """ Operation for checking if each position has archived trades that are changed
    after the build of the aggregate trade.
    Such positions must be rebuilt by forced in archive-mode. """
    return []

def strdup(s):
    """ to overcome problems with getopt """
    n=''
    for i in s:
        n=n+i
    return n


#=========================================================================
# Were the work is actually done
#=========================================================================
def perform_pos_main(args):
    global log_filename
    
    # Determent the set of instruments
    insids=get_par('instruments', args)
    instypes=get_par('instypes', args)
    markets=get_par('markets', args)
    und_insids=get_par('underlyings', args)
    p=get_par('portfolios', args)
    
    if und_insids:
        if not insids:
            instruments=[]
        else:
            instruments=insids
        for und_insid in und_insids:
            ins=ael.Instrument[und_insid]
            if not ins:
                print "Error: Instrument %s in underlyings doesn't exists in database! Aborts." % und_insid
                sys.exit(2)
            c=("und_insaddr=%d" % ins.insaddr)
            for der in ael.Instrument.select(c):
                if der in insids or not insids:
                    instruments.append(der.insid)
        insids = instruments
        
    instruments=determent_instruments(instypes, markets, insids)
    if len(instruments) == 0:
        print "No instruments match filter criteria!"
        return
    else:
        print "Found %d instruments" % len(instruments)




    #Determent the set of portfolios
    portfolios=determent_physical_portfolios(p)
    print "Found %d portfolios" % len(portfolios)

    #Determent the maximum set of positions, [(prfid,insid),.....]
    positions=determent_positions(instruments, portfolios)
    positions.sort(cmp_pos) # Sort them in prfid,insid order
    print "Number of positions are: %s " % len(positions)



    #==============================================
    # Here external filter is called
    #==============================================
    try:
        import FDMExtend
        init_fn='init_position_filter'
        val_fn='include_position_position'
        if FDMExtend.__dict__.has_key(init_fn):
            FDMExtend.__dict__[init_fn](inifile, args)
        if FDMExtend.__dict__.has_key(val_fn):
            tmp=[]
            for (prfid, insid) in positions:
                try:
                    if FDMExtend.__dict__[val_fn](prfid, insid):
                        tmp.append((prfid, insid))
                except:
                    # The traceback module may not be visible so only print the error.
                    print "Exception occured when calling %s(%s,%s)!" % (val_fn, prfid, insid)
                    sys.exit(2)
            positions=tmp
    except:
        pass

    #==============================================

    #Get a defined date (if defined)
    tmp=get_par('date', args)
    if not tmp:
        d1=None
    else:
        d1=ael.date(tmp[0])

    # Get the prices from price file (not implemented)
    pricefile=get_par('pricefile', args)
    if pricefile:
        (prices, dates)=parse_price_file(pricefile)
    else:
        prices={}
        dates={}



    print "\n=============================================================\n"
    print "Start processing ................"
    print "\n-------------------------------------------------------------\n"
    n_error=0
    n_ok=0
    n_pos=0
    n_non_expired=0
    expired=1
    action=get_par('action', args)[0]
    if get_par('next_day_prices', args):
        next_day_prices=get_par('next_day_prices', args)[0]
    else:
        next_day_prices=0
    mode_text=string.capitalize(action)
    for (p, i) in positions:
        try:
            pos=FDMPosition.FDMPosition(p, i) #Throws exception on no existance
            price=prices.get(i)
            mdate=dates.get(i, d1)
            n_pos=n_pos+1
            msg=("%s trades in [%s:%s]" % (mode_text, p, i))
            print msg,
            if mdate:    print ", date=%s" % str(mdate),
            if price: print  ", price=%s" % str(price),
            print "  ...",
            #sys.stdout.flush()  Flush output for tailing piped logfile Does not seem to work when running script from module editor
            try:
                if not testmode:
                    if action == FDMPosition.ABA:
                        if not pos.ins.exp_day or ael.date_today().days_between(pos.ins.exp_day) >= 0:
                            msg="Only positions in expired instruments can be abandoned"
                            print msg
                            expired=0
                        elif mdate and mdate.days_between(pos.ins.exp_day) >= 0:
                            msg="The instrument expires after the specified date %s" % mdate
                            print msg
                            expired=0
                        elif pos.Qty(FDMPosition.exp_day_to_date(pos.ins)) == 0.0:
                            msg=('Qty 0.0 in [%s:%s] => Nothing to Abandon' % (p, i))
                            print msg
                        else:
                            pos.abandon(mdate, price)
                    elif action  == FDMPosition.CLO:
                        if pos.Qty(mdate) == 0.0:
                            msg=('Qty 0.0 in [%s:%s] => Nothing to Close' % (p, i))
                            print msg
                        else:
                            pos.close(mdate, price)	    
                    elif action  == FDMPosition.RPL:
                        pos.clear_rpl(mdate)
                    elif action  == FDMPosition.CSP:
                        pos.cash_post(mdate)
                    elif action  == FDMPosition.UPL:
                        pos.clear_upl(mdate, price, next_day_prices)	    
                    elif action  == FDMPosition.TPL:
                        pos.clear_tpl(mdate, price, next_day_prices)	    
                    elif action  == FDMPosition.XPL:
                        pos.clear_xpl(mdate, price)
                    elif action  == FDMPosition.ACH:
                        pos.archive() # 
                    elif action  == FDMPosition.DCH:
                        pos.dearchive()	  
                    elif action  == FDMPosition.DEL:
                        pos.delete()
                    else:
                        print "INVALID ACTION"
                if log_filename: log(msg+'OK')
                if action == FDMPosition.ABA and not expired:
                    n_non_expired=n_non_expired+1;
                else:
                    n_ok=n_ok+1
                    print "OK!"
            except:
                n_error=n_error+1
                if log_filename: logE(msg+'Error!')
                print "ERROR!"
     	    sys.stdout.flush() # Flush output for tailing piped logfile
        except:
            pass

    print "\n------------------- S U M M A R Y ---------------------------\n"
    print "%-32s:%-d" % ('Number of Positions', n_pos) 
    print "%-32s:%-d" % ('Number of '+mode_text, n_ok) 
    if action == FDMPosition.ABA:
        print "%-32s:%-d" % ('Number of Non-Expired Positions', n_non_expired)
    print "%-32s:%-d" % ('Number of Errors', n_error) 
    print "\n-------------------------------------------------------------\n"

    print "Done!"



#=======================================================================
# Main 
#=======================================================================
if __name__ == '__main__': # Started from command promt    
    try:
        #Note: starting script using ael consumes parameters by inivar
        #i.e. -inifile consumes -i so other options needs to be used.
       opts, args = getopt.getopt(sys.argv[1:], 'f:l:t')
       if len(opts) < 1: raise getopt.error, ''
    except getopt.error, msg:
        print msg
        print USAGE
        sys.exit(2)

    inifile=None
    testmode=0
    for o, a in opts:
        if o == '-f': inifile = strdup(a)
        if o == '-t': testmode = 1
        if o == '-l': log_filename=strdup(a)
        
    if not inifile:
        print USAGE
        sys.exit(2)
        
    args=parse_inifile(inifile)
    
    error=0
    for a in mandatory:
        if not args.has_key(a):
            print "Error: argument %s in inifile must be given" % a
            error=1
    if error:
        print "Errors in inifile found! Aborts."
        sys.exit(2)
    
    # check given action parameter
    action=get_par('action', args)[0]
    if not action in valid_actions:
        print "Invalid action %s!" % action
        print "Valid actions are:"
        for i in valid_actions:
            print i
        sys.exit(2)
    applic='PMaint'+string.upper(action)
    
    #Connect in non-archive mode
    try:
        ael.disconnect() # For test
    except:
        pass
        
    if action in use_archive_mode:
    	ael.connect(args['server'], args['username'], args['password'], applic, 1) # ArchiveMode
    	try:
            import FDMCascadeHandler
    	except:
            print "Unable to import module FDMCascadeHandler"
            print module_error
            sys.exit(2)
    else:
        ael.connect(args['server'], args['username'], args['password'], applic)
    print "Connected to server %s" % args['server']
    
    #check if the action should be performed on all portfolios
    portfs_string = args.get('portfolios')
    portfs=string.split(portfs_string, ',')
    portfs=map(string.strip, portfs)
    if '*ALL*' in portfs:
        prfvect = []
        for p in ael.Portfolio.select():
		    prfvect.append(p.prfid)
		    prfvect.sort()
        args['portfolios'] = prfvect
    
    if not validate_parameters(args):
        sys.exit(2)
    else:
        perform_pos_main(args)
        ael.disconnect()
    
else:
    testmode=0
    #inifile="C:\\WINNT\\Profiles\\fredrikk\\Desktop\\Aggregation\\myinifile.txt"  Use ael_variables instead 
    
    insvect = []
    marklist = []
    instypes = []
    undvect = []
    prfvect = []
         
    for i in ael.Instrument.select():
        insvect.append(i.insid)
        c=("und_insaddr=%d" % i.insaddr)
        if ael.Instrument.select(c):
            undvect.append(i.insid)
    insvect.sort()
    undvect.sort()
    
    for ml in ael.Party.select():
        if ml.type == 'Market':
            marklist.append(ml.ptyid)
    marklist.sort()
    
    e = 1
    typ = 'Start'
    while typ != '?' and e < 100:
        typ = ael.enum_to_string('InsType', e)
        e = e + 1 
        if typ != '?' and typ != 'StrockRight' and typ != 'LEPO':
            instypes.append(typ)
    instypes.sort()
    
    for p in ael.Portfolio.select():
        prfvect.append(p.prfid)
    prfvect.sort()
    prfvect.append('* ALL PORTFOLIOS *')
    
    actions = valid_actions
#    if not ael.archived_mode():
#        actions.remove(FDMPosition.CSP)
#        actions.remove(FDMPosition.DEL)
#    else:
#    	try:
#            import FDMCascadeHandler
#    	except:
#            print "Unable to import module FDMCascadeHandler"
#            print module_error
#            sys.exit(2)
    
    ael_variables = [('instypes', 'InsTypes', 'string', instypes, '', 1, 1),
                     ('portfolios', 'Portfolios', 'string', prfvect, '', 1, 1),
                     ('instruments', 'Instruments', 'string', insvect, '', 0, 1),
                     ('markets', 'Markets', 'string', marklist, '', 0, 1),
                     ('underlyings', 'Underlyings', 'string', undvect, '', 0, 1),
                     ('action', 'Action', 'string', actions, '', 1, 0),
                     ('date', 'Date', 'string', [], '', 0, 0),
                     ('next_day_prices', 'NextDayPrices', 'string', ['Yes', 'No'], '', 0, 0)]

    def ael_main(dic):
        if '* ALL PORTFOLIOS *' in dic.get('portfolios'):
            if '* ALL PORTFOLIOS *' in prfvect:
                prfvect.remove('* ALL PORTFOLIOS *')
            dic['portfolios'] = prfvect
        if validate_parameters(dic):
            perform_pos_main(dic)