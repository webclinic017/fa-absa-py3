from __future__ import print_function
import acm
from DealPackageDevKit import DealPackageDefinition, Settings, Delegate, List, Action, Object, CalcVal, Str, Bool, ReturnDomainDecorator, DealPackageException, SetNew
from FXStripGenerateLegs import GenerateStripLegs
from PairOptionsFormatters import SingleValueFormatter, TheorPriceFormatterCBImpl, SingleValueIfAllEqualFormatter, FXRateFormatter, FXPointsFormatter, HideValueFormatter
from PairOptionsUtil import CurrencyStrFromDV, SetCombinationParamsFromFXOTrade, PriceGreekExcludeVolatilityMovement, GetSingleValue, UsePerUnitQuotationImpl, DomesticColumnConfig, SolverAttributeToGuiAttributeName, SolverAttributeChangeOnStripFlip
from FXCalculations import SaveTradeCalculations
from TraitBasedDealPackage import MuteParentDealPackageDelegateUpdates

CHILDLEG_PREFIX = 'Leg'
NoVal = 'NoVal'

SHEET_DEFAULT_COLUMNS = []
@Settings(GraphApplicable=False,
          SheetApplicable=False,
          SheetDefaultColumns=SHEET_DEFAULT_COLUMNS)
class FXStripDefinition(DealPackageDefinition):
    # Delegate Attributes to all children
    # - values MUST equal on all children
    instrumentPair =            Delegate(  attributeMapping='AllChildren.instrumentPair',
                                           onChanged = '@UpdateCombinationTrade',
                                           _excludeFromSorting = True )
    
    counterparty =              Delegate(  attributeMapping='AllChildren.counterparty')
    
    settlementType =            Delegate(  attributeMapping='NonDigitalChildren.settlementType',
                                           enabled="@NonDigitalChildren",
                                           visible="@NonDigitalChildren")
    
    payType =                   Delegate(  attributeMapping='AllChildren.payType')
    
    portfolio =                 Delegate(  attributeMapping='AllChildren.portfolio')
    
    acquirer =                  Delegate(  attributeMapping='AllChildren.acquirer')
    
    broker =                    Delegate(  attributeMapping='AllChildren.broker')
    
    tradeStatus =               Delegate(  attributeMapping='AllChildren.tradeStatus')

    foreignInstrument =         Delegate(  label='', # Not shown in GUI, may be mismatching
                                           attributeMapping='AllChildren.foreignInstrument')
    
    domesticCurrency =          Delegate(  label='', # Not shown in GUI, may be mismatching
                                           attributeMapping='AllChildren.domesticCurrency')

    marketValuesLocked =        Delegate(  attributeMapping='AllChildren.marketValuesLocked')

    saveTradeQuotation =        Delegate(  attributeMapping='LegsOrTemplate.saveTradeQuotation')
    
    premiumCurrency =           Delegate(  attributeMapping='LegsOrTemplate.premiumCurrency',
                                           transform = "@SetValueToTemplate",
                                           domain=acm.FCurrency,
                                           _excludeFromSorting = True )


    # Delegate Attributes to all children
    # - values might differ per child
    
    expiryDate =                Delegate(  attributeMapping='LegsOrTemplate.expiryDate',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate")
                                         
    deliveryDate =              Delegate(  attributeMapping='LegsOrTemplate.deliveryDate',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           tabStop = False)
                                         
    fixingSource =              Delegate(  attributeMapping='LegsOrTemplate.fixingSource',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate")
                                     
    baseType =                  Delegate(  attributeMapping='LegsOrTemplate.baseType',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate")
                                         
    valGroup =                  Delegate(  attributeMapping='AllChildren.valGroup',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate")
                                           
    valueDay =                  Delegate(  attributeMapping='AllChildren.valueDay',
                                           validateMapping = False)
                                           
    amountForeignStorage =      Delegate(  attributeMapping='AllChildren.amountForeign',
                                           validateMapping = False) 
                                           
    amountDomesticStorage =     Delegate(  attributeMapping='AllChildren.amountDomestic',
                                           validateMapping = False)
    # -------------------------------------------------------------------------------
    # Exotic type mappings
    # -------------------------------------------------------------------------------
    
    subtypeForeign =            Delegate(  label = 'Subtype',
                                           attributeMapping='LegsOrTemplate.subtypeForeign',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           enabled = "@SubtypeEnabled",
                                           visible = "@VisibleFromChildren")

    subtypeDomestic =           Delegate(  label = 'Subtype',
                                           attributeMapping='LegsOrTemplate.subtypeDomestic',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           enabled = "@SubtypeEnabled",
                                           visible = "@VisibleFromChildren")                                    
                                     
    payAtExpiry =               Delegate(  attributeMapping='AllChildren.payAtExpiry',
                                           validateMapping = False)

    # -------------------------------------------------------------------------------
    # Exotic barrier mappings
    # -------------------------------------------------------------------------------                                        
    barrierDomesticPerForeign = Delegate(  attributeMapping='LegsOrTemplate.barrierDomesticPerForeign',
                                           label = '@LabelFromChildren',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           visible = "@VisibleFromChildren")

    barrierForeignPerDomestic = Delegate(  attributeMapping='LegsOrTemplate.barrierForeignPerDomestic',
                                           label = '@LabelFromChildren',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           visible = "@VisibleFromChildren")

    doubleBarrierDomesticPerForeign=Delegate(  attributeMapping='LegsOrTemplate.doubleBarrierDomesticPerForeign',
                                           label = '@LabelFromChildren',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           visible = "@VisibleFromChildren")

    doubleBarrierForeignPerDomestic=Delegate(  attributeMapping='LegsOrTemplate.doubleBarrierForeignPerDomestic',
                                           label = '@LabelFromChildren',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           visible = "@VisibleFromChildren")

    # Delegate to children (ignore Template)
    # - values might differ per child
    strikeDomesticPerForeign =  Delegate(  label='Strike',
                                           attributeMapping='LegsOrTemplate.strikeDomesticPerForeign',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           visible = "@VisibleFromChildren")

    strikeForeignPerDomestic =  Delegate(  label='Strike',
                                           attributeMapping='LegsOrTemplate.strikeForeignPerDomestic',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate",
                                           visible = "@VisibleFromChildren")
                                           
    tradeTime =                 Delegate(  attributeMapping='LegsOrTemplate.tradeTime',
                                           validateMapping = False)
                                           
    optionType =                Delegate(  attributeMapping='LegsOrTemplate.optionType',
                                           validateMapping = False,
                                           transform = "@SetValueToTemplate")

    # Object mapping to child deal packages                                      
    amountForeign =             Object(    objMapping='StripForeignAmount',
                                           domain='double',
                                           label = '@ForeignCurrencyAsLabel') 
                                                               
    amountDomestic =            Object(    objMapping='StripDomesticAmount',
                                           domain='double',
                                           label = '@DomesticCurrencyAsLabel') 
                                         
    tradePrice =                Object(    objMapping='StripTradePrice',
                                           domain='double',
                                           label = 'Price')
                            
    tradePremium =              Object(    objMapping='StripTradePremium',
                                           domain='double',
                                           label = 'Premium')

    # Attributes on Strip
    memo =                      Object(    defaultValue='',
                                           label='Memo',
                                           objMapping='DealPackage.AdditionalInfo.MemoString')  
   
    volatility =                CalcVal(   calcMapping='CombinationTrade:FDealSheet:Strategy Volatility FXOStrat',
                                           transform='@SetValueToChildren',
                                           formatter = SingleValueIfAllEqualFormatter,
                                           enabled='@HasChildren',
                                           label='Volatility')
                                           
    undVal =                    CalcVal(   calcMapping='TemplatePackageTrade:FDealSheet:Portfolio Underlying Price FXOStrat',
                                           transform='@SetValueToChildren',
                                           formatter = '@FXRateFormatterCB',
                                           calcConfiguration='@UsePerUnitQuotation',
                                           enabled='@HasChildren',
                                           label='Spot',
                                           _excludeFromSorting = True )
    
    saveTradeCalcVal =          SaveTradeCalculations('CombinationTrade', enabled = False)

        # As it is not possible to have onChanged on a Delegate attribute, this attribute has been
        # introduced as a work around for having onChanged on saveIsFlippedSide.
    saveIsFlippedSide =         Object( objMapping = 'SaveIsFlippedSide',
                                        onChanged = '@FlipSimulations|FlipSolverParamters')

    # Actions
    addStripLeg =               Action(    action='@AddStripLeg')
    removeStripLeg =            Action(    action='@RemoveStripLeg')
    updateTradePriceFromTheor = Action(    action='@DoActionForEachChild')
    removeSimulations =         Action(    action='@RemoveSimulations')
    setLegAsLeading =           Action(    action='@SetLegAsLeading')
    insertCopyOfLeg =           Action(    action='@InsertCopyOfLeg')
    setForeignAsSave =          Action(    action='@DoActionForEachChildAndTemplate',
                                           enabled='@SetForeignAsSaveEnabled',
                                           recreateCalcSpaceOnChange=True)
    setDomesticAsSave =         Action(    action='@DoActionForEachChildAndTemplate',
                                           recreateCalcSpaceOnChange=True)
    flipPremiumCurrency =       Action(    action='@DoActionForEachChildAndTemplate')
    sortStripLegs =             Action(    action='@SortStripLegs')
 
    generateStripLegs =         GenerateStripLegs(templatePackage='TemplatePackage')
    
    # Ux
    gridModelView =             List()

    customCalculations =        Delegate(  attributeMapping='AllChildren.customCalculations')
    getCustomCalculations =     Action(    action='@GetCustomCalculation',
                                           visible=True,
                                           enabled=False,
                                           noDealPackageRefreshOnChange=True)

    redrawNeeded =              Bool(False)
    sortOrder =                 List (onChanged = '@PerformTouch')
    legIsSetAsLeading =         Bool(False)

    '''*******************************************************
    * Deal Package Interface Methods
    *******************************************************'''     
    def OnInit(self):
        self._updateCombinationWeightsNeeded = None
        self.templatePackage = self.CreateTemplateDealpackage()
        self.stripCombinationTrade = self.CreateStripCombinationTrade()
        self._combinationUpdateHandler = CombinationUpdateLogicHandler(self)
        self.sortOrder = acm.FArray()
    
    def OnOpen(self):
        self._updateCombinationWeightsNeeded = True
        self.UpdateCombinationWeights()

    def LeadTrade(self):
        if not self.DealPackage().AllTrades():
            return []
        if self.legIsSetAsLeading:
            return self.DealPackage().LeadTrade()
        leadTrade = self.DealPackage().AllTrades().First()
        for trade in self.DealPackage().AllTrades():
            ins = trade.Instrument()
            if ins.ExpiryDate() > leadTrade.Instrument().ExpiryDate():
                leadTrade = trade
        return leadTrade
    
    def LeadTradeDealPackage(self):
        leadTrade = self.LeadTrade()
        return leadTrade.DealPackage() if leadTrade else self.TemplatePackage()
        
    def Refresh(self):
        self.TemplatePackage().Refresh()
        self.UpdateCombinationWeights()        

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator(
            { 'saveTradeCalcVal_fwdPoints'              : dict(label = 'Fwd Points',
                                                               enabled = False,
                                                               formatter = HideValueFormatter ),
              'saveTradeCalcVal_fwd'                    : dict(label = 'Fwd',
                                                               enabled = False,
                                                               formatter = HideValueFormatter ),
              'saveTradeCalcVal_deltaBS'                : dict(label = 'Delta'),
              'saveTradeCalcVal_fwdDeltaBS'             : dict(label = 'Fwd Delta'),
              'saveTradeCalcVal_delta'                  : dict(label = 'Vol Adj Delta'),
              'saveTradeCalcVal_theorVal'               : dict(label = 'TheorVal'),
              'saveTradeCalcVal_theorValNoPremium'      : dict(label = 'TheorVal Ins'),
              'saveTradeCalcVal_theor'                  : dict(label = 'Price',
                                                               toolTip = '@TheorTooltip')})

    '''*******************************************************
    * Binding Collections
    *******************************************************'''       
    def AllChildren(self):
        return list(self.OpeningDealPackages()) + [self.TemplatePackage()]
        
    def LegsOrTemplate(self):
        return self.OpeningDealPackages() if self.OpeningDealPackages() else [self.TemplatePackage()]
        
    def NonDigitalChildren(self, *args):
        return [child for child in self.AllChildren() if not child.GetAttribute('baseType').startswith('Digital')]
     
    def AsPortfolio(self):
        return self.DealPackage().AsPortfolio()
        
    def TemplatePackage(self):
        return self.templatePackage

    def TemplatePackageTrade(self):
        return self.TemplatePackage().Trades().First()
        
    def CombinationTrade(self):
        return self.stripCombinationTrade

    def CombinationInstrument(self):
        return self.CombinationTrade().Instrument()
 
 
    '''*******************************************************
    * Object Mappings
    *******************************************************'''   
    def AggregateFromChildren(self, attr, val = NoVal, weighted = True):
        if val == NoVal:
            GetChildContribution = lambda dp: dp.GetAttribute(attr) * (self.GetDealPackageWeight(dp) if weighted else 1)
            return sum(GetChildContribution(child) for child in self.DealPackage().ChildDealPackages())
        else:
            thVal = self.saveTradeCalcVal_theorValNoPremium.Value()
            if not thVal:
                raise ValueError("Can't distribute %s when sum of amounts are zero" % attr)
            for child in self.DealPackage().ChildDealPackages():
                v = val * child.GetAttribute('saveTradeCalcVal_theorValNoPremium').Value() /  thVal / (self.GetDealPackageWeight(child) if weighted else 1)
                child.SetAttribute(attr, float(v))
                
    def StripTradePrice(self, val = NoVal):
        return self.AggregateFromChildren('tradePrice', val)

    def StripTradePremium(self, val = NoVal):
        return self.AggregateFromChildren('tradePremium', val, False)
        
    def StripAmount(self, attrName, val = NoVal):
        if val == NoVal:
            attrName = attrName[:attrName.find('Storage')] if attrName.find('Storage') > 0 else attrName
            leadTradeDealPackage = self.LeadTradeDealPackage()
            return leadTradeDealPackage.GetAttribute(attrName) if leadTradeDealPackage else self.amountForeignStorage
        else:
            self.DealPackage().SetAttribute(attrName, val)
            
    def StripForeignAmount(self, val = NoVal):
        return self.StripAmount('amountForeignStorage', val)
        
    def StripDomesticAmount(self, val = NoVal):
        return self.StripAmount('amountDomesticStorage', val)

    @ReturnDomainDecorator('bool')
    def SaveIsFlippedSide(self, val = NoVal, *args):
        if val == NoVal:
            firstChild = self.LegsOrTemplate()[0] #Can't use the own traits as they might not have been updated yet
            saveTradeQuotation = firstChild.GetAttribute("saveTradeQuotation")
            domesticCurrency = firstChild.GetAttribute("domesticCurrency").Name()
            return saveTradeQuotation.endswith(domesticCurrency)

    def ChildPackageLabel(self, attrName):
        return self.LegsOrTemplate()[0].GetAttributeMetaData(attrName, 'label')()

            
    '''*******************************************************
    * Trait callback methods
    *******************************************************'''     
    def FXRateFlipFormatterCB(self, *args):
        pass # saveTradeCalcVal_fwd expects this method to exist
    
    def SingleValueFormatterCB(self, *args):
        return SingleValueFormatter("Buy")

    def PriceGreekExcludeVolatilityMovement(self, attrName):
        return PriceGreekExcludeVolatilityMovement(attrName)
    
    def TheorPriceFormatterCB(self, attrName):
        value = getattr(self, attrName).Value()
        unit = GetSingleValue(value).Unit()
        return TheorPriceFormatterCBImpl(attrName, unit)
    
    def SetValueToChildren(self, attrName, value):
        for child in self.DealPackage().ChildDealPackages():
            child.SetAttribute(attrName, value)
        if self.DealPackage().ChildDealPackages():
            value = self.DealPackage().ChildDealPackages()[0].GetAttributeMetaData(attrName, 'transform')(value)
        return value
    
    def HasChildren(self, attrName = None):
        return bool(self.DealPackage().ChildDealPackages())
    
    def TransformDelta(self, name, newDelta):
        return newDelta
    
    def TheorValSaveTradeLabel(self, *args):
        return 'TheorVal' + CurrencyStrFromDV(self.saveTradeCalcVal_theorVal)
        
    def TheorValNoPremiumSaveTradeLabel(self, *args):
        return 'TheorVal Ins' + CurrencyStrFromDV(self.saveTradeCalcVal_theorVal)

    def SetForeignAsSaveEnabled(self, attrName, *args):
        return self.TemplatePackage().GetAttributeMetaData('setForeignAsSave', 'enabled')()
        
    def SubtypeEnabled(self, attrName, *args):
        return bool(self.baseType)
    
    def SetValueToTemplate(self, attrName, value):
        try:
            self.TemplatePackage().SetAttribute(attrName, value)
        except Exception as e:
            self.Log().Error("Failed to set value '%s' for '%s' on template: %s" % (value, attrName, e))
        return value
    
    def VisibleFromChildren(self, attrName):
        if not (attrName.endswith("Foreign") if self.saveIsFlippedSide else attrName.endswith("Domestic")):
            for dp in self.LegsOrTemplate():
                if dp.GetAttributeMetaData(attrName, "visible")():
                    return True
        return False

    def ForeignRateLabel(self, *rest):
        return '%s Rate' % self.foreignInstrument.Name()

    def DomesticRateLabel(self, *rest):
        return '%s Rate' % self.domesticCurrency.Name()

    def TheorTooltip(self, *rest):
        return 'Price (%s)' % (self.saveTradeQuotation)

    def ForeignCurrencyAsLabel(self, *rest):
        return self.foreignInstrument.Name()
    
    def DomesticCurrencyAsLabel(self, *rest):
        return self.domesticCurrency.Name()

    def PerformTouch(self, attributeName, *rest):
        self.DealPackage().Touch()
        self.DealPackage().Changed()
        
    def LabelFromChildren(self, attrName):
        def SortValue(dp, attr):
            domain = dp.GetAttributeMetaData(attr, 'domain')()
            value = dp.GetAttribute(attr)
            if hasattr(domain, 'IsKindOf') and domain.IsKindOf('FEnumeration'):
                value = domain.Enumeration(value)
            return value
        children = sorted(self.LegsOrTemplate(), key = lambda dp:(SortValue(dp, 'baseType'), SortValue(dp, 'subtypeForeign')))
        for dp in children:
            if dp.GetAttributeMetaData(attrName, 'visible')():
                return dp.GetAttributeMetaData(attrName, 'label')()
        return children[0].GetAttributeMetaData(attrName, 'label')()

    def UpdateCombinationTrade(self, attrName, oldValue, newValue, *rest):
        combinationTrade = self.CombinationTrade()
        fxoTrade = self.AllChildren()[0].Trades().First()
        if SetCombinationParamsFromFXOTrade(combinationTrade, fxoTrade):
            self._calculationsRegistered = False
        
    '''*******************************************************
    * Util Methods
    *******************************************************'''
    def CreateStripCombinationTrade(self):
        combination = acm.DealCapturing.CreateNewInstrument('Combination')
        combinationTrade = acm.FBusinessLogicDecorator.WrapObject(acm.DealCapturing.CreateNewTrade(combination))
        SetCombinationParamsFromFXOTrade(combinationTrade, self.TemplatePackage().Trades().First())
        for instrument in self.DealPackage().AllInstruments():
            combination.AddInstrument(instrument, 1)
        return combinationTrade
        
    def CreateTemplateDealpackage(self):
        if self.DealPackage().ChildDealPackages():
            return self.DealPackage().ChildDealPackages().Last().Copy()
        return acm.DealPackage.NewAsDecorator('FX Option')
    
    def UpdateCombinationWeights(self):
        if self._updateCombinationWeightsNeeded:
            try:
                if self.CombinationInstrument().Instruments() != self.DealPackage().DealPackage().AllInstruments():
                    #Dealpackage instruments are changing, wait until they are in sycn
                    return
                amountAttribute = "amountDomestic" if self.saveIsFlippedSide else "amountForeign"
                instrumentAmounts = dict((child.Instruments().First().Oid(), child.GetAttribute(amountAttribute)) for child in self.DealPackage().ChildDealPackages())
                leadAmount = self.LeadTradeDealPackage().GetAttribute(amountAttribute)
                for map in self.CombinationInstrument().InstrumentMaps():
                    map.Weight = instrumentAmounts[map.Instrument().Oid()] / leadAmount
            except Exception as e:
                self.Log().Error('UpdateCombinationWeights failed: %s' % e)
                raise
            finally:
                self._updateCombinationWeightsNeeded = False

    def UsePerUnitQuotation(self, attrName):
        return UsePerUnitQuotationImpl(attrName)
        
    def CreateNewFxOptionDealPackage(self):
        return self.TemplatePackage().Copy()
        
    def CreateLinkName(self):
        legName = None        
        nbr = len(self.DealPackage().ChildDealPackages())
        while not legName or legName in self.DealPackage().ChildDealPackageKeys():
            nbr += 1
            legName = "%s%02d" % (CHILDLEG_PREFIX, nbr)
        return legName
    
    def AddChildDealPackage(self, fxOptionDP):
        newTrade = fxOptionDP.Trades().First()
        newInstrument = fxOptionDP.Trades().First().Instrument()
        SetNew([fxOptionDP, newTrade, newInstrument, fxOptionDP.InstrumentPackage()])
        for sim in self._GetSimulations():
            if self.trait_metadata(sim, 'transform') == "@SetValueToChildren":
                fxOptionDP.SetAttribute(sim, self._GetSimulations()[sim])
        self.DealPackage().AddChildDealPackage(fxOptionDP, self.CreateLinkName())
        self.UpdateSortOrder(fxOptionDP, 'Add')
        self.SetFirstChildAsLeadPackage()
        self.redrawNeeded = True

    def UpdateSortOrder(self, childPackage, action):
        if len(self.sortOrder) > 0:
            if action == 'Add':
                self.sortOrder.Add(childPackage)
            elif action == 'Remove':
                self.sortOrder.Remove(childPackage)

    def PersistSortOrder(self):
        if len(self.sortOrder) > 0:
            allLinks = [cpl for cpl in self.DealPackage().ChildDealPackageLinks()]
            allChildPackageOids = [cpl.ChildDealPackage().Oid() for cpl in allLinks]
            allNames = [p.Name() for p in allLinks]
            allLead = [p.IsLead() for p in allLinks]
            
            self.DealPackage().RemoveAllChildDealPackages(False, False)
            for i in range(len(self.sortOrder)):
                linkName = allNames[allChildPackageOids.index(self.sortOrder[i].Oid())]
                cp = self.DealPackage().AddChildDealPackage(self.sortOrder[i], linkName)
                cp.ParentDealPackageLink().IsLead(allLead[allChildPackageOids.index(self.sortOrder[i].Oid())])

    def OnSave(self, saveConfig):
        self.PersistSortOrder()
        super(FXStripDefinition, self).OnSave(saveConfig)
        if saveConfig.InstrumentPackage() == 'SaveNew':
            self.InstrumentPackage().Name('')

    def OnCopy(self, oldPackage, *rest):
        if len(self.sortOrder) > 0:
            if len(self.sortOrder)  == len(self.DealPackage().ChildDealPackageLinks()):
                sortOrderCopiedChildren = []
                originalChildrenOid = [c.OriginalOrSelf().Oid() for c in self.ChildDealPackages()]
                sortOrderOid = [p.Oid() for p in self.sortOrder]
                for cdp in self.sortOrder:
                    storedIndex = originalChildrenOid.index(cdp.Oid())
                    sortOrderCopiedChildren.append(self.ChildDealPackages()[storedIndex])
                self.sortOrder = sortOrderCopiedChildren
                            
    def GetDealPackageWeight(self, dealPackage):
        self.UpdateCombinationWeights()
        insMap = self.CombinationInstrument().MapAtInstrument(dealPackage.Instruments().First().Instrument())
        return insMap.Weight() if insMap else 1
        
    def FlipSpotSimulation(self):
        if self.IsCalculationSimulated('undVal'):
            currentSimStr = self.GetSimulatedCalculationValue('undVal')
            form = self.GetAttributeMetaData('undVal', 'formatter')()
            currentSim = form.Parse(currentSimStr)
            if currentSim != 0.0:
                inverseSimulation = 1.0 / currentSim
            else:
                inverseSimulation = 0.0
            self.undVal = form.Format(inverseSimulation)

    def FlipSimulations(self, attrName, *args):
        # Flip values on the strip
        self.FlipSpotSimulation()
        # Flip values on the children
        for child in self.AllChildren():
            child.GetAttribute('flipSaveTradeSimulations')(self.saveIsFlippedSide)

    def FlipSolverParamters(self, attrName, *args):
        for child in self.AllChildren():
            currentSolverParameter = child.GetAttribute('solverParameter')
            currentGUISolver = SolverAttributeToGuiAttributeName(currentSolverParameter)
            newGUISolver = SolverAttributeChangeOnStripFlip(currentGUISolver)
            child.GetAttribute('setSolverParameterAction')(newGUISolver)
            
    def CustomCalcConfig(self, *args):
        if self.saveIsFlippedSide:
            val = PriceGreekExcludeVolatilityMovement(None).Merge(DomesticColumnConfig(None))
        else:
            val = PriceGreekExcludeVolatilityMovement(None)
        return val
    
    '''*******************************************************
    * Action Methods
    *******************************************************'''       
    def AddStripLeg(self, attrName, *args):
        fxOptionDP = self.CreateNewFxOptionDealPackage()
        self.AddChildDealPackage(fxOptionDP)
        
    def RemoveStripLeg(self, attrName, legNames, *args):
        for leg in legNames:
            dp = self.DealPackage().ChildDealPackageAt(leg)
            if dp:
                self.DealPackage().RemoveChildDealPackage(dp, True)
                self.UpdateSortOrder(dp, 'Remove')
                self.redrawNeeded = True
        self.SetFirstChildAsLeadPackage()
        
    def SetFirstChildAsLeadPackage(self):
        if not self.DealPackage().LeadTrade():
            childLinks = self.DealPackage().ChildDealPackageLinks()
            if childLinks:
                childLinks.First().IsLead(True)
        
    def DoActionForEachChild(self, attrName, *args):
        for child in self.DealPackage().ChildDealPackages():
            child.GetAttribute(attrName)(*args)

    def DoActionForEachChildAndTemplate(self, attrName, *args):
        with MuteParentDealPackageDelegateUpdates(self):
            self.DoActionForEachChild(attrName, *args)
            self.TemplatePackage().GetAttribute(attrName)(*args)

    def RemoveSimulations(self, attrName, *args):
        self.RemoveAllSimulations()
        self.DoActionForEachChild(attrName, *args)
        
    def SetLegAsLeading(self, attrName, childDealPackage, *args):
        for childLink in self.DealPackage().DealPackageLinks():
            childLink.IsLead(False)
        childDealPackage.ParentDealPackageLink().IsLead(True)
        self.legIsSetAsLeading = True
        self._updateCombinationWeightsNeeded = True
        self.UpdateCombinationWeights()
        
    def InsertCopyOfLeg(self, attrName, childDealPackage, *args):
        fxOptionDP = childDealPackage.Copy()
        self.AddChildDealPackage(fxOptionDP)

    def GetCustomCalculation(self, attrName, columnName):
        if not columnName in self.customCalculations:
            raise DealPackageException('%s is not a valid custom calculation' % columnName)
        calcName = str(columnName).replace(' ', '_')
        calc = self.GetCalculation(calcName)
        if not calc:
            calcObj = 'CombinationTrade'
            calcConfig = self.CustomCalcConfig
            self.CreateCalculation(calcName, '%s:FDealSheet:%s' % (calcObj, columnName), calcConfig)
            calc = self.GetCalculation(calcName)
        return calc

    def SortStripLegs(self, attrName, sortAttribute, sortDirection = 'Ascending', calculationName = None):
        self.SortChildren(sortAttribute, sortDirection, calculationName)
        self.redrawNeeded = True

    '''*******************************************************
    * Formatter methods
    *******************************************************'''                    
    def FXRateFormatterCB(self, attrName):
        return FXRateFormatter(self.foreignInstrument, self.domesticCurrency, self.saveIsFlippedSide)

    def FXPointsFormatterCB(self, attrName):
        return FXPointsFormatter(self.foreignInstrument, self.domesticCurrency, self.saveIsFlippedSide)

    '''*******************************************************
    * Sorting methods
    *******************************************************'''                    

    def SortChildren(self, sortAttribute, sortDirection, calculationColumn = None):
        
        def UseCompare():
            if sortAttribute in ('expiryDate', 'deliveryDate', 'valueDay', 'tradeTime'):
                return acm.Time.DateDifference
            return None

        def GetCustomCalculationValue(childPackage):
            return childPackage.GetAttributeMetaData(sortAttribute, 'action')(calculationColumn, self.saveIsFlippedSide)

        def AttributeValueAsSortingKey(childPackage, attributeName = None):
            attributeName = sortAttribute if attributeName is None else attributeName
            if attributeName == 'customCalculations':
                attributeValue = GetCustomCalculationValue(childPackage)
            else:
                attributeValue = childPackage.GetAttribute(attributeName)
            if hasattr(attributeValue, 'IsKindOf') and attributeValue.IsKindOf(acm.FBusinessObject):
                return attributeValue.Name()
            if hasattr(attributeValue, 'IsKindOf') and attributeValue.IsKindOf(acm.FCalculation):
                return attributeValue.Value().Number()
            domain = childPackage.GetAttributeMetaData(attributeName, 'domain')()
            if hasattr(domain, 'IsKindOf') and domain.IsKindOf(acm.FEnumeration):
                return domain.Enumeration(attributeValue)
            return attributeValue

        def GetKey(item):
            try:
                if sortAttribute in ('subtypeForeign', 'subtypeDomestic'):
                    # We need to sort on both sub type and base type
                    return [AttributeValueAsSortingKey(item, 'baseType'), AttributeValueAsSortingKey(item)] 
                return AttributeValueAsSortingKey(item)
            except:
                return item.Oid()

        if sortDirection == 'Default':
            postSortedPackages = acm.FArray()
        else:
            preSortedPackages = self.GetAttribute('sortOrder')
            if len(preSortedPackages) == 0:
                preSortedPackages = self.DealPackage().ChildDealPackages()
            postSortedPackages = sorted(preSortedPackages, 
                                        cmp=UseCompare(), 
                                        key=GetKey, 
                                        reverse={'Ascending':False,'Descending':True}.get(sortDirection, False))

        ArrayCast = acm.GetFunction('array', 1)
        self.sortOrder = ArrayCast(postSortedPackages)

    '''*******************************************************
    * Ux
    *******************************************************'''         
    def CustomPanes(self):
        return self.GetCustomPanesFromExtValue('CustomPanes_FxStripDealPackage')
        
    def _gridModelView_default(self):
        from PairOptionsPricerGridViewModel import ColumnHeaderRow, Label, Attr, AttrMidBoldQuotation, AttrPerLegName
        from PairOptionsPricerGridViewModel import AttrPerLegReadOnlyIfFlippedDirectionColor, AttrPerLegReadOnlyIfNotFlippedDirectionColor
        from PairOptionsPricerGridViewModel import StripCustomCalculationsRows, StripAttributeRow, StripAttributeMarketDataRow, StripAttributeCalculationRow
        try:
            return [
                ColumnHeaderRow([Label('Summary'),                      AttrMidBoldQuotation('saveTradeQuotation'),      AttrPerLegName('')]),
                StripAttributeRow('instrumentPair'),
                StripAttributeRow('premiumCurrency'),
                StripAttributeRow('expiryDate'),
                StripAttributeRow('deliveryDate'),
                StripAttributeRow('fixingSource'),
                StripAttributeRow('optionType'),
                StripAttributeRow('baseType'),
                StripAttributeRow('subtypeForeign'),                    StripAttributeRow('subtypeDomestic'),
                StripAttributeRow('valGroup'),
                StripAttributeRow('strikeDomesticPerForeign'),          StripAttributeRow('strikeForeignPerDomestic'),
                StripAttributeRow('barrierDomesticPerForeign'),         StripAttributeRow('barrierForeignPerDomestic'),
                StripAttributeRow('doubleBarrierDomesticPerForeign'),   StripAttributeRow('doubleBarrierForeignPerDomestic'),
                StripAttributeRow('intrinsicFwd'),
                
                StripAttributeRow('amountForeign', legAttrItem = 'AttrPerLegReadOnlyIfFlippedDirectionColor'),
                StripAttributeRow('amountDomestic', legAttrItem = 'AttrPerLegReadOnlyIfNotFlippedDirectionColor'),
                
                StripAttributeMarketDataRow('undVal', setValueOnParent = True),
                StripAttributeMarketDataRow('saveTradeCalcVal_fwdPoints'),
                StripAttributeMarketDataRow('saveTradeCalcVal_fwd'),
                StripAttributeMarketDataRow('quoteTradeCalcVal_interestRate', labelCB = self.ForeignRateLabel),
                StripAttributeMarketDataRow('flippedQuoteTradeCalcVal_interestRate', labelCB = self.DomesticRateLabel),
                StripAttributeMarketDataRow('volatility'),

                StripAttributeCalculationRow('saveTradeCalcVal_theor'),
                StripAttributeCalculationRow('saveTradeCalcVal_deltaBS'),
                StripAttributeCalculationRow('saveTradeCalcVal_fwdDeltaBS'),
                StripAttributeCalculationRow('saveTradeCalcVal_delta'),

                StripCustomCalculationsRows('customCalculations', 'getCustomCalculations'),
                
                StripAttributeCalculationRow('saveTradeCalcVal_theorVal', standardLabelBackground = True),
                StripAttributeCalculationRow('saveTradeCalcVal_theorValNoPremium', standardLabelBackground = True),
                
                StripAttributeRow('tradePrice'),
                StripAttributeRow('tradePremium'),
               ]
        except Exception as e:
            print ('_gridModelView_default', e)
              

    '''*******************************************************
    * Callbacks that are required for saveTradecalcVal but only relevant for individual legs
    *******************************************************'''         
    def ValueSimulated(self, *args):
        pass
    
    def TransformPrice(self, attrName, value, *args):
        return value
    
    def FXRateLabel(self, *args):
        return ''
    
'''*******************************************************
* CombinationUpdateLogicHandler
*******************************************************'''         
class CombinationUpdateLogicHandler(object):
    def __init__(self, parent):
        self.parent = parent
        parent.AsPortfolio().Trades().AddDependent(self)
        
    def ServerUpdate(self, sender, aspectSymbol, parameter):
        if str(aspectSymbol) == 'insert':
            combinationTrade = self.parent.CombinationTrade()
            combinationTrade.Instrument().AddInstrument(parameter.Instrument(), 1)
            if SetCombinationParamsFromFXOTrade(combinationTrade, parameter):
                self.parent._calculationsRegistered = False
        elif str(aspectSymbol) == 'remove':
            self.parent.CombinationInstrument().Remove(parameter.Instrument())
        elif str(aspectSymbol) == 'update':
            pass
        else:
            self.parent.Log().Error('Unexpected aspect in ServerUpdate %s' % aspectSymbol)

        self.parent._updateCombinationWeightsNeeded = True
