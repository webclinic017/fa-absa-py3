
import acm
import math

class PayoffGraphCalculations():

    def __init__(self, dealpackageDefinition, GetCalcSpaceCb):
        self._dealpackageDefinition = dealpackageDefinition
        self.GetGraphCalcSpace = GetCalcSpaceCb

    def DealPackage(self):
        return self.DealPackageDefinition().DealPackage()
    
    def DealPackageDefinition(self):
        return self._dealpackageDefinition

    def DealPackageInstruments(self):
        return [] if not self.DealPackage() else self.DealPackage().AllInstruments()
            
    def DealPackageTrades(self):
        return [] if not self.DealPackage() else self.DealPackage().AllTrades()
    
    '''** General Scenario **'''
    def CreateScenarioConfig(self, dimensions):
        scenario = acm.FExplicitScenario()
        for d in dimensions:
            scenario.AddDimension(d)
        config = acm.Sheet().Column().ConfigurationFromScenario(scenario, None)
        return config
    
    def CreateXValueDimension(self, extAttr, xValues):
        dim = acm.FDirectScenarioDimension()
        scm = acm.CreateScenarioMember(acm.GetFunction("replaceNumericValue", 2), extAttr, acm.FObject, xValues)
        dim.AddScenarioMember( scm )
        return dim
    
    def CreateVolAndTimeDimension(self, instrument):
        def GetValuationOffset(instrument):
            valuationOffset = 0
            timeToExpiry = self.GetGraphCalcSpace().CreateCalculation(instrument, "Time to Expiry")
            if timeToExpiry.Value():
                spotDateInverted = instrument.SpotDateInverted(instrument.ExpiryDateOnly())
                holidayAdjustedSpot = acm.Time().DateDifference(acm.Time.AsDate(instrument.ExpiryDateOnly()), spotDateInverted)
                valuationOffset = timeToExpiry.Value() - holidayAdjustedSpot - 1
            return valuationOffset
        
        dim = acm.FDirectScenarioDimension()
        valuationOffset = GetValuationOffset(instrument)
        volaAttributes = acm.GetDefaultContext().MemberNames("FExtensionAttribute", "risk factors", "volatility information")
        volaScm = acm.CreateScenarioMember(acm.GetFunction("*", 2), volaAttributes, acm.FObject, [0])
        timeScm = acm.CreateScenarioMember(acm.GetFunction("fixedvalue", 2), "valuationBaseDateTimeOffsetInput", acm.FObject, [valuationOffset])
        dim.AddScenarioMember( volaScm )
        dim.AddScenarioMember( timeScm )
        return dim
        
    def CreateDivDimension(self):
        # make sure that the underlying price is not dividend adjusted when the setting valuation date offset
        dim = acm.FDirectScenarioDimension()
        dividendAttributes = ['priceNeedsDividendAdjustment']
        divScm =  acm.CreateScenarioMember(acm.GetFunction("fixedvalue", 2), dividendAttributes, acm.FObject, [False])
        dim.AddScenarioMember( divScm )
        return dim

    '''** General Graph Coordinates **'''
    def GraphYValues(self, xVals):
        yVals = []
        if len(xVals):
            volAndTimeDim = None
            for i in self.DealPackageInstruments():
                if i.InsType() == 'Option':
                    volAndTimeDim = self.CreateVolAndTimeDimension(i)
                    break
            priceAttributes = acm.GetDefaultContext().MemberNames("FExtensionAttribute", "risk factors", "market price")
            priceDim = self.CreateXValueDimension(priceAttributes, xVals)
            divDim = self.CreateDivDimension()
            dimensions = [divDim, volAndTimeDim, priceDim] if volAndTimeDim else [divDim, priceDim]
            config = self.CreateScenarioConfig(dimensions)
            yVals = [0.0]*len(xVals)
            for t in self.DealPackageTrades():
                calc = self.GetGraphCalcSpace().CreateCalculation(t, "Portfolio Theoretical Value", config)
                theorVals = [x.Number() for x in calc.Value()]
                yVals = [sum(x) for x in zip(theorVals, yVals)]
        return yVals

    def GetStrike(self, option):
        #TODO, handle different strike types
        strike = option.StrikePrice()
        return strike
    
    def GetBarrierValues(self, option):
        barrierValues = acm.FArray()
        if option.Exotic() and option.Exotic().BarrierCrossedStatus() != 'Confirmed':
            for barrier in [option.Barrier(), option.Exotic().DoubleBarrier()]:
                if barrier:
                    barrierValues.Add(barrier)
                    # Need values just outside of the barrier to get the right shape
                    barrierValues.Add(barrier * 0.999)
                    barrierValues.Add(barrier * 1.001)
        return barrierValues
        
    def GetStrikeAndBarrierValues(self, option):
        strikeAndBarrierValues = acm.FArray()
        if self.GetStrike(option):
            if option.Digital():
                strikeAndBarrierValues.Add(self.GetStrike(option) * 0.999)
                strikeAndBarrierValues.Add(self.GetStrike(option) * 1.001)
            else:
                strikeAndBarrierValues.Add(self.GetStrike(option))
        strikeAndBarrierValues.AddAll(self.GetBarrierValues(option))
        return strikeAndBarrierValues
    
    def GetCurrentUnderlyingPrice(self, option):
        undPriceCalc = self.GetGraphCalcSpace().CreateCalculation(option, "Portfolio Underlying Price")
        undPrice = undPriceCalc.Value().Number()
        return 0.0 if math.isnan(undPrice) else undPrice
            
    def GenerateXValues(self):
        xAxisInstrument = None
        xValues = acm.FArray()
        for i in self.DealPackageInstruments():
            if i.InsType() == 'Option':
                #if i.Underlying().InsType() == 'Currency':
                #    pass
                #    # TODO: Handle FX options properly
                if not xAxisInstrument:
                    xAxisInstrument = i.Underlying()
                    xValues.Add(self.GetCurrentUnderlyingPrice(i))
                    xValues.AddAll(self.GetStrikeAndBarrierValues(i))
                elif i.Underlying().Originator() == xAxisInstrument.Originator():
                    xValues.AddAll(self.GetStrikeAndBarrierValues(i))
                else:
                    # TODO: Handle more than one underlying, make axis in %?
                    continue
        
        if not xAxisInstrument:
            self.DealPackageDefinition().Log().Warning('No underlying instrument for payoff graph found')
        else:
            xValues.Sort()
            # TODO, not hard code the upper and lower x values
            xValues.Add(xValues.Last() * 1.50)
            xValues.AtInsert(0, xValues.First() * 0.50)

        return xValues
        
