
from __future__ import print_function
import acm

ael_gui_parameters = {'hideExtraControls': False, 'windowCaption' : 'Calibrate Constant Price Spread Bid/Ask Vol'}
inspairHelp = 'Select the instrument pairs for which the mapped Bid/Ask volatility surfaces will be calibrated. The ATM vol will be read from the surface itself.'                      
ael_variables = [['instrumentPairs', 'Select Instrument Pairs', 'FInstrumentPair', acm.FInstrumentPair.Select(''), None, 1, 1, inspairHelp, None, True],
                ['setConstantBidAskVolSpread', 'Set Constant Ask Volatility When Failing To Calibrate Bid Volatility', 'bool', [True, False], True]]

#-----------------------------------------
calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
deltaConfig = acm.Sheet.Column().ConfigurationFromColumnParameterDefinitionNamesAndValues({"PriceGreekIncludeVolatilityMovement":False})

def GetVolatiltySurfaces(ins):
    volatilities = acm.GetCalculatedValueFromString(ins, acm.GetDefaultContext(), 'snoop(scenarioaxis(theoreticalPrice, <["alternativeContext"], , , ["Bid", "Ask"]>), "volatilityInformation", object)', acm.CreateEBTag()).Value()
    vola, bidAskVola = volatilities
    if not bidAskVola.IsKindOf('FArray'):
        raise ValueError('No bid/ask volatilty surfaces mapped for %s/%s' % (ins.Underlying().Name(), ins.StrikeCurrency().Name()))
    vola, volaBid, volaAsk = map(lambda vol:vol.VolatilityStructure(), [vola] + list(bidAskVola))
    if not volaAsk.IsKindOf('FMalzVolatilityStructure') and volaBid.IsKindOf('FMalzVolatilityStructure'):
        raise ValueError('Bid ask vola structures have to be malz structures')
    return vola, volaBid, volaAsk 


def GetSpreadSkew(volaSkews, skewDict, expiry):
    skew = skewDict.pop(expiry, None)
    if not skew:
        if set(skewDict) - set(volaSkews):
            skew = skewDict.pop((set(skewDict) - set(volaSkews))[0])
            skew.ExpiryPeriod(expiry)
        else:
            raise ValueError('More skews in mid surface than in spread surface. No %s skew.\nThis skew should be created.' % expiry)
    return skew
        

def GetSpread(ins, baseContext, spreadContext):
    contexts = ('"%s", "%s"' % (baseContext, spreadContext)).replace('"None"', 'nil')
    atmStrike, atmStrikeSpread = acm.GetCalculatedValueFromString(ins, acm.GetDefaultContext(), 'scenarioaxis(vannaVolgaAtmStrike, <["alternativeContext"], , , [%s]>)' % contexts, acm.CreateEBTag()).Value()
    calcSpace.SimulateValue(ins, 'Strike Price', atmStrikeSpread)
    calcSpace.SimulateValue(ins, "alternativeContext", spreadContext)
    atmSpreadPrice = calcSpace.CalculateValue(ins, 'Price Theor')
    if baseContext:
        calcSpace.SimulateValue(ins, "alternativeContext", baseContext)
    else:
        calcSpace.RemoveSimulation(ins, "alternativeContext")
    spread = atmSpreadPrice - calcSpace.CalculateValue(ins, 'Price Theor')
    calcSpace.RemoveSimulation(ins, "alternativeContext")
    return spread


def SolveStrikeForDelta(ins, delta, deltaColumn):
    maxIterations = 50
    precision = 0.0000001
    def SolveBlock(args, value):
        instrument = args['ins']
        calcSpace.SimulateValue(instrument, 'Strike Price', value)
        return calcSpace.CalculateValue(instrument, deltaColumn, deltaConfig).Value().Number()
    
    
    maxStrike = ins.StrikePrice() * 3
    minStrike = ins.StrikePrice() / 3
    if ins.IsCall() and ins.Currency().Name() == ins.Underlying().Name():
        #Delta vs strike for a premium adjusted call is bell shaped, need to find the solving boundaries
        #The strike should be a little smaller than it is for the non premium adjusted option
        insCopy = ins.Clone()
        insCopy.RegisterInStorage()
        insCopy.Currency = ins.StrikeCurrency()
        vola = calcSpace.CalculateValue(ins, 'Portfolio Volatility')
        calcSpace.SimulateValue(insCopy, 'Portfolio Volatility', vola * 100)
        maxStrike = acm.Math.Solve(SolveBlock, {'ins':insCopy}, delta, minStrike, maxStrike, 0.001, maxIterations)
        deltaBound = SolveBlock({'ins':ins}, maxStrike)
        #maxStrike should always be greater than the strike we're looking for. Something goes wrong when it isn't. The result is good enough so let it be for now.
        minStrike = maxStrike * (0.9 if deltaBound < delta else 1.1)
        
    return acm.Math.Solve(SolveBlock, {'ins':ins}, delta, minStrike, maxStrike, precision, maxIterations)

def SolveVolaForPrice(ins, theor):
    maxIterations = 50
    precision = 0.0000001
    def SolveBlock(args, value):
        calcSpace.SimulateValue(ins, 'Portfolio Volatility', value)
        return calcSpace.CalculateValue(ins, 'Price Theor').Value().Number()
    
    return acm.Math.Solve(SolveBlock, None, theor, 0, 100, precision, maxIterations) * 0.01


def SolveVolatility(ins, priceSpread, deltaValue, deltaColumn = 'Instrument Delta'):
    maxIterations = 100
    precision = 0.0000001
    previousDelta = None
    for i in range(maxIterations):
        strike = SolveStrikeForDelta(ins, deltaValue, deltaColumn)
        if not acm.Math.IsFinite(strike):
        
            print ('ERROR - Failed to find strike that gives a delta of %f' % deltaValue)
            #acm.StartApplication('Valuation Viewer', calcSpace.CreateCalculation(ins, 'Price Theor'))
            return None
        calcSpace.RemoveSimulation(ins, 'Portfolio Volatility')
        price = calcSpace.CalculateValue(ins, 'Price Theor').Value()
        vola = SolveVolaForPrice(ins, price + priceSpread)
        if not acm.Math.IsFinite(vola):
            print ('ERROR - Failed to find volatility that gives a theoretical value of %f for delta %f with expiry %s' % (price + priceSpread, deltaValue, ins.ExpiryDateOnly()))
            #acm.StartApplication('Valuation Viewer', calcSpace.CreateCalculation(ins, 'Price Theor'))
            return None
        delta = calcSpace.CalculateValue(ins, deltaColumn, deltaConfig).Value().Number()
        if abs(delta - deltaValue) < precision:
            #print ('SOLVED!!!!', vola, calcSpace.CalculateValue(ins, 'Price Theor').Value(), calcSpace.CalculateValue(ins, 'Price Theor').Value() - price, delta, strike)
            return vola
        elif previousDelta == delta:
            #Same value as in previous iteration, stop
            break
        previousDelta = delta
        
    if abs(delta - deltaValue) < precision * 1000:
        #print ('GOOD enough', vola, calcSpace.CalculateValue(ins, 'Price Theor').Value(), calcSpace.CalculateValue(ins, 'Price Theor').Value() - price, delta, strike)
        return vola
    print ('No solution!!!!', vola, calcSpace.CalculateValue(ins, 'Price Theor').Value() - price, delta, ins.ExpiryDateOnly(), deltaValue, priceSpread)
    

def CalibrateSkew(dp, baseContext, spreadContext, spreadSkew):
    if dp.GetAttributeMetaData('foreignOptionType', 'Label')() != 'Call':
        dp.GetAttribute('foreignOptionType')()
    ins = dp.Instruments().First().Instrument()
    priceSpread = GetSpread(ins, baseContext, spreadContext)
    if baseContext:
        calcSpace.SimulateValue(ins, "alternativeContext", baseContext)
    deltaColumn = 'Instrument Forward Delta' if spreadSkew.DeltaType() == 'Forward' else 'Instrument Delta'
    atmVol = spreadSkew.A1()
    vol40Call = SolveVolatility(ins, priceSpread, 0.40, deltaColumn) or atmVol
    vol25Call = SolveVolatility(ins, priceSpread, 0.25, deltaColumn) or vol40Call
    vol10Call = SolveVolatility(ins, priceSpread, 0.10, deltaColumn) or vol25Call
    dp.GetAttribute('foreignOptionType')()
    vol40Put = SolveVolatility(ins, priceSpread, -0.40, deltaColumn) or atmVol
    vol25Put = SolveVolatility(ins, priceSpread, -0.25, deltaColumn) or vol40Put
    vol10Put = SolveVolatility(ins, priceSpread, -0.10, deltaColumn) or vol25Put
    calcSpace.RemoveSimulation(ins, "alternativeContext")
    leftCutoff = -0.1
    rightCutoff = 0.1
    return spreadSkew, [atmVol, vol40Call, vol25Call, vol10Call, vol40Put, vol25Put, vol10Put, leftCutoff, rightCutoff]


def SetConstantBidAskVolSpread(volaBid, volaAsk):
    calls = ['A1', 'A2', 'A3', 'A4']
    puts =  ['A1', 'A5', 'A6', 'A7']
    
    nameDict = {'A1':'ATM',
                'A2':'40C',
                'A3':'25C',
                'A4':'10C',
                'A5':'40P',
                'A6':'25P',
                'A7':'10P'}
    
    askSkews = dict((s.ExpiryPeriod(), s) for s in volaAsk.Skews())
    for skew in volaBid.Skews():
        for params in (calls, puts):
            for p1, p2 in zip(params[:-1], params[1:]):
                if getattr(skew, p1)() == getattr(skew, p2)():
                    askSkew = askSkews[skew.ExpiryPeriod()]
                    vol = getattr(askSkew, p1)()
                    setattr(askSkew, p2, vol)
                    print ("Setting %s Vol to %s Vol (%f) on %s %s skew." % (nameDict[p2], nameDict[p1], vol, volaAsk.Name(), skew.ExpiryPeriod()))
    volaAsk.Commit()



def ael_main(params):
    global calcSpace
    for insPair in params['instrumentPairs']:
        print ("Calibrating %s bid/ask surfaces..." % insPair.Name())
        if insPair.IsKindOf('FCurrencyPair'):
            dp = acm.DealPackage.NewAsDecorator('FX Option')
        else:
            dp = acm.DealPackage.NewAsDecorator('PM Option')
        dp.SetAttribute('instrumentPair', insPair.Name())
        ins = dp.Instruments().First().Instrument()
        try:
            vola, volaBid, volaAsk = GetVolatiltySurfaces(ins)
        except ValueError as e:
            print (e)
            continue

        volaBid.ButterflyQuote('None')
        volaAsk.ButterflyQuote('None')

        if vola.DeltaTerm() == "Pct of foreign":
            dp.SetAttribute('premiumCurrency', dp.GetAttribute('foreignInstrument'))

        volaSkews = dict((s.ExpiryPeriod(), s) for s in vola.Skews())
        for spreadVola, (spreadContext, baseContext) in ((volaAsk, ("Ask", None)), (volaBid, ("Bid", "Ask"))):
            calibratedSkews = []
            spreadSkews = dict((s.ExpiryPeriod(), s) for s in spreadVola.Skews())
            for expiry in volaSkews:
                dp.SetAttribute('expiryDate', expiry)
                calcSpace = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FDealSheet')
                spreadSkew = GetSpreadSkew(volaSkews, spreadSkews, expiry)
                calibratedSkews.append(CalibrateSkew(dp, baseContext, spreadContext, spreadSkew))

            for expiry, skew in spreadSkews.items():
                raise ValueError('More skews in spread surface than in mid surface.\nThe %s skew in %s should be deleted' % (expiry, skew.Structure().Name()))

            for skew, values in calibratedSkews:
                #print ('Setting values', skew.Structure().Name(), skew.ExpiryPeriod(), values)
                skew.SkewInputType('Option Quotes')
                skew.NumberOfInterpolationPoints(7)
                skew.SetMalzOptionQuotes(*values)
            
            
            spreadVola.Commit()
            
        if params['setConstantBidAskVolSpread']:
            SetConstantBidAskVolSpread(volaBid, volaAsk)
        
        print ("Finished calibrating %s bid/ask surfaces." % insPair.Name())
        print (" ")
        print ("#"*80)
