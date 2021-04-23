""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementAggregation.py - aggregation of settlements

    (c) Copyright 2004 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module contains functionality for aggregating settlements.

    The functionality of this script follows that of standard FRONT ARENA
    aggregation scripts:

    When running the script from a client in non archived mode only aggregation
    is possible, whereas in archived mode both aggregation and deaggregation is
    possible (though preferably archived mode should only be used for
    deaggregation).

    Three variables can be added at run time and these are open_days, acquirer
    and portfolio. Only open_days is mandatory and it specifies the number of
    banking days that settlements should be kept open for (not aggregated).
    When aggregating, also an acquier and/or portfolio can be specified but
    if they are left unspecified, all settlements up to and including
    the specified date are aggregated. Only settlements in status Closed
    are aggregated and all settlements in void referencing a closed settlement
    are archived. There is one exception to this though. If a net settlement
    record lacks portfolio information it is not aggregated.

    In archived mode all settlements with value day before the given date are
    aggregated and archived, and all settlements after this date are
    dearchived.

    The script can be run either from the AEL Module editor or from the command
    line, both on Windows and Solaris.

ENDDESCRIPTION 
----------------------------------------------------------------------------"""
import ael, time

securities = ['Security Nominal', 'End Security']
agg_party = None
agg_user = None
agg_dict = {}

def remove_net(settles):
    real_list = []
    for s in settles:
        settle = ael.Settlement[s]
        if settle.ref_type=='Net' and not settle.to_prfnbr and not \
           settle.from_prfnbr:
            pass
        else:
            real_list.append(settle)
    return real_list

def sv(val):
    if val == None:
        return 'NULL'
    else:
        return `val`
    
def get_agg_settlements(prf, acquirer):
    settle_list = []
    for settle in ael.Settlement.select():
        if settle.status == 'Closed' and settle.aggregate == 0:
            prf_ok = 0
            if not prf or \
               (settle.to_prfnbr and settle.to_prfnbr.prfnbr==prf.prfnbr) or \
               (settle.from_prfnbr and settle.from_prfnbr.prfnbr==prf.prfnbr):
                prf_ok = 1

            acquirer_ok = 0
            if not acquirer or settle.acquirer_ptyid == acquirer.ptyid:
                acquirer_ok = 1

            if prf_ok and acquirer_ok:
                settle_list.append(settle.seqnbr)

    if len(settle_list)>0:
        real_list = remove_net(settle_list)
        return real_list
    else:
        return []

def get_prfnbr(settle):
    prfnbr = 0
    if not settle:
        return prfnbr
    if settle.to_prfnbr:
        prfnbr = settle.to_prfnbr.prfnbr
    elif settle.from_prfnbr:
        prfnbr = settle.from_prfnbr.prfnbr
    return prfnbr

def create_aggregate(settle, prfnbr, agg_date):
    global securities
    global agg_party
    global agg_user
    
    agg = ael.Settlement.new()
    if settle.type in securities:
        agg.type = 'Aggregate Security'
        agg.org_sec_nom = 1
        if settle.sec_insaddr:
            agg.sec_insaddr = settle.sec_insaddr.insaddr
    else:
        agg.type = 'Aggregate Cash'

    agg.curr = settle.curr.insaddr
    agg.value_day = agg_date
    agg.to_prfnbr = prfnbr
    agg.from_prfnbr = prfnbr
    agg.status = 'Closed'
    agg.acquirer_ptyid = settle.acquirer_ptyid
    agg.acquirer_account = settle.acquirer_account
    agg.acquirer_accname = settle.acquirer_accname
    agg.party_ptyid = agg_party.ptyid
    agg.aggregate = 1
    agg.archive_status = 0
    agg.creat_usrnbr = agg_user.usrnbr
    agg.creat_time = ael.date_today().to_time()
    agg.updat_usrnbr = agg_user.usrnbr
    agg.updat_time = ael.date_today().to_time()
    agg.protection = 'W:RW,O:RW,G:RW,U:RW'
    agg.owner_usrnbr = agg_user.usrnbr

    return agg

def do_comparison(settle, prf, type, curr, account, sec_insaddr):
    if not settle or not curr or not account:
        return 0
    if type==1 and not settle.type=='Aggregate Security': #type=1 means security
        return 0
    if type==0 and settle.type=='Aggregate Security':
        return 0
    if settle.sec_insaddr and settle.sec_insaddr.insaddr != sec_insaddr:
        return 0
    s_prf = get_prfnbr(settle)
    if not s_prf==prf:
        return 0
    if settle.curr:
        if not settle.curr.insaddr==curr:
            return 0
    settle_acc = None
    par_acc = settle.acquirer_accname
    if settle.acquirer_ptyid:
        par = ael.Party[settle.acquirer_ptyid]
        par_nbr = par.ptynbr
        if par_nbr and par_acc:
            settle_acc = ael.Account.read("ptynbr=%d and name='%s'" % \
                                          (par_nbr, par_acc))
            if settle_acc and not settle_acc.accnbr==account.accnbr:
                return 0
        else:
            return 0
    else:
        return 0
    return 1

def find_aggregate(settle, agg_dict):
    global securities

    if not settle:
        return None

    if settle.aggregate_seqnbr:
        return settle.aggregate_seqnbr    

    type = 0 # Cash settlement
    curr = 0
    prf = 0
    aggregate = None
    sec_insaddr = 0
    if settle.type in securities:
        type = 1
        if settle.sec_insaddr:
            sec_insaddr = settle.sec_insaddr.insaddr 
    if settle.curr:
        curr = settle.curr.insaddr
    prf = get_prfnbr(settle)
    s_acc = None
    par_acc = settle.acquirer_accname
    if settle.acquirer_ptyid:
        par = ael.Party[settle.acquirer_ptyid]
        par_nbr = par.ptynbr
        if par_nbr and par_acc:
            s_acc = ael.Account.read("ptynbr=%d and name='%s'" % \
                                     (par_nbr, par_acc))
    if not curr or not s_acc:
        return None
    for k, v in agg_dict.iteritems():
        if do_comparison(k, prf, type, curr, s_acc, sec_insaddr):
            return k
    agg_list = []
    sel = ael.Settlement.select()
    for s in sel:
        if s.aggregate:
            agg_list.append(s)
    for agg in agg_list:
        if do_comparison(agg, prf, type, curr, s_acc, sec_insaddr):
            return agg
    return aggregate

def archive_or_dearchive_children(settle, archive_flag):
    child_list = []
    if settle.ref_type=='Net' or settle.ref_type=='Split Part':
        child_list = ael.Settlement.select('ref_seqnbr=%d' % settle.seqnbr)
    elif settle.settle_seqnbr:
        tmp = ael.Settlement[settle.settle_seqnbr.seqnbr]
        if tmp.status!='Closed': #These will be dealt with in the first select
            if tmp:
                if tmp.ref_type=='Net' or tmp.ref_type=='Split Part':
                    clone = tmp.clone()
                    if archive_flag:
                        clone.archive_status=1
                    else:
                        clone.archive_status=0
                        clone.aggregate_seqnbr=0
                    clone.commit()
                    archive_or_dearchive_children(tmp, 1)
                else:
                    child_list = [tmp,]
    for child in child_list:
        clone = child.clone()
        if archive_flag:
            clone.archive_status = 1
        else:
            clone.archive_status = 0
            clone.aggregate_seqnbr = 0
        clone.commit()
                    
def perform_aggregation(agg_dict, agg_date, archive):
    if not agg_dict:
        return 1

    for k, v in agg_dict.iteritems():

        if k.seqnbr > 0:
            seqnbr = k.seqnbr
            ael.poll()
            k_clone = ael.Settlement[seqnbr].clone()
            k_clone.amount = 0.0
        else:
            k_clone = k
        if archive:
            str = 'Archiving'
        else:
            str = 'Dearchiving'
        str = str + ' %d settlements with currency =  %s, account = %s, '\
              'type = %s' % (len(v), k_clone.curr.insid, k_clone.acquirer_accname, k_clone.type)
        if k_clone.to_prfnbr:
            str = str + ', portfolio %s' % k_clone.to_prfnbr.prfid
        print str
 
        ael.begin_transaction()

        if archive:
            for settle in v:    
                k_clone.amount = k_clone.amount + settle.amount
        else:
            k_clone.amount = 0
        k_clone.value_day = agg_date
        k_clone.commit()

        for item in v:
            clone = item.clone()
            clone.archive_status = archive
            if archive:
                clone.aggregate_seqnbr = k_clone.seqnbr
            else:
                clone.aggregate_seqnbr = None
            clone.commit()
            archive_or_dearchive_children(item, archive)

        try:
            ael.commit_transaction()
        except:
            ael.abort_transaction()
            print 'Could not aggregate settlement'
            return 0
    return 1

def add_to_dict(dict, agg, settle):
    settle_list = []
    if dict.has_key(agg):
        settle_list = dict[agg]
    settle_list.append(settle)
    dict[agg] = settle_list
    return

def aggregate(agg_date, prf, acquirer):
    global securities

    n = 0
    agg_dict = {}
    deagg_dict = {}
    agg_list = get_agg_settlements(prf, acquirer)
    result = 1
    for settle in agg_list:
        agg = find_aggregate(settle, agg_dict)
        if agg:
            if agg.value_day > agg_date and not ael.archived_mode():
                print 'The date given is %s but there exists an \n'\
                      'aggregate trade with a later value day %s. \n'\
                      'To reaggregate this position the script must \n'\
                      'be run from a client in archived mode.' \
                      % (agg_date, agg.value_day)
                return
            elif agg_date.days_between(settle.value_day) <= 0:
                add_to_dict(agg_dict, agg, settle)
            elif settle.aggregate_seqnbr and settle.archive_status:
                add_to_dict(deagg_dict, agg, settle)
        elif agg_date.days_between(settle.value_day) <= 0:
            prfnbr = get_prfnbr(settle)
            agg = create_aggregate(settle, prfnbr, agg_date)
            settle_list = [settle,]
            agg_dict[agg] = settle_list

    remove_aggs = []
    for k, v in agg_dict.iteritems():
        if k.seqnbr < 0 and len(v) <= 3:
            remove_aggs.append(k)
    for agg in remove_aggs:
        del agg_dict[agg]

    if result and len(deagg_dict) and ael.archived_mode():
        str = 'Performing dearchiving on %d aggregates' % len(deagg_dict)
        print str
        result = perform_aggregation(deagg_dict, agg_date, 0)

    if len(agg_dict):
        str = 'Performing aggregation. Creating/updating %d aggregates' % \
            len(agg_dict)
        print str
        result = perform_aggregation(agg_dict, agg_date, 1)

    return result

try:
    if __name__ == "__main__":
        import sys, getopt

        try:
            opts, args = getopt.getopt(sys.argv[1:], \
                                       's:u:p:o:a:f:')

            if len(opts) < 4:
                raise getopt.error, ''
        except getopt.error, msg:
            print msg
            m = '''Usage: ael <config name> FSettlementAggregation.py -u username
                -p password -s server -o open days -a acquirer
                -f portfolio'''
            print m
            sys.exit(2)

        ads_address = ''
        prime_user = ''
        prime_passw = ''
        prf = None
        acquirer = None
        open_days = ''

        for o, a in opts:
            if o == '-s' : ads_address = a
            if o == '-u' : prime_user = a
            if o == '-p' : prime_passw = a
            if o == '-o' : open_days = a
            if o == '-a' : acquirer = a
            if o == '-p' : portfolio = a

        print 'Now starting to connect to AEL...'
        if not ads_address:
            ael.connect(environ['ADS_ADDRESS'], str(prime_user), str(prime_passw))
        else:
            ael.connect(ads_address, str(prime_user), str(prime_passw))

        curr = ael.used_acc_curr()
        try:
            open_days = 0 - int(open_days)
        except TypeError:
            print '-o (open days) must be an integer'
            sys.exit(2)
        agg_date = ael.date_today().add_banking_day(ael.Instrument[curr],\
                                                        open_days)
        agg_party = ael.Party['FMAINTENANCE']
        agg_user = ael.User['FMAINTENANCE']
        if agg_party and agg_user:
            if aggregate(agg_date, prf, acquirer):
                print '\nArchiving & aggregation finished %s' % \
                          time.ctime(time.time())
                ael.disconnect()
            else:
                print '\nArchiving & aggregation failed'
                sys.exit(2)
        else:
            print 'A counterparty and a user called FMAINTENANCE must exist'
            sys.exit(2)
    else:
        prfs = []
        for p in ael.Portfolio.select():
            prfs.append(p.prfid)

        acqs = []
        for a in ael.Party.select():
            if a.type=='Intern Dept':
                acqs.append(a.ptyid)

        prfs.sort()
        acqs.sort()

        ael_variables = \
            [('date', 'Date (or specify number of open days below)', 'string', '', str(ael.date_today()), 0),
             ('open_days', 'Open Business Days', 'string', '', '', 0, 1),
             ('portfolio', 'Portfolio', 'string', prfs, None, 0, 0),
             ('acquirer', 'Acquirer', 'string', acqs, None, 0, 0)]

        def ael_main(dict):
            global agg_party
            global agg_user

            prf = None
            acquirer = None
            agg_date = None
            if dict['open_days']:
                try:
                    open_days = int(dict['open_days'][0])
                except:
                    raise 'Open days has to be a number'
                curr = ael.used_acc_curr()
                open_days = 0 - open_days
                agg_date = ael.date_today().add_banking_day(\
                    ael.Instrument[curr], open_days)
            if dict['date'] and agg_date:
                raise 'Too many variables have been entered. Please enter either open days or a date.'
            elif dict['date']:
                agg_date = ael.date(dict['date'])
            if dict['portfolio']:
                prf = ael.Portfolio[dict['portfolio']]
            if dict['acquirer']:
                acquirer = ael.Party[dict['acquirer']]
            agg_party = ael.Party['FMAINTENANCE']
            agg_user = ael.User['FMAINTENANCE']
            if agg_party and agg_user:
                if aggregate(agg_date, prf, acquirer):
                    print '\nArchiving & aggregation finished %s' % \
                          time.ctime(time.time())
                else:
                    print '\nArchiving & aggregation failed'
            else:
                print 'A counterparty and a user called FMAINTENANCE must exist'
            return

except Exception, e:
    if globals().has_key('ael_variables'):
        del globals()['ael_variables']
    if globals().has_key('ael_main'):
        del globals()['ael_main']
    print 'Could not run FSettlementAggregation due to '
    print e




