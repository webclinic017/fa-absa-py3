import ael, string, math

def CheckBSB(temp,prf,ins,*rest):
    
    trds = ael.Trade.select('prfnbr = %s' % ael.Portfolio[prf].prfnbr)
 
    for t in trds:
        if ael.date_from_time(t.creat_time) == ael.date_today():
            if t.insaddr.und_insaddr == ael.Instrument[ins]:
                if t.text1 == 'Ael booked':
                    return 1
                else:
                    return 0
    return 0
    
    
def CreateBSB(temp,security,repo,amount,portfolio,portfolionew,*rest):

    if ael.Portfolio[portfolio].prfnbr == 1990 and security[0:5] != 'ZAR/R': #ALBI GOVI Structures
        bookBSB = 0
    else:
        bookBSB = 1
        
    if bookBSB and amount != 0:
        i_new = ael.Instrument.new('BuySellback')
        t_new = ael.Trade.new(i_new)

        today = ael.date_today()
        sec = ael.Instrument[security]
        
        i_new.start_day = today.add_banking_day(ael.Instrument['ZAR'], 2)#t.start_day
        i_new.exp_day = today.add_banking_day(ael.Instrument['ZAR'], 3)#t.exp_day
        i_new.rate = float(repo)
        i_new.contr_size = 1000000
        i_new.und_insaddr = sec
        i_new.insid = i_new.suggest_id()
        i_new.daycount_method = 'Act/365'
        #i_new.commit()    
        #print i_new.pp()
        
        t_new.quantity = (amount/1000000) * -1
        t_new.counterparty_ptynbr = 'DRA TRANSAKSIES'
        t_new.acquirer_ptynbr = 'CM Funding'
        t_new.status = 'Simulated'
        if portfolio == 'JOB15':
            t_new.prfnbr = ael.Portfolio['JOB14']
        else:
            t_new.prfnbr = portfolio
        t_new.text1 = 'Ael booked'
        t_new.price = (float)(sec.mtm_price_suggest(today, 'ZAR'))
        t_new.premium=t_new.premium_from_quote(i_new.start_day, t_new.price)
        i_new.ref_price=t_new.buy_sellback_ref_price()
        i_new.ref_value=t_new.buy_sellback_ref_value(1)

        #i_new.ref_value=math.floor(i_new.ref_value*t_new.quantity)/t_new.quantity
        #print 'premium',t_new.premium
        #print 'end cash',i_new.ref_value
        i_new.commit()
        if portfolio == ('JOB1' or 'JOBX1'):
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT001"')
        elif portfolio == 'JOB11':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT011"')
        elif portfolio == 'DERV':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="DER001"')
        elif portfolio == 'JOB4':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT004"')
        elif portfolio == 'JOB5':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT005"')
        elif portfolio == 'JOB3':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT003"')
        elif portfolio == 'JOB8':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT008"')
        elif portfolio == 'JOB2':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT002"')
        elif portfolio == 'JOB10':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT010"')
        elif portfolio == ('MAN_BOND' or 'MAN_BOND_2'):
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="MAN_Bond"')
        elif portfolio == 'DERV2':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="DER002"')
        elif portfolio == 'DERV3':
            t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="DER003"')
        else:
            t_new.optkey1_chlnbr = 0

        t_new.commit()

        
        ii_new = ael.Instrument.new('BuySellback')
        tt_new = ael.Trade.new(ii_new)

        ii_new.start_day = today.add_banking_day(ael.Instrument['ZAR'], 2)#t.start_day
        ii_new.exp_day = today.add_banking_day(ael.Instrument['ZAR'], 3)#t.exp_day
        ii_new.rate = float(repo)
        ii_new.contr_size = 1000000
        ii_new.und_insaddr = sec
        ii_new.insid = ii_new.suggest_id()
        ii_new.daycount_method = 'Act/365'
        #ii_new.commit()
    
    
        tt_new.quantity = (amount/1000000)
        tt_new.counterparty_ptynbr = 'DRA TRANSAKSIES'
        tt_new.acquirer_ptynbr = 'CM Funding'
        tt_new.status = 'Simulated'
        tt_new.prfnbr = portfolionew
        tt_new.text1 = 'Ael booked'
        tt_new.price = (float)(sec.mtm_price_suggest(today, 'ZAR'))
        tt_new.premium=tt_new.premium_from_quote(i_new.start_day, t_new.price)
        ii_new.ref_price=tt_new.buy_sellback_ref_price()
        ii_new.ref_value=tt_new.buy_sellback_ref_value(1)

        #ii_new.ref_value=math.floor(i_new.ref_value*10)/10
        tt_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SPT006"')
        ii_new.commit()
        tt_new.commit()
        return 'work'
        
#print CreateBSB(1,'ZAR/R153',11,10000000,'ALBI GOVI Structures','CA_Test')
