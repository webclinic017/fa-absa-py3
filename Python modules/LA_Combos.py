import ael, SAGEN_Cashflows


def GetComboNominal(temp, i, *rest):
     
    if i.insid.__contains__('TARF'):
        nom = 0.00
        for u in i.combination_links():
            if len(u.member_insaddr.legs()) == 0:
                print('no legs')
            else:
                for ul in u.member_insaddr.legs():
                    if ul.curr.insid == 'ZAR':
                        for c in ul.cash_flows():
                            nom = nom + c.nominal_amount()
        return nom


def GetComboAVGStrike(temp, i, *rest):
     
    if i.insid.__contains__('TARF'):
        pnom = 0.00
        rnom = 0.00
        for u in i.combination_links():
            if len(u.member_insaddr.legs()) == 0:
                print('no legs')
            else:
                for ul in u.member_insaddr.legs():
                    if ul.payleg == 1:
                        for c in ul.cash_flows():
                            pnom = pnom + c.nominal_amount()
                    else:
                        for c in ul.cash_flows():
                            rnom = rnom + c.nominal_amount()
        return abs(pnom/rnom)
'''
def GetComboNominal(temp, trd, sdate, flag, *rest):

    try:
    	d = ael.date_from_string(sdate)
    except:
        #print '\n argument1 not in string format\n'
	d = sdate
    
    
    i = trd.insaddr
    nom = t.nominal_amount() #trd.quantity * i.contr_size
    n, r = 0.0, 0.0
    rate = 0.0

    if trd.value_day > d:
        nom = n
    elif t.trdnbr == 2602876:
        nom = t.quantity
    else:
        for u in i.combination_links():
            if len(u.member_insaddr.legs()) == 0:
                print 'no legs'
                nom = n
            elif i.insid.__contains__('TARF'): # == 'FX_TARF_MUSTEK_28OCT08':
                print i.insid
                nom = SAGEN_Cashflows.GetCashflow_Ins(1, i, d, 3, 'NextCF')
                print nom
                '''            
'''            
                for c in u.member_insaddr.cash_flows():
                    #print 2, u.member_insaddr.insid
                    if c.start_day <= d and c.end_day >= d and c.pay_day >= d:
                        n = c.nominal_amount()*(trd.quantity/i.index_factor)
                        #print 'xxxxxxxxxxxxx', c.cfwnbr, n
                        if n > nom:
                            nom = n
                        if c.type == 'Float Rate':
                            r = c.period_rate(c.start_day, c.end_day)
                            #print 'r', r
                        if r > rate:
                            rate = r
        '''
    #print 'RETURN', nom, rate                        
'''
    if flag == 1:
        return nom
    else:
        return rate

    '''

        #print dir(u.member_insaddr.'cash_flows', )

    #print i, dir(i)
'''
    else:
        nom = t.nominal_amount()
        nom2 = trd.quantity * i.contr_size
        
    return 1

    '''
        
        
        
        
#t = ael.Trade[3461499].insaddr #2701025] 
#print GetComboNominal2(1, t)
