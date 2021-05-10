
import acm

def Direction(self):

    try:
        ins = self.Instrument()
        
        # Interest Rate Swap
        if ins.IsKindOf('FSwap'):
            return SwapDirection(self, ins)
         
        # Credit Default Swap
        if ins.IsKindOf('FCreditDefaultSwap'):
            return CreditDefaultSwapDirection(self, ins)
        
        # Deposit/Loan   
        if ins.IsKindOf('FDeposit'):
            return DepositDirection(self, ins);
            
        # Repo/Reverse
        if ins.IsKindOf('FRepo'):
            return RepoDirection(self)
            
        # Buy-Sellback
        if ins.IsKindOf('FBuySellBack'):
            return BuySellbackDirection(self)
        
        return self.BoughtAsString()
    except:
        return self.BoughtAsString()

def SwapDirection(trade, ins):
    qty = trade.Quantity()
    rec = ins.RecLeg()
    pay = ins.PayLeg()
    
    recIsFixed = rec.IsFixedLeg()
    payIsFixed = pay.IsFixedLeg()

    # Fixed/Float
    if (qty > 0 and (not recIsFixed) and payIsFixed) or (qty < 0 and recIsFixed and (not payIsFixed)):
        return 'Pay Fixed'
        
    if (qty > 0 and recIsFixed and (not payIsFixed)) or (qty < 0 and (not recIsFixed) and payIsFixed):
        return 'Receive Fixed'
        
    recRef = rec.FloatRateReference()
    payRef = pay.FloatRateReference()
    
    # Basis swaps
    if  rec.IsFloatLeg() and \
        pay.IsFloatLeg() and \
        (recRef.InsType() == 'RateIndex') and \
        (payRef.InsType() == 'RateIndex') and \
        (pay.FloatRateReference2() == None) and \
        (rec.FloatRateReference2() == None) and \
        (payRef.FirstFixedLeg().EndPeriod() != recRef.FirstFixedLeg().EndPeriod()):
        
        payLegRateIndexPeriodValue = payRef.FirstFixedLeg().EndPeriod()
        count = acm.Time.DatePeriodCount(payLegRateIndexPeriodValue)
        unit = acm.Time.DatePeriodUnit(payLegRateIndexPeriodValue)
        if unit == 'Days':
            payLegRateIndexPeriod = str(count) + 'D' 
        if unit == 'Weeks':
            payLegRateIndexPeriod = str(count) + 'W' 
        if unit == 'Months':
            payLegRateIndexPeriod = str(count) + 'M'   
        if unit == 'Years':
            payLegRateIndexPeriod = str(count) + 'Y'
        if (unit == 'Days' and count == 1):
            payLegRateIndexPeriod = 'ON'
    
        if (qty > 0):
            return 'Pay ' + payLegRateIndexPeriod + ' Float'

        if (qty < 0):
            return 'Receive ' + payLegRateIndexPeriod + ' Float'

    return ''
    
def CreditDefaultSwapDirection(trade, ins):
    qty = trade.Quantity()
    recIsCreditDefault = ins.RecLeg().LegType() == 'Credit Default'
    payIsCreditDefault = ins.PayLeg().LegType() == 'Credit Default'
    
    if (qty > 0 and recIsCreditDefault and (not payIsCreditDefault)) or (qty < 0 and (not recIsCreditDefault) and payIsCreditDefault):
        return 'Buy Protection'
        
    if (qty > 0 and (not recIsCreditDefault) and payIsCreditDefault) or (qty < 0 and recIsCreditDefault and (not payIsCreditDefault)):
        return 'Sell Protection'
        
    return ''
  
def DepositDirection(trade, ins):  
    legType = ins.Legs().First().LegType()
    if legType == 'Fixed' or legType == 'Float':
        if trade.StartCash() > 0:
            return 'Deposit'
        if trade.StartCash() < 0:
            return 'Loan'
    return ''

def RepoDirection(trade):     
    if trade.Nominal() < 0:
        return 'Repo'
    if trade.Nominal() > 0:
        return 'Reverse Repo'
    return ''
 
def BuySellbackDirection(trade):   
    if trade.Nominal() > 0:
        return 'Buy-Sellback'
    if trade.Nominal() < 0:
        return 'Sell-Buyback'
    return ''
