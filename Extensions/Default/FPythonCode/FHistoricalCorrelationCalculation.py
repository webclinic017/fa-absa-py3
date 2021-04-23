""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/correlation/FHistoricalCorrelationCalculation.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FHistCorrCalc - Calculate and store historical correlations
    
DESCRIPTION
    Calculate historical correlations using the historical prices stored in
    FRONT ARENA. Save the correlations in a correlation parameter.

NOTE 1
    The script does only handle instruments.

NOTE 2
    The time bucket should be 0d if the SEQ package should work properly.


## !! SPECIFY THE FOLLOWING VARIABLES!! ##

Base Currency:              The option strike currency. The correlation pairs are
                            defined by the two currencies ins_curr and base currency.
Correlation Time Bucket:    The time bucket of the matrix

Correlation Table Name:     The name of the correlation matrix.

Price Hist. StartDate:      The start date. 1970-01-01 is default.

Price Hist. EndDate:        The end date. Today is default.

Days Between Prices:        Number of days between each observation. 5 gives e.g. 
                            weekly hist corr.

Page:                       Page specifying the instruments for which correlations are 
                            calculated.

Intervals:                  The target number of observations for the calculations. 

Prices stored in Market:    The market from which historical prices is used.

------------------------------------------------------------------------------"""
import ael
from math import *

#-----------------------------------------------------
#
# Calculate historical correlation
#
#-----------------------------------------------------
def calc(ins1, ins2, daysbetween, intervals, priceMatrix):
    if ins1 == ins2: return 1.0
    if daysbetween == '': d = 1
    else: d = int(daysbetween)

    prvect = comb_prices(ins1, ins2, daysbetween, intervals, priceMatrix)

    i = 0
    n = 0
    xsum = 0.0; xsum2 = 0.0
    ysum = 0.0; ysum2 = 0.0
    xysum = 0.0
    xvol = 0.0;yvol = 0.0
    b = 0.0; c = 0.0

    l = len(prvect)

    if l>3*d:
        for p in prvect:
            if i < l-d:
                oldx = prvect[i][1]
                oldy = prvect[i][2]
                
                xret = (prvect[i+d][1] - oldx)/oldx
                yret = (prvect[i+d][2] - oldy)/oldy

                # Logarithmic return can be used as alternative
                # xret = log(prvect[i+d][1] / oldx)               
                # yret = log(prvect[i+d][2] / oldy)
                
                xsum = xsum + xret
                ysum = ysum + yret          
                xsum2 = xsum2 + xret*xret
                ysum2 = ysum2 + yret*yret
                xysum = xysum + xret*yret
                # print i,prvect[i+d][0], prvect[i+d][1], prvect[i+d][2],xret,yret,(prvect[i+d][1] - oldx)/oldx,(prvect[i+1][2] - oldy)/oldy #,xsum,ysum,xsum2,xysum  
                i = i + d
        
        n = i/d
        years = prvect[0][0].years_between(prvect[l-1][0])
        xvol = sqrt((xsum2 - xsum*xsum/n) / (n-1)) * sqrt(n/years)
        yvol = sqrt((ysum2 - ysum*ysum/n) / (n-1)) * sqrt(n/years)
        b = (xysum - xsum*ysum/n) / (ysum2 - ysum*ysum/n)
        c = b*yvol/xvol
        n = n+1
        print("\t* Corr. for ", ins1.insid, " / ", ins2.insid, " = ", c, " (", n, " actual intervals )") 
    else: 
        print("\n\t## !! NO VALUE !! ##")
        print("\t- There are only ", l, " intervals available for the instruments ", ins1.insid, " and ", ins2.insid) 
        print("\t- To calculate the correlations there have to be at least ", 3*d+1, "intervals available.\n")
    return c
                
#-----------------------------------------------------
#
# Read historcal prices from the database and create a price vector.
# 
#-----------------------------------------------------
def init_prices(ins, d1, d2, pty):
    vect = []

    if d2 == '': da2 = ael.date_today()
    else: da2 =  ael.date(d2)
    
    if d1 == '': da1 = ael.date('1970-01-01')
    else: da1 =  ael.date(d1)
    
    pr = ins.historical_prices(da1)
    
    for p in pr:
        prityp = []
        if (p.ptynbr == pty and da2.days_between(p.day) <= 0): 
            # Use the last price if it is larger than zero.
            if p.settle > 0: 
                vect.append((p.day, p.settle))
            else:
                # If there is no last price, fetch bid and ask prices
                if p.bid > 0: prityp.append(p.bid)
                if p.ask > 0: prityp.append(p.ask)
            
                prityp.sort()
                l = len(prityp)
                # Only one of the prices existed. Use this price
                if l == 1: vect.append((p.day, prityp[0]))
                # Both bid and ask exist Calculate the spread average
                if l == 2: vect.append((p.day, (prityp[0]+prityp[1])/2))
    vect.sort() 
    return vect     
    
#-----------------------------------------------------
#
# Use dates where data is available for both instruments. 
# 
#-----------------------------------------------------
def comb_prices(ins1, ins2, daysbetween, intervals, priceMatrix):
    vect = []
    prvect1 = priceMatrix[ins1][:]
    prvect2 = priceMatrix[ins2][:]
    for p1 in prvect1:
        for p2 in prvect2:
            if p1[0] == p2[0]: vect.append((p1[0], p1[1], p2[1]))

    if intervals != '':
        v = int(intervals) 

        l = len(vect)
        start = l - v*int(daysbetween)

        if start > 0: del vect[0:start]
    return vect                    

#-----------------------------------------------------
#
# Save correlation in a Correlation parameter
# 
#-----------------------------------------------------
def save(ins0, ins1, corr, corrpar, corrbucket, basecurr):
    if ins0 == ins1: return 1
    
    if corr == 0.0: return 0 
    if str(ins0.instype) == 'Curr': 
        if ins0.insid == basecurr: return 0
        try:
            curr_pair0 = ael.Instrument[basecurr].currency_pair(ins0.insid)
        except Exception as msg:
            print("\t## !! NO VALUE !! ##")
            print("\tError: ", msg)
            print()
            return 0
        recaddr0 = curr_pair0.seqnbr
        rectype0 = 'CurrencyPair'
    else: 
        recaddr0 = ins0.insaddr
        rectype0 = 'Instrument'
        
    if str(ins1.instype) == 'Curr': 
        if ins1.insid == basecurr: return 0
        try:
            curr_pair1 = ael.Instrument[basecurr].currency_pair(ins1.insid)    
        except Exception as msg:
            print("\t## !! NO VALUE !! ##")
            print("\tError: ", msg)
            print()
            return 0    
        recaddr1 = curr_pair1.seqnbr
        rectype1 = 'CurrencyPair'
    else: 
        recaddr1 = ins1.insaddr
        rectype1 = 'Instrument'
    
    corrs = ael.Correlation.select('corr_matrix_seqnbr=' + str(corrpar))
    for c in corrs:
        if (c.recaddr0 == recaddr0 or c.recaddr1 == recaddr0) and\
           (c.recaddr0 == recaddr1 or c.recaddr1 == recaddr1) and\
           (c.bucket0.lower() == corrbucket.lower()) and\
           (c.bucket1.lower() == corrbucket.lower()): 
            cc = c.clone()
            cc.corr = corr
            cc.commit()
            ael.poll()
            return 1

    corr_matrix = ael.CorrelationMatrix[corrpar].clone()
    new_corr = ael.Correlation.new(corr_matrix)
    new_corr.recaddr0 = recaddr0
    new_corr.recaddr1 = recaddr1
    new_corr.rec_type0 = rectype0
    new_corr.rec_type1 = rectype1
    new_corr.bucket0 = corrbucket
    new_corr.bucket1 = corrbucket
    new_corr.corr = corr
    corr_matrix.commit()
    ael.poll()
    return 1


#-----------------------------------------------------
#
# Access functions
# 
#-----------------------------------------------------
def correlations():
    corr = []
    for c in ael.CorrelationMatrix.select(): corr.append(c.name)
    corr.sort()
    return corr

def currs():
    cur=[]
    for curr in ael.Instrument.select('instype="Curr"'): cur.append(curr.insid)
    cur.sort()
    return cur
    
def markets():
    market_vec = []
    for m in ael.Party.select('type="Market"'): market_vec.append(m.ptyid)
    for m in ael.Party.select('type="MtM Market"'): market_vec.append(m.ptyid)
    market_vec.sort()
    return market_vec 

def get_ins_of_type(instype):
    ins = []
    for i in ael.Instrument.select('instype=' + instype): 
        ins.append(i.insid)
    ins.sort()
    return ins

def get_list():
    ins = []
    str = ''
    get_children(0, ins, str)
    ins.sort()
    return ins
    
def get_children(nodnbr, ins, str):
    pages = ael.ListNode.select('father_nodnbr=%d' % nodnbr)  
    for p in pages:
        if p.terminal == 0:
            s = str + ' | ' + p.id
            get_children(p.nodnbr, ins, s)
        else:
            s = str +' | '+p.id
            ins.append(s)
            
def get_page(str):
    ins =[]
    for item in str:
        list = item.split(' | ')
        list[0] = list[0][2:]
        j = len(list)
    
        pages = ael.ListNode.select('father_nodnbr=0')
     
        while j > 0 :
            for p in pages:
                if list:
                    if p.id == list[0]:
                        
                        nodnbr = p.nodnbr                   
                        del list[0]
                        j = len(list)
                        
                        if j == 0:                          
                            instr = p.leafs()

                        pages = ael.ListNode.select('father_nodnbr=%d' % nodnbr)

        for l in instr:
            if l.insaddr.instype in ['EquityIndex', 'Curr', 'Stock']:
                ins.append(l.insaddr.insid)
    return ins        
        
                
ael_variables = [('corrname', 'Correlation Table Name', 'string', correlations(), None, 1, 0),
                 ('corrbucket', 'Correlation Time Bucket', 'string', None, '0d', 1, 0),
                 ('intervals', 'Intervals', 'int', None, '100', 1, 0),
                 ('date1', 'Price Hist. StartDate', 'string', None, '1970-01-01', 1, 0),
                 ('date2', 'Price Hist. EndDate', 'string', None, str(ael.date_today()), 1, 0),
                 ('daysbetween', 'Days Between Prices', 'int', None, '1', 1, 0),
                 ('market', 'Price stored in Market', 'string', markets(), None, 1, 0),
                 ('basecurr', 'Base Currency', 'string', currs(), None, 1, 0),
                 ('inslist', 'Page', 'string', get_list(), None, 0, 1)]
                 
#-----------------------------------------------------
# 
# Calculate the correlations
#
#-----------------------------------------------------
def ael_main(dict):
    corrname = dict["corrname"]
    corrbucket = dict["corrbucket"]
    intervals = dict["intervals"]
    date1 = dict["date1"]
    date2 = dict["date2"]
    daysbetween = dict["daysbetween"]
    market = dict["market"]
    page = dict["inslist"]
    inslist = get_page(page)
    basecurr = dict["basecurr"]
    
    #print "List of Stocks etc." , inslist
    
    if len(inslist) < 2: 
        raise TypeError('At least two instruments must be chosen (stocks, currencies or equity indexes)')
    
    corr_matrix = ael.CorrelationMatrix[corrname]
    
    if corr_matrix != None: 
        corrpar = corr_matrix.seqnbr
    else:
        new_corr = ael.CorrelationMatrix.new()
        new_corr.name = corrname
        new_corr.commit()
        corrpar = new_corr.seqnbr
        ael.poll()
    
    party = ael.Party[market]
    
    #Create a matrix with prices
    print("CALCULATE CORRELATIONS BASED ON HISTORICAL PRICES")
    print("* Create a matrix with prices.\n")
    priceMatrix = {}
    for i in range(len(inslist)):
        ins = ael.Instrument[inslist[i]]
        priceMatrix[ins] = init_prices(ins, date1, date2, party)

    # Calculate and save the correlations
    print("* Calculate and save the correlations:\n")
    for i in range(len(inslist)):
        ins1 = ael.Instrument[inslist[i]]

        for j in range(i+1):
            ins2 = ael.Instrument[inslist[j]]

            corr = calc(ins1, ins2, daysbetween, intervals, priceMatrix)
            save(ins1, ins2, corr, corrpar, corrbucket, basecurr)
    print("* The correlations have been calculated and stored in the database.\n")
    print()
    
    return "SUCCESS"            

def start_ael(p,*rest):
    return 'Called AEL'

