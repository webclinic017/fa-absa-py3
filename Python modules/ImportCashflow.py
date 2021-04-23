"""-----------------------------------------------------------------------------
MODULE	    	ImportCashFlow 

(c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

Version: 1.0

DESCRIPTION
This module is for demo purposes. It takes a text file as indata and from this
file it imports cash flows to instruments in ATLAS.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael
import string

def read_data(source_name):
    src=open(source_name, 'r')
    line=src.readline()
    rows=[]
    while line != '':
	rows.append(string.split(line, '\t'))
	line=src.readline()
    src.close()
    return rows

def get_index(rows, name):
    i=0
    for r in rows[0]:
	if name == r:
	    return i
	i=i+1
    
def importcf(ins,source_name,*rest):
    try:
	rows=read_data(source_name)
	print rows
	i_copy=ins.clone()
	for l in i_copy.legs():
	    for c in l.cash_flows():
		for i in rows:
		    legnbr=get_index(rows, 'Leg Nbr')
		    cfnbr=get_index(rows, 'CF Nbr')
		    if str(l.legnbr) == i[legnbr]:
			if str(c.cfwnbr) == i[cfnbr]:
			    try:
			    	c.start_day=ael.date(i[get_index(rows, 'Start Day')])
			    except:
			    	nr=1
				print 'No start day'
				return 0.0
			    try:
			    	c.end_day=ael.date(i[get_index(rows, 'End Day')])
			    except:
			    	nr=1
				print 'No end day'
				return 0.0
			    try:
			    	c.pay_day=ael.date(i[get_index(rows, 'Pay Day')])
			    except:
			    	nr=1
				print 'No pay day'
				return 0.0
			    try:
			    	if i[get_index(rows, 'Strike')] == "":
				    c.strike_rate = 0.0
				else:
				    c.strike_rate=float(i[get_index(rows, 'Strike')])
			    except:
			    	nr=1
				print 'No strike'
				return 0.0
			    try:
			    	if i[get_index(rows, 'Rate')] == "":
				    c.rate = 0.0
				else:
				    c.rate=float(i[get_index(rows, 'Rate')])
			    except:
			    	nr=1
				print 'No rate'
				return 0.0
			    try:
			    	if i[get_index(rows, 'Off')] == "":
				    c.float_rate_offset = 0
				else:
				    c.float_rate_offset=int(i[get_index(rows, 'Off')])
			    except:
			    	nr=1
			    	print 'No off'
				return 0.0
			    try:
			    	if i[get_index(rows, 'Fctr')] == "":
				    c.float_rate_factor = 0.0
				else:
				    c.float_rate_factor=float(i[get_index(rows, 'Fctr')])
			    except:
			    	nr=1
				print 'No fctr'
				return 0.0
			    try:
			    	if i[get_index(rows, 'Sprd')] == "":
				    c.spread = 0.0
				else:
				    c.spread=float(i[get_index(rows, 'Sprd')])
			    except:
			    	nr=1
				print 'No spread'
				return 0.0
			    try:
			    	nom_tmp=string.split(i[get_index(rows, 'Nominal')], '.')
				nom=''
				for n in nom_tmp:
				    nom=nom+n
				nom_tmp=string.split(nom, ',')
				nom=''
				for n in nom_tmp:
				    nom=nom+n
				nom=float(nom)/100    
			    	c.nominal_factor=float(nom)/i_copy.contr_size
				print float(nom)/i_copy.contr_size
			    except:
			    	nr=1
				print 'No nominal'
				return 0.0
			    try:
			    	l.curr=ael.Instrument[i[get_index(rows, 'Curr')]]
			    except:
			    	nr=1
				print 'No curr'
				return 0.0
			    c.commit()
	i_copy.commit()
	instr = i_copy
	if instr.instype == 'Swap':
	    fix_resets(instr)
	return 1
    except:
    	return 0



def fix_resets(i):

    legs = i.legs()
    for l in legs:
    	if l.type == 'Float':
    	    cfs = l.cash_flows()
    	    for cf in cfs:
	    	cfr = cf.resets()

    	    	x = cfr[0]
    	    	xc = x.clone()

    	    	xc.day = cf.start_day
    	    	xc.start_day = cf.start_day
    	    	xc.end_day = cf.end_day
		xc.commit()
