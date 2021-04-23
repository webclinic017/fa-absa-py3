import ael

#dt = ael.date_today()

#ael_variables = [('Date', 'Run Date', 'date', dt, dt, 0, 0)]

#def ael_main(dict):


def PriceKeeper(temp, sday, *rest):

    print '**************************************'    
    print '******Starting To Copy *****'	
    print '**************************************'
    
    ael.poll()
    
    try:
    	td = ael.date_from_string(sday)
    except:
#       	print '\n argument1 not in string format\n'
	td = sday
    
    try:
    	ad = ael.date_from_string('0000/01/01')
    except:
#       	print '\n argument1 not in string format\n'
#	pass
        ad = 0000-01-01
        
#td = dict["Date"] #.date(dt)
    #ael_dict["TradeFilter"]
    print td
    #list = []
    #list.append(ael.Instrument['USD/IRS/F-LI/030811-080811/3.565'])
    for ins in ael.Instrument:
        if (ins.exp_day >= td or ins.exp_day == ad):
            cp = ins.prices()
            hp = ins.historical_prices(td.add_day(ael.Instrument['ZAR'], -1))
            if ins.instype not in ('BuySellback', 'Repo/Reverse', 'Deposit', 'FRN'): 
        #and ins.exp_day >= ael.date_today():
                print len(cp), len(hp)
                if len(hp) == 2:
                    #hp.sort()
                    
                    for p in hp:
                        if p.day == td.add_day(ael.Instrument['ZAR'], -1):
                            yes_price = p
                        if p.day == td:
                            tdy_price = p
                    
                    #print hp[0].day, hp[1].day, hp[2].day
                    nhp = tdy_price.clone()
                    nhp.settle = yes_price.settle
                    try:
                        nhp.commit()
                    except:
                        print 'Failed to keep price for ', ins.insid
                    
                    '''                        
                        print 'one'
                        nhp = p.clone() #new()
                        #nhp.day = td #ael.date_today()
                        #nhp.ptynbr = 10
                        print p.pp(), nhp.pp()
                        nhp.commit()
                    '''
                elif len(hp) == 1:
                    nhp = hp[0].new()
                    nhp.day = td #ael.date_today()
                    nhp.ptynbr = 1563
                    print nhp.pp()
                    try:
                        nhp.commit()
                    except:
                        print 'Failed to keep price for ', ins.insid
                        
                   
                    '''
                    ncp = p.clone()
                    ncp.day = td #ael.date_today()
                    #ncp.ptynbr = 10
                    print ncp.pp()
                    ncp.commit()
                    '''
            
    ael.poll()
    print '**************************************'    
    print '******Finished Copy *****'	
    print '**************************************'
    
    return 'Success'









