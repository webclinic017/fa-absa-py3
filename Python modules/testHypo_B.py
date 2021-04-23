import acm

parameters = {80594173:[51250000, '31/10/2018', 10.50525, 0], 
    80353595:[57400000, '31/10/2018', 10.51073, 0], 
    51456204:[141445781.123864, '31/10/2018', 10.48807, 0], 
    82021659:[55500000, '31/01/2019', 10.3401, 0], 
    81785272:[52000000, '31/01/2019', 10.32543, 0], 
    76969625:[26633628.252, '31/10/2018', 10.86294, 0], 
    80589185:[51500000, '31/10/2018', 10.50525, 0], 
    73727086:[17550000, '31/10/2018', 11.13214, 0], 
    75152197:[17800000, '31/10/2018', 11.16148, 0], 
    75138173:[16700000, '31/10/2018', 11.16148, 0], 
    70948815:[15916212, '31/10/2018', 11.1704, 0], 
    83330457:[12700000, '31/10/2018', 11.24554, 0], 
    85721266:[16950000, '31/10/2018', 11.26916, 0], 
    90276173:[17500000, '26/09/2018', 11.24673, 0], 
    76801315:[11875000, '31/10/2018', 11.32105, 0], 
    96750997:[12400000, '26/09/2018', 11.3058, 0], 
    96384516:[11000000, '27/09/2018', 10.96148, 0], 
    95529484:[16000000, '15/10/2018', 10.7776, 0], 
    85082415:[78750000, '31/01/2019', 10.33129, 0], 
    99992697:[9900000, '31/10/2018', 11.39068, 0], 
    84910002:[419500000, '31/01/2019', 10.33438, 0], 
    4874138:[6160000, '12/11/2018', 11.33451, 1.92], 
    70718202:[28101000, '19/12/2018', 10.74242, 0], 
    97932055:[263900000, '06/09/2018', 10.57966, 0], 
    98304491:[263900000, '06/09/2018', 10.57598, 0], 
    98469243:[263900000, '06/09/2018', 10.57549, 0], 
    78808995:[50000000, '31/01/2019', 10.43401, 0], 
    83065788:[52500000, '31/01/2019', 10.36232, 0], 
    93481413:[40527000, '31/01/2019', 10.35319, 0], 
    70119923:[136850000, '31/01/2019', 10.3371, 0], 
    40692546:[52200000, '31/01/2019', 10.36024, 0], 
    97645223:[40000000, '31/01/2019', 10.34974, 0], 
    72337112:[59400000, '31/12/2018', 10.44051, 0], 
    69823954:[816649359.818452, '30/11/2018', 10.45083, 0], 
    68650941:[539712500.016549, '30/11/2018', 10.44265, 0], 
    76927843:[386000000, '31/10/2018', 10.39534, 0], 
    12867454:[44000000, '31/01/2019', 10.41353, 0.49], 
    99549594:[54940000, '18/02/2019', 10.39273, 0], 
    100837007:[56000000, '04/02/2019', 10.34356, 0], 
    98876478:[152500000, '05/02/2019', 10.36835, 0], 
    100256047:[157000000, '05/02/2019', 10.35526, 0], 
    90495172:[28000000, '07/02/2019', 10.35115, 0]} 

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
        new_ins.Name(old_ins.Name()+'_Hypo_B'+'/'+str(parameters[trade_nbr][2]))
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
