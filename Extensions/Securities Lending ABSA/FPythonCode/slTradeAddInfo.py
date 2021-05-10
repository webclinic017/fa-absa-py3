
import acm 

def LendFee(ins):
    
    trd=ins.Trades().At(0)
    lf = str(trd.AdditionalInfo().SL_G1Fee2())
    return lf
    
def FundLender(ins):
    trd=ins.Trades().At(0)
    funder_lender = str(trd.AdditionalInfo().SL_G1Counterparty2())
    return funder_lender
    
def Borrow(ins):
    trd=ins.Trades().At(0)
    borrower = str(trd.AdditionalInfo().SL_G1Counterparty1())
    return borrower
    
def SDSID(party):
    return party.AdditionalInfo().BarCap_SMS_LE_SDSID()

def BorrowSDSID(ins):
    borrower = Borrow(ins)
    party = acm.FParty[borrower]
    if party:
        return SDSID(party)

def FundLenderSDSID(ins):
    lender = FundLender(ins)
    party = acm.FParty[lender]
    if party:
        return SDSID(party)
