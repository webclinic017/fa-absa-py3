
import acm

def PromissoryLoanCLN(eii):
    acm.StartApplication("Instrument Definition", acm.FSymbol("Promissory Loan CLN"))
    return    

def PromissoryLoanDualCurrency(eii):
    acm.StartApplication("Instrument Definition", acm.FSymbol("Promissory Loan Dual Currency"))
    return    

def PromissoryLoanIndexLinked(eii):
    acm.StartApplication("Instrument Definition", acm.FSymbol("Promissory Loan Index Linked"))
    return    

def PromissoryLoanZero(eii):
    acm.StartApplication("Instrument Definition", acm.FSymbol("Promissory Loan Zero"))
    return    

def UpdateDefaultInstrument(ins):
    ins.IssuanceType = "Registered"

def UpdateDefaultTrade(trade):
    trade.FlatAccrued= True
