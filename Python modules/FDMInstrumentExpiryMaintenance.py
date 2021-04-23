""" AbandonClose:1.0.7 """

"""----------------------------------------------------------------------------
MODULE
        instrument_expiry_maintenance.py - Script for maintenace when instruments expiry

DESCRIPTION
        This module performs instrument maintenance such as clearing the listleafs, orderbooks,
        price definitions and own orders.
        If wanted the expired instrument could also be deleted or archived.

        Normally it is only possible to delete an instrument were no trading have occured but if
        the quantity and RPL is zero (zero positions) in all positions then those trades and the
        instrument could also be deleted depending on requirements in the organisation. Use the
        include_zero_pos flag to activate this option.

        To be able to get rid of expired instruments with trades and RPL contribution the positions
        could be cash-posted which means that the RPL contribution is moved to a special instrument.
        After that the expired instrument could be deleted because now the RPL and QTY is zero.
        If the instrument is archived or keept  the position is archived and could be unwinded but
        if the instrument is deleted the position's trades are ( of course ) deleted.

        By using the force flag it is possible to ignore all previous listed checks and just delete/archive
        the instrument and all relations (e.g. trades, own orders, e.t.c). This could be used as an EOY
        where last years expired instruments and it's trades is of NO interest. BUT NOTE then PL contribution
        will be lost (or hidden).

        If instruments are to be deleted or archived it is possible to get a listing of
        affected Volatility Surfaces in the report. The report is actived by specifying the report_path
        parameter.

        Because of previous errors it may exists hidden references to instruments which should
        be cleared and this could be done by the script cleanup_dangling_references.

        This script could also be applied against underlyings such as Combination.
        An underlying is interpreted as expired if some of it's legs(children) are expired or if no
        legs exists and no trades and no orders books exists.

        By listing instruments using the -instruments parameter or using an instrument name file (-dat_filename parameter)
        no instrument filtering is done, only trade filtering. Which means that this script could be used to delete
        any instrument and associated relations (except BO Confirmed trades).

NOTE:
	- Trades in status BO Confirmed can't be deleted from the database so if instruments are to be cash posted
	or deleted they can't contain BO Confirmed trades. But Archiving is possible.
	- When the script executes it generates an instrument name file,.dat file (insid;insaddr), with instrument
	processed that can be used for later processing. For exmaple if first ListLeafs e.t.c should be cleared and
	afterwords (an other day) deleted or archived. But if the instruments already have been archived and now
	should be deleted the script must be executed in archive mode.
	
REQUIREMENTS
        - The module FDMCascadeHandler must be visble for this script to be able to delete or
          archive instruments.
        - The module FDMPosition must be visble to handle zero positions and csh-posting.
        - The User must have access to execute dbsql questions.


COMMANDLINE PARAMETER
        See USAGE

DATA-PREP
        inifile:
                #
                # Mandatory
                #
                -username               username to use when doing the maintenance
                -password               password for the user
                -server                 host:port

                #
                # Optional
                #
                -aliastypes             	.
                -exp_date               <[%Y-%m-%d,-N], Only include instrument expire BEFORE that date.
                			-N means TODAY-N days. Default TODAY>
                -include_zero_pos       <[Yes/No], If zero position instruments should also be included. Default No>
                -cash_post_nonzero_pos  <[Yes/No], If nonzero positions should be cash-posted. Default No>
                -used_cash_post_curr    <['Accounting','Portfolio','Instrument', or insid of a currency instrument>],
                                        Determents which currency that should be used when cash-posting a position>
                -instruments            <comma separated list of instruments>
                -instrument_handling    <Archive,Delete,Keep] if instrument (and all relations) should
                                          be archived, deleted or kept. Default Keep which means that
                                          only the leafs, orderbooks e.t.c. are removed>
                -instypes                <comma separated list of instypes. Default: Option,Future/Forward>
                -markets                <comma separated list of parties of type market>
                -underlyings            <comma separated list of underlyings>

                #
                # Special
                #
                -dat_filename		<filename with path included of a previous generated file of
                			processed instruments. Overrides any instrument filterings e.g. definitions
                			by -instype,-markets, -underlyings e.t.c.>.
                -force                  <[Yes,No] to force handling of all relations to an expired instrument.
                                        Default No.
                                        Use this force archive/delete of expired instruments and
                                        all it's trades, orders e.t.c. MUST BE USED WITH CARE!>
                -list_affected_volas    <[Yes,No] if affected volatility surfaces of instrument deletion should
                                        be listed or not. May be timeconsuming. Default: No.>
                -report_path        	<Path to a directory where a log and report file will be generated.
                                        If undefined only log to standard output.
                                        Filenames will be:
                                        instrument_expiry_maintenance_$date[_N].log and
                                        instrument_expiry_maintenance_$date[_N].txt (report) and
                                        instrument_expiry_maintenance_$date[_N].dat (processed instruments).
                                        NOTE: This means that report path MUST be defined to be able to
                                        store processed instruments for later processing.

                -testmode               <[Yes/No] if Yes the different actions will only be listed. Default No.
                                        May differ a little from true processing because of errors when
                                        deleting/archive data.




        The username,password,server are mandatory.


        Example:
                (example of a inifile for deleting all price definitions, order books, own orders
                list leafs (pages) on instrument of Option and Future/Forward that expired before TODAY
                traded on EUREX.
                 expired before today)
                -server                 <host:port>
                -username               <username>
                -password               <secret>
                -instype                Option,Future/Forward
                -aliastypes             EUREX
                -instrument_handling    Keep

        Note:
        - The instruments traded on a market are determind by using the
        alias type with name EUREX in the database in the example above.
        - When filtering on listnode references both from OrderBook or ListLeaf could
          by included/excluded.
        - If underlyings are specified the underlying and its derivatives will be appended
        to the list of instruments and then filtered by instypes and markets (if specified).


REFERENCES
        FDMPosition, FDMCascadeHandler


ENDDESCRIPTION
----------------------------------------------------------------------------"""
import sys, getopt, string
import re, os
import time
import ael





#==================================================================
# GLOBALS
#==================================================================
USAGE="""%ael <config> instrument_expiry_maintenance.py -f inifile [-t] [-l <logfilename>]
    If -t is given means testmode i.e. just log the operations"""


ini_args=['username', 'password', 'server', 'instypes', 'instruments', 'underlyings',
    'aliastypes', 'markets', 'instrument_handling', 'include_zero_pos', 'exp_date',
    'force', 'report_path', 'testmode', 'list_affected_volas', 'cash_post_nonzero_pos',
    'used_cash_post_curr', 'dat_filename']
mandatory=['username', 'password', 'server']


# reason_descr: Used in reporting etc.
reason_descr={
    0:'OwnOrder Reference',
    1:'Trade Reference',
    2:'Non-Zero Position exists',
    3:'Included, Only Non-Zero Positions exists',
    4:'Included, Positions may be cash-posted',
    5:'Failed to CashPost some positions',
    6:'BO Confirmed trade exists'}

# report_descr: the different list describes if instrument have been deleted/archive, skipped or where delete failed.
# In the list of skipped instruments each element is a tuple (insid,reason_flag).
# keys: the value of instrument_handling, SKIP and Failed.
#
report_descr={}



log_filename=None
rep_filename=None
dat_filename=None
testmode=0

#==================================================================
# HELPER CLASSES
#==================================================================


#==================================================================
# Local Operations
#==================================================================

#==================================================================
# Logging
#==================================================================
def log(text,tag='[i]'):
    global log_filename

    now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    line=('%s %s %s' % (now, tag, str(text)))
    if log_filename:
        o=open(log_filename, 'a')
        # Fix cutting of length
        o.write(line+'\n')
        o.close()
    print line

def logE(text):
    log(text, '[e]')

def logW(text):
    log(text, '[?]')

def logI(text):
    log(text, '[i]')

#########################################################
# Parameter handling operations
#########################################################

def get_par(key, dict):
    """ Get's and validates a parameter """
    value=dict.get(key)
    if value:
        if not type(value) == type([]):     #If run from command prompt
            value=string.split(value, ',')
            value=map(string.strip, value)
        if not validate_par(key, value):
            local_exit(__name__, 2)
    return value



def parse_inifile(filename):
    """ Parses a inifile and returns the arguments """
    global ini_args
    args={}
    try:
        fp=open(filename, 'r')
    except:
        print "Unable to open file:", filename
        local_exit(__name__, 2)
    for line in fp.readlines():
        if line[0] == '#':
            continue
        matched=0
        for exp in ini_args:
            match=('-%s\s+(.*)\s+' % (exp))
            #print match,line
            m=re.search(match, line, re.I)
            if m:
                #print "YES"
                v=string.strip(m. group(1))
                args[exp]=v
                matched=1
        if not matched and len(line) > 1 and line[0] != '#':
            msg='Invalid parameter [%s] in %s' % (line, filename)
            print msg
            raise msg

    return args



def validate_par(type, values):
    n_errors=0
    read_lookup={
        'instruments':('Instrument', "insid"),
        'portfolios' :('Portfolio', "prfid"),
        'aliastypes':('InstrAliasType', "alias_type_name"),
        'markets':('Party', "ptyid"),
        'underlyings':('Instrument', 'insid')
        }
    enum_lookup={'instypes':'InsType'}

    if read_lookup.has_key(type):
        (name, column)=read_lookup[type]
        tmp="ael_table=ael.%s" % name
        f1="%s='%%s'" % column
        f2="%s=%%s" % column
        exec(tmp) # Get the ael_table object
        for v in values:
            c1=f1 % v
            c2=f2 % v
            #print c1,c2
            try:
                if not ael_table.read(c1):
                    print "ERROR in parameter %s: %s %s does not exists!" % (type, name, v)
                    n_errors=n_errors+1
            except:
                if not ael_table.read(c2):
                    print "ERROR in parameter %s: %s %s does not exists!" % (type, name, v)
                    n_errors=n_errors+1

    elif enum_lookup.has_key(type):
        for v in values:
            et=enum_lookup[type]
            if ael.enum_from_string(et, v) == 0:
                print "ERROR in parameter %s: Invalid enum value[%s] for type %s!" % (type, v, et)
                n_errors=n_errors+1
    elif type == 'exp_date':
        try:
            offset=int(values[0])
            if offset > 0:
               print "ERROR in parameter %s: Date offset (%s) must be less than zero." % (type, values[0])
               n_errors=n_errors+1
        except:
            try:
            	d=ael.date(values[0])
            except:
                print "ERROR in parameter %s: Invalid date (%s). Format is: %Y-%m-%d e.g. 2001-01-01 or -N" % (type, values[0])
            	n_errors=n_errors+1
    elif type in ['force', 'include_zero_pos', 'testmode', 'list_affected_volas', 'cash_post_nonzero_pos']:
        if not values[0] in ['Yes', 'No']:
            print "ERROR in parameter %s, unsupported value %s. Valid values are: Yes or No." % (type, values[0])
            n_errors=n_errors+1
    elif type == 'instrument_handling':
        if not values[0] in ['Archive', 'Delete', 'Keep']:
            print "ERROR in parameter %s, unsupported value %s. Valid values are: Archive,Delete or Keep." % (type, values[0])
            n_errors=n_errors+1
    elif type in ['report_path', 'dat_filename']:
        import os
        if not os.path.exists(values[0]):
            print "ERROR in parameter %s. Directory (or file) [%s] doesn't exists." % (type, values[0])
            n_errors=n_errors+1
    elif type == 'used_cash_post_curr':
        import FDMPosition
        if not values[0] in FDMPosition.get_valid_styles():
            print "ERROR in parameter %s, unsupported value %s. Valid values are: %s" % (type, values[0], FDMPosition.get_valid_styles())
            n_errors=n_errors+1
    else:
        msg="Undefined parameter %s in inifile" % type
        print msg
        raise msg

    if n_errors > 0:
        return 0
    return 1

def set_par_value(par_name, default_value, args):
    """ Helper operation for setting default values for parameters.
        Will also add default values to args """

    ret=get_par(par_name, args)
    if type(default_value)==type([]):
        if not ret:
            ret=default_value
            args[par_name]=string.join(ret, ',')
    elif type(default_value) ==type('string'):
        if not ret:
            ret=default_value
        else:
            ret=ret[0]
        args[par_name]=ret
        if default_value in ['Yes', 'No']: # Treated as boolean values
            if ret == 'No':
                ret=None
                args[par_name]='No'
            else:
                args[par_name]='Yes'
    elif type(default_value) == type(ael.date_today()):
        if not ret:
            ret=default_value
            args[par_name]=str(ret)
        else:
            try:
                offset=int(ret[0])
                ret=ael.date_today().add_days(offset)
            except:
            	ret=ael.date(ret[0])
    return ret



#########################################################
# Other helper operations
#########################################################

def cmp_ins(a, b):
    """ Sorts on insid """
    return cmp(a.insid, b.insid)


def import_required_modules(modules):
    """ This operation checks if the required FRONT ARENA modules are visible.
         This operation should be called after connect to always import a saved module
             in the database before a file.
        Returns 1 OK and 0 an failure"""
    no_errors=1
    for m in modules:
        try:
            c=('import %s' % m)
            exec(c)
        except:
            print "Failed to import module:", m
            no_errors=0
    return no_errors


def local_exit(name,n=0):
    """ To avoid the problem that local_exit(__name__,) halts Prime or Atlas.
    --- Note: local_exit(__name__,) raises the exception SystemExit exception and this
    --- should always be handled by ael.
    --- Must always be called by the special variable __name__"""
    if name == '__main__':
        sys.exit(n)
    else:
        raise RuntimeError, "local_exit(%d)" % n


def is_und_expired(ins, exp_day):
    """ predicate for checking if underlyings are expired. Defined for combinations."""
    has_legs=0
    for e in ael.Instrument.select('und_insaddr=%d' % ins.insaddr):
        has_legs=1
        if e.exp_day and e.exp_day < exp_day:
            return 1
    if not has_legs and not ins.trades() and not ael.OrderBook.select('insaddr=%d' % ins.insaddr):
        return 1
    return 0


def log_skip(insid, n):
    global reason_descr, report_descr
    log("SKIP %s.Reason: %s" % (insid, reason_descr[n]))
    t=report_descr.get('SKIP', [])
    t.append((insid, n))
    report_descr['SKIP']=t

def determent_instruments(instypes,exp_day,alias_type_names,listnodes,insids=[]):
    """ Returns a dictionary of {insaddr:ael_entity instrument,} """
    #
    # Note: Values are already validated.
    #
    ins={} # Use a dictionary to be able to sure unique number of instruments
    if len(insids) > 0:
        for insid in insids:
            i=ael.Instrument[insid]
            if i and (not instypes or i.instype in instypes):
                ins[i.insaddr]=i
    elif not instypes:
        for i in ael.Instrument.select():
            ins[i.insaddr]=i
    else:
        for type in instypes:
            c=("instype='%s'" % type)
            for i in ael.Instrument.select(c):
                ins[i.insaddr]=i
    log('Number of instruments before filtering: %d' % len(ins))
    #
    # Filter generic and default instruments
    #
    for (insaddr, i) in ins.items():
        if i.generic:
            del ins[insaddr]
        elif re.search('DEFAULT', i.insid, re.I):
            del ins[insaddr]
    log('Number of instruments after generic and default name filtering: %d' % len(ins))
    #
    # Filter on exp_day, underlyings is also handled
    #
    log('Filtering on exp_day < %s' % str(exp_day))
    for (insaddr, i) in ins.items():
        if (not i.exp_day and not is_und_expired(i, exp_day)) or i.exp_day >= exp_day:
            del ins[insaddr]

    filters=[(alias_type_names, ael.InstrAliasType, ['InstrumentAlias'], 'aliastypes'),
        (listnodes, ael.ListNode, ['ListLeif', 'OrderBook'], 'markets')]

    for (values, ael_table, record_types, logging) in filters:
        if not values or len(ins) <= 0:
            continue
        log("Number of instruments before filtering on %s: %d" % (logging, len(ins.keys())))
        #
        # It is assumed faster to read all reference_in() and then
        # check if the instrument should be included.
        # But it may be better to use dbsql() instead.
        #
        log("Building filter for %s..." % logging)
        filter={} # of insaddr numbers
        for v in values:
            log("+ process %s: %s" % (logging, v))
            for e in ael_table[v].reference_in():
                if e.record_type in record_types:
                    try:    filter[e.insaddr.insaddr]=None # ! Works for many record_types
                    except: pass

        log("Filtering instrument by %s..." % logging)
        for insaddr in ins.keys():
            if not filter.has_key(insaddr): del ins[insaddr]
    log("Number of instruments after filtering: %d" % len(ins.keys()))
    return ins.values()




def list_affected_volas(instruments):
    """ Operation for listing affected volatility surfaces
        if instruments are deleted """

    # Check if vola point can be used
    affected_surfaces={}
    log('Checking affected VolaSurfaces...')
    insaddrs={}
    dangling_points=[]
    for i in instruments:
        insaddrs[i.insaddr]=i.insaddr

    try:
        log('VolaSurface: Checking according to NEW model.')

        # Build a table of seqnbr:vol_name
        surfaces={}
        stmt='select seqnbr,vol_name from volatility'
        for row in ael.dbsql(stmt)[0]:
            surfaces[int(row[0])]=row[1]

        exists_dangling_points=0
        tmp={}
        for table in ['vol_beta_benchmark', 'vol_beta_point', 'vol_point', 'volatility_cell']:
            stmt='''select vol_seqnbr,insaddr from %s''' % table
            try:
                #print stmt
                rows=ael.dbsql(stmt)[0]
                for row in rows:
                    insaddr=int(row[1])
                    vol_seqnbr=int(row[0])
                    try:
                        if insaddrs.has_key(insaddr) and not tmp.has_key(vol_seqnbr):
                            tmp[vol_seqnbr]=None
                    except:
                        exists_dangling_points=1
                        pass

            except:
                pass
        # Fix return values
        for k in tmp.keys():
            affected_surfaces[surfaces[k]]=None
        if exists_dangling_points:
            logW('Dangling points detected!')
        if len(affected_surfaces) == 0:
            raise 'Trying using the old model'
    except:
        log('VolaSurface: Checking according to OLD model.')
        for p in ael.Parameter.select("type='VOL'"):
            for e in p.reference_in():
                if e.record_type == 'Instrument' and insaddrs.has_key(e.insaddr):
                    affected_surfaces[p.name]=None
                    break # check next parameter
    log('Finished with checking vola surfaces')
    return affected_surfaces.keys()


def cmp_reason(a, b):
    ret=cmp(a[1], b[1])
    if not ret:
        ret=cmp(a[0], b[0])
    return ret

def generate_report(action,filename,args,summary=None,affected_volas=None):
    global report_descr, reason_descr, testmode
    try: fp=open(filename, 'w')
    except:
        logE("Failed to open file: %s. Can't generate report." % filename)
        return
    action_map={'Archive':'Archived','Delete':'Deleted','Keep':'Keept'}

    sep  ='='*60+'\n'
    sep2 ='-'*60+'\n'
    line ='| %-56s |\n'
    line2='%-60s\n'
    log("Generating report: %s" %filename)

    #Header
    fp.write(sep)
    s="Report Date: %s" % str(ael.date_today())
    fp.write(line % s)
    mode=''
    if testmode:
        mode=' (in testmode)'
    s="ACTION: %s%s" % (action, mode)
    fp.write(line % s)

    fp.write(line % 'ARGUMENTS:')
    keys=args.keys()
    keys.sort()
    for k in keys:
        if k == 'password':
            v='********'
        else:
            v=str(args[k])
        s="  %-22s: %s" % (k, v)
        fp.write(line % s)
    fp.write(sep)

    # Handling and Failed section
    simple_section=[(action, 'The following Instruments were %s:'),
        ('Failed', 'Failed to %s the following instruments:')]

    for (key, format) in simple_section:
        if report_descr.get(key):
            fp.write(sep2)
            s=format % action_map.get(action, 'Unknown')
            fp.write(line % s)
            fp.write(sep2)
            s='INSID'
            fp.write(line2 % s)
            s='-----'
            fp.write(line2 % s)
            for insid in report_descr[key]:
                fp.write(line2 % insid)
            fp.write('\n\n')

    # Skip section
    if report_descr.get('SKIP'):
        fp.write(sep2)
        f='%-40s%s'
        s='The following instruments were skipped or'
        fp.write(line % s)
        s='included because of position handling choices:'
        fp.write(line % s)
        fp.write(sep2)
        s=f % ('INSID', 'REASON')
        fp.write(line2 % s)
        s=f % ('-----', '------')
        fp.write(line2 % s)
        values=report_descr['SKIP']
        values.sort(cmp_reason)
        for (insid, reason_tag) in values:
            s=f % (insid, reason_descr.get(reason_tag, 'Unknown'))
            fp.write(line2 % s)
        fp.write('\n\n')

    if affected_volas:
        fp.write(sep2)
        fp.write(line % 'The following Volatility Surfaces may be affected')
        fp.write(line % 'by deletion of above described instruments:')
        fp.write(line % '(that instrument may be skipped is ignored')
        fp.write(line % 'in the listing i.e. the list may be to long)')
        fp.write(sep2)
        affected_volas.sort()
        for v in affected_volas:
            fp.write(line2 % v)
        fp.write('\n\n')


    if summary:
        fp.write(sep)
        fp.write(line % 'SUMMARY:')
        s='%-20s%-10s%-10s%-10s' % ('TABLE', 'N-DELETED', 'N-ERRORS', 'N-IGNORED')
        fp.write(line % s)
        fp.write(line % ('-'*50))
        keys=summary.keys()
        keys.sort()
        for k in keys:
            (n, e, i)=summary[k]
            s='%-20s%-10d%-10d%-10d' % (k, n, e, i)
            fp.write(line % s)
        fp.write(sep)
    log("Done Generating Report!")
    return


def now():
    return time.strftime('%c', time.localtime(time.time()))

def only_zero_pos(i):
    """ Checks if all positions are zero. Uses FDMPosition"""
    positions={}
    for t in i.trades():
        if t.prfnbr:
            positions[(t.prfnbr.prfnbr, i.insaddr)]=None
    if not positions:
        return 1
    import FDMPosition
    for (prfnbr, insaddr) in positions.keys():
        pos=FDMPosition.FDMPosition(prfnbr, insaddr)
        if not (zero(pos.Qty()) and zero(pos.Rpl())):
            return 0
    return 1






def strdup(s):
    """ to overcome problems with getopt """
    n=''
    for i in s:
        n=n+i
    return n


def zero(a):
    """ Defines precision"""
    if abs(a) < 0.000001:
        return 1
    return 0

#=========================================================================
# Were the work is actually done
#=========================================================================
def perform_instrument_expiry(args):
    global dat_filename, log_filename, rep_filename, testmode, reason_descr, report_descr

    #####################################################
    # Get the parameters
    #####################################################
    instrument_handling	    = set_par_value('instrument_handling', 'Keep', args)
    include_zero_pos	    = set_par_value('include_zero_pos', 'No', args)
    cash_post_nonzero_pos   = set_par_value('cash_post_nonzero_pos', 'No', args)
    used_cash_post_curr     = set_par_value('used_cash_post_curr', 'Accounting', args)
    force                   = set_par_value('force', 'No', args)
    exp_date                = set_par_value('exp_date', ael.date_today(), args)
    report_path             = set_par_value('report_path', '', args) # trick if '' is false
    instypes		    = set_par_value('instypes', ['Option', 'Future/Forward'], args)
    insids		    = get_par('instruments', args)
    markets		    = get_par('markets', args)
    und_insids		    = get_par('underlyings', args)
    aliastypes		    = set_par_value('aliastypes', [], args)
    list_vola		    = set_par_value('list_affected_volas', 'No', args)
    dat_file		    = get_par('dat_filename', args)
    tmp                     = set_par_value('testmode', 'No', args)
    if not testmode: testmode = tmp  # Special to be able to override in ini-file.



    #####################################################
    # Check that required modules could be imported
    #####################################################
    modules=''
    if instrument_handling != 'Keep'and include_zero_pos:
        modules='FDMPosition,FDMCascadeHandler'
    elif instrument_handling != 'Keep':
        modules='FDMCascadeHandler'
    if modules:
        if not import_required_modules(string.split(modules, ',')):
            msg="Unable to import required modules[%s]. Can't continue!" % modules
            logW(msg)
            raise 'Abort Execution: '+msg


    #####################################################
    # Report and logging
    #####################################################

    if report_path:
        import os
        if not os.path.exists(report_path):
            os.makedirs(report_path)
            print "Created directory:", report_path
        module='instrument_expiry_maintenance'
        d_str=ael.date_today().to_string(ael.DATE_Quick)
        fileprefix=os.path.join(report_path, "%s_%s" % (module, d_str))
        n=''
        j=0
        while os.path.exists(fileprefix+n+".txt"):
            j=j+1
            if j > 0:
                n="_%d" % j
            if j > 100:
                log("More than 100 report files exists! Aborts execution!")
                local_exit(2)
        log_filename=os.path.normpath(fileprefix+n+".log")
        rep_filename=os.path.normpath(fileprefix+n+".txt")
	dat_filename=os.path.normpath(fileprefix+n+".dat")


    #####################################################
    # Get the markets listnodes
    #####################################################
    listnodes=[] #Note: listnodes has no unique id
    if markets:
        #Note: can't use market_ptynbr constraint on ListNode
        for ln in ael.ListNode.select():
            if ln.market_ptynbr and ln.market_ptynbr.type == 'Market' and ln.market_ptynbr.ptyid in markets:
                listnodes.append(ln.nodnbr)

    #####################################################
    # Determent the set of instruments
    #####################################################
    instruments=[] # A list of ael entities of type Instrument
    if dat_file:
        fp=open(dat_file[0], 'r')
        log('Opened file: %s' % dat_file[0])
        n_found=0
        n_not_found=0
        for line in fp.readlines():
            if line[0] == '#': continue
            line=line[:-1]
            values=string.split(line, ';')
            if len(values) == 2:
                (insid, insaddr)=values
                if ael.Instrument[insid]:
                    instruments.append(ael.Instrument[insid])
                    n_found=n_found+1
              	elif ael.Instrument[int(insaddr)]:
                    instruments.append(ael.Instrument[int(insaddr)])
                    n_found=n_found+1
              	else:
                    log('Unable to find instrument %s[%s]' % (insid, str(insaddr)))
                    n_not_found=n_not_found+1
        if n_found > 0 and n_not_found > 0:
            logW('Some instruments were missing. Continues anyway...')
        elif n_found > 0:
            log('Read %d instruments from file: %s' % (len(instruments), dat_file[0]))
    elif und_insids:
        if not insids:
            instruments=[]
        else:
            instruments=insids
        for und_insid in und_insids:
            ins=ael.Instrument[und_insid]
            if not ins:
                print "Error: Instrument %s in underlyings doesn't exists in database! Aborts." % und_insid
                local_exit(__name__, 2)
            instruments.append(ins.insid)
            c=("und_insaddr=%d" % ins.insaddr)
            for der in ael.Instrument.select(c):
                instruments.append(der.insid)
        instruments=determent_instruments(instypes, exp_date, aliastypes, listnodes, instruments)
    elif insids:
        #See comment above, market and instype are ignored
        for i in insids:
            instruments.append(ael.Instrument[i])
    else:
        instruments=determent_instruments(instypes, exp_date, aliastypes, listnodes)
    if len(instruments) == 0:
        logE("No instruments match filter criteria!")
        local_exit(__name__, 1)
    else:
        log("Found %d expired instruments" % len(instruments))

    instruments.sort(cmp_ins) # Nice for logging and generating report


    #####################################################
    #
    # PRE-PHASE: Logging of handled instruments
    #
    #####################################################
    if dat_filename:
        fp=open(dat_filename, 'w')
        fp.write("# insid;insaddr\n")
        for i in instruments:
            fp.write("%s;%d\n" % (i.insid, i.insaddr))
        fp.close()
        log("Generated file: %s" % dat_filename)

    #####################################################
    #
    # PHASE 1
    #
    #####################################################


    log('PHASE 1: Dropping of ListNodes, OrderBooks, PriceDefinitions and OwnOrders...')

    ###########################################################
    #Delete listleafs for instruments in instruments.
    #For performance resons each list nodes leafs are handled in
    #one transaction.
    ###########################################################
    log('Reading ListLeafs...')
    list_nodes={}   # nodenbr : (ListNode,[list_leaf lefnbr's])
    n=0             # Counter of number of list leafs
    n_errors=0
    summary={}
    dangling_leafs={}
    for i in instruments:
        for leaf in ael.ListLeaf.select("insaddr=%d" % i.insaddr):
            try: # To avoid problems with dangling list_leafs
                if not leaf.nodnbr or not leaf.insaddr:
                    dangling_leafs[leaf.lefnbr]=None
                else:
                    (ln, ld)=list_nodes.get(leaf.nodnbr.nodnbr, (leaf.nodnbr, {}))
                    ld[leaf.lefnbr]=None
                    list_nodes[ln.nodnbr]=(ln, ld)
                    n=n+1
            except:
                n_errors=n_errors+1
                logE('Dangling ListLeaf: %d' % leaf.lefnbr)


    ###########################################################
    # OK, now delete OK elements
    ###########################################################
    log('Deleting %d ListLeafs...' % n)
    n=0 # True number
    for (dummy, (ln, ld)) in list_nodes.items():
        log('+ deleting %-5d leafs for ListNode %s(%d)' % (len(ld), ln.id, ln.nodnbr))
        if not testmode:
            ln2=ln.clone()
            for leaf in ln2.leafs().members():
                if ld.has_key(leaf.lefnbr):
                    leaf.delete()
                    n=n+1
            ln2.commit()
    ael.poll() # refresh
    log('Delete of ListLeafs finished!')
    summary['ListLeif']=(n, n_errors, 0)
    if n_errors > 0:
        logW('Found %d danglings leafs! See logfile or printout' % n_errors)

    if len(dangling_leafs) > 0:
        log('Deleting %d dangling ListLeafs...' % len(dangling_leafs))
        leafs=map(str, dangling_leafs.keys())
        i=0
        n_max=100
        tmp=[]
        import FDMCascadeHandler
        h=FDMCascadeHandler.FDMCascadeHandler()
        while leafs:
            tmp.append(leafs.pop(0))
            if len(tmp) == n_max:
                stmt="delete from list_leaf where lefnbr in (%s)" % string.join(tmp, ',')
                ael.dbsql(stmt)
                tmp=[]
        if tmp:
            stmt="delete from list_leaf where lefnbr in (%s)" % string.join(tmp, ',')
            ael.dbsql(stmt)
        log('Synchronize with ads')
        h.synchronize_with_ads()
        log('Deleted %d dangling ListLeafs!' % len(dangling_leafs))
        summary['Dangling ListLeif']=(n, n_errors, 0)





    ###########################################################
    # Dropipping PriceDefinitions, OrderBooks and OwnOrders is done in the same way
    # except that for an OwnOrders trade references must be checked or ignored.
    # To avoid reading to much data errors in dropping OwnOrders is done by trusting
    # check of reference integrity by server.
    ###########################################################
    table_descr=[('OrderBook', 'order_book'),
        ('PriceDefinition', 'price_definition'),
        ('OwnOrder', 'own_order')]
    ignore_ins={} # dict of insaddr of instruments to ignore because of own order references
    n_errors_own=0 #OwnOrders
    n_errors=0 #
    n_commit_freq=500 # Commit frequence
    for (name, dbsql_name) in table_descr:
        log("Reading the %s's..." % name)
        exec('ael_table=ael.%s' % name)
        entities=[]
        for i in instruments:
            selection=[]
            try:
                if name == 'OwnOrder':
                    sel=i.own_orders()
                else:
                    sel= ael_table.select('insaddr=%d' % i.insaddr)
                for e in sel:
                    entities.append(e)
            except:
                #############################################
                # Try using dbsql because select doesn't work
                # on OwnOrders
                #############################################
                logW('Tries with dbsql for %s on %s' % (name, i.insid))
                id=''
                for k in ael_table.keys():
                    if k[1] == 'primary':
                        id=k[0]
                        break
                if id:
                    stmt='select %s from %s where insaddr = %d' % (id, dbsql_name, i.insaddr)
                    #logW('Tries with dbsql statement: %s' % stmt)
                    try:
                        for id in ael.dbsql(stmt)[0]:
                            entities.append(ael_table[int(id[0])])
                    except:
                        logE('ERROR: Failed to select %d for %s' % (i.insaddr, name))
        log("Deleting %d %s's..." % (len(entities), name))
        n_del=0
        n_err=0
        n_ign=0
        if not testmode:
            ael.begin_transaction()
            for j in range(len(entities)):
                if not j%n_commit_freq:
                    ael.commit_transaction()
                    log('Commited %d(%d) %s' % (n_commit_freq, j, name))
                    ael.begin_transaction()
                e=entities[j]
                try:
                    e.delete()
                    n_del=n_del+1
                except:
                    if name != 'OwnOrder':
                        logE('Failed to delete:\n%s\n\n' % e.pp())
                        n_errors=n_errors+1
                        n_err=n_err+1
                    else:
                        n_errors_own=n_errors_own
                        ignore_ins[e.insaddr.insaddr]=None
                        n_ign=n_ign+1
        else:
            n_del=len(entities) # For test logging
        try:
            ael.commit_transaction()
            log('Commited %d(%d) %n' % (j%n_commit_freq, j, name))
        except: pass
        summary[name]=(n_del, n_err, n_ign)
        ael.poll() #refresh
        log('Delete of %s finished!' % name)




    ###########################################################
    # Log found errors.
    # NOTE: OwnOrder errors should be ignored!
    ###########################################################

    if n_errors+n_errors_own > 0:
        names=[]
        for (n, d) in table_descr:
            names.append(n)
        tables=string.join(names, ',')
        logW('Total number of errors when deleting %s: %d' % (tables, n_errors+n_errors_own))
    if n_errors_own > 0:
        logW('Total number of OwnOrder errors: %d' % n_errors_own)
        logW('Total number of instruments to skipped(by OwnOrder errors): %d' % len(ignore_ins))





    ###########################################################
    # If instruments shouldn't be deleted
    # we are done.
    ###########################################################
    if instrument_handling == 'Keep':
        if report_path:
            generate_report(instrument_handling, rep_filename, args, summary)
        log('Done!')
        return 1



    ###########################################################
    #
    # PHASE 2
    #
    ###########################################################


    ###########################################################
    # List affected volas if wanted
    ###########################################################
    affected_volas=[]
    if list_vola:
        affected_volas=list_affected_volas(instruments)
        affected_volas.sort()
        for v in affected_volas:
            log('VolaSurface %s may be affected' % v)

    ###########################################################
    # Delete the instrument if no trades exists or (if requested)
    # because all positions are zero.
    # NOTE: It is assumed that number of trades in instruments
    # handled here are not that many.
    ###########################################################

    log('PHASE 2: Dropping of instruments...')
    import FDMCascadeHandler
    h=FDMCascadeHandler.FDMCascadeHandler()
    #h.verbose=1
    n=0
    n_errors=0
    n_ignore=0
    cash_post_ins=[]
    for i in instruments:
        if not force and ignore_ins.has_key(i.insaddr):
            log_skip(i.insid, 0)
            n_ignore=n_ignore+1
            continue
        if len(i.trades()) > 0:
            if not force and not include_zero_pos and not cash_post_nonzero_pos:
                log_skip(i.insid, 1)
                n_ignore=n_ignore+1
                continue
            if not force and (not cash_post_nonzero_pos and not only_zero_pos(i)):
                log_skip(i.insid, 2)
                n_ignore=n_ignore+1
                continue
            if instrument_handling == 'Delete': # Check BO Confirmed trades
                do_ignore=0
                for t in i.trades():
                    if t.bo_trdnbr > 0:
                        do_ignore=1
                        break
                if do_ignore:
                    log_skip(i.insid, 6)
                    n_ignore=n_ignore+1
                    continue

        ###########################################################
        # Cash Post all positions in the instrument.
        ###########################################################
            if cash_post_nonzero_pos:
                positions={}
                errors=0
                for t in i.trades():
                    positions[(t.prfnbr, t.insaddr)]=None
                for (port, ins) in positions.keys():
                    import FDMPosition
                    pos=FDMPosition.FDMPosition(port.prfnbr, ins.insaddr)
                    curr=pos.GetCurr(used_cash_post_curr)
                    try:
                        if instrument_handling == 'Delete':
                            if not testmode: pos.cash_post(None, curr, 1, 1)
                        else:
                            if not testmode: pos.cash_post(None, curr, 1, 0)
                    except:
                        errors=1
                        logE("Failed to cash post position %s!" % pos.Name())
                        n_ignore=n_ignore+1
                if errors:
                    t=report_descr.get('Failed', [])
                    t.append(i.insid)
                    report_descr['Failed']=t
                    n_errors=n_errors+1
                    log_skip(i.insid, 5)
                    continue

        ###########################################################
        # Note: The FDMCascadeHandler deletes all references to an
        # instrument i.e. take care of of trades in zero pos also
        ###########################################################


        #log('Tries to deletes instrument: %s' % i.insid)
        insid=strdup(i.insid)       # Save for logging
        insaddr=i.insaddr           # Save for logging
        try:
            if instrument_handling == 'Delete':
                if not testmode: h.delete_object('instrument', insaddr)
            elif instrument_handling == 'Archive':
                if not testmode: h.archive_object('instrument', insaddr)
            t=report_descr.get(instrument_handling, [])
            t.append(insid)
            report_descr[instrument_handling]=t
            log('%sd instrument %s' % (instrument_handling, insid))
            n=n+1
        except:
            logE('Failed to %s instrument: %s' % (instrument_handling, insid))
            t=report_descr.get('Failed', [])
            t.append(insid)
            report_descr['Failed']=t
            n_errors=n_errors+1
    summary['Instrument']=(n, n_errors, n_ignore)
    ###########################################################
    # And we are done
    ###########################################################
    s='SUMMARY:\n%-15s%-20s%-10s%-10s%-10s\n%-15s%-s\n' % (' ', 'TABLE', 'N-DELETED', 'N-ERRORS', 'N-IGNORED', ' ', '-'*50)

    keys=summary.keys()
    keys.sort()
    for k in keys:
        (n, e, i)=summary[k]
        s2='%-15s%-20s%-10d%-10d%-10d\n' % (' ', k, n, e, i)
        s=s+s2
    log(s)

    #log('SUMMARY: Number of handled(%s) instruments: %d' % (instrument_handling,n))
    #if n_errors > 0:
    #    log('SUMMARY: Number of errors: %d' % n_errors)

    if report_path:
        generate_report(instrument_handling, rep_filename, args, summary, affected_volas)

    log("Done!")



#=======================================================================
# Main
#=======================================================================
from_idle=0
inifile="C:\\Temp\myinifile.txt"
if  __name__ == '__main__':
    try:
        #Note: starting script using ael consumes parameters by inivar
        #i.e. -inifile consumes -i so other options needs to be used.
        opts, args = getopt.getopt(sys.argv[1:], 'f:t')
        if len(opts) < 0: raise getopt.error, ''
    except getopt.error, msg:
        print msg
        print USAGE
        local_exit(__name__, 2)

    inifile=None
    applic='PMaintExpIns'
    inifile="C:\\Temp\myinifile.txt" # test


    for o, a in opts:
        if o == '-f': inifile = strdup(a)
        if o == '-t': testmode = 1

    if not inifile:
        print USAGE
        local_exit(__name__, 2)

    args=parse_inifile(inifile)

    error=0
    for a in mandatory:
        if not args.has_key(a):
            print "Error: argument %s in inifile must be given" % a
            error=1
    if error:
        print "Errors in inifile found! Aborts."
        local_exit(__name__, 2)

    ael.connect(args['server'], args['username'], args['password'], 'DelExpIns')
    ael.poll()
    import FDMCascadeHandler, FDMPosition
    log("Connected to server %s" % args['server'])
    perform_instrument_expiry(args)



elif from_idle:
    inifile="C:\\Temp\myinifile.txt"
    args=parse_inifile(inifile)
    error=0
    for a in mandatory:
        if not args.has_key(a):
            print "Error: argument %s in inifile must be given" % a
            error=1
    if error:
        print "Errors in inifile found! Aborts."
        local_exit(__name__, 2)
    perform_instrument_expiry(args)


else:
    import FDMCascadeHandler, FDMPosition
    insvect = []
    marklist = []
    instypes = []
    undvect = []
    aliasvect=[]
    dat_filevect=[]

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

    for at in ael.InstrAliasType.select():
        aliasvect.append(at.alias_type_name)
    aliasvect.sort()

    default_report_path='c:/temp'
    module='instrument_expiry_maintenance'
    if os.path.exists(default_report_path):
        for name in os.listdir(default_report_path):
            if re.search("%s.*\.dat" % module, name, re.I):
                dat_filevect.append(os.path.normpath(os.path.join(default_report_path, name)))
        


    ael_variables = [
        ('2_instypes', 'InsTypes', 'string', instypes, 'Option,Future/Forward', 0, 1),
        ('7_instruments', 'Instruments', 'string', insvect, '', 0, 0),
        ('4_markets', 'Markets', 'string', marklist, '', 0, 1),
        ('5_underlyings', 'Underlyings', 'string', undvect, '', 0, 1),
        ('1_exp_date', 'Date', 'string', [], str(ael.date_today()), 0, 0),
        ('8_aliastypes', 'AliasTypes', 'string', aliasvect, '', 0, 1),
        ('3_instrument_handling', 'InstrumentHandling', 'string', ['Archive', 'Delete', 'Keep'], 'Keep', 0, 0),
        ('9_include_zero_pos', 'IncludeZeroPositions', 'string', ['Yes', 'No'], 'No', 0, 0),
        ('6_report_path', 'ReportDirecoryPath', 'string', [], default_report_path, 0, 0),
        ('e_force', 'ForceHandling', 'string', ['Yes', 'No'], 'No', 0, 0),
        ('0_testmode', 'OnlyTest', 'string', ['Yes', 'No'], 'No', 0, 0),
        ('c_list_affected_volas', 'ListAffectedVolaSurfaces', 'string', ['Yes', 'No'], 'No', 0, 0),
        ('a_cash_post_nonzero_pos', 'CashPostNonZeroPos', 'string', ['Yes', 'No'], 'No', 0, 0),
        ('b_used_cash_post_curr', 'CashPostCurrency', 'string', FDMPosition.get_valid_styles(), 'Accounting', 0, 0),
        ('d_dat_filename', 'InstrumentNameFile (.dat)', 'string', dat_filevect, '', 0, 0),
        ('f_log_report', 'LogReportInConsole', 'string', ['Yes', 'No'], 'No', 0, 0)]

    def ael_main(dictionary):
        global rep_filename
        tmp={}
        do_log_report=0
        for (k, v) in dictionary.items():
            if k[2:] == 'log_report':
                if v == 'Yes':
                    do_log_report=1
                continue
            tmp[k[2:]]=v
        print tmp
        perform_instrument_expiry(tmp)
        if do_log_report:
            fp=open(rep_filename, 'r')
            print "\n\n"
            for line in fp.readlines():
                line=line[:-1]
                print line
            fp.close()



if __name__ == '__main__': # Started from command promt
    print "Done!"
    ael.disconnect()

