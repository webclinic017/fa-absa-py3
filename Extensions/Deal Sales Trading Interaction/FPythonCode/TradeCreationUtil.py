import acm
from DealPackageUtil import UnDecorate
from SalesTradingCustomizations import TradeCreation as TradeCreationCustomizations
from SalesTradingCustomizations import Limits
from DealPackageDevKit import DealPackageUserException    

class TradeCreation(object):  
    createNewInsAndTrade = 0
    createNewTrade = 1
    update = 2
    manual = 3
    
    @staticmethod
    def TradeSettingDict(isOnDp):
        names = TradeCreationCustomizations.TradeSettingDisplayNames(isOnDp)
        return { names[0] : TradeCreation.createNewInsAndTrade,
                 names[1] : TradeCreation.createNewTrade,
                 names[2] : TradeCreation.update,
                 names[3] : TradeCreation.manual
               }
    
    @staticmethod
    def Names(isOnDp):
        return TradeCreation.TradeSettingDict(isOnDp).keys()
    
    @staticmethod
    def EnumValues(isOnDp):
        return TradeCreation.TradeSettingDict(isOnDp).values()
    
    @staticmethod
    def EnumValue(tradeSettingName, isOnDp):
        return TradeCreation.TradeSettingDict(isOnDp)[tradeSettingName]
    
    @staticmethod
    def TradeSettingName(enumValue, isOnDp):
        for k, v in TradeCreation.TradeSettingDict(isOnDp).iteritems():
            if v == enumValue:
                return k
        return None
    
    @staticmethod
    def TradeSettingNames(enumValues, isOnDp):
        f = lambda x : TradeCreation.TradeSettingName(x, isOnDp)
        return map(f, enumValues)
    
    @staticmethod
    def CreateNewInsAndTrade(isOnDp):
        return TradeCreation.TradeSettingName(TradeCreation.createNewInsAndTrade, isOnDp)
    
    @staticmethod
    def CreateNewTrade(isOnDp):
        return TradeCreation.TradeSettingName(TradeCreation.createNewTrade, isOnDp)
    
    @staticmethod
    def Manual(isOnDp):
        return TradeCreation.TradeSettingName(TradeCreation.manual, isOnDp)
    
    @staticmethod
    def Update(isOnDp):
        return TradeCreation.TradeSettingName(TradeCreation.update, isOnDp)

    @staticmethod
    def DefaultValueOverride(isOnDp, isOnOriginalTradeOrDealPackage, multiTradingEnabled, insType, dpType):
        value = None
        tradeSettingName = TradeCreationCustomizations.DefaultValueOverride(isOnOriginalTradeOrDealPackage, multiTradingEnabled, insType, dpType)
        if tradeSettingName:
            value = TradeCreation.EnumValue(tradeSettingName, isOnDp)
        return value
            
    @staticmethod        
    def SettingVisibleInDialog(insType, dealPackageType):
        return TradeCreationCustomizations.SettingVisibleInDialog(insType, dealPackageType)  

class TABTradeCreationSetting(object):
    createNewTrade = 'Create New Trade'
    updateExistingTrade = 'Trade Update'
    manualTradeHanling = 'Update Manually'
    
    @staticmethod
    def FromTradeCreationSetting(tradeCreation, trade, dealPackage):
        tabRule = TABTradeCreationSetting.manualTradeHanling if tradeCreation == TradeCreation.manual else TABTradeCreationSetting.updateExistingTrade
        if tradeCreation in [TradeCreation.createNewInsAndTrade, TradeCreation.createNewTrade]:
            if not TradeCreationUtil.CreateTradesOnRequest(trade, dealPackage):
                tabRule = TABTradeCreationSetting.createNewTrade
        return tabRule    
        
    @staticmethod
    def ToTradeCreationSetting(tabRule):
        tradeCreation = TradeCreation.createNewInsAndTrade
        if tabRule == TABTradeCreationSetting.updateExistingTrade:
            tradeCreation = TradeCreation.update
        elif tabRule == TABTradeCreationSetting.manualTradeHanling:
            tradeCreation = TradeCreation.manual
        return tradeCreation
    
class TradeCreationUtil(object):
    @staticmethod
    def CreateTradesOnRequest(trade, dealPackage):
        checkLimits = Limits.CheckLimitsRequired(trade, dealPackage)
        createTradesOnRequest = checkLimits
        insType = trade.Instrument().InsType() if trade else None
        dealPackageType = dealPackage.DefinitionName() if dealPackage else None
        createTradesOnRequest |= TradeCreationCustomizations.CreateTradesOnRequest(insType, dealPackageType)
        return createTradesOnRequest

    @staticmethod    
    def ValidTradeCreationChoices(trade, dealPackage):
        isOnDp = dealPackage and not dealPackage.IsDeal()
        iOrig = dealPackage.InstrumentPackage().Originator() if isOnDp else trade.Instrument().Originator()
        tOrig = dealPackage.Originator() if isOnDp else trade.Originator()
        multiTradingEnabled = not dealPackage or dealPackage.GetAttribute('multiTradingEnabled')
        choices = TradeCreation.EnumValues(isOnDp)
        if tOrig.StorageId() < 0:
            if iOrig.StorageId() > 0 and multiTradingEnabled:
                choices = [TradeCreation.createNewInsAndTrade, TradeCreation.createNewTrade]
            else:
                choices = [TradeCreation.createNewInsAndTrade]
        elif multiTradingEnabled:
            choices = [TradeCreation.createNewInsAndTrade, TradeCreation.createNewTrade, TradeCreation.update, TradeCreation.manual]     
        else:
            choices = [TradeCreation.createNewInsAndTrade, TradeCreation.update, TradeCreation.manual]
        if not dealPackage:
            if iOrig.StorageId() > 0:
                if TradeCreation.createNewInsAndTrade in choices:
                    choices.remove(TradeCreation.createNewInsAndTrade)
        return TradeCreation.TradeSettingNames(choices, isOnDp)
    
    @staticmethod
    def InitialTradeCreationSetting(trade, dealPackage):
        value = None
        isOnDp = dealPackage and not dealPackage.IsDeal()
        iOrig = dealPackage.InstrumentPackage().Originator() if isOnDp else trade.Instrument().Originator()
        tOrig = dealPackage.Originator() if isOnDp else trade.Originator()
        multiTradingEnabled = not dealPackage or dealPackage.GetAttribute('multiTradingEnabled')
        choices = TradeCreation.EnumValues(isOnDp)
        if tOrig.StorageId() < 0:
            if iOrig.StorageId() > 0 and multiTradingEnabled:
                value = TradeCreation.createNewTrade
            else:
                value = TradeCreation.createNewInsAndTrade
        else:
            value = TradeCreation.update
            
        insType = trade.Instrument().InsType()
        dpType = dealPackage.DefinitionName() if isOnDp else None
        overrideValue = TradeCreation.DefaultValueOverride(isOnDp, tOrig.StorageId() > 0, multiTradingEnabled, insType, dpType)
        if overrideValue:
            value = overrideValue
        value = value if value in choices else choices[0]
        return TradeCreation.TradeSettingName(value, isOnDp)

    @staticmethod
    def SetAddInfoOnTrades(trades, addInfoName, value):
        if value:
            for trade in trades:
                if hasattr(trade.AdditionalInfo(), addInfoName):
                    getattr(trade.AdditionalInfo(), addInfoName)(value)
    
    @staticmethod
    def TagTrades(tradeOrDp, addInfoName, tag):
        tradeOrDp = UnDecorate(tradeOrDp)
        acm.BeginTransaction()
        try:
            if tradeOrDp.Originator().StorageId() > 0:
                if tradeOrDp.IsKindOf('FDealPackage'):
                    trades = tradeOrDp.Trades()
                else:
                    trades = acm.FArray()
                    trades.Add(tradeOrDp)
                TradeCreationUtil.SetAddInfoOnTrades(trades, addInfoName, tag)
                trades.Commit()
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            raise DealPackageUserException('Failed to set ' + addInfoName + ' AdditionalInfo: ' + str(e))
    
    @staticmethod
    def TagTradesIfNecessary(trade, dp, addInfoName, tag, tradeCreationSetting, isOnDp):
        createNew = tradeCreationSetting in [TradeCreation.CreateNewInsAndTrade(isOnDp), TradeCreation.CreateNewTrade(isOnDp)]
        updateOrManual = tradeCreationSetting in [TradeCreation.Update(isOnDp), TradeCreation.Manual(isOnDp)]
        if updateOrManual or (createNew and TradeCreationUtil.CreateTradesOnRequest(trade, dp)):
            tradeOrDealPackage = dp.Originator() if isOnDp else trade.Originator() #Must use originators, else user can change things after Check Limits and it will be commited here
            TradeCreationUtil.TagTrades(tradeOrDealPackage, addInfoName, tag)
    
    @staticmethod
    def ObjectToQuote(dp, trade, quoteOnlyInstrumentPart):
        objectToQuote = None
        if dp:
            if quoteOnlyInstrumentPart:
                objectToQuote = dp.InstrumentPackage().Originator()
            else:
                objectToQuote = dp.Originator()
        else:
            if quoteOnlyInstrumentPart:
                objectToQuote = trade.Instrument().Originator()
            else:
                objectToQuote = trade.Originator()
        return UnDecorate(objectToQuote)
    
    @staticmethod
    def CreateCustomDict(dp, isOnDp, trade, tradeCreationSetting, customAttributes, setObjectsToQuoteCb):
        try:
            def SetSalesObject(dp, trade, customDict, quoteOnlyInstrumentPart):
                dp = dp if dp and not dp.IsDeal() else None
                salesObject = TradeCreationUtil.ObjectToQuote(dp, trade, quoteOnlyInstrumentPart)
                customDict.AtPut('salesObject', salesObject)
            
            def SetObjectsToQuote(customDict, quoteOnlyInstrumentPart):
                objectsToQuote = acm.FDictionary()
                customDict.AtPut('objectsToQuote', objectsToQuote)
                setObjectsToQuoteCb(objectsToQuote, quoteOnlyInstrumentPart)
                
            customDict = acm.FDictionary()
            tabRule = TABTradeCreationSetting.FromTradeCreationSetting(TradeCreation.EnumValue(tradeCreationSetting, isOnDp), trade, dp)
            quoteOnlyInstrumentPart = tabRule == TABTradeCreationSetting.createNewTrade
            SetSalesObject(dp, trade, customDict, quoteOnlyInstrumentPart)
            SetObjectsToQuote(customDict, quoteOnlyInstrumentPart)
            customDict.AtPut('tradeCreationSetting', tabRule)
            customDict.AtPut('customAttributes', customAttributes)
            return customDict
        except Exception as e:
            print(('Failed to create custom dict', e))
