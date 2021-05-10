
import acm
import ael
from DealPackageDevKit import Object, ReturnDomainDecorator, AcquirerChoices, PortfolioChoices, CounterpartyChoices
from DealPackageTradeActionBase import TradeActionBase
from DealPackageUtil import SetStatus, CreateCleanPackageCopy

class TradeActionMirror(TradeActionBase):

    counterparty =      Object( objMapping = "MirrorTrades.Counterparty",
                                label = "Mirror Cpty",
                                choiceListSource = CounterpartyChoices())
    
    acquirer =          Object( objMapping = "MirrorTrades.Acquirer",
                                label = "Mirror Acquirer",
                                choiceListSource = AcquirerChoices())
    
    portfolio =         Object( objMapping = "MirrorTrades.Portfolio",
                                label = "Mirror Portfolio",
                                choiceListSource = PortfolioChoices())
    
    updatedOriginalTrades = Object( domain = 'FArray',
                                    defaultValue = acm.FArray())
    
    # ------- #
    # Dev Kit #
    # ------- #
    def AssemblePackage(self, arguments):
        self._args = arguments
        origDp = arguments.At('dealPackage')
        origEdit = origDp.Edit()
        self._origEdit = origEdit
        mirrorDp = CreateCleanPackageCopy(self.OriginalDealPackage(), fromOriginator=True)
        self.TouchTradeTime(mirrorDp.AllOpeningTrades())
        self.DealPackage().AddChildDealPackage(mirrorDp, 'mirror')
        
    def OnNew(self):
        SetStatus(self.MirrorDealPackage(), self._args)
        self.ResetTradeTimes()
        self.SetMirrorQuantities()
        self.SetDefaultMirrorValues()
        self.SetTransactionReferences()
        self.MirrorHook(self.GetMirrorHook())
        self.SendTradesToMirrorHook()

    def OpenAfterSave(self, config):
        return self.MirrorDealPackage()

    def CustomPanes(self):
    
        return [{'Mirror':"""
                        vbox(;
                            counterparty;
                            acquirer;
                            portfolio;
                            );
                        """}]

    def OnSave(self, saveConfig):
        saveConfig.InstrumentPackage('Exclude')
        super(TradeActionMirror, self).OnSave(saveConfig)
        if len(self.updatedOriginalTrades) > 0:
            return {'commit': self.updatedOriginalTrades}

    # ------------------------------------------- #
    # Methods for setting mirror trade attributes #
    # ------------------------------------------- #
    def SetMirrorQuantities(self):
        quantityAttr = self._args.At('quantityAttr', None)
        if quantityAttr:
            self.MirrorDealPackage().SetAttribute(quantityAttr, -self.OriginalDealPackage().GetAttribute(quantityAttr))
        else:
            mirrorTrades = self.MirrorTrades()
            originalTrades = self.OriginalTrades()
            for i in range(0, len(mirrorTrades)):
                mirrorTrades.At(i).Quantity(-originalTrades.At(i).Quantity())

    def SetDefaultMirrorValues(self):
        mirrorTrades = self.MirrorTrades()
        originalTrades = self.OriginalTrades()
        for i in range(0, len(mirrorTrades)):
            #mirrorTrades.At(i).Quantity(-originalTrades.At(i).Quantity())
            mirrorTrades.At(i).Counterparty(originalTrades.At(i).Acquirer())
            mirrorTrades.At(i).Acquirer(self.CheckAndGetAcquirer(originalTrades.At(i).Counterparty()))
            mirrorTrades.At(i).Portfolio(None)

    def SetTransactionReferences(self):
        mirrorTrades = self.MirrorTrades()
        originalTrades = self.OriginalTrades()
        for i in range(0, len(mirrorTrades)):
            trxReference = self.GetTransactionReference(originalTrades.At(i))
            mirrorTrades.At(i).TrxTrade(trxReference)
            if originalTrades.At(i).TrxTrade() is None:
                originalTrades.At(i).TrxTrade(trxReference)
                self.updatedOriginalTrades.Add(originalTrades.At(i))

    def TouchTradeTime(self, mirrorTrades):
        for i in range(0, len(mirrorTrades)):
            mirrorTrades.At(i).TradeTime(acm.Time.TimeNow())

    def ResetTradeTimes(self):
        mirrorTrades = self.MirrorTrades()
        originalTrades = self.OriginalTrades()
        for i in range(0, len(mirrorTrades)):
            mirrorTrades.At(i).TradeTime(originalTrades.At(i).TradeTime())
            mirrorTrades.At(i).ValueDay(originalTrades.At(i).ValueDay())
            mirrorTrades.At(i).AcquireDay(originalTrades.At(i).AcquireDay())
        
    def SendTradesToMirrorHook(self):
        if self.MirrorHook() is not None:
            mirrorTrades = self.MirrorTrades()
            originalTrades = self.OriginalTrades()
            for i in range(0, len(mirrorTrades)):
                self.CallMirrorHook(originalTrades.At(i), mirrorTrades.At(i))
    
    # ------------ #
    # Help methods #
    # ------------ #
    def CheckAndGetAcquirer(self, party):
        acqChoices = self.DealPackage().GetAttributeMetaData('acquirer', 'choiceListSource')().GetChoiceListSource()
        return party if party in acqChoices else None

    def CallMirrorHook(self, origTrade, mirrorTrade):
        self.MirrorHook()(self.AsAelTrade(origTrade), self.AsAelTrade(mirrorTrade))

    def OriginalDealPackage(self):
        return self._origEdit

    def OriginatorPackage(self):
        return self.OriginalDealPackage().Originator()

    def MirrorDealPackage(self):
        return self.DealPackage().ChildDealPackageAt('mirror')

    def MirrorTrades(self):
        return self.MirrorDealPackage().AllOpeningTrades()

    def OriginalTrades(self):
        return self.OriginalDealPackage().AllOpeningTrades()

    def GetMirrorHook(self):
        try:
            import FMirror
        except ImportError:
            return None
        return getattr(FMirror, 'mirrored_trade', None)

    def MirrorHook(self, value = 'Reading'):
        if value == 'Reading':
            return self._mirrorHook
        else:
            self._mirrorHook = value

    def AsAelTrade(self, acmTrade):
        return ael.Trade[acmTrade.Oid()]

    def GetTransactionReference(self, originalTrade):
        if originalTrade.TrxTrade() is None:
            return originalTrade.Originator()
        else:
            return originalTrade.TrxTrade()
