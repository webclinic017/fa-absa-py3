import ael
def greateBench(ucurr, scurr, valg):
    today = ael.date_today()
    optend = ['1D', '1W', '1M', '2M', '3M', '6M', '9M', '1Y', '2Y', '3Y', '4Y', '5Y', '6Y']
    strikes = [0.10, 0.25, 0.5, 0.75, 0.90]
    for k in optend:
        for s in strikes:
            newins = ael.Instrument.new('Option')
            newins.exp_period = k
            newins.exercise_type = 'European'
            newins.call_option = 0
            newins.strike_type = 'Delta'
            newins.strike_price = s - 1 
            newins.und_insaddr = ucurr
            newins.curr = ael.Instrument['USD']
            newins.strike_curr = scurr
            entry = ael.ChoiceList.read('entry = "%s"' %(valg))
            newins.product_chlnbr = entry
            newins.settlement = 'Cash'
            newins.pay_day_offset = 2
            newins.insid = scurr + '-' + ucurr + '/' + (str)(s) + 'DEL/' + 'PUT/' + k 
            newins.generic = 1
            newins.quote_type = 'Per Contract'
            newins.paytype = 'Spot'
            newins.otc = 1
            ninsid = newins.insid
            if ael.Instrument[newins.insid]:
                print 'Duplicate: ', newins.insid
            else:
                try:
                    newins.commit()
                except:
                    print 'Not created'
                    print ninsid
            newins = ael.Instrument.new('Option')
            newins.exp_period = k
            newins.exercise_type = 'European'
            newins.call_option = 1
            newins.strike_type = 'Delta'
            newins.strike_price = s 
            newins.und_insaddr = ucurr
            newins.curr = ael.Instrument['USD']
            newins.strike_curr = scurr
            newins.product_chlnbr = entry
            newins.settlement = 'Cash'
            newins.pay_day_offset = 2
            newins.insid = scurr + '-' + ucurr + '/' + (str)(s) + 'DEL/' + 'CALL/' + k 
            newins.generic = 1
            newins.quote_type = 'Per Contract'
            newins.paytype = 'Spot'
            newins.otc = 1
            ninsid = newins.insid
            if ael.Instrument[newins.insid]:
                print 'Duplicate: ', newins.insid
            else:
                try:
                    newins.commit()
                except:
                    print 'Not created'
                    print ninsid
 
def getFirstCurr():
    list = []
    cp = ael.CurrencyPair.select()
    for c in cp:
        if c not in list:
            list.append(c.curr1.insid)
    return list
 
def getSecondCurr():
    list = []
    cp = ael.CurrencyPair.select()
    for c in cp:
        if c not in list:
            list.append(c.curr1.insid)
    return list
    
def getValgroup():
    list = []
    cl = ael.ChoiceList.select()
    for c in cl:
        if c.list == 'ValGroup':
            if c not in list:
                list.append(c.entry)
    return list
    
ael_variables = [('und', 'BaseCurr', 'string', getFirstCurr(), None, 1, 0),
                ('scurr', 'QuotedCurr', 'string', getSecondCurr(), None, 1, 0),
                ('valg', 'ValGroup', 'string', getValgroup(), None, 1, 0)]
 
def ael_main(ael_dict):
    ui = ael_dict['und']
    sc = ael_dict['scurr']
    v = ael_dict['valg']
    greateBench(ui, sc, v)
