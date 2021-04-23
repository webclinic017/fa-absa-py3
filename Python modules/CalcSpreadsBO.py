"""-----------------------------------------------------------------------------
MODULE	    	CalcSpreadsBO 

(c) Copyright 2001 by Front Capital Systems AB. All rights reserved.

Version: 1.1

DESCRIPTION
This module is for demo purposes. It takes a text file as indata and from this
file it creates an AMBA message and makes an uppload of this message via the
AMBA to the ISSUER yield curve. (The text file has to have a specific structure.)
To run this script use the sql query that is called DefaultProbToSpread
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael
import string
import commands
import math
import os
from os import environ

"""-----------------------------------------------------------------------------
FUNCTION    read_data
DESCRIPTION
    This function reads the infile and returns all the relevant data from this
    file.
ARGUMENTS
    source_name=name of infile
RETURNS
    years=a vector containing all the years that it exists data for.
    default=a dictionary containing all the defualt rates for every
    	    issuer and every year
    rec=a dictonary containing all the recoverys for every issuer.
    issuers=a vector containing all issuers.
-----------------------------------------------------------------------------"""
def read_data(source_name):
    """os.system(str('net use z: /d'))"""
    os.system(str('net use z: \\\\atlasprd\\local'))
    src=open(source_name, 'rb')
    line=src.readline()
    
    tmp=string.split(line, '\t')
    years=[]
    for i in range(5, len(tmp)-1):
    	 year_tmp=string.split(tmp[i], '-')
	 years.append(int(year_tmp[0]))
    row=[]
    while line != '':
	try:
	    t=int(line[0])
	    row.append(string.split(line, '\t'))
	except:
	    t=0
    	line=src.readline()
    default={}
    rec={}
    issuers=[]
    for r in row:
    	tmp={}
	for y in years:
	    print y
	    tmp[y]=float(r[4+y])
	    print tmp[y]
    	default[r[1]]=tmp
	rec_tmp=(string.split(r[2], '%'))
    	rec[r[1]]=int(rec_tmp[0])
	issuers.append(r[1])
    src.close()
    return years, default, rec, issuers

"""-----------------------------------------------------------------------------
FUNCTION    credit_spreads
DESCRIPTION
    This function saves asset swap spreads to the database.
ARGUMENTS
    source_name=the name of the input file
RETURNS
    credits=a dictionary containing the intermedian step in the spread calculation
-----------------------------------------------------------------------------"""
def credit_spread(source_name):
    years, default, rec, issuers=read_data(source_name)
    RecRate=0.0
    Prob=0.0
    credits={}
    for i in issuers:
	tmp={}
	tmp2={}
	for y in years:
	    Prob=float(default[i][y])
	    RecRate=float(rec[i])
	    #Changed by Jonathon Tyler 27/06/01
	    #Updated for BackOffice by Parin and Anton 04/02/03
	    tmp[y]=1-(Prob/100*(1-RecRate/100))
	    tmp2[y]=1-tmp[y]
	    print tmp2[y]
	credits[i]=tmp
    return credits
    
"""-----------------------------------------------------------------------------
FUNCTION    write_amba
DESCRIPTION
    This function writes an AMBA message in a file and starts the AMBA to send
    the message.
ARGUMENTS
    spread=
    rfyc=the name of the risk free yield curve
    server=the server name
    user=the user name for login in to AMBA
    password=the password for login in to AMBA
RETURNS
    0 if succeded -1 otherwise
     Make sure the z: share is mapped to \\atlasprd\local
-----------------------------------------------------------------------------"""
def write_amba(spread, rfyc, server, user, password, dates):
    list=['CDIssuerCurve']
    home=os.getcwd()
    #print environ.keys
    os.chdir('z:')
    file='outfilebo.txt'
    tar=open(file, 'w')
    for l in list:
	tar.write('[MESSAGE]'+'\n')
    	tar.write('   TYPE=UPDATE_YIELDCURVE'+'\n')
    	tar.write('   VERSION=1.0'+'\n')
    	tar.write('   TIME=2001-02-27 18:00:00'+'\n')
    	tar.write('   SOURCE=INT-UPLOAD'+'\n')
	tar.write('   [YIELDCURVE]'+'\n')
	tar.write('      YIELD_CURVE_NAME='+l+'\n')
	tar.write('      YIELD_CURVE_TYPE=IR_ATTRIBUTE_SPREAD'+'\n')
	for d in dates:
	    tar.write('      [YIELDCURVEPOINT]'+'\n')
	    tar.write('         DATE_PERIOD='+str(d)+'y'+'\n')
	    for c in spread.keys():
		for cd in spread[c].keys():
		    d_new=str(cd)
		    if d_new == (str(d)+'y'):
			tar.write('         [ATTRIBUTESPREAD]'+'\n')
		    	tar.write('            ATTRIBUTE='+str(c)+'\n')
			tar.write('            SPREAD='+str(spread[c][cd])+'\n')
	    	    	tar.write('         [/ATTRIBUTESPREAD]'+'\n')
	    tar.write('      [/YIELDCURVEPOINT]'+'\n')
    	tar.write('   [/YIELDCURVE]'+'\n')
    	tar.write('[/MESSAGE]'+'\n')
    tar.close()
    amba='z:\\amba.exe'
    com_line=amba+' -server '+server+' -message_file '+file+' -user '+user+' -password '+password
    os.system(str(com_line))
    return 0

"""-----------------------------------------------------------------------------
FUNCTION    mod_yield_curve
DESCRIPTION
    This is the main function that is called from the sql. This function starts
    the hole conversion process.
ARGUMENTS
    o=an AEL entity, is never used
    rfyc=the name of the risk free yield curve
    server=the name of the server containing the ADS
    user=the user name
    password=the password
RETURNS
    1 if succeded 0 otherwise
-----------------------------------------------------------------------------"""
def mod_yield_curve(o,rfyc,infile,server,user,password,*rest):
    par=ael.YieldCurve.select()
    dates=[1, 2, 3, 4, 5]
    risk_free={}
    for p in par:
    	if p.yield_curve_name == rfyc:
	    for d in dates:
		end_day=ael.date_valueday().add_years(d)
		start_day=end_day.add_years(-1)
		risk_free[d]=p.yc_rate(start_day,\
    	    	    	end_day, 'Annual Comp', 'Act/365', 'discount')
    credit=credit_spread(infile)
    spread={}    
    for c in credit.keys():
    	tmp_forward={}
	risk_free_forward={}
    	for y in credit[c].keys():
	    risk_free_forward[str(y)+'y']=(1/risk_free[y])-1
	    tmp_forward[str(y)+'y']=1/(risk_free[y]*credit[c][y])-1-risk_free_forward[str(y)+'y']
	tmp_spot={}	
	for z in dates:
	    if z == 1:
	    	tmp_spot['1y']=tmp_forward['1y']
	    else:
	    	year=str(z)+'y'
		last_year=str(z-1)+'y'
	    	z=float(z)
	    	tmp_spot[year]=(math.pow(tmp_forward[year]+1, 1/z)*math.pow(tmp_spot[last_year]+1, (z-1)/z)-1)
	spread[c]=tmp_spot
    a=write_amba(spread, rfyc, server, user, password, dates)
    if a == 0:
    	return 1
    else:
    	return 0
