"""-----------------------------------------------------------------------------
MODULE	    	FBasketCDS 

(c) Copyright 2000 by Front Capital Systems AB. All rights reserved.

Version: 1.0

DESCRIPTION
    This module values basket credit default swaps, both ordinary ones and 
    digital ones changed.
ENDDESCRIPTION
-----------------------------------------------------------------------------"""
import ael
import math
import Numeric

def Theor(o, calc, ref):
    payments=[]
    if o.record_type == 'CashFlow':
    	TheorCf(o, calc, ref, payments)
	return payments
    if o.record_type == 'Leg':
    	for c in o.cash_flows():
            TheorCf(c, calc, ref, payments)
	return payments
    for j in o.legs():
    	for c in j.cash_flows():
            TheorCf(c, calc, ref, payments)
    return payments

def ReadData(c):
    issuers=[]
    inst=[]
    weights={}
    creditref=c.legnbr.credit_ref
    if creditref.instype == 'Combination':
    	for m in creditref.combination_links():
	    issuers.append(m.member_insaddr.issuer_ptynbr)
	    inst.append(m.member_insaddr)
	    weights[m.member_insaddr.issuer_ptynbr]=m.weight*m.member_insaddr.nominal_amount()
    else:
    	return 0, 0, 0, 0
    recrate={}
    for i in issuers:
    	try:
	    recrate[i]=(float(i.add_info('RecoveryRate')))
	except:
	    recrate[i]=(50.0)
    return recrate, issuers, inst, weights

def Correlation(date, issuers):
    cov=ael.Covariance['BasketCDS']
    mat={}
    for i in issuers:
        for j in issuers:
	    if i == j:
		try:
		    tmp=mat[i.ptyid]
		except:
		    tmp={}
		tmp[j.ptyid]=1.0
	    	mat[i.ptyid]=tmp
	    else:
		try:
		    tmp=mat[i.ptyid]
		except:
		    tmp={}
		tmp[j.ptyid]=cov.corr_get_correlation(i, j, date)	    	
		mat[i.ptyid]=tmp
    return mat
    
def DefProb(c, date1, date2, inst, recrate):
    ycrf=c.legnbr.insaddr.used_yield_curve(c.legnbr.curr)
    prob={}
    for i in inst:
	ycry=i.used_yield_curve(i.curr)
	discrisky=ycry.yc_rate(date1, date2, 'Continuous', 'Act/360',\
	    	    'Discount', 0)
	discriskfree=ycrf.yc_rate(date1, date2, 'Continuous', 'Act/360',\
	   	    'Discount', 0)
	prob[i]=(1.0-discrisky/discriskfree)/(1-recrate[i.issuer_ptynbr]/100.0)
 	if prob[i] < 0:
	    prob[i]=0.0
    return prob
    
def CondDefProb(defprob, recrate, corrmat, issuers):
    conddefprob={}
    cut={}
    minimum=1
    for i in defprob.keys():
    	tmpprob={}
    	for j in defprob.keys():
	    corr=corrmat[i.issuer_ptynbr.ptyid][j.issuer_ptynbr.ptyid]
	    if corr > 0:
	    	tmpprob[j.issuer_ptynbr]=(1-(1-corr)*(1-defprob[i]))*defprob[j]
	    else:
	    	tmpprob[j.issuer_ptynbr]=((1+corr)*(defprob[i]))*defprob[j]
	    if tmpprob[j.issuer_ptynbr] < minimum:
	    	minimum=tmpprob[j.issuer_ptynbr]
	cut[i.issuer_ptynbr]=tmpprob
    for i in defprob.keys():
    	tmptop=defprob[i]
	tmpbottom=0
	for j in defprob.keys():
	    tmpbottom=tmpbottom+defprob[j]
	for j in range(0, len(issuers)):
	    for k in range(j, len(issuers)):
		if (issuers[k] != issuers[j]):
		    tmpbottom=tmpbottom-cut[issuers[j]][issuers[k]]
	tmpbottom=tmpbottom+minimum
	tmp=tmptop/tmpbottom
	conddefprob[i.issuer_ptynbr]=tmp
    return conddefprob, cut

def PortfolioRec(conddefprob, recrate, weights):
    portrec=0.0
    conddef=0.0
    for i in recrate.keys():
    	weights[i]=1
  	portrec=portrec+recrate[i]/100*conddefprob[i]*weights[i]
	conddef=conddef+conddefprob[i]*weights[i]
    return portrec/conddef

def Prob(defprob, cut, issuers):
    res=0.0
    for i in defprob.keys():
    	res=res+defprob[i]
    minimum=1
    for j in range(0, len(issuers)):
	for k in range(j, len(issuers)):
	    if (issuers[k] != issuers[j]):
		tmp=cut[issuers[j]][issuers[k]]
		res=res-tmp
		if minimum > tmp:
		    minimum=tmp
    if len(issuers) > 2:
    	res=res+minimum
    return res

def TreeProb(c, recrate, issuers, inst, weights, nrofstep):
    prob=[]
    riskfree=[]
    rec=[]
    today=ael.date_valueday()
    if nrofstep <= 0:
    	nrofstep=1
    start=date=c.start_day
    end=c.end_day
    dt=int(date.days_between(end)/nrofstep)
    if dt < 1:
    	dt=1
    ycrf=c.legnbr.insaddr.used_yield_curve(c.legnbr.curr)
    while (date < end):
	date2=date.add_days(dt)
	corrmat=Correlation(date, issuers)
	if date2 < end:
	    defprob=DefProb(c, date, date2, inst, recrate)
	    conddef, cut=CondDefProb(defprob, recrate, corrmat, issuers)
	    portrecrate=PortfolioRec(conddef, recrate, weights)
	    rec.append(portrecrate)
	    riskfree.append(ycrf.yc_rate(today, date2, 'Continuous', 'Act/360',\
	    	    'Discount', 0,))
	else:
	    defprob=DefProb(c, date, end, inst, recrate)
	    conddef, cut=CondDefProb(defprob, recrate, corrmat, issuers)
	    portrecrate=PortfolioRec(conddef, recrate, weights)
	    rec.append(portrecrate)
	    riskfree.append(ycrf.yc_rate(today, end, 'Continuous', 'Act/360',\
	    	    'Discount', 0,))
    	if portrecrate >= 100:
	    prob.append(0.0)
	else:
	    prob.append(Prob(defprob, cut, issuers))
	date=date2
    return prob, riskfree, rec

def TheorCf(c, calc, ref, payments):
    if ref == None or c == ref:
    	res = 0.0
	if calc:
	    recrate, issuers, inst, weights=ReadData(c)
	    if recrate == 0 and issuers == 0 and inst == 0 and weights == 0:
	    	print 'Wrong type on credit reference'
		p=[0.0, c.pay_day, c.legnbr.curr, 'Float', c]
		payments.append(p)
		return 0
	    if c.type == 'Credit Default':
	    	payout=0.0
	    	start=date=c.start_day
    	    	end=c.end_day
    	    	nrofstep=int(start.periods_between(end, '1m'))
    	    	prob, riskfree, rec=TreeProb(c, recrate, issuers, inst, weights, nrofstep)		
		res=0.0
		for i in range(0, len(prob)):
	    	    if c.legnbr.insaddr.add_info('CDPayoutType') == 'ParMinusRecovery':
			payout=(1.0-rec[i])
	    	    elif c.legnbr.insaddr.add_info('CDPayoutType') == 'Digital':
	    		percentpayout=float(c.legnbr.insaddr.add_info('CDPercentPayout'))
		    	if (percentpayout > 0.0): 
		            payout=percentpayout/100.0
		    	else:
		            print 'CDPercentPayout value is unrealistic'
			    payout=0.0
	    	    else:
			print 'Unknown CD PayoutType method'
			payout=0.0
		    res=res+(payout*prob[i]*riskfree[i]*\
		        c.nominal_amount()/c.legnbr.insaddr.contr_size)
		if c.legnbr.payleg:
		    res=-1.0*res
		p=[res, c.pay_day, c.legnbr.curr, 'Float', c]
	    else:
		nominal=c.nominal_amount()/c.legnbr.insaddr.contr_size
		if c.type == 'Fixed Amount':
		    res=nominal
		else:
		    rate=c.period_rate()
    	    	    period=c.start_day.years_between(c.end_day, c.legnbr.daycount_method)
		    res=rate/100.0*nominal*period
		nr=1
		prob, discriskfree, rec=TreeProb(c, recrate, issuers, inst, weights, nr)		
		disc=1-prob[0]
		if c.pay_day <= ael.date_today():
		    res=res
		else:
		    res=disc*discriskfree[0]*res
	    	p=[res, c.pay_day, c.legnbr.curr, 'Fixed', c]
	    payments.append(p)
	else:
    	    if c.type == 'Credit Default':
	    	p=[res, c.pay_day, c.legnbr.curr, 'Float', c]
    	    else:
	    	p=[res, c.pay_day, c.legnbr.curr, 'Fixed', c]
	    payments.append(p)
