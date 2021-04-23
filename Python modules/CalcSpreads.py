"""-----------------------------------------------------------------------------
MODULE	    	CalcSpreads 

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
FUNCTION    real_round
DESCRIPTION
    This function converts a number to a real number
    file.
ARGUMENTS
    number = number to be converted
    dec = number of deciamls required
RETURNS
    number with requested decimals
-----------------------------------------------------------------------------"""
def real_round(number, dec):
    r = round(number, dec)
    if dec == 0:
        return str(int(r))
    else:
        str_dec = str(r - math.floor(r))
        zeros = dec + 2 - len(str_dec)
        return str(r) + zeros * '0' 

"""-----------------------------------------------------------------------------
FUNCTION    file_upload
DESCRIPTION
    This function reads the infile in csv format and returns all the relevant 
    data from this file.
ARGUMENTS
    source_name=name of infile
RETURNS
    years=a vector containing all the years that it exists data for.
    default=a dictionary containing all the defualt rates for every
    	    issuer and every year
    rec=a dictonary containing all the recoverys for every issuer.
    issuers=a vector containing all issuers.
ADDED BY
    Aaeda Salejee - Changed upload file format to csv.
-----------------------------------------------------------------------------"""   
def file_upload(filename):
    
    try:
        infile = open(filename, 'rb')
    except:
        return 'Error opening file'
        
    count = 0
    list = []
    line = infile.readline()
    
    years = []
    l = string.split(line, ',')
    for i in range(5, len(l)-1):
        y = string.split(l[i], '-')
        years.append(int(y[0]))
    #print years

    row = []
    line = infile.readline()
    while line != '':
        l = string.split(line, ',')
        row.append(l)
        line = infile.readline()
    #print row
    
    data_list = {}
    rec = {}
    issuers = []
    for r in row:
        iss = r[1]
        vals = {}
        for y in years:
            v = r[4+y].rstrip()
            v = v.lstrip()
            vals[y] = real_round(float(v), 2)            
        data_list[iss] = vals
        r_temp = string.split(r[2], '%')
        rec[iss] = float(r_temp[0])
        issuers.append(iss)
        
    infile.close()
    return years, data_list, rec, issuers
    


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
    #os.system(str('net use z: \\\\atlasprd\\local'))
           
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
	    #print y
	    tmp[y]=float(r[4+y])
	    #print tmp[y]
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
    years, default, rec, issuers=file_upload(source_name)
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
	    tmp[y]=1-(Prob/100*(1-RecRate/100))
	    tmp2[y]=1-tmp[y]
	    #print tmp2[y]
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
    list=['CDIssuerCurveFO', 'CDIssuerCurve']
    home=os.getcwd()
    os.chdir('z:')
    file='outfile.txt'
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
	
	#Added 2003-11-13 Russel Webber
	#Need 0d point with value of 0 to allow valid interpolation
	#between 0d and 1Y
	#Since CD curves are attribute spreads need to have a spread 
	#equal to -1 * the value of the underlying curve at 0d.
    	#Amended 2003-11-17 to make spread at 0d zero.
	
	
    	#Start changes - RW - 2003-11-13

    	#zero_value = ael.YieldCurve[l].underlying_yield_curve_seqnbr.yc_rate(ael.date_today(),\
    	#    	    	ael.date_today(),'Annual Comp','Act/365','Spot Rate')
	#zero_value = -1 * zero_value

	zero_value = 0.0

        #Added 2006-12-01 Aaeda Salejee, Shaun Steyn
        #Changed layout of amba message for new data model (3.7.1)

        # Zero d bucket
    	tar.write('      [YIELDCURVEPOINT]'+'\n')
	tar.write('         DATE_PERIOD=0d'+'\n')
	tar.write('      [/YIELDCURVEPOINT]'+'\n')
       
	
	for d in dates:
	    tar.write('      [YIELDCURVEPOINT]'+'\n')
	    tar.write('         DATE_PERIOD='+str(d)+'y'+'\n')
	    tar.write('      [/YIELDCURVEPOINT]'+'\n')
	    
        for c in spread.keys():
            tar.write('      [YCATTRIBUTE]'+'\n')
            tar.write('         ISSUER_PTYNBR.PTYID='+str(c)+'\n')
            
            #Zero d spreads
            tar.write('         [YCSPREAD]'+'\n')
            tar.write('            POINT_SEQNBR.DATE_PERIOD=0d'+'\n')
            tar.write('            SPREAD=' + str(zero_value)+'\n')
            tar.write('         [/YCSPREAD]'+'\n') 
    
            for cd in spread[c].keys():
                for d in dates:
                    d_new=str(cd)
		    if d_new == (str(d)+'y'):
                        tar.write('         [YCSPREAD]'+'\n')
                        tar.write('            POINT_SEQNBR.DATE_PERIOD='+str(d)+'y'+'\n')
			tar.write('            SPREAD='+str(spread[c][cd])+'\n')
	    	    	tar.write('         [/YCSPREAD]'+'\n')
	    	 
            tar.write('      [/YCATTRIBUTE]'+'\n')
	    
    	tar.write('   [/YIELDCURVE]'+'\n')
    	tar.write('[/MESSAGE]'+'\n')
    tar.close()
    amba='z:\\amba.exe'
    com_line=amba+' -server '+server+' -message_file '+file+' -user '+user+' -password '+password
    os.system(str(com_line))
    
    return 0





#Aaeda (2006-12-01)  backup before change of amba message for new data model
def write_amba_backup(spread, rfyc, server, user, password, dates):
    list=['CDIssuerCurveFO', 'CDIssuerCurve']
    home=os.getcwd()
    os.chdir('z:')
    file='outfile.txt'
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
	
	#Added 2003-11-13 Russel Webber
	#Need 0d point with value of 0 to allow valid interpolation
	#between 0d and 1Y
	#Since CD curves are attribute spreads need to have a spread 
	#equal to -1 * the value of the underlying curve at 0d.
    	#Amended 2003-11-17 to make spread at 0d zero.
	
	
    	#Start changes - RW - 2003-11-13

    	#zero_value = ael.YieldCurve[l].underlying_yield_curve_seqnbr.yc_rate(ael.date_today(),\
    	#    	    	ael.date_today(),'Annual Comp','Act/365','Spot Rate')
	#zero_value = -1 * zero_value
	
	zero_value = 0.0
		
    	tar.write('      [YIELDCURVEPOINT]'+'\n')
	tar.write('         DATE_PERIOD=0d'+'\n')

	for c in spread.keys():
    	    tar.write('         [ATTRIBUTESPREAD]'+'\n')
	    tar.write('            ATTRIBUTE='+str(c)+'\n')
	    tar.write('            SPREAD=' + str(zero_value)+'\n')
	    tar.write('         [/ATTRIBUTESPREAD]'+'\n')
	
	tar.write('      [/YIELDCURVEPOINT]'+'\n')
	
	#End changes - RW - 2003-11-13
	
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
