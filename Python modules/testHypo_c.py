import acm

parameters = {81785272:[104500000, '31/01/2019', 10.32543, 0], 
    76969625:[17003389.788, '31/10/2018', 10.86294, 0], 
    85721266:[17250000, '31/10/2018', 11.26916, 0], 
    70948815:[17093115, '31/10/2018', 11.1704, 0], 
    83330457:[12650000, '31/10/2018', 11.24554, 0], 
    90276173:[12400000, '26/09/2018', 11.24673, 0], 
    83065788:[342720000, '31/01/2019', 10.36232, 0], 
    69823954:[820235400.918948, '30/11/2018', 10.45082, 0], 
    12867454:[36200000, '16/01/2019', 10.46849, 0.49], 
    80589185:[86000000, '31/10/2018', 10.50525, 0]} 

import acm


for trade_nbr in parameters.keys():
    trade = acm.FTrade[trade_nbr]
    old_ins = trade.Instrument()

    new_ins = acm.FSwap()

    old_ins = trade.Instrument()
    new_ins.Apply(old_ins)
    
    new_ins_name = old_ins.Name()+'_Hypo'+'/'+str(parameters[trade_nbr][2])
    existing_ins = acm.FInstrument[new_ins_name]

    if existing_ins:
        new_ins.Name(old_ins.Name()+'_Hypo_C'+'/'+str(parameters[trade_nbr][2]))
    else:
        new_ins.Name(new_ins_name)

    #new_ins.Name(old_ins.Name()+'_Hypo'+'/'+str(parameters[trade_nbr][2]))

    for leg in new_ins.Legs():
        if leg.LegType() == 'Fixed':
            leg.FixedRate = parameters[trade_nbr][2]
            leg.GenerateCashFlows(0)
        else:
            leg.FloatRateReference=acm.FRateIndex['ZAR/Hypo_Spread_3mJibar']
            leg.Spread = parameters[trade_nbr][3]
            leg.GenerateCashFlows(0)
            
        for cash_flow in leg.CashFlows():
            if cash_flow.ExternalId() is None:
                continue
            else:
                cash_flow.ExternalId = ''                

    new_ins.ExternalId2 = ''
    new_ins.ValuationGrpChlItem=acm.FChoiceList['AC_GLOBAL']
    
    try:
        new_ins.Commit()
        print 'Created a Hypo instrument %s' %new_ins.Name()
    except Exception as e:        
       print 'Error on trade: Cannot create intrument', trade_nbr, e
        

    #trade = acm.FTrade[trade_nbr]

    new_trade = acm.FTrade()
    new_trade.Apply(trade)
    new_trade.Instrument = new_ins
    new_trade.OptionalKey = ''
    new_trade.Portfolio=acm.FPhysicalPortfolio['Simulate_GT Hypo Primary']
    new_trade.ValueDay = parameters[trade_nbr][1]
    new_trade.Nominal = parameters[trade_nbr][0]
    new_trade.MirrorPortfolio=acm.FPhysicalPortfolio['Simulate_GT Hypo Control']
    new_trade.Counterparty =acm.FInternalDepartment['GROUP TREASURY']
    new_trade.Acquirer=acm.FInternalDepartment['GROUP TREASURY']
    new_trade.Trader(acm.User())
    new_trade.Status = 'Simulated'
    
    try:
        new_trade.Commit()
        print 'Done creating a new trade with trade number {0}, original trade {1}, intrument {2}'.format(new_trade.Oid(), trade.Oid(), new_trade.Instrument().Name() )
    except Exception as e:
        print 'Error on trade: cannot create trade', trade_nbr, e
