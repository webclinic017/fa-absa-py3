
import acm
from SP_TrfExtension import TrfFxExtensionDefinition, TrfCommodityExtensionDefinition
from DealPackageDevKit import DealPackageException, CalcVal, Object, Str, Action, List, Bool, Float, Int, Date, DatePeriod, DealPackageChoiceListSource, Settings, CustomActions, TradeActions
from SP_CustomTradeActions import FlipTRFBuySellAction
import ChoicesExprInstrument
from SP_DealPackageHelper import DoubleBarrierChoices
from SP_CustomTradeActions import TrfExerciseAction, CheckTargetLevelAction

@Settings(GraphApplicable=True)
@CustomActions(flipBuySell = FlipTRFBuySellAction(ActionName = 'flipBuySell'),
               checkTargetLevel = CheckTargetLevelAction())
@TradeActions( exercise = TrfExerciseAction())
class FxTargetRedemptionForwardDefinition(TrfFxExtensionDefinition):
        
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'productType': dict(defaultValue='Target Redemption Forward'),
            'barrierApplicable': dict(defaultValue=True)
        })

    def GraphYValues(self, xValues):
        yValues = []
        if xValues:
            if self.strikeQuotation.Name() == 'Per Unit':
                attr = 'rateDomesticPerForeign'
                quotation = 1.0
            else:
                attr = 'rateForeignPerDomestic'
                quotation = -1.0
            strike = self.GetAttribute('strike_%s' % attr)
            barrier = self.GetAttribute('barrier_%s' % attr)
            buySell = 1.0 if self.buySellForeign == 'BUY' else -1.0
            for x in xValues:
                barrierHit = 1.0
                if self.hasEkiBarrier and self.barrier_rateDomesticPerForeign > 0.0:
                    if (x > barrier and x < strike) or (x < barrier and x > strike):
                        barrierHit = 0.0
                iv = (x - strike) * buySell * quotation * barrierHit
                notional = self.notional1 if iv > 0.0 else self.notional2
                yValues.append(iv * notional)
        return yValues

    def GraphXValues(self):
        try:
            tailPercent = 0.1
            xValues = []
            if self.strikeQuotation.Name() == 'Per Unit':
                attr = 'rateDomesticPerForeign'
            else:
                attr = 'rateForeignPerDomestic'
            strike = self.GetAttribute('strike_%s' % attr)
            tailSize = tailPercent * strike
            minX = strike * (1 - tailPercent)
            maxX = strike * (1 + tailPercent)
            xValues.append(1.0001 * strike)
            xValues.append(strike)
            xValues.append(0.9999 * strike)
            if self.hasEkiBarrier and self.barrier_rateDomesticPerForeign > 0.0:
                barrier = self.GetAttribute('barrier_%s' % attr)
                xValues.append(1.0001 * barrier)
                xValues.append(barrier)
                xValues.append(0.9999 * barrier)
                tailSize = max(tailSize, abs(strike - barrier) * tailPercent)
                minX = max(0, min(strike, barrier) - tailSize)
                maxX = max(strike, barrier) + tailSize
            xValues.append(minX)
            xValues.append(maxX)
            xValues.sort()
            return xValues
        except:
            return []
    
def StartFxTargetRedemptionForwardApplication(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'FX Target Redemption Forward')

@Settings(GraphApplicable = True)
@CustomActions(checkTargetLevel = CheckTargetLevelAction())
@TradeActions(exercise = TrfExerciseAction())
class CommodityTargetRedemptionForwardDefinition(TrfCommodityExtensionDefinition):
        
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'productType': dict(defaultValue='Target Redemption Forward')
        })
        
    def GraphXValues(self):
        k = self.strike.strikePrice
        xs = []
        if k:
            margin = 0.1
            x1 = k * (1 - margin)
            x2 = k * (1 + margin)
            xs = [x1, k, x2]
        return xs
        
    def GraphYValues(self, xs):
        ys = [0] * len(xs)
        n1 = self.notional1 or 0.0
        n2 = self.notional2 or 0.0
        if xs:
            k = self.strike.strikePrice
            for i, x in enumerate(xs):
                nom = n1 if x > k else n2
                ys[i] = (x - k) * nom
        return ys

def StartCommodityTargetRedemptionForwardApplication(eii):
    acm.UX().SessionManager().StartApplication('Deal Package', 'Commodity Target Redemption Forward')


# ----------------------------------------------------------------------------------------
# Structured Forward - NOTE: To be used as a template, no exercise and no valuation implemented
# ----------------------------------------------------------------------------------------

columnsExoticEventsStructuredForward = [
                        {'methodChain': 'Date',                'label':'Fixing Date'},
                        {'methodChain': 'EndDate',                   'label':'Pay Date'},
                        {'methodChain': 'TrfFixingDomesticPerForeign',  'label':'Fixing',       'fotmatter':'FXRate'},
                        {'methodChain': 'TrfFixingForeignPerDomestic',  'label':'Fixing Inv',   'fotmatter':'FXRate'},
                        {'methodChain': 'Instrument.ContractSize',      'label':'Notional 1'},
                        {'methodChain': 'Instrument.AdditionalInfo.sp_LeverageNotional', 'label':'Notional 2'},
                        ]

@CustomActions(flipBuySell = FlipTRFBuySellAction(ActionName = 'flipBuySell'))
class FxStructuredForwardDefinition(TrfFxExtensionDefinition):

    #-----------------------------
    # Base Class Overrides
    #-----------------------------

    
    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'exoticEvents':            dict(columns=columnsExoticEventsStructuredForward),
            
            'targetApplicable':        dict(defaultValue=False),
            
            'productType':             dict(defaultValue='Structured Forward')
            
            })


# ----------------------------------------------------------------------------------------
# Target Pivot Forward - NOTE: To be used as a template, no exercise and no valuation implemented
# ----------------------------------------------------------------------------------------
class FxTargetPivotForwardDefinition(TrfFxExtensionDefinition):

    def AttributeOverrides(self, overrideAccumulator):
        overrideAccumulator({
            'barrier_rateDomesticPerForeign':
                                dict(label='Lower Barrier'),
            
            'barrier_rateForeignPerDomestic':
                                dict(label='Upper Barrier'),
            
            'barrierType':      dict(choiceListSource=DoubleBarrierChoices()),
            
            'strike_rateDomesticPerForeign':
                                dict(label="Lower Strike"),
                                     
            'strike_rateForeignPerDomestic':
                                dict(label="Upper Strike"),
            
            'strike2Applicable':
                                dict(defaultValue=True),
            
            'pivotApplicable':  dict(defaultValue=True),
            
            'barrier2Applicable':
                                dict(defaultValue=True),
                                     
            'strike2_rateDomesticPerForeign':
                                dict(label="Upper Strike"),
            
            'strike2_rateForeignPerDomestic':
                                dict(label="Lower Strike"),
            
            'foreignCurrency':  dict(label='Foreign'),
            
            'domesticCurrency': dict(label='Domestic'),
            
            'productType':      dict(defaultValue='Target Pivot Forward')
            })   
