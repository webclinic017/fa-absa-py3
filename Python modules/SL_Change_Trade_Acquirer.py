import acm

trade_key = '0'
acquirer_key = '1'



RELEVANT_COUNTERPARTIES = [
    acm.FParty['SBL AGENCY I/DESK']
]

ael_variables = [[trade_key, 'Trades Selection', 'FTrade', None,
        None, 0, 1, 'Global One trade selection.', None, 1],
    [acquirer_key, 'Acquirer Name', 'FParty', None,
        None, 1, 1, 'Acquirer', None, 1]]

portfolioMapping = {'ACS - Script Lending':'SBL_Accrued_1','Bond - Script Lending':'SBL_Agency_Bond_ETF','SBL - Prime Clients':'SBL_Agency_Prime_Broker',
			'SBL_CFD_Old Mutual':'SBL_Agency_OmsfinCFD','SBL_Fixed Income DBR':'SBL_Agency_Bond','SBL_Fixed Income Denel':'SBL_Agency_Bond',
			'SBL_Fixed Income Denel RF':'SBL_Agency_Bond','SBL_Fixed Income National Tertiary RF':'SBL_Agency_Bond', 'SBL_Fixed Income UPT':'SBL_Agency_Bond',
			'SBL_Fixed Income_ Unisa':'SBL_Agency_Bond','SBL_Fixed Income_ University Free State':'SBL_Agency_Bond',
			'SBL_Structured Repo':'SBL_Agency_Bond','SBL_Fixed Income_De Beers':'SBL_Agency_Bond','SL_LEIPS':'SBL_Accrued_1'}


def ael_main(parameters):
    acquirer = parameters[acquirer_key]
    if len(acquirer) > 1:
        print('Too many Acquirer selected..')
        return
        
    trades = parameters[trade_key]    
    
    partyAcquirer = acquirer[0]  
    print(trades)
            
    for trd in trades:
        print(trd.Oid(), trd.Portfolio().Name(), trd.Counterparty().Name())
        if trd.Portfolio().Name() in portfolioMapping.keys() and RELEVANT_COUNTERPARTIES[0].Name() == trd.Counterparty().Name():
            try:
                trd.Acquirer(partyAcquirer)
                trd.Commit()
                print('Changed the acquirer for trade %s '%(trd.Oid()))
            except Exception, ex:
                print('Exception updating acquirer for trade %s ' % (trade.Oid()))
            

        
         

    
    
