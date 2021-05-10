import acm

def getInterestReinvestment(trade, noticetype):
    reinvested_amount = 0
    if noticetype == "Primary Deposit": 
        for cashflow in trade.Instrument().Legs()[0].CashFlows():
            if cashflow.CashFlowType() == 'Interest Reinvestment':
                reinvested_amount += cashflow.FixedAmount()
    return reinvested_amount
    
def noticeAmount(portfolio, noticetype):
    amount = 0
    for trade in portfolio.Trades():
        instrument = trade.Instrument()
        amount += depositNoticeAmount(instrument, noticetype)
    return amount 

def depositNoticeAmount(instrument, noticetype):
    amount = 0
    reinvested_interest = getInterestReinvestment(instrument.Trades()[0], noticetype) 
    for trade in instrument.Trades():
        if trade.Status() in ["FO Confirmed", "BO Confirmed", "BO-BO Confirmed"]:
            for leg in instrument.Legs():
                for cashflow in leg.CashFlows():
                    if cashflow.CashFlowType() == "Fixed Amount" and cashflow.AdditionalInfo().Deposit_Notice_Type() == noticetype:
                        amount += cashflow.FixedAmount() 
    return (amount + reinvested_interest)
