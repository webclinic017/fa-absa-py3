import acm
from DealPackageGridViewModelItem import ModelRow, ModelItem
from PairOptionsUtil import GuiAttributeToSolverAttributeName, SolverAttributeToGuiAttributeName, GetColumnProperties, IsOfTypeFLot
from PairOptionsFormatters import FXRateFormatter, FXPointsFormatter

COLOR_BUY_CTRL = (200, 255, 200)
COLOR_SELL_CTRL = (255, 200, 200)
COLOR_SIMULATED_CALCULATION_CTRL = (225, 240, 255)
COLOR_CALCULATION_CTRL = (255, 255, 255)
COLOR_CALCULATION_READONLY_CTRL = (240, 240, 240)
COLOR_MARKET_DATA_LABEL_CTRL = (255, 229, 204)
COLOR_CALCULATION_LABEL_CTRL = (255, 255, 204)
COLOR_EDITABLE_LABEL_CTRL = (255, 255, 255)

class Row(ModelRow):
    pass

class ColumnHeaderRow(ModelRow):
    def IsColumnHeaderRow(self, dp):
        return True

def PriceBackColorIfIsQuoted(dp, attr):
    backColor = COLOR_CALCULATION_LABEL_CTRL
    quoted = dp.GetAttribute('saveTradeQuotation')
    currentLabel = dp.GetAttributeMetaData(attr, 'label')()
    if quoted == currentLabel:
        if 'buy' in dp.GetAttributeMetaData('buySell', 'label')().lower():
            backColor = COLOR_BUY_CTRL
        else:
            backColor = COLOR_SELL_CTRL
    return backColor
        
def RecurseForTip(val, flippValues):
    tip = None
    if val:
        if isinstance(val, float):
            tip = val
        elif val.IsKindOf(acm.FLot):
            first = RecurseForTip(val[0], flippValues)
            second = RecurseForTip(val[1], flippValues)
            if flippValues and first and second and first > second:
                tip = str(second) + "/" + str(first)
            else:
                tip = str(first) + "/" + str(second)
        elif val.IsKindOf(acm.FDenominatedValue):
            tip = val.Number()
    return tip
    
def IsNotDigital(dp):
    isNotDigital = True
    if 'baseType' in dp.GetAttributes():
        baseType = dp.GetAttribute('baseType')
        isNotDigital = not 'digital' in baseType.lower()
    return isNotDigital

def IsStrip(dealPackage):
    return str(dealPackage.DefinitionName()) == 'FXStripDealPackage'
    
class EmptyRow(ModelRow):
    def RowHight(self, dp):
        return 9
        
class VanillaRow(ModelRow):
    def Visible(self, dp):
        return dp.GetAttribute('baseType') == 'Vanilla'

class BarrierRow(ModelRow):
    def Visible(self, dp):
        return dp.GetAttribute('baseType') == 'Barrier'

class FlippedRow(ModelRow):
    def Visible(self, dp):
        return dp.GetAttribute('saveIsFlippedSide')

class NonFlippedRow(ModelRow):
    def Visible(self, dp):
        return not dp.GetAttribute('saveIsFlippedSide')
        
class DigitalEuropeanRow(ModelRow):
    def Visible(self, dp):
        return dp.GetAttribute('baseType') == 'Digital European'
        
class DigitalAmericanRow(ModelRow):
    def Visible(self, dp):
        return dp.GetAttribute('baseType') == 'Digital American'
        
class NotDigitalRow(ModelRow):
    def Visible(self, dp):
        baseType = dp.GetAttribute('baseType')
        return not baseType.startswith('Digital')

class SingleBarrierRow(ModelRow):
    def Visible(self, dp):
        baseType = dp.GetAttribute('baseType')
        barrierType = dp.GetAttribute('digitalEuropeanTypeForeign')
        return baseType in ['Barrier', 'Digital European', 'Digital American'] and barrierType != 'Vanilla'
        
class DoubleBarrierRow(SingleBarrierRow):
    def Visible(self, dp):
        return super(DoubleBarrierRow, self).Visible(dp) and dp.GetAttribute('barrierTypeForeign').startswith('Double') 

class VannaVolgaRow(ModelRow):
    def Visible(self, dp):
        return dp.GetAttribute('valuationAddOnModel') == 'Vanna Volga Pricing'
            
class NotVannaVolgaRow(VannaVolgaRow):
    def Visible(self, dp):
        return not super(NotVannaVolgaRow, self).Visible(dp)
        
class NotDigitalAmericanRow(DigitalAmericanRow):
    def Visible(self, dp):
        return not super(NotDigitalAmericanRow, self).Visible(dp)
                
class B2BRow(ModelRow):
    def Visible(self, dp):
        return dp.GetAttribute('b2b_b2bEnabled')

class CallPutAmountRow(ModelRow):
    def Visible(self, dp):
        if dp.GetAttribute("saveIsFlippedSide"):
            return round(abs(dp.GetAttribute('amountCallDomestic')), 2) != round(abs(dp.GetAttribute('amountPutDomestic')), 2) or not dp.GetAttribute('uiViewModeIsSlim')["DetailedMode1"]
        else:
            return round(abs(dp.GetAttribute('amountCallForeign')), 2) != round(abs(dp.GetAttribute('amountPutForeign')), 2) or not dp.GetAttribute('uiViewModeIsSlim')["DetailedMode1"]

class AmountRow(CallPutAmountRow):
    def Visible(self, dp):
        return not super(AmountRow, self).Visible(dp)
        
class StripAttributeRow(ModelRow):
    def __init__(self, attrName, legAttrItem = 'AttrPerLeg'):
        self._attrName = attrName
        #self._rowItems = [Attr(attrName), StripAttrLabel(attrName), AttrPerLeg(attrName)]
        self._rowItems = [Attr(attrName), StripAttrLabel(attrName), eval(legAttrItem)(attrName)]

    def Visible(self, dp):
        visible = self._rowItems[0].Visible(dp)
        if visible is None:
            for child in dp.ChildDealPackages():
                visible = self._rowItems[-1].Visible(child)
                if visible:
                    break
        return visible

class StripAttributeMarketDataRow(StripAttributeRow):
    def __init__(self, attrName, showSummary = True, 
                       setValueOnParent = False, labelCB = None):
        self._attrName = attrName
        legItem     = AttrMarketDataPerLeg(attrName, setValueOnParent)
        labelItem   = StripMarketDataAttrLabel(attrName, labelCB)
        summaryItem = AttrCalc(attrName)
        self._rowItems = [summaryItem, labelItem, legItem]

    def Visible(self, dp):
        return True

class StripAttributeCalculationRow(StripAttributeRow):
    def __init__(self, attrName, standardLabelBackground = False):
        self._attrName = attrName
        legItem = AttrPerLeg(attrName)
        if standardLabelBackground is True:
            labelItem = StripAttrLabel(attrName)
        else:
            labelItem = StripCalcAttrLabel(attrName)
        summaryItem = AttrCalc(attrName)
        self._rowItems = [summaryItem, labelItem, legItem]

'''********************************************************'''
class ModelAttrItem(ModelItem):
    def __init__(self, attrName):
        self._attrName = attrName
        self._metaDataCache = acm.FDictionary()
        
    def AttrName(self):
        return self._attrName
    
    def MetaDataCache(self, dp):
        metaDataKey = dp.Handle() if dp else dp
        cache = self._metaDataCache.At(metaDataKey)
        if not cache:
            cache = self._metaDataCache.AtPut(metaDataKey, self._metaDataCache.At(None, acm.FDictionary()))
        return cache
        
    def GetMetaData(self, dp, metaDataName, *args):
        callBack = self.MetaDataCache(dp).At(metaDataName)
        if not callBack:
            try:
                callBack = dp.GetAttributeMetaData(self.AttrName(), metaDataName)
            except RuntimeError: #Should be KeyError but the exception gets wrapped in a RuntimeError
                #dp has no attribute self.AttrName(), set callback to dummy that returns None
                callBack = lambda:None
            self.MetaDataCache(dp).AtPut(metaDataName, callBack)
        return callBack(*args)

    def GetMetaDataPerLeg(self, dp, metaDataName, *args):
        callBack = self.MetaDataCachePerLeg(dp).At(metaDataName)
        if not callBack:
            callBack = dp.GetAttributeMetaData(self.AttrName(), metaDataName)
            self.MetaDataCachePerLeg(dp).AtPut(metaDataName, callBack)
        return callBack(*args)

    def MetaDataCachePerLeg(self, dp):
        totalCache = self.MetaDataCache(dp)
        legName = dp.ParentDealPackageLink().Name() if dp.ParentDealPackageLink() else None
        if not legName:
            return self.MetaDataCache(dp)
        if not totalCache.HasKey(legName):
            legDict = acm.FDictionary()
            legDict.AtPut('calcMapping', lambda:str(calculation))
            totalCache.AtPut(legName, legDict)
        return totalCache.At(legName)

    def DelegateWithValidateMapping(self, dp):
        return (self.GetMetaData(dp.TopParentDealPackage(), "validateMapping") and 
                self.GetMetaData(dp.TopParentDealPackage(), "attributeMapping"))
    
    def ToolTip(self, dp):
        tip = self.GetMetaData(dp, 'toolTip')
        if not tip or (tip and len(tip) == 0):
            attrVal = dp.GetAttribute(self.AttrName())
            if attrVal:
                if isinstance(attrVal, float):
                    tip = str(attrVal)
        return tip
       
    def TabStop(self, dp):
        return self.GetMetaData(dp, 'enabled') and self.GetMetaData(dp, 'tabStop')
        
    def Label(self, dp): 
        return  self.GetMetaData(dp, 'label')
        
    def IsOptionTypeQuickEntryValue(self, dp):
        return False
        
    def IsMarketDataAttr(self, dp):
        return False
    
    def HasSolverParameter(self, dp):
        return False
        
    def Visible(self, dp):
        return self.GetMetaData(dp, 'visible')
        
    def ShowQuotationMenu(self, dp):
        return False

    def ShowStripRowLabelRightClickMenu(self, dp):
        return False


'''********************************************************'''
class Attr(ModelAttrItem):
    def GetValue(self, dp):
        return dp.GetAttribute(self.AttrName())
   
    def SetValue(self, dp, value):
        dp.SetAttribute(self.AttrName(), value)
     
    def ReadOnly(self, dp):
        return not self.GetMetaData(dp, 'enabled')
        
    def Formatter(self, dp):
        return self.GetMetaData(dp, 'formatter')
        
    def ChoiceListSource(self, dp):
        if self.ReadOnly(dp):
            choiceListSource = None
        else:
            choiceListSource = self.GetMetaData(dp, 'choiceListSource')
        if choiceListSource:
            choiceListSource = choiceListSource.GetChoiceListSource()
            try:
                # In case of a FChoiceListPopulator, get source as an FArray
                choiceListSource = choiceListSource.Source()
            except: pass
            choiceListSource = [obj.StringKey() if hasattr(obj, 'StringKey') else obj for obj in choiceListSource]

        return choiceListSource

    def IsCalculatedValue(self, dp):
        return self.GetMetaData(dp, 'calcMapping')
    
    def OnDoubleClick(self, dp):
        if 'setSolverParameterAction' in dp.GetAttributes():
            dp.GetAttribute('setSolverParameterAction')(self.AttrName())
        
    def UseBoldFont(self, dp):
        return SolverAttributeToGuiAttributeName(dp.GetAttribute('solverParameter')) == self.AttrName()
        
    def OnDeleteKeyDown(self, dp):
        if self.IsCalculatedValue(dp) and self.IsCalculationSimulated(dp):
            try:
                self.SetValue(dp, '')
            except Exception: 
                pass 
 
    def HasSolverParameter(self, dp):
        return dp.GetAttributeMetaData(GuiAttributeToSolverAttributeName(self.AttrName()), 'solverParameter')() != False
              
'''********************************************************'''    
class AttrReadOnly(Attr):
    def ReadOnly(self, dp):
        return True
        
    def BackColor(self, dp):
        return COLOR_CALCULATION_READONLY_CTRL 
        
'''********************************************************'''    
class CurrOrPairAttr(Attr):
    def SetValue(self, dp, value):
        value = dp.GetAttributeMetaData(self.AttrName(), 'transform')(value)
        if value and isinstance(value, str):
            if acm.FCurrency[value] or acm.FCommodityVariant[value]:
                dp.SetAttribute(self.AttrName(), value)
            elif acm.FInstrumentPair[value]:
                dp.SetAttribute('instrumentPair', value)
    
'''********************************************************'''    
class OptionTypeAttr(Attr):
    def IsOptionTypeQuickEntryValue(self, dp):
        return True
    
    def IsMarketDataAttr(self, dp):
        return False

    def HasSolverParameter(self, dp):
        return False
        
'''********************************************************'''    
class AttrPerLeg(Attr):
    def IsOptionTypeQuickEntryValue(self, dp):
        return self.AttrName() == 'subtypeForeign'
        
    def IsChildPackageLegAttr(self):
        return True

    def ReadOnly(self, dp):
        if self.DelegateWithValidateMapping(dp):
            return True
        return not self.GetMetaDataPerLeg(dp, 'enabled')

'''********************************************************'''    
class AttrPerLegReadOnly(AttrPerLeg):
    def ReadOnly(self, dp):
        return True

'''********************************************************'''    
class AttrPerLegWithDirectionColor(AttrPerLeg):
    def BackColor(self, dp):
        if 'buy' in dp.GetAttributeMetaData('buySell', 'label')().lower():
            backColor = COLOR_BUY_CTRL
        else:
            backColor = COLOR_SELL_CTRL
        return backColor

'''********************************************************'''    
class AttrPerLegWithDirectionColorIfNotReadOnly(AttrPerLegWithDirectionColor):
    def IsDigital(self, dp):
        return dp.GetAttribute("baseType").startswith("Digital")

    def SaveIsFlipped(self, dp):
        if self.IsDigital(dp):
            return not dp.GetAttributeMetaData('amountForeign', 'enabled')()
        return dp.GetAttribute('saveIsFlippedSide')

    def BackColor(self, dp):
        if self.ReadOnly(dp):
            return COLOR_CALCULATION_READONLY_CTRL
        else:
            return super(AttrPerLegWithDirectionColorIfNotReadOnly, self).BackColor(dp)

'''********************************************************'''    
class AttrPerLegReadOnlyIfNotFlippedDirectionColor(AttrPerLegWithDirectionColorIfNotReadOnly):
    def ReadOnly(self, dp):
        return not self.SaveIsFlipped(dp)

'''********************************************************'''    
class AttrPerLegReadOnlyIfFlippedDirectionColor(AttrPerLegWithDirectionColorIfNotReadOnly):
    def ReadOnly(self, dp):
        return self.SaveIsFlipped(dp)

'''********************************************************'''    
class CurrOrPairAttrLeft(CurrOrPairAttr):
    def Alignment(self, dp):
        return 'MiddleLeft'
        
'''********************************************************'''    
class AttrMid(Attr):
    def Alignment(self, dp):
        return 'MiddleCenter'
    
'''********************************************************'''    
class AttrLeft(Attr):
    def Alignment(self, dp):
        return 'MiddleLeft'

'''********************************************************'''    
class AttrBold(Attr):
    def UseBoldFont(self, dp):
        return True

'''********************************************************'''    
class AttrMidBold(AttrMid):
    def UseBoldFont(self, dp):
        return True

'''********************************************************'''
class AttrMidBoldQuotation(AttrMidBold):

    def ShowQuotationMenu(self, dp):
        return True
    
'''********************************************************'''    
class AttrLeftReadOnly(Attr):
    def Alignment(self, dp):
        return 'MiddleLeft'
        
    def ReadOnly(self, dp):
        return True
        
    def TabStop(self, dp):
        return False
        
    def ChoiceListSource(self, dp):
        pass
    
'''********************************************************'''    
class AttrAction(Attr):
    def GetValue(self, dp):
        return self.Label(dp)
    
    def OnDoubleClick(self, dp):
        dp.GetAttribute(self.AttrName())()
    
    def UseBoldFont(self, dp):
        return True
        
    def ReadOnly(self, dp):
        return True
        
    def TabStop(self, dp):
        return False


'''********************************************************'''    
class AttrActionBuySell(AttrAction):
    def Alignment(self, dp):
        return 'MiddleCenter'

    def BackColor(self, dp):
        if 'buy' in self.GetValue(dp).lower():
            backColor = COLOR_BUY_CTRL
        else:
            backColor = COLOR_SELL_CTRL
        return backColor
        
'''********************************************************'''    
class AttrActionLeft(AttrAction):
    def Alignment(self, dp):
        return 'MiddleLeft'
        
'''********************************************************'''    
class AttrActionRight(AttrAction):
    def Alignment(self, dp):
        return 'MiddleRight'
        
'''********************************************************'''    
class AttrActionForeignCurr(AttrActionLeft):
    def UseBoldFont(self, dp):
        return not dp.GetAttribute('saveIsFlippedSide') if IsNotDigital(dp) else False
        
    def OnDoubleClick(self, dp):
        if IsNotDigital(dp):
            super(AttrActionForeignCurr, self).OnDoubleClick(dp)

'''********************************************************'''    
class AttrActionDomesticCurr(AttrActionRight):
    def UseBoldFont(self, dp):
        return dp.GetAttribute('saveIsFlippedSide') if IsNotDigital(dp) else False
        
    def OnDoubleClick(self, dp):
        if IsNotDigital(dp):
            super(AttrActionDomesticCurr, self).OnDoubleClick(dp)
      
  
'''********************************************************'''    
class AttrCalc(Attr):
    def BackColor(self, dp):
        backColor = None
        if self.IsCalculatedValue(dp):
            if self.IsCalculationSimulated(dp):
                backColor = COLOR_SIMULATED_CALCULATION_CTRL
            elif self.ReadOnly(dp):
                backColor = COLOR_CALCULATION_READONLY_CTRL
            else:
                backColor = COLOR_CALCULATION_CTRL
        return backColor
        
    def GetCalculationColumnName(self, dp):
        columnName = None
        if self.IsCalculatedValue(dp):
            columnName = self.GetMetaData(dp, 'calcMapping').split(':')[-1]
        return columnName

    def IsCalculationSimulated(self, dp):
        isCalculationSimulated = None
        if self.IsCalculatedValue(dp):
            isCalculationSimulated = self.GetMetaData(dp, '_isUserSimulated')
            if isCalculationSimulated is None:
                isCalculationSimulated = self.GetMetaData(dp, 'isCalculationSimulated')
        return isCalculationSimulated

    def UseItalicFont(self, dp):
        return self.IsCalculationSimulated(dp)
        
    def ToolTip(self, dp):
        tip = ''
        try:
            calc = self.GetValue(dp)
            if calc and hasattr(calc, 'FormattedValue') and calc.IsKindOf(acm.FCalculation):
                formatter = self.GetMetaData(dp, 'formatter')
                try:
                    value = calc.Value()
                except Exception as e:
                    tip = str(e)
                else:
                    tip = str(RecurseForTip(value, hasattr(formatter, 'CompoundFormatting')))
            else:
                tip = str(calc)
        except Exception as e: 
            acm.Log('ToolTip error: %s' % e)
        return tip

'''********************************************************'''    
class AttrCalcLeft(AttrCalc):
    def Alignment(self, dp):
        return 'MiddleLeft'
      
'''********************************************************'''    
class AttrCalcMarketData(AttrCalc):
    def IsMarketDataAttr(self, dp):
        return True
    
        
'''********************************************************'''        
class AttrMarketDataPerLeg(AttrCalcMarketData):
    def __init__(self, attrName, setValueOnParent = False):
        AttrCalcMarketData.__init__(self, attrName)
        self._setValueOnParent = setValueOnParent

    def IsChildPackageLegAttr(self):
        return True
    
    def GetValue(self, dp):
        value = dp.GetAttribute(self.AttrName())
        if IsOfTypeFLot(value):
            return value[0]
        else:
            return value
    
    def SetValue(self, dp, value):
        if self._setValueOnParent:
            dp = dp.TopParentDealPackage()
            dp.SetAttribute(self.AttrName(), value)
        else:
            AttrCalcMarketData.SetValue(self, dp, value)

    def ReadOnly(self, dp):
        if self.DelegateWithValidateMapping(dp):
            return True
        return not self.GetMetaDataPerLeg(dp, 'enabled')
    
'''********************************************************'''        
class AttrParentMarketDataPerLeg(AttrMarketDataPerLeg):
    def SetValue(self, dp, value):
        dp = dp.TopParentDealPackage()
        dp.SetAttribute(self.AttrName(), value)

'''********************************************************'''        
class AttrParentMarketDataPerLegFxFlipFormat(AttrParentMarketDataPerLeg):
    def Formatter(self, dp):
        return FXRateFormatter( dp.GetAttribute('foreignInstrument'), 
                                dp.GetAttribute('domesticCurrency'),
                                dp.GetAttribute('saveIsFlippedSide'))
    
'''********************************************************'''        
class AttrMarketDataPerLegLot(AttrMarketDataPerLeg):
    def GetValue(self, dp):
        return dp.GetAttribute(self.AttrName())[0]
'''********************************************************'''    
class AttrCalcMarketDataLeft(AttrCalcLeft):
    def IsMarketDataAttr(self, dp):
        return True
        
'''********************************************************'''    
class AttrCalcMarketDataLeftReadOnly(AttrCalcMarketDataLeft):
    def ReadOnly(self, dp):
        return True

'''********************************************************'''        
class AttrMarketDataPerLegFxRateFormat(AttrMarketDataPerLeg):
    def Formatter(self, dp):
        return FXRateFormatter( dp.GetAttribute('foreignInstrument'), 
                                dp.GetAttribute('domesticCurrency'),
                                dp.GetAttribute('saveIsFlippedSide'))

'''********************************************************'''        
class AttrMarketDataPerLegFxPointsFormat(AttrMarketDataPerLeg):
    def Formatter(self, dp):
        return FXPointsFormatter( dp.GetAttribute('foreignInstrument'), 
                                  dp.GetAttribute('domesticCurrency'),
                                  dp.GetAttribute('saveIsFlippedSide'))

'''********************************************************'''    
class AttrCalcMarketDataLot(AttrCalcMarketData):
    def GetValue(self, dp):
        return dp.GetAttribute(self.AttrName())[0]
        
'''********************************************************'''    
class AttrCalcMarketDataLotLeft(AttrCalcMarketDataLot):
    def GetValue(self, dp):
        return dp.GetAttribute(self.AttrName())[0]
        
    def Alignment(self, dp):
        return 'MiddleLeft'

'''********************************************************'''    
class AttrCalcReadOnly(AttrCalc):
    def ReadOnly(self, dp):
        return True
        
    def BackColor(self, dp):
        return COLOR_CALCULATION_READONLY_CTRL
        
'''********************************************************'''    
class AttrCalcReadOnlyLeft(AttrCalcReadOnly):
    def Alignment(self, dp):
        return 'MiddleLeft'
        
'''********************************************************'''
class AttrLabel(ModelAttrItem):
    def GetValue(self, dp):
        return self.Label(dp)
             
    def ToolTip(self, dp):
        return self.GetMetaData(dp, 'toolTip')
        
    def TabStop(self, dp):
        return False

 
'''********************************************************'''
class AttrLabelLeft(AttrLabel):
    def Alignment(self, dp):
        return 'MiddleLeft'
        
'''********************************************************'''
class AttrLabelMarketDataLeft(AttrLabelLeft):
    def BackColor(self, dp):
        return COLOR_MARKET_DATA_LABEL_CTRL
        
'''********************************************************'''
class AttrLabelBoldLeft(AttrLabelLeft):
    def UseBoldFont(self, dp):
        return True
   
'''********************************************************'''
class AttrLabelRight(AttrLabel):
    def Alignment(self, dp):
        return 'MiddleRight'
        
'''********************************************************'''
class AttrLabelMarketDataRight(AttrLabelRight):
    def BackColor(self, dp):
        return COLOR_MARKET_DATA_LABEL_CTRL
        
'''********************************************************'''
class AttrLabelCalcRight(AttrLabelRight):
    def BackColor(self, dp):
        return COLOR_CALCULATION_LABEL_CTRL
    
'''********************************************************'''
class AttrLabelCalcLeft(AttrLabelLeft):
    def BackColor(self, dp):
        return COLOR_CALCULATION_LABEL_CTRL

'''********************************************************'''
class AttrLabelPriceLeft(AttrLabelLeft):
    def BackColor(self, dp):
        return PriceBackColorIfIsQuoted(dp, self.AttrName())
        
'''********************************************************'''
class AttrLabelPriceRight(AttrLabelRight):
    def BackColor(self, dp):
        return PriceBackColorIfIsQuoted(dp, self.AttrName())

'''********************************************************'''
class AttrLabelBoldRight(AttrLabelRight):
    def UseBoldFont(self, dp):
        return True
        
'''********************************************************'''
class Label(ModelItem):
    def __init__(self, label):
        self._label = label
    
    def ToolTip(self, dp):
        return self._label
        
    def GetValue(self, dp):
        return self._label

    def UseBoldFont(self, dp):
        return True
        
    def Alignment(self, dp):
        return 'MiddleCenter'
        
    def IsOptionTypeQuickEntryValue(self, dp):
        return False
        
    def IsMarketDataAttr(self, dp):
        return False
        
    def HasSolverParameter(self, dp):
        return False
        
    def Visible(self, dp):
        return True

    def ShowStripRowLabelRightClickMenu(self, dp):
        return IsStrip(dp)

    def TabStop(self, dp):      
        return False
        
'''********************************************************'''
class LabelLeft(Label):
    def UseBoldFont(self, dp):
        return False
        
    def Alignment(self, dp):
        return 'MiddleLeft'
        
'''********************************************************'''
class LabelRight(LabelLeft):
    def Alignment(self, dp):
        return 'MiddleRight'

'''********************************************************'''
class AttrPerLegName(Label):
    def IsChildPackageLegHeader(self):
        return True
        
    def Alignment(self, dp):
        return 'MiddleCenter'
        
    def GetValue(self, dp):
        return dp.ParentDealPackageLink().Name() if dp.ParentDealPackageLink() else None

    def UseBoldFont(self, dp):
        return True
        
    def UseItalicFont(self, dp):
        useItalic = False
        parentLink = dp.ParentDealPackageLink()
        if parentLink:
            useItalic = parentLink.IsLead()
        return useItalic
        
'''********************************************************'''
class EmptyCell(Label):   
    def __init__(self):
        self._label = ''

'''********************************************************'''
class LabelParam(Label):
    def BackColor(self, dp):
        return COLOR_MARKET_DATA_LABEL_CTRL
       
'''********************************************************'''
class LabelCalc(Label):
    def BackColor(self, dp):
        return COLOR_CALCULATION_LABEL_CTRL

'''********************************************************'''
class LabelCalcTooltip(LabelCalc):

    def __init__(self, label, tooltipAttribute):
        super(LabelCalcTooltip, self).__init__(label)
        self._tooltipAttribute = tooltipAttribute
    
    def ToolTip(self, dp):
        return '%s (%s)' % (self._label, dp.GetAttribute(self._tooltipAttribute))

'''********************************************************'''
class LabelCalcTooltipQuotation(LabelCalcTooltip):

    def ShowQuotationMenu(self, dp):
        return True

'''********************************************************'''
class LabelWhite(Label):
    def BackColor(self, dp):
        return COLOR_EDITABLE_LABEL_CTRL
    
    def UseBoldFont(self, dp):
        return False
'''********************************************************'''
class AttrLabelMidBold(ModelAttrItem):
   
    def GetValue(self, dp):
        return self.Label(dp)
    
    def UseBoldFont(self, dp):
        return True
        
    def Alignment(self, dp):
        return 'MiddleCenter'

    def ShowStripRowLabelRightClickMenu(self, dp):
        return IsStrip(dp)

'''********************************************************'''
class StripAttrLabel(AttrLabelMidBold):
    def GetValue(self, dp):
        label = self.Label(dp)
        if label is None:
            for child in dp.ChildDealPackages():
                label = self.Label(child)
                if label is not None:
                    break
        return label

    def Visible(self, dp):
        return True
        
    def ToolTip(self, dp):
        try:
            return AttrLabelMidBold.ToolTip(self, dp)
        except:
            pass

class StripMarketDataAttrLabel(StripAttrLabel):
    def __init__(self, attrName, labelCB = None):
        StripAttrLabel.__init__(self, attrName)
        self._labelCB = labelCB
        
    def BackColor(self, dp):
        return COLOR_MARKET_DATA_LABEL_CTRL
    
    def GetValue(self, dp):
        if self._labelCB is None:
            return StripAttrLabel.GetValue(self, dp)
        else:
            return self._labelCB()

class StripCalcAttrLabel(StripAttrLabel):
        
    def BackColor(self, dp):
        return COLOR_CALCULATION_LABEL_CTRL
        
'''********************************************************'''

class AttrLabelCusomCalcRight(AttrLabelCalcRight):
    def GetValue(self, dp):
        return AttrLabelCalcRight.GetValue(self, dp).split(';')[-1]
    
    def Visible(self, dp):
        return IsNotDigital(dp) and super(AttrLabelCusomCalcRight, self).Visible(dp)

class AttrLabelCusomCalcLeft(AttrLabelCalcLeft):
    def GetValue(self, dp):
        return AttrLabelCalcLeft.GetValue(self, dp).split(';')[0]

class CustomCalc(AttrCalc):
    def __init__(self, calculation, attribute):
        AttrCalc.__init__(self, attribute)
        self._calculation = calculation
        self._isFlipped = False
        self.MetaDataCache(None).AtPut('calcMapping', lambda:str(calculation))
    
    def GetValue(self, dp):
        return self.GetMetaData(dp, 'action', self._calculation, self._isFlipped)

class CustomCalcFlipped(CustomCalc):
    def __init__(self, calculation, attribute):
        CustomCalc.__init__(self, calculation, attribute)
        self._isFlipped = True

    def Alignment(self, dp):
        return 'MiddleLeft'
        
    def Visible(self, dp):
        return IsNotDigital(dp) and super(CustomCalcFlipped, self).Visible(dp)

class CustomCalculationsRows(object):
    def __init__(self, attribute, showFlippedCalculation = True):
        self._attribute = attribute
        self._flippedCalc = showFlippedCalculation
        
    def CalcLabel(self, columnName):
        properties = GetColumnProperties(str(columnName))
        labels = str(properties.get(acm.FSymbol('LabelList'), '')).split(';')
        return labels[0] if labels else 'Label'

    def ModelRows(self, dp):
        rows = []
        for calc in dp.GetAttribute(self._attribute):
            row = Row([ CustomCalc(calc, self._attribute),
                        AttrLabelCusomCalcLeft(self._attribute),
                        LabelCalc(self.CalcLabel(calc)),
                        AttrLabelCusomCalcRight(self._attribute) if self._flippedCalc else Label(''),
                        CustomCalcFlipped(calc, self._attribute) if self._flippedCalc else Label('')])
            rows.append(row)
        return rows

'''********************************************************'''
class CustomCalcPerLeg(AttrCalc):
    def __init__(self, calculation, attribute):
        AttrCalc.__init__(self, attribute)
        self._calculation = calculation
        self.MetaDataCache(None).AtPut('calcMapping', lambda:str(calculation))

    def GetValue(self, dp):
        return self.GetMetaDataPerLeg(dp, 'action', self._calculation, dp.GetAttribute('saveIsFlippedSide'))

    def IsChildPackageLegAttr(self):
        return True

class CustomCalcStrip(AttrCalc):
    def __init__(self, calculation, attribute):
        AttrCalc.__init__(self, attribute)
        self._calculation = calculation
        self.MetaDataCache(None).AtPut('calcMapping', lambda:str(calculation))

    def GetValue(self, dp):
        return self.GetMetaData(dp, 'action', self._calculation)

class LabelCalcStrip(LabelCalc):
    def __init__(self, calc, dpAttribute):
        self._dpAttribute = dpAttribute
        self._columnName = calc
        self._label = self.GetLabelValue()

    def GetLabelValue(self):
        properties = GetColumnProperties(str(self._columnName))
        labels = str(properties.get(acm.FSymbol('LabelList'), '')).split(';')
        return labels[0] if labels else 'Label'

    def AttrName(self):
        return self._dpAttribute
    
    def GetCalculationColumnName(self, dp):
        return self._columnName
    
class StripCustomCalculationsRows(CustomCalculationsRows):
    def __init__(self, attribute, stripAttribute):
        self._attribute = attribute
        self._stripAttribute = stripAttribute

    def ModelRows(self, dp):
        rows = []
        for calc in dp.GetAttribute(self._attribute):
            row = Row([CustomCalcStrip(calc, self._stripAttribute),
                       LabelCalcStrip(calc, self._attribute),
                       CustomCalcPerLeg(calc, self._attribute)])
            rows.append(row)
        return rows


