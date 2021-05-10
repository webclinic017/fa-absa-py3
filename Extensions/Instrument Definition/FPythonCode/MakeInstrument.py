import acm
import FUxCore

class MakeInstrument():

    def Label(self):
        raise RuntimeError('Label not implemented')    
        
    def Applicable(self, instrumentOrTrade):
        raise RuntimeError('Applicable not implemented')
    
    def Invoke(self, instrumentOrTrade):
        raise RuntimeError('Invoke not implemented')
        
    def Instrument(self, instrumentOrTrade):
        instrument = None
        if instrumentOrTrade.IsKindOf('FInstrument'):
            instrument = instrumentOrTrade
        elif instrumentOrTrade.IsKindOf('FTrade'):
            instrument = instrumentOrTrade.Instrument()
        return instrument
        
    def Trade(self, instrumentOrTrade):
        return instrumentOrTrade if instrumentOrTrade.IsKindOf('FTrade') else None
        
    def IsApplicationInProfile(self):
        return acm.User().IsAllowed(self.Label(), 'Application')
    
        
class MakeInstrumentMenu(FUxCore.SubMenu):
    def __init__(self, extObj):
        self.m_extObj = extObj
        self.m_items = acm.FDictionary()
        self.RegisterItems()

    def RegisterItems(self):
        self.AddItem(MakeOption())
        self.AddItem(MakeSwap())
        self.AddItem(MakeDeposit())
        self.AddItem(MakeCDS())
        self.AddItem(MakeBasketCDS())
        self.AddItem(MakeTRS())
        self.AddItem(MakeCurrencySwap())
        self.AddItem(MakeCollateral())
        self.AddItem(MakeSecurityLoan())
        self.AddItem(MakeBuySellback())
        self.AddItem(MakeRepo())
        self.AddItem(MakeFVA())
        self.RegisterCustomItems()
    
    def RegisterCustomItems(self):
        import FCustomMakeInstrument
        customItems = FCustomMakeInstrument.CustomMakeInstrumentItems()
        for customItem in customItems:
            self.AddItem(customItem)

    def AddItem(self, item):
        self.m_items[item.Label()] = item
        
    def Items(self):
        return self.m_items
        
    def ExtensionObject(self, extensionObject):
        if hasattr(extensionObject, '__len__'):
            extensionObject = extensionObject[0]
        instrumentOrTrade = extensionObject
        if hasattr(extensionObject, 'OriginalInstrument'):
            instrument = extensionObject.OriginalInstrument()
            if instrument:
                instrumentOrTrade = instrument
        if hasattr(extensionObject, 'OriginalTrade'):
            trade = extensionObject.OriginalTrade()
            if trade:
                instrumentOrTrade = trade
        instrumentOrTrade = instrumentOrTrade.Originator()
        return instrumentOrTrade
        
    def Invoke(self, eii):
        menu = acm.FUxMenu()
        instrumentOrTrade = self.ExtensionObject(eii.ExtensionObject())
        result = None
        items = self.Items()
        labels = items.Keys().Sort()
        for label in labels:
            item = items[label]
            if item.Applicable(instrumentOrTrade):
                menu.AddItem( item.Invoke, instrumentOrTrade, item.Label())
                result = menu
        return result
    
    def Applicable(self):
        result = False

        instrumentOrTrade = self.ExtensionObject(self.m_extObj)
        items = self.Items()
        for item in items.Values():
            if item.Applicable(instrumentOrTrade):
                result = True
                break
                
        return result
        
    def Enabled(self):
        return True


def CreateMenu(extObj):
    return MakeInstrumentMenu(extObj)

        
class MakeOption(MakeInstrument):
    
    def Label(self):
        return 'Make Option'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeOptionInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        ins = self.Instrument(instrumentOrTrade)
        return self.IsApplicationInProfile() and ins and ins.IsValidAsUnderlying('Option')
        
class MakeSwap(MakeInstrument):
    
    def Label(self):
        return 'Make Swap'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeSwapInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
        
    def Applicable(self, instrumentOrTrade):
        applicable = False
        ins = self.Instrument(instrumentOrTrade)
        if ins:
            if 'Deposit' == ins.InsType():
                applicable = True
            elif ins.IsSecurity():
                applicable = 'Stock' != ins.InsType() and 'Commodity' != ins.InsType()
        return self.IsApplicationInProfile() and applicable
        
class MakeDeposit(MakeInstrument):
    
    def Label(self):
        return 'Make Deposit'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeDepositInitData(self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        applicable = False
        ins = self.Instrument(instrumentOrTrade)
        trade = self.Trade(instrumentOrTrade)
        if trade:
            applicable = 'Certificate' != ins.InsType() and 'Curr' != ins.InsType() and 'Average Future/Forward' != ins.InsType()
        return self.IsApplicationInProfile() and applicable
        
class MakeCDS(MakeInstrument):
    
    def Label(self):
        return 'Make Credit Def Swap'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeCDSInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        applicable = False
        ins = self.Instrument(instrumentOrTrade)
        if ins:
            applicable = 'Bond' == ins.InsType() or 'Convertible' == ins.InsType()
        return self.IsApplicationInProfile() and applicable
        
class MakeBasketCDS(MakeInstrument):
    
    def Label(self):
        return 'Make Basket CDS'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeBasketCDSInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        applicable = False
        ins = self.Instrument(instrumentOrTrade)
        if ins:
            applicable = 'Combination' == ins.InsType() or 'CreditIndex' == ins.InsType()
        return self.IsApplicationInProfile() and applicable
        
class MakeTRS(MakeInstrument):
    
    def Label(self):
        return 'Make Total Return Swap'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeTRSInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        applicable = False
        ins = self.Instrument(instrumentOrTrade)
        if ins:
            applicable = 'Bond' == ins.InsType() or 'FRN' == ins.InsType()
        return self.IsApplicationInProfile() and applicable
        
class MakeCurrencySwap(MakeInstrument):
    
    def Label(self):
        return 'Make Curr Swap'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeCurrencySwapInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        applicable = False
        ins = self.Instrument(instrumentOrTrade)
        if ins and ins.IsSecurity():
            applicable = 'Stock' != ins.InsType() and 'Commodity' != ins.InsType() and 'FreeDefCF' != ins.InsType()
        return self.IsApplicationInProfile() and applicable
        
class MakeCollateral(MakeInstrument):
    
    def Label(self):
        return 'Make Collateral'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeCollateralInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        applicable = False
        ins = self.Instrument(instrumentOrTrade)
        if ins:
            applicable = ins.IsSecurity() or 'CD' == ins.InsType()
        return self.IsApplicationInProfile() and applicable
        
class MakeSecurityLoan(MakeInstrument):
    
    def Label(self):
        return 'Make Security Loan'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeSecurityLoanInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        ins = self.Instrument(instrumentOrTrade)
        applicable = ins and ins.IsSecurity()
        return self.IsApplicationInProfile() and applicable
        
class MakeBuySellback(MakeInstrument):
    
    def Label(self):
        return 'Make Buy-Sellback'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeBuySellbackInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        ins = self.Instrument(instrumentOrTrade)
        applicable = ins and ins.IsSecurity()
        return self.IsApplicationInProfile() and applicable
        
class MakeRepo(MakeInstrument):
    
    def Label(self):
        return 'Make Repo/Reverse'
       
    def Invoke(self, instrumentOrTrade):
        initData = acm.DealCapturingUX.MakeRepoInitData(self.Instrument(instrumentOrTrade), self.Trade(instrumentOrTrade))
        acm.StartApplication('Instrument Definition', initData)
    
    def Applicable(self, instrumentOrTrade):
        ins = self.Instrument(instrumentOrTrade)
        applicable = ins and ins.IsSecurity()
        return self.IsApplicationInProfile() and applicable
        
class MakeFVA(MakeInstrument):
    
    def Label(self):
        return 'Make FVA'
     
    def Invoke(self, instrumentOrTrade):
        future = acm.DealCapturing().CreateNewInstrument('Future/Forward')
        decorator = acm.FBusinessLogicDecorator.WrapObject(future)
        decorator.Underlying = self.Instrument(instrumentOrTrade)
        if decorator.Quotation() not in decorator.DefaultQuotations():
            decorator.Quotation('Per Contract')
        acm.StartApplication('Instrument Definition', future)
    
    def Applicable(self, instrumentOrTrade):
        ins = self.Instrument(instrumentOrTrade)
        return self.IsApplicationInProfile() and ins and ins.IsForwardStartingFxStraddle()
