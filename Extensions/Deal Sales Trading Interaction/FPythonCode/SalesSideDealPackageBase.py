
import acm
from DealPackageDevKit import Delegate, NoTradeActions, Settings, DealPackageDefinition, DealPackageException, DealPackageUserException
from DealPackageUtil import UnpackPaneInfo, UnDecorate, CreateCleanPackageCopy, SetNewInstrument, SetNewTrade
from RFQUtils import Misc, MethodDirection, Validation, Amount
from TradeCreationUtil import TradeCreation, TradeCreationUtil
from SalesTradingCustomizations import Limits

DELEGATED_DP_NAME = 'delegatedDP'
DELEGATED_TRADE_NAME = 'delegatedTrade'

@NoTradeActions
@Settings( GraphApplicable=False,
           SheetApplicable=False )
           

class SalesSideDealPackageBase(DealPackageDefinition):        
    
    delegatedDP        = Delegate(  attributeMapping='DelegatedDealPackage', 
                                    enabled='@DelegatedDealPackageSectionEnabled',
                                    customPanes='@DealPackageCustomPanes')

    '''***********************************************************************************************
    * Deal Package interface
    ***********************************************************************************************'''    
    def OnInit(self, *args, **kwargs):
        self._delegatedDP = None
        self._delegatedTrade = None
        self._reOpening = False
        self._originalObject = None
        self._isSaved = False
    
    def SetNew(self, trade, dealPackage):
        if not self.ReOpening():
            trades = []
            if dealPackage and self.DealPackagePersisted(dealPackage):
                dealPackage = CreateCleanPackageCopy(dealPackage)
                trades = dealPackage.Trades()
            elif trade:
                if trade.StorageId() > 0:
                    trade = trade.StorageImage()
                SetNewTrade(acm.FBusinessLogicDecorator.WrapObject(UnDecorate(trade), self.DealPackage().GUI()), True)
                trades = [trade]
            if trades:
                TradeCreationUtil.SetAddInfoOnTrades(trades, 'SalesOrderId', '')
                TradeCreationUtil.SetAddInfoOnTrades(trades, 'QuoteRequestId', '')
        return trade, dealPackage
    
    def SetOriginalObject(self, trade, dealPackage):
        if not self._originalObject: # Already set if initiated from IM Object
            if dealPackage and dealPackage.Originator().StorageId() > 0:
                self._originalObject = dealPackage.Originator()
            elif dealPackage and dealPackage.IsDeal():
                self._originalObject = dealPackage.Trades().First().Originator() if self.DealPackagePersisted(dealPackage) else None
            elif trade and trade.Originator().StorageId() > 0:
                self._originalObject = trade.Originator()
        
    def AssemblePackage(self, arguments):    
        trade = dealPackage = None
        content = arguments.At('content')
        if arguments.At('reOpening') is not None:
            self._reOpening = arguments.At('reOpening')
        wrapDeal = arguments.At('wrapDeal') if arguments.At('wrapDeal') is not None else True
        if arguments.At('imObject'):
            trade, dealPackage = self.TradeOrDealPackageFromImObject(arguments.At('imObject'), wrapDeal)
        else:
            dealPackage = Misc.FindDealPackage(content, self.DealPackage().GUI(), True, wrapDeal)
            if not dealPackage:
                trade = Misc.FindTrade(content, self.DealPackage().GUI())
        self.SetOriginalObject(trade, dealPackage)
        trade, dealPackage = self.SetNew(trade, dealPackage)
        self.DelegatedDealPackage(dealPackage)        
        self.DelegatedTrade(trade)
        if not self.DelegatedDealPackage() and not self.DelegatedTrade():
            raise DealPackageUserException('Could not assemble package: No trade or dealpackage found.')

    '''***********************************************************************************************
    * Init
    ***********************************************************************************************''' 
    def TradeOrDealPackageFromImObject(self, imObject, wrapDeal):
        trade = None
        dealPackage = Misc.FindDealPackageFromImObject(imObject, self.DealPackage().GUI(), True, wrapDeal)
        if not dealPackage:
            trade = Misc.FindTradeFromImObject(imObject, self.DealPackage().GUI())
        return trade, dealPackage

    def Arguments(self, input):
        try:
            content = input['content']
            reOpening = input['reOpening']
        except:
            arguments = acm.FDictionary()
            arguments.AtPut('content', input)
            arguments.AtPut('reOpening', False)
        else:
            arguments = acm.FDictionary()
            arguments.AddAll(input)
        return arguments

    '''***********************************************************************************************
    * Object mappings
    ***********************************************************************************************'''     
    def DelegatedDealPackageAttribute(self):
        return self.delegatedDP
        
    def DelegatedTrade(self, trade = MethodDirection.asGetMethod):
        if trade == MethodDirection.asGetMethod:
            delegatedTrade = Misc.GetTradeFromDealPackage(self.DelegatedDealPackage())
            if not delegatedTrade:
                delegatedTrade = self._delegatedTrade
            return delegatedTrade
        else:
            self.AddTradeAt(trade)
            
    def DelegatedDealPackage(self, dealPackage = MethodDirection.asGetMethod):
        if dealPackage == MethodDirection.asGetMethod:
            #try:
            #    delegatedDP = self.DealPackage().ChildDealPackageAt(DELEGATED_DP_NAME)
            #except:
            #    pass
            return self._delegatedDP
        else:
            self.AddChildDealPackageAt(dealPackage)
    
    def ReOpening(self):
        return self._reOpening
    
    def OriginalObject(self):
        return self._originalObject

    '''***********************************************************************************************
    * Save
    ***********************************************************************************************'''
    def IsSaved(self, val = MethodDirection.asGetMethod):
        if MethodDirection.AsGetMethod(val):
            return self._isSaved
        else:
            self._isSaved = val
    
    def CheckLimits(self, *args):
        limitsOk = True
        if self.CheckLimitsRequired():
            self.Save()
            limitsOk = False
            dialogCb = self.GetAttribute('uxCallbacks').At('dialog')
            if dialogCb:
                dpDef = acm.GetDefaultContext().GetExtension(acm.FDealPackageDefinition, acm.FObject, 'CheckLimits')
                if dpDef is None:
                    raise DealPackageUserException("Cannot perform limit checks, no FDealPackageDefinition 'CheckLimits' exists.") 
                limitsDp = acm.DealPackage.NewAsDecorator('CheckLimits', self.DealPackage().GUI(), [self.DelegatedTrade(), self.DelegatedDealPackage()])
                limitsOk = dialogCb(limitsDp, 'result')
        return limitsOk

    def DealPackageToBeSaved(self):
        if self.ShouldCreateCleanCopy():
            dp = CreateCleanPackageCopy(self.DelegatedDealPackage())
            dp.Refresh()
        else:
            dp = self.DelegatedDealPackage()
        self.UpdateTradeTimes(dp)
        self.SetPreDealTradeStatus(dp)
        return dp
    
    def TradeToBeSaved(self):
        if self.ShouldCreateCleanCopy():
            trade = self.DelegatedTrade().StorageNew()
        else:
            trade = self.DelegatedTrade()
        self.UpdateTradeTimes(trade)
        self.SetPreDealTradeStatus(trade)
        return trade
    
    def ShouldCreateCleanCopy(self):
        return self.HasOriginator() and self.CreateTradesOnRequest() and (self.CreateNewInsAndTradeCreationHandling() or self.CreateNewTradeCreationHandling())
    
    def NewDelegatedDealPackage(self, package, gui):
        package = UnDecorate(package)
        if package.IsDeal():
            trade = package.Trades().First()
            ins = package.Instruments().First()
            tradeOrIns = trade if trade.Originator().StorageId() > 0 else ins
            dealType = package.DefinitionName()          
            newDp = acm.Deal().WrapAsDecorator(tradeOrIns.Originator(), gui, dealType)
        else:
            if package.IsKindOf(acm.FInstrumentPackage):
                newDp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(package.Originator(), gui)
            else:
                newDp = acm.FBusinessLogicDecorator.WrapObject(package.Originator(), gui).Edit()
        return newDp
    
    def InitializeInstrumentPackage(self):
        dp = self.DelegatedDealPackage()
        insOrIp = dp.Instruments().First() if dp.IsDeal() else dp.InstrumentPackage()
        insOrIp.Name('')
        if dp.IsDeal():
            dp.Instruments().First().InitializeUniqueIdentifiers()
    
    def CreateSaveConfig(self):
        dp = self.DelegatedDealPackage()
        saveConfig = acm.FDealPackageSaveConfiguration()
        if not self.InstrumentPackagePersisted(self.DelegatedDealPackage()):
            saveConfig.InstrumentPackage('SaveNew')
        elif self.CreateNewInsAndTradeCreationHandling():
            self.InitializeInstrumentPackage()
            saveConfig.InstrumentPackage('SaveNew')
        else:
            saveConfig.InstrumentPackage('Exclude')
    
        if self.CreateTradesOnRequest():
            saveConfig.DealPackage('Save')
        else:
            saveConfig.DealPackage('Exclude')
        return saveConfig
    
    def CheckLimitsRequired(self):
        return Limits.CheckLimitsRequired(self.DelegatedTrade(), self.DelegatedDealPackage())
    
    def CreateTradesOnRequest(self):
        return TradeCreationUtil.CreateTradesOnRequest(self.DelegatedTrade(), self.DelegatedDealPackage())

    def SetPreDealTradeStatus(self, dpOrTrade):
        preDealStatus = 'Simulated'
        if hasattr(dpOrTrade, 'GetAttribute'):
            statusAttr = dpOrTrade.GetAttribute('salesTradingInteraction').At('statusAttr')
            if statusAttr:
                status = dpOrTrade.GetAttribute('salesTradingInteraction').At('preDealStatus')
                if status:
                    preDealStatus = status
                dpOrTrade.SetAttribute(statusAttr, preDealStatus)
        else:
            dpOrTrade.Status(preDealStatus)
            
    def UpdateTradeTimes(self, dpOrTrade):
        if hasattr(dpOrTrade, 'GetAttribute'):
            tradeTimeAttr = dpOrTrade.GetAttribute('salesTradingInteraction').At('tradeTimeAttr')
            if tradeTimeAttr:
                dpOrTrade.SetAttribute(tradeTimeAttr, acm.Time().TimeNow())
        else:
            dpOrTrade.TradeTime(acm.Time().TimeNow())
    
    def InstrumentPackagePersisted(self, dp):
        isDeal = dp.IsDeal()
        iOrig = dp.Instruments().First().Originator() if isDeal else dp.InstrumentPackage().Originator()
        ipId = iOrig.StorageId()
        return ipId > 0
    
    def DealPackagePersisted(self, dp):
        isDeal = dp.IsDeal()
        tOrig = dp.Trades().First().Originator() if isDeal else dp.Originator()
        dpId = tOrig.StorageId()
        return dpId > 0
    
    def DealPackageOrInstrumentPackagePersisted(self):
        return self.InstrumentPackagePersisted(self.DelegatedDealPackage()) or self.DealPackagePersisted(self.DelegatedDealPackage())
    
    def ShouldSaveDelegatedDealPackage(self):
        return not self.ManualTradeCreationHandling()
    
    def SaveNewDelegatedTradeAndInstrument(self):
        successfulSave = True
        if not self.DelegatedDealPackage():
            try:
                trade = self.TradeToBeSaved()
                if trade.Instrument().Originator().StorageId() < 0:
                    trade.Instrument().Commit()
                    trade.Instrument(trade.Instrument().Originator())
                if self.CreateTradesOnRequest():
                    trade.Commit()
                    trdDeco = acm.FBusinessLogicDecorator.WrapObject(trade.Originator().StorageImage(), self.DealPackage().GUI())
                    self.DelegatedTrade(trdDeco)
            except Exception as e:
                successfulSave = False
                errorStr = 'Save New Failed: ' + str(e)
                raise DealPackageUserException(errorStr)
            Validation.Instrument(self.DelegatedTrade().Instrument())
        return successfulSave

    def SaveNewDelegatedDealPackage(self):
        successfulSave = True
        try:
            if self.DelegatedDealPackage() and self.ShouldSaveDelegatedDealPackage():
                gui = self.DelegatedDealPackage().GUI()
                saveConfig = self.CreateSaveConfig()
                dp = self.DealPackageToBeSaved()
                newPackage = dp.Save(saveConfig).First()
                self._UpdateDelegations()
                newDp = self.NewDelegatedDealPackage(newPackage, gui)
                self.DelegatedDealPackage(newDp)
        except Exception as e:
            successfulSave = False
            errorStr = 'Save New Failed: ' + str(e)
            raise DealPackageUserException(errorStr)
        return successfulSave
    
    def Save(self):
        self.SaveNewDelegatedTradeAndInstrument() and self.SaveNewDelegatedDealPackage()
        self.IsSaved(True)
    
    '''***********************************************************************************************
    * Attribute overrides
    ***********************************************************************************************''' 
    def SetAttributeOnDelegatedDealPackage(self, attrKey, val):
        if not self.ManualTradeCreationHandling():
            attrName = self.DelegatedDealPackage().GetAttribute('salesTradingInteraction').At(attrKey)
            if attrName:
                self.DelegatedDealPackage().SetAttribute(attrName, val)
                
    def OnClientChanged(self, attributeName, oldValue, newValue, *args):
        if self.DelegatedDealPackage():
            self.SetAttributeOnDelegatedDealPackage('clientAttr', newValue)
        elif self.DelegatedTrade():
            self.DelegatedTrade().Counterparty(newValue)
        
    def OnPortfolioChanged(self, attributeName, oldValue, newValue, *args):
        if self.DelegatedDealPackage():
            self.SetAttributeOnDelegatedDealPackage('portfolioAttr', newValue)
        elif self.DelegatedTrade():
            self.DelegatedTrade().Portfolio(newValue)
    
    def OnQuantityChanged(self, attributeName, oldValue, newValue, *args):
        dp = self.DelegatedDealPackage()
        trade = self.DelegatedTrade()
        if dp and (not dp.IsDeal() or Amount.UseQuantity(trade.Instrument(), dp)):
            if not self.ManualTradeCreationHandling():
                amountInfo = self.DelegatedDealPackage().GetAttribute('salesTradingInteraction').At('amountInfo')
                if amountInfo:
                    self.DelegatedDealPackage().SetAttribute(amountInfo['amountAttr'], newValue)
        elif not dp and trade and Amount.UseQuantity(trade.Instrument(), None):
            self.DelegatedTrade().Quantity(newValue)
        
    def OnNominalChanged(self, attributeName, oldValue, newValue, *args):
        dp = self.DelegatedDealPackage()
        trade = self.DelegatedTrade()
        # Nominal should only be set on deals, regular deal packages only use the quantity
        if dp and dp.IsDeal() and not Amount.UseQuantity(trade.Instrument(), dp):
            if not self.ManualTradeCreationHandling():
                amountInfo = self.DelegatedDealPackage().GetAttribute('salesTradingInteraction').At('amountInfo')
                if amountInfo:
                    self.DelegatedDealPackage().SetAttribute(amountInfo['amountAttr'], newValue)
        elif not dp and trade and not Amount.UseQuantity(trade.Instrument(), None):
            self.DelegatedTrade().Nominal(newValue)
    
    def OnNewInsAndTradeAction(self, *args):
        trade = self.DelegatedTrade()
        dp = self.DelegatedDealPackage()
        if dp:
            if dp.IsDeal():
                ins = dp.Instruments().First().Originator()
                ins = ins.StorageImage()
                SetNewInstrument(ins, True)
                dp = acm.Deal.WrapAsDecorator(ins, dp.GUI())
            else:
                dp = acm.DealPackage.NewAsDecorator(dp.DefinitionName(), dp.GUI())
            self.AddChildDealPackageAt(dp)
        elif trade:
            raise DealPackageUserException('Not possible to create new instrument if not wrapped in a Deal')
        self.IsSaved(False)
    
    def OnNewTradeAction(self, *args):
        trade = self.DelegatedTrade()
        dp = self.DelegatedDealPackage()
        if dp:
            if dp.IsDeal():
                dp = acm.Deal.WrapAsDecorator(dp.Instruments().First().Originator(), dp.GUI())
            else:
                dp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(dp.Originator().InstrumentPackage(), dp.GUI())
            self.AddChildDealPackageAt(dp)
        elif trade:
            gui = trade.GUI()
            trade = acm.DealCapturing.CreateNewTrade(trade.Originator().Instrument())
            trade = acm.FBusinessLogicDecorator.WrapObject(trade, gui)
            self.AddTradeAt(trade)
        self.IsSaved(False)
    
    '''***********************************************************************************************
    * Misc.
    ***********************************************************************************************'''    
    def IsOnDealPackage(self):
        return self.DelegatedDealPackage() != None and not self.DelegatedDealPackage().IsDeal()
        
    def AddChildDealPackageAt(self, dp):
        if self.DelegatedDealPackage():
            self.DealPackage().RemoveChildDealPackage(self.DelegatedDealPackage(), False)
        if dp:
            self._delegatedDP = dp
            self.DealPackage().AddChildDealPackage(dp, DELEGATED_DP_NAME)
            dp.RefreshNeeded(True)
        self._UpdateDelegations() 
    
    def AddTradeAt(self, trade):
        if self.DelegatedTrade():
            self.DealPackage().RemoveTrade(self.DelegatedTrade())
        if trade:
            self._delegatedTrade = trade   
            self.DealPackage().AddTrade(trade, DELEGATED_TRADE_NAME)              
    
    def HasOriginator(self):
        originator = self.DelegatedTrade().Originator() if not self.IsOnDealPackage() else self.DelegatedDealPackage().Originator()
        return originator.StorageId() > 0 
    
    def TradeCreationSetting(self):
        raise DealPackageException('Override in child class')
    
    def ManualTradeCreationHandling(self):
        return self.TradeCreationSetting() == TradeCreation.Manual(self.IsOnDealPackage())
    
    def UpdateTradeCreationHandling(self):
        return self.TradeCreationSetting() == TradeCreation.Update(self.IsOnDealPackage())
    
    def CreateNewInsAndTradeCreationHandling(self):
        return self.TradeCreationSetting() == TradeCreation.CreateNewInsAndTrade(self.IsOnDealPackage())
    
    def CreateNewTradeCreationHandling(self):
        return self.TradeCreationSetting() == TradeCreation.CreateNewTrade(self.IsOnDealPackage())
    
    '''***********************************************************************************************
    * Enabled callbacks
    ***********************************************************************************************'''                                                     
    def DelegatedDealPackageSectionEnabled(self, attrName):
        raise DealPackageException('Override in base class')

    '''***********************************************************************************************
    * UX Layout
    ***********************************************************************************************'''     
    def CustomPanesName(self):
        raise DealPackageException('Override in base class')
        
    def DealPackageCustomPanes(self):
        return Misc.DealPackageCustomPanes(self.DelegatedDealPackage(), self.GetCustomPanesFromExtValue, 'salesCustomPane')
        
    def CustomPanes(self):
        if self.DelegatedDealPackage():
            tabControls = self.DelegatedDealPackageAttribute().GetLayout()
            tabCtrlName, tabCtrlLayout = UnpackPaneInfo(tabControls[0])
            tabName, paneLayout = UnpackPaneInfo(tabCtrlLayout[0])
            
            panes = self.GetCustomPanesFromExtValue(self.CustomPanesName())
            key = list(panes[0].keys())[0]
            panes[0][key] = paneLayout + panes[0][key]
        else:
            panes = self.GetCustomPanesFromExtValue(self.CustomPanesName())
        return panes


        
        
