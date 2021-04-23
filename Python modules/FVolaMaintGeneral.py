""" MarkToMarket:1.1.10.hotfix1 """

"""----------------------------------------------------------------------------
2001-07-24

MODULE
    FVolaMaintGeneral - Module including functions regarding maintenance of
    	    	        volatility surfaces.

    (c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module stores those functions regarding maintenance of volatility
    surfaces.

----------------------------------------------------------------------------"""
print 'Inside FVolaMaintGeneral.'
try:
    import ael
except ImportError:
    print 'The module ael was not found.'
    print

"""----------------------------------------------------------------------------
FUNCTION
    find_alias_ins() - Function which retrieves all instruments with a 
    	    	       certain Alias Type.

DESCRIPTION
    The function selects all instruments which have a certain Alias Type set in
    the Alias application.
    
ARGUMENTS
    aliastypes	String  A list of all Alias Types
    
RETURNS
    l	    List of instruments
----------------------------------------------------------------------------"""

def find_alias_ins(aliastypes):
    l = {}
    
    for at in aliastypes:
    	sl = ael.InstrumentAlias.select("type.alias_type_name = %s" % at)
    	for s in sl:
    	    i = ael.Instrument.read("insaddr = '%s'" %s.insaddr.insaddr)
    	    if i.instype == 'Option':
	    	und = i.und_insaddr
    	    	if l.has_key(und):
    	    	    l[und].append(i)
    	    	else:
    	    	    l[und] = [i]
    return l

"""----------------------------------------------------------------------------
FUNCTION
    find_opt_ins() - Function which retrieves all options.

DESCRIPTION
    The function selects all options.
 
RETURNS
    l	    List of instruments
----------------------------------------------------------------------------"""

def find_opt_ins():
    l = {}
    
    ins = ael.Instrument.select("instype = 'Option'")
    for i in ins:
	und = i.und_insaddr
    	if l.has_key(und):
    	    l[und].append(i)
    	else:
    	    l[und] = [i]
    return l  

"""----------------------------------------------------------------------------
FUNCTION
    volname() - Function which returns the first part of the volatility-name.

DESCRIPTION
    The function returns the instruments insid.
    
ARGUMENTS
    ins	  Instrument An instrument.
     
----------------------------------------------------------------------------"""

def volname(ins):
    if ins.insid:
        return ins.insid

"""----------------------------------------------------------------------------
FUNCTION
    update_volsurface() - Function which creates and updates volatility-
    	    	    	  surfaces.

DESCRIPTION
    The function calls the functions create_vol_surface(), 
    and update_vol_surface().
    
ARGUMENTS
    volsuffix	String	A suffix that is added to an instrument to give the
    	    	    	give the created volatility surface its name
    aliastypes  String  A list of all Alias Types
    
----------------------------------------------------------------------------"""

def update_volsurface(volsuffix, aliastypes):
    for vs in volsuffix:
    	l = find_alias_ins(aliastypes)
    	#l = find_opt_ins()
    	for (ins, olist) in l.items():
    
    	    c = 0
	    p = 0
	    call_list = []
	    put_list = []
	
	    for opt in olist:
	    	if opt.call_option == 1:  # Add the call option to the call_list
	    	    call_list.append(opt)
		    c = c + 1
	    	else:   	    	    # Add the put option to the put_list
	    	    put_list.append(opt)
		    p = p + 1
	
    	    surf = None
	    for v in ael.Volatility.select():
    	    	if v.vol_name == volname(ins) + vs:
	    	    surf = v.vol_name
		
	    # CREATE VOLATILITY SURFACE
	    if surf == None:
	    	surf = create_vol_surface(ins, vs)
    	
	    # UPDATE THE VOLATILITY SURFACE WITH THE RIGHT INSTRUMENTS
	    volat = ael.Volatility.read("vol_name= '%s'" % surf)
	
	    if surf == volname(ins) + vs:
	    	update_vol_surface(volat, call_list)
		update_vol_surface(volat, put_list)
	    
"""----------------------------------------------------------------------------
FUNCTION
    create_vol_surface() - Function which creates volatility-surfaces.

DESCRIPTION
    The function creates volatility surfaces.
    
ARGUMENTS
    ins	    	Instrument  An instrument
    volsuffix	String	    A suffix that is added to the instrument to give 
    	    	    	    the created volatility surface its name
    
RETURNS
    vol_name	The new volatility surface
----------------------------------------------------------------------------"""

def create_vol_surface(ins, volsuffix):
    
    newvs = ael.Volatility.new()
    newvs.curr = ins.curr
    newvs.framework = 'Black & Scholes'
    newvs.ref_insaddr = ins
    newvs.strike_type = 'Absolute'
    newvs.use_und_market_price = 1
    newvs.vol_type = 'Benchmark Call/Put'
    newvs.vol_value_type = 'Absolute'
    newvs.abs_und_maturity = 1
    if (ins.instype == 'Future/Forward' and ins.und_instype == 'Bond'):
    	newvs.bond_vol_type = 'Yield Spot'
    else:
    	newvs.bond_vol_type = 'Price'
    
    newvs.vol_name = volname(ins) + volsuffix
    
    try:
    	newvs.commit()
    	print newvs.vol_name, 'Created'
    except RuntimeError:
    	print 'VolaSurf exists'
    
    return newvs.vol_name

"""----------------------------------------------------------------------------
FUNCTION
    update_vol_surface() - Function which updates a volatility surface.

DESCRIPTION
    The function updates a volatility surface. All expired options will be 
    deleted from the volatility surface.
    
ARGUMENTS
    surf    	String	    A volatility surface to which an instrument is 
    	    	    	    mapped
    inslist	String	    A list of instruments that could be added to the
    	    	    	    volatility surface

----------------------------------------------------------------------------"""

def update_vol_surface(surf, inslist):
    #print "Update volatility surface %s" % surf.vol_name
    vc = surf.clone()
    vol_points = vc.points()		
    for p in vol_points:
    	if p.insaddr.generic != 1 and p.insaddr.exp_day < ael.date_today(): 
	    #Delete expired options
	    print "Delete volpoint %s, %d in surface %s" % (p.insaddr.insid, 
	    	    	    	    	            p.seqnbr, surf.vol_name)
	    p.delete()
	    ael.poll()
    
    for ins in inslist:
    	if ins.generic != 1 and ins.exp_day > ael.date_today():
	    found = 0
	    for p in vol_points:
	    	if p.insaddr.insid == ins.insid:
    	    	    # Update volatility point. The option is in the surface.
	    	    print "Update volpoint %s, %d in surface %s" % (
		    	    	    p.insaddr.insid, p.seqnbr, surf.vol_name)
	    	    p.volatility = (ins.implied_volat(2, 'Close')/100)
		    found = 1
		
    	    if found == 0:	
    	    	print "Option %s not in surface %s. Add it" % (ins.insid,
                                                               surf.vol_name) 
    	    	vp = ael.VolPoint.new(vc)
    	    	vp.insaddr = ins
    	    	vp.volatility = (ins.implied_volat(2, 'Close')/100)
    vc.commit()
