import ael


def AfricaWT(Temp,trd,ins,CNT,*rest):
    TAX = {'AOA':0.2,'BWP':0.15,'GHS':0.0,'KES':0.15,'MUR':0.0,'MZM':0.2,'NAD':0.0,'TZS':0.1,'UGX':0.15,'ZMK':0.16,'ZMW':0.16}
    if CNT in TAX:
        counter = 1
        listp = []
        listpt = []
        listcf = []
        trade = ael.Trade[trd].clone()
        pymnts = trade.payments()
        ins = ael.Instrument[ins]
        legs = ins.legs()
        for l in legs:
            for p in pymnts:
                listp = listp + [p.payday]
                listpt = listpt + [p.text]            
            for cf in l.cash_flows():
                if (cf.type != 'Fixed Amount'):
                    listcf = listcf + [cf.pay_day]
        listcf.sort()
        for l in legs:
            for i in listcf:
                for cf in l.cash_flows():
                    if (i == cf.pay_day):
                        if (cf.pay_day not in listp):
                            if (cf.type != 'Fixed Amount'):
                                ptext = 'Witholdings tax C' + str(counter)
                                while ptext in listpt:
                                    counter = counter + 1
                                    ptext = 'Witholdings tax C' + str(counter)
                                else:
                                    pymnt = ael.Payment.new(trade)
                                    pymnt.amount = -1*trade.quantity*cf.projected_cf()*TAX[CNT]
                                    pymnt.payday = cf.pay_day
                                    pymnt.text = ptext
                                    pymnt.commit()
                                    listpt = listpt + [ptext]
                        elif (cf.pay_day >= ael.date_today()):
                            if (cf.type != 'Fixed Amount'):
                                for pnbr in pymnts:
                                    if (pnbr.payday == cf.pay_day):
                                        pymnt = ael.Payment[pnbr.paynbr].clone()
                                        pymnt.amount = -1*trade.quantity*cf.projected_cf()*TAX[CNT]
                                        pymnt.commit()
        return 'Success'
    elif CNT == '':
        return 'No Africa country specified'
    else: return 'Africa country not found'
    
#ael.date_today()

def Old(temp,inst,CNT,*rest):
    TAX = {'AOA':0.2,'BWP':0.15,'GHS':0.0,'KES':0.15,'MUR':0.0,'MZM':0.2,'NAD':0.0,'TZS':0.1,'UGX':0.15,'ZMK':0.16,'ZMW':0.16}
    if CNT in TAX:
        ins = ael.Instrument[inst].clone()
        legs = ins.legs()
        
        ins.commit()
        return 'Success'
    elif CNT == '':
        return 'No Africa country specified'
    else: return 'Africa country not found'


def TaxRates(*rest):
    TAX = {'AOA':0.2,'BWP':0.15,'GHS':0.0,'KES':0.15,'MUR':0.0,'MZM':0.2,'NAD':0.0,'TZS':0.1,'UGX':0.15,'ZMK':0.16,'ZMW':0.16}
    for i in TAX:
        print(i, TAX[i])


def deletetrd(trd,pymnt,*rest):
    trade = ael.Trade[trd].clone()
    for py in trade.payments():
        if (py.paynbr == pymnt):
            py.delete()
    trade.commit()
    ael.poll()


#print AfricaWT(4708208,'MZN-Govt-Bond-110908','MZM')
#print deletetrd(4708208,25263)
#print TaxRates()
