import acm

GBPCalendar=acm.FCurrency['GBP'].Calendar()

def InitiateDeal(ins):
    insDeco = acm.FBusinessLogicDecorator.WrapObject(ins)
    insDeco.RegenerateCashFlowsIfNeeded(True, True, True, True, True, True, True, True, True, None, None)
    insDeco.UpdateLegFixedRateOrSpread()

def CADSwapDealDefault(ins):
    CADSwapDefault(ins)
    InitiateDeal(ins)

def CHFSwapDealDefault(ins):
    CHFSwapDefault(ins)
    InitiateDeal(ins)

def EURSwapDealDefault(ins): 
    EURSwapDefault(ins)
    InitiateDeal(ins)

def GBPSwapDealDefault(ins):
    GBPSwapDefault(ins)
    InitiateDeal(ins)

def JPYSwapDealDefault(ins):
    JPYSwapDefault(ins)
    InitiateDeal(ins)

def USDSwapDealDefault(ins):
    USDSwapDefault(ins)
    InitiateDeal(ins)
    
def ZARSwapDealDefault(ins):
    ZARSwapDefault(ins)
    InitiateDeal(ins)

def CADSwapDefault(ins):
    insDeco=acm.FBusinessLogicDecorator.WrapObject(ins)
    recLeg=insDeco.FirstReceiveLeg()
    payLeg=insDeco.FirstPayLeg()
    
    if not payLeg.Currency() == 'Float':
        payLeg.LegType('Float')
    payLeg.RollingPeriod('3m')
    payLeg.RollingConv('Preserve EOM')
    
    if not payLeg.Currency().Name()=='CAD':
        payLeg.Currency('CAD')
    
    insDeco.MtmFromFeed(False)
    insDeco.SpotBankingDaysOffset(0)
    
    insDeco.LegStartPeriod('0d')
    insDeco.LegEndPeriod('5y')
        
    recLeg.LegType('Fixed')
    recLeg.RollingPeriod('6m')
    recLeg.DayCountMethod('Act/365')
    recLeg.RollingConv('None')
    recLeg.PayDayMethod('Mod. Following')
    
    payLeg.ResetDayMethod('Mod. Following')
    payLeg.ResetDayOffset(0)
    payLeg.RollingPeriod('6m')
    payLeg.ResetType('Compound Spread Excluded')
    payLeg.ResetPeriod('3m')
    payLeg.PayDayMethod('Mod. Following')
    
    insDeco.RegenerateCashFlowsIfNeeded(True, True, True, True, True, True, True, True, True, None, None)


def CHFSwapDefault(ins):
    insDeco=acm.FBusinessLogicDecorator.WrapObject(ins)
    recLeg=insDeco.FirstReceiveLeg()
    payLeg=insDeco.FirstPayLeg()
    
    if not payLeg.Currency() == 'Float':
        payLeg.LegType('Float')
    payLeg.RollingPeriod('6m')
    
    if not payLeg.Currency().Name()=='CHF':
        payLeg.Currency('CHF')
    insDeco.MtmFromFeed(False)
    insDeco.SpotBankingDaysOffset(2)

    insDeco.LegStartPeriod('0d')
    insDeco.LegEndPeriod('5y')
    
    recLeg.LegType('Fixed')
    recLeg.RollingPeriod('1y')
    recLeg.DayCountMethod('30/360')
    recLeg.RollingConv('Preserve EOM')
    recLeg.PayDayMethod('Mod. Following')
        
    payLeg.ResetDayMethod('Mod. Following')
    payLeg.PayDayMethod('Mod. Following')
    payLeg.RollingConv('Preserve EOM') 
    

def EURSwapDefault(ins):
    insDeco=acm.FBusinessLogicDecorator.WrapObject(ins)
    recLeg=insDeco.FirstReceiveLeg()
    payLeg=insDeco.FirstPayLeg()
            
    if not payLeg.Currency() == 'Float':
        payLeg.LegType('Float')
    payLeg.RollingPeriod('6m')
    
    if not payLeg.Currency().Name()=='EUR':
        payLeg.Currency('EUR')
    
    insDeco.MtmFromFeed(False)
    insDeco.SpotBankingDaysOffset(2)

    insDeco.LegStartPeriod('0d')
    insDeco.LegEndPeriod('5y')

    recLeg.LegType('Fixed')
    recLeg.RollingPeriod('1y')
    recLeg.DayCountMethod('30/360')
    recLeg.RollingConv('Preserve EOM')
    recLeg.PayDayMethod('Mod. Following')
    
    payLeg.ResetDayMethod('Mod. Following')
    payLeg.PayDayMethod('Mod. Following')
    payLeg.RollingConv('Preserve EOM')

def GBPSwapDefault(ins):
    insDeco=acm.FBusinessLogicDecorator.WrapObject(ins)
    recLeg=insDeco.FirstReceiveLeg()
    payLeg=insDeco.FirstPayLeg()

    if not payLeg.Currency() == 'Float':
        payLeg.LegType('Float')
    payLeg.RollingPeriod('6m')
    
    if not payLeg.Currency().Name()=='GBP':
        payLeg.Currency('GBP')

    insDeco.MtmFromFeed(False)
    insDeco.SpotBankingDaysOffset(0)

    insDeco.LegStartPeriod('0d')
    insDeco.LegEndPeriod('5y')    
        
    recLeg.LegType('Fixed')
    recLeg.RollingPeriod('6m')
    recLeg.DayCountMethod('Act/365')
    recLeg.RollingConv('Preserve EOM')
    recLeg.PayDayMethod('Mod. Following')
    
    payLeg.ResetDayMethod('Mod. Following')
    payLeg.ResetDayOffset(0)
    payLeg.PayDayMethod('Mod. Following')
    payLeg.RollingConv('Preserve EOM')

def JPYSwapDefault(ins):
    insDeco=acm.FBusinessLogicDecorator.WrapObject(ins)
    recLeg=insDeco.FirstReceiveLeg()
    payLeg=insDeco.FirstPayLeg()

    if not payLeg.Currency() == 'Float':
        payLeg.LegType('Float')
    payLeg.RollingPeriod('6m')
    
    if not payLeg.Currency().Name()=='JPY':
        payLeg.Currency('JPY')
    
    insDeco.MtmFromFeed(False)
    insDeco.SpotBankingDaysOffset(2)
    
    insDeco.LegStartPeriod('0d')
    insDeco.LegEndPeriod('5y')
    
    recLeg.LegType('Fixed')
    recLeg.RollingPeriod('6m')
    recLeg.DayCountMethod('Act/365')
    recLeg.RollingConv('Preserve EOM')
    recLeg.PayDayMethod('Mod. Following')
    recLeg.Pay2Calendar(GBPCalendar)
        
    payLeg.ResetDayMethod('Mod. Following')
    payLeg.PayDayMethod('Mod. Following')
    payLeg.Pay2Calendar(GBPCalendar)
    payLeg.ResetCalendar(GBPCalendar)
    payLeg.RollingConv('Preserve EOM')
    

def USDSwapDefault(ins):
    insDeco=acm.FBusinessLogicDecorator.WrapObject(ins)
    recLeg=insDeco.FirstReceiveLeg()
    payLeg=insDeco.FirstPayLeg()
    
    if not payLeg.Currency() == 'Float':
        payLeg.LegType('Float')
    payLeg.RollingPeriod('3m')
    
    if not payLeg.Currency().Name()=='USD':
        payLeg.Currency('USD')
    
    insDeco.MtmFromFeed(False)
    insDeco.SpotBankingDaysOffset(2)

    insDeco.LegStartPeriod('0d')
    insDeco.LegEndPeriod('5y')
    
    recLeg.LegType('Fixed')
    recLeg.RollingPeriod('6m')
    recLeg.DayCountMethod('30/360')
    recLeg.RollingConv('Preserve EOM')
    recLeg.PayDayMethod('Mod. Following')
    recLeg.Pay2Calendar(GBPCalendar)


    payLeg.ResetDayMethod('Mod. Following')
    payLeg.PayDayMethod('Mod. Following')
    payLeg.Pay2Calendar(GBPCalendar)
    payLeg.ResetCalendar(GBPCalendar)
    payLeg.RollingConv('Preserve EOM')
    
def ZARSwapDefault(ins):
    insDeco=acm.FBusinessLogicDecorator.WrapObject(ins)
    recLeg=insDeco.FirstReceiveLeg()
    payLeg=insDeco.FirstPayLeg()

    if not payLeg.Currency() == 'Float':
        payLeg.LegType('Float')
    payLeg.RollingPeriod('3m')
    payLeg.RollingConv('None')
    
    if not payLeg.Currency().Name()=='ZAR':
        payLeg.Currency('ZAR')
    
    insDeco.MtmFromFeed(False)
    insDeco.SpotBankingDaysOffset(0)
    
    insDeco.LegStartPeriod('0d')
    insDeco.LegEndPeriod('5y')
    
    recLeg.LegType('Fixed')
    recLeg.RollingPeriod('3m')
    recLeg.DayCountMethod('Act/365')
    recLeg.RollingConv('None')
    recLeg.PayDayMethod('Mod. Following')
    
    payLeg.ResetDayMethod('Mod. Following')
    payLeg.PayDayMethod('Mod. Following')
    payLeg.ResetDayOffset(0)
