import acm

def ProjectCashFlowAmend(fTrade):
        ContractTrade = fTrade.Contract()
        ContractTrade.Status('Terminated')
        ContractTrade.Type('Normal')
        ContractTrade.OptionalKey('')
        ContractTrade.Commit()
        
        ClosingTrade = ContractTrade.Clone()
        ClosingTrade.Nominal(-1*ContractTrade.Nominal())
        ClosingTrade.TradeTime(acm.Time.TimeNow())
        ClosingTrade.ValueDay(acm.Time.DateToday())
        ClosingTrade.AcquireDay(acm.Time.DateToday())
        ClosingTrade.Counterparty('MARKET RISK DUMMY')
        ClosingTrade.Portfolio('Swap Flow')
        ClosingTrade.OptionalKey('')
        ClosingTrade.Type('Closing')
        ClosingTrade.MirrorTrade(None)
        ClosingTrade.Commit()    

list = [59818839,
59818713,
59818395,
59818392,
59818391,
59818390,
59818389,
59818388,
59818387,
59818386,
59810636,
59810617,
59810602,
59810593,
59810580,
59810564,
59810555,
59810522,
59810511,
59810490,
59810471,
59810446,
59810390,
59810362,
59810340,
59810320,
59810312,
59810292,
59810238,
59810212,
59810180,
59810161,
59810151]

for lis in list:
    print lis
    fTrade = acm.FTrade[lis]
    try:
        ProjectCashFlowAmend(fTrade)
        print ' Created trade XXXXXXXXXXXXXXXXXXXXXXXXXX'
    except StandardError, e:
        print 'The following error occurred', str(e)
