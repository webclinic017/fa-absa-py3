'''
Date                    : 2010-06-27
Purpose                 : theoretical model for randised futures. And shadow function to fix delta values on the futures/derivatives
Department and Desk     : Commodities
Requester               : Khunal Ramesar
Developer               : Rohan van der Walt
JIRA Ref                : ABITFA-776
CR Number               : 696347
'''

import acm

def theoreticalModelCallAgrisTheorPrice(cbotUnderlyingIns, agrisFX, agrisConvFactor, curr, valuationDate, marketSpotValue, instrument):

    #add instrument input on custon function, and extension value, so that I can shift the valuation date on the safex inst and see price effect. (hopefully not endless recursion)

    
    result = acm.FVariantDictionary()
    newResult = acm.DenominatedValue(0.0, curr, valuationDate)  #Default value in case simulation or calc fails
  
    calcSpace = acm.Calculations().CreateStandardCalculationsSpaceCollection()
    ins_calc = cbotUnderlyingIns.Calculation()
    cbotMarketPrice = ins_calc.MarketPrice(calcSpace, valuationDate)
       
    cbotQuotationFactor = cbotUnderlyingIns.Quotation().QuotationFactor()
    calcPrice = cbotMarketPrice.Number() * agrisFX * cbotQuotationFactor / agrisConvFactor
        
    newResult = acm.DenominatedValue(calcPrice, curr, valuationDate)
    result.AtPut("result", newResult)

    return result
    
def getTheorPrice( node, calc_space, column_id):
    if node.NumberOfChildren():
        child_iter = node.Iterator().FirstChild()
        return calc_space.CreateCalculation( child_iter.Tree(), column_id)
        
def agrisTheorShadowFunction(model, modelOutput, input, inputShift):
    
    shiftAmount = 1
    if input[5].Number() != inputShift[5].Number():
        shiftAmount = inputShift[5].Number() / input[5].Number()
        
    resultDict = model(*input)
    tempResult = resultDict['result']
    newResult = acm.DenominatedValue(tempResult.Number() * shiftAmount, tempResult.Unit(), tempResult.DateTime()) 
    
    if input[4] != inputShift[4]:
        calcSpace = acm.Calculations().CreateCalculationSpace( acm.GetDefaultContext(), 'FTradeSheet')
        node = calcSpace.InsertItem(input[6])
        prc = getTheorPrice(node, calcSpace, 'Price Theor')
        val1 = prc.Value().Number()
        calcSpace.SimulateGlobalValue('Valuation Date', inputShift[4])
        prc1 = getTheorPrice(node, calcSpace, 'Price Theor')
        val2 = prc1.Value().Number()
        calcSpace.RemoveGlobalSimulation('Valuation Date')
        thetaShift = val2 - val1
        newResult = acm.DenominatedValue(tempResult.Number() + thetaShift, tempResult.Unit(), inputShift[4]) 
    resultDict['result'] = newResult
    return resultDict

'''
ins = acm.FFuture['ZAR/CORN/SAFEX/DEC11']
calcSpace = acm.Calculations().CreateCalculationSpace( acm.GetDefaultContext(), 'FTradeSheet')
calcSpace.SimulateGlobalValue('Valuation Date', '2011-06-14')
top_node = calcSpace.InsertItem(ins)
print getTheorPrice( top_node, calcSpace, 'Price Theor').Value()
'''
