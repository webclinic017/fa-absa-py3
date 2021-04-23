'''
This script is a preliminary version of the task included in the mirror trade booking for Non ZAR deposits.
It nets all cashflows per portfolio, currency and pay day and books it on the relevant account. 
Since several pieces of information are still missing at this point of time (11/12/2014) it has to be adapted once decision are taken.

'''

import ael, acm
import PACE_MM_Parameters as Params
from PACE_MM_Helper_Functions import PACE_MM_Helper_Functions as Utils

query = "select c.cfwnbr 'Cfwnbr', pf.prfid from trade t, instrument i, leg l, cashflow c, party p,  party aq, portfolio pf where t.insaddr = i.insaddr and i.insaddr = l.insaddr and l.legnbr = c.legnbr and t.counterparty_ptynbr = p.ptynbr and t.acquirer_ptynbr = aq.ptynbr and t.prfnbr = pf.prfnbr and to_date(i.exp_day) >= TODAY and i.instype = 'Deposit' and i.open_end = 'Open End' and add_info(p,'PACE_MM_Client') = 'Yes' and c.type in ('Fixed Amount','Interest Reinvestment') and to_date(c.updat_time) = TODAY and t.optional_key like '%BARXMM%MMG%' and t.status in ('BO Confirmed','BO-BO Confirmed') and aq.ptyid in ('Funding Desk', 'Money Market Desk') and l.type = 'Call Fixed Adjustable'" 
cashflows = ael.asql(query)[1][0]

#currencies = ['USD']
currencies = Params.VALID_CURRENCIES
currencies = [x for x in currencies if x != 'ZAR']
portfolios = ['Call_5617 CIB Dp CAPE', 'Call_5615 CIB Dp GTNG', 'Call_5616 CIB Dp DBN']


for currency in currencies:
    print ''
    print '****************************'
    print 'Now processing currency %s' %currency
    print '****************************'
    for portfolio in portfolios: 
        print ''
        print 'Portfolio %s' %portfolio
        print '-----------------------------------------------------'
        # get relevant pay dates
        dates = set()
        for cf in cashflows:
            cashflow = acm.FCashFlow[cf[0]]
            if cashflow.Leg().Currency().Name() == currency and cf[1] == portfolio:
                dates.add(cashflow.PayDate())
        if not dates:
            print 'No cashflows for this portfolio'
        else:
            # net per paydate
            for paydate in dates: 
                print ''
                print '  Netting of all cashflows for paydate %s:' %paydate
                print '---------------------------------------------------------'
                net = 0
                for cf in cashflows:
                    cashflow = acm.FCashFlow[cf[0]]
                    if cashflow.Leg().Currency().Name() == currency and cashflow.PayDate()== paydate and cf[1] == portfolio:
                        print 'The cashflow %s of instrument %s with an amount of %s is included in the netting.' %(cashflow.Oid(), cashflow.Leg().Instrument().Name(), cashflow.FixedAmount())
                        net = net + cashflow.FixedAmount()
                print 'The netted amount for currency %s, portfolio %s and paydate %s is %s.' %(currency, portfolio, paydate, net)
                '''if net != 0:
                    #instrument name has to be specified
                    insname = currency+'_'+portfolio[17:]+'_NonZAR_B2B'
                    print insname
                    updateinstr = acm.FInstrument[insname]
                    newCf = acm.FCashFlow()
                    newCf.Leg(updateinstr.Legs()[0])
                    newCf.PayDate(paydate)
                    newCf.CashFlowType(Utils.GetEnum('CashFlowType','Fixed Amount'))
                    newCf.FixedAmount(net)
                    newCf.NominalFactor(1)
                    newCf.Commit()
                print 'The netted amount was booked on instrument %s as cashflow %s' %(updateinstr.Name(),newCf.Oid()) '''
      
       
        
