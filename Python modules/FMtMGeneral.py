""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
MODULE
    FMtMGeneral - Module including all functions common to the Mark to Market
                  procedure.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module stores those functions which are common to run the Mark to
    Market procedure.

----------------------------------------------------------------------------"""
print 'Inside FMtMGeneral.'
try:
    import re
except:
    print 'The module re was not found.\n'
try:
    import sys
except:
    print 'The module sys was not found.\n'
try:
    import time
except:
    print 'The module time was not found.\n'
try:
    import ael
except ImportError:
    print 'The module ael was not found.'
    print
try:
    import FMtMVariables
    from FMtMVariables import PreferredMarkets, Verb, ExcludePreferredInsTypes
except ImportError:
    print 'The FMtMVariables module was not found'
    print

def now():
  return ttos(time.time())

LARGE_NUMBER = 10.0**30

def ttos(t):
    """ Time to string e.g. 2002-09-30 15:00:00"""
    s=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    return s

def doLog(level):
    """ For reducing some logging time """
    if Verb >= level: 
        return 1
    return 0

def log(level, s):
    """Log me."""
    if Verb >= level: 
	s=str(s)
	if s[0] == '\n':
	    print "\n%s :: %s" % (now(), s[1:])
	else:
	    print "%s :: %s" % (now(), s)
	try:
            sys.stdout.flush() # REMOVE LATER
        except:
            pass

def get_exception():
    """Returns last exception as string"""

    import sys, traceback, string
    t, v, tb=sys.exc_info()
    d=traceback.format_exception_only(t, v)
    msg=string.join(d, '')
    return msg


"""----------------------------------------------------------------------------
FUNCTION
    find_alias_ins() - Function which retrieves all instruments with a
                       certain Alias Type.

DESCRIPTION
    The function selects all instruments which have a certain Alias Type set in
    the Alias application.

ARGUMENTS
    aliastypes  String  A list of all Alias Types

RETURNS
    l       List of instruments
    count   The number of instruments
----------------------------------------------------------------------------"""

def find_alias_ins(aliastypes,calc_day=None,instypes=['Option', 'Warrant']):
    l = {}
    count = 0
    if not calc_day:
        calc_day=ael.date_today()

    for at in aliastypes:
        try:
            sl = ael.InstrumentAlias.select("type.alias_type_name = %s" % at)
            log(2, 'Number of instruments with alias of Type %s: %i' %
                (at, len(sl)))
            for s in sl:
                i = s.insaddr # Identical to row above.
                #log(3, '%s, %s' % (i.instype, i.insid))
                if (i.mtm_from_feed or i.otc) and i.instype in instypes and not is_ins_expired(i, calc_day):
                    count = count + 1
                    und = i.und_insaddr
                    if l.has_key(und):
                        l[und].append(i)
                    else:
                        l[und] = [i]
        except RuntimeError:
            log(0, "The Alias Type %s does not exist" % at)
    level=3
    if doLog(level):
        log(level, '\nResulting alias dictionary:')
        for i in l.keys():
            log(level, 'Underlying: %s' % i.insid)
            log(level, 'Options on underlying:')
            for v in l[i]:
                log(level, '%s' % v.insid)
    return (l, count)

"""----------------------------------------------------------------------------
FUNCTION
    find_opt_and_warrants_on_stock() - Function which retrieves all options and
                                       warrants on stocks which are not linked
                                       to a PriceDistributor.

DESCRIPTION
    The function selects all instruments of type option and warrant which have
    a stock as underlying and are not linked to a PriceDistributor.

RETURNS
    l       List of instruments
----------------------------------------------------------------------------"""

def find_opt_and_warrants_on_stock(calc_day=None,exclude_instypes=[]):
    l = []
    if not calc_day:
        calc_day = ael.date_today()
    inst=[]
    inst2=[]
    if not 'Option' in exclude_instypes:
        inst = ael.Instrument.select("instype = 'Option'")
    if not 'Warrant' in exclude_instypes:
        inst2 = ael.Instrument.select("instype = 'Warrant'")
    for i in inst:
        pdef = ael.PriceDefinition.select("insaddr = %d" % i.insaddr)
        if not pdef:
            try:
                if i.und_insaddr.instype == 'Stock' and not is_ins_expired(i, calc_day):
                    l.append(i)
            except:
                print 'Not possible - Stock'

    for i in inst2:
        pdef = ael.PriceDefinition.select("insaddr = %d" % i.insaddr)
        if not pdef or not i.mtm_from_feed:
            if i.und_insaddr.instype == 'Stock' and not is_ins_expired(i, calc_day):
                l.append(i)

    return l

"""----------------------------------------------------------------------------
FUNCTION
    find_opt_and_warrants_on_index() - Function which retrieves all options and
                                       warrants on indicies which are not linked
                                       to a PriceDistributor.

DESCRIPTION
    The function selects all instruments of type option and warrant which have
    an index as underlying and are not linked to a PriceDistributor.

RETURNS
    l       List of instruments
----------------------------------------------------------------------------"""

def find_opt_and_warrants_on_index(calc_day=None,exclude_instypes=[]):
    l = []
    if not calc_day:
        calc_day=ael.date_today()
    inst=[]
    inst2=[]
    if not 'Option' in exclude_instypes:
        inst = ael.Instrument.select("instype = 'Option'")
    if not 'Warrant' in exclude_instypes:
        inst2 = ael.Instrument.select("instype = 'Warrant'")
    for i in inst:
        pdef = ael.PriceDefinition.select("insaddr = %d" % i.insaddr)
        if not pdef:
            try:
                if i.und_insaddr.instype == 'EquityIndex' and not is_ins_expired(i, calc_day):
                    l.append(i)
            except:
                print 'Not possible - Equity index'
    for i in inst2:
        pdef = ael.PriceDefinition.select("insaddr = %d" % i.insaddr)
        if not pdef or not i.mtm_from_feed:
            if i.und_insaddr.instype == 'EquityIndex' and not is_ins_expired(i, calc_day):
                l.append(i)
    return l

"""----------------------------------------------------------------------------
FUNCTION
    find_distributors_ins() - Function which retrieves all instruments that
                              comes in from a certain Price Distributor.

DESCRIPTION
    The function selects all instruments which comes in from a certain Price
    Distributor.

ARGUMENTS
    distributors    String  A list of Price Distributors.

RETURNS
    l       List of instruments
    count   The number of instruments
----------------------------------------------------------------------------"""

def find_distributors_ins(distributors,calc_day=None,instypes=['Option', 'Warrant']):
    l = {} #[]
    count = 0
    if not calc_day:
        calc_day=ael.date_today()
    handled_ins2 = {}

    for d in distributors:
        log(3, '\nPrice Distributor: %s' % d)
        prdist = ael.PriceDistributor.read("disid = '%s'" % d)
        try:
            pdef = ael.PriceDefinition.select("disnbr = '%s'" % prdist.disnbr)
        except AttributeError:
            pdef = []
            log(0, 'No Price Distributor with name %s exists.' % d)

        if pdef != []:
            log(3, 'Resulting distributor list:')
        for p in pdef:
            ins = ael.Instrument.read("insaddr = '%s'" % p.insaddr.insaddr)
            if handled_ins2.has_key(ins.insid):
                log(3, "Duplicate, delete '%s' from list" % ins.insid)
            else:
                handled_ins2[ins.insid]=1
                if (ins.mtm_from_feed or ins.otc) and ins.instype in instypes and not is_ins_expired(ins, calc_day):
                    count = count+1
                    und = ins.und_insaddr
                    if l.has_key(und):
                        l[und].append(ins)
                    else:
                        l[und] = [ins]
    level=3
    if doLog(level):
        log(level, '\nResulting distributors dictionary:')
        for i in l.keys():
            log(level, 'Underlying: %s' % i.insid)
            log(level, 'Options on underlying:')
            for v in l[i]:
                log(level, '%s' % v.insid)
    return (l, count)

"""----------------------------------------------------------------------------
FUNCTION
    update_yc() - Function which updates yield curves.

DESCRIPTION
    The function updates yield curves.

ARGUMENTS
    ycs     String  A list of all yield curves to update

----------------------------------------------------------------------------"""
def update_yc(ycs):
    for name in ycs:
        yc = ael.YieldCurve[name]
        if yc == None:
            log(1, "The Yield Curve %s does not exist" % name)
            continue
        # If in historical mode, the historical yc should be updated
        try:
            if ael.historical_mode():
                yc = yc.get_historical_entity(ael.date_today())
        except:
            pass

        try:
            ycc = yc.clone()
            ycc.calculate()
            ycc.commit()
            ycc.simulate()
        except RuntimeError, msg:
            log(1, "%s, not enough price information on included instruments "\
                "in %s." % (msg, name))

"""----------------------------------------------------------------------------
FUNCTION
    volname() - Function which returns the first part of the volatility-name.

DESCRIPTION
    The function returns the instruments insid.

ARGUMENTS
    ins   Instrument An instrument.

----------------------------------------------------------------------------"""

def volname(ins, base = 'insid',vs='',curr_name=''):
    suffix=''
    if vs:
        if curr_name:
            suffix="%s/%s" % (vs, curr_name)
            max_len=31
        else:
            suffix=vs
            max_len=28
    else:
        max_len=15
    if base == 'insid' and ins.insid:
        return (str(ins.insid)+suffix)[0:max_len]
    elif base == 'extern_id2' and ins.extern_id2:
        return (str(ins.extern_id2)+suffix)[0:max_len]

"""----------------------------------------------------------------------------
FUNCTION
    create_vols_and_ctx() - Function which creates volatility-
                            surfaces and contexts.

DESCRIPTION
    The function calls the functions create_vol_surface() and
    insert_context_link().

ARGUMENTS
    volsuffix   String  A suffix that is added to an instrument to give the
                        give the created volatility surface its name
    aliastypes  String  A list of all Alias Types
    context     String  The name of the context in which the mapping of
                        instruments and volatility surfaces is done
      base         String The name of the field used when building the surface name

----------------------------------------------------------------------------"""

def create_vols_and_ctx(mtm, volsuffix, inslist, context,base='insid'):
    for vs in volsuffix:
        if inslist == mtm.aliastypes:
            instr_list = mtm.ins1.items()
        else:
            instr_list = mtm.ins4.items()
        for (ins, olist) in instr_list: #l.items():
            opt_curr_buckets={} # A list of options divided in strike_currency
            for o in olist:
                elements=opt_curr_buckets.get(o.strike_curr, [])
                elements.append(o)
                opt_curr_buckets[o.curr]=elements
            old_name = volname(ins, base, vs) # No currency appended, just suffix
            drop_context_link(ins, context, old_name)

            for (curr, olist) in opt_curr_buckets.items():
                # FIND VOLATILITY SURFACE if it already exists.
                exists=0
                surf_name=volname(ins, base, vs, curr.insid)
                exists=ael.Volatility.read('vol_name=%s' % surf_name) #FK

                # CREATE VOLATILITY SURFACE if it does not already exist.
                if not exists:
                    surf_name = create_vol_surface(ins, vs, curr.insid)

                # INSERT CONTEXT LINK if surf has been assigned.
                if surf_name:
                    insert_context_links(ins, context, surf_name, curr.insid)

    ael.poll()


"""----------------------------------------------------------------------------
FUNCTION
    update_vols() - Function which updates volatility-
                            surfaces.

DESCRIPTION
    The function calls the function update_vol_surface().

ARGUMENTS
    volsuffix   String  A suffix that is added to an instrument to give the
                        give the created volatility surface its name
    aliastypes  String  A list of all Alias Types
    context     String  The name of the context in which the mapping of
                        instruments and volatility surfaces is done
      base         String The name to use when building surface name

----------------------------------------------------------------------------"""

def update_vols(mtm, volsuffix, inslist, context,base='insid',cutoff=100.0,update_vol_instypes=[]):
    for vs in volsuffix:
        if inslist == mtm.aliastypes:
            instr_list = mtm.ins1.items()
        else:
            instr_list = mtm.ins4.items()
        for (ins, olist) in instr_list:
            opt_curr_buckets={} # A list of options divided in strike_currency
            for o in olist:
                elements=opt_curr_buckets.get(o.strike_curr, [])
                elements.append(o)
                opt_curr_buckets[o.curr]=elements
            for (curr, olist) in opt_curr_buckets.items():
                # UPDATE THE VOLATILITY SURFACE WITH THE RIGHT INSTRUMENTS
	        surf_name=volname(ins, base, vs, curr.insid)
                volat = ael.Volatility.read("vol_name= '%s'" % surf_name)
                if volat:
                    log(2, "Update volatility surface %s" % surf_name)
                    update_vol_surface(mtm, volat, olist, curr.insid, cutoff, update_vol_instypes)


"""----------------------------------------------------------------------------
FUNCTION
    create_vol_surface() - Function which creates volatility-surfaces.

DESCRIPTION
    The function creates volatility surfaces.

ARGUMENTS
    instrument  Instrument  An instrument
    volsuffix   String      A suffix that is added to the instrument to give
                            the created volatility surface its name

RETURNS
    vol_name    The new volatility surface
----------------------------------------------------------------------------"""

def create_vol_surface(ins, volsuffix,curr_name='',base='insid'):

    newvs = ael.Volatility.new()
    if curr_name:
        newvs.curr = ael.Instrument[curr_name]
    else:
        newvs.curr = ins.curr
    newvs.framework = 'Black & Scholes'
    newvs.ref_insaddr = ins
    newvs.strike_type = 'Absolute'
    newvs.use_und_market_price = 1
    newvs.vol_type = 'Benchmark Call/Put'
    newvs.vol_value_type = 'Absolute'
    newvs.abs_und_maturity = 1
    newvs.bond_vol_type = 'Price'
    newvs.vol_name = volname(ins, base, volsuffix, curr_name)
    try:
        newvs.commit()
        log(1, "Created Vol %s" % newvs.vol_name)
    except RuntimeError:
        log(1, "VolSurf exists")

    return newvs.vol_name



"""----------------------------------------------------------------------------
FUNCTION
    insert_context_links() - Function which inserts context links.

DESCRIPTION
    The function maps an instrument to a volatility surface.

ARGUMENTS
    ins         Instrument  An instrument
    context     String      The name of the context in which the mapping of
                            instruments and volatility surfaces is done
    vol_name    String      A volatility surface to which an instrument is
                            mapped
    curr_name   String      Name on the currency to map trough
----------------------------------------------------------------------------"""
def insert_context_links(ins, context, vol_name,curr_name=''):
    i = 0
    ct = ael.ContextLink.select("insaddr = " + str(ins.insaddr))
    if(ct):
        for c in ct:
            if(c.context_seqnbr.name == context and
                c.name == vol_name):
                log(3, "ContextLink %s exists" % context)
                return
    ctx = ael.Context[context].clone()
    newlink = ael.ContextLink.new(ctx)
    if curr_name:
        newlink.curr = ael.Instrument[curr_name]
    else:
        newlink.curr = ins.curr
    newlink.insaddr = ins
    newlink.type = 'Volatility'
    newlink.mapping_type = 'Instrument'
    newlink.name = vol_name
    try:
        ctx.commit()
        log(1, "Added %s to context %s" % (newlink.name, context))
    except Exception, msg:
        log(1, "Exception was %s. ContextLink exists." % msg)


"""----------------------------------------------------------------------------
FUNCTION
    drop_context_link() - Function which drop an context links.

DESCRIPTION
    The function drops a context link.

ARGUMENTS
        ins         Instrument  An instrument
        context     String      The name of the context in which the mapping of
                instruments and volatility surfaces is done
        vol_name    String      A volatility surface name to which an instrument is
                                mapped
----------------------------------------------------------------------------"""

def drop_context_link(ins, context, vol_name):
    i = 0
    ct = ael.ContextLink.select("insaddr = " + str(ins.insaddr))
    if(ct):
        for c in ct:
            if(c.context_seqnbr.name == context and c.name == vol_name):
                cxt=c.context_seqnbr.clone()
                for c2 in cxt.links().members():
                    if c2.seqnbr == c.seqnbr:
                        c2.delete()
                        cxt.commit()
                        log(1, "Dropped old ContextLink %s in context %s" % (vol_name, context))
                return


def is_ca_adjusted(ins):
    """ Checks if the instrument is CapitalAdjusted i.e. has the CASuffix """
    if not FMtMVariables.CASuffixExp: return 0
    if re.search(FMtMVariables.CASuffixExp, ins.insid):
        return 1
    return 0

"""----------------------------------------------------------------------------
FUNCTION
    update_vol_surface() - Function which updates a volatility surface.

DESCRIPTION
    The function updates a volatility surface. All expired options will be
    deleted from the volatility surface.

ARGUMENTS
    surf        String      A volatility surface to which an instrument is
                            mapped
    inslist     String      A list of instruments that could be added to the
                            volatility surface

----------------------------------------------------------------------------"""

vp_keys={}
def vp_key(insaddr):
    """ Predicate for checking so that points are unique"""
    global vp_keys
    key=vp_keys.get(insaddr)    
    if not key:
        key=(insaddr.strike_price, str(insaddr.exp_day), insaddr.call_option)
        vp_keys[insaddr]=key
    return key

def cmp_points(a, b):
    if a.insaddr and b.insaddr:
        return cmp(a.insaddr.insaddr, b.insaddr.insaddr)
    return 0

def ignore_vol_ins(ins, calc_date, no_valid_prices, update_vol_instypes):
    if not ins.instype in update_vol_instypes or \
           no_valid_prices.get(ins, 0) or \
           ins.generic == 1 or is_ins_expired(ins, calc_date) or \
           is_ca_adjusted(ins):
        return 1
    return 0

def calculate_vol(ins,quote=None):
    if  ins.otc and ins.instype in ['Option', 'Warrant']:
        sugg_vol = ins.used_vol()
    elif quote:
        sugg_vol = ins.implied_volat(2, 'Close', None, None, quote)
    else:
        sugg_vol = ins.implied_volat(2, 'Close')
    return sugg_vol
        
handled_vol={}
def update_vol_surface(mtm, surf, inslist,curr_name='',cutoff=1.0,update_vol_instypes=[]):
    global handled_vol
    st=time.time()
    #In historical mode update the historical vol-surface
    try:
        if ael.historical_mode():
            surf = surf.get_historical_entity(ael.date_today())
    except:
        pass
    vc = surf.clone()

    if curr_name:
        vc.curr=ael.Instrument[curr_name]

    vol_points = vc.points().members()
    vol_points.sort(cmp_points) # Process them in reversed insaddr order
    vol_points.reverse()
    ignore_ins={}
    remaining_points={}
    unique_points={}

    log(2, "Calculating surface: %s" %(surf.vol_name))
    if type(mtm.date) == type(''):
        calc_date=ael.date(mtm.date) # improve date handling in MTM !!!!!!!!!
    else:
        calc_date=mtm.date

    valid_ins={}  # Only points should be added for these instruments
    for ins in inslist:
        if not ignore_vol_ins(ins, calc_date, mtm.no_valid_prices, update_vol_instypes):
            valid_ins[ins]=None
    n_del=0
    n_add=0
    n_upd=0
    n_ign=0
    
    # phase1 : Remove expired points and points out of the range
    for p in vol_points:
        if doLog(4):
            log(4, '\nCandidate for Delete:%s,         %i, %s' % (p.insaddr.insid,
                                                                  p.seqnbr, p.insaddr.exp_day))
        if not p.insaddr or p.volatility <= 0.0 or p.volatility > cutoff:
            if doLog(3):
                log(3, "Delete volpoint %s %d as been illegal" % (surf.vol_name, p.seqnbr))
            p.delete()
            n_del=n_del+1
        elif ignore_vol_ins(p.insaddr, calc_date, mtm.no_valid_prices, update_vol_instypes):
            if doLog(3):
                log(3, "Delete volpoint %s %s %d" % (surf.vol_name, p.insaddr.insid, p.seqnbr))
                log(3, "delete invalid instrument : Instrument %s\n" %(p.insaddr.insid))
            p.delete()
            n_del=n_del+1
        elif unique_points.has_key(vp_key(p.insaddr)):
            if doLog(1):
                log(1, "\nDelete volpoint %s %s %d" % (surf.vol_name, p.insaddr.insid, p.seqnbr))
                log(1, "delete duplicate point for option: Instrument %s\n" %(p.insaddr.insid))
            p.delete()
            n_del=n_del+1
        else:
            remaining_points[p.insaddr]=p
            unique_points[vp_key(p.insaddr)]=p

    ael.poll() # FK
    # phase 2: process the options and store or update existing points
    instruments=valid_ins.keys()
    instruments.sort(lambda x, y: cmp(y.insaddr, x.insaddr)) # Process them in reversed insaddr order
    for ins in instruments:
        if ins.otc and ins.instype in ['Option', 'Warrant']:
            new_vol = calculate_vol(ins)/100.0
        else:
            if mtm.calc_mtm_price.has_key(ins):
                quote = mtm.calc_mtm_price.get(ins)
            else:
                quote=suggest_price(ins, calc_date, ins.curr.insid, 1, 1)
                mtm.calc_mtm_price[ins] = quote
            new_vol = calculate_vol(ins, quote)/100.0
            
        key=vp_key(ins)
        if new_vol >= cutoff or new_vol <= 0.0:
            # Remove any existing points
            if remaining_points.has_key(ins):
                p=remaining_points[ins]
                log(3, "Delete volpoint %s %d as been out of range" % (surf.vol_name, p.seqnbr))
                if unique_points.has_key(key):
                    p2=unique_points[key]
                    if p2.insaddr == ins:
                        del unique_points[key]
                p.delete()
                n_del=n_del+1
            continue

        p=remaining_points.get(ins)
        if p:
            if doLog(3):
                log(3, "Update volpoint %s %s %d" % (surf.vol_name, p.insaddr.insid, p.seqnbr))
            #log(3," update volapoint: Instrument %s,new_vol %f, mtm_price %f\n" % (ins.insid, new_vol, sugg_price))       # <--- ADD
            p.volatility = new_vol
            n_upd=n_upd+1
        else:
	    if unique_points.has_key(key): # Ignore create duplicate
		log(3, 'Ignore adding duplicate instrument %s. Uses point from %s!' % (ins.insid, unique_points.get(key).insaddr.insid))
		n_ign=n_ign+1
		continue
            log(3, "\nOption not in surface %s. Add it." % surf.vol_name)
            vp = ael.VolPoint.new(vc)
            vp.insaddr = ins
            if doLog(3):
                log(3, "Instr: %s" % ins.insid)
                log(3, "Vola: %s" % str(new_vol*100))
            vp.volatility = new_vol
            n_add=n_add+1
	    unique_points[key]=vp

    error_so_far = 0
    try:
        vc.commit()
    except:
        error_so_far = 1
        error_str = get_exception()
        log(0, "%s :: I(%d) U(%d) D(%d) IGN(%d) Time(%.2lfsec)\n" % (surf.vol_name, n_add, n_upd, n_del, n_ign, tot))
        log(0, "\n Exception when commiting surface: %s\nException[%s]" %( surf.vol_name, error_str))

    if error_so_far == 0: 
        try:
            vc.simulate()
            handled_vol[vc]=None  # Trick, suppress destruction
	    tot=time.time()-st
            if doLog(2):
	        log(2, "%s :: I(%d) U(%d) D(%d) IGN(%d) Time(%.2lfsec)\n" % (vc.vol_name, n_add, n_upd, n_del, n_ign, tot))
        except:
            error_str = get_exception()
            log(0, "\n Exception when simulating surface: %s\nException[%s]" %( surf.vol_name, error_str))

"""----------------------------------------------------------------------------
FUNCTION
    recalc_vol_surfaces() - Function which recalculates volatility surfaces.

DESCRIPTION
    The function recalculates volatility surfaces. All expired options will be
    deleted from the volatility surface.

ARGUMENTS
    surf        String      A volatility surface to update
----------------------------------------------------------------------------"""
def recalc_vol_surfaces(vol_surf_ids):
    for vol_name in vol_surf_ids:
        vol_surf = ael.Volatility[vol_name]
        try:
            if ael.historical_mode():
                vol_surf = vol_surf.get_historical_entity()
        except:
            pass
        if vol_surf == None:
            log(1, 'Volatility surface does not exist, will not recalculate %s'
                % (vol_name))
            break

        # Delete expired instruments
        vc = vol_surf.clone()
        vol_points_clone = vc.points()
        l = []
        for p in vol_points_clone:
            l.append(p)
        for i in range(len(l)):
            p = l.pop()
            if p.insaddr.generic != 1 and (p.insaddr.exp_day < ael.date_today()
                or p.volatility <= 0):
                # Delete expired options
                log(2, "Delete volpoint in vol surface %s, ins = %s " %
                    (vol_name, p.insaddr.insid))
                p.delete()

        # Recalculate the volatility surface
        vc.calculate()
        vc.commit()
        vc.simulate()
        log(2, "Updated volatility surface %s" % vol_name)


def save_daily_crossrate(descr, day, market):
    """ Function for generating a daily crossrate.
            descr : [((ins,curr,fx),[drop currencies])] where
            ins is the name of the instrument to create a price in currency curr
            and assigning fx as rate (i.e. price).
            drop currencies is a list of names on instruments (currencies) were
            any found price on day "day" in curr should be deleted.
            Example: descr [(('GBP','GBX',100.0),['USD'])]"""

    for ((insid, currid, fx), drop_currencies) in descr:
        try:
            ins = ael.Instrument[insid]
            curr= ael.Instrument[currid]
            fx = float(fx)

            cr = ael.Price.read(('insaddr = %d and curr = %d and day = "%s" and ptynbr = %d') \
                % (ins.insaddr, curr.insaddr, day, market.ptynbr))
            if not cr:
                cr = ael.Price.new()
            else:
                cr = cr.clone()
            cr.insaddr = ins
            cr.curr = curr
            cr.ptynbr = market
            cr.ask = fx
            cr.bid = fx
            cr.last = fx
            cr.settle =fx

            if type(day) == ael.ael_date:
                cr.day = day
            else:
                cr.day = ael.date_from_string(day)

            cr.commit()
            log(1, '\nSaved daily crossrate %s:%s 1:%.2lf' % (ins.insid, curr.insid, float(fx)))

            for insid in drop_currencies:
                ins = ael.Instrument[insid]
                cr = ael.Price.read(('insaddr = %d and curr = %d and day = "%s" and ptynbr = %d') \
                    % (ins.insaddr, curr.insaddr, day, market.ptynbr))
                if cr:
                    log(1, '\nDropped crossrate %s:%s' % (ins.insid, curr.insid))
                    cr.delete()

        except:
            detail = get_exception()
            msg="Failed to set %s:%s crossrate." % (insid, currid)
            log(0, msg)
            raise RuntimeError, detail



"""----------------------------------------------------------------------------
FUNCTION
    Miscellaneous functions.

DESCRIPTION
    In this section help functions are stored.
----------------------------------------------------------------------------"""
def mtm_markets():
    """Create list with MtM Market names."""
    mtm_list = []
    selection = ael.Party.select('type = "%s"' % 'MtM Market')
    for instance in selection:
        mtm_list.append(instance.ptyid)
    return mtm_list


def is_ins_expired(ins, aDate):
    """ Predicate to check if an instrument is expired.
    NOTE: An instrument is not treated as expired in MTM until after the used
    MtM day because we need to store an mtm price on expiration for futures"""
    # 1st check date format!
    if type( aDate ) == ael.ael_date:
        cut_off_date = aDate
    else:
        cut_off_date = ael.date( aDate )
    a_day=24*60*60
    if ins.exp_time > a_day and ins.exp_time < 2 * a_day:
        return ins.exp_day.add_days(-1) < cut_off_date
    else:
        return ins.exp_day < cut_off_date


def zero(a,b=0.0,prec=0.001):
    """ zero: checks if a == b or if a is zero or near by that value """
    if abs(a-b) < prec: return 1
    return 0

def cmp_prices(a, b):
    """ Note: sorts in reverse order"""
    global PreferredMarkets
    o2=o1=0
    if a.ptynbr:
        o1=PreferredMarkets.get(a.ptynbr.ptyid, 0)
    if b.ptynbr:
        o2=PreferredMarkets.get(b.ptynbr.ptyid, 0)
    if o2 == o1:
        if b.time_last and a.time_last:
            return b.time_last-a.time_last
        else:
            return b.updat_time-a.updat_time
    return o2-o1

def choose_value(p1,bs_flag=None):
    if bs_flag == 1: return p1.bid
    elif bs_flag == -1: return p1.ask
    if not zero(p1.settle): return p1.settle
    if not zero(p1.last): return p1.last
    if not zero(p1.bid) and zero(p1.ask): return (p1.bid+p1.ask)/2
    return 0.0

logged_missing_fx={}
def get_fx(c1, c2, d1):
    """ Returns the fx rate between currency c1,c2 at date d1"""
    global logged_missing_fx
    if c1 == c2:
        return 1.0
    fx=c1.used_price(d1, c2.insid)
    if not zero(fx): return fx
    fx=c2.used_price(d1, c1.insid)
    if not zero(fx): return (1/fx)
    key=(c1, c2, str(d1))
    if not logged_missing_fx.has_key(key):
        logged_missing_fx[key]=None
        log(1, "\n ERROR: Not able to determent FX between %s and %s at %s" % (c1.insid, c2.insid, str(d1)))
    return 0.0

def get_hist_price(ins, d1):
    """ Dirty operation picking historical prices using dbsql """
    s="select prinbr from price_hst where insaddr=%d and day='%s'" % (ins.insaddr, str(d1))
    prices=[]
    mask=1<<30
    for row in ael.dbsql(s)[0]:
        addr = int(row[0])
        addr=((addr)&(~mask))|mask
        prices.append(ael.Price[addr])
    return prices



bs_flag_map={1 : 'Bid', -1 : 'Ask', 0 : ''} # Mapping to use when used_price is called.
def mtm_price_suggest_default(ins,d1,currid,incl=1,umtm=1,bs_flag=0,check_hist=1):
    """ Default way of generating an mtm_price """
    global bs_flag_map
    log(3, 'Calling %s.mtm_price_suggest(%s,%s,%d,%d,%d)'  % (ins.insid, d1, currid, incl, umtm, bs_flag))
    p1 = ins.mtm_price_suggest(d1, currid, incl, umtm, bs_flag)
    if 0 and zero(p1) and ins.mtm_from_feed:
        # try using used_price or historical prices
        p1 = ins.used_price(d1, curr, bs_flag_map[bs_flag])
        if zero(p1) and d1.days_between(ael.date_today()) > 1 and check_hist:
            # fallback
            log(2, '\n No prices found for %s at %s. Checks historical prices' % (ins.insid, d1))
            prices=get_hist_price(ins, d1)
            if prices:
                prices.sort(lambda x, y: x.updat_time-y.updat_time)
                prices.reverse()
                p1=choose_price(prices, ins, d1, ael.Instrument[currid], bs_flag)

    try:
        if p1 > LARGE_NUMBER:
            p1 = 0
    except:
        p1 = 0
    return p1


def choose_price(prices, ins, d1, curr, bs_flag):
    """ Chooses a price by evaluating them in order. Sorting is done by caller """
    price = 0.0
    for p1 in prices:
        price=choose_value(p1, bs_flag)
        if not zero(price):
            if p1.curr != ins.curr:
                fx=get_fx(p1.curr, ins.curr, d1)
                if fx == 0.0:
                    log(0, "\n ERROR: Unable to calculate a suggested mtm price for %s because of missing FX" % ins.insid)
                price=price*get_fx(p1.curr, ins.curr, d1)
            break
    return price

valid_und_prices={} # Dict whith checked stock prices
 
def mtm_price_suggest_preferred(ins,d1,currid,incl=1,umtm=1,bs_flag=0):
    """ returns the suggested price in instrument currency (i.e. curr) or exchanged
         and filtered in passed curr.
         ins : ael entity of type instrument
         d1 : an ael date
         curr : returning currency
         incl : include prices in any currency
         umtm : underlying mtm flag !!!
         bs_flag : bid/ask flag."""
    global ExcludePreferredInsTypes, valid_und_prices
    price=0.0
    prices=[]
    all_prices=[]
    curr = ael.Instrument[currid]
    if ins.mtm_from_feed and not ins.instype in ExcludePreferredInsTypes:
        for p in ins.prices():
            if p.day == d1:
                all_prices.append(p)
                if 1 or (incl or p.curr == curr): # Don't filter on currency
                    prices.append(p)
        if not all_prices:
            if ins.instype == 'Stock': 
                return 0.0
            if ins.und_insaddr:
	        if not valid_und_prices.has_key(ins.und_insaddr):
		    if ins.und_insaddr.mtm_from_feed and ins.und_insaddr.instype == 'Stock' and ins.instype in ['Option', 'Warrant']:
                        has_ok=0
		        for p2 in ins.und_insaddr.prices():
			    if p2.day == d1:
                                has_ok=1
                                break
                    else:
    	                has_ok=1
                    valid_und_prices[ins.und_insaddr]=has_ok
                if not valid_und_prices.get(ins.und_insaddr):
                    return 0.0            
            if bs_flag == 0:
                price=ins.theor_price(currid, 2)
            elif bs_flag == 1: 
               price=ins.theor_price_bid(currid, 2)            
            else:
               price=ins.theor_price_ask(currid, 2)

        elif not prices:
            prices=all_prices
        if prices:
            prices.sort(cmp_prices)
            price=choose_price(prices, ins, d1, curr, bs_flag)
        # print "got price from mtm_price_suggest_preferred", ins.insid,ins.instype,price,currid
    else:
        price = mtm_price_suggest_default(ins, d1, currid, incl, umtm, bs_flag, 0) # FK,CORR 
        # print "got price from mtm_price_suggest_default", ins.insid,ins.instype,price,currid

    return price


#--------------------
# Here the suggest_price functions is defined diffrently depending on setting
#--------------------
if PreferredMarkets:
    def suggest_price(ins,d1,currid,incl=1,umtm=1,bs_flag=0):
        return mtm_price_suggest_preferred(ins, d1, currid, incl, umtm, bs_flag)
else:
    def suggest_price(ins,d1,currid,incl=1,umtm=1,bs_flag=0):
        return mtm_price_suggest_default(ins, d1, currid, incl, umtm, bs_flag)
